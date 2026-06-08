import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from integrations import voice_job


class _DummyGate(object):
    def locked(self):
        return False

    def release(self):
        return None

    def acquire(self, blocking):
        return True


class _DummyConvo(object):
    def __init__(self):
        self.turn_gate = _DummyGate()
        self.turn_in_progress = False
        self.spoken_segments = []
        self.robot = type("DummyRobot", (object,), {"disable_motion_for_chat": True})()

    def set_ready_mode(self):
        return None

    def speak_n_gest_next_level(self, segments_list, leds=True):
        self.spoken_segments.append(segments_list)


class TestVoiceJob(unittest.TestCase):
    def setUp(self):
        self._orig_reply = voice_job.transcribe.reply
        self._orig_sleep = voice_job.time.sleep

    def tearDown(self):
        setattr(voice_job.transcribe, "reply", self._orig_reply)
        setattr(voice_job.time, "sleep", self._orig_sleep)
        if hasattr(voice_job, "raw_input"):
            delattr(voice_job, "raw_input")  # type: ignore[attr-defined]

    def test_watchdog_enter_gate_is_independent_from_turn_reply_gate(self):
        convo = _DummyConvo()
        consumer = voice_job.NaoJobConsumer(
            convo,
            require_enter_before_speak=False,
            require_enter_for_watchdog=True,
        )

        prompts = []

        def _fake_raw_input(prompt):
            prompts.append(prompt)
            return ""

        voice_job.raw_input = _fake_raw_input  # type: ignore[attr-defined]

        consumer._wait_for_operator_enter("turn_reply")
        self.assertEqual(prompts, [])

        consumer._wait_for_operator_enter("watchdog")
        self.assertEqual(len(prompts), 1)
        self.assertIn("watchdog", prompts[0])

    def test_turn_reply_gate_can_auto_release_with_typing_delay(self):
        convo = _DummyConvo()
        consumer = voice_job.NaoJobConsumer(
            convo,
            require_enter_before_speak=True,
            require_enter_for_watchdog=True,
            operator_reply_delay_cfg={
                "enabled": True,
                "characters_per_minute": 120.0,
                "min_sec": 1.0,
                "max_sec": 10.0,
            },
        )

        prompts = []
        sleeps = []

        def _fake_raw_input(prompt):
            prompts.append(prompt)
            return ""

        def _fake_sleep(delay_sec):
            sleeps.append(delay_sec)

        voice_job.raw_input = _fake_raw_input  # type: ignore[attr-defined]
        setattr(voice_job.time, "sleep", _fake_sleep)

        consumer._wait_for_operator_enter("turn_reply", "hello")
        self.assertEqual(prompts, [])
        self.assertEqual(sleeps, [2.5])

        consumer._wait_for_operator_enter("watchdog", "hello")
        self.assertEqual(len(prompts), 1)
        self.assertIn("watchdog", prompts[0])
        self.assertEqual(sleeps, [2.5])

    def test_empty_turn_does_not_advance_logical_turn_count(self):
        convo = _DummyConvo()
        consumer = voice_job.NaoJobConsumer(
            convo,
            watchdog_cfg={
                "enabled": True,
                "activate_after_turn": 2,
                "interval_sec": 13.0,
            },
        )
        consumer._robot_stiffened_for_speech = True

        seen_turn_counts = []

        def _fake_reply(transcript, model, interlocutor, type_, turn_count, prompt=None, history=None, watchdog_mode=False, ephemeral_system=None):
            seen_turn_counts.append(turn_count)
            return [["Test reply", None, None, 1.0]]

        setattr(voice_job.transcribe, "reply", _fake_reply)

        empty_result = consumer.handle_input_job({
            "turn_id": 1,
            "user": "",
            "recording_started_at": "2026-04-01T10:00:00",
        })
        self.assertEqual(consumer.turn_count, 0)
        self.assertEqual(empty_result["ai"], "")
        self.assertEqual(seen_turn_counts, [])

        first_real_result = consumer.handle_input_job({
            "turn_id": 2,
            "user": "Hi Zeke, I am ready now.",
            "recording_started_at": "2026-04-01T10:00:05",
        })
        self.assertEqual(seen_turn_counts, [1])
        self.assertEqual(consumer.turn_count, 1)
        self.assertIsNone(consumer._watchdog_due_mono)
        self.assertEqual(first_real_result["ai"], "Test reply")

        second_real_result = consumer.handle_input_job({
            "turn_id": 3,
            "user": "Tell me about the lab",
            "recording_started_at": "2026-04-01T10:00:10",
        })
        self.assertEqual(seen_turn_counts, [1, 2])
        self.assertEqual(consumer.turn_count, 2)
        self.assertIsNotNone(consumer._watchdog_due_mono)
        self.assertEqual(second_real_result["ai"], "Test reply")

    def test_rewrite_session_dialogue_skips_fully_empty_turn_pairs(self):
        session_dir = tempfile.mkdtemp(prefix="voice_job_test_")
        try:
            inbox_dir = os.path.join(session_dir, "robot_inbox")
            outbox_dir = os.path.join(session_dir, "robot_outbox")
            os.makedirs(inbox_dir)
            os.makedirs(outbox_dir)

            with open(os.path.join(inbox_dir, "turn_0001_input.json"), "w") as f:
                json.dump({"turn_id": 1, "user": ""}, f)
            with open(os.path.join(outbox_dir, "turn_0001_output.json"), "w") as f:
                json.dump({"turn_id": 1, "ai": ""}, f)

            with open(os.path.join(inbox_dir, "turn_0002_input.json"), "w") as f:
                json.dump({"turn_id": 2, "user": "Hello"}, f)
            with open(os.path.join(outbox_dir, "turn_0002_output.json"), "w") as f:
                json.dump({"turn_id": 2, "ai": "Hi there"}, f)

            voice_job._rewrite_session_dialogue(session_dir)

            dialogue_path = os.path.join(session_dir, "session_dialogue.txt")
            with open(dialogue_path, "r") as f:
                dialogue_text = f.read()

            self.assertNotIn('turn_1 user: ""', dialogue_text)
            self.assertNotIn('turn_1 robot: ""', dialogue_text)
            self.assertIn('turn_2 user: "Hello"', dialogue_text)
            self.assertIn('turn_2 robot: "Hi there"', dialogue_text)
        finally:
            shutil.rmtree(session_dir)

    def test_language_metrics_include_robot_word_stats(self):
        session_dir = tempfile.mkdtemp(prefix="voice_job_metrics_")
        try:
            inbox_dir = os.path.join(session_dir, "robot_inbox")
            outbox_dir = os.path.join(session_dir, "robot_outbox")
            os.makedirs(inbox_dir)
            os.makedirs(outbox_dir)

            with open(os.path.join(inbox_dir, "turn_0001_input.json"), "w") as f:
                json.dump({"turn_id": 1, "user": "Hello there", "participant_duration_sec": 2.0}, f)
            with open(os.path.join(outbox_dir, "turn_0001_output.json"), "w") as f:
                json.dump({"turn_id": 1, "ai": "Hi there friend", "ai_duration_sec": 1.5, "latency_sec": 0.4}, f)

            with open(os.path.join(inbox_dir, "turn_0002_input.json"), "w") as f:
                json.dump({"turn_id": 2, "user": "How are you doing today", "participant_duration_sec": 4.0}, f)
            with open(os.path.join(outbox_dir, "turn_0002_output.json"), "w") as f:
                json.dump({"turn_id": 2, "ai": "I am doing well today thanks", "ai_duration_sec": 2.5, "latency_sec": 0.6}, f)

            with open(os.path.join(inbox_dir, "turn_0003_input.json"), "w") as f:
                json.dump({"turn_id": 3, "user": "Go back to sleep", "participant_duration_sec": 2.0}, f)
            with open(os.path.join(outbox_dir, "turn_0003_output.json"), "w") as f:
                json.dump({
                    "turn_id": 3,
                    "ai": "Going to sleep now",
                    "ai_duration_sec": 1.5,
                    "latency_sec": 0.2,
                    "special_command": "gotosleeplittlerobot",
                }, f)

            voice_job._write_language_metrics_summary(session_dir)

            with open(os.path.join(session_dir, "session_language_metrics.json"), "r") as f:
                summary = json.load(f)

            self.assertEqual(summary["total_words"], 7)
            self.assertEqual(summary["spoken_turn_count"], 2)
            self.assertEqual(summary["robot_total_words"], 9)
            self.assertEqual(summary["robot_spoken_turn_count"], 2)
            self.assertEqual(summary["mean_words_per_turn"], 3.5)
            self.assertEqual(summary["robot_mean_words_per_turn"], 4.5)
            self.assertEqual(summary["word_rate_wps"], 7.0 / 6.0)
            self.assertEqual(summary["robot_word_rate_wps"], 9.0 / 4.0)
            self.assertEqual(summary["mean_latency_sec"], 0.5)
        finally:
            shutil.rmtree(session_dir)


if __name__ == "__main__":
    unittest.main()
