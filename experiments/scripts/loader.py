# loader.py
# A data loader for SQL ProcBench benchmark.
#
# usage: loader.py [-h] [--create-only] [--db-user DB_USER]
#                  [--db-password DB_PASSWORD] [--db-name DB_NAME]
#                  [--db-host DB_HOST] [--db-port DB_PORT]
#                  schema_file data_directory
#
# positional arguments:
#   schema_file           The path to the schema file (.sql)
#   data_directory        The path the directory with output from dsgen
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --create-only         Create tables only (do not load data)
#   --db-user DB_USER     The database user (default:
#   --db-password DB_PASSWORD
#                         The database user password (default: )
#   --db-name DB_NAME     The database name (default: noisepage)
#   --db-host DB_HOST     The database server host (default: localhost)
#   --db-port DB_PORT     The database server port (default: 15721)


import os
import sys
import argparse
import psycopg2
from contextlib import contextmanager

from tqdm import tqdm
from typing import List
from psycopg2 import OperationalError

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Database connection defaults
DEFAULT_DB_USER = ""
DEFAULT_DB_PASS = ""
DEFAULT_DB_NAME = "noisepage"
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "15721"

# The column delimiter in data source files
DATA_SOURCE_FILE_DELIMITER = "|"

# Maps from table name -> table data filename
TABLE_DATA_SOURCES = {
    "store_sales": "store_sales.dat",
    "store_returns": "store_returns.dat",
    "catalog_sales": "catalog_sales.dat",
    "catalog_returns": "catalog_returns.dat",
    "web_sales": "web_sales.dat",
    "web_returns": "web_returns.dat",
    "inventory": "inventory.dat",
    "store": "store.dat",
    "call_center": "call_center.dat",
    "catalog_page": "catalog_page.dat",
    "web_site": "web_site.dat",
    "web_page": "web_page.dat",
    "warehouse": "warehouse.dat",
    "customer": "customer.dat",
    "customer_address": "customer_address.dat",
    "customer_demographics": "customer_demographics.dat",
    "date_dim": "date_dim.dat",
    "household_demographics": "household_demographics.dat",
    "item": "item.dat",
    "income_band": "income_band.dat",
    "promotion": "promotion.dat",
    "reason": "reason.dat",
    "ship_mode": "ship_mode.dat",
    "time_dim": "time_dim.dat",
    # NOTE: The history tables are populated with the same data
    # as the standard fact tables for the TPC-DS benchmark
    "store_sales_history": "store_sales.dat",
    "store_returns_history": "store_returns.dat",
    "catalog_sales_history": "catalog_sales.dat",
    "catalog_returns_history": "catalog_returns.dat",
    "web_sales_history": "web_sales.dat",
    "web_returns_history": "web_returns.dat",
    "inventory_history": "inventory.dat",
}

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
    parser.add_argument(
        "schema_file", help="The path to the schema file (.sql)", type=str
    )
    parser.add_argument(
        "data_directory", help="The path the directory with output from dsgen", type=str
    )
    parser.add_argument(
        "--create-only",
        help="Create tables only (do not load data)",
        action="store_true",
    )
    parser.add_argument(
        "--db-user",
        help=f"The database user (default: {DEFAULT_DB_USER}",
        type=str,
        default=DEFAULT_DB_USER,
    )
    parser.add_argument(
        "--db-password",
        help=f"The database user password (default: {DEFAULT_DB_PASS})",
        type=str,
        default=DEFAULT_DB_PASS,
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
    info(f"Connecting to database server at {db_host}:{db_port}...")
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        info("Connection to database server successful")
    except OperationalError as e:
        error(f"Failed to connect to database server: {e}")
        raise RuntimeError("")
    return connection


def close_connection(connection):
    """
    Close a connection to the NoisePage server instance.
    :param connection The connection
    """
    if connection is not None:
        connection.commit()
        connection.close()
        info("Connection to database server closed")


# -----------------------------------------------------------------------------
# Loading Table Metadata
# -----------------------------------------------------------------------------


class Column:
    """
    The column class represents a schema column.
    """

    @staticmethod
    def from_column_definition(column_definition: str):
        """
        Construct a Column from a column definition string.
        :param The column definition string
        :return The Column
        """
        name, type = column_definition.strip().split()[:2]
        return Column(name, type.strip(","))

    def __init__(self, name: str, type: str):
        """
        Initialize a new Column instance.
        :param name The name of the column
        :param type The type of the column
        """
        self.name = name
        self.type = type

    def __str__(self):
        """Return a string representation of the column."""
        return f"({self.name} : {self.type})"


class Schema:
    """
    The Schema class represents a table schema.
    """

    @staticmethod
    def from_column_definitions(column_definitions: List[str]):
        """
        Construct a Schema instance from a list of column definitions.
        :param column_definitions The list of column definitions
        :return The Schema
        """
        return Schema([Column.from_column_definition(d) for d in column_definitions])

    def __init__(self, columns: List[Column]):
        """
        Initialize a new Schema instance.
        :param columns The list of columns
        """
        self.columns = columns

    def __str__(self):
        """Return a string representation of the schema."""
        n_columns = len(self.columns)
        name_width = max(len(c.name) for c in self.columns)
        s = "(\n"
        for idx, column in enumerate(self.columns):
            comma = "," if idx < n_columns - 1 else ""
            s += f"\t{column.name:<{name_width}} {column.type}{comma}\n"
        s += ")"
        return s


class TableMeta:
    """
    The TableMeta class describes a table.
    """

    @staticmethod
    def from_statement(statement: str, data_directory: str):
        """
        Factory function to construct a TableMeta
        instance from a CREATE TABLE statement.
        :param statement The statement
        :param data_directory The path to the data directory
        :return The TableMeta instance
        """
        lines = [
            l
            for l in statement.split("\n")
            if l != ")" and l != "(" and len(l.strip()) > 0
        ]
        if not lines[0].startswith("CREATE TABLE"):
            raise RuntimeError("Malformed schema file")

        # Extract the table name
        name = lines[0].strip("CREATE TABLE").strip()
        if name not in TABLE_DATA_SOURCES:
            raise RuntimeError("Unexpected table in schema")

        # Extract the table columns
        schema = Schema.from_column_definitions(lines[1:])
        # Construct the path to the data source
        data_source = os.path.join(data_directory, TABLE_DATA_SOURCES[name])

        return TableMeta(name, schema, data_source)

    def __init__(self, name: str, schema: Schema, data_source: str):
        """
        Initialize a new TableMeta instance.
        :param name The name of the table
        :param schema The table schema
        :param data_source The path to the table data file
        """
        # The name of the table
        self.name = name
        # The table schema
        self.schema = schema
        # The path to the table data source
        self.data_source = data_source

    def __str__(self):
        """Return a string representation of the table metdata."""
        return f"{self.name}\n{self.schema}"


def load_table_metadata(schema_file: str, data_directory: str) -> List[TableMeta]:
    """
    Load all SQL ProcBench schemas from the schema file.
    :param schema The path to the schema file
    :param data_directory The path to the data directory
    :return A list of table metadata objects
    """
    with open(schema_file, "r") as f:
        statements = [s for s in map(str.strip, f.read().split(";")) if len(s) > 0]
        return [TableMeta.from_statement(s, data_directory) for s in statements]


# -----------------------------------------------------------------------------
# General Connection Helpers
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
        error(f"Failed to execute query: {e}")


# -----------------------------------------------------------------------------
# Table Create and Drop
# -----------------------------------------------------------------------------


def find_table(name: str, tables: List[TableMeta]) -> TableMeta:
    """
    Find the table identified by `name`.
    :param name The name of the desired table
    :param tables The collection of tables
    :return The requested table, or `None` if not found
    """
    for table in tables:
        if table.name == name:
            return table
    return None


def create_table(connection, table: TableMeta):
    """
    Create a table.
    :param connection The database connection
    :param table The table metadata
    """
    info(f"Creating table {table.name}...")

    query = f"CREATE TABLE {table.name} {table.schema};"
    execute_query(connection, query)

    info(f"Created table {table.name}")


def create_tables(connection, tables: List[TableMeta]):
    """
    Create all benchmark tables.
    :param connection The database connection
    :param tables The list of tables to create.
    """
    for table in tables:
        create_table(connection, table)


def drop_table(connection, table: TableMeta):
    """
    Drop a table.
    :param connection The database connection
    :param table The table metadata
    """
    info(f"Dropping table {table.name}...")

    query = f"DROP TABLE IF EXISTS {table.name};"
    execute_query(connection, query)

    info(f"Dropped table {table.name}")


def drop_tables(connection, tables: List[TableMeta]):
    """
    Drop all benchmark tables.
    :param connection The database connection
    :param tables The list of tables to drop.
    """
    for table in tables:
        drop_table(connection, table)


def setup_tables(connection, tables: List[TableMeta]):
    """
    Ensure all benchmark tables are created.
    :param connection The database connection
    :param tables The list of table metdata objects
    """
    drop_tables(connection, tables)
    create_tables(connection, tables)


# -----------------------------------------------------------------------------
# Data Loading
# -----------------------------------------------------------------------------


def requires_quote(column_type: str) -> bool:
    """
    Determine if the column type requires quotation.
    :param column_type The type of the column, as a string.
    :return `True` if the column value requires quotation
    """
    return "VARCHAR" in column_type or "CHAR" in column_type or "DATE" in column_type


def escape_quotes(field: str) -> str:
    """
    Escape a single quotation mark in string value.
    :param field The input field
    :return The escaped string
    """
    return "".join("" if c == "'" else c for c in field)


def format_value(line: str, schema: Schema) -> str:
    """
    Format a value suitable for insert
    from a raw data source file line.
    :param line The input line
    :param schema The table schema
    :return The formatted value
    """
    # Handle missing values in generated data
    fields = [
        field if len(field) > 0 else "NULL"
        for field in line.split(DATA_SOURCE_FILE_DELIMITER)
    ]
    # Escape individual quotation marks
    fields = [escape_quotes(field) for field in fields]
    # Handle string values (enclose in quotes)
    fields = [
        f"'{field}'" if requires_quote(column.type) and field != "NULL" else field
        for field, column in zip(fields, schema.columns)
    ]
    # Join the fields into a single value
    return f"({','.join(fields).strip().strip(',')})"


def load_table(connection, table: TableMeta):
    """
    Load a table.
    :param connection The database connection
    :param table The table metadata object
    """
    info(f"Loading table {table.name}...")

    layout = f"{table.name}("
    for idx, column in enumerate(table.schema.columns):
        comma = "," if idx < len(table.schema.columns) - 1 else ""
        layout += f"{column.name}{comma}"
    layout += ")"

    base_query = f"INSERT INTO {layout} VALUES {{}}"
    line_count = sum(1 for line in open(table.data_source, "r", encoding="latin-1"))
    with open(table.data_source, "r", encoding="latin-1") as f:
        for line in tqdm(f, total=line_count):
            value = format_value(line, table.schema)
            query = base_query.format(value)
            execute_query(connection, query)

    info(f"Loaded table {table.name}")


def load_tables(connection, tables: List[TableMeta]):
    """
    Load all benchmark tables.
    :param connection The database connection
    :param table The list of table metadata objects
    """
    for table in tables:
        load_table(connection, table)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> int:
    """Run the program."""

    args = parse_arguments()

    # Load tables to in-memory representation
    tables = load_table_metadata(args.schema_file, args.data_directory)
    info(f"Loaded {len(tables)} tables from {args.schema_file}")

    with connection(
        args.db_name, args.db_user, args.db_password, args.db_host, args.db_port
    ) as conn:
        # Initialize tables
        setup_tables(conn, tables)
        if not args.create_only:
            # Load from generated data
            load_tables(conn, tables)

    info("Database loading complete!")

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
