import csv
import glob
import json
import os

from util.calc_annotation_error import calc_annotation_error

SOUNDSCAPES_FOLDER = '../data/Scaper/'
ANNOTATIONS_FOLDER = '../data/Annotations/'
RESULTS_FILE = 'scaper_results.tsv'

with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['file', ' duration', ' num_events', ' polyphony_max', ' polyphony_gini', ' reverb', ' avg_snr',
                        ' avg_time_stretch', ' avg_pitch_shift', 'ANNOTATION_ERROR'])

    for soundscape_file in glob.glob(SOUNDSCAPES_FOLDER + '*.wav'):
        soundscape_name = os.path.basename(soundscape_file).split('.')[0]
        jams = json.load(open(SOUNDSCAPES_FOLDER + soundscape_name + '.jams'))

        actual_annotations_file = SOUNDSCAPES_FOLDER + soundscape_name + '.txt'
        predicted_annotations_file = ANNOTATIONS_FOLDER + soundscape_name + '.txt'
        annotation_error = calc_annotation_error(actual_annotations_file, predicted_annotations_file)

        filename = soundscape_name + '.wav'
        duration = jams['file_metadata']['duration']
        num_events = jams['annotations'][0]['sandbox']['scaper']['n_events']
        polyphony_max = jams['annotations'][0]['sandbox']['scaper']['polyphony_max']
        polyphony_gini = round(jams['annotations'][0]['sandbox']['scaper']['polyphony_gini'], 6)
        reverb = jams['annotations'][0]['sandbox']['scaper']['reverb']
        sounds = jams['annotations'][0]['data']
        avg_snr = round(sum(map(lambda sound: sound['value']['snr'], sounds)) / len(sounds), 6)
        avg_time_stretch = round(sum(map(lambda sound: sound['value']['time_stretch'], sounds)) / len(sounds), 6)
        avg_pitch_shift = round(sum(map(lambda sound: sound['value']['pitch_shift'], sounds)) / len(sounds), 6)
        ANNOTATION_ERROR = round(annotation_error, 6)

        csvwriter.writerow(
            [filename, duration, num_events, polyphony_max, polyphony_gini, reverb, avg_snr, avg_time_stretch,
             avg_pitch_shift, ANNOTATION_ERROR])
