#!/bin/sh
# oeis.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://oeis.org/search?q=$1&fmt=json" | sed 's/<[^>]*>//g' | words 60
