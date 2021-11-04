## Manual Benchmarks

This document describes the process for running manual benchmarks.

### Overhead of Function Call

This benchmark is implemented by the `call.py` script. The procedure for running the benchmark is as follows:

Start the database server

```bash
./noisepage
```

Create the table

```bash
psql -h localhost -d noisepage -p 15721 -f ddl/custom.sql
```

Load the table

```bash
python scripts/loader.py ddl/custom.sql data/
```

Load the function

```bash
psql -h localhost -d noisepage -p 15721 -f plpgsql/custom/fn_call.sql
```

Run the benchmark

```
python scripts/bench/call.py --iterations 100
```

### Lighweight Loop

This benchmark is implemented by the `loop.py` script. The procedure for running the benchmark is as follows:

Start the database server

```bash
./noisepage
```

Load the function

```bash
psql -h localhost -d noisepage -p 15721 -f ./plpgsql/custom/fn_loop.sql
```

Run the benchmark

```bash
python scripts/bench/loop.py --iterations 100
```
