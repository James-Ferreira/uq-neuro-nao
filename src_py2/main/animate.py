# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time

from src_py2.robot.nao_robot import NAORobot

clas = NAORobot("clas")
#clas = Converse("clas")

if __name__ == "__main__":
    clas.anm.animate()