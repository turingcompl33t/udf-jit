# subset.py
# Create a subset of the input data for loading.

import os
import sys
import argparse

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def info(msg: str):
    print(f"[+] {msg}")


def error(msg: str):
    print(f"[-] {msg}")


def parse_arguments():
    """
    Parse commandline arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_dir",
        help="The path to the directory in which data is located.",
        type=str,
    )
    parser.add_argument(
        "output_dir",
        help="The path to the directory in which subset is created.",
        type=str,
    )
    parser.add_argument(
        "subset_size",
        help="The size of the subset, as a percentage of the input data.",
        type=int,
    )
    args = parser.parse_args()
    return (args.input_dir, args.output_dir, args.subset_size)


def validate_arguments(input_dir: str, output_dir: str, subset_size: int) -> bool:
    """
    Validate commandline arguments.
    :param input_dir The path to the input directory
    :param output_dir The path to the output directory
    :param subset_size The size of the subset
    :return `true` if arguments are valid, `false` otherwise
    """
    if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
        return False
    if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
        return False
    return subset_size > 0 and subset_size <= 100


def main() -> int:
    input_dir, output_dir, subset_size = parse_arguments()
    if not validate_arguments(input_dir, output_dir, subset_size):
        error("Invalid arguments")
        return EXIT_FAILURE

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
