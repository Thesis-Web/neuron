#!/bin/sh
# arxiv.sh Q: lower source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "http://export.arxiv.org/api/query?search_query=$1&max_results=3" | sed 's/<[^>]*>//g' | words 60
