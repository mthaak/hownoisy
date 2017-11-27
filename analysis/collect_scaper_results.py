import csv
import glob
import itertools
import json
import os

from util.calc_annotation_error import calc_annotation_error
from util.calc_annotation_match import calc_annotation_match

SOUNDSCAPES_FOLDER = "data/Scaper/"
ANNOTATIONS_FOLDER = "data/Annotations/"
RESULTS_FILE = "data/Output/results.txt"
OUTPUT_FILE = "analysis/scaper_results.tsv"

with open("annoyances.json") as file:
    annoyances = json.load(file)

classes = list(annoyances.keys())


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


with open(RESULTS_FILE) as file:
    results = {}
    for line in file.readlines():
        split_line = line.split('\t')
        try:
            results[split_line[0]] = (split_line[1], split_line[2].rstrip())
        except:
            pass

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    match_columns = list(
        itertools.chain(*[(class_ + "_true", class_ + "_pred", class_ + "_overlap") for class_ in classes]))
    csvwriter.writerow(["file", " duration", " num_events", " polyphony_max", " polyphony_gini", " reverb", " avg_snr",
                        " avg_time_stretch", " avg_pitch_shift", "noise_rating", "running_time",
                        "annotation_error"] + match_columns)

    for soundscape_file in glob.glob(SOUNDSCAPES_FOLDER + "*.wav"):
        soundscape_name = os.path.basename(soundscape_file).split(".")[0]
        jams = json.load(open(SOUNDSCAPES_FOLDER + soundscape_name + ".jams"))

        actual_annotation_filepath = SOUNDSCAPES_FOLDER + soundscape_name + ".txt"
        pred_annotation_filepath = ANNOTATIONS_FOLDER + soundscape_name + ".txt"

        actual_annotation = read_annotation(actual_annotation_filepath)
        pred_annotation = read_annotation(pred_annotation_filepath)

        annotation_error = calc_annotation_error(actual_annotation, pred_annotation, annoyances)
        annotation_match = calc_annotation_match(actual_annotation, pred_annotation)
        match_values = list(itertools.chain(*[annotation_match[class_] for class_ in classes]))
        match_values = ["{:.6f}".format(v) for v in match_values]

        filename = soundscape_name + ".wav"
        duration = jams['file_metadata']['duration']
        num_events = jams['annotations'][0]['sandbox']['scaper']['n_events']
        polyphony_max = jams['annotations'][0]['sandbox']['scaper']['polyphony_max']
        polyphony_gini = round(jams['annotations'][0]['sandbox']['scaper']['polyphony_gini'], 6)
        reverb = jams['annotations'][0]['sandbox']['scaper']['reverb']
        sounds = jams['annotations'][0]['data']
        avg_snr = round(sum(map(lambda sound: sound['value']['snr'], sounds)) / len(sounds), 6)
        avg_time_stretch = round(sum(map(lambda sound: sound['value']['time_stretch'], sounds)) / len(sounds), 6)
        avg_pitch_shift = round(sum(map(lambda sound: sound['value']['pitch_shift'], sounds)) / len(sounds), 6)
        try:
            noise_rating, running_time = results[filename]
        except:
            noise_rating, running_time = -1, -1
        annotation_error = round(annotation_error, 6)

        csvwriter.writerow(
            [filename, duration, num_events, polyphony_max, polyphony_gini, reverb, avg_snr, avg_time_stretch,
             avg_pitch_shift, noise_rating, running_time, annotation_error] + match_values)
