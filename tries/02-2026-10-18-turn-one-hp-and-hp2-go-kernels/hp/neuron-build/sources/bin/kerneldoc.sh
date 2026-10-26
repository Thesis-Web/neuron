#!/bin/sh
# kerneldoc.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://docs.kernel.org/$1.html" | sed 's/<[^>]*>//g' | words 60
