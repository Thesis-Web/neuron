import sqlite3, sys, time, json
db = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True, timeout=30); db.execute("PRAGMA query_only = 1")
t0 = time.time(); schema = "main"
tables = set(r[0] for r in db.execute(f"SELECT name FROM {schema}.sqlite_master WHERE type = 'table' AND name GLOB '[0-9]*'"))
names = [n for n in tables if not n.endswith('.node')]; t1 = time.time()
dna = []
for n in names:
    for r in db.execute(f'SELECT shard, before, trigger, call, spawn, times FROM {schema}."{n}"'): dna.append((int(n),) + tuple(r))
t2 = time.time(); nodes = {}
for n in names:
    nodes[int(n)] = db.execute(f'SELECT count(*) FROM {schema}."{n}.node"').fetchone()[0] if n + '.node' in tables else 0
t3 = time.time()
rels = db.execute(f"SELECT gate, kind, other, run FROM {schema}.rel").fetchall()
mem = dict(db.execute(f"SELECT gate, count(*) FROM {schema}.run_memory GROUP BY gate").fetchall()); t4 = time.time()
firsts = dict(db.execute(f"SELECT run, gate FROM {schema}.seq WHERE pos = 1").fetchall()); t5 = time.time()
size = len(json.dumps({'dna': dna, 'nodes': nodes, 'rel': rels, 'tables': len(names), 'mem': mem, 'first': firsts})); t6 = time.time()
print("gates %d shards %d rel %d first %d | catalogue %.1f s, dna %.1f s, node counts %.1f s, rel+mem %.1f s, first %.1f s, json %.1f s (%.1f MB) | total %.1f s" % (len(names), len(dna), len(rels), len(firsts), t1 - t0, t2 - t1, t3 - t2, t4 - t3, t5 - t4, t6 - t5, size / 1e6, t6 - t0))
