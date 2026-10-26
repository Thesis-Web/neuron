#!/bin/bash
# dryrun.sh: run a scratch brain from 00-roots.lay + the given lay files, feed it lines, show its acts and rows.
# usage: tools/dryrun.sh [-s SECONDS] [-n] [-i "line"]... FILE.lay...
#   -n   do not add tools/dev-miss.lay (use when your files lay miss/end-of-run/sixth themselves)
#   -i   a line to say to the brain (repeatable; sent 1.5 s apart after birth)
#   -s   how long the brain lives (default 12 s)
#   -t   trace every step into acts.log (STEP lines: run, at, from, head, pad)
# The brain's folder is printed at the end; query it with: sqlite3 -readonly DIR/brain.db "..."
set -e
B=/home/james/neuron-build
SECS=12; STUB=1; INPUTS=()
TRACE=""
while getopts "s:ni:t" o; do case $o in s) SECS=$OPTARG;; n) STUB=0;; i) INPUTS+=("$OPTARG");; t) TRACE=1;; esac; done
shift $((OPTIND-1))
D=$(mktemp -d /home/james/ndry/d.XXXX)
mkdir -p $D/home $D/lay
cp $B/lay/00-roots.lay $D/lay/
[ $STUB = 1 ] && cp $B/tools/dev-miss.lay $D/lay/99-dev-miss.lay
for f in "$@"; do cp "$f" $D/lay/; done
# a scratch brain runs inside a memory cap: a runaway in a dry run must never take hp down
(systemd-run --user --scope -q -p MemoryMax=1500M -p MemorySwapMax=0 env NEURON_TRACE=$TRACE NEURON_HOME=$D/home timeout $SECS $B/kernel/neuron-dev run $D/lay > $D/run.out 2>&1 &)
sleep 4
python3 - "$D/home/ports/talk" "${INPUTS[@]}" <<'PY'
import socket,sys,time
path=sys.argv[1]; lines=sys.argv[2:]
if lines:
    s=socket.socket(socket.AF_UNIX); s.connect(path); s.settimeout(1.2)
    s.send(b"/who builder\n")
    for l in lines:
        s.send((l+"\n").encode()); time.sleep(1.5)
        try:
            while True:
                data=s.recv(65536)
                if not data: break
                sys.stdout.write("  < "+data.decode())
        except Exception: pass
PY
sleep $((SECS-2)); sleep 1
echo "=== loader"; cat $D/run.out
echo "=== acts (COMMIT and STEP lines dropped; STEP lines are in $D/home/acts.log)"; grep -v "COMMIT\|STEP" $D/home/acts.log
echo "=== run memories"; sqlite3 -readonly $D/home/brain.db "select id,kind,home,sig,outcome,seen,shape from mem where kind not in ('told') order by id" | tail -40
echo "=== brain: $D/home/brain.db"
