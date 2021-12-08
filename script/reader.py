# reader.py
# Read the CSV file of functions to a CSV file
# with features extracted, ready for load to DB.

import os
import sys
import json
import argparse
import pandas as pd

from tqdm import tqdm
from typing import Tuple
from parser import parse_procedure
from analyzer import FEATURE_KEYS, get_features

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The name of the output file
OUTPUT_FILENAME = "features.csv"

# Procedure parser binary setup
PROC_PARSER_NAME = "proc_parser"
PROC_PARSER_DIRECTORY = "sql"
PROC_PARSER_BINARY_PATH = os.path.join(
    os.getcwd(), PROC_PARSER_DIRECTORY, PROC_PARSER_NAME
)

# -----------------------------------------------------------------------------
# Logging


def info(msg: str):
    """
    Log an informational message.
    :param msg The message
    """
    print(f"[+] {msg}")


def error(msg: str):
    """
    Log an error message.
    :param msg The message
    """
    print(f"[-] {msg}")


# -----------------------------------------------------------------------------
# Argument Parsing


def parse_arguments() -> Tuple[str, str]:
    """
    Parse commandline arguments.
    :return (input_path, output_path)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="The path to the input file.", type=str)
    parser.add_argument(
        "output_path", help="The path to the output directory.", type=str
    )
    args = parser.parse_args()
    return args.input_path, args.output_path


def validate_arguments(input_path: str, output_path: str) -> bool:
    """
    Validate commandline arguments.
    :param input_path The path to the input file
    :param output_path The path to the output file
    :return `True` if validation passes, `False` otherwise
    """
    iv = os.path.exists(input_path) and os.path.isfile(input_path)
    ov = os.path.exists(output_path) and os.path.isdir(output_path)
    return iv and ov


# -----------------------------------------------------------------------------
# Processing


def parse(text: str) -> str:
    """
    Parse function body text to JSON string.
    :param text The raw function text
    :return The parsed function
    """
    return json.dumps(parse_procedure(text, PROC_PARSER_BINARY_PATH))


def process(input_path: str, output_path: str):
    """
    Process raw data at `input_path` to `output_path`.
    :param input_path The input path to raw functions
    :param output_path The path to which results are saved
    """
    columns = ["text"] + list(set([name.lower() for name in FEATURE_KEYS.values()]))

    df = pd.DataFrame(columns=columns)
    dd = pd.read_csv(input_path)
    for row in tqdm(dd.iterrows(), total=len(dd)):
        t = row[1]["text"]

        p = parse(t)
        if p is None:
            continue

        f = get_features(p)
        if f is None:
            continue

        r = {"text": t}
        for key in FEATURE_KEYS.values():
            r[key.lower()] = f[key]

        df = df.append(r, ignore_index=True)

    # Save the completed dataframe
    df.to_csv(output_path)


# -----------------------------------------------------------------------------
# Main


def main() -> int:
    input_path, output_path = parse_arguments()
    if not validate_arguments(input_path, output_path):
        error("Invalid arguments")
        return EXIT_FAILURE

    info("Processing...")
    out = os.path.join(output_path, OUTPUT_FILENAME)
    try:
        process(input_path, out)
    except RuntimeError as e:
        error(f"{e}")
        return EXIT_FAILURE

    info("Done.")

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry

if __name__ == "__main__":
    sys.exit(main())
