# sql.py
# Common SQL helpers.

import psycopg2

from contextlib import contextmanager
from psycopg2 import OperationalError

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
    Create a connection to the database server instance.
    :param db_name The database name
    :param db_user The database user
    :param db_password The user password
    :param db_host The host on which the database accepts connections
    :param db_port The port on which the database accepts connections
    :return The connection
    :raise RuntimeError in the event the connection fails
    """
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError as e:
        raise RuntimeError(f"Failed to connect to database server: {e}")
    return connection


def close_connection(connection):
    """
    Close a connection to the NoisePage server instance.
    :param connection The connection
    """
    if connection is not None:
        connection.commit()
        connection.close()


# -----------------------------------------------------------------------------
# ServerConfig
# -----------------------------------------------------------------------------


class ServerConfig:
    """
    The ServerConfig class encapsulates a database server configuration.
    """

    @staticmethod
    def from_args(args):
        """
        Construct a ServerConfig instance from a a ArgParse object.
        :param args The arguments object
        """
        return ServerConfig(
            args.db_user, args.db_password, args.db_name, args.db_host, args.db_port
        )

    def __init__(
        self, db_user: str, db_pass: str, db_name: str, db_host: str, db_port: str
    ):
        """
        Initialize a new ServerConfig instance.
        :param db_user The database user
        :param db_pass The database password
        :param db_name The database name
        :param db_host The database host
        :param db_port The database port
        """
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
