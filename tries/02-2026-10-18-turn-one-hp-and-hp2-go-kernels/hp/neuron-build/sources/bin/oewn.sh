#!/bin/sh
# oewn.sh WORD: Open English WordNet 2025. Finds WORD in the index files, fetches its first synsets by offset, prints the synset words and gloss.
. /opt/neuron/bin/words.sh
W=/srv/sources/wordnet/oewn-2025/english-wordnet-2025/oewn2025
for pos in noun verb adj adv; do
  line=$(grep -m1 "^$1 " $W/index.$pos) || continue
  n=$(echo "$line" | awk '{print $3}')
  for off in $(echo "$line" | awk '{for(i=NF-$3+1;i<=NF&&i<=NF-$3+3;i++)print $i}'); do
    grep -m1 "^$off " $W/data.$pos | sed 's/^[0-9]* [0-9]* [a-z] [0-9a-f]* //; s/ [0-9a-f] / /g'
  done
done | headed "$1" 200
