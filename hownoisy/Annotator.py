import glob
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score
import sys

sound_class_table = {
    'air_conditioner' : 0,
    'car_horn' : 1,
    'children_playing' : 2,
    'dog_bark' : 3,
    'drilling' : 4,
    'engine_idling' : 5,
    'gun_shot' : 6,
    'jackhammer' : 7,
    'siren' : 8,
    'street_music' : 9
}

gaussian_mixture_model = pickle.load(open('./gaussian_mixture_model.pkl', 'rb'))

def segment_window(audio_len, segment_len, segment_stride):
    
    start = 0
    while start < audio_len:
        yield start, start + segment_len
        start += segment_stride

class Annotator:
    def __init__(self, sounds_folder, sounds_labels_file):
        self.sounds_folder = sounds_folder
        self.sounds_labels_file = sounds_labels_file
        self.sound_detectors = self.load_sound_detector_models()


    def load_sound_detector_models(self):
        sound_detectors = {}

        for k, _ in sound_class_table.items():
            detector_path = './sound_detectors/%s_detector.pkl' % k
            model = pickle.load(open(detector_path, 'rb'))
            sound_detectors[k] = model

        return sound_detectors

    def gen_test_fn_features(self, X, sample_rate, gmm=gaussian_mixture_model):
        
        segment_len = int(sample_rate * 0.1)
        segment_stride = int(sample_rate * 0.05)
        
        file_F_features = np.empty((0, 64))

        for start, end in segment_window(X.size, segment_len, segment_stride):

            segment_mfccs = librosa.feature.mfcc(X[start:end], sample_rate, 
                                n_fft=int(0.02 * sample_rate), 
                                hop_length=int(0.01 * sample_rate))

            segment_F_features = np.sum(gmm.predict_proba(segment_mfccs.T), axis=0) \
                                    / (segment_mfccs.shape[1])

            file_F_features = np.vstack([file_F_features, segment_F_features])
        
        return file_F_features

    def extract_test_fn_labels(self, fn, duration, target_class):

        label_file_path = fn.replace('wav', 'txt')

        with open(label_file_path) as fd:
            lines = fd.readlines()
            time_sections_with_label = list(map(lambda x: (float(x[0]), float(x[1]), x[2]), map(lambda x : x.split(), lines)))
        
        time_intervals = np.arange(0.0, duration, 0.05)
        labels = np.zeros((time_intervals.shape[0]), dtype=np.int)

        for idx, t in enumerate(time_intervals):
            
            labels[idx] = -1
            
            for time_section in time_sections_with_label:
                if t < time_section[0] or t > time_section[1]:
                    continue
                
                if time_section[2] == target_class:
                    labels[idx] = 1
                    break

        return labels

    def find_possible_detectors(self, f_path, f_F_features, duration):
        
        possible_detectors = {}
        
        for sound_name, model in self.sound_detectors.items():

            y = self.extract_test_fn_labels(fn=f_path, duration=duration, target_class=sound_name)
            preds = model.predict(f_F_features)
            
            if recall_score(y, preds) == 0.0:
                continue
            
            if precision_score(y, preds) == 0.0:
                continue
                
            possible_detectors[sound_name] = model
        
        return possible_detectors

    def gen_segments_annotations(self, f_F_features, possible_detectors):

        segments_annotations = [[] for _ in range(f_F_features.shape[0])]

        for idx, segment_F_feature in enumerate(f_F_features):
    
            for sound_name, model in possible_detectors.items():
                
                if model.predict([segment_F_feature])[0] == -1:
                    continue
                
                segments_annotations[idx].append(sound_class_table[sound_name])

        return segments_annotations

    def gen_sound_events_pieces(self, segments_annotations, possible_detectors):

        sound_pieces = {}

        for key in possible_detectors.keys():
            sound_pieces[key] = [True]

        for idx, seg_annotations in enumerate(segments_annotations):
            
            if len(seg_annotations) == 0:
                for k in sound_pieces.keys():
                    sound_pieces[k][0] = True
                    if type(sound_pieces[k][-1]) is list \
                                        and (sound_pieces[k][-1][1] - sound_pieces[k][-1][0]) <= 4:
                        sound_pieces[k].pop(-1)
                continue
            
            for k in sound_pieces.keys():
                
                if sound_class_table[k] in seg_annotations:
                    
                    if sound_pieces[k][0] == True:
                        sound_pieces[k][0] = False
                        if type(sound_pieces[k][-1]) is list \
                                        and (sound_pieces[k][-1][1] - sound_pieces[k][-1][0]) <= 4:
                            sound_pieces[k].pop(-1)
                        
                        sound_pieces[k].append([idx, idx])
                    else:
                        sound_pieces[k][-1][1] = idx
                
                else:
                    sound_pieces[k][0] = True
                    if type(sound_pieces[k][-1]) is list \
                                        and (sound_pieces[k][-1][1] - sound_pieces[k][-1][0]) <= 4:
                        sound_pieces[k].pop(-1)

        return sound_pieces

    def gen_sound_events_annotations(self, sound_pieces):

        sound_events_annotations = []

        for k, v in sound_pieces.items():
            
            for piece in v[1:]:
                sound_events_annotations.append((piece[0] * 0.05, piece[1] * 0.05, k))

        return sorted(sound_events_annotations, key=lambda event: event[0])

    # TODO implement
    def annotate(self, soundscape_wav):

        X, sample_rate = librosa.load(soundscape_wav, sr=None, mono=True)
        if sample_rate != 44100:
            raise Exception('Audio file sample rate is not 44100!')

        f_F_features = self.gen_test_fn_features(X, sample_rate)
        possible_detectors = self.find_possible_detectors(soundscape_wav, f_F_features, X.size/sample_rate)

        segments_annotations = self.gen_segments_annotations(f_F_features, possible_detectors)

        sound_pieces = self.gen_sound_events_pieces(segments_annotations, possible_detectors)
        sound_events_annotations = self.gen_sound_events_annotations(sound_pieces)

        return sound_events_annotations

def main():
    annotator = Annotator(',', '.')

    print('test file name:', sys.argv[1])

    sound_events_annotations = annotator.annotate(sys.argv[1])

    for i in sound_events_annotations:
        print(i)

if __name__ == "__main__":
    main()

