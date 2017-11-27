"""Script used for testing/debugging Annotator"""

import glob
import os.path

from hownoisy.Annotator import Annotator

SOUNDSCAPES_FOLDER = "../data/Scaper/"  # input
ANNOTATIONS_FOLDER = "../data/Annotations/"  # output

# Create annotations folder if it does not yet exist
if not os.path.isdir(ANNOTATIONS_FOLDER):
    os.mkdir(ANNOTATIONS_FOLDER)

annotator = Annotator()
for soundscape_wav in glob.glob(SOUNDSCAPES_FOLDER + "*.wav"):
    annotation = annotator.annotate(soundscape_wav)
    soundscape_name = str(os.path.basename(soundscape_wav).split(".")[0])
    annotation_str = "\r\n".join(["\t".join([str(s) for s in e]) for e in annotation])
    annotation_filepath = ANNOTATIONS_FOLDER + soundscape_name + ".txt"
    with open(annotation_filepath, 'w', newline="") as file:
        print(annotation_str, file=file)
