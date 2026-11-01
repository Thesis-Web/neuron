#!/bin/bash
# hub-go.sh (2026-11-01): with the door down: the brain out of /tmp, the physics laid, the sources' flush off, the door up.
log(){ echo "$(date +%H:%M:%S) $*"; }
OLD=/tmp/claude-1000/-home-exnulla-neuron-v3/4e06790d-7d80-473e-8cc8-4014a0561261/scratchpad/w/19; NEW=/home/exnulla/neuron/hub
HERE=/mnt/d/Neuron/tries/33-2026-11-01-the-hub-to-spec
kill 445330 2>/dev/null; sleep 2; log "twin stopped"
[ -d "$NEW" ] && { log "$NEW exists; stopping"; exit 1; }
mv "$OLD" "$NEW" && log "the brain is at $NEW"; ls -la --block-size=M "$NEW/brain/brain.db" | cut -c24-90
cd "$NEW/brain"; python3 -I "$HERE/hub_fix.py" "$NEW/brain" 2>&1 | tail -n 4; log "physics laid"
python3 - <<'PY'
p = "bottom7.py"; s = open(p).read()
a = "db.execute('ATTACH ? AS sixth', (SIXTH,)); db.execute('PRAGMA sixth.journal_mode = WAL')"
b = a + "; db.execute('PRAGMA sixth.synchronous = NORMAL')"
assert s.count(a) == 1; s = s.replace(a, b)
a = "            except sqlite3.Error: pass\n"
b = a + "            db.execute(f'PRAGMA {s}.synchronous = OFF')   # a source is read; only its mailbox is written: no flush to disk on every ask\n"
assert s.count(a) == 1; s = s.replace(a, b)
open(p, "w").write(s)
PY
cd "$NEW/page"; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; curl -s -m 5 http://localhost:8056/api/info | cut -c1-260; echo; echo FINISHED
