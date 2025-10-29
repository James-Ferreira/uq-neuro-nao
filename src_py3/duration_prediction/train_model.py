# train_model.py
import ast

#from duration_predictor import train_and_save_model
from src_py3.duration_prediction.duration_predictor import train_and_save_model

if __name__ == "__main__":

    with open("src_py3/duration_prediction/texts/training_segments_list.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()

    training_segments_list = ast.literal_eval(text)
    print(training_segments_list, type(training_segments_list))

    with open("src_py3/duration_prediction/texts/training_durations_list.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()

    training_durations_list = ast.literal_eval(text)
    print(training_durations_list, type(training_durations_list))       

    train_and_save_model(training_segments_list, training_durations_list)