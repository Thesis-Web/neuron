#!/usr/bin/env python3
# serve18.py (2026-10-26): the new v18 core (../11-2026-10-25-new-v18-core, unchanged) behind a local HTTP door, so the
# Point Of Connection 18 page can type a line into the brain's input table and read the brain's tables back.
#
# The door does two things and nothing else:
#   - a typed line goes to host18.Brain.type(line, direction), which is INSERT INTO input; the brain's triggers do the rest,
#     exactly as at the native prompt (neuron_prompt18.py): same host, same SQLite, same 512 MB thread stack;
#   - a SELECT the page asks for is run and its rows sent back. Anything that is not a SELECT is refused here, so the only
#     way this door writes into the brain is a typed line.
# It decides nothing. The brain lives in memory, loaded from the .db file as neuron_prompt18.py loads it, and the file is
# never written unless you save from the page, to a path you name (it refuses to overwrite the file it loaded).
#
# usage: python3 serve18.py [brain.db] [port]
#   brain.db  default ../11-2026-10-25-new-v18-core/NEURON-v18-CORE-2026-10-25/brain18.db (the tested brain)
#             a path that does not exist lays the bare core into a new brain (then teach the four lines from the page)
#   port      default 8018
# then open http://localhost:8018/
import sys, os, json, time, threading, queue, http.server, urllib.parse, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.normpath(os.path.join(HERE, '..', '11-2026-10-25-new-v18-core', 'NEURON-v18-CORE-2026-10-25'))
PAGE = os.path.join(HERE, 'NEURON-POINT-OF-CONNECTION-v18-2026-10-26.html')
sys.path.insert(0, CORE)
from host18 import Brain   # v18's own bottom and mother, unchanged

DBFILE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(CORE, 'brain18.db')
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8018
sys.setrecursionlimit(200000)          # as neuron_prompt18.py
STARTED = time.time()

# ---- one thread owns the brain (SQLite connections are not shared across threads); every job runs there in order
JOBS = queue.Queue(); JOBMAP = {}; JOBLOCK = threading.Lock(); JOBN = [0]
READY = threading.Event(); STATE = {'brain': None, 'busy': None, 'error': None, 'loaded_from_file': os.path.exists(DBFILE)}

class Job:
    def __init__(self, kind, args):
        with JOBLOCK: JOBN[0] += 1; self.id = JOBN[0]; JOBMAP[self.id] = self
        self.kind, self.args, self.done, self.result, self.error = kind, args, threading.Event(), None, None
        self.created, self.started, self.finished, self.progress = time.time(), None, None, None
    def view(self):
        now = time.time()
        return {'id': self.id, 'kind': self.kind, 'done': self.done.is_set(), 'result': self.result, 'error': self.error,
                'started': self.started, 'elapsed': (self.finished or now) - (self.started or now) if self.started else None,
                'waited': (self.started or now) - self.created, 'progress': self.progress,
                'line': self.args.get('line') if isinstance(self.args, dict) else None}

