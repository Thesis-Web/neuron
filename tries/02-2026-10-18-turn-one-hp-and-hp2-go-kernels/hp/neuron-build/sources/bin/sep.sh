#!/bin/sh
# sep.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://plato.stanford.edu/entries/$1/" | sed 's/<[^>]*>//g' | words 60
