#!/usr/bin/env python3
# serve6.py (2026-10-29): the v6 brains behind a local HTTP door, so the Point Of Connection v6 page can type a line at the user's
# prompt or the sixth's and read the brains' tables back. The door does two things and nothing else: a typed line goes to the
# bottom's type_line (an insert into main.input or sixth.input; the brain's triggers and mother do the rest, exactly as at the
# terminal), and a SELECT the page asks for is run and its rows sent back. Anything else is refused. It decides nothing.
# From serve5.py. v6: no call types a file of lines (the owner types each line; the page lists them to click into the prompt); the door
# serves the lines file with its {run:k} and {gate:x} read from the brains; the graph read returns the DNA rows, the node row counts,
# the relationship rows, the memory counts per gate and the calls' first gates in one go.
# usage: python3 serve6.py [port]      default 8056; then open http://localhost:8056/
import sys, os, json, time, threading, queue, http.server, urllib.parse, traceback
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); BRAINDIR = os.path.join(ROOT, 'brain')
sys.path.insert(0, BRAINDIR)
import bottom6 as bottom5
PAGE = os.path.join(HERE, 'NEURON-POINT-OF-CONNECTION-v6-2026-10-29.html')
LINES = os.path.join(BRAINDIR, 'LINES-v6.txt'); FIRST = os.path.join(ROOT, 'FIRST-RUNS-v6-2026-10-29.txt')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8056
STARTED = time.time()
JOBS = queue.Queue(); JOBMAP = {}; JOBLOCK = threading.Lock(); JOBN = [0]
READY = threading.Event(); STATE = {'db': None, 'busy': None, 'error': None}

class Job:
    def __init__(self, kind, args):
        with JOBLOCK: JOBN[0] += 1; self.id = JOBN[0]; JOBMAP[self.id] = self
        self.kind, self.args, self.done, self.result, self.error = kind, args, threading.Event(), None, None
        self.created, self.started, self.finished, self.progress = time.time(), None, None, None
    def view(self):
        now = time.time()
        return {'id': self.id, 'kind': self.kind, 'done': self.done.is_set(), 'result': self.result, 'error': self.error, 'progress': self.progress,
                'elapsed': (self.finished or now) - (self.started or now) if self.started else None, 'line': self.args.get('line') if isinstance(self.args, dict) else None}

def brain_thread():
    try:
        STATE['db'] = bottom5.open_brain()
    except Exception:
        STATE['error'] = traceback.format_exc(); READY.set(); return
    READY.set(); db = STATE['db']
    while True:
        j = JOBS.get(); j.started = time.time(); STATE['busy'] = j
        try:
            if j.kind == 'type':
                if not bottom5.RUNS and os.path.exists(LINES): bottom5.match_runs(db, [l.rstrip('\n') for l in open(LINES, encoding='utf-8')])
                r = bottom5.type_line(db, bottom5.fill(db, j.args['line']), quiet=True)
                j.result = r
            elif j.kind == 'graph':
                schema = j.args.get('schema') or 'main'
                names = [r[0] for r in db.execute(f"SELECT name FROM {schema}.sqlite_master WHERE type = 'table' AND name GLOB '[0-9]*' AND name NOT GLOB '*.node'")]
                dna = []
                for n in names:
                    for r in db.execute(f'SELECT shard, before, trigger, call, spawn, times FROM {schema}."{n}"'): dna.append((int(n),) + tuple(r))
                nodes = {}
                for n in names:
                    c = db.execute(f'SELECT count(*) FROM {schema}."{n}.node"').fetchone()[0] if db.execute(f"SELECT 1 FROM {schema}.sqlite_master WHERE name = ?", (n + '.node',)).fetchone() else 0
                    nodes[int(n)] = c
                rels = db.execute(f"SELECT gate, kind, other, run FROM {schema}.rel").fetchall() if db.execute(f"SELECT 1 FROM {schema}.sqlite_master WHERE name = 'rel'").fetchone() else []
                mem = dict(db.execute(f"SELECT gate, count(*) FROM {schema}.run_memory GROUP BY gate").fetchall())
                firsts = dict(db.execute(f"SELECT run, gate FROM {schema}.seq WHERE pos = 1").fetchall())
                j.result = {'dna': dna, 'nodes': nodes, 'rel': rels, 'tables': len(names), 'mem': mem, 'first': firsts}
            elif j.kind == 'lines':
                # the lines files, each line with its grounding, its {run:k}/{gate:x} read from the brains now, and the run it started if it was typed
                out = []
                for which, path in (('tools', LINES), ('first', FIRST)):
                    if not os.path.exists(path): continue
                    raw = [l.rstrip('\n') for l in open(path, encoding='utf-8')]
                    runs = bottom5.match_runs(db, raw) if which == 'tools' else None
                    k = 0; note = []
                    for l in raw:
                        if not l.strip(): note = []; continue
                        if l.startswith('#'): note.append(l[1:].strip()); continue
                        k += 1
                        try: filled = bottom5.fill(db, l)
                        except Exception: filled = l
                        out.append({'file': which, 'k': k, 'note': ' '.join(note), 'raw': l, 'line': filled, 'run': (runs[k - 1] if runs and k - 1 < len(runs) else None)})
                        note = []
                j.result = {'lines': out}
            elif j.kind == 'fresh':
                db.close(); STATE['db'] = None
                import subprocess
                for f in ('brain.db', 'sixth.db', 'brain.db-journal', 'sixth.db-journal'):
                    p = os.path.join(BRAINDIR, f)
                    if os.path.exists(p): os.remove(p)
                subprocess.run(['sqlite3', os.path.join(BRAINDIR, 'brain.db'), '.read egg6.sql'], cwd=BRAINDIR, check=True)
                subprocess.run(['sqlite3', os.path.join(BRAINDIR, 'sixth.db'), '.read egg6-sixth.sql'], cwd=BRAINDIR, check=True)
                sat = os.path.join(ROOT, '..', '11-2026-10-25-new-v18-core', 'NEURON-v18-CORE-2026-10-25', 'sat172.json')
                if not os.path.exists(sat): sat = os.path.join(ROOT, 'sources', 'sat172.json')
                subprocess.run([sys.executable, '-I', 'make_sources.py', sat, '.', 'wn=7,gcide=8,mw=9,mwt=10,moby=11,map=12,sqldoc=13,measured=14,guess=15'], cwd=os.path.join(ROOT, 'sources'), check=True)
                bottom5.RUNS.clear(); db = STATE['db'] = bottom5.open_brain()
                j.result = {'fresh': True}
            elif j.kind == 'q':
                cur = db.execute(j.args['sql'], j.args.get('params') or [])
                cols = [d[0] for d in cur.description] if cur.description else []
                j.result = {'cols': cols, 'rows': cur.fetchall()}
            else: raise ValueError('unknown job ' + j.kind)
        except Exception as e:
            j.error = str(e) or e.__class__.__name__
        j.finished = time.time(); STATE['busy'] = None; j.done.set()

