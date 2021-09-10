## Experimental Evaluation

This document provides metadata information for the experiemental evaluation.

### Data

The functions on which we perform the evaluation are drawn from [SQL ProcBench](https://github.com/microsoft/SQL-ProcBench).

**Function Support**

SQL ProcBench contains XXX scalar UDFs.

Supported Functions (XXX):
- 10 "Is List Distinct"
- 11 "Generate Random Character"
- 12 "Increase in Web Spending"
- 13 "Max Purchase Channel"
- 20b "Get Manufacturer (Complex)"

Unsupported Functions (XXX):

**Schema**

The complete schema for ProcBench is described by _schema.txt_. The first step in performing experiements on any system is to create the necessary tables by executing each of the DDL statements in this file.

**Functions**



### References

- [SQL ProcBench](https://github.com/microsoft/SQL-ProcBench)
- [Procedural Extensions of SQL: Understanding Their Usage in the Wild](http://www.vldb.org/pvldb/vol14/p1378-ramachandra.pdf)
