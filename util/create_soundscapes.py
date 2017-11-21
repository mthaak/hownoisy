"""Script used to create artificial soundscapes using Scaper"""

import os

import numpy as np
import scaper
from datetime import datetime
import sys


# OUTPUT FOLDER
# outfolder = '../data/Soundscapes'
outfolder = sys.argv[1]

# SCAPER SETTINGS
fg_folder = '../data/ByClass'
bg_folder = '../data/ByClass'

n_soundscapes = int(sys.argv[2])
ref_db = -50
duration = 20.0

min_events = 5
max_events = 5

for n in range(n_soundscapes):

    print('Generating soundscape: {:d}/{:d}'.format(n + 1, n_soundscapes))

    before = datetime.now()
    # create a scaper
    sc = scaper.Scaper(duration, fg_folder, bg_folder)
    sc.protected_labels = ['car_horn', 'dog_bark', 'gun_shot', 'siren']
    sc.ref_db = ref_db

    # add background
    # sc.add_background(label=('const', 'noise'),
    #                   source_file=('choose', []),
    #                   source_time=('const', 0))

    # add random number of foreground events
    n_events = np.random.randint(min_events, max_events + 1)
    time_interval = duration / n_events

    sc.add_event(label=('const', outfolder.split('/')[-1]),
                 source_file=('choose', []),
                 source_time=('const', 0.0),
                 event_time=('uniform', 0.0, duration - 4.0),
                 event_duration=('const', 4.0),
                 snr=('const', 3),
                 pitch_shift=None,
                 time_stretch=None)

    for idx in range(n_events - 1):

        sc.add_event(label=('choose', []),
                     source_file=('choose', []),
                     source_time=('const', 0.0),
                     event_time=('uniform', 0.0, duration - 4.0),
                     event_duration=('const', 4.0),
                     snr=('const', 3),
                     pitch_shift=None,
                     time_stretch=None)

    # generate
    audiofile = os.path.join(outfolder, "soundscape_{:d}.wav".format(n))
    jamsfile = os.path.join(outfolder, "soundscape_{:d}.jams".format(n))
    txtfile = os.path.join(outfolder, "soundscape_{:d}.txt".format(n))

    sc.generate(audiofile, jamsfile,
                allow_repeated_label=True,
                allow_repeated_source=False,
                reverb=0.0,
                disable_sox_warnings=True,
                no_audio=False,
                txt_path=txtfile)

    after = datetime.now()
    time_took = (after - before).total_seconds() * 1000

    print('Soundscape %d took %d ms to generate' % (n, time_took))