threading.stack_size(1 << 30)
threading.Thread(target=brain_thread, daemon=True).start()
threading.stack_size(0)

def submit(kind, args, wait=None):
    j = Job(kind, args); JOBS.put(j)
    if wait is not None: j.done.wait(wait)
    return j
READONLY = ('SELECT', 'WITH', 'PRAGMA TABLE_INFO', 'PRAGMA DATABASE_LIST')

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
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); qs = urllib.parse.parse_qs(u.query)
        if u.path in ('/', '/index.html'):
            try: self.send(200, open(PAGE, 'rb').read(), 'text/html')
            except FileNotFoundError: self.send(404, {'error': 'page not found: ' + PAGE})
            return
        if u.path == '/api/info':
            import sqlite3
            return self.send(200, {'brain': bottom5.BRAIN, 'sixth': bottom5.SIXTH, 'sources': bottom5.SRC, 'sqlite': sqlite3.sqlite_version, 'started': STARTED, 'ready': READY.is_set() and STATE['db'] is not None, 'error': STATE['error'], 'busy': STATE['busy'].view() if STATE['busy'] else None, 'queued': JOBS.qsize()})
        if u.path == '/api/graph':
            if not READY.is_set() or STATE['error']: return self.send(503, {'error': STATE['error'] or 'the brain is still opening'})
            j = submit('graph', {'schema': qs.get('schema', ['main'])[0]}, wait=600)
            return self.send(200, j.result) if j.error is None and j.done.is_set() else self.send(500, {'error': j.error or 'timed out'})
        if u.path == '/api/lines':
            if not READY.is_set() or STATE['error']: return self.send(503, {'error': STATE['error'] or 'the brain is still opening'})
            j = submit('lines', {}, wait=600)
            return self.send(200, j.result) if j.error is None and j.done.is_set() else self.send(500, {'error': j.error or 'timed out'})
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
            j = submit('q', {'sql': sql, 'params': d.get('params') or []}, wait=600)
            return self.send(200, j.result) if j.error is None and j.done.is_set() else self.send(500, {'error': j.error or 'timed out'})
        self.send(404, {'error': 'no such path'})

if __name__ == '__main__':
    sys.setrecursionlimit(1000000)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H); srv.daemon_threads = True
    print('brain  ', bottom5.BRAIN); print('sixth  ', bottom5.SIXTH); print('sources', bottom5.SRC); print('page   ', PAGE); print('open    http://localhost:%d/' % PORT, flush=True)
    try: srv.serve_forever()
    except KeyboardInterrupt: pass
