# !/bin/bash
# noisepage.sh
# Shortcut for loading NoisePage.

python loader.py ../ddl/schema-decimal.sql ../loader/data --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 15721
python loader.py ../ddl/schema-float.sql ../loader/data --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 15721

python runner.py ../plpgsql/decimal/ out.txt --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 15721
python runner.py ../plpgsql/float/ out.txt --db-user postgres --db-password password --db-name noisepage --db-host localhost --db-port 15721
