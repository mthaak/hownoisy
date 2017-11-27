import csv

import matplotlib.pyplot as plt
import numpy as np

DATA_FILE = "soundcities_results.tsv"

times_list = []
locations_list = []
running_times_list = []
noise_ratings_list = []
with open(DATA_FILE, newline='', encoding='utf-8') as csvfile:
    csv = csv.reader(csvfile, delimiter='\t', quotechar='|')
    next(csv)  # skip first line
    for row in csv:
        times_list.append(float(row[8]))
        locations_list.append(row[12])
        running_times_list.append(float(row[13]))
        noise_ratings_list.append(float(row[14]))

times = np.array(times_list)
locations = np.array(locations_list)
running_times = np.array(running_times_list)
noise_ratings = np.array(noise_ratings_list)

# RUNNING_TIME
running_time_min = np.min(running_times)
running_time_median = np.median(running_times)
running_time_max = np.max(running_times)
running_time_mean = np.mean(running_times)
running_time_std = np.std(running_times)

# NOISE_RATING
noise_rating_min = np.min(noise_ratings)
noise_rating_median = np.median(noise_ratings)
noise_rating_max = np.max(noise_ratings)
noise_rating_mean = np.mean(noise_ratings)
noise_rating_std = np.std(noise_ratings)

# Scatter plot running time vs soundscape duration
plt.figure()
plt.title("Running time vs soundscape duration")
plt.xlabel("Duration (s)")
plt.ylabel("Running time (s)")
plt.scatter(times, running_times)

# Bar plot noise rating per location
locations_set = list(set(locations_list))
noise_per_location = [0] * len(locations_set)
sounds_per_location = [0] * len(locations_set)
for i, location in enumerate(locations_set):
    noise_per_location[i] = np.mean(noise_ratings[locations == location])
    sounds_per_location[i] = len(noise_ratings[locations == location])

locations_set, noise_per_location = zip(
    *sorted(zip(locations_set, noise_per_location), key=lambda x: x[1], reverse=True))

fig, ax = plt.subplots()

plt.title("Average noise rating per location")
plt.ylabel("Noise rating")
# plt.setp(locations_set, rotation=45, fontsize=8)
plt.xticks(rotation=90)
colors = ['C' + str(i % 10) for i in range(len(locations_set))]
rects = ax.bar(range(len(locations_set)), noise_per_location, color=colors, tick_label=locations_set)
# for rect, sounds in zip(rects, sounds_per_location):
#     height = rect.get_height()
#     ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#             '%d' % int(sounds),
#             ha='center', va='bottom')

# World chart time per lat/long

plt.show()
pass
