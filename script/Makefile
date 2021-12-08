# Makefile

default:
	@echo No default target!

# Open the database for querying
.PHONY: query
query:
	sqlite3 input-prep/features.sqlite

# Prepare CSV for loading into SQLite
.PHONY: prep
prep:
	python reader.py input-raw/functions.csv input-prep/

# Clean build artifacts
.PHONY: clean
clean:
	make -C sql clean
