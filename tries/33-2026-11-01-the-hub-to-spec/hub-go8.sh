#!/bin/bash
# hub-go8.sh: the door's graph read kept and read by key after the first read (what changed: hits since, returns since, new tables); the
# owner's page re-reads the brain every 45 s and shows the memory nodes of every run.
log(){ echo "$(date +%H:%M:%S) $*"; }
HUB=/home/exnulla/neuron/hub; cd $HUB/page; python3 -I - <<'PY'
s = open("serve7.py").read()
if "GRAPH = {" not in s:
    a = "def read_graph(db, schema):\n"
    b = '''GRAPH = {'built': False, 'dna': {}, 'nodes': {}, 'hit_id': 0, 'run_id': 0, 'names': set()}
def read_gate(db, schema, n, tables):
    GRAPH['dna'][n] = [(int(n),) + tuple(r) for r in db.execute(f'SELECT shard, before, trigger, call, spawn, times FROM {schema}."{n}"')]
    GRAPH['nodes'][int(n)] = db.execute(f'SELECT count(*) FROM {schema}."{n}.node"').fetchone()[0] if n + '.node' in tables else 0
def read_graph(db, schema):
    if schema == 'main':
        tables = set(r[0] for r in db.execute(f"SELECT name FROM {schema}.sqlite_master WHERE type = 'table' AND name GLOB '[0-9]*'"))
        names = set(n for n in tables if not n.endswith('.node'))
        hit_id = db.execute("SELECT coalesce(max(id), 0) FROM main.hit").fetchone()[0]; run_id = db.execute("SELECT coalesce(max(id), 0) FROM main.run").fetchone()[0]
        if not GRAPH['built']:
            for n in names: read_gate(db, schema, n, tables)
            GRAPH['built'] = True
        else:
            changed = set(str(r[0]) for r in db.execute("SELECT DISTINCT gate FROM main.hit WHERE id > ?", (GRAPH['hit_id'],))) | set(str(r[0]) for r in db.execute("SELECT DISTINCT about FROM main.run WHERE id > ? AND kind = 3 AND about IS NOT NULL", (GRAPH['run_id'],))) | (names - GRAPH['names'])
            for n in changed:
                if n in names: read_gate(db, schema, n, tables)
        GRAPH['hit_id'] = hit_id; GRAPH['run_id'] = run_id; GRAPH['names'] = names
        dna = [row for n in GRAPH['dna'] for row in GRAPH['dna'][n]]; nodes = dict(GRAPH['nodes'])
        rels = db.execute(f"SELECT gate, kind, other, run FROM {schema}.rel").fetchall() if db.execute(f"SELECT 1 FROM {schema}.sqlite_master WHERE name = 'rel'").fetchone() else []
        mem = dict(db.execute(f"SELECT gate, count(*) FROM {schema}.run_memory GROUP BY gate").fetchall())
        firsts = dict(db.execute(f"SELECT id, g FROM (SELECT id, (SELECT gate FROM {schema}.seq WHERE run = r.id AND pos = 1) AS g FROM {schema}.run r) WHERE g IS NOT NULL").fetchall())
        return {'dna': dna, 'nodes': nodes, 'rel': rels, 'tables': len(names), 'mem': mem, 'first': firsts}
    return read_graph_whole(db, schema)
def read_graph_whole(db, schema):
'''
    assert s.count(a) == 1; s = s.replace(a, b)
    a = "    READY.set(); env = STATE['env']\n"
    b = "    READY.set(); env = STATE['env']\n    try: env.submit(lambda db: read_graph(db, 'main'))   # the first graph read, once, so the page opens on the kept one\n    except Exception: pass\n"
    assert s.count(a) == 1; s = s.replace(a, b)
    open("serve7.py", "w").write(s); print("door: graph kept")
p = "NEURON-POINT-OF-CONNECTION-v6-2026-10-29.html"; s = open(p, encoding="utf-8").read()
if "reread" not in s:
    a = '<input type="checkbox" id="memall">'; b = '<input type="checkbox" id="memall" checked>'
    assert s.count(a) == 1; s = s.replace(a, b)
    a = "  open(0);\n"
    b = "  open(0);\n  // the page follows the brain: every 45 s, when nothing is running here, the tables are read again (by key at the door) and the drawing keeps up\n  setInterval(function reread() { if (!ready || busy || playing) return; loadBundle().then(function () { renderAll(); renderOut(); refreshMem(function () { render(TK, true); }); }).catch(function () {}); }, 45000);\n"
    assert s.count(a) == 1; s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s); print("page: rereads every 45 s, memory nodes on")
PY
P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && { kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; }; log "door down"
setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; echo FINISHED
