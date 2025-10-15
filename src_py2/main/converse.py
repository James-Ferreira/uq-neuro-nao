# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time

from src_py2.robot.conversation_manager import ConversationManager

#meta = ConversationManager("meta")
clas = NAORobot("clas")

if __name__ == "__main__":

    clas.mm.sit()
    text = "take a hot towel bath now."
    clas.cm.speak(text)
    # text2 = """
  
    # """

    # meta.speak_n_time(text2)
    #meta.gns(text)

    #MEAN ACCURACY PERCENTAGE: 0.824859115911