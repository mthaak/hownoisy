import re
import subprocess

ANNOYANCE = {'air_conditioner': 0.5, 'car_horn': 0.9, 'children_playing': 0.2, 'dog_bark': 0.6, 'drilling': 0.8,
             'engine_idling': 0.6, 'gun_shot': 1.0, 'jackhammer': 0.9, 'siren': 0.5, 'street_music': 0.3}


class Rater:
    def rate(self, soundscape_wav, annotations_txt):
        def readEvents(filepath):
            events = []
            with open(filepath) as file:
                for line in file:
                    try:
                        split = line.split('\t')
                        event = {'start': float(split[0]), 'end': float(split[1]), 'class': split[2].rstrip()}
                        events.append(event)
                    except:
                        pass  # skip line
            return events

        events = readEvents(annotations_txt)

        markers = []
        for event in events:
            markers.append({'soundscape': 1, 'isStart': True, 'time': event['start'], 'class': event['class']})
            markers.append({'soundscape': 1, 'isStart': False, 'time': event['end'], 'class': event['class']})
        markers.sort(key=lambda k: k['time'])

        def getLoudness(soundscape_wav, start, end):
            command = ['ffmpeg.exe', '-nostats', '-i', soundscape_wav, '-filter_complex',
                       'atrim={0}:{1}'.format(round(start, 3), round(end, 3)) + ',ebur128=peak=true', '-f', 'null',
                       '-']
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            summary = str(output).split("Summary:")[-1]
            loudness = float(re.search(r"Integrated loudness:.*?([\-0-9.]*) LUFS", summary).group(1))
            return loudness

        rating = 0
        classes = []
        a = 0
        for marker in markers:
            b = marker['time']

            if classes:
                loudness = getLoudness(soundscape_wav, a, b) + 70.0  # assuming that -70.0 is the lowest LUFS
                rating += sum(
                    map(lambda class_name: (b - a) * loudness / len(classes) * ANNOYANCE[class_name], classes))

            if marker['isStart']:
                classes.append(marker['class'])
            else:
                classes.remove(marker['class'])

            a = b

        return rating
