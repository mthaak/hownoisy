"""
This module contains only the Rater class that calculates the final noise rating for a soundscape.
"""

import re
import subprocess

# Annoyance coefficients of different sound types
ANNOYANCE = {'air_conditioner': 0.5, 'car_horn': 0.9, 'children_playing': 0.2, 'dog_bark': 0.6, 'drilling': 0.8,
             'engine_idling': 0.6, 'gun_shot': 1.0, 'jackhammer': 0.9, 'siren': 0.5, 'street_music': 0.3}


class Rater:
    """
    Component that calculates the final noise rating for a soundscape.
    """

    def rate(self, soundscape_wav, annotation):
        """
        Calculates the final noise rating for the given soundscape recording using the supplied annotation file.

        :param soundscape_wav: string with path to WAV file containing the soundscape recording
        :param annotation: string with path to textfile containing the soundscape annotation
        :return: float denoting the noise rating (higher means more noise with a scale of 0-duration in seconds)
        """

        if not soundscape_wav.endswith(".wav"):
            raise ValueError("Soundscape file has bad format")

        # Try to open soundscape_wav, raises FileNotFound exception if does not exist
        with open(soundscape_wav):
            pass

        # Converts the sound events from the annotation file to a dict
        def _read_events(annotation):
            events = []
            for line in annotation.split("\r\n"):
                if line != '':
                    try:
                        split = line.split('\t')
                        event = {'start': float(split[0]), 'end': float(split[1]), 'class': split[2].rstrip()}
                        events.append(event)
                    except:
                        raise ValueError("Annotation has illegal format")
            return events

        # Creates a list of pairs of start and end markers for each sound event, sorted by time
        def _create_markers(events):
            markers = []
            for event in events:
                markers.append({'soundscape': 1, 'isStart': True, 'time': event['start'], 'class': event['class']})
                markers.append({'soundscape': 1, 'isStart': False, 'time': event['end'], 'class': event['class']})
            markers.sort(key=lambda k: k['time'])
            return markers

        # Determines the loudness of a part of a soundscape recording using ffmpeg
        def _get_loudness(soundscape_wav, start, end):
            try:
                command = ['ffmpeg.exe', '-nostats', '-i', soundscape_wav, '-filter_complex',
                           'atrim={0}:{1}'.format(round(start, 3), round(end, 3)) + ',ebur128=peak=true', '-f', 'null',
                           '-']
                output = subprocess.check_output(command, stderr=subprocess.STDOUT)
                summary = str(output).split("Summary:")[-1]
                loudness = float(re.search(r"Integrated loudness:.*?([\-0-9.]*) LUFS", summary).group(1))
                return loudness
            except FileNotFoundError:
                raise FileNotFoundError("ffmpeg.exe not found. Make sure you have correctly installed ffmpeg.")

        # Calculates the final rating by iterating over all the sound event start and end markers
        # Based on the noise model formula
        def _calc_rating(markers):
            rating = 0
            classes = []  # current classes
            a = 0  # start time of current interval
            for marker in markers:
                b = marker['time']  # end time of current interval

                if classes:
                    loudness = _get_loudness(soundscape_wav, a, b) + 70.0  # assuming that -70.0 is the lowest LUFS
                    rating += sum(map(lambda class_: (b - a) * loudness / len(classes) * ANNOYANCE[class_], classes))

                if marker['isStart']:
                    class_ = marker['class'].rstrip()
                    classes.append(class_)
                    try:
                        ANNOYANCE[class_]
                    except Exception:
                        raise ValueError('Annotation file contains illegal class ({0})'.format(class_))
                else:
                    classes.remove(marker['class'])

                a = b

            return rating

        events = _read_events(annotation)
        if not events:
            raise ValueError("Annotation file is empty")
        markers = _create_markers(events)
        rating = _calc_rating(markers)

        return rating
