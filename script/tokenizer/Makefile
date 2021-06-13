# Build commands for simple commandline PL/pgSQL tokenizer.

MAKE = make

CC = gcc
CFLAGS = -Wall -pedantic -std=gnu11 -ggdb

PGDIR = libpg_query
PGLIB = libpg_query.a

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
	$(CC) $(CFLAGS) -o $@ -L $(PGDIR) -l $(PGDIR)/$(PGLIB) -I $(PGDIR) $^

# ---------------------------------------------------------
# Clean

clean:
	rm -rf *.o
	rm -f tokenizer
	$(MAKE) -C $(PGDIR) clean

.PHONY: clean
