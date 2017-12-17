import glob

import os

SOUNDSCAPES_FOLDER = "../data/Analysis/"  # input
OUTPUT_FILE = "n_events.txt"

output = []
for soundscape_jam in glob.glob(SOUNDSCAPES_FOLDER + "*.jams"):
    soundscape_name = str(os.path.basename(soundscape_jam).split(".")[0])

    n_events = "err"
    with (open(soundscape_jam)) as jams_file:  # "n_events": 14,
        for line in jams_file.readlines():
            index = line.find("n_events")
            if index > -1:
                n_events = line[index + 11: index + 13]
                break
    output.append(soundscape_name + " " + n_events)
with open(OUTPUT_FILE, 'w', newline="") as file:
    print("\r\n".join(output), file=file)
