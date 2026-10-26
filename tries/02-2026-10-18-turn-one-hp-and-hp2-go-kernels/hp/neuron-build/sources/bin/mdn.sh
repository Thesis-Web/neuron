#!/bin/sh
# mdn.sh Q: lower source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://developer.mozilla.org/api/v1/search?q=$1" | sed 's/<[^>]*>//g' | words 60
