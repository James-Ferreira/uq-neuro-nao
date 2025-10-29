# any_other_script.py
import ast
import statistics

from src_py3.duration_prediction.duration_predictor import predict_duration

if __name__ == "__main__":
    sentences = [
        "Short.",
        "A longer sentence with commas, periods, and a question?",
        "Wow!!!"
    ]
    with open("src_py3/duration_prediction/texts/verification_segments_list.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()
    verification_segments_list = ast.literal_eval(text)

    with open("src_py3/duration_prediction/texts/verification_durations_list.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()
    verification_durations_list = ast.literal_eval(text)

    accuracy_percentages = []

    for index, s in enumerate(verification_segments_list):
        model_dur = predict_duration(s)
        real_dur = verification_durations_list[index]
        accuracy_percentage = 100 - (model_dur - real_dur) / real_dur
        accuracy_percentages += [accuracy_percentage]
        #print(f'"{s}" → {dur:.3f} s')
    mean = statistics.mean(accuracy_percentages)
    median = statistics.median(accuracy_percentages)
    stdev = statistics.stdev(accuracy_percentages)

    print(f"MEAN ACCURACY DIFFERENCE: {mean}")
    print(f"MEDIAN ACCURACY: {median}")
    print(f"STD ACCURACY: {stdev}")