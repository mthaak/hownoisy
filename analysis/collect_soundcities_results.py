import csv
import xml.etree.ElementTree as ET
from random import random

METADATA_FILE = '../data/Soundcities/metadata.xml'
RATINGS_FOLDER = '../data/Ratings/'
RESULTS_FILE = 'scaper_results.tsv'

tree = ET.parse(METADATA_FILE)
snds = tree.getroot()

with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter='\t', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(
        ['file', 'title', 'mood', 'recorder', 'description', 'date', 'active', 'quality', 'time', 'size', 'lat', 'long',
         'location', 'RUNNING_TIME', 'NOISE_RATING'])

    for city in snds:
        for snd in city[0]:
            file = snd[0].text
            title = snd[1].text
            mood = snd[2].text
            recorder = snd[3].text
            description = snd[4].text.replace('\r', '').replace('\n', '')
            date = snd[5].text
            active = snd[6].text
            quality = snd[7].text
            time = snd[8].text
            size = snd[9].text
            lat = snd[10][0].text
            long = snd[10][0].text
            location = snd[11].text
            time_as_float = float(time)
            RUNNING_TIME = str(round(0.1 * time_as_float * random(), 6))  # fake
            NOISE_RATING = str(round(time_as_float * random(), 6))  # fake

            csvwriter.writerow([file, title, mood, recorder, description, date, active, quality, time, size, lat, long,
                                location, RUNNING_TIME, NOISE_RATING])
