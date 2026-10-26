#!/bin/sh
# wikipedia.sh TITLE: the Wikipedia summary extract of TITLE (headword first, first 40 words). Lower trust: crowd-edited.
. /opt/neuron/bin/words.sh
get "https://en.wikipedia.org/api/rest_v1/page/summary/$1" | sed 's/\\"/ /g' | grep -o '"extract":"[^"]*"' | sed 's/"extract"://' | headed "$1" 200
