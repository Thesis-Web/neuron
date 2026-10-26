#!/bin/sh
# roget.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://www.gutenberg.org/cache/epub/10681/pg10681.txt" | sed 's/<[^>]*>//g' | words 60
