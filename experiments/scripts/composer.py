# composer.py
# Compose a set of benchmarks.

import os
import sys
import shutil
import argparse
import subprocess
from enum import Enum

from server import NoisePageServer
from typing import List

# Process exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# NoisePage database server information
NOISEPAGE_DB_HOST = "localhost"
NOISEPAGE_DB_PORT = "15721"
NOISEPAGE_DB_USER = "postgres"
NOISEPAGE_DB_PASS = "password"
NOISEPAGE_DB_NAME = "noisepage"

# Postgres database server information
POSTGRES_DB_HOST = "localhost"
POSTGRES_DB_PORT = "5432"
POSTGRES_DB_USER = "postgres"
POSTGRES_DB_PASS = "password"
POSTGRES_DB_NAME = "noisepage"

# Excluded functions
EXCLUDED_FUNCTIONS = "06,13"

# The parameters for database subset sizes
MIN_SUBSET_SIZE = 5
MAX_SUBSET_SIZE = 100
SUBSET_SIZE_STEP = 5

# The name of the directory that contains database subset
SUBSET_DIR = "subset"

# The path to the file in which results are recorded
OUTPUT_FILE = "out.txt"

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
    parser.add_argument("noisepage_bin", help="The path to the NoisePage binary")
    parser.add_argument(
        "data_dir", help="The path to the data source directory", type=str
    )

    return parser.parse_args()


# -----------------------------------------------------------------------------
# BenchmarkConfig
# -----------------------------------------------------------------------------


class System(Enum):
    NOISEPAGE = (1,)
    POSTGRES = 2


class BenchmarkConfig:
    """
    The BenchmarkConfig class encapsulates all information required to run a benchmark.
    """

    def __init__(
        self,
        system: System,
        binary: str,
        db_host: str,
        db_port: str,
        db_user: str,
        db_pass: str,
        db_name: str,
        data_dir: str,
    ):
        """
        Initialize a BenchmarkConfig instance.
        """
        self.system = system
        self.binary = binary

        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name
        self.data_dir = data_dir

        self.subset_size = 0

        # An opaque handle for running DBMS server process
        self.server_handle = None


# -----------------------------------------------------------------------------
# Results I/O
# -----------------------------------------------------------------------------


def clear_results():
    """Clear the results file."""
    with open(OUTPUT_FILE, "w") as f:
        f.write("")


def write_result(config: BenchmarkConfig, result: str):
    """
    Write an individual result to the results file.
    :param config The benchmark configuration for the result
    :param result The result to write
    """
    system = "POSTGRES" if config.system == System.POSTGRES else "NOISEPAGE"
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"System: {system} Subset Size: {config.subset_size}\n")
        f.write(result)


# -----------------------------------------------------------------------------
# Server Management
# -----------------------------------------------------------------------------


def start_postgres(config: BenchmarkConfig):
    """
    Start the Postgres server.
    :param config The benchmark configuration
    """
    p = subprocess.run(["sudo", "pg_ctlcluster", "12", "main", "start"])
    if p.returncode != EXIT_SUCCESS:
        raise RuntimeError("Failed to start Postgres server")


def stop_postgres(config: BenchmarkConfig):
    """
    Stop the Postgres server.
    :param config The benchmark configuration
    """
    p = subprocess.run(["sudo", "pg_ctlcluster", "12", "main", "stop"])
    if p.returncode != EXIT_SUCCESS:
        raise RuntimeError("Failed to stop Postgres server")


def start_noisepage(config: BenchmarkConfig):
    """
    Start the NoisePage server.
    :param config The benchmark configuration
    """
    handle = NoisePageServer(config.binary, config.db_pass, config.db_port)
    handle.start()
    config.server_handle = handle


def stop_noisepage(config: BenchmarkConfig):
    """
    Stop the NoisePage server.
    :param config The benchmark configuration
    """
    if config.server_handle is None:
        raise RuntimeError("Missing server handle")
    config.server_handle.stop()
    config.server_handle = None

    # Remove the write-ahead log file;
    # assumes the WAL is written in CWD
    os.remove("wal.log")


