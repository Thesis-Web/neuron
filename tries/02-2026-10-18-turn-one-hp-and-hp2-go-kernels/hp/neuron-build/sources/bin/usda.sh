#!/bin/sh
# usda.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query=$1&pageSize=3" | sed 's/<[^>]*>//g' | words 60