def brain_thread():
    try:
        sat = json.load(open(os.path.join(CORE, 'sat172.json')))
        STATE['brain'] = Brain(os.path.join(CORE, 'physics18.json'), sat=sat, dbfile=DBFILE if os.path.exists(DBFILE) else None)
    except Exception as e:
        STATE['error'] = traceback.format_exc(); READY.set(); return
    READY.set()
    b = STATE['brain']
    while True:
        j = JOBS.get(); j.started = time.time(); STATE['busy'] = j
        try:
            if j.kind == 'type':
                t = time.time(); out = b.type(j.args['line'], j.args.get('direction') or 'heard')
                j.result = {'output': out, 'seconds': time.time() - t}
            elif j.kind == 'sheet':
                lines = json.load(open(os.path.join(CORE, 'sheet18.json'))); outs = []
                for k, (name, line) in enumerate(lines):
                    j.progress = {'k': k, 'of': len(lines), 'name': name}; t = time.time()
                    outs.append({'name': name, 'line': line[:120], 'output': b.type(line), 'seconds': time.time() - t})
                j.result = {'lines': outs}
            elif j.kind == 'q':
                cur = b.con.execute(j.args['sql'], j.args.get('params') or [])
                cols = [d[0] for d in cur.description] if cur.description else []
                j.result = {'cols': cols, 'rows': cur.fetchall()}
            elif j.kind == 'dna':
                since = int(j.args.get('since') or 0); dna = []; defs = []
                names = [r[0] for r in b.con.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name GLOB 'g[0-9]*'")]
                for n in names:
                    cols = [c[1] for c in b.con.execute('PRAGMA table_info(' + n + ')')]
                    g = int(n[1:])
                    if 'shard' in cols:
                        for r in b.con.execute('SELECT shard, arrival, remainder, trigger FROM ' + n + ' WHERE shard > ?', (since,)): dna.append((g,) + tuple(r))
                    elif 'score' in cols:
                        for r in b.con.execute('SELECT id, source, run, score FROM ' + n): defs.append((g,) + tuple(r))
                j.result = {'dna': dna, 'defs': defs, 'tables': len(names)}
            elif j.kind == 'save':
                p = os.path.abspath(j.args['path'])
                if os.path.exists(p) and os.path.exists(DBFILE) and os.path.samefile(p, DBFILE): raise ValueError('that is the file the brain was loaded from; name a new file')
                b.save(p); j.result = {'saved': p, 'bytes': os.path.getsize(p)}
            else: raise ValueError('unknown job ' + j.kind)
        except Exception as e:
            j.error = str(e) or e.__class__.__name__
        j.finished = time.time(); STATE['busy'] = None; j.done.set()

threading.stack_size(1 << 29)           # as neuron_prompt18.py: the born run nests 1,272 hops through mother
threading.Thread(target=brain_thread, daemon=True).start()
threading.stack_size(0)

def running_line():
    j = STATE['busy']; return j if j and j.kind in ('type', 'sheet') else None   # a read waiting its turn is not "busy"

def submit(kind, args, wait=None):
    j = Job(kind, args); JOBS.put(j)
    if wait is not None: j.done.wait(wait)
    return j

READONLY = ('SELECT', 'WITH', 'EXPLAIN', 'PRAGMA TABLE_INFO', 'PRAGMA INDEX_LIST', 'PRAGMA INDEX_INFO')

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *a): pass
    def send(self, code, obj, ctype='application/json'):
        body = obj if isinstance(obj, bytes) else json.dumps(obj, default=str).encode()
        self.send_response(code); self.send_header('Content-Type', ctype + ('; charset=utf-8' if not isinstance(obj, bytes) or ctype.startswith('text') else ''))
        self.send_header('Content-Length', str(len(body))); self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(body)
    def do_OPTIONS(self):
        self.send_response(204); self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Access-Control-Allow-Headers', 'content-type'); self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'); self.end_headers()
    def body(self):
        n = int(self.headers.get('Content-Length') or 0); return json.loads(self.rfile.read(n) or b'{}')
    def info(self):
        import sqlite3, platform
        told = json.load(open(os.path.join(CORE, 'physics18.json')))
        return {'brain': DBFILE, 'loaded_from_file': STATE['loaded_from_file'], 'core': CORE, 'page': PAGE, 'sqlite': sqlite3.sqlite_version, 'python': platform.python_version(),
                'sats': told['sats'], 'handlaid': told['handlaid'], 'statements': len(told['statements']), 'started': STARTED, 'ready': READY.is_set() and STATE['brain'] is not None, 'error': STATE['error'],
                'busy': running_line().view() if running_line() else None, 'queued': JOBS.qsize()}
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); qs = urllib.parse.parse_qs(u.query)
        if u.path in ('/', '/index.html'):
            try: self.send(200, open(PAGE, 'rb').read(), 'text/html')
            except FileNotFoundError: self.send(404, {'error': 'page not found: ' + PAGE})
            return
        if u.path == '/api/info': return self.send(200, self.info())
        if u.path == '/api/job':
            j = JOBMAP.get(int(qs.get('id', ['0'])[0]))
            return self.send(200, j.view()) if j else self.send(404, {'error': 'no such job'})
        if u.path == '/api/dna':
            if not READY.is_set() or STATE['error']: return self.send(503, {'error': STATE['error'] or 'the brain is still loading'})
            if running_line(): return self.send(503, {'error': 'the brain is running a line', 'busy': running_line().view()})
            j = submit('dna', {'since': qs.get('since', ['0'])[0]}, wait=600)
            return self.send(200, j.result) if j.error is None and j.done.is_set() else self.send(500, {'error': j.error or 'timed out'})
        self.send(404, {'error': 'no such path'})
    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        try: d = self.body()
        except Exception as e: return self.send(400, {'error': 'bad json: ' + str(e)})
        if not READY.is_set() or STATE['error']: return self.send(503, {'error': STATE['error'] or 'the brain is still loading'})
        if u.path == '/api/type':
            line = str(d.get('line') or '').strip()
            if not line: return self.send(400, {'error': 'an empty line'})
            j = submit('type', {'line': line, 'direction': d.get('direction') or 'heard'}); return self.send(200, j.view())
        if u.path == '/api/sheet':
            j = submit('sheet', {}); return self.send(200, j.view())
        if running_line(): return self.send(503, {'error': 'the brain is running a line', 'busy': running_line().view()})
        if u.path == '/api/q':
            sql = str(d.get('sql') or '').strip()
            if not sql.upper().startswith(READONLY): return self.send(400, {'error': 'only a SELECT is read through this door; a line is typed through /api/type'})
            j = submit('q', {'sql': sql, 'params': d.get('params') or []}, wait=600)
            return self.send(200, j.result) if j.error is None and j.done.is_set() else self.send(500, {'error': j.error or 'timed out'})
        if u.path == '/api/save':
            path = str(d.get('path') or '').strip() or os.path.join(HERE, time.strftime('brain18-%Y-%m-%d-%H%M%S.db'))
            if not os.path.isabs(path): path = os.path.join(HERE, path)
            j = submit('save', {'path': path}, wait=600)
            return self.send(200, j.result) if j.error is None and j.done.is_set() else self.send(500, {'error': j.error or 'timed out'})
        self.send(404, {'error': 'no such path'})

if __name__ == '__main__':
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H); srv.daemon_threads = True
    print('core   ', CORE); print('brain  ', DBFILE, '(exists)' if os.path.exists(DBFILE) else '(new: the bare core is laid)'); print('page   ', PAGE)
    print('open    http://localhost:%d/' % PORT, flush=True)
    try: srv.serve_forever()
    except KeyboardInterrupt: pass
