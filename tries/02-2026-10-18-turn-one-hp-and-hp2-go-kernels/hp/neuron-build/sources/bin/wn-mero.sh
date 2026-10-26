#!/bin/sh
# wn-mero.sh WORD: WordNet meronyms (the parts WORD has): headword then the part words
. /opt/neuron/bin/words.sh
wn "$1" -meron 2>/dev/null | grep 'HAS \(PART\|MEMBER\|SUBSTANCE\):' | sed 's/.*: //' | words 20 | tr ' ' '\n' | grep -v -x "$1" | headed "$1" 20
