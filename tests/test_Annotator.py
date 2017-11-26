import unittest

from hownoisy.Annotator import Annotator


class test_Annotator(unittest.TestCase):
    def setUp(self):
        self.annotator = Annotator()

    def test_soundscape_wav_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.annotator.annotate("dummy/soundscape_nonexistent.wav")

    def test_soundscape_wav_illegal_format(self):
        with self.assertRaises(ValueError):
            self.annotator.annotate("dummy/soundscape_illegal_format.mp3")

    def check_annotation_format(self, annotation):
        self.assertIsInstance(annotation, str, "annotate result is not a string")
        self.assertFalse(annotation == "", "annotate result is an empty string")

        classes = ['air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 'drilling', 'engine_idling',
                   'gun_shot', 'jackhammer', 'siren', 'street_music']
        for line in annotation.split("\r\n"):
            if line != "":
                try:
                    start, end, class_ = tuple(line.split("\t"))
                    try:
                        start_as_float = float(start)
                        self.assertTrue(0 <= start_as_float <= 60.0,
                                        "start time ({0}) is not in range 0 <= end <= 60.0".format(start_as_float))
                        try:
                            end_as_float = float(end)
                            self.assertTrue(0 <= end_as_float <= 60.0,
                                            "end time ({0}) is not in range 0 <= end <= 60.0".format(end_as_float))
                            self.assertTrue(end > start,
                                            "end time ({0}) is not larger than start time ({1})".format(start_as_float,
                                                                                                        end_as_float))
                        except ValueError:
                            self.fail("end time ({0}) is not a float".format(end))
                    except ValueError:
                        self.fail("start time ({0}) is not a float".format(start))
                    self.assertTrue(class_ in classes, class_ + " is not a valid class")
                except ValueError:
                    self.fail("not three values on line '{0}'")

    def test_success(self):
        annotation = self.annotator.annotate("dummy/soundscape_good.wav")
        self.check_annotation_format(annotation)


if __name__ == '__main__':
    unittest.main()
