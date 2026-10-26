#!/bin/sh
# openstax.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://openstax.org/apps/cms/api/v2/pages/?type=books.Book&fields=title&limit=200&search=$1" | sed 's/<[^>]*>//g' | words 60
