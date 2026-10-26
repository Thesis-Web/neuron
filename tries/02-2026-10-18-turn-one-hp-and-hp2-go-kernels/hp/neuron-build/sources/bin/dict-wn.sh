#!/bin/sh
# dict-wn.sh WORD: the local dictd 'wn' entry for WORD, as plain words (headword first, first 40 words)
. /opt/neuron/bin/words.sh
dict -h localhost -d wn -f -- "$1" 2>/dev/null | sed '1,/^  /{/^[0-9]* definitions\? found/d;/^localhost/d}' | headed "$1" 200
