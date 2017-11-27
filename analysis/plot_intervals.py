import json

import matplotlib.pyplot as plt
import numpy as np
import sys

# INPUT_FILE = "data/Scaper/soundscape_x0.txt"
INPUT_FILE = sys.argv[1]

with open("annoyances.json") as file:
    annoyances = json.load(file)

classes = list(annoyances.keys())

# Use numpy to read the data in
data = np.genfromtxt(INPUT_FILE, names=['start', 'stop', 'class'], dtype=None)
class_, start, stop = data['class'], data['start'], data['stop']


def plot_class_intervals(y, xstart, xstop, color):
    # Plot intervals at y from xstart to xstop with given color
    y = np.full(len(xstart), y)
    plt.hlines(y, xstart, xstop, color, lw=4)
    plt.vlines(xstart, y + 0.03, y - 0.03, color, lw=2)
    plt.vlines(xstop, y + 0.03, y - 0.03, color, lw=2)


for i, class_ in enumerate(classes):
    class_intervals = (data['class'] == class_.encode('utf-8'))
    color = 'b' if i % 2 else 'r'
    plot_class_intervals(0.1 + 0.1 * i, start[class_intervals], stop[class_intervals], color)

plt.xticks(np.arange(0, 61, 1), np.arange(0, 61, 1))
plt.yticks(np.arange(0.1, 1.2, 0.1), classes)
plt.ylim(0, 1.1)
plt.xlim(-1, 61)
plt.xlabel('time')
plt.show()
