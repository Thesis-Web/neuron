#!/bin/sh
# europepmc.sh Q: lower source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=$1&format=json&pageSize=3" | sed 's/<[^>]*>//g' | words 60
