"""Script used to create artificial soundscapes using Scaper"""

import os
from datetime import datetime

import numpy as np
import scaper

# OUTPUT FOLDER
outfolder = '../data/Analysis_Dur'
# outfolder = sys.argv[1]

# SCAPER SETTINGS
fg_folder = '../data/ByClass'
bg_folder = '../data/ByClass'

n_soundscapes = 100
# n_soundscapes = int(sys.argv[2])
ref_db = -50
duration = 30.0

min_events = 1
max_events = 60

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

    # sc.add_event(label=('const', outfolder.split('/')[-1]),
    #              source_file=('choose', []),
    #              source_time=('const', 0.0),
    #              event_time=('uniform', 0.0, duration - 4.0),
    #              event_duration=('const', 4.0),
    #              snr=('const', 3),
    #              pitch_shift=None,
    #              time_stretch=None)

    for idx in range(n_events):

        sc.add_event(label=('choose', []),
                     source_file=('choose', []),
                     source_time=('const', 0.0),
                     event_time=('uniform', 0.0, duration - 4.0),
                     event_duration=('uniform', 1.0, 4.0),
                     snr=('uniform', 0, 50),
                     pitch_shift=('uniform', -2.0, 2.0),
                     time_stretch=('uniform', 0.8, 1.2))

    # generate
    audiofile = os.path.join(outfolder, "soundscape_a{:d}.wav".format(n))
    jamsfile = os.path.join(outfolder, "soundscape_a{:d}.jams".format(n))
    txtfile = os.path.join(outfolder, "soundscape_a{:d}.txt".format(n))

    sc.generate(audiofile, jamsfile,
                allow_repeated_label=True,
                allow_repeated_source=True,
                reverb=0.0,
                disable_sox_warnings=True,
                no_audio=False,
                txt_path=txtfile)

    after = datetime.now()
    time_took = (after - before).total_seconds() * 1000

    print('Soundscape %d took %d ms to generate' % (n + 1, time_took))

    if n % 10 == 9:
        duration += 30.0
