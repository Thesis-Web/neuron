#!/bin/bash
# run-on-hp.sh (2026-10-30): the kernel on hp, from ~/nk. The brain lives in memory; its persistence is a snapshot (every region as tables,
# the small source files beside it, the count of journal lines typed by then) and the journal of every line typed since the egg.
#   bash run-on-hp.sh fresh            the sources laid again from their egg (sources-egg), the kernel started with the egg, LINES-nk typed, the door up
#   bash run-on-hp.sh type FILE        a lines file typed in order (ledger in out/LEDGER-<file>.md)
#   bash run-on-hp.sh snapshot         a snapshot into out/snap-<stamp>, out/snap-latest pointing at it
#   bash run-on-hp.sh resume           the newest snapshot loaded, the journal lines typed after it typed again, the door up
#   bash run-on-hp.sh stop             the kernel and the door stopped
cd ~/nk; MODE=${1:-fresh}
SOURCES="wn gcide mwt moby map sqldoc measured guess wikt"
wait_up(){ for i in $(seq 1 120); do python3 -c "import socket; socket.create_connection(('127.0.0.1', 7007), timeout=1).close()" 2>/dev/null && return 0; sleep 1; done; echo "the kernel did not answer in 120 s"; return 1; }
ask(){ python3 - "$1" <<'PY'
import socket, json, sys
s = socket.create_connection(("127.0.0.1", 7007)); s.sendall((sys.argv[1] + "\n").encode()); buf = b""
while True:
    d = s.recv(1 << 20)
    if not d: break
    buf += d
    if buf.endswith(b"\n"): break
print(buf.decode().strip()[:400])
PY
}
door(){ pkill -f serve8.py; sleep 0.3; (nohup python3 serve8.py 8058 7007 NEURON-POINT-OF-CONNECTION-nk-2026-10-30.html LINES-nk.txt FIRST-RUNS-nk.txt 0.0.0.0 > door.log 2>&1 &); sleep 1; cat door.log; }
build(){ gcc -O2 -Wall -Wno-unused-function -Wno-unused-parameter -I. -o nk nk.c nkvt.c nkio.c -L/usr/lib/x86_64-linux-gnu -l:libsqlite3.so.0 -lpthread -lm -ldl || exit 1; }
case "$MODE" in
  stop) pkill -x nk; pkill -f serve8.py; echo stopped ;;
  door) door ;;
  type) python3 nkbottom.py 7007 --lines "$2" --ledger "out/LEDGER-$(basename "$2" .txt).md" --quiet | tail -1 | cut -c1-300 ;;
  snapshot) D="out/snap-$(date +%Y%m%d-%H%M%S)"; ask "snapshot /home/james/nk/$D" && rm -f out/snap-latest && ln -s "$(basename $D)" out/snap-latest && echo "snapshot: $D" ;;
  fresh)
    if pgrep -x nk >/dev/null && [ "$2" != "--stop-the-running-kernel" ]; then echo "a kernel is running; fresh would replace its source files. Stop it first, or use a second kernel with its own folder (hp-agree-slice.sh)"; exit 1; fi
    pkill -x nk; pkill -f serve8.py; sleep 0.5; build; mkdir -p out
    rm -f sources/*.db; cp sources-egg/*.db sources/
    [ -s out/typed.txt ] && mv out/typed.txt "out/typed-until-$(date +%Y%m%d-%H%M%S).txt"; rm -f out/snap-latest
    (NK_JOURNAL=out/typed.txt nohup ./nk 7007 egg-symbols.txt sources $SOURCES > nk.log 2>&1 &); wait_up || exit 1; cat nk.log
    python3 nkbottom.py 7007 --lines LINES-nk.txt --ledger out/LEDGER-nk-60-lines.md --quiet | tail -1 | cut -c1-200
    door; echo "journal: $(wc -l < out/typed.txt) lines typed since the egg" ;;
  resume)
    pkill -x nk; pkill -f serve8.py; sleep 0.5; build
    [ -L out/snap-latest ] || { echo "no snapshot; use fresh"; exit 1; }
    SNAP="out/$(readlink out/snap-latest)"; N=$(cat "$SNAP/typed-lines.txt")
    for f in "$SNAP"/*.db; do b=$(basename "$f"); [ "$b" = brain.db -o "$b" = sixth.db ] && continue; cp "$f" "sources/$b"; done
    cp out/typed.txt out/typed-before-resume.txt; head -n "$N" out/typed-before-resume.txt > out/typed.txt; tail -n +"$((N + 1))" out/typed-before-resume.txt > out/replay.txt
    (NK_JOURNAL=out/typed.txt NK_LOAD="$SNAP" nohup ./nk 7007 egg-symbols.txt sources $SOURCES > nk.log 2>&1 &); wait_up || exit 1; cat nk.log
    if [ -s out/replay.txt ]; then python3 nkbottom.py 7007 --lines out/replay.txt --ledger out/LEDGER-replay.md --quiet | tail -1 | cut -c1-200; echo "$(wc -l < out/replay.txt) lines typed again after the snapshot"; fi
    door; echo "journal: $(wc -l < out/typed.txt) lines typed since the egg" ;;
esac
