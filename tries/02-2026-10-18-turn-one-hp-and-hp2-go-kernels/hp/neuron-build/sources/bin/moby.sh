#!/bin/sh
# moby.sh WORD: Moby Thesaurus II synonyms of WORD from dict.org (headword first, then the synonym words)
. /opt/neuron/bin/words.sh
get "dict://dict.org/d:$1:moby-thesaurus" | grep -v '^[0-9][0-9][0-9] \|^ *[0-9]* Moby' | tr ',' '\n' | words 20 | tr ' ' '\n' | grep -v -x "$1" | headed "$1" 20
