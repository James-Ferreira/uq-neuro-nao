# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time

from src_py2.robot.nao_robot import NAORobot

#meta = ConversationManager("meta")
clas = NAORobot("clas")

if __name__ == "__main__":

    clas.mm.sit()

    transcription = clas.cm.converse(rounds=6)
    print(transcription)

    #MEAN ACCURACY PERCENTAGE: 0.824859115911

    text2 = """
    # And this one is just regular old random, but you feel it, don't you?
    # [look upward] Just look at the stars, will you? They are so beautiful.
    # You know what?  You can [point down] go to hell and stay there!
    # Lots of people like green tea, but [point forward] what about you?
    # [point up] God is looking down at us and sees everything we do.
    # Yes! [pump fist] Hell yeah, hell yeah, we won!
    # Geez, [scratch head] I don't know what to think about that.
    # [shake fist] You bastards, you damn bastards.
    # [shrug] You got me, I don't have a clue.
    # [spread arms] Come one, come all.  We shall have feasting this night.
    # [wave hand] Bye bye folks.
    """

    # clas.cm.speak_n_gest(text2)

