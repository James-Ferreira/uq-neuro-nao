# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random

from src_py2.robot.nao_robot import NAORobot

#meta = ConversationManager("meta")
clas = NAORobot("clas")

def measure_speech_duration(train=True):

    if train: 
        insert = "training"
    else:
        insert = "verification"
    
    open_path = "src_py3/duration_prediction/texts/" + insert + "_text_block.txt"
    save_segments_path = "src_py3/duration_prediction/texts/" + insert + "_segments_list.txt"
    save_durations_path = "src_py3/duration_prediction/texts/" + insert + "_durations_list.txt"

    with open(open_path, 'r') as file:
        text = file.read().strip()

    segments_etc = clas.cm.preprocess_segments(text)
    random.shuffle(segments_etc)
    segments = []
    real_durations = []
    for seg in segments_etc:
        print(seg)
        segments += [seg[0]]
        real_duration = clas.cm.speak_n_time(seg[0])
        real_durations += [real_duration]

    try:
        with open(save_segments_path, "w") as f:
            f.write(str(segments))
        print("File saved successfully!")
    except Exception as e:
        print("Error saving file:", e)

    try:
        with open(save_durations_path, "w") as f:
            f.write(str(real_durations))
        print("File saved successfully!")
    except Exception as e:
        print("Error saving file:", e)  
    
if __name__ == "__main__":
   
   measure_speech_duration()
   
