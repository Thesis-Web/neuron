#!/bin/sh
# tee-own.sh NAME WORD...: writes the words (one per line) to /home/neuron/own/NAME and prints them back. The brain's own file store.
mkdir -p "$HOME/own"; n=$1; shift; printf '%s\n' "$@" | tee "$HOME/own/$n"
