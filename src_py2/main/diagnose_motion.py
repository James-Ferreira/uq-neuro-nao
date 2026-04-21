from __future__ import print_function

import argparse
import os
import sys
import time

_THIS_FILE = globals().get("__file__")
if _THIS_FILE:
    _BASE_DIR = os.path.dirname(os.path.abspath(_THIS_FILE))
else:
    _BASE_DIR = os.getcwd()
_REPO_ROOT = os.path.abspath(os.path.join(_BASE_DIR, "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.append(_REPO_ROOT)

from src_py2.robot.nao_robot import NAORobot

BODY_JOINTS = [
    "HeadYaw", "HeadPitch",
    "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
    "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
    "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll",
    "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
]

RARM_JOINTS = [
    "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand",
]


def safe_call(label, fn):
    print("\n=== {} ===".format(label))
    try:
        result = fn()
        print("OK: {}".format(result))
        return result
    except Exception as e:
        print("ERROR: {}".format(e))
        return None


def print_stiffness_map(values):
    print("\n=== Body stiffness by joint ===")
    if not isinstance(values, list):
        print("Unavailable: {}".format(values))
        return
    for joint, value in zip(BODY_JOINTS, values):
        print("{:<16} {}".format(joint, value))


def print_notifications(robot):
    print("\n=== Notifications ===")
    try:
        from naoqi import ALProxy
        nm = ALProxy("ALNotificationManager", robot.ip, robot.port)
        notes = nm.notifications()
        if not notes:
            print("No active notifications.")
            return
        for note in notes:
            try:
                data = dict(note)
            except Exception:
                data = note if isinstance(note, dict) else {}
            print(
                "id={} severity={} message={}".format(
                    data.get("id"),
                    data.get("severity"),
                    data.get("message"),
                )
            )
    except Exception as e:
        print("ERROR: {}".format(e))


def print_right_arm_diagnostics(robot):
    print("\n=== Right arm diagnosis keys ===")
    keys = []
    for joint in RARM_JOINTS:
        keys.extend([
            "Diagnosis/Active/{}/Error".format(joint),
            "Diagnosis/Temperature/{}/Error".format(joint),
            "Device/SubDeviceList/{}/Temperature/Sensor/Value".format(joint),
            "Device/SubDeviceList/{}/Temperature/Sensor/Status".format(joint),
            "Device/SubDeviceList/{}/Position/Sensor/Value".format(joint),
            "Device/SubDeviceList/{}/ElectricCurrent/Sensor/Value".format(joint),
            "Device/SubDeviceList/{}/Hardness/Actuator/Value".format(joint),
        ])
    for key in keys:
        try:
            value = robot.memory.getData(key)
            print("{} = {}".format(key, value))
        except Exception as e:
            print("{} = ERROR: {}".format(key, e))

    print("\n=== ALDiagnosis summary ===")
    try:
        from naoqi import ALProxy
        diagnosis = ALProxy("ALDiagnosis", robot.ip, robot.port)
        try:
            print("Active diagnosis: {}".format(diagnosis.getActiveDiagnosis()))
        except Exception as e:
            print("Active diagnosis ERROR: {}".format(e))
        try:
            print("Passive diagnosis: {}".format(diagnosis.getPassiveDiagnosis()))
        except Exception as e:
            print("Passive diagnosis ERROR: {}".format(e))
    except Exception as e:
        print("ALDiagnosis unavailable: {}".format(e))


def main():
    parser = argparse.ArgumentParser(description="Minimal NAO motion/posture diagnostic.")
    parser.add_argument("--robot", default="clas", help="Robot name or IP")
    parser.add_argument("--username", default="nao")
    parser.add_argument("--password", default="nao")
    parser.add_argument("--port", type=int, default=9559)
    parser.add_argument(
        "--enable-life",
        action="store_true",
        help="Temporarily enable autonomous life during the diagnostic.",
    )
    args = parser.parse_args()

    print("Connecting to {}...".format(args.robot))
    robot = NAORobot(
        args.robot,
        port=args.port,
        usrnme=args.username,
        pword=args.password,
    )
    print("Connected to {} at {}".format(robot.name, robot.ip_used))

    safe_call("Autonomous life state", lambda: robot.life.getState())
    safe_call("Basic awareness enabled", lambda: robot.basic_awareness.isEnabled())
    safe_call("Robot posture", lambda: robot.posture.getPosture())
    safe_call("Robot is awake", lambda: robot.motion.robotIsWakeUp())
    stiffness_before = safe_call("Body stiffness", lambda: robot.motion.getStiffnesses("Body"))
    print_stiffness_map(stiffness_before)
    safe_call("Body angles", lambda: robot.motion.getAngles("Body", True)[:6])
    print_notifications(robot)
    print_right_arm_diagnostics(robot)

    if args.enable_life:
        safe_call("Enable autonomous life", lambda: robot.life.setState("solitary"))
    else:
        safe_call("Disable autonomous life", lambda: robot.life.setState("disabled"))
    safe_call("Disable basic awareness", lambda: robot.basic_awareness.setEnabled(False))
    safe_call("Wake up", lambda: robot.motion.wakeUp())
    time.sleep(1.0)

    safe_call("Robot is awake after wakeUp", lambda: robot.motion.robotIsWakeUp())
    stiffness_after_wakeup = safe_call("Body stiffness after wakeUp", lambda: robot.motion.getStiffnesses("Body"))
    print_stiffness_map(stiffness_after_wakeup)
    safe_call("Set RArm stiffness to 1.0", lambda: robot.motion.setStiffnesses("RArm", 1.0))
    time.sleep(0.5)
    safe_call("RArm stiffness after explicit set", lambda: robot.motion.getStiffnesses("RArm"))
    print_right_arm_diagnostics(robot)
    safe_call("Posture family", lambda: robot.posture.getPostureFamily())
    safe_call("Posture before stand", lambda: robot.posture.getPosture())
    safe_call("Head yaw angles", lambda: robot.motion.getAngles("HeadYaw", True))

    safe_call("Go to StandInit", lambda: robot.posture.goToPosture("StandInit", 0.5))
    time.sleep(2.0)
    safe_call("Posture after StandInit", lambda: robot.posture.getPosture())

    safe_call("Small head move", lambda: robot.motion.angleInterpolation(["HeadYaw"], [0.2], [1.0], True))
    safe_call("Head yaw after move", lambda: robot.motion.getAngles("HeadYaw", True))

    safe_call("Go to Sit", lambda: robot.posture.goToPosture("Sit", 0.5))
    time.sleep(2.0)
    safe_call("Posture after Sit", lambda: robot.posture.getPosture())

    safe_call("Rest", lambda: robot.motion.rest())
    safe_call("Robot is awake after rest", lambda: robot.motion.robotIsWakeUp())


if __name__ == "__main__":
    main()
