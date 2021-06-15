# analyzer.py
# UNIX-style PL/pgSQL UDF analyzer.

import os
import sys
import json
import argparse
from subprocess import Popen, PIPE
from typing import Dict, List, Set, FrozenSet

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Query parser binary setup
QUERY_PARSER_DEFAULT_NAME = "query_parser"
QUERY_PARSER_DEFAULT_DIRECTORY = "sql"
QUERY_PARSER_DEFAULT_BINARY_PATH = os.path.join(
    os.getcwd(), QUERY_PARSER_DEFAULT_DIRECTORY, QUERY_PARSER_DEFAULT_NAME
)

# The raw identifiers for the features of interest
ATTR_STATEMENT_BLOCK = "PLpgSQL_stmt_block"
ATTR_STATEMENT_IF = "PLpgSQL_stmt_if"
ATTR_STATEMENT_RETURN = "PLpgSQL_stmt_return"
ATTR_STATEMENT_RAISE = "PLpgSQL_stmt_raise"
ATTR_STATEMENT_WHILE = "PLpgSQL_stmt_while"
ATTR_STATEMENT_FORI = "PLpgSQL_stmt_fori"
ATTR_STATEMENT_FORS = "PLpgSQL_stmt_fors"
ATTR_STATEMENT_DYNAMIC = "PLpgSQL_stmt_dynexecute"
ATTR_EXCEPTION_BLOCK = "PLpgSQL_exception_block"
ATTR_STATEMENT_SQL = "PLpgSQL_stmt_execsql"

# The raw identifiers for SQL statements
STATEMENT_SELECT = "SelectStmt"
STATEMENT_INSERT = "InsertStmt"
STATEMENT_UPDATE = "UpdateStmt"
STATEMENT_DELETE = "DeleteStmt"

# The complete collection of SQL statement identifiers
STATEMENT_IDENTIFIERS = frozenset(
    [STATEMENT_SELECT, STATEMENT_INSERT, STATEMENT_UPDATE, STATEMENT_DELETE]
)

# A complete collection of the features of interest
# NOTE: We don't include the attribute for embedded SQL
# queries here because we analyze these separately
FEATURE_ATTRS = frozenset(
    [
        ATTR_STATEMENT_BLOCK,
        ATTR_STATEMENT_IF,
        ATTR_STATEMENT_RETURN,
        ATTR_STATEMENT_RAISE,
        ATTR_STATEMENT_WHILE,
        ATTR_STATEMENT_FORI,
        ATTR_STATEMENT_FORS,
        ATTR_STATEMENT_DYNAMIC,
        ATTR_EXCEPTION_BLOCK,
    ]
)

# A mapping from raw identifiers to postprocessing keys
FEATURE_KEYS = {
    ATTR_STATEMENT_BLOCK: "STATEMENT_BLOCK",
    ATTR_STATEMENT_IF: "STATEMENT_IF",
    ATTR_STATEMENT_RETURN: "STATEMENT_RETURN",
    ATTR_STATEMENT_RAISE: "STATEMENT_RAISE",
    ATTR_STATEMENT_WHILE: "STATEMENT_WHILE",
    ATTR_STATEMENT_FORI: "STATEMENT_FOR",
    ATTR_STATEMENT_FORS: "STATEMENT_FOR",
    ATTR_STATEMENT_DYNAMIC: "STATEMENT_DYNAMIC",
    ATTR_EXCEPTION_BLOCK: "EXCEPTION_BLOCK",
    STATEMENT_SELECT: "QUERY_SELECT",
    STATEMENT_INSERT: "QUERY_INSERT",
    STATEMENT_UPDATE: "QUERY_UPDATE",
    STATEMENT_DELETE: "QUERY_DELETE",
}

# -----------------------------------------------------------------------------
# Commandline Parsing
# -----------------------------------------------------------------------------


