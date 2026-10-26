#!/bin/sh
# posix.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://pubs.opengroup.org/onlinepubs/9799919799/utilities/$1.html" | sed 's/<[^>]*>//g' | words 60
