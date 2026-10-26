#!/bin/sh
# man.sh THING: the man page of THING, NAME and DESCRIPTION, as plain words (headword first, first 40 words). Nothing when there is no page.
. /opt/neuron/bin/words.sh
man -P cat "$1" 2>/dev/null | sed -n '/^NAME/,/^SYNOPSIS/p;/^DESCRIPTION/,/^OPTIONS/p' | grep -v '^NAME\|^SYNOPSIS\|^DESCRIPTION\|^OPTIONS' | headed "$1" 200
