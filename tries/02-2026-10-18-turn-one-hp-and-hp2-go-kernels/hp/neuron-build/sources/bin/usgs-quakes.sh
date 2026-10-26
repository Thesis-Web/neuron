#!/bin/sh
# usgs-quakes.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=$1&limit=3" | sed 's/<[^>]*>//g' | words 60
