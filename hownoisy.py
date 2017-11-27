import argparse
import os

from hownoisy.run import run

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
        # Add / to end of output folder name
        args.output = args.output if args.output.endswith("/") else args.output + "/"
    except:
        args.output = os.getcwd() + "/"  # if output folder not set, then define output as the current working directory

    run(args)  # run HowNoisy pipeline with given command line arguments
