# runner.py
# Wrapper for running simple benchmarks with psql.

import os
import sys
import time
import argparse
import subprocess

from typing import List

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The list of function identifiers
FUNCTION_IDS = ["01", "04", "05", "06", "11", "13", "20a"]
# The relative path to the directory containing
# the function definitions and invoking queries
FUNCTIONS_DIR = "../plpgsql/"

# The default number of iterations for each benchmark
DEFAULT_N_ITERATIONS = 1

# The default database connection parameters
DEFAULT_DB_USER = "postgres"
DEFAULT_DB_PASS = "password"
DEFAULT_DB_NAME = "noisepage"
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "5432"

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
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "results_out",
        help="The path to the file to which results are written",
        type=str,
    )
    parser.add_argument(
        "--iterations",
        help=f"The number of iterations run for each function (default: {DEFAULT_N_ITERATIONS})",
        type=int,
        default=DEFAULT_N_ITERATIONS,
    )
    parser.add_argument(
        "--db-user", help="The database user", type=str, default=DEFAULT_DB_USER
    )
    parser.add_argument(
        "--db-password",
        help="The database user password",
        type=str,
        default=DEFAULT_DB_PASS,
    )
    parser.add_argument(
        "--db-name", help="The database name", type=str, default=DEFAULT_DB_NAME
    )
    parser.add_argument(
        "--db-host",
        help="The address at which database accepts connections",
        type=str,
        default=DEFAULT_DB_HOST,
    )
    parser.add_argument(
        "--db-port",
        help="The port at which database accepts connections",
        type=str,
        default=DEFAULT_DB_PORT,
    )
    return parser.parse_args()


# -----------------------------------------------------------------------------
# Connection Metadata
# -----------------------------------------------------------------------------


class ConnectionMeta:
    """
    The ConnectionMeta class encapsulates metdata
    for a database connection session.
    """

    def __init__(
        self, db_user: str, db_pass: str, db_name: str, db_host: str, db_port: str
    ):
        """Initialize a new ConnectionMeta instance."""
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port


# -----------------------------------------------------------------------------
# Function Metadata
# -----------------------------------------------------------------------------


class FunctionMeta:
    """
    The FunctionMeta class contains all metadata
    required to execute a benchmark for a function.
    """

    @staticmethod
    def from_id(function_id: str):
        """
        Load a function metdata instance from a function ID.
        :param function_id The function identifier
        :return The FunctionMeta instance
        """
        definition_path = os.path.join(FUNCTIONS_DIR, f"fn_{function_id}.sql")
        invocation_path = os.path.join(FUNCTIONS_DIR, f"invoke_{function_id}.sql")
        return FunctionMeta(function_id, definition_path, invocation_path)

    def __init__(self, function_id: str, definition_file: str, invocation_file: str):
        """
        Initialize a new FunctionMeta instance.
        :param function_id A human-readable identifier for the function
        :param definition_file The path to function definition file
        :param invocation_file The path to the function invocation file
        """
        self.function_id = function_id
        self.definition_file = definition_file
        self.invocation_file = invocation_file


# -----------------------------------------------------------------------------
# Benchmark Result
# -----------------------------------------------------------------------------


class BenchmarkResult:
    """
    The BenchmarkResult encapsulates a benchmark result.
    """

    def __init__(self, function_id: str, duration: float):
        """
        Initialize a new BenchmarkResult instance.
        :param function_id The function identifier
        :param duration The benchmark duration
        """
        self.function_id = function_id
        self.duration = duration

    def __str__(self):
        """Return a string representation of the result."""
        return f"Function {self.function_id} : {self.duration} seconds"


# -----------------------------------------------------------------------------
# Generic Helpers
# -----------------------------------------------------------------------------


def psql_connection(conn_meta: ConnectionMeta) -> List[str]:
    """
    Return the base command for connecting to
    a database instance with psql.
    :param conn_meta The connection metadata
    :return The base command
    """
    return [
        "psql",
        "-U",
        conn_meta.db_user,
        "-w",
        "-d",
        conn_meta.db_name,
        "-h",
        conn_meta.db_host,
        "-p",
        conn_meta.db_port,
    ]


# -----------------------------------------------------------------------------
# Function Definition
# -----------------------------------------------------------------------------


def load_function(conn_meta: ConnectionMeta, function: FunctionMeta):
    """
    Load a function into the database.
    :param conn_meta The connection metadata
    :param function The function metadata
    """
    info(f"Loading function {function.function_id}...")

    p = subprocess.run(
        [*psql_connection(conn_meta), "-f", function.definition_file],
        env={"PGPASSWORD": conn_meta.db_pass},
        capture_output=True,
    )
    if p.returncode != EXIT_SUCCESS:
        raise RuntimeError(f"Failed to load function {function.function_id}")

    info(f"Loaded function {function.function_id}")


def load_functions(conn_meta: ConnectionMeta, functions: List[FunctionMeta]):
    """
    Load all functions from the benchmark.
    :param conn_meta The connection metadata
    :param functions The list of function metadata objects
    """
    for function in functions:
        load_function(conn_meta, function)


# -----------------------------------------------------------------------------
# Benchmarking
# -----------------------------------------------------------------------------


def benchmark_function(
    conn_meta: ConnectionMeta, function: FunctionMeta, iterations: int
) -> BenchmarkResult:
    """
    Benchmark a single function.
    :param The connection metadata
    :param function The function metadata
    :param iterations The number of iterations
    """
    durations = []
    for _ in range(iterations):
        start = time.time()
        p = subprocess.run(
            [*psql_connection(conn_meta), "-f", function.invocation_file],
            env={"PGPASSWORD": conn_meta.db_pass},
            capture_output=True,
        )
        stop = time.time()
        if p.returncode != EXIT_SUCCESS:
            raise RuntimeError("Failed to execute query")
        durations.append(stop - start)

    return BenchmarkResult(function.function_id, sum(durations) / len(durations))


def benchmark_functions(
    conn_meta: ConnectionMeta, functions: List[FunctionMeta], iterations: int
) -> List[BenchmarkResult]:
    """
    Benchmark all functions.
    :param The connection metadata
    :param functions The list of function metadata objects
    :param The number of iterations
    """
    return [benchmark_function(conn_meta, f, iterations) for f in functions]


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> int:
    args = parse_arguments()

    # Save database connection information
    conn_meta = ConnectionMeta(
        args.db_user, args.db_password, args.db_name, args.db_host, args.db_port
    )

    # Load function metatdata
    functions = [FunctionMeta.from_id(fn_id) for fn_id in FUNCTION_IDS]

    # Load functions
    load_functions(conn_meta, functions)

    # Run benchmarks
    results = benchmark_functions(conn_meta, functions, args.iterations)
    for result in results:
        print(result)

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
