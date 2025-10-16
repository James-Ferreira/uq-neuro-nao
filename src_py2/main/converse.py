# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time

from src_py2.robot.nao_robot import NAORobot

#meta = ConversationManager("meta")
clas = NAORobot("clas")

if __name__ == "__main__":

    clas.mm.sit()
    # text = "take a hot towel bath now."
    # clas.cm.speak(text)
    text2 = """
    "[point to self] if you ask me, the mafia are a big part of the deep state. 

    """

    # meta.speak_n_time(text2)
    clas.cm.speak_n_gest(text2)

    #MEAN ACCURACY PERCENTAGE: 0.824859115911

    #     [pump fist] I'm rooting for jfk the sequel.
    # Right, I should also do some of my random untagged gestures for you.
    # [point forward] So what is your opinion on this important matter?
    # I used to think that washing in the sink was a good idea, but now I believe [point up] it's all up to God.
    # [look upward] Hey, I could use some help down here, big guy.
    # Another sequence of random gestures.
    # Well: [shrug] you got me. I have no idea.
    # Bad people, you know, they go [point down] down to hell and suffer forever.
    # [shake fist] You damn bastards, you damn pieces of shit.
    # Oh God. [facepalm] I can't believe how dumb that guy is.
    # He's got [spread arms] the whole world in his hands. 