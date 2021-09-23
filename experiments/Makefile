# Makefile
#
# Automates some top-level experiment operations.

MAKE = make

default:
	@echo "No Default Target!"

# Generate data with dsdgen
generate-data: build-dsdgen
	mkdir loader/data
	./loader/tools/dsdgen -scale 1 -dir loader/data

# Clean data from dsdgen
clean-data:
	rm -rf loader/data/

# Build the dsdgen tool
build-dsdgen:
	$(MAKE) -C loader/tools dsdgen

# Clean the dsdgen tool
clean-dsdgen:
	$(MAKE) -C loader/tools clean

clean: clean-dsdgen clean-data

.PHONY: clean
