#!/bin/sh
# britannica1911.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://en.wikisource.org/w/api.php?action=query&list=search&srsearch=$1&format=json" | sed 's/<[^>]*>//g' | words 60
