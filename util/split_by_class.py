"""Script used to split the UrbanSound8K dataset by class into separate folders"""

import os
import shutil

FOLDS = ['9', '10']  # the folds to be split

csv = open("../data/UrbanSound8K.tar/UrbanSound8K/metadata/UrbanSound8K.csv")
csv.readline()
for line in csv.readlines():
    split = line.split(",")
    slice_file_name = split[0]
    fold = split[5]
    if fold in FOLDS:
        class_name = split[7].rstrip()
        src_path = "../data/UrbanSound8K.tar/UrbanSound8K/audio/fold" + fold + "/" + slice_file_name
        dest_path = "../data/ByClass2/" + class_name + "/"
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        shutil.copy2(src_path, dest_path)
        print(slice_file_name)
