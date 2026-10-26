#!/bin/sh
# archive.sh Q: lower source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://archive.org/advancedsearch.php?q=$1&fl[]=identifier&output=json" | sed 's/<[^>]*>//g' | words 60
