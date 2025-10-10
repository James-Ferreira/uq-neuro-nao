# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time

from src_py2.robot.conversation_manager import Converse

meta = Converse("meta")
clas = Converse("clas")

if __name__ == "__main__":
    
    # meta.say("coconut sucker")
    # time.sleep(0.1)
    # clas.say("condermilions")

    meta.mm.sit()
    text = "One of the common motivations behind why a necrophiliac is sexually attracted to a corpse is the notion that they own an object or sexual partner that does not resist or reject them. " \
    "Havelock Ellis claimed that necrophilia and algolagnia (sexual pleasure derived from pain, especially around erogenous areas) were interrelated. " \
    "Both acts refer to how negative effects like fear and disgust are transformed into feelings of arousal and desire."
    meta.gns(text)
