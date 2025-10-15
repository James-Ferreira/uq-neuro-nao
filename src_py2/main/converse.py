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

    text2 = """
    “Curiouser and curiouser!” cried Alice (she was so much surprised, that for the moment she quite forgot how to speak good English); “now I’m opening out like the largest telescope that ever was! Good-bye, feet!” (for when she looked down at her feet, they seemed to be almost out of sight, they were getting so far off). “Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears? I’m sure I shan’t be able! I shall be a great deal too far off to trouble myself about you: you must manage the best way you can;—but I must be kind to them,” thought Alice, “or perhaps they won’t walk the way I want to go! Let me see: I’ll give them a new pair of boots every Christmas.”
I would sing in the face of fears,
When about my feet they throng;
I would pass them by with a heart that drips
A hymn of joy from my eager lips;
For fear cannot live for long—
With song!
Miss Bartlett was already seated on a tightly stuffed arm-chair, which had the colour and the contours of a tomato. She was talking to Mr. Beebe, and as she spoke, her long narrow head drove backwards and forwards, slowly, regularly, as though she were demolishing some invisible obstacle. “We are most grateful to you,” she was saying. “The first evening means so much. When you arrived we were in for a peculiarly mauvais quart d’heure.”
This week, I made a life-changing decision — I’ve officially snipped off my little nutsack and handed it over to every slow driver on the Gold Coast.

From now on, I’ll no longer attempt to drive at the speed limit. I’ve ascended. I’m now spiritually aligned with the chosen few who drive 10–20km under at all times.
I used to get into the left lane for my exit with adequate time before the exit.

Silly me!

The trick is to be like everyone else and dart across 2 lanes at the last minute to avoid getting stuck in the exit queue.

Also, when taking the Coomera exit I now make sure to use the right lane to skip the queue then cut someone off and join the front of the queue before the turn.

I hate you all, fuck you!
    """

    meta.speak_n_time(text2)
    #meta.gns(text)

    #MEAN ACCURACY PERCENTAGE: 0.824859115911