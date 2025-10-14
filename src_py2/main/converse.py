# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time

from src_py2.robot.conversation_manager import Converse

meta = Converse("meta")
#clas = Converse("clas")

if __name__ == "__main__":


    meta.mm.sit()
    text = "“How little we know of what there is to know. I wish that I were going to live a long time instead of going to die today because I have learned much about life in these four days; more, I think than in all other time. I’d like to be an old man to really know. I wonder if you keep on learning or if there is only a certain amount each man can understand. I thought I knew so many things that I know nothing of. I wish there was more time. One of the common motivations behind why a necrophiliac is sexually attracted to a corpse is the notion that they own an object or sexual partner that does not resist or reject them. " \
    "Havelock Ellis claimed that necrophilia and algolagnia (sexual pleasure derived from pain, especially around erogenous areas) were interrelated. " \
    "Both acts refer to how negative effects like fear and disgust are transformed into feelings of arousal and desire. Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, “and what is the use of a book,” thought Alice “without pictures or conversations? So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

    #meta.speak_n_time(text)
    meta.gns(text)
