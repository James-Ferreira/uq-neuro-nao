# -*- coding: utf-8 -*-

from __future__ import absolute_import

from src_py2.robot.nao_robot import NAORobot


name = raw_input("Choose a robot: meta / clas: ")

if name == "meta":
    ips = ["192.168.0.78", "192.168.0.79"]
elif name == "clas":
    ips = ["192.168.0.183"]
else:
    ips = []

connected = []
for ip in ips:
    try:
        robot_converser = NAORobot(name, ip)
        connected.append(robot_converser)
    except Exception as e:
        print("WARN: could not connect to {} ({}) - skipping".format(ip, e))

if __name__ == "__main__":
    robot_converser.tts.say("butternuts")
