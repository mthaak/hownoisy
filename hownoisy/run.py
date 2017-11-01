"""
This module should be executed in order to run the whole HowNoisy pipeline on a set of soundscape recordings.
"""

import glob
import os.path

from hownoisy.Annotator import Annotator
from hownoisy.Rater import Rater

###############################################################################
# Input parameters that can be modified by the user

# Labeled sounds used for annotating the soundscapes
SOUNDS_FOLDER = "../data/UrbanSound8k.tar/audio"

# CSV file that contains the labels of all the sounds
SOUNDS_LABELS_FILE = "../data/UrbanSound8k.tar/metadata/UrbanSound8K.csv"

# INPUT: soundscape recordings
SOUNDSCAPES_FOLDER = "../data/Scaper/"

# Intermediary folder for soundscape annotations
ANNOTATIONS_FOLDER = "../data/Annotations/"

# OUTPUT: soundscape noise ratings
RATINGS_FOLDER = "../data/Ratings/"

###############################################################################

# TODO command line arguments
# TODO input & parameter checking

###############################################################################

# Create Annotator and Rater components
annotator = Annotator(SOUNDS_FOLDER, SOUNDS_LABELS_FILE)
rater = Rater()

# Annotate and rate each soundscape one after the other
for soundscape_wav in glob.glob(SOUNDSCAPES_FOLDER + "*.wav"):
    soundscape_name = str(os.path.basename(soundscape_wav).split(".")[0])

    try:
        # Annotation...
        print("Annotating {0}...".format(soundscape_name + ".txt"))
        annotation = annotator.annotate(soundscape_wav)
        annotation_filepath = ANNOTATIONS_FOLDER + soundscape_name + ".txt"
        print(annotation, file=open(annotation_filepath, 'w'))

        # Rating...
        if os.path.exists(annotation_filepath):  # check if annotations exist
            rating = rater.rate(soundscape_wav, annotation_filepath)
            print("Noise rating: {0}\n".format(rating))
            rating_filepath = RATINGS_FOLDER + soundscape_name + ".txt"
            print(rating, file=open(rating_filepath, 'w'))

    except Exception as e:
        print(e)
