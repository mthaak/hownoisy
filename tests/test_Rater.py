import unittest

# TODO Rater unit test
from hownoisy.Rater import Rater


class test_Rater(unittest.TestCase):
    def setUp(self):
        self.rater = Rater()

    def read_annotation(self, filepath):
        events = []
        with open(filepath) as file:
            for line in file:
                try:
                    split_line = line.split('\t')
                    events.append((float(split_line[0]), float(split_line[1]), split_line[2].rstrip()))
                except:
                    pass  # skip line
        return events

    def test_soundscape_wav_not_found(self):
        annotation = self.read_annotation("tests/dummy/annotation_good.txt")
        with self.assertRaises(FileNotFoundError):
            self.rater.rate("tests/dummy/soundscape_nonexistent.wav", annotation)

    def test_soundscape_wav_illegal_format(self):
        annotation = self.read_annotation("tests/dummy/annotation_good.txt")
        with self.assertRaises(ValueError):
            self.rater.rate("tests/dummy/soundscape_good.mp3", annotation)

    def test_annotation_illegal_class(self):
        annotation = self.read_annotation("tests/dummy/annotation_illegal_class.txt")
        with self.assertRaises(ValueError):
            self.rater.rate("tests/dummy/soundscape_good.wav", annotation)

    def test_annotation_empty(self):
        annotation = self.read_annotation("tests/dummy/annotation_empty.txt")
        with self.assertRaises(ValueError):
            self.rater.rate("tests/dummy/soundscape_good.wav", annotation)

    def test_success(self):
        annotation = self.read_annotation("tests/dummy/annotation_good.txt")
        rating = self.rater.rate("tests/dummy/soundscape_good.wav", annotation)
        self.assertIsInstance(rating, float)
        self.assertAlmostEqual(rating, 660.0, delta=1.0)


if __name__ == '__main__':
    unittest.main()
