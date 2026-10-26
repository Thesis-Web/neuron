#!/bin/sh
# wiktionary.sh WORD: the Wiktionary English definitions of WORD, tags stripped (headword first, first 40 words). Lower trust: crowd-edited.
. /opt/neuron/bin/words.sh
get "https://en.wiktionary.org/api/rest_v1/page/definition/$1" | sed 's/\\"/ /g; s/<[^>]*>//g' | grep -o '"definition":"[^"]*"' | sed 's/"definition"://' | sed 's/<[^>]*>//g; s/\\n/ /g' | headed "$1" 200
