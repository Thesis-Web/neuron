#!/bin/sh
# cmudict.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict" | sed 's/<[^>]*>//g' | words 60
