#!/bin/sh
# factbook.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://raw.githubusercontent.com/factbook/factbook.json/master/$1.json" | sed 's/<[^>]*>//g' | words 60
