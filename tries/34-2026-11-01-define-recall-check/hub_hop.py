#!/usr/bin/env python3
# g34/hub_hop.py (2026-11-01, 18:40). The hop as one shard on the hub (8056, SQLite + triggers), as the owner's prose orders and as the kernel
# on hp now has it. Measured first: the hub page pulled every meaning to the colon because its landing trigger lays a pass row per
# (before, after) key on every landing: 1,342,183 DNA rows over 314,126 point tables, 170,683 on the colon's own table, 181,588 rows with the
# colon before them, drawn by the page as lines; rel rows (2,296,711, like/opposite) were whole. Three changes, SQL on the brain's own tables:
#  1. land_go's second step: when no row matches the landing's key, count it on the space's one row (table "3", shard 17) instead of inserting
#     a row; the receipt names shard 17. The old trigger text is saved beside this script before it is replaced.
#  2. Every point table's pass rows (no call, no spawn) are folded: their times onto shard 17, the rows deleted. Kept: rows with a call or
#     spawn, the ok neuron's rows (table "81"), the space's row, and the birth rows (before and trigger NULL) of the core (gates <= 90).
#  3. run_receipt, hit and run_memory rows that named a folded shard name shard 17 (so the page's history still reads), if their counts allow.
# WAL: the hub keeps running; each batch is one transaction.
import sqlite3, time, sys, os
DB = '/home/exnulla/neuron/hub/brain/brain.db'
ARCH = '/mnt/d/Neuron/tries/34-2026-11-01-define-recall-check'
con = sqlite3.connect(DB, timeout=600, isolation_level=None); con.execute('PRAGMA busy_timeout = 600000')
t0 = time.time()
old = con.execute("SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = 'land_go'").fetchone()[0]
open(ARCH + '/hub-land_go-before-2026-11-01.sql', 'w').write(old + ';\n'); print('old land_go saved,', len(old), 'chars')
i = old.index("INSERT OR REPLACE INTO step (k, v) SELECT 1, mother('INSERT INTO ' || 'main.\"' || NEW.gate")
j = old.index("WHERE (SELECT v FROM step WHERE k = 1) = 'ok';", i) + len("WHERE (SELECT v FROM step WHERE k = 1) = 'ok';")
step2 = "INSERT OR REPLACE INTO step (k, v) SELECT 1, mother('UPDATE main.\"3\" SET times = times + 1 WHERE shard = 17 RETURNING shard, call, spawn') WHERE (SELECT v FROM step WHERE k = 1) = 'ok';"
new = old[:i] + step2 + old[j:]
assert "SELECT n + 1, ?, ?, 1 FROM main.shards" not in new and new.count('shard = 17') == 1
if 'DRY' in sys.argv: print(new[:1200]); sys.exit(0)
con.execute('BEGIN'); con.execute('DROP TRIGGER land_go'); con.execute(new); con.execute('COMMIT')
chk = con.execute("SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = 'land_go'").fetchone()[0]
print('land_go replaced:', 'shard = 17' in chk and 'FROM main.shards RETURNING' not in chk, '| %.1f s' % (time.time() - t0), flush=True)
open(ARCH + '/hub-land_go-after-2026-11-01.sql', 'w').write(chk + ';\n')
# 2. the fold
names = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name GLOB '[0-9]*' ORDER BY CAST(name AS INTEGER)")]
print('point tables:', len(names), flush=True)
con.execute('CREATE TABLE IF NOT EXISTS kept_shards (shard INTEGER PRIMARY KEY)'); con.execute('DELETE FROM kept_shards')
moved = 0; folded = 0; kept = 0; done = 0; B = 1500
for k in range(0, len(names), B):
    con.execute('BEGIN')
    for name in names[k:k + B]:
        g = int(name)
        if name == '3' or name == '81':
            for (sh,) in con.execute('SELECT shard FROM "%s"' % name): con.execute('INSERT OR IGNORE INTO kept_shards VALUES (?)', (sh,)); kept += 1
            continue
        passcond = 'call IS NULL AND spawn IS NULL' + (' AND NOT (before IS NULL AND trigger IS NULL)' if g <= 90 else '')
        s, n = con.execute('SELECT coalesce(sum(times), 0), count(*) FROM "%s" WHERE %s' % (name, passcond)).fetchone()
        if n:
            moved += s; folded += n; con.execute('DELETE FROM "%s" WHERE %s' % (name, passcond))
        for (sh,) in con.execute('SELECT shard FROM "%s"' % name): con.execute('INSERT OR IGNORE INTO kept_shards VALUES (?)', (sh,)); kept += 1
    con.execute('COMMIT'); done += len(names[k:k + B])
    if done % 30000 < B: print('  %d tables: folded %d rows, kept %d, %.0f s' % (done, folded, kept, time.time() - t0), flush=True)
con.execute('UPDATE "3" SET times = times + ? WHERE shard = 17', (moved,))
print('fold done: folded %d rows, times moved %d, kept %d rows; hop shard 17 times now %s | %.0f s' % (folded, moved, kept, con.execute('SELECT times FROM "3" WHERE shard = 17').fetchone()[0], time.time() - t0), flush=True)
# 3. receipts and memory rows that named a folded shard
for tbl in ('run_receipt', 'hit', 'run_memory'):
    n = con.execute('SELECT count(*) FROM %s' % tbl).fetchone()[0]; print(tbl, 'rows', n, flush=True)
    if n > 12000000: print('  left as they are (too many to rewrite live); the page shows such a hit as not in any DNA table now'); continue
    t = time.time(); con.execute('BEGIN')
    c = con.execute('UPDATE %s SET shard = 17 WHERE shard <> 17 AND shard NOT IN (SELECT shard FROM kept_shards)' % tbl).rowcount
    con.execute('COMMIT'); print('  repointed %d rows to shard 17 in %.0f s' % (c, time.time() - t), flush=True)
con.execute('DROP TABLE kept_shards')
print('ALL DONE in %.0f s' % (time.time() - t0))
