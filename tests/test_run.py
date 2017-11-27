import os
import shutil
import unittest

from hownoisy.run import run


class test_run(unittest.TestCase):
    def setUp(self):
        if os.path.isdir("output"):
            shutil.rmtree("output")  # remove output folder before tests

    def test_input_missing(self):
        args = {}
        with self.assertRaises(ValueError):
            run(args)

    def test_input_output(self):
        args = {
            'input': ["tests/dummy/soundscape_good.wav"],
            'output': "tests/output/",
            'separate_results': False,
            'running_time': False,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(args['output']))

    def test_separate_results_false(self):
        args = {
            'input': ["tests/dummy/soundscape_good.wav", "tests/dummy/folder/"],
            'output': "tests/output/",
            'separate_results': False,
            'running_time': False,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)
        expected_files = ["soundscape_good.wav", "soundscape_x0.wav", "soundscape_x1.wav"]
        output_filename = args['output'] + "results.txt"
        self.assertTrue(os.path.exists(output_filename))
        # Assert output format
        with open(output_filename, newline="\r\n") as file:
            output = file.read()
            try:
                lines = output.split("\r\n")
                for line in lines:
                    if line != "\n":
                        split_line = line.split("\t")
                        expected_files.remove(split_line[0])
                        float(split_line[1])  # noise rating
                self.assertTrue(expected_files == [])  # check all expected files seen
            except:
                self.fail()

    def test_separate_results_true(self):
        args = {
            'input': ["tests/dummy/soundscape_good.wav", "tests/dummy/folder/"],
            'output': "tests/output/",
            'separate_results': True,
            'running_time': False,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)
        expected_files = ["soundscape_good.txt", "soundscape_x0.txt", "soundscape_x1.txt"]
        # Assert output format
        for file in expected_files:
            output_filename = args['output'] + file
            self.assertTrue(os.path.exists(output_filename))
            with open(output_filename, newline="\r\n") as file:
                output = file.read()
                try:
                    float(output)  # noise rating
                except:
                    self.fail()

    def test_include_running_time(self):
        args = {
            'input': ["tests/dummy/soundscape_good.wav", "tests/dummy/folder/"],
            'output': "tests/output/",
            'separate_results': False,
            'running_time': True,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)
        expected_files = ["soundscape_good.wav", "soundscape_x0.wav", "soundscape_x1.wav"]
        with open(args['output'] + "results.txt", newline="\r\n") as file:
            output = file.read()
            # Assert output format
            try:
                lines = output.split("\r\n")
                for line in lines:
                    if line != "\n":
                        split_line = line.split("\t")
                        expected_files.remove(split_line[0])
                        float(split_line[1])  # noise rating
                        float(split_line[2])  # running time
                self.assertTrue(expected_files == [])  # check all expected files seen
            except:
                self.fail()

    def test_include_running_time_separate(self):
        args = {
            'input': ["tests/dummy/soundscape_good.wav", "tests/dummy/folder/"],
            'output': "tests/output/",
            'separate_results': True,
            'running_time': True,
            'verbose': False
        }
        success = run(args)
        self.assertTrue(success)
        expected_files = ["soundscape_good.txt", "soundscape_x0.txt", "soundscape_x1.txt"]
        # Assert output format
        for file in expected_files:
            output_filename = args['output'] + file
            self.assertTrue(os.path.exists(output_filename))
            with open(output_filename, newline="\r\n") as file:
                output = file.read().split("\t")
                try:
                    float(output[0])  # noise rating
                    float(output[1])  # running time
                except:
                    self.fail()


if __name__ == '__main__':
    unittest.main()
