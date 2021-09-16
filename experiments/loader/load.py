# load.py
# A data loader for NoisePage.

import sys
import argparse
import psycopg2
from contextlib import contextmanager

from psycopg2 import OperationalError

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Database connection defaults
DEFAULT_DB_NAME = "noisepage"
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "15721"

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
    """
    Parse commandline arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", help="The path to the schema file (.sql)", type=str)
    parser.add_argument(
        "data_directory", help="The path the directory with output from dsgen", type=str
    )
    parser.add_argument(
        "--db-name",
        help=f"The database name (default: {DEFAULT_DB_NAME})",
        type=str,
        default=DEFAULT_DB_NAME,
    )
    parser.add_argument(
        "--db-host",
        help=f"The database server host (default: {DEFAULT_DB_HOST})",
        type=str,
        default=DEFAULT_DB_HOST,
    )
    parser.add_argument(
        "--db-port",
        help=f"The database server port (default: {DEFAULT_DB_PORT})",
        type=str,
        default=DEFAULT_DB_PORT,
    )
    return parser.parse_args()


# -----------------------------------------------------------------------------
# Database Connection
# -----------------------------------------------------------------------------


@contextmanager
def connection(
    db_name: str, db_user: str, db_password: str, db_host: str, db_port: str
):
    """
    Context manager for database connection.
    :param db_name The database name
    :param db_user The database user
    :param db_password The user password
    :param db_host The host on which the database accepts connections
    :param db_port The port on which the database accepts connections
    """
    conn = open_connection(db_name, db_user, db_password, db_host, db_port)
    try:
        yield conn
    finally:
        close_connection(conn)


def open_connection(
    db_name: str, db_user: str, db_password: str, db_host: str, db_port: str
):
    """
    Create a connection to the NoisePage server instance.
    NOTE: I took this straight from the RealPython article.
    :param db_name The database name
    :param db_user The database user
    :param db_password The user password
    :param db_host The host on which the database accepts connections
    :param db_port The port on which the database accepts connections
    :return The connection
    :raise RuntimeError in the event the connection fails
    """
    connection = None
    info(f"Connecting to NoisePage server at {db_host}:{db_port}...")
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        info("Connection to NoisePage server successful")
    except OperationalError as e:
        error(f"Failed to connect to NoisePage server: {e}")
        raise RuntimeError("")
    return connection


def close_connection(connection):
    """
    Close a connection to the NoisePage server instance.
    :param connection The connection
    """
    if connection is not None:
        connection.close()
        info("Connection to NoisePage server closed")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> int:
    args = parse_arguments()
    try:
        with connection(args.db_name, "", "", args.db_host, args.db_port) as conn:
            print("Context Manager!")
    except RuntimeError:
        return EXIT_FAILURE

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
