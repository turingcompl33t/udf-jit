# to_sqlite.py

import sys
import csv_to_sqlite

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

INPUT = "input-prep/features.csv"
OUTPUT = "input-prep/features.sqlite"

def main() -> int:
    options = csv_to_sqlite.CsvOptions()
    csv_to_sqlite.write_csv([INPUT], OUTPUT, options)
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())
