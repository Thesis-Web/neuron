#!/usr/bin/env python3
# serve7.py (2026-10-29, v7; v7.1 2026-10-30: reads and typed lines run on the one router connection between batches): the v7 brains behind a local HTTP door, so the Point Of Connection page can type a line at the user's prompt
# or the sixth's and read the brains' tables back. From serve6.py. What v7 changes: the brain is never held by one line. A typed line is
# an insert into a brain's input on the typing connection; its hops are pasted one at a time by the router loops (bottom7.py); every read
# the page asks for (the graph, the lines, a SELECT) runs at once on a reading connection of its own, in WAL mode, without waiting for a
# run to end. The door still decides nothing: it types what it is given and runs the SELECT it is asked for.
# usage: python3 serve7.py [port]      default 8057; then open http://localhost:8057/
import sys, os, json, time, threading, queue, http.server, urllib.parse, traceback, sqlite3
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); BRAINDIR = os.path.join(ROOT, 'brain')
sys.path.insert(0, BRAINDIR)
import bottom7
def find_page():
    for p in [os.path.join(HERE, f) for f in sorted(os.listdir(HERE)) if f.endswith('.html')]: return p
    cand = os.path.join(os.path.dirname(ROOT), '19-2026-10-29-v6-space-shards-tools-and-page', 'page', 'NEURON-POINT-OF-CONNECTION-v6-2026-10-29.html')
    return cand
PAGE = find_page()
LINES = os.path.join(BRAINDIR, 'LINES-v6.txt'); FIRST = os.path.join(ROOT, 'FIRST-RUNS-v6-2026-10-29.txt')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8057
HISTORY_CAP = int(os.environ.get('NK_HISTORY_CAP', '50000'))
STARTED = time.time()
JOBS = queue.Queue(); JOBMAP = {}; JOBLOCK = threading.Lock(); JOBN = [0]
READY = threading.Event(); STATE = {'env': None, 'busy': None, 'error': None, 'read': None}
READLOCK = threading.Lock()

class Job:
    def __init__(self, kind, args):
        with JOBLOCK: JOBN[0] += 1; self.id = JOBN[0]; JOBMAP[self.id] = self
        self.kind, self.args, self.done, self.result, self.error = kind, args, threading.Event(), None, None
        self.created, self.started, self.finished, self.progress = time.time(), None, None, None
    def view(self):
        now = time.time()
        return {'id': self.id, 'kind': self.kind, 'done': self.done.is_set(), 'result': self.result, 'error': self.error, 'progress': self.progress,
                'elapsed': (self.finished or now) - (self.started or now) if self.started else None, 'line': self.args.get('line') if isinstance(self.args, dict) else None}

def typing_thread():
    """the typing connection and the router loops; a typed line waits here until its hops have run out, so its ledger row is whole"""
    try:
        STATE['env'] = bottom7.open_brain(); STATE['read'] = STATE['env']
    except Exception:
        STATE['error'] = traceback.format_exc(); READY.set(); return
    READY.set(); env = STATE['env']
    try: env.submit(lambda db: read_graph(db, 'main'))   # the first graph read, once, so the page opens on the kept one
    except Exception: pass
    while True:
        j = JOBS.get(); j.started = time.time(); STATE['busy'] = j
        try:
            if j.kind == 'type':
                if '{run:' in j.args['line'] and not bottom7.RUNS and os.path.exists(LINES): bottom7.match_runs(env.db, [l.rstrip('\n') for l in open(LINES, encoding='utf-8')])
                j.result = bottom7.type_line(env, bottom7.fill(env.db, j.args['line']), quiet=True)
            elif j.kind == 'fresh':
                raise ValueError("v7's door does not lay fresh brains; lay them with the scripts and start the door again")
            else: raise ValueError('unknown job ' + j.kind)
        except Exception as e:
            j.error = str(e) or e.__class__.__name__
        j.finished = time.time(); STATE['busy'] = None; j.done.set()

threading.stack_size(1 << 30)
threading.Thread(target=typing_thread, daemon=True).start()
threading.stack_size(0)

def submit(kind, args, wait=None):
    j = Job(kind, args); JOBS.put(j)
    if wait is not None: j.done.wait(wait)
    return j
READONLY = ('SELECT', 'WITH', 'PRAGMA TABLE_INFO', 'PRAGMA DATABASE_LIST')

GRAPH = {'built': False, 'dna': {}, 'nodes': {}, 'hit_id': 0, 'run_id': 0, 'names': set()}
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
    tables = set(r[0] for r in db.execute(f"SELECT name FROM {schema}.sqlite_master WHERE type = 'table' AND name GLOB '[0-9]*'"))   # one read of the catalogue, not one per gate
    names = [n for n in tables if not n.endswith('.node')]
    dna = []
    for n in names:
        for r in db.execute(f'SELECT shard, before, trigger, call, spawn, times FROM {schema}."{n}"'): dna.append((int(n),) + tuple(r))
    nodes = {}
    for n in names:
        c = db.execute(f'SELECT count(*) FROM {schema}."{n}.node"').fetchone()[0] if n + '.node' in tables else 0
        nodes[int(n)] = c
    rels = db.execute(f"SELECT gate, kind, other, run FROM {schema}.rel").fetchall() if db.execute(f"SELECT 1 FROM {schema}.sqlite_master WHERE name = 'rel'").fetchone() else []
    mem = dict(db.execute(f"SELECT gate, count(*) FROM {schema}.run_memory GROUP BY gate").fetchall())
    firsts = dict(db.execute(f"SELECT id, g FROM (SELECT id, (SELECT gate FROM {schema}.seq WHERE run = r.id AND pos = 1) AS g FROM {schema}.run r) WHERE g IS NOT NULL").fetchall())
    return {'dna': dna, 'nodes': nodes, 'rel': rels, 'tables': len(names), 'mem': mem, 'first': firsts}

def read_lines(db):
    out = []
    for which, path in (('tools', LINES), ('first', FIRST)):
        if not os.path.exists(path): continue
        raw = [l.rstrip('\n') for l in open(path, encoding='utf-8')]
        runs = bottom7.match_runs(db, raw) if which == 'tools' else None
        k = 0; note = []
        for l in raw:
            if not l.strip(): note = []; continue
            if l.startswith('#'): note.append(l[1:].strip()); continue
            k += 1
            try: filled = bottom7.fill(db, l)
            except Exception: filled = l
            out.append({'file': which, 'k': k, 'note': ' '.join(note), 'raw': l, 'line': filled, 'run': (runs[k - 1] if runs and k - 1 < len(runs) else None)})
            note = []
    return {'lines': out}

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *a): pass
    def send(self, code, obj, ctype='application/json'):
        body = obj if isinstance(obj, bytes) else json.dumps(obj, default=str).encode()
        self.send_response(code); self.send_header('Content-Type', ctype + ('' if isinstance(obj, bytes) and not ctype.startswith('text') else '; charset=utf-8'))
        self.send_header('Content-Length', str(len(body))); self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(body)
    def do_OPTIONS(self):
        self.send_response(204); self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Access-Control-Allow-Headers', 'content-type'); self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'); self.end_headers()
    def body(self):
        n = int(self.headers.get('Content-Length') or 0); return json.loads(self.rfile.read(n) or b'{}')
    def read(self, fn):
        """a read runs on the router's own connection between two batches of hops (v7.1), so it never meets a changed schema"""
        if not READY.is_set() or STATE['error'] or STATE['env'] is None: return self.send(503, {'error': STATE['error'] or 'the brain is still opening'})
        try: return self.send(200, STATE['env'].submit(fn, timeout=600))
        except Exception as e: return self.send(500, {'error': str(e) or e.__class__.__name__})
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); qs = urllib.parse.parse_qs(u.query)
        if u.path in ('/', '/index.html'):
            try: self.send(200, open(PAGE, 'rb').read(), 'text/html')
            except FileNotFoundError: self.send(404, {'error': 'page not found: ' + PAGE})
            return
        if u.path == '/api/info':
            env = STATE['env']
            routers = {s: {'idle': env.router.idle.is_set(), 'hops': env.router.hops[s], 'refused': env.router.refused[s]} for s in ('main', 'sixth')} if env else None
            return self.send(200, {'brain': bottom7.BRAIN, 'sixth': bottom7.SIXTH, 'sources': bottom7.SRC, 'sqlite': sqlite3.sqlite_version, 'started': STARTED, 'ready': READY.is_set() and env is not None, 'error': STATE['error'], 'busy': STATE['busy'].view() if STATE['busy'] else None, 'queued': JOBS.qsize(), 'routers': routers, 'version': 'v7'})
        if u.path == '/api/graph': return self.read(lambda db: read_graph(db, qs.get('schema', ['main'])[0]))
        if u.path == '/api/lines': return self.read(read_lines)
        if u.path == '/api/prof': return self.send(200, {k: v for k, v in sorted(STATE['env'].router.prof.items(), key=lambda x: -x[1][1])[:16]})
        if u.path == '/api/job':
            j = JOBMAP.get(int(qs.get('id', ['0'])[0])); return self.send(200, j.view()) if j else self.send(404, {'error': 'no such job'})
        self.send(404, {'error': 'no such path'})
    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        try: d = self.body()
        except Exception as e: return self.send(400, {'error': 'bad json: ' + str(e)})
        if not READY.is_set() or STATE['error']: return self.send(503, {'error': STATE['error'] or 'the brain is still opening'})
        if u.path == '/api/type':
            line = str(d.get('line') or '').strip()
            if not line: return self.send(400, {'error': 'an empty line'})
            if d.get('prompt') == 'sixth' and not line.startswith('6> '): line = '6> ' + line
            j = submit('type', {'line': line}); return self.send(200, j.view())
        if u.path == '/api/fresh':
            j = submit('fresh', {}); return self.send(200, j.view())
        if u.path == '/api/q':
            sql = str(d.get('sql') or '').strip()
            if not sql.upper().startswith(READONLY): return self.send(400, {'error': 'only a SELECT is read through this door; a line is typed through /api/type'})
            def q(db):
                params = d.get('params') or []
                # 2026-10-30 06:00: the page's history read asks for every receipt after the last it saw; on a brain of millions this door
                # answers the newest HISTORY_CAP (50,000) so the page can open; the brain itself is untouched. Takes effect when the door is started again.
                if sql.startswith('SELECT id, run, gate, shard FROM main.run_receipt WHERE id > ?') and params:
                    top = db.execute('SELECT max(id) FROM main.run_receipt').fetchone()[0] or 0
                    if top - int(params[0]) > HISTORY_CAP: params = [top - HISTORY_CAP]
                cur = db.execute(sql, params); cols = [c[0] for c in cur.description] if cur.description else []
                return {'cols': cols, 'rows': cur.fetchall()}
            return self.read(q)
        self.send(404, {'error': 'no such path'})

if __name__ == '__main__':
    sys.setrecursionlimit(1000000)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H); srv.daemon_threads = True
    print('brain  ', bottom7.BRAIN); print('sixth  ', bottom7.SIXTH); print('sources', bottom7.SRC); print('page   ', PAGE); print('open    http://localhost:%d/' % PORT, flush=True)
    try: srv.serve_forever()
    except KeyboardInterrupt: pass
