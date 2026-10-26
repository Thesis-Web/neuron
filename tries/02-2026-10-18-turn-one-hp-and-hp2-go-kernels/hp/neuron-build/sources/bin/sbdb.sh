#!/bin/sh
# sbdb.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=$1" | sed 's/<[^>]*>//g' | words 60
