#!/bin/bash
# hub-go7.sh (2026-11-01): a definition is kept whether or not the point has been walked yet (the return arrives before the landing births the
# point: the dropped half); the dropped ones repaired from the returns the brain holds; the undefined re-asked; ok listens to the sheet.
log(){ echo "$(date +%H:%M:%S) $*"; }
HUB=/home/exnulla/neuron/hub; P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; log "door down"
cd $HUB/brain; python3 -I - <<'PY'
import sqlite3, time
DDL = lambda g: f'CREATE TABLE IF NOT EXISTS main."{g}" (shard INTEGER PRIMARY KEY, before INTEGER, trigger INTEGER, call INTEGER, spawn INTEGER, times INTEGER); CREATE TABLE IF NOT EXISTS main."{g}.node" (id INTEGER PRIMARY KEY, source INTEGER, run INTEGER)'
for path, S in (("brain.db", "main"), ("sixth.db", "sixth")):
    db = sqlite3.connect(path, isolation_level=None, timeout=120); db.execute("PRAGMA journal_mode = WAL")
    get = lambda n: db.execute("SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = ?", (n,)).fetchone()[0]
    sec = get("secondary_go")
    a = f""" SELECT mother('INSERT INTO {S}."' || about || '.node" (source, run) VALUES (?, ?)', arrival, id) FROM run WHERE id = (SELECT max(id) FROM run) AND about IS NOT NULL"""
    b = f""" SELECT mother('CREATE TABLE IF NOT EXISTS {S}."' || about || '" (shard INTEGER PRIMARY KEY, before INTEGER, trigger INTEGER, call INTEGER, spawn INTEGER, times INTEGER); CREATE TABLE IF NOT EXISTS {S}."' || about || '.node" (id INTEGER PRIMARY KEY, source INTEGER, run INTEGER)') FROM run WHERE id = (SELECT max(id) FROM run) AND about IS NOT NULL AND NOT EXISTS (SELECT 1 FROM sqlite_master WHERE name = about || '.node');""" + a
    if "CREATE TABLE IF NOT EXISTS" not in sec:
        assert sec.count(a) == 1, S; sec2 = sec.replace(a, b)
    else: sec2 = sec
    fill = get("sheet_fill"); comp = get("complete_go")
    ok = db.execute("SELECT gate FROM label WHERE symbol = 'ok'").fetchone()[0]
    if "ok listens" not in fill:
        k = fill.rindex("END")
        fill2 = fill[:k] + f"""  -- ok listens: a row of the ok neuron for each cell of a line's sheet, ticked when that cell populates
  INSERT INTO "{ok}" (shard, before, trigger, times) SELECT n + 1, NEW.cell, NULL, 0 FROM shards WHERE NEW.cell <> {ok} AND (SELECT kind FROM run WHERE id = NEW.run) = 0 AND NOT EXISTS (SELECT 1 FROM "{ok}" WHERE before = NEW.cell AND trigger IS NULL);
  UPDATE shards SET n = n + 1 WHERE (SELECT max(shard) FROM "{ok}") = n + 1;
  UPDATE "{ok}" SET times = times + 1 WHERE before = NEW.cell AND trigger IS NULL AND NEW.cell <> {ok} AND (SELECT kind FROM run WHERE id = NEW.run) = 0;
""" + fill[k:]
        k = comp.index("  INSERT INTO out_user")
        comp2 = comp[:k] + f"""  INSERT OR REPLACE INTO run_sheet (run, cell, state, value) SELECT NEW.run, {ok}, 1, 'ok' WHERE (SELECT kind FROM run WHERE id = NEW.run) = 0 AND NOT EXISTS (SELECT 1 FROM run_sheet WHERE run = NEW.run AND cell = {ok});
""" + comp[k:]
    else: fill2, comp2 = fill, comp
    db.execute("BEGIN IMMEDIATE")
    for n, q in (("secondary_go", sec2), ("sheet_fill", fill2), ("complete_go", comp2)):
        db.execute(f"DROP TRIGGER {n}"); db.execute(q)
    db.execute("COMMIT"); print(S, "physics laid", flush=True)
    # the repair: every point the sources answered about, its tables and its definition rows
    t = time.time(); made = rows = 0
    pts = [r[0] for r in db.execute("SELECT DISTINCT about FROM run WHERE kind = 3 AND about IS NOT NULL AND arrival <> 4")]
    have = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE name LIKE '%.node'")}
    db.execute("BEGIN IMMEDIATE")
    for g in pts:
        if f"{g}.node" not in have: db.executescript(DDL(g)); made += 1
        n = db.execute(f'SELECT count(*) FROM "{g}.node"').fetchone()[0]
        if n == 0:
            db.execute(f'INSERT INTO "{g}.node" (source, run) SELECT arrival, id FROM run WHERE kind = 3 AND about = ? AND arrival <> 4 ORDER BY id', (g,)); rows += db.execute("SELECT changes()").fetchone()[0]
    db.execute("COMMIT"); print(S, "repair: points with returns", len(pts), "tables made", made, "node rows laid", rows, round(time.time() - t, 1), "s", flush=True)
    db.execute("PRAGMA wal_checkpoint(TRUNCATE)"); db.close()
db = sqlite3.connect("sixth.db", isolation_level=None, timeout=120); db.execute("ATTACH 'brain.db' AS main")
n = db.execute("UPDATE spawned SET sent = 0 WHERE sent = 1 AND NOT EXISTS (SELECT 1 FROM main.sqlite_master m WHERE m.name = spawned.gate || '.node') RETURNING id").fetchall()
print("re-asked", len(n), "spawned", db.execute("SELECT sent, count(*) FROM spawned GROUP BY sent").fetchall()); db.close()
PY
cd $HUB/page; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; echo FINISHED
