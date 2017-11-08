import unittest

# TODO Rater unit test
from hownoisy.Rater import Rater


class test_Rater(unittest.TestCase):
    def setUp(self):
        self.rater = Rater()

    def test_soundscape_wav_not_found(self):
        annotation = open("dummy/annotation_good.txt", newline="\r\n").read()
        with self.assertRaises(FileNotFoundError):
            self.rater.rate("dummy/soundscape_nonexistent.wav", annotation)

    def test_soundscape_wav_illegal_format(self):
        annotation = open("dummy/annotation_good.txt", newline="\r\n").read()
        with self.assertRaises(ValueError):
            self.rater.rate("dummy/soundscape_illegal_format.mp3", annotation)

    def test_annotation_illegal_format(self):
        annotation = open("dummy/annotation_illegal_format.txt", newline="\r\n").read()
        with self.assertRaises(ValueError):
            self.rater.rate("dummy/soundscape_good.wav", annotation)

    def test_annotation_illegal_class(self):
        annotation = open("dummy/annotation_illegal_class.txt", newline="\r\n").read()
        with self.assertRaises(ValueError):
            self.rater.rate("dummy/soundscape_good.wav", annotation)

    def test_annotation_empty(self):
        annotation = open("dummy/annotation_empty.txt", newline="\r\n").read()
        with self.assertRaises(ValueError):
            self.rater.rate("dummy/soundscape_good.wav", annotation)

    def test_success(self):
        annotation = open("dummy/annotation_good.txt", newline="\r\n").read()
        rating = self.rater.rate("dummy/soundscape_good.wav", annotation)
        self.assertIsInstance(rating, float)
        self.assertAlmostEqual(rating, 660.0, delta=1.0)


if __name__ == '__main__':
    unittest.main()
