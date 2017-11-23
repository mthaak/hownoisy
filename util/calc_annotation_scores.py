import numpy as np
import pandas as pd
import sys
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score

def extract_test_fn_labels(fn, duration=20.0):
    
    target_classes = set()
    time_sections_with_label = []
    
    with open(fn) as fd:
        lines = fd.readlines()
    
    for line in lines:
        line_splits = line.split()
        
        target_classes.add(line_splits[2])
        time_sections_with_label.append((float(line_splits[0]), float(line_splits[1]), line_splits[2]))
    
    target_classes_labels = {}
    
    for target_class in target_classes:
        
        time_intervals = np.arange(0.0, duration, 0.05)
        labels = np.full(time_intervals.shape[0], -1, dtype=np.int)

        for idx, t in enumerate(time_intervals):

            for time_section in time_sections_with_label:
                if t < time_section[0] or t > time_section[1]:
                    continue

                if time_section[2] == target_class:
                    labels[idx] = 1
                    break
        
        target_classes_labels[target_class] = labels

    return target_classes_labels

def calc_annotation_scores(true_annotation_fn_path, pred_annotation_fn_path, print_score=True):

    true_annotation_target_classes_labels = extract_test_fn_labels(true_annotation_fn_path)
    pred_annotation_target_classes_labels = extract_test_fn_labels(pred_annotation_fn_path)

    scores = []

    for target_class, labels in true_annotation_target_classes_labels.items():
        recall = recall_score(labels, pred_annotation_target_classes_labels[target_class])
        precision = precision_score(labels, pred_annotation_target_classes_labels[target_class])
        f1_ = f1_score(labels, pred_annotation_target_classes_labels[target_class])
        accuracy = accuracy_score(labels, pred_annotation_target_classes_labels[target_class])
        
        scores.append([target_class, recall, precision, f1_, accuracy])

    scores = pd.DataFrame(scores)
    scores.columns = ['target_class', 'recall', 'precision', 'f1_score', 'accuracy']
    
    if print_score:
        print(scores)

    return scores

def main():
    true_annotation_fn_path = sys.argv[1]
    pred_annotation_fn_path = sys.argv[2]

    scores = calc_annotation_scores(true_annotation_fn_path, pred_annotation_fn_path)

if __name__ == "__main__":
    main()