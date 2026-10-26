#!/bin/sh
# dictorg-gcide.sh WORD: GCIDE from dict.org (headword first, first 40 words)
. /opt/neuron/bin/words.sh
get "dict://dict.org/d:$1:gcide" | grep -v '^[0-9][0-9][0-9] ' | headed "$1" 200
