from __future__ import print_function

import time

from src_py2.robot.nao_robot import NAORobot


def main():
    print("Connecting to clas...")
    clas = NAORobot("clas", usrnme="nao", pword="nao")
    print("Connected to clas at {}".format(clas.ip_used))
    print("Loosening all joints so the motors can rest...")
    clas.mm.loose()
    time.sleep(0.5)
    print("clas.mm.loose() completed.")


if __name__ == "__main__":
    main()
