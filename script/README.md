## PL/pgSQL Function Analysis

This directory contains a set of tools / scripts to analyze PL/pgSQL functions.

### Contents

This section provides a brief overview of the contents of this directory.

**Subdirectories**:

- `input-invalid/`: Input functions that are not properly handled by the Postgres parser.
- `input-scalar/`: Input scalar UDFs.
- `input-table/`: Input table-valued UDFs.
- `sql/`: The underlying C tools used invoked by the Python scripts.
- `test/`: Simple input UDFs for testing.

**Tools / Scripts**:

- `parser.py`: A UNIX-style tool that parses an input PL/pgSQL function into the Postgres parse tree. The parse tree is written to standard output to in JSON format.
- `analyzer.py`: A UNIX-style tool that extracts features of interest from the Postgres parse tree. The tool accepts a parse tree in JSON format, and writes the resulting analysis to standard output, also in JSON format.
- `postprocessor.py`: A UNIX-style tool that performs some basic post-processing on the analysis results (essentially just aggregation)
- `driver.sh`: A bash script that orchestrates the three tools above.

### Results

Results from the Github survey of PL/pgSQL functions by Nayak [1].

| Feature | Percentage |
| --- | ---: |
| `SELECT` Statement | 43.7 |
| `IF` Statement | 30.4 |
| `RAISE` Statement | 8.6 |
| Cursor Loop | 8.2 |
| `INSERT` / `UPDATE` / `DELETE` Statement | 7.2 |
| `FOR` / `WHILE` Loop | 4.0 |
| Dynamic Execution | 3.6 |
| `EXCEPTION` Block | 2.9 |

Results from analysis of the PL/pgSQL function sample from Gupta [2].

| Feature | Percentage |
| --- | ---: |
| `IF` Statement | 54.2 |
| `SELECT` Statement | 37.5 |
| `FOR` Loop | 8.3 |
| `WHILE` Loop | 4.2 |
| Cursor Loop | 3.5 |
| `RAISE` Statement | 0.0 |
| `INSERT` Statement | 0.0 |
| `UPDATE` Statement | 0.0 |
| `DELETE` Statement | 0.0 |
| Dynamic Execution | 0.0 |
| `EXCEPTION` Block | 0.0 |

### References

1. An Evaluation of Compilation-Based PL/pgSQL Execution. Tanuj Nayak. 2021.
2. Procedural Extensions of SQL: Understanding Their Usage in the Wild. Surabhi Gupta and Karthik Ramachandra. 2021. 