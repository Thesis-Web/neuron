#!/bin/sh
# nist-constants.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://physics.nist.gov/cuu/Constants/Table/allascii.txt" | sed 's/<[^>]*>//g' | words 60
