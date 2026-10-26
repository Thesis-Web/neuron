#!/bin/sh
# mw-thesaurus.sh WORD: Merriam-Webster Collegiate Thesaurus synonyms of WORD (headword first, then the synonym words)
. /opt/neuron/bin/words.sh
K=$(cat "$HOME/.config/merriam-webster/thesaurus.key" 2>/dev/null) || exit 0
get "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/$1?key=$K" | grep -o '"syns":\[\[[^]]*\]' | sed 's/"syns"://' | words 20 | tr ' ' '\n' | grep -v -x "$1" | headed "$1" 20
