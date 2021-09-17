#!/bin/bash
# postgres.sh
# Shortcut for loading Postgres.

python loader.py ../schema.sql ../loader/data --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 5432

python runner.py out.txt --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 5432