def parse_arguments():
    """
    Parse commandline arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input", help="The input JSON parse tree", nargs="?", type=str, default=None
    )

    return parser.parse_args()


# -----------------------------------------------------------------------------
# Parse Tree I/O
# -----------------------------------------------------------------------------


def read_from_file(path: str) -> Dict:
    """
    Read the JSON-formatted parse tree from `path`.
    :param path The input path
    :return The in-memory JSON representation of the parse tree
    """
    with open(path, "r") as f:
        return json.loads(f.read())


def read_from_stdin() -> str:
    """
    Read the JSON-formatted parse tree from standard input.
    :return The in-memory JSON representation of the parse tree
    """
    return json.loads(sys.stdin.read())


def read_parse_tree(path: str) -> Dict:
    """
    Read the input parse tree.
    :param path The path to the input file from which to read the procedure.
    :return The in-memory JSON representation of the parse tree.
    """
    return read_from_file(path) if path is not None else read_from_stdin()


# -----------------------------------------------------------------------------
# Feature Analysis
# -----------------------------------------------------------------------------


def flatten_to(structure, features: Set):
    """
    Flatten hierarchical function parse tree structure.
    :param structure Polymorphic structure
    :param features The set of features to populate
    """
    if type(structure) is dict:
        for item in structure:
            features.add(item)
            flatten_to(structure[item], features)
    elif type(structure) is list:
        for element in structure:
            flatten_to(element, features)
    else:
        features.add(structure)


def analyze_features(parse_tree: Dict) -> FrozenSet:
    """
    Analyze the parse tree to extract raw token counts.
    :param parse_tree The input parse tree
    :return A set of the unique features that appear in the tree
    """
    # Isolate actions within the function
    action = parse_tree["PLpgSQL_function"]["action"]

    # Visit the top-level statement block
    features = set()
    flatten_to(action["PLpgSQL_stmt_block"], features)

    return frozenset([f for f in features if f in FEATURE_ATTRS])


# -----------------------------------------------------------------------------
# Embedded Query Analysis
# -----------------------------------------------------------------------------


def collect_to(structure, queries: List):
    """
    Collect embedded queries from hierarchical parse tree structure.
    :param structure Polymorphic structure
    :param queries The list of queries to populate
    """
    if type(structure) is dict:
        for item in structure:
            if item == ATTR_STATEMENT_SQL:
                queries.append(structure[item])
            collect_to(structure[item], queries)
    elif type(structure) is list:
        for element in structure:
            collect_to(element, queries)


def extract_queries(parse_tree: Dict) -> List:
    """
    Extract the embedded queries from the function parse tree.
    :param parse_tree The input parse tree
    :return The list of query objects in the parse tree
    """

    # Isolate actions within the function
    action = parse_tree["PLpgSQL_function"]["action"]

    # Visit the top-level statement block
    queries = []
    collect_to(action["PLpgSQL_stmt_block"], queries)

    return queries


def parse_query(query_obj: Dict) -> Dict:
    """
    Parse an individual SQL query with the Postgres parser.
    :param query_obj The query object (from the function parse tree)
    :return The query parse tree
    """

    # Extract the raw SQL from the query object
    sql = query_obj["sqlstmt"]["PLpgSQL_expr"]["query"]

    # Run the query through the Postgres parser
    process = Popen(
        [QUERY_PARSER_DEFAULT_BINARY_PATH], stdin=PIPE, stdout=PIPE, stderr=PIPE
    )
    stdout, stderr = process.communicate(input=sql.encode())
    return None if len(stderr) != 0 else json.loads(stdout)


def extract_statements(parsed_query: Dict) -> FrozenSet:
    """
    Extract the statements of interest from a query parse tree.
    :param parsed_query The query parse tree
    :return A set of the statements of interest in the query
    """
    ids = set()
    statements = parsed_query["stmts"]
    for statement in statements:
        for key in statement["stmt"].keys():
            if key in STATEMENT_IDENTIFIERS:
                ids.add(key)
    return frozenset(ids)


def analyze_queries(parse_tree: Dict) -> FrozenSet:
    """
    Analyze all queries appearing in the function parse tree.
    :param parse_tree The function parse tree
    :return A set of statement identifiers for each query
    type that appears in the input parse tree
    """

    # Collect the embedded queries from the parse tree
    queries = extract_queries(parse_tree)

    # Parse each query with the Postgres parser
    queries = [parse_query(q) for q in queries]

    # Extract the statement identifers from each query
    statements = set()
    for q in queries:
        statements = statements | extract_statements(q)
    return frozenset(statements)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    args = parse_arguments()

    # Read the parse tree
    parse_tree = read_parse_tree(args.input)

    # Get all of the raw features
    features = analyze_features(parse_tree)
    # Get the embedded queries
    queries = analyze_queries(parse_tree)

    # Combine the results of analysis
    unified = features | queries
    results = {
        k: v
        for k, v in zip(FEATURE_KEYS, [1 if x in unified else 0 for x in FEATURE_KEYS])
    }
    results = {FEATURE_KEYS[k]: v for k, v in results.items()}

    # Write the results to standard output
    sys.stdout.write(json.dumps(results))

    return EXIT_SUCCESS


# -----------------------------------------------------------------------------
# Script Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
