## Experimental Evaluation

This document provides metadata information for the experiemental evaluation.

### Data

The functions on which we perform the evaluation are drawn from [SQL ProcBench](https://github.com/microsoft/SQL-ProcBench).

The complete schema for ProcBench is described by _schema.txt_. The first step in performing experiements on any system is to create the necessary tables by executing each of the DDL statements in this file.

### Query Plans

This section describes the status of generating query plans for UDF inlining techniques.

**Froid**

- Function 01: `totalLargePurchases` inlined
- Function 04: `genRandomInt` inlined
- Function 06: `totalDiscount` inlined
- Function 11: `genRandomChar` inlined
- Function 13: `maxPurchaseChannel` inined
- Function 18: `preferredChannel_wrtExpenditure` not inlined

**Apfel**

TODO

### Procedure: Froid (SQL Server)

TODO

### Procedure: Apfel (Postgres)

Setup:

```sql
-- List databases
\list
-- Switch databases
\connect jit
-- List tables
\dt
```

Functions:

```bash
# Function 01
sudo -u postgres psql -d jit -f fn_01.sql
sudo -u postgres psql -d jit -f invoke_01.sql

# Function 04
sudo -u postgres psql -d jit -f fn_04.sql
sudo -u postgres psql -d jit -f invoke_04.sql

# Function 06
sudo -u postgres psql -d jit -f fn_06.sql
sudo -u postgres psql -d jit -f invoke_06.sql

# Function 11
sudo -u postgres psql -d jit -f fn_11.sql
sudo -u postgres psql -d jit -f invoke_11.sql

# Function 12
sudo -u postgres psql -d jit -f fn_12.sql
sudo -u postgres psql -d jit -f invoke_12.sql

# Function 13
sudo -u postgres psql -d jit -f fn_13.sql
sudo -u postgres psql -d jit -f invoke_13.sql

# Function 18
sudo -u postgres psql -d jit -f fn_18.sql
sudo -u postgres psql -d jit -f invoke_18.sql
```

### Procedure: NoisePage

TODO

### References

- [SQL ProcBench](https://github.com/microsoft/SQL-ProcBench)
- [Procedural Extensions of SQL: Understanding Their Usage in the Wild](http://www.vldb.org/pvldb/vol14/p1378-ramachandra.pdf)
