import unittest

# TODO Rater unit test
from hownoisy.Rater import Rater


class test_Rater(unittest.TestCase):
    def setUp(self):
        self.rater = Rater()

    def test_soundscape_wav_not_found(self):
        self.assertRaises(FileNotFoundError, self.rater.rate, "dummy/soundscape_nonexistent.wav",
                          "dummy/annotation_good.txt")

    def test_annotation_txt_not_found(self):
        self.assertRaises(FileNotFoundError, self.rater.rate, "dummy/soundscape_good.wav",
                          "dummy/annotation_nonexistent.txt")

    def test_soundscape_wav_illegal_format(self):
        self.assertRaises(ValueError, self.rater.rate, "dummy/soundscape_illegal_format.mp3",
                          "dummy/annotation_good.txt")

    def test_annotation_txt_illegal_format(self):
        self.assertRaises(ValueError, self.rater.rate, "dummy/soundscape_good.wav",
                          "dummy/annotation_illegal_format.txt")

    def test_annotation_txt_illegal_class(self):
        self.assertRaises(ValueError, self.rater.rate, "dummy/soundscape_good.wav",
                          "dummy/annotation_illegal_class.txt")

    def test_annotation_txt_empty(self):
        self.assertRaises(ValueError, self.rater.rate, "dummy/soundscape_good.wav", "dummy/annotation_empty.txt")

    def test_success(self):
        rating = self.rater.rate("dummy/soundscape_good.wav", "dummy/annotation_good.txt")
        self.assertAlmostEqual(rating, 660.0, delta=1.0)


if __name__ == '__main__':
    unittest.main()
