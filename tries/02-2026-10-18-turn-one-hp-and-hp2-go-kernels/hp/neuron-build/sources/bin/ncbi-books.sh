#!/bin/sh
# ncbi-books.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=books&term=$1&retmode=json" | sed 's/<[^>]*>//g' | words 60
