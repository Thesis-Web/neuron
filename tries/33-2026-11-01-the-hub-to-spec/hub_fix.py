#!/usr/bin/env python3
# hub_fix.py (2026-11-01): the hub's physics to the owner's words, what the kernel learned, laid into both brain files while the door is down.
# "pull the fucking information to the run data sheet" (returns are not walked); draft 3.2 "one hop to the memory. No rows fire, nothing is laid,
# and mother is not called" (a closed formula fires from its list); "walkers are illegal". usage: hub_fix.py BRAINDIR
import sqlite3, sys, os
D = sys.argv[1]
def holes(s, run):
    return f"coalesce((SELECT value FROM run_sheet WHERE run = {run} AND cell = s.gate AND state = 1), (SELECT value FROM run_sheet WHERE run = (SELECT parent FROM run WHERE id = {run}) AND cell = s.gate AND state = 1), (SELECT value FROM run_sheet WHERE run = (SELECT parent FROM run WHERE id = (SELECT parent FROM run WHERE id = {run})) AND cell = s.gate AND state = 1), l.symbol)"
def patch(path, S):
    db = sqlite3.connect(path, isolation_level=None, timeout=60); db.execute("PRAGMA journal_mode = WAL")
    get = lambda n: db.execute("SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = ?", (n,)).fetchone()[0]
    if db.execute("SELECT 1 FROM sqlite_master WHERE name = 'fire_go'").fetchone(): print(S, "already done"); return
    sec, rep, end = get("secondary_go"), get("replay_go"), get("ended_go")
    # ---- a return arrives on the sheet; it is not walked
    i = sec.index(" INSERT INTO land (run, pos, gate, before, next, via) SELECT (SELECT max(id) FROM run), 0,"); j = sec.rindex("END")
    has = "EXISTS (SELECT 1 FROM seq WHERE run = (SELECT max(id) FROM run) AND pos = 1)"
    sec2 = sec[:i] + f""" INSERT OR REPLACE INTO run_sheet (run, cell, state, value) SELECT parent, cell, 1, id FROM run WHERE id = (SELECT max(id) FROM run) AND cell IS NOT NULL AND parent IS NOT NULL AND {has}; SELECT mother('INSERT INTO {S}."' || about || '.node" (source, run) VALUES (?, ?)', arrival, id) FROM run WHERE id = (SELECT max(id) FROM run) AND about IS NOT NULL AND {has};\n""" + sec[j:]
    # ---- a closed formula fires from its list
    a = "INSERT INTO run (arrival, parent, root, kind, cell, about, at, moment) VALUES (2, NEW.parent, NULL, NEW.kind, NULL, NULL, (SELECT n FROM clock), strftime('%s', 'now'));"
    b = "INSERT INTO run (arrival, parent, root, kind, cell, about, at, moment, src) VALUES (2, NEW.parent, NULL, NEW.kind, NULL, NULL, (SELECT n FROM clock), strftime('%s', 'now'), NEW.source);"
    assert rep.count(a) == 1; rep2 = rep.replace(a, b)
    a = "FROM seq WHERE run = NEW.source;"; b = "FROM seq WHERE run = NEW.source AND NOT EXISTS (SELECT 1 FROM closed WHERE source = NEW.source);"
    assert rep2.count(a) == 1; rep2 = rep2.replace(a, b)
    k = rep2.rindex("END"); a = "WHERE EXISTS (SELECT 1 FROM seq WHERE run = (SELECT max(id) FROM run) AND pos = 1);"
    assert rep2.count(a) == 1
    rep2 = rep2.replace(a, "WHERE NOT EXISTS (SELECT 1 FROM closed WHERE source = NEW.source) AND EXISTS (SELECT 1 FROM seq WHERE run = (SELECT max(id) FROM run) AND pos = 1);")
    k = rep2.rindex("END")
    rep2 = rep2[:k] + f"""  INSERT INTO hop (text, p1, p2) SELECT 'INSERT INTO {S}.fire (run, ord) VALUES (?, ?)', (SELECT max(id) FROM run), ord FROM (SELECT ord FROM fire_ev WHERE source = NEW.source ORDER BY ord DESC);
  UPDATE closed SET again = again + 1 WHERE source = NEW.source;
""" + rep2[k:]
    k = end.rindex("END")
    end2 = end[:k] + """  INSERT OR IGNORE INTO closed (source, run) SELECT r.src, NEW.run FROM run r WHERE r.id = NEW.run AND r.src IS NOT NULL AND NOT EXISTS (SELECT 1 FROM closed c WHERE c.source = r.src) AND NOT EXISTS (SELECT 1 FROM hit h WHERE h.run = NEW.run AND h.via = 1);
  INSERT OR IGNORE INTO fire_ev (source, ord, pos, gate, call, spawn) SELECT c.source, h.pos * 2, h.pos, h.gate, h.call, h.spawn FROM closed c JOIN hit h ON h.run = c.run WHERE c.run = NEW.run AND (h.call IS NOT NULL OR h.spawn IS NOT NULL);
  INSERT OR IGNORE INTO fire_ev (source, ord, pos, gate, opened) SELECT c.source, b.pos * 2 + 1, b.pos, 29, b.o FROM closed c JOIN (SELECT pos, lag(pos) OVER (ORDER BY pos) AS o, row_number() OVER (ORDER BY pos) AS n FROM hit WHERE run = NEW.run AND gate = 29 AND via = 0) b ON b.n % 2 = 0 WHERE c.run = NEW.run;
""" + end[k:]
    fire = f"""CREATE TRIGGER fire_go AFTER INSERT ON fire BEGIN
  INSERT INTO hop (text, p1, p2, p3) SELECT 'INSERT INTO {S}.replay (parent, source, kind) VALUES (?, ?, ?)', NEW.run, e.spawn, 2 FROM fire_ev e WHERE e.source = (SELECT src FROM run WHERE id = NEW.run) AND e.ord = NEW.ord AND e.spawn IS NOT NULL;
  INSERT INTO hop (text, p1, p2, p3) SELECT 'INSERT INTO {S}.replay (parent, source, kind) VALUES (?, ?, ?)', NEW.run, e.call, 1 FROM fire_ev e WHERE e.source = (SELECT src FROM run WHERE id = NEW.run) AND e.ord = NEW.ord AND e.call IS NOT NULL;
  INSERT INTO out_mother (run, cell, gate, at, text) SELECT NEW.run, 22, 29, (SELECT at FROM run WHERE id = NEW.run), (SELECT group_concat(piece, '') FROM (SELECT {holes(None, 'NEW.run')} AS piece FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = e.source AND s.pos > e.opened AND s.pos < e.pos ORDER BY s.pos)) FROM fire_ev e WHERE e.source = (SELECT src FROM run WHERE id = NEW.run) AND e.ord = NEW.ord AND e.opened IS NOT NULL;
  DELETE FROM fire WHERE id = NEW.id;
END"""
    db.execute("BEGIN IMMEDIATE")
    db.execute("ALTER TABLE run ADD COLUMN src INTEGER")
    db.execute("CREATE TABLE closed (source INTEGER PRIMARY KEY, run INTEGER, again INTEGER DEFAULT 0)")
    db.execute("CREATE TABLE fire_ev (source INTEGER, ord INTEGER, pos INTEGER, gate INTEGER, call INTEGER, spawn INTEGER, opened INTEGER, PRIMARY KEY (source, ord)) WITHOUT ROWID")
    db.execute("CREATE TABLE fire (id INTEGER PRIMARY KEY, run INTEGER, ord INTEGER)")
    for n, q in (("secondary_go", sec2), ("replay_go", rep2), ("ended_go", end2)):
        db.execute(f"DROP TRIGGER {n}"); db.execute(q)
    db.execute(fire)
    db.execute("COMMIT")
    db.execute("CREATE INDEX IF NOT EXISTS hit_run ON hit (run)")
    db.execute("PRAGMA wal_checkpoint(TRUNCATE)"); db.close(); print(S, "patched")
patch(os.path.join(D, "brain.db"), "main"); patch(os.path.join(D, "sixth.db"), "sixth")
