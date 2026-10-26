#!/bin/sh
# wn-hyper.sh WORD: WordNet direct hypernyms (what WORD is a kind of): headword then the hypernym words
. /opt/neuron/bin/words.sh
wn "$1" -hypen -hypev 2>/dev/null | grep '^       => ' | sed 's/=>//' | words 20 | tr ' ' '\n' | grep -v -x "$1" | headed "$1" 20
