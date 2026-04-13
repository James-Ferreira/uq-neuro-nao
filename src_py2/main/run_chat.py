import os
import time

from src_py2.integrations.voice_job import NaoJobConsumer
from src_py2.robot.nao_robot import NAORobot
from src_py2.robot.conversation_manager import ConversationManager
from config.project_loader import load_active_project_profile, get_nested


def default_sessions_root():
    here = os.path.dirname(os.path.abspath(__file__))
    uq_repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    repos_parent = os.path.dirname(uq_repo_root)
    return os.path.join(repos_parent, "voice-llm-chat", "sessions")


PROJECT_PROFILE = load_active_project_profile()
ROBOT_CHAT_CFG = PROJECT_PROFILE.get("robot_chat", {})
SESSIONS_ROOT = get_nested(ROBOT_CHAT_CFG, ["sessions_root"], default_sessions_root())
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
    print("Active project profile: {}".format(PROJECT_PROFILE.get("_project_id")))
    session_dir = wait_for_current_session(SESSIONS_ROOT)

    robot_name = get_nested(ROBOT_CHAT_CFG, ["robot_name"], "clas")
    robot_username = get_nested(ROBOT_CHAT_CFG, ["robot_username"], None)
    robot_password = get_nested(ROBOT_CHAT_CFG, ["robot_password"], None)
    robot = NAORobot(robot_name, usrnme=robot_username, pword=robot_password)
    robot.mm.sit()
    convo = ConversationManager(robot)

    consumer_model = get_nested(ROBOT_CHAT_CFG, ["consumer_model"], "gesturizer2:latest")
    consumer_interlocutor = get_nested(ROBOT_CHAT_CFG, ["consumer_interlocutor"], None)
    consumer_include_segments = bool(get_nested(ROBOT_CHAT_CFG, ["include_segments"], False))
    consumer_special_commands = get_nested(ROBOT_CHAT_CFG, ["special_commands"], None)
    session_end_cfg = get_nested(PROJECT_PROFILE, ["conversation", "session_end"], {})
    consumer = NaoJobConsumer(
        convo,
        model=consumer_model,
        interlocutor=consumer_interlocutor,
        include_segments=consumer_include_segments,
        special_commands=consumer_special_commands,
        session_end_cfg=session_end_cfg
    )

    consumer.run_job_worker(session_dir)


if __name__ == "__main__":
    main()
