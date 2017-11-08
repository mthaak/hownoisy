import os
import shutil
import unittest

from hownoisy.run import run


# TODO run unit test
class test_Rater(unittest.TestCase):
    def setUp(self):
        if os.path.isdir('output'):
            shutil.rmtree('output')  # remove output folder before tests

    def test_input_missing(self):
        args = {}
        with self.assertRaises(ValueError):
            run(args)

    def test_input(self):
        args = {
            'input': ['dummy/soundscape_good.wav', 'dummy/soundscape_illegal_format.mp3', 'dummy'],
            'output': 'output/',
            'separate_results': False,
            'running_time': False,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)

    def test_output(self):
        args = {
            'input': ['dummy/soundscape_good.wav', 'dummy/soundscape_illegal_format.mp3', 'dummy'],
            'output': 'output/',
            'separate_results': False,
            'running_time': False,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(args['output']))

    def test_separate_results_false(self):
        args = {
            'input': ['dummy/soundscape_good.wav', 'dummy/soundscape_illegal_format.mp3', 'dummy'],
            'output': 'output/',
            'separate_results': False,
            'running_time': False,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)
        output_filename = "output/results.txt"
        self.assertTrue(os.path.exists(output_filename))
        # Assert output format
        with open(output_filename, newline="\r\n") as file:
            output = file.read()
            try:
                lines = output.split("\r\n")
                for line in lines:
                    if line != "\n":
                        split_line = line.split("\t")
                        self.assertTrue(split_line[0] == "soundscape_good.wav")
                        float(split_line[1])
            except:
                self.fail()

    def test_separate_results_true(self):
        args = {
            'input': ['dummy/soundscape_good.wav', 'dummy/soundscape_illegal_format.mp3', 'dummy'],
            'output': 'output/',
            'separate_results': True,
            'running_time': False,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)
        output_filename = "output/soundscape_good.txt"
        self.assertTrue(os.path.exists(output_filename))
        # Assert output format
        with open(output_filename, newline="\r\n") as file:
            output = file.read()
            try:
                float(output)
            except:
                self.fail()

    def test_running_time(self):
        args = {
            'input': ['dummy/soundscape_good.wav', 'dummy/soundscape_illegal_format.mp3', 'dummy'],
            'output': 'output/',
            'separate_results': False,
            'running_time': True,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)
        output_filename = "output/results.txt"
        with open(output_filename, newline="\r\n") as file:
            output = file.read()
            # Assert output format
            try:
                lines = output.split("\r\n")
                for line in lines:
                    if line != "\n":
                        split_line = line.split("\t")
                        float(split_line[1])
                        float(split_line[2])
            except:
                self.fail()

    def test_verbose(self):
        args = {
            'input': ['dummy/soundscape_good.wav', 'dummy/soundscape_illegal_format.mp3', 'dummy'],
            'output': 'output/',
            'separate_results': False,
            'running_time': False,
            'verbose': True
        }
        success = run(args)
        self.assertTrue(success)
        # It is not really possible to test verbosity


if __name__ == '__main__':
    unittest.main()
