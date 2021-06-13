# Build commands for simple commandline PL/pgSQL tokenizer.

MAKE = make

CC     = gcc
CFLAGS = -Wall -pedantic -std=gnu11 -ggdb

PGDIR = libpg_query
PGLIB = pg_query

# ---------------------------------------------------------
# Default Target

all: tokenizer

# ---------------------------------------------------------
# Dependency: libpg_query

$(PGLIB):
	$(MAKE) -C $(PGDIR) build

# ---------------------------------------------------------
# Command-Line Utility

tokenizer: tokenizer.c $(PGLIB)
	$(CC) $(CFLAGS) -o $@ -I$(PGDIR) -L$(PGDIR) -pthread $< -l$(PGLIB) 

# ---------------------------------------------------------
# Clean

clean:
	rm -f *.o
	rm -f *.a
	rm -f tokenizer
	$(MAKE) -C $(PGDIR) clean

.PHONY: clean
