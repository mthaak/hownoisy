"""Script used to calculate the error between the actual and the predicted annotations produced by Annotator"""

import glob
import os.path
from itertools import product

ANNOYANCE = {'air_conditioner': 0.5, 'car_horn': 0.9, 'children_playing': 0.2, 'dog_bark': 0.6, 'drilling': 0.8,
             'engine_idling': 0.6, 'gun_shot': 1.0, 'jackhammer': 0.9, 'siren': 0.5, 'street_music': 0.3}


def calc_annotation_error(filepath1, filepath2):
    # Converts the sound events from the annotation file to a dict
    def _read_events(filepath):
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

    events1 = _read_events(filepath1)
    events2 = _read_events(filepath2)

    markers = []
    for event in events1:
        markers.append({'soundscape': 1, 'isStart': True, 'time': event['start'], 'class': event['class']})
        markers.append({'soundscape': 1, 'isStart': False, 'time': event['end'], 'class': event['class']})
    for event in events2:
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
                error += (b - a) * min(abs(ANNOYANCE[d] - ANNOYANCE[c]) for c, d in product(classes1, classes2))
            else:
                error += (b - a) * min([ANNOYANCE[c] for c in classes1])
        else:
            if classes2:
                error += (b - a) * min([ANNOYANCE[c] for c in classes2])
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


ACTUAL_ANNOTATIONS_FOLDER = "../data/Soundscapes/"
PREDICTED_ANNOTATIONS_FOLDER = "../data/Annotations/"

print("SOUNDSCAPE\t\t\tERROR")
for act, pred in product(glob.glob(ACTUAL_ANNOTATIONS_FOLDER + "*.txt"),
                         glob.glob(PREDICTED_ANNOTATIONS_FOLDER + "*.txt")):
    act_basename = os.path.basename(act)
    pred_basename = os.path.basename(pred)
    if act_basename == pred_basename:
        soundscape_column = act_basename + ((20 - len(act_basename)) // 4) * "\t"
        error = calc_annotation_error(act, pred)
        print(soundscape_column, error, sep="")
