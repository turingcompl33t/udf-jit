# loop.py
# Lighweight loop benchmark script.

import sys
import time
import json
import math
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
DEFAULT_DB_PORT = "15721"

# The default number of iterations for each benchmark
DEFAULT_N_ITERATIONS = 1

# The minimum and maximum subset sizes
COUNT_MIN = 0
COUNT_MAX = 100000000

# The name of the function we are benchmarking
FUNCTION_NAME = "busyLoop"

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


def run_compiled_at_count(conn, count: int, iterations: int):
    """
    Run the compiled query benchmark.
    :param conn The database connection
    :param count The number of iterations in loop
    :param iterations The number of iterations for benchmark
    :return The average duration
    """
    query = f"SELECT {FUNCTION_NAME}({count});"
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
        for count in tqdm(
            [1 * math.pow(10, i) for i in range(int(math.log(COUNT_MAX, 10)) + 1)]
        ):
            # Initialize results for this subset size
            batch = []

            # Run the benchmarks
            batch.append(run_compiled_at_count(conn, int(count), iterations))

            # Record results
            results[count] = batch

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
