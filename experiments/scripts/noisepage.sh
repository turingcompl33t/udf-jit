# !/bin/bash
# noisepage.sh
# Shortcut for loading NoisePage.

python loader.py ../schema.sql ./data --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 15721

python runner.py out.txt --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 15721
