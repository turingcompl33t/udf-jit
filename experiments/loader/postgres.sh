#!/bin/bash
# postgres.sh
# Shortcut for loading Postgres.

python load.py ../schema.sql ./data --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 5432
