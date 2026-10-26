#!/bin/sh
# cldr.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-rbnf/rbnf/$1.json" | sed 's/<[^>]*>//g' | words 60
