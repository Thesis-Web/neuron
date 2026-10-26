#!/bin/sh
# worldbank.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://api.worldbank.org/v2/country/$1/indicator/NY.GDP.MKTP.CD?format=json&mrv=1" | sed 's/<[^>]*>//g' | words 60
