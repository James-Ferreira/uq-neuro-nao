import os, time, json, urllib2, threading

from src_py2.integrations.voice_job import NaoJobConsumer
from src_py2.robot.nao_robot import NAORobot
from src_py2.robot.conversation_manager import ConversationManager
from config.project_loader import load_active_project_profile, get_nested

# --- Machine-agnostic sessions root (derive from repo structure) ---
def default_sessions_root():
    # this file: .../repos/uq-neuro-nao/src_py2/main/run_chat_with_bumper.py
    here = os.path.dirname(os.path.abspath(__file__))
    
    # go up: src_py2/main -> src_py2 -> uq-neuro-nao
    uq_repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    
    # parent folder that contains both repos (e.g., .../repos)
    repos_parent = os.path.dirname(uq_repo_root)
    
    # .../repos/voice-llm-chat/sessions
    return os.path.join(repos_parent, "voice-llm-chat", "sessions")

PROJECT_PROFILE = load_active_project_profile()
NAO_WORKER_CFG = PROJECT_PROFILE.get("nao_worker", {})
SESSIONS_ROOT = get_nested(NAO_WORKER_CFG, ["sessions_root"], default_sessions_root())

CURRENT_SESSION_FILENAME = "CURRENT_SESSION.txt"

BRIDGE = get_nested(NAO_WORKER_CFG, ["bridge_url"], "http://127.0.0.1:5055")
BRIDGE_START_TIMEOUT_SEC = float(get_nested(NAO_WORKER_CFG, ["bridge_start_timeout_sec"], 10.0))
BRIDGE_STOP_TIMEOUT_SEC = float(get_nested(NAO_WORKER_CFG, ["bridge_stop_timeout_sec"], 120.0))
BUMPER_RELEASE_TIMEOUT_SEC = float(
    get_nested(NAO_WORKER_CFG, ["bumper_release_timeout_sec"], 15.0)
)
ROBOT_NAME = get_nested(NAO_WORKER_CFG, ["robot_name"], "clas")
ROBOT_USERNAME = get_nested(NAO_WORKER_CFG, ["robot_username"], "nao")
ROBOT_PASSWORD = get_nested(NAO_WORKER_CFG, ["robot_password"], "nao")
CONSUMER_MODEL = get_nested(NAO_WORKER_CFG, ["consumer_model"], "gesturizer4")
CONSUMER_INTERLOCUTOR = get_nested(NAO_WORKER_CFG, ["consumer_interlocutor"], None)
CONSUMER_INCLUDE_SEGMENTS = bool(get_nested(NAO_WORKER_CFG, ["include_segments"], False))
CONSUMER_SPECIAL_COMMANDS = get_nested(NAO_WORKER_CFG, ["special_commands"], None)
CONSUMER_REQUIRE_ENTER_BEFORE_SPEAK = get_nested(
    NAO_WORKER_CFG, ["require_enter_before_speak"], False
)
CONSUMER_REQUIRE_ENTER_FOR_WATCHDOG = get_nested(
    NAO_WORKER_CFG, ["require_enter_for_watchdog"], False
)
WATCHDOG_CFG = get_nested(PROJECT_PROFILE, ["conversation", "watchdog"], {})
SESSION_END_CFG = get_nested(PROJECT_PROFILE, ["conversation", "session_end"], {})
VERBOSE = os.getenv("NAO_WORKER_VERBOSE", "0") == "1"


def vprint(msg):
    if VERBOSE:
        print(msg)

def log_diag(message):
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print("[BUMPER {}] {}".format(stamp, message))

def _one_line_text(s):
    txt = (s or "").strip()
    if not txt:
        return "(no speech detected)"
    return " ".join(txt.split())

def post_json(url, payload=None, timeout=10):
    data = json.dumps(payload or {}).encode("utf-8")
    req = urllib2.Request(url, data, {"Content-Type": "application/json"})
    resp = urllib2.urlopen(req, timeout=timeout)
    return json.loads(resp.read())

def read_current_session_dir(sessions_root):
    pointer_path = os.path.join(sessions_root, CURRENT_SESSION_FILENAME)
    if not os.path.isfile(pointer_path):
        return None
    try:
        with open(pointer_path, "r") as f:
            s = f.read().strip()
        return s if s else None
    except Exception:
        return None

def wait_for_current_session(sessions_root, poll_sec=0.25):
    print("Waiting for CURRENT_SESSION.txt in: {}".format(sessions_root))
    while True:
        session_dir = read_current_session_dir(sessions_root)
        if session_dir:
            outbox_dir = os.path.join(session_dir, "robot_outbox")
            if os.path.isdir(outbox_dir):
                print("Using session: {}".format(session_dir))
                return session_dir
        time.sleep(poll_sec)

def _release_turn_gate(convo, reason):
    convo.turn_in_progress = False
    if hasattr(convo, "turn_gate") and convo.turn_gate.locked():
        try:
            convo.turn_gate.release()
        except Exception:
            pass
    try:
        convo.set_ready_mode()
    except Exception as e:
        vprint("WARN: set_ready_mode failed ({}): {}".format(reason, e))

