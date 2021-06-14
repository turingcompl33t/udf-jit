# Build commands for SQL commandline utilities.

MAKE = make

CC     = gcc
CFLAGS = -Wall -pedantic -std=gnu11 -ggdb

PGDIR = libpg_query
PGLIB = pg_query

# ---------------------------------------------------------
# Default Target

all: proc_parser query_parser

# ---------------------------------------------------------
# Dependency: libpg_query

$(PGLIB):
	$(MAKE) -C $(PGDIR) build

# ---------------------------------------------------------
# Command-Line Utilities

proc_parser: proc_parser.c $(PGLIB)
	$(CC) $(CFLAGS) -o $@ -I$(PGDIR) -L$(PGDIR) -pthread $< -l$(PGLIB) 

query_parser: query_parser.c $(PGLIB)
	$(CC) $(CFLAGS) -o $@ -I$(PGDIR) -L$(PGDIR) -pthread $< -l$(PGLIB) 

# ---------------------------------------------------------
# Clean

clean:
	rm -f *.o
	rm -f *.a
	rm -f proc_parser
	rm -f query_parser
	$(MAKE) -C $(PGDIR) clean

.PHONY: clean
