import os
import time

from src_py2.integrations.voice_job import NaoJobConsumer
from src_py2.robot.nao_robot import NAORobot
from src_py2.robot.conversation_manager import ConversationManager


# Set this once to the sessions/ folder inside voice-llm-chat
SESSIONS_ROOT = "/Users/neurorobots/Desktop/repos/voice-llm-chat/sessions"
CURRENT_SESSION_FILENAME = "CURRENT_SESSION.txt"


def read_current_session_dir(sessions_root):
    """
    Reads sessions/CURRENT_SESSION.txt written by voice-llm-chat and returns the session_dir path.
    Returns None if the pointer file doesn't exist yet or is empty.
    """
    pointer_path = os.path.join(sessions_root, CURRENT_SESSION_FILENAME)
    if not os.path.isfile(pointer_path):
        return None

    try:
        with open(pointer_path, "r") as f:
            session_dir = f.read().strip()
        return session_dir if session_dir else None
    except Exception:
        return None


def wait_for_current_session(sessions_root, poll_sec=0.25):
    """
    Wait until CURRENT_SESSION.txt exists and the referenced session has robot_outbox/.
    """
    print("Waiting for CURRENT_SESSION.txt in: {}".format(sessions_root))

    while True:
        session_dir = read_current_session_dir(sessions_root)
        if session_dir:
            outbox_dir = os.path.join(session_dir, "robot_outbox")
            if os.path.isdir(outbox_dir):
                print("Using session: {}".format(session_dir))
                return session_dir

        time.sleep(poll_sec)


def main():
    session_dir = wait_for_current_session(SESSIONS_ROOT)

    robot = NAORobot("clas")
    robot.mm.sit()
    convo = ConversationManager(robot)

    consumer = NaoJobConsumer(
        convo,
        model="gesturizer2:latest",
        interlocutor="Dude"
    )

    consumer.run_job_worker(session_dir)


if __name__ == "__main__":
    main()
