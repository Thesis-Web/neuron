#!/usr/bin/env python3
# load_live.py (2026-10-29): puts a full source corpus into a live source file in place of the slice, keeping the file, its gate (me)
# and its triggers, so the door's attachment stays as it is. The slice rows go; the full rows come in chunks of 100,000 in their own
# transactions, so the brain's own asks wait at most a moment between chunks.   usage: python3 -I load_live.py <built.db> <live.db>
import sqlite3, sys, time
built, live = sys.argv[1], sys.argv[2]
db = sqlite3.connect(live, timeout=120, isolation_level=None)
db.execute("ATTACH ? AS b", (built,))
gate = db.execute("SELECT gate FROM me").fetchone()[0]
n0 = db.execute("SELECT count(*) FROM corpus").fetchone()[0]
top = db.execute("SELECT max(id) FROM b.corpus").fetchone()[0]
t = time.time()
db.execute("BEGIN IMMEDIATE"); db.execute("DELETE FROM corpus"); db.execute("COMMIT")
lo = 0
while lo < top:
    db.execute("BEGIN IMMEDIATE")
    db.execute("INSERT INTO corpus (word, hw, text) SELECT word, hw, text FROM b.corpus WHERE id > ? AND id <= ? ORDER BY id", (lo, lo + 100000))
    db.execute("COMMIT"); lo += 100000
n1, w1 = db.execute("SELECT count(*), count(DISTINCT word) FROM corpus").fetchone()
print(f"{live}: gate {gate}, {n0} slice lines out, {n1} lines in ({w1} words), {time.time() - t:.1f} s; inbox {db.execute('SELECT count(*) FROM inbox').fetchone()[0]}, outbox {db.execute('SELECT count(*) FROM outbox').fetchone()[0]}")
