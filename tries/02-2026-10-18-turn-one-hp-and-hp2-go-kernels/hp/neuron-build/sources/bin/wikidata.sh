#!/bin/sh
# wikidata.sh Q: lower source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=$1&language=en&format=json" | sed 's/<[^>]*>//g' | words 60
