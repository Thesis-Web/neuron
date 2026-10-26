#!/bin/sh
# python.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://docs.python.org/3/library/$1.html" | sed 's/<[^>]*>//g' | words 60
