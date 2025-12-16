import time
from src_py2.robot.nao_robot import NAORobot
from src_py2.robot.audio_manager import sound_library

clas = NAORobot("clas")

if __name__ == "__main__":

    clas.tm.wait_for_left_bumper_press()
    clas.audio_player.post.playFile(sound_library["thinking"])

    clas.tm.wait_for_left_bumper_release()
    start = time.time()
    clas.audio_player.stopAll()
    print("Released!")
    end = time.time()
    print("Elapsed time: {} seconds").format(end-start)
