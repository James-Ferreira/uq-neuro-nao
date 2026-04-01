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
        self.robot = None

    def set_ready_mode(self):
        return None

    def speak_n_gest_next_level(self, segments_list, leds=True):
        self.spoken_segments.append(segments_list)


class TestVoiceJob(unittest.TestCase):
    def setUp(self):
        self._orig_reply = voice_job.transcribe.reply

    def tearDown(self):
        voice_job.transcribe.reply = self._orig_reply

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

        seen_turn_counts = []

        def _fake_reply(transcript, model, interlocutor, type_, turn_count, prompt=None, history=None, watchdog_mode=False, ephemeral_system=None):
            seen_turn_counts.append(turn_count)
            return [["Test reply", None, None, 1.0]]

        voice_job.transcribe.reply = _fake_reply

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
            "user": "Hi, Zeke. No, we're not ready yet. Go back to sleep.",
            "recording_started_at": "2026-04-01T10:00:05",
        })
        self.assertEqual(seen_turn_counts, [1])
        self.assertEqual(consumer.turn_count, 1)
        self.assertIsNone(consumer._watchdog_due_mono)
        self.assertEqual(first_real_result["ai"], "Test reply")

        second_real_result = consumer.handle_input_job({
            "turn_id": 3,
            "user": "Go back to sleep",
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


if __name__ == "__main__":
    unittest.main()
