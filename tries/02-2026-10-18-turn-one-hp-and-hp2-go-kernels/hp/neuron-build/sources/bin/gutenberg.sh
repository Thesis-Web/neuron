#!/bin/sh
# gutenberg.sh Q: lower source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://www.gutenberg.org/ebooks/search/?query=$1" | sed 's/<[^>]*>//g' | words 60
