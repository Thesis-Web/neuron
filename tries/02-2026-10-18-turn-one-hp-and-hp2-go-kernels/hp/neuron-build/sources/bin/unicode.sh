#!/bin/sh
# unicode.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt" | sed 's/<[^>]*>//g' | words 60
