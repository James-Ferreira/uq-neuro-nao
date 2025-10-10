# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from src_py2.robot.nao_robot import NAORobot


class Converse(object):
    """
    Usage:
        converser = Converse("meta")      # auto-connect; tries both meta IPs
        converser.say("Hello from NAO!")  # uses the connected NAORobot

        # If you created with connect_on_init=False:
        converser = Converse("clas", connect_on_init=False)
        converser.connect()               # connect later
    """

    def __init__(self, name, connect_on_init=True):
        self.name = name
        self._robot = None       # the NAORobot instance once connected
        self.ip_used = None      # which IP actually worked
        self._ip_pool = self._ips_for(name)
        if connect_on_init:
            self.connect()

    def _ips_for(self, name):
        if name == "meta":
            # meta flips between these two
            return ["192.168.0.78", "192.168.0.79"]
        elif name == "clas":
            return ["192.168.0.183"]
        else:
            return []

    def connect(self):
        """
        Try each known IP until one succeeds. Raises if none work.
        """
        if not self._ip_pool:
            raise ValueError("Unknown robot name '{}' (no IPs configured).".format(self.name))

        last_err = None
        for ip in self._ip_pool:
            try:
                self._robot = NAORobot(self.name, ip)
                self.ip_used = ip
                return self._robot
            except Exception as e:
                last_err = e
                print("WARN: Failed to connect to {} @ {}: {}".format(self.name, ip, e))

        # If we got here, all IPs failed
        self._robot = None
        self.ip_used = None
        raise RuntimeError(
            "Could not connect to {} using any known IPs: {}. Last error: {}".format(
                self.name, ", ".join(self._ip_pool), last_err
            )
        )

    @property
    def is_connected(self):
        return self._robot is not None

    def say(self, quote):
        """
        Speak via NAORobot TTS, connecting on-demand if needed.
        """
        if not self._robot:
            self.connect()
        self._robot.tts.say(quote)

    def get_robot(self):
        """
        Access the underlying NAORobot (connects on-demand).
        """
        if not self._robot:
            self.connect()
        return self._robot

    def reconnect(self, ip=None):
        """
        Force a reconnect. Optionally prefer a specific IP first.
        """
        if ip is not None:
            # Put the requested IP at the front of the pool if not already there
            self._ip_pool = [ip] + [x for x in self._ip_pool if x != ip]
        return self.connect()

    def __getattr__(self, attr):
        """
        Delegate unknown attributes/methods to the underlying NAORobot,
        so you can do converser.motion, converser.posture, etc.
        """
        robot = self.get_robot()
        return getattr(robot, attr)
