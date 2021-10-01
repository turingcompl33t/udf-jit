# call.py
# Overhead of a function call benchmark script.

import sys
import time
import json
import argparse

from tqdm import tqdm
from typing import Dict, List
from psycopg2 import OperationalError
from sql import connection, ServerConfig

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Default database configuration
DEFAULT_DB_USER = "postgres"
DEFAULT_DB_PASS = "password"
DEFAULT_DB_NAME = "noisepage"
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "5432"

# The default number of iterations for each benchmark
DEFAULT_N_ITERATIONS = 2

# The minimum and maximum subset sizes
SUBSET_SIZE_MIN = 0
SUBSET_SIZE_MAX = 100
# The step between individual iterations
SUBSET_SIZE_STEP = 5

# The name of the table
TABLE_NAME = "integers"
# The number of rows in `integers`
TABLE_SIZE = 100000000
# The name of the function we are benchmarking
FUNCTION_NAME = "addOne"

# The name of the output file
RESULTS_FILE_OUT = "results.json"

# -----------------------------------------------------------------------------
# Argument Parsing
# -----------------------------------------------------------------------------


def parse_arguments():
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--iterations",
        help="The number of iterations for each benchmark.",
        type=int,
        default=DEFAULT_N_ITERATIONS,
    )
    parser.add_argument(
        "--db-user", help="The database user.", type=str, default=DEFAULT_DB_USER
    )
    parser.add_argument(
        "--db-password",
        help="The database password.",
        type=str,
        default=DEFAULT_DB_PASS,
    )
    parser.add_argument(
        "--db-name", help="The database name.", type=str, default=DEFAULT_DB_NAME
    )
    parser.add_argument(
        "--db-host",
        help="The host on which the database server listens.",
        type=str,
        default=DEFAULT_DB_HOST,
    )
    parser.add_argument(
        "--db-port",
        help="The port on which the database server listens.",
        type=str,
        default=DEFAULT_DB_PORT,
    )
    return parser.parse_args()


# -----------------------------------------------------------------------------
# Benchmarking
# -----------------------------------------------------------------------------


def execute_query(connection, query: str):
    """
    Execute the query against the database instance.
    :param connection The database connection to use
    :param query The query text
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except OperationalError as e:
        raise RuntimeError(f"Failed to execute query: {e}")


def average_duration_over(conn, query: str, iterations: int):
    """
    Compute the average duration required to execute
    `query` over the specified number of iterations.
    :param conn The database connection
    :param query The query to execute
    :param iterations The number of iterations to run
    """
    durations = []
    for _ in range(iterations):
        start = time.time()
        execute_query(conn, query)
        stop = time.time()
        durations.append(stop - start)

    return sum(durations) / len(durations)


def run_baseline_at_limit(conn, limit: int, iterations: int) -> float:
    """
    Run the baseline query benchmark.
    :param conn The database connection
    :param limit The value for LIMIT clause
    :param iterations The number of iterations
    :return The average duration
    """
    query = f"SELECT x FROM {TABLE_NAME} LIMIT {limit};"
    return average_duration_over(conn, query, iterations)


def run_inlined_at_limit(conn, limit: int, iterations: int):
    """
    Run the inlined query benchmark.
    :param conn The database connection
    :param limit The value for LIMIT clause
    :param iterations The number of iterations
    :return The average duration
    """
    query = f"SELECT x + 1 FROM {TABLE_NAME} LIMIT {limit};"
    return average_duration_over(conn, query, iterations)


def run_compiled_at_limit(conn, limit: int, iterations: int):
    """
    Run the compiled query benchmark.
    :param conn The database connection
    :param limit The value for LIMIT clause
    :param iterations The number of iterations
    :return The average duration
    """
    query = f"SELECT {FUNCTION_NAME}(x) FROM {TABLE_NAME} LIMIT {limit};"
    return average_duration_over(conn, query, iterations)


def run(config: ServerConfig, iterations: int) -> Dict[int, List[float]]:
    """
    Run the benchmark.
    :param config The database server configuation
    :param iterations The number of iterations for each run
    :return The results dictionary
    """
    results = {}
    with connection(
        config.db_name, config.db_user, config.db_pass, config.db_host, config.db_port
    ) as conn:
        conn.autocommit = True
        for subset_size in tqdm(
            range(SUBSET_SIZE_MIN, SUBSET_SIZE_MAX + SUBSET_SIZE_STEP, SUBSET_SIZE_STEP)
        ):
            # Initialize results for this subset size
            batch = []

            # Compute the limit for this subset size
            limit = int((subset_size / 100.0) * TABLE_SIZE)

            # Run the benchmarks
            batch.append(run_baseline_at_limit(conn, limit, iterations))
            batch.append(run_inlined_at_limit(conn, limit, iterations))
            batch.append(run_compiled_at_limit(conn, limit, iterations))

            # Record results
            results[subset_size] = batch

    return results


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> int:
    args = parse_arguments()
    config = ServerConfig.from_args(args)

    results = None
    try:
        results = run(config, args.iterations)
    except RuntimeError as e:
        print(f"[-] {e}")
        return EXIT_FAILURE

    # Write the results file
    with open(RESULTS_FILE_OUT, "w") as f:
        json.dump(results, f)

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
