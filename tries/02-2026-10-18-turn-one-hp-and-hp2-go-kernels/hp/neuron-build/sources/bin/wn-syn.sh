#!/bin/sh
# wn-syn.sh WORD: WordNet synonyms (the words sharing a synset with WORD): headword then the synonym words
. /opt/neuron/bin/words.sh
wn "$1" -synsn -synsv -synsa -synsr 2>/dev/null | grep '^[a-z]' | grep -v -i '^sense \|senses of \|synonyms\|similarity of ' | tr ',' '\n' | sed 's/(.*//' | grep -v "^ *$1 *$" | words 20 | tr ' ' '\n' | grep -v -x "$1" | headed "$1" 20
