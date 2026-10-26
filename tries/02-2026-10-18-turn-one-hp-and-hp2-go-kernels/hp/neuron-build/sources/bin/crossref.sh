#!/bin/sh
# crossref.sh Q: lower source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://api.crossref.org/works?query=$1&rows=3" | sed 's/<[^>]*>//g' | words 60
