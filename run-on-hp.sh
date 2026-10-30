#!/bin/bash
# run-on-hp.sh (2026-10-30): the kernel on hp, from ~/nk.
#   bash run-on-hp.sh fresh    the sources laid again from the egg (sources-egg), the kernel started with the egg, the sixty lines typed, the door up
#   bash run-on-hp.sh resume   the same, then every line typed since the last fresh start (the journal out/typed.txt) typed again in order
#   bash run-on-hp.sh stop     the kernel and the door stopped
# The kernel's brain lives in memory: the journal and 'export' are its persistence tonight.
cd ~/nk; MODE=${1:-fresh}
pkill -x nk; pkill -f serve8.py; sleep 0.5
[ "$MODE" = stop ] && exit 0
gcc -O2 -Wall -Wno-unused-function -Wno-unused-parameter -I. -o nk nk.c nkvt.c nkio.c -L/usr/lib/x86_64-linux-gnu -l:libsqlite3.so.0 -lpthread -lm -ldl || exit 1
mkdir -p out; rm -f sources/*.db; cp sources-egg/*.db sources/
if [ "$MODE" = resume ] && [ -s out/typed.txt ]; then mv out/typed.txt out/replay.txt; else [ -s out/typed.txt ] && mv out/typed.txt "out/typed-until-$(date +%Y%m%d-%H%M%S).txt"; rm -f out/replay.txt; fi
(NK_JOURNAL=out/typed.txt nohup ./nk 7007 egg-symbols.txt sources > nk.log 2>&1 &); sleep 1; cat nk.log
if [ "$MODE" = resume ]; then python3 nkbottom.py 7007 --lines out/replay.txt --ledger out/LEDGER-resume.md --quiet | tail -1 | cut -c1-200
else python3 nkbottom.py 7007 --lines LINES-nk.txt --ledger out/LEDGER-nk-60-lines.md --quiet | tail -1 | cut -c1-200; fi
(nohup python3 serve8.py 8058 7007 NEURON-POINT-OF-CONNECTION-nk-2026-10-30.html LINES-nk.txt FIRST-RUNS-nk.txt 0.0.0.0 > door.log 2>&1 &); sleep 1; cat door.log
echo "journal: $(wc -l < out/typed.txt) lines typed since the egg"
