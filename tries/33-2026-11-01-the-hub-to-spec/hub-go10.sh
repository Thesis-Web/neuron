#!/bin/bash
# hub-go10.sh: the space is the hop, not a landing (the owner, 10-30 and 11-01). The run steps from symbol to symbol; the space neuron is not landed on.
log(){ echo "$(date +%H:%M:%S) $*"; }
HUB=/home/exnulla/neuron/hub; P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; log "door down"
cd $HUB/brain; python3 -I - <<'PY'
import sqlite3
for path, S in (("brain.db", "main"), ("sixth.db", "sixth")):
    db = sqlite3.connect(path, isolation_level=None, timeout=120); db.execute("PRAGMA journal_mode = WAL")
    get = lambda n: db.execute("SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = ?", (n,)).fetchone()[0]
    changed = {}
    first_old = "(SELECT gate FROM seq WHERE run = (SELECT max(id) FROM run) AND pos = 1)"
    first_new = "(SELECT gate FROM seq WHERE run = (SELECT max(id) FROM run) AND gate <> 3 ORDER BY pos LIMIT 1)"
    for n in ("input_go", "third_go", "replay_go"):
        t = get(n)
        if first_old in t: changed[n] = t.replace(first_old, first_new)
    h = get("hit_go")
    if "NEW.pos + 1, NEW.next" in h:
        NP = "(SELECT min(pos) FROM seq WHERE run = NEW.run AND pos > NEW.pos AND gate <> 3)"
        h2 = h.replace("NEW.pos + 1, NEW.next", NP + ", NEW.next", 1)
        a = "(SELECT gate FROM seq WHERE run = NEW.run AND pos = NEW.pos + 2)"; assert h2.count(a) == 1
        h2 = h2.replace(a, "(SELECT gate FROM seq WHERE run = NEW.run AND pos > " + NP + " AND gate <> 3 ORDER BY pos LIMIT 1)")
        a = "coalesce((SELECT gate FROM seq WHERE run = NEW.run AND pos > NEW.pos + 1 AND gate <> 3 ORDER BY pos LIMIT 1), 0)"; assert h2.count(a) == 1
        h2 = h2.replace(a, "coalesce((SELECT gate FROM seq WHERE run = NEW.run AND pos > " + NP + " AND gate <> 3 ORDER BY pos LIMIT 1), 0)")
        changed["hit_go"] = h2
    db.execute("BEGIN IMMEDIATE")
    for n, t in changed.items(): db.execute(f"DROP TRIGGER {n}"); db.execute(t)
    db.execute("COMMIT"); print(S, "space is the hop in", sorted(changed)); db.close()
PY
cd $HUB/page; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; echo FINISHED
