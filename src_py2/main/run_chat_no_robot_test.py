import json, threading, time

from src_py2.integrations.voice_job import NaoJobConsumer
from src_py2.main import run_chat_with_bumper as bumper


def _segments_to_text(segments_list):
    parts = []
    for segment in segments_list or []:
        try:
            text = segment[0]
        except Exception:
            text = None
        if text:
            parts.append(str(text))
    return " ".join(parts).strip()


class TerminalConversationManager(object):
    def __init__(self):
        self.robot = type("TerminalRobot", (object,), {"disable_motion_for_chat": True})()
        self.turn_gate = threading.Lock()
        self.turn_in_progress = False

    def set_ready_mode(self):
        print("[no_robot_test] READY")

    def set_listening_mode(self):
        print("[no_robot_test] LISTENING")

    def set_busy_mode(self):
        print("[no_robot_test] BUSY")

    def speak_n_gest_next_level(self, segments_list, leds=True):
        try:
            text = _segments_to_text(segments_list)
            print("\n[no_robot_test] Robot reply: {}".format(text or "(empty reply)"))
            if bumper.CONSUMER_INCLUDE_SEGMENTS:
                print("[no_robot_test] Segments: {}".format(json.dumps(segments_list)))
        finally:
            self.turn_in_progress = False
            if self.turn_gate.locked():
                try:
                    self.turn_gate.release()
                except Exception:
                    pass
            if leds:
                self.set_ready_mode()


def terminal_recording_loop(convo, consumer):
    print("No-robot test mode: press Enter to start recording, then Enter again to stop.")
    while True:
        try:
            raw_input("\nPress Enter to START recording, or Ctrl-C to exit... ")  # type: ignore
        except KeyboardInterrupt:
            print("\nNo-robot test input loop exiting.")
            return
        except EOFError:
            print("\nstdin closed; no-robot test input loop exiting.")
            return

        started_at = time.time()
        if not convo.turn_gate.acquire(False):
            print("[no_robot_test] Busy: turn already in progress.")
            time.sleep(0.05)
            continue

        convo.turn_in_progress = True

        try:
            convo.set_listening_mode()
            bumper.log_diag("Starting bridge recording")
            bumper.post_json(
                bumper.BRIDGE + "/start",
                timeout=bumper.BRIDGE_START_TIMEOUT_SEC,
            )
            consumer.note_input_attempt_started()
            bumper.log_diag("Bridge recording started")

            try:
                raw_input("Recording from microphone. Press Enter to STOP... ")  # type: ignore
            except KeyboardInterrupt:
                print("\nStopping current recording before exit.")

            convo.set_busy_mode()
            stop_started_at = time.time()
            stop_resp = bumper.post_json(
                bumper.BRIDGE + "/stop",
                timeout=bumper.BRIDGE_STOP_TIMEOUT_SEC,
            )
            consumer.note_input_attempt_finished()
            bumper.log_diag(
                "Bridge stop returned after {:.3f}s".format(
                    max(0.0, time.time() - stop_started_at)
                )
            )

            turn_id = stop_resp.get("turn_id")
            raw_transcript = stop_resp.get("transcript", "")
            print("Turn {} | Participant: {}".format(
                turn_id,
                bumper._one_line_text(raw_transcript),
            ))
            bumper.log_diag(
                "Turn {} transcript captured after {:.3f}s; nonempty={}".format(
                    turn_id,
                    max(0.0, time.time() - started_at),
                    bool(str(raw_transcript or "").strip()),
                )
            )

            if (not turn_id) or (not str(raw_transcript or "").strip()):
                bumper.log_diag("No valid user utterance captured; releasing turn gate.")
                bumper._release_turn_gate(convo, "empty_or_missing_transcript")
                time.sleep(0.05)
                continue

        except Exception as e:
            consumer.note_input_attempt_finished()
            bumper.log_diag("ERROR in terminal_recording_loop: {}".format(e))
            bumper._release_turn_gate(convo, "terminal_loop_exception")
            time.sleep(0.2)
            continue

        time.sleep(0.05)


def main():
    print("Active project profile: {}".format(bumper.PROJECT_PROFILE.get("_project_id")))
    print("No-robot test mode enabled; NAO connection and bumper input are bypassed.")
    session_dir = bumper.wait_for_current_session(bumper.SESSIONS_ROOT)
    condition = bumper._prompt_contingency_condition()
    non_contingent_fixed_replies = {}
    if condition == "non-contingent":
        non_contingent_fixed_replies = bumper._load_non_contingent_fixed_replies()

    convo = TerminalConversationManager()
    consumer = NaoJobConsumer(
        convo,
        model=bumper.CONSUMER_MODEL,
        interlocutor=bumper.CONSUMER_INTERLOCUTOR,
        include_segments=bumper.CONSUMER_INCLUDE_SEGMENTS,
        special_commands=bumper.CONSUMER_SPECIAL_COMMANDS,
        watchdog_cfg=bumper.WATCHDOG_CFG,
        session_end_cfg=bumper.SESSION_END_CFG,
        require_enter_before_speak=bumper.CONSUMER_REQUIRE_ENTER_BEFORE_SPEAK,
        require_enter_for_watchdog=bumper.CONSUMER_REQUIRE_ENTER_FOR_WATCHDOG,
        operator_reply_delay_cfg=bumper.CONSUMER_OPERATOR_REPLY_DELAY_CFG,
        fixed_reply_delay_cfg=bumper.CONSUMER_FIXED_REPLY_DELAY_CFG,
        contingency_condition=condition,
        non_contingent_fixed_replies=non_contingent_fixed_replies,
    )

    t = threading.Thread(target=terminal_recording_loop, args=(convo, consumer))
    t.daemon = True
    t.start()

    consumer.run_job_worker(session_dir)


if __name__ == "__main__":
    main()
