"""
This module should be executed in order to run the whole HowNoisy pipeline on a set of soundscape recordings.
"""
import os.path
from datetime import datetime

from hownoisy.Annotator import Annotator
from hownoisy.Rater import Rater


def run(args):
    # Check if all arguments have been set
    try:
        args = vars(args)
    except TypeError:
        pass
    if {'input', 'output', 'separate_results', 'running_time', 'verbose'} - args.keys() != set():
        raise ValueError("Arguments missing")

    # Collect all files
    files = []
    for item in args['input']:
        if os.path.isfile(item):
            files.append(item)
        elif os.path.isdir(item):
            item = item if item.endswith("/") else item + "/"
            files.extend(map(lambda filename: item + filename, os.listdir(item)))

    # Ignore files with illegal format
    files = filter(lambda filename: filename.endswith(".wav"), files)

    # Create output folder if it does not yet exist
    if not os.path.isdir(args['output']):
        os.mkdir(args['output'])

    # Create Annotator and Rater components
    annotator = Annotator()
    rater = Rater()

    output_results = ""

    n_files = 0
    # Annotate and rate each soundscape one after the other
    for soundscape_wav in files:
        n_files += 1
        soundscape_name = str(os.path.basename(soundscape_wav).split(".")[0])

        try:
            if args['running_time']:
                start_time = datetime.now()

            # Annotating...
            if args['verbose']:
                print("Annotating {0}...".format(soundscape_name + ".txt"))
            annotation = annotator.annotate(soundscape_wav)

            # Rating...
            output = rater.rate(soundscape_wav, annotation)
            if args['verbose']:
                print("Noise rating: {0}\n".format(output))
            if args['running_time']:
                dt = datetime.now() - start_time
                running_time = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
                output = str(output) + "\t" + str(running_time)
            if args['separate_results']:
                output_filepath = args['output'] + soundscape_name + ".txt"
                with open(output_filepath, 'w') as file:
                    print(output, file=file)
            else:
                output_results += soundscape_name + ".wav\t" + str(output) + "\r\n"

        except ValueError as e:
            print(e)

    if not args['separate_results']:
        output_filepath = args['output'] + "results.txt"
        with open(output_filepath, 'w', newline="") as file:
            print(output_results, file=file)

    if args['verbose']:
        print("HowNoisy completed on {0} files".format(n_files))

    return True  # denotes successful completion
