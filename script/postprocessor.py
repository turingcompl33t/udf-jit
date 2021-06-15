# postprocessor.py
# UNIX-style results preprocessor for PL/pgSQL function analysis.

import sys
import json
import argparse
import fileinput
from typing import List, Dict

# Exit code
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# -----------------------------------------------------------------------------
# Argument Parsing
# -----------------------------------------------------------------------------


def parse_arguments():
    """
    Parse commandline arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file",
        help="The input data to process (JSON format, one entry per line)",
        nargs="?",
        type=str,
    )

    return parser.parse_args()


# -----------------------------------------------------------------------------
# I/O
# -----------------------------------------------------------------------------


def read_from_stdin():
    """
    Read the input data from standard input.
    :return The internal representation of the data
    """
    return [json.loads(l) for l in fileinput.input()]


def read_from_file(path: str) -> List[Dict]:
    """
    Read the input data from the file at `path`.
    :param path The input file path
    :return The internal representation of the data
    """
    return [json.loads(l) for l in fileinput.input(path)]


def read_input(path: str) -> List[Dict]:
    """
    Read the input data from `input_path`.
    :param path The path to the input file, or `None`
    :return A list of JSON objects that represent
    the set of input data to postprocess
    """
    return read_from_file(path) if path is not None else read_from_stdin()


# -----------------------------------------------------------------------------
# PostProcessing
# -----------------------------------------------------------------------------


def process(data: List[Dict]):
    """
    Perform some simple processing of the data.
    :param data The input data
    """

    # No processing to do if no data
    if len(data) == 0:
        return None

    # Initialize counts to 0 for each label
    results = {k: 0 for k in data[0].keys()}
    for sample in data:
        for label, flag in sample.items():
            results[label] += flag

    # Normalize the results
    count = len(data)
    return {k: v / count for k, v in results.items()}


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    args = parse_arguments()
    data = read_input(args.input_file)

    # Generate a histogram of proportions
    hist = process(data)
    if hist is not None:
        sys.stdout.write(json.dumps(hist))

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
