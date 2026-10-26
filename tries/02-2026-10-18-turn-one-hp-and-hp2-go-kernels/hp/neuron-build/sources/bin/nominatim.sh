#!/bin/sh
# nominatim.sh Q: lower source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://nominatim.openstreetmap.org/search?q=$1&format=json&limit=2" | sed 's/<[^>]*>//g' | words 60
