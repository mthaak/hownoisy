"""Script used to create artificial soundscapes using Scaper"""

import os

import numpy as np
import scaper
from datetime import datetime

# OUTPUT FOLDER
# outfolder = '../data/Soundscapes'
outfolder = '../../soundscapes'

# SCAPER SETTINGS
fg_folder = '../data/ByClass'
bg_folder = '../data/ByClass'

n_soundscapes = 1000
ref_db = -50
duration = 60.0

min_events = 10
max_events = 10

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
    for _ in range(n_events):
        sc.add_event(label=('choose', []),
                     source_file=('choose', []),
                     source_time=('const', 0.0),
                     event_time=('uniform', 0.0, 60.0),
                     event_duration=('uniform', 1.0, 4.0),
                     snr=('uniform', 6, 30),
                     pitch_shift=('uniform', -3.0, 3.0),
                     time_stretch=('uniform', 0.8, 1.2))

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
