"""File used for testing/debugging Rater"""

import glob
import os.path

from hownoisy.Rater import Rater

SOUNDSCAPES_FOLDER = "../data/Soundscapes/"  # input
ANNOTATIONS_FOLDER = "../data/Annotations/"  # input
RATINGS_FOLDER = "../data/Ratings/"  # output

rater = Rater()
for soundscape_wav in glob.glob(SOUNDSCAPES_FOLDER + "*.wav"):
    soundscape_name = os.path.basename(soundscape_wav).split(".")[0]
    annotations_txt = ANNOTATIONS_FOLDER + soundscape_name + ".txt"
    if os.path.exists(annotations_txt):  # check if annotations exist
        rating = rater.rate(soundscape_wav, annotations_txt)
        rating_filepath = RATINGS_FOLDER + soundscape_name + ".txt"
        print(rating, file=open(rating_filepath, 'w'))
