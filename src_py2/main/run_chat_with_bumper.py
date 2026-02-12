import os, time, json, urllib2, threading

from src_py2.integrations.voice_job import NaoJobConsumer
from src_py2.robot.nao_robot import NAORobot
from src_py2.robot.conversation_manager import ConversationManager

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

SESSIONS_ROOT = default_sessions_root()

CURRENT_SESSION_FILENAME = "CURRENT_SESSION.txt"

BRIDGE = "http://127.0.0.1:5055"

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

def bumper_loop(robot, convo):
    while True:
        robot.tm.wait_for_left_bumper_press()

        # Busy: consume press->release but do nothing
        if not convo.turn_gate.acquire(False):
            print("BUSY: ignoring bumper press (turn in progress)")
            robot.tm.wait_for_left_bumper_release()
            time.sleep(0.05)
            continue

        convo.turn_in_progress = True

        try:
            # LISTENING (held down)
            try:
                convo.set_listening_mode()  # e.g., yellow
            except Exception as e:
                print("WARN: set_listening_mode failed: {}".format(e))

            post_json(BRIDGE + "/start")

            robot.tm.wait_for_left_bumper_release()

            # BUSY (processing/speaking)
            try:
                convo.set_busy_mode()  # blue
            except Exception as e:
                print("WARN: set_busy_mode failed: {}".format(e))

            post_json(BRIDGE + "/stop")

            print("TURN CAPTURED: waiting for robot to finish reply before accepting another")

            # IMPORTANT: do not release gate here.
            # speak_n_gest_next_level() releases it in finally.

        except Exception as e:
            print("ERROR in bumper_loop: {}".format(e))
            convo.turn_in_progress = False
            try:
                convo.turn_gate.release()
            except Exception:
                pass
            raise

        time.sleep(0.05)

def main():
    session_dir = wait_for_current_session(SESSIONS_ROOT)

    robot = NAORobot("clas")
    robot.mm.sit(post=True)

    convo = ConversationManager(robot)
    convo.set_ready_mode()

    consumer = NaoJobConsumer(convo, model="gesturizer2:latest", interlocutor="Dude", include_segments=False)

    t = threading.Thread(target=bumper_loop, args=(robot, convo))
    t.daemon = True
    t.start()

    consumer.run_job_worker(session_dir)

if __name__ == "__main__":
    main()
