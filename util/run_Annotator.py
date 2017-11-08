"""Script used for testing/debugging Annotator"""

import glob
import os.path

from hownoisy.Annotator import Annotator

SOUNDS_FOLDER = "../data/UrbanSound8k.tar/audio/"
SOUNDS_LABELS_FILE = "../data/UrbanSound8k.tar/metadata/UrbanSound8K.csv"

SOUNDSCAPES_FOLDER = "../data/Scaper/"  # input
ANNOTATIONS_FOLDER = "../data/Annotations/"  # output

annotator = Annotator(SOUNDS_FOLDER, SOUNDS_LABELS_FILE)
for soundscape_wav in glob.glob(SOUNDSCAPES_FOLDER + "*.wav"):
    annotation = annotator.annotate(soundscape_wav)
    soundscape_name = str(os.path.basename(soundscape_wav).split(".")[0])
    annotation_filepath = ANNOTATIONS_FOLDER + soundscape_name + ".txt"
    print(annotation, file=open(annotation_filepath, 'w'))
