#!/bin/sh
# mw-collegiate.sh WORD: Merriam-Webster Collegiate short definitions of WORD (headword first, first 40 words)
. /opt/neuron/bin/words.sh
K=$(cat "$HOME/.config/merriam-webster/collegiate.key" 2>/dev/null) || exit 0
get "https://www.dictionaryapi.com/api/v3/references/collegiate/json/$1?key=$K" | grep -o '"shortdef":\[[^]]*\]' | sed 's/"shortdef"://' | headed "$1" 200
