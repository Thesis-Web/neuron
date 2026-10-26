#!/bin/sh
# medlineplus.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term=$1" | sed 's/<[^>]*>//g' | words 60
