"""
This module should be executed in order to run the whole HowNoisy pipeline on a set of soundscape recordings.
"""
import argparse
import os.path
from datetime import datetime

from hownoisy.Annotator import Annotator
from hownoisy.Rater import Rater

###############################################################################
# CONFIGURATION PARAMETERS

path = os.path.dirname(__file__)

# Labeled sounds used for annotating the soundscapes
SOUNDS_FOLDER = path + "/../data/UrbanSound8k.tar/audio/"

# CSV file that contains the labels of all the sounds
SOUNDS_LABELS_FILE = path + "/../data/UrbanSound8k.tar/metadata/UrbanSound8K.csv"


###############################################################################
# COMPLETE RUN

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
    annotator = Annotator(SOUNDS_FOLDER, SOUNDS_LABELS_FILE)
    rater = Rater()

    if not args['separate_results']:
        output_results = ""

    n_files = 0
    # Annotate and rate each soundscape one after the other
    for soundscape_wav in files:
        n_files += 1
        soundscape_name = os.path.basename(soundscape_wav).split(".")[0]

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


###############################################################################
# COMMAND LINE ARGUMENTS

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the HowNoisy pipeline.')
    parser.add_argument('--input', '-i', nargs='*', required=True,
                        help='files or folders containing the input files')

    parser.add_argument('--output', '-o',
                        help='folder in which the output file(s) should be stored')

    parser.add_argument('--separate_results', '-sep', action='store_true',
                        help='whether to put the results in separate text files')

    parser.add_argument('--running_time', '-rt', action='store_true',
                        help='whether to include the running time (in ms) in the output')

    parser.add_argument('--verbose', '-v', action='store_true',
                        help='whether to print intermediate steps')

    args = parser.parse_args()

    try:
        # Add / to end of folder names
        args.output = args.output if args.output.endswith("/") else args.output + "/"
    except:
        args.output = os.getcwd() + "/"  # if output folder not set, then define output as the current working directory

    run(args)  # run pipeline with given command line arguments
