import json

import numpy as np

INPUT_FILE = "analysis/scaper_results.tsv"
OUTPUT_FILE = "analysis/detector_performance.tsv"

with open("annoyances.json") as file:
    annoyances = json.load(file)

classes = list(annoyances.keys())

scaper_results = np.loadtxt(INPUT_FILE, delimiter='\t', skiprows=1, usecols=range(12, 42))
n = len(scaper_results)

output = [['class', 'precision', 'recall', 'f1', 'accuracy']]  # header
for i, class_ in enumerate(classes):
    total_pred = np.sum(scaper_results[:, 3 * i])
    total_true = np.sum(scaper_results[:, 3 * i + 1])
    total_overlap = np.sum(scaper_results[:, 3 * i + 2])
    precision = total_overlap / total_pred
    recall = total_overlap / total_true
    f1 = 2 * precision * recall / (precision + recall)
    accuracy = 1 - (total_pred + total_true - 2 * total_overlap) / (60.0 * n)
    output.append(
        [class_, "{:.6f}".format(precision), "{:.6f}".format(recall), "{:.6f}".format(f1), "{:.6f}".format(accuracy)])

array = np.array(output)

np.savetxt(OUTPUT_FILE, array, fmt='%s', delimiter='\t')
