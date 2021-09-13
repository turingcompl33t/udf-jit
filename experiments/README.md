## Experimental Evaluation

This document provides metadata information for the experiemental evaluation.

### Data

The functions on which we perform the evaluation are drawn from [SQL ProcBench](https://github.com/microsoft/SQL-ProcBench).

**Schema**

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

### References

- [SQL ProcBench](https://github.com/microsoft/SQL-ProcBench)
- [Procedural Extensions of SQL: Understanding Their Usage in the Wild](http://www.vldb.org/pvldb/vol14/p1378-ramachandra.pdf)
