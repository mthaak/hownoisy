import csv
import glob
import json
import os

SOUNDSCAPES_FOLDER = "data/Analysis_Dur/"
RESULTS_FILE = "data/Analysis_Dur/results.txt"
OUTPUT_FILE = "analysis/scaper_dur_results.tsv"

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
    csvwriter.writerow(["file", " duration", " num_events", " polyphony_max", " polyphony_gini", " reverb", " avg_snr",
                        " avg_time_stretch", " avg_pitch_shift", "noise_rating", "running_time"])

    for soundscape_file in glob.glob(SOUNDSCAPES_FOLDER + "*.wav"):
        soundscape_name = os.path.basename(soundscape_file).split(".")[0]
        jams = json.load(open(SOUNDSCAPES_FOLDER + soundscape_name + ".jams"))

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

        csvwriter.writerow(
            [filename, duration, num_events, polyphony_max, polyphony_gini, reverb, avg_snr, avg_time_stretch,
             avg_pitch_shift, noise_rating, running_time])
