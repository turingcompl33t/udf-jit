# parser.py
# UNIX-style PL/pgSQL procedure parser.
#
# Parses a single input user-defined function in PL/pgSQL
# to the raw Postgres parse tree using libpg_query.
#
# Output is textual format via a JSON dictionary to standard output.
#
# usage: parser.py [-h] [-b BINARY_PATH] [-v] [input_file]
#
# positional arguments:
#   input_file            The path to the file that contains the input procedure
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -b BINARY_PATH, --binary-path BINARY_PATH
#                         The path to the procedure parser binary
#   -v, --verbose         Enable verbose debugging output

import os
import sys
import json
import logging
import argparse
from typing import Dict
from subprocess import Popen, PIPE

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Procedure parser binary setup
PROC_PARSER_DEFAULT_NAME = "proc_parser"
PROC_PARSER_DEFAULT_DIRECTORY = "sql"
PROC_PARSER_DEFAULT_BINARY_PATH = os.path.join(
    os.getcwd(), PROC_PARSER_DEFAULT_DIRECTORY, PROC_PARSER_DEFAULT_NAME
)

# -----------------------------------------------------------------------------
# Commandline Parsing
# -----------------------------------------------------------------------------


def parse_arguments() -> Dict:
    """
    Parse commandline arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file",
        help="The path to the file that contains the input procedure",
        nargs="?",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-b",
        "--binary-path",
        help="The path to the procedure parser binary",
        default=PROC_PARSER_DEFAULT_BINARY_PATH,
        type=str,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose debugging output",
        default=False,
        action="store_true",
    )
    return parser.parse_args()


# -----------------------------------------------------------------------------
# Procedure I/O
# -----------------------------------------------------------------------------


def read_from_file(path: str) -> str:
    """
    Read a procedure from the specified file.
    :param path The file path
    :return The procedure string
    """
    with open(path, "r") as f:
        return f.read()


def read_from_stdin() -> str:
    """
    Read a procedure from standard input.
    :return The procedure string
    """
    return sys.stdin.read()


def read_procedure(path: str) -> str:
    """
    Read the procedure from the file specified by `path`.
    """
    return read_from_file(path) if path is not None else read_from_stdin()


def write_procedure(parse_tree: Dict):
    """
    Write the procedure parse tree to standard output.
    :param parse_tree The parse tree, as an in-memory JSON object.
    """
    sys.stdout.write(json.dumps(parse_tree))


# -----------------------------------------------------------------------------
# Procedure Parsing
# -----------------------------------------------------------------------------


def parse_procedure(proc: str, bin_path: str) -> Dict:
    """
    Parse the procedure `proc` and return parse tree as a JSON dictionary.
    :param proc The input procedure
    :param path The path to the procedure parser executable
    :return The parse tree for the procedure as a JSON dictionary, None on failure
    """

    # Spawn the subprocess
    process = Popen([bin_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    # Write the procedure and terminating EOF
    stdout, stderr = process.communicate(input=proc.encode())
    if len(stderr) != 0:
        print(stderr)
        return None

    # Load the JSON output
    parse_tree = json.loads(stdout)

    # We only expect to parse a single procedure
    return None if len(parse_tree) == 0 else parse_tree[0]


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    args = parse_arguments()

    parser = args.binary_path

    log_level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=log_level)

    proc = read_procedure(args.input_file)
    if proc is None:
        logging.warning("Failed to read procedure")
        return EXIT_FAILURE

    proc = parse_procedure(proc, parser)
    if proc is None:
        logging.warning("Failed to parse procedure")
        return EXIT_FAILURE

    logging.info("Successfully parsed procedure")
    write_procedure(proc)

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
