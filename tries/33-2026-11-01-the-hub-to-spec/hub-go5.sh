#!/bin/bash
# hub-go5.sh: the door reads a list of gates in one read; the last character walkers (input_go, third_go) become the encoder.
log(){ echo "$(date +%H:%M:%S) $*"; }
HUB=/home/exnulla/neuron/hub; P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; log "door down"
cd $HUB/brain; python3 -I - <<'PY'
import sqlite3, re
s = open("bottom7.py").read()
a = """            v = ' '.join((db.execute(f"SELECT symbol FROM {schema}.label WHERE gate = ?", (int(x),)).fetchone() or ['?'])[0] for x in str(value).split()) or '(none)'"""
b = """            names = dict(db.execute(f"SELECT gate, symbol FROM {schema}.label WHERE gate IN ({','.join(str(int(x)) for x in str(value).split()) or 0})").fetchall())
            v = ' '.join(names.get(int(x), '?') for x in str(value).split()) or '(none)'"""
assert s.count(a) == 1; open("bottom7.py", "w").write(s.replace(a, b))
for path, S in (("brain.db", "main"), ("sixth.db", "sixth")):
    db = sqlite3.connect(path, isolation_level=None, timeout=60); db.execute("PRAGMA journal_mode = WAL"); db.execute("BEGIN IMMEDIATE")
    for n in ("input_go", "third_go"):
        q = db.execute("SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = ?", (n,)).fetchone()[0]
        if "encode(" in q: print(S, n, "already"); continue
        i = q.index("INSERT INTO label (symbol) SELECT s FROM (WITH RECURSIVE ch")
        k = q.index("INSERT INTO seq (run, pos, gate) SELECT ", i); e = q.index("ORDER BY n);", k) + len("ORDER BY n);")
        head = q[k:q.index(", n, (SELECT gate FROM label WHERE symbol = s) FROM", k)]
        new = q[:i] + head + f", key + 1, value FROM json_each(encode('{S}', NEW.text));" + q[e:]
        db.execute(f"DROP TRIGGER {n}"); db.execute(new); print(S, n, "encoder in:", (head[-60:]))
    db.execute("COMMIT"); db.close()
PY
cd $HUB/page; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; echo FINISHED
