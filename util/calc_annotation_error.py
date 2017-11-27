"""Script used to calculate the error between the actual and the predicted annotations produced by Annotator"""

import json
import os.path
import sys
from itertools import product


def calc_annotation_error(annotation1, annotation2, annoyances):
    markers = []
    for event in annotation1:
        markers.append({'soundscape': 1, 'isStart': True, 'time': event['start'], 'class': event['class']})
        markers.append({'soundscape': 1, 'isStart': False, 'time': event['end'], 'class': event['class']})
    for event in annotation2:
        markers.append({'soundscape': 2, 'isStart': True, 'time': event['start'], 'class': event['class']})
        markers.append({'soundscape': 2, 'isStart': False, 'time': event['end'], 'class': event['class']})
    markers.sort(key=lambda k: k['time'])

    error = 0
    classes1 = []
    classes2 = []
    a = 0
    for marker in markers:
        b = marker['time']
        if classes1:
            if classes2:
                error += (b - a) * min(abs(annoyances[d] - annoyances[c]) for c, d in product(classes1, classes2))
            else:
                error += (b - a) * min([annoyances[c] for c in classes1])
        else:
            if classes2:
                error += (b - a) * min([annoyances[c] for c in classes2])
            else:
                error += (b - a) * 0
        a = b

        if marker['soundscape'] == 1:
            if marker['isStart']:
                classes1.append(marker['class'])
            else:
                classes1.remove(marker['class'])
        elif marker['soundscape'] == 2:
            if marker['isStart']:
                classes2.append(marker['class'])
            else:
                classes2.remove(marker['class'])

    return error


if __name__ == '__main__':
    true_annotation_filepath = sys.argv[1]
    pred_annotation_filepath = sys.argv[2]


    def read_annotation(filepath):
        events = []
        with open(filepath) as file:
            for line in file:
                try:
                    split = line.split('\t')
                    event = {'start': float(split[0]), 'end': float(split[1]), 'class': split[2].rstrip()}
                    events.append(event)
                except:
                    pass  # skip line
        return events


    true_annotation = read_annotation(true_annotation_filepath)
    pred_annotation = read_annotation(pred_annotation_filepath)

    with open(os.path.dirname(os.path.realpath(__file__)) + "/../annoyances.json") as file:
        annoyances = json.load(file)

    match = calc_annotation_error(true_annotation, pred_annotation, annoyances)

    print(match)
