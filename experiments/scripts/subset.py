# subset.py
# Create a subset of the input data for loading.

import os
import sys
import argparse

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The file encoding
ENCODING = "latin-1"

# -----------------------------------------------------------------------------
# Logging


def info(msg: str):
    print(f"[+] {msg}")


def error(msg: str):
    print(f"[-] {msg}")


# -----------------------------------------------------------------------------
# Argument Management


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
    return (subset_size > 0) and (subset_size <= 100)


# -----------------------------------------------------------------------------
# File I/O


def line_count(path: str) -> int:
    """
    Compute the line count for file at `path`.
    :param path The path the file
    :return The line count for the file
    """
    return sum(1 for _ in open(path, "r", encoding=ENCODING))


def copy_file(input_path: str, output_path: str, subset_size: int):
    """
    Copy the file contents from `input_path` to `output_path`,
    repecting the specified subset size for lines copied.
    :param input_path The path to the input file
    :param output_path The path to the output file
    :param subset_size The subset size
    """
    # Compute the line count of the input file
    count = line_count(input_path)
    # Compute the corresponding line count for subset
    count = int(max(count * (subset_size / 100.0), 1))

    info(f"Copying {count} lines from {input_path} to {output_path}...")

    with open(input_path, "r", encoding=ENCODING) as input_file:
        with open(output_path, "w", encoding=ENCODING) as output_file:
            for _ in range(count):
                line = input_file.readline()
                output_file.write(line)

    info("Done")


def copy_files(input_dir: str, output_dir: str, subset_size: int):
    """
    Copy files from `input_dir` to `output_dir`,
    respecting the specified subset size for each.
    :param input_dir The path to the input directory
    :param output_dir The path to the output directory
    :param subset_size The subset size
    """
    for filename in os.listdir(input_dir):
        copy_file(
            os.path.join(input_dir, filename),
            os.path.join(output_dir, filename),
            subset_size,
        )


# -----------------------------------------------------------------------------
# Main


def main() -> int:
    input_dir, output_dir, subset_size = parse_arguments()
    if not validate_arguments(input_dir, output_dir, subset_size):
        error("Invalid arguments")
        return EXIT_FAILURE

    copy_files(input_dir, output_dir, subset_size)

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry

if __name__ == "__main__":
    sys.exit(main())
