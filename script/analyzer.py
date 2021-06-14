# analyzer.py
# UNIX-style PL/pgSQL UDF analyzer.

import sys
import json
import argparse
from typing import Dict

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# -----------------------------------------------------------------------------
# Commandline Parsing
# -----------------------------------------------------------------------------


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input", help="The input JSON parse tree", nargs="?", type=str, default=None
    )

    return parser.parse_args()


# -----------------------------------------------------------------------------
# Parse Tree I/O
# -----------------------------------------------------------------------------


def read_from_file(path: str) -> Dict:
    """
    Read the JSON-formatted parse tree from `path`.
    :param path The input path
    :return The in-memory JSON representation of the parse tree
    """
    with open(path, "r") as f:
        return json.loads(f.read())


def read_from_stdin() -> str:
    """
    Read the JSON-formatted parse tree from standard input.
    :return The in-memory JSON representation of the parse tree
    """
    return json.loads(sys.stdin.read())


def read_parse_tree(path: str) -> Dict:
    """
    Read the input parse tree.
    :param path The path to the input file from which to read the procedure.
    :return The in-memory JSON representation of the parse tree.
    """
    return read_from_file(path) if path is not None else read_from_stdin()


# -----------------------------------------------------------------------------
# Parse Tree Analysis
# -----------------------------------------------------------------------------


def analyze(parse_tree: Dict) -> Dict:
    """
    Analyze the parse tree to extract raw token counts.
    :param parse_tree The input parse tree
    :return The results of the analysis
    """
    # Isolate actions within the function
    action = parse_tree["PLpgSQL_function"]["action"]

    # Locate the outermost statement block
    # TODO: Is it always the case there is only a single such block?
    body = action["PLpgSQL_stmt_block"]["body"]

    features = {}
    for feature in body:
        key = [k for k in feature.keys()][0]
        if key in features:
            features[key] = features[key] + 1
        else:
            features[key] = 1

    return features


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    args = parse_arguments()

    # Read the parse tree
    parse_tree = read_parse_tree(args.input)

    # Perform the analysis
    analysis = analyze(parse_tree)
    print(analysis)

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
