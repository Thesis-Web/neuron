#!/bin/bash
# hub-go4.sh: every source's carry hands its return to mother as parameters: one statement, prepared once. The kernel's carry-params.sh of 10-30.
log(){ echo "$(date +%H:%M:%S) $*"; }
HUB=/home/exnulla/neuron/hub; P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; log "door down"
cd $HUB/sources; python3 -I - <<'PY'
import sqlite3
for s in ('wn','gcide','mwt','moby','map','sqldoc','measured','guess','wikt'):
    db = sqlite3.connect(s + '.db', isolation_level=None, timeout=30)
    old = db.execute("SELECT sql FROM sqlite_master WHERE name = 'carry'").fetchone()[0]
    if 'VALUES (?, ?, ?, ?, ?)' in old: print(s, 'already'); continue
    db.execute("BEGIN IMMEDIATE"); db.execute("DROP TRIGGER carry")
    db.execute("""CREATE TRIGGER carry AFTER INSERT ON outbox BEGIN
  SELECT mother('INSERT INTO main.secondary (run, cell, gate, about, text) VALUES (?, ?, ?, ?, ?)', NEW.run, NEW.cell, (SELECT gate FROM me), NEW.about, NEW.text);
  DELETE FROM outbox WHERE id = NEW.id;
END"""); db.execute("COMMIT"); db.close(); print(s, 'carry by parameters')
PY
cd $HUB/page; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; echo FINISHED
