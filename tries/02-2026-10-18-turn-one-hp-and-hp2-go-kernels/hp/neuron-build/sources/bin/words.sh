# words.sh: sourced by the reach scripts. words N: reads stdin, keeps lowercase letters, prints the first N words on one line.
# headed WORD N: like words, but prints WORD first and prints nothing at all when the stream is empty (a gap is a gap).
words() { tr 'A-Z' 'a-z' | tr -c 'a-z\n' ' ' | tr -s ' \n' '\n' | grep -v '^$' | head -n "${1:-40}" | tr '\n' ' '; }
headed() { local t; t=$(words "$2"); [ -n "$t" ] && printf '%s %s\n' "$1" "$t"; return 0; }
UA='neuron-turn-one/0.1 (a self-building brain on a private machine)'
get() { curl -fsS -m 20 -A "$UA" "$@" 2>/dev/null; return 0; }
