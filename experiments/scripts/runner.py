# runner.py
# Wrapper for running simple benchmarks with psql.

import os
import sys
import time
import argparse
import subprocess

from tqdm import tqdm
from typing import List

# Exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The list of function identifiers
FUNCTION_IDS = ["01", "04", "05", "06", "11", "13", "20a"]

# The default number of iterations for each benchmark
DEFAULT_N_ITERATIONS = 2

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
        "functions_dir", help="The path to the directory containing functions", type=str
    )
    parser.add_argument(
        "--results_out",
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
        "--include",
        help="A comma-separated list of function identifiers to include",
        type=str,
    )
    parser.add_argument(
        "--exclude",
        help="A common-separated list of function identifiers to exclude",
        type=str,
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
    parser.add_argument("--verbose", help="Enable verbose output", action="store_true")
    return parser.parse_args()


def parse_include_list(include_list: str) -> List[str]:
    """
    Parse the comma-separated string of functions to include to a list.
    :param include_list The comma-separated string
    :return A list of the individual function IDs
    """
    return FUNCTION_IDS if include_list is None else include_list.split(",")


def parse_exclude_list(exclude_list: str) -> List[str]:
    """
    Parse the comma-separated string of functions to exclude to a list.
    :param exclude_list The comma-separated string
    :return A list of the individual function IDs
    """
    return [] if exclude_list is None else exclude_list.split(",")


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
    def from_id(functions_dir: str, function_id: str):
        """
        Load a function metdata instance from a function ID.
        :param functions_dir The path to the directory in which functions are located
        :param function_id The function identifier
        :return The FunctionMeta instance
        """
        definition_path = os.path.join(functions_dir, f"fn_{function_id}.sql")
        invocation_path = os.path.join(functions_dir, f"invoke_{function_id}.sql")
        if not os.path.exists(definition_path):
            raise RuntimeError(f"Function definition {definition_path} is missing")
        if not os.path.exists(invocation_path):
            raise RuntimeError(f"Function invocation {invocation_path} is missing")

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


def load_function(conn_meta: ConnectionMeta, function: FunctionMeta, verbose: bool):
    """
    Load a function into the database.
    :param conn_meta The connection metadata
    :param function The function metadata
    :param verbose Enable verbose output
    """
    info(f"Loading function {function.function_id}...")

    p = subprocess.run(
        [*psql_connection(conn_meta), "-f", function.definition_file],
        env={"PGPASSWORD": conn_meta.db_pass},
        capture_output=True,
    )
    if p.returncode != EXIT_SUCCESS:
        raise RuntimeError(f"Failed to load function {function.function_id}")

    if verbose:
        info(f"Loaded function {function.function_id}")


def load_functions(
    conn_meta: ConnectionMeta, functions: List[FunctionMeta], verbose: bool
):
    """
    Load all functions from the benchmark.
    :param conn_meta The connection metadata
    :param functions The list of function metadata objects
    :param verbose Enable verbose output
    """
    for function in functions:
        load_function(conn_meta, function, verbose)


# -----------------------------------------------------------------------------
# Benchmarking
# -----------------------------------------------------------------------------


def benchmark_function(
    conn_meta: ConnectionMeta, function: FunctionMeta, iterations: int, verbose: bool
) -> BenchmarkResult:
    """
    Benchmark a single function.
    :param The connection metadata
    :param function The function metadata
    :param iterations The number of iterations
    :param verbose Enable verbose output
    """

    if verbose:
        info(f"Benchmarking function {function.function_id}...")

    durations = []
    for iter in tqdm(range(iterations)):
        start = time.time()
        p = subprocess.run(
            [*psql_connection(conn_meta), "-f", function.invocation_file],
            env={"PGPASSWORD": conn_meta.db_pass},
            capture_output=True,
        )
        stop = time.time()
        if p.returncode != EXIT_SUCCESS:
            raise RuntimeError("Failed to execute query")
        duration = stop - start
        durations.append(duration)

        if verbose:
            info(
                f"Ran iteration {iter} for function {function.function_id} in {duration} seconds"
            )

    if verbose:
        info(f"Completed benchmark for function {function.function_id}")

    return BenchmarkResult(function.function_id, sum(durations) / len(durations))


def benchmark_functions(
    conn_meta: ConnectionMeta,
    functions: List[FunctionMeta],
    iterations: int,
    verbose: bool,
) -> List[BenchmarkResult]:
    """
    Benchmark all functions.
    :param The connection metadata
    :param functions The list of function metadata objects
    :param iterations The number of iterations
    :param verbose Enable verbose output
    """
    return [benchmark_function(conn_meta, f, iterations, verbose) for f in functions]


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def desired_functions(args) -> List[str]:
    """
    Determine the desired functions to run from commandline arguments.
    :param args The parsed commandline arguments
    :return A list of function identifiers
    """
    functions = [fn_id for fn_id in parse_include_list(args.include)]
    return [
        fn_id for fn_id in functions if fn_id not in parse_exclude_list(args.exclude)
    ]


def main() -> int:
    args = parse_arguments()

    # Save database connection information
    conn_meta = ConnectionMeta(
        args.db_user, args.db_password, args.db_name, args.db_host, args.db_port
    )

    functions = desired_functions(args)
    if len(functions) == 0 or not all(fn_id in FUNCTION_IDS for fn_id in functions):
        error("No functions to test")
        return EXIT_FAILURE

    try:
        functions = [
            FunctionMeta.from_id(args.functions_dir, fn_id) for fn_id in functions
        ]
    except RuntimeError as e:
        error(f"{e}")
        return EXIT_FAILURE

    # Load functions
    load_functions(conn_meta, functions, args.verbose)

    # Run benchmarks
    results = benchmark_functions(conn_meta, functions, args.iterations, args.verbose)

    # Record results
    if args.results_out is not None:
        with open(args.results_out, "w") as f:
            f.write("\n".join([f"{r}" for r in results]))

    # Write results to standard output
    sys.stdout.write("\n".join([f"{r}" for r in results]))
    sys.stdout.write("\n")

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
