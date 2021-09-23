#!/bin/bash
# postgres.sh
# Shortcut for loading Postgres.

python loader.py ../ddl/schema-clean.sql ../loader/data --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 5432
python loader.py ../ddl/schema-dirty.sql ../loader/data --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 5432

python runner.py ../plpgsql/clean/ out.txt --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 5432
python runner.py ../plpgsql/dirty/ out.txt --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 5432
