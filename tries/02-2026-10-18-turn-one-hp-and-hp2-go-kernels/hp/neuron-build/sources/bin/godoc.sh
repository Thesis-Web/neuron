#!/bin/sh
# godoc.sh PKG.NAME: the Go documentation of a package or name, as plain words (first 60). Grounded, for computer actions.
. /opt/neuron/bin/words.sh
go doc "$1" 2>/dev/null | words 60
