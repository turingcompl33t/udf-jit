# generator.py
# Data generator for custom tables.
#
# usage: generator.py [-h] output_path
#
# positional arguments:
#   output_path  The path to the directory in which data is generated
#
# optional arguments:
#   -h, --help   show this help message and exit


import os
import sys
import random
import argparse

from tqdm import tqdm
from enum import Enum
from typing import List

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Values for the `integers` table
INTEGERS_MIN_VAL = 0
INTEGERS_MAX_VAL = 100000000

# Number of rows in the `integers` table
INTEGERS_N_ROWS = 1000

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------


def info(message: str):
    """Log an informational message."""
    print(f"[+] {message}")


def error(message: str):
    """Log an error message."""
    print(f"[-] {message}")


# -----------------------------------------------------------------------------
# Argument Parsing
# -----------------------------------------------------------------------------


def parse_arguments():
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_path",
        help="The path to the directory in which data is generated",
        type=str,
    )
    return parser.parse_args()


# -----------------------------------------------------------------------------
# Schema Definition
# -----------------------------------------------------------------------------


class ColumnType(Enum):
    """The ColumnType enumeration describes SQL schema column types."""

    TINYINT = 0
    INTEGER = 1
    SMALLINT = 2
    BIGINT = 3
    FLOAT = 4
    DOUBLE = 5
    DECIMAL = 6
    VARCHAR = 7


class Column:
    """The Column class represents a SQL table column."""

    def __init__(self, name: str, type: ColumnType):
        """
        Initialize a new Column instance.
        :param name The name of the column
        :param type The column type
        """
        self.name = name
        self.type = type


class Schema:
    @staticmethod
    def from_columns(name: str, columns: List[Column]):
        """
        Construct a new Schema from the given `name` and `columns`.
        :param name The name of the table
        :param columns The list of column definitions
        :return The Schema
        """
        return Schema(name, columns)

    """ The Schema class represents a SQL table schema. """

    def __init__(self, name: str, columns: List[Column]):
        """
        Initialize a new Schema instance.
        :param name The name of the table
        :param columns The list of column definitions
        """
        self.name = name
        self.columns = columns


# -----------------------------------------------------------------------------
# Data Generators
# -----------------------------------------------------------------------------


class Generator:
    """
    The Generator class encapsulates all of
    the information necessary to generate data.
    """

    def __init__(self, path: str, schema: Schema, gen_fns, rows: int):
        """
        Initialize a new Generator instance.
        :param path The path to the data directory
        :param schema The table schema for which to generate data
        :param gen_fns The generator callback functions
        :rows The number of rows to generate
        """
        assert len(schema.columns) == len(
            gen_fns
        ), "Must have a generator function for each column in schema."
        # The path to the output file
        self.path = f"{os.path.join(path, schema.name)}.dat"
        # The schema
        self.schema = schema
        # The generator functions
        self.gen_fns = gen_fns
        # The number of rows to generate
        self.rows = rows

    def run(self):
        """Run the generator."""
        info(f"Generating data for {self.schema.name}...")

        with open(self.path, "w") as f:
            for _ in tqdm(range(self.rows)):
                f.write(f"{'|'.join([str(gen_fn()) for gen_fn in self.gen_fns])}\n")

        info(f"Generation for {self.schema.name} complete")


def random_integer(min: int, max: int) -> int:
    """
    A data generator for random integers on [`min`, `max`].
    :param min The minimum value in the range (inclusive)
    :param max The maximum value in the range (inclusive)
    :return The value
    """
    return random.randint(min, max)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> int:
    args = parse_arguments()
    generators = [
        Generator(
            args.output_path,
            Schema.from_columns("integers", [Column("x", ColumnType.INTEGER)]),
            [lambda: random_integer(INTEGERS_MIN_VAL, INTEGERS_MAX_VAL)],
            INTEGERS_N_ROWS,
        )
    ]
    for generator in generators:
        generator.run()

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
