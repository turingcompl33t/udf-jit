#!/bin/bash
#
# driver.sh
# Driver script for PL/pgSQL function analysis.

if [ "$#" -ne 1 ]; then
  echo "Error: invalid arguments"
  echo "Usage: driver.sh <INPUT_PATH>"
  exit 1
fi

# The input file directory
INPUT_FILES="$1/*"

# Create a ramdisk for intermediate results
RAMDISK=$(mktemp -p /dev/shm/)

# Process each of the input files
for f in $INPUT_FILES
do
  echo "Processing file $f..."
  cat $f | python parser.py | python analyzer.py >> $RAMDISK
done

# Aggregate the results
cat $RAMDISK | python postprocessor.py > results.json

rm $RAMDISK
exit 0
 