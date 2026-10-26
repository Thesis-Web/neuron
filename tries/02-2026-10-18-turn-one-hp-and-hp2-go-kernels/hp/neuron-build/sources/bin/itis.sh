#!/bin/sh
# itis.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://www.itis.gov/ITISWebService/jsonservice/searchByScientificName?srchKey=$1" | sed 's/<[^>]*>//g' | words 60
