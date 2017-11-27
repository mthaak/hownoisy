import unittest

from hownoisy.Annotator import Annotator


class test_Annotator(unittest.TestCase):
    def setUp(self):
        self.annotator = Annotator()

    def test_soundscape_wav_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.annotator.annotate("tests/dummy/soundscape_nonexistent.wav")

    def test_soundscape_wav_mp3_format(self):
        annotation = self.annotator.annotate("tests/dummy/soundscape_good.mp3")
        self.check_annotation_format(annotation)

    def check_annotation_format(self, annotation):
        self.assertTrue(len(annotation) > 0, "annotate result is empty")

        classes = ['air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 'drilling', 'engine_idling',
                   'gun_shot', 'jackhammer', 'siren', 'street_music']
        for event in annotation:
            try:
                start_as_float = float(event[0])
                self.assertTrue(0 <= start_as_float <= 60.0,
                                "start time ({0}) is not in range 0 <= end <= 60.0".format(start_as_float))
                try:
                    end_as_float = float(event[1])
                    self.assertTrue(0 <= end_as_float <= 60.0,
                                    "end time ({0}) is not in range 0 <= end <= 60.0".format(end_as_float))
                    self.assertTrue(end_as_float > start_as_float or end_as_float == 60.0,
                                    "end time ({0}) is not larger than start time ({1})".format(start_as_float,
                                                                                                end_as_float))
                except ValueError:
                    self.fail("end time ({0}) is not a float".format(event[1]))
            except ValueError:
                self.fail("start time ({0}) is not a float".format(event[0]))
            self.assertTrue(event[2] in classes, event[2] + " is not a valid class")

    def test_success(self):
        annotation = self.annotator.annotate("tests/dummy/soundscape_good.wav")
        self.check_annotation_format(annotation)


if __name__ == '__main__':
    unittest.main()
