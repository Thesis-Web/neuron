#!/bin/sh
# metamath.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://us.metamath.org/mpeuni/$1.html" | sed 's/<[^>]*>//g' | words 60
