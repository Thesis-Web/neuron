#!/bin/sh
# uniprot.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://rest.uniprot.org/uniprotkb/search?query=$1&format=json&size=3" | sed 's/<[^>]*>//g' | words 60
