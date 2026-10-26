#!/bin/sh
# wn-ant.sh WORD: WordNet direct antonyms of WORD (every part of speech): headword then the antonym words
. /opt/neuron/bin/words.sh
wn "$1" -antsn -antsv -antsa -antsr 2>/dev/null | grep '^[a-z]' | grep -v -i '^sense \|senses of \|antonyms of ' | sed 's/(.*//; s/ *$//' | grep -v "^$1\b" | headed "$1" 20