def bumper_loop(robot, convo, consumer):
    while True:
        log_diag("Awaiting next bumper press")
        robot.tm.wait_for_left_bumper_press()
        hold_started_at = time.time()
        log_diag("Bumper press accepted by worker loop")

        # Busy: consume press->release but do nothing
        if not convo.turn_gate.acquire(False):
            vprint("BUSY: ignoring bumper press (turn in progress)")
            released = robot.tm.wait_for_left_bumper_release(BUMPER_RELEASE_TIMEOUT_SEC)
            if not released:
                log_diag(
                    "WARN: Timed out waiting {:.1f}s for ignored bumper release; "
                    "refreshing touch subscriptions.".format(BUMPER_RELEASE_TIMEOUT_SEC)
                )
                try:
                    robot.tm.reset_hold_state()
                    robot.tm.refresh_event_subscriptions()
                except Exception as touch_error:
                    log_diag("WARN: Failed to refresh touch subscriptions: {}".format(touch_error))
            else:
                log_diag(
                    "Ignored bumper press released after {:.3f}s".format(
                        max(0.0, time.time() - hold_started_at)
                    )
                )
            time.sleep(0.05)
            continue

        convo.turn_in_progress = True

        try:
            # LISTENING (held down)
            try:
                convo.set_listening_mode()  # e.g., yellow
            except Exception as e:
                vprint("WARN: set_listening_mode failed: {}".format(e))

            log_diag("Starting bridge recording")
            post_json(BRIDGE + "/start", timeout=BRIDGE_START_TIMEOUT_SEC)
            consumer.note_input_attempt_started()
            log_diag("Bridge recording started")

            released = robot.tm.wait_for_left_bumper_release(BUMPER_RELEASE_TIMEOUT_SEC)
            if not released:
                log_diag(
                    "ERROR: Timed out waiting {:.1f}s for left bumper release. "
                    "Resetting listening state.".format(BUMPER_RELEASE_TIMEOUT_SEC)
                )
                try:
                    log_diag("Attempting bridge stop after missing release")
                    stop_resp = post_json(BRIDGE + "/stop", timeout=BRIDGE_STOP_TIMEOUT_SEC)
                    log_diag(
                        "Recovered after missing bumper release; hold_duration_sec={:.3f}; "
                        "captured transcript: {}".format(
                            max(0.0, time.time() - hold_started_at),
                            _one_line_text(stop_resp.get("transcript", ""))
                        )
                    )
                except Exception as stop_error:
                    log_diag("WARN: Failed to stop bridge after bumper release timeout: {}".format(stop_error))
                consumer.note_input_attempt_finished()
                try:
                    robot.tm.reset_hold_state()
                    robot.tm.refresh_event_subscriptions()
                except Exception as touch_error:
                    log_diag("WARN: Failed to refresh touch subscriptions: {}".format(touch_error))
                _release_turn_gate(convo, "bumper_release_timeout")
                time.sleep(0.2)
                continue

            log_diag(
                "Bumper release received after {:.3f}s; stopping bridge recording".format(
                    max(0.0, time.time() - hold_started_at)
                )
            )

            # BUSY (processing/speaking)
            try:
                convo.set_busy_mode()  # blue
            except Exception as e:
                vprint("WARN: set_busy_mode failed: {}".format(e))

            bridge_stop_started_at = time.time()
            stop_resp = post_json(BRIDGE + "/stop", timeout=BRIDGE_STOP_TIMEOUT_SEC)
            consumer.note_input_attempt_finished()
            log_diag(
                "Bridge stop returned after {:.3f}s".format(
                    max(0.0, time.time() - bridge_stop_started_at)
                )
            )
            turn_id = stop_resp.get("turn_id")
            raw_transcript = stop_resp.get("transcript", "")
            transcript = _one_line_text(raw_transcript)
            print("Turn {} | Participant: {}".format(turn_id, transcript))
            log_diag(
                "Turn {} transcript captured; nonempty={}".format(
                    turn_id, bool(str(raw_transcript or "").strip())
                )
            )

            # If no usable speech was captured, no downstream robot reply may occur.
            # Release the turn gate here to avoid a deadlock waiting for speak_n_gest_next_level().
            if (not turn_id) or (not str(raw_transcript or "").strip()):
                log_diag("No valid user utterance captured; releasing turn gate.")
                _release_turn_gate(convo, "empty_or_missing_transcript")
                time.sleep(0.05)
                continue

            vprint("TURN CAPTURED: waiting for robot to finish reply before accepting another")

            # IMPORTANT: do not release gate here.
            # speak_n_gest_next_level() releases it in finally.

        except Exception as e:
            consumer.note_input_attempt_finished()
            log_diag("ERROR in bumper_loop: {}".format(e))
            _release_turn_gate(convo, "bumper_loop_exception")
            time.sleep(0.2)
            continue

        time.sleep(0.05)

def main():
    print("Active project profile: {}".format(PROJECT_PROFILE.get("_project_id")))
    session_dir = wait_for_current_session(SESSIONS_ROOT)

    robot = NAORobot(ROBOT_NAME, usrnme=ROBOT_USERNAME, pword=ROBOT_PASSWORD)
    robot.mm.sit()
    robot.mm.repose(False)

    convo = ConversationManager(robot)

    consumer = NaoJobConsumer(
        convo,
        model=CONSUMER_MODEL,
        interlocutor=CONSUMER_INTERLOCUTOR,
        include_segments=CONSUMER_INCLUDE_SEGMENTS,
        special_commands=CONSUMER_SPECIAL_COMMANDS,
        watchdog_cfg=WATCHDOG_CFG,
        session_end_cfg=SESSION_END_CFG,
        require_enter_before_speak=CONSUMER_REQUIRE_ENTER_BEFORE_SPEAK,
        require_enter_for_watchdog=CONSUMER_REQUIRE_ENTER_FOR_WATCHDOG,
    )

    t = threading.Thread(target=bumper_loop, args=(robot, convo, consumer))
    t.daemon = True
    t.start()

    consumer.run_job_worker(session_dir)

if __name__ == "__main__":
    main()