def start_server(config: BenchmarkConfig):
    """
    Start the database server.
    :param config The benchmark configuration
    """
    if config.system == System.POSTGRES:
        start_postgres(config)
    elif config.system == System.NOISEPAGE:
        start_noisepage(config)
    else:
        raise RuntimeError("Unrecognized system")


def stop_server(config: BenchmarkConfig):
    """
    Stop the database server.
    :param config The benchmark configuration
    """
    if config.system == System.POSTGRES:
        stop_postgres(config)
    elif config.system == System.NOISEPAGE:
        stop_noisepage(config)
    else:
        raise RuntimeError("Unrecognized system")


# -----------------------------------------------------------------------------
# Subset Directory
# -----------------------------------------------------------------------------


def create_directory(path: str):
    """
    Create a directory.
    :param The path at which the directory is created
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def remove_directory(path: str):
    """
    Remove a directory.
    :param The path at which the directory is removed
    """
    shutil.rmtree(path)


# -----------------------------------------------------------------------------
# Configuration Running
# -----------------------------------------------------------------------------


def run_configuration(config: BenchmarkConfig):
    """
    Run a complete benchmark configuration.
    :param config The configuration to run
    """

    # Create a directory for the database subset
    subset_path = os.path.join(os.getcwd(), SUBSET_DIR)
    create_directory(subset_path)

    # Generate the subset
    p = subprocess.run(
        ["python", "subset.py", config.data_dir, subset_path, f"{config.subset_size}"]
    )
    if p.returncode != EXIT_SUCCESS:
        raise RuntimeError("Failed to create subset")

    # Start the database
    start_server(config)

    # Load the database
    p = subprocess.run(
        [
            "python",
            "loader.py",
            "../ddl/schema-dirty.sql",
            subset_path,
            "--db-host",
            config.db_host,
            "--db-port",
            config.db_port,
            "--db-user",
            config.db_user,
            "--db-password",
            config.db_pass,
            "--db-name",
            config.db_name,
        ]
    )
    if p.returncode != EXIT_SUCCESS:
        raise RuntimeError("Failed to load database")

    # Run the benchmark
    p = subprocess.run(
        [
            "python",
            "runner.py",
            "../plpgsql/dirty/",
            "--exclude",
            EXCLUDED_FUNCTIONS,
            "--db-host",
            config.db_host,
            "--db-port",
            config.db_port,
            "--db-user",
            config.db_user,
            "--db-password",
            config.db_pass,
            "--db-name",
            config.db_name,
        ],
        capture_output=True,
    )
    if p.returncode != EXIT_SUCCESS:
        raise RuntimeError("Failed to run benchmark")

    write_result(config, p.stdout.decode("utf-8"))

    # Stop the database
    stop_server(config)

    # Cleanup
    remove_directory(subset_path)


def run_configurations(configs: List[BenchmarkConfig]):
    """
    Run the specified configurations under various subset sizes.
    :param configs The list of configurations
    """

    clear_results()
    for subset_size in range(
        MIN_SUBSET_SIZE, MAX_SUBSET_SIZE + SUBSET_SIZE_STEP, SUBSET_SIZE_STEP
    ):
        for config in configs:
            config.subset_size = subset_size
            run_configuration(config)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> int:
    args = parse_arguments()
    configs = [
        BenchmarkConfig(
            System.POSTGRES,
            "",
            POSTGRES_DB_HOST,
            POSTGRES_DB_PORT,
            POSTGRES_DB_USER,
            POSTGRES_DB_PASS,
            POSTGRES_DB_NAME,
            args.data_dir,
        ),
        BenchmarkConfig(
            System.NOISEPAGE,
            args.noisepage_bin,
            NOISEPAGE_DB_HOST,
            NOISEPAGE_DB_PORT,
            NOISEPAGE_DB_USER,
            NOISEPAGE_DB_PASS,
            NOISEPAGE_DB_NAME,
            args.data_dir,
        ),
    ]

    try:
        run_configurations(configs)
    except RuntimeError as e:
        error(f"Runtime Error: {e}")
        return EXIT_FAILURE

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
