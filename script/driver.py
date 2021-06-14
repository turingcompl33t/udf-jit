# driver.py

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

# Tokenizer binary setup
TOKENIZER_DEFAULT_NAME = "tokenizer"
TOKENIZER_DEFAULT_DIRECTORY = "tokenizer"
TOKENIZER_DEFAULT_BINARY_PATH = os.path.join(
    os.getcwd(), TOKENIZER_DEFAULT_DIRECTORY, TOKENIZER_DEFAULT_NAME
)

PROC = "CREATE OR REPLACE FUNCTION cs_fmt_browser_version(v_name varchar, \
                                                  v_version varchar) \
RETURNS varchar AS $$ \
BEGIN \
    IF v_version IS NULL THEN \
        RETURN v_name; \
    END IF; \
    RETURN v_name || '/' || v_version; \
END; \
$$ LANGUAGE plpgsql;"

# -----------------------------------------------------------------------------
# Commandline Parsing
# -----------------------------------------------------------------------------


def parse_arguments() -> Dict:
    """
    Parse commandline arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--binary-path",
        help="The path to the tokenizer binary",
        default=TOKENIZER_DEFAULT_BINARY_PATH,
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
# Commandline Parsing
# -----------------------------------------------------------------------------


def parse_procedure(proc: str, bin_path: str) -> Dict:
    """
    Parse the procedure `proc` and return parse tree as a JSON dictionary.
    :param proc The input procedure
    :param path The path to the tokenizer executable
    :return The parse tree for the procedure as a JSON dictionary, None on failure
    """

    # Spawn the subprocess
    process = Popen([bin_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    # Write the procedure and terminating EOF
    stdout, stderr = process.communicate(input=proc.encode())
    if len(stderr) != 0:
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

    tokenizer = args.binary_path
    log_level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=log_level)

    proc = parse_procedure(PROC, tokenizer)
    if proc is None:
        logging.warning("Failed to parse procedure")
        return EXIT_FAILURE

    logging.info("Successfully parsed procedure")
    print(proc)

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
