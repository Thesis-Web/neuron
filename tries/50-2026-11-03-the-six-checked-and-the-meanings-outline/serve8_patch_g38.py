# serve8_patch_g38.py (tries/50, 2026-11-03): the kernel door's open set by key, never the whole-brain bundle.
# The owner, 20:10: "I hate signing off on things that are potentially built wrong, so double and triple check c9,c10,c11,c12,c15,c16".
# Found: the page's open made three reads (input, out_user, the counts) and its history read that the door answered from the whole-brain
# bundle (bundle K in C: a walk of every neuron's shards and the whole rel table, 1.3 to 1.9 s on the kernel, 37 to 43 MB of JSON, the door at
# 550 to 660 MB), rebuilt on a read whenever older than 600 s. Now: the open set is the newest K lines and every run under them, read by key
# (newest, run per root, run_memory by run), the out rows of a line its root's sheet cells (the owner, 10-26: output to the user comes from the
# same memory table), the counts from stats; refreshed only when the kernel's run count grew, never on a clock; bundle() only for /api/graph.
import sys, re
src = open(sys.argv[1], encoding='utf-8').read(); out = sys.argv[2]
def sub(old, new, count=1):
    global src
    assert src.count(old) == count, (old[:80], src.count(old))
    src = src.replace(old, new)
# 1. bundle() no longer seeds the page's history
sub("""        if LIVE['base'] is None:   # the history the page replays: the first bundle's receipts, then every line typed through this door, appended; ids never go back
            LIVE['base'] = BUNDLE['d']['receipts']; LIVE['next'] = (LIVE['base'][-1][0] if LIVE['base'] else 0) + 1
            LIVE['seen'] = set(r[1] for r in LIVE['base']); LIVE['gates'] = set(l[0] for l in BUNDLE['d']['label'])
""", "")
# 2. a typed line is appended to the open set whether or not the old whole-brain page ever asked for the bundle; its memory row read by key
sub("""    if BUNDLE['d'] is None: return   # tries/44: no whole-brain snapshot is built for a typed line; the bundle exists only if the old whole-brain page asked for it
    x = ask('run main %d' % r['run'])""", """    open_set()   # tries/50: the open set exists without the bundle
    x = ask('run main %d' % r['run'])""")
sub("""    LIVE['n'] += 1; LIVE['inputs'].append(['main', LIVE['n'], r['run']])
    for o in r.get('out', []):
        if o[0] == 'main': LIVE['out'].append([LIVE['next'], o[1], o[2], o[3]]); LIVE['next'] += 1
""", """    LIVE['n'] += 1; LIVE['inputs'].append(['main', LIVE['n'], r['run']])
    for o in r.get('out', []):
        if o[0] == 'main': LIVE['out'].append([LIVE['next'], o[1], o[2], o[3]]); LIVE['next'] += 1
    for m in (q('SELECT run, gate, shard, input FROM main.run_memory WHERE run = ?', [root]) or {}).get('rows') or []: LIVE['memrows'].append(m)   # the root's memory row, by key
OPEN_K = int(os.environ.get('NK_OPEN_K', '400')); OPEN_LOCK = threading.Lock(); OPEN = {'runs_at': -1, 'built': 0, 'adds': 0, 'rel': None}
def open_set():
    \"\"\"tries/50: the page's open set, the newest K lines of the main brain (typed and told) and every run under them, read by key: newest, run per root,
    run_memory by run. No whole-brain bundle. Refreshed only when the kernel's run count grew since the last read (the brain changed), never on a clock.\"\"\"
    st = (ask('stats').get('main') or {}); runs = st.get('runs') or 0
    if LIVE['base'] is not None and runs == OPEN['runs_at']: return
    with OPEN_LOCK:
        if LIVE['base'] is not None and runs == OPEN['runs_at']: return
        if LIVE['base'] is None:
            LIVE['base'] = []; LIVE['next'] = (st.get('receipts') or 0) + 1   # ids after every receipt the kernel holds, so the ids only go forward
            n = ask('newest main %d' % OPEN_K); OPEN['built'] += 1
            lines = [('main', l) for l in n.get('lines', [])] + [('sixth', l) for l in n.get('told', [])]
        else:
            n = ask('newest main 50'); lines = [('main', l) for l in n.get('lines', [])] + [('sixth', l) for l in n.get('told', [])]
        lines = [(who, l) for who, l in lines if l.get('run') and l['run'] not in LIVE['seen']]
        lines.sort(key=lambda wl: wl[1]['run'])   # oldest first: the history replays in the order it happened
        for who, l in lines: open_add(who, l['id'], l['run'])
        OPEN['runs_at'] = runs
def open_add(who, mail_id, run):
    x = ask('run main %d' % run)
    if 'hops' not in x: return
    root = (x.get('run') or {}).get('root') or run; OPEN['adds'] += 1
    for t in x.get('tree', []):
        if t['id'] in LIVE['seen']: continue
        LIVE['seen'].add(t['id']); LIVE['runs'].append([t['id'], t['arrival'], t.get('parent'), root, t['kind'], t.get('cell') or None, t.get('about') or None, t['id']])
    for h in x['hops']:
        if h[1] == 0 and h[0] not in LIVE['first']: LIVE['first'][h[0]] = h[2]
        LIVE['rc'].append([LIVE['next'], h[0], h[2], h[3]]); LIVE['next'] += 1
    for g, v in (x.get('gates') or {}).items():
        g = int(g)
        if g not in LIVE['gates']: LIVE['gates'].add(g); LIVE['label'].append([g, v.get('s')])
    LIVE['inputs'].append([who, mail_id, run])
    for c in x.get('cells') or []:   # the line's output: its root's sheet cells with a value (the owner, 10-26: output to the user comes from the same memory table)
        if c[1] == 1 and c[2] is not None: LIVE['out'].append([LIVE['next'], root, c[0], c[2]]); LIVE['next'] += 1
    for m in (q('SELECT run, gate, shard, input FROM main.run_memory WHERE run = ?', [root]) or {}).get('rows') or []: LIVE['memrows'].append(m)
""")
# 3. the page's open reads answered from the open set; bundle() only for the old whole-brain page's reads
sub("""    s = sql.strip()
    if not s.startswith(BUNDLE_PREFIXES): return None
    d = bundle()
""", """    s = sql.strip()
    if not s.startswith(BUNDLE_PREFIXES): return None
    if s.startswith(("SELECT 'main', id, run FROM main.input", 'SELECT id, run, cell, value FROM main.out_user', 'SELECT (SELECT count(*) FROM main.label)', 'SELECT run, gate, shard, input FROM main.run_memory', 'SELECT m.run, m.gate, m.shard, m.input FROM main.run_memory m JOIN main.run r', 'SELECT id, run, gate, shard FROM main.run_receipt WHERE id > ?')):
        open_set()   # tries/50: by key, never the whole brain
        if s.startswith("SELECT 'main', id, run FROM main.input"): return {'cols': [], 'rows': list(LIVE['inputs'])}
        if s.startswith('SELECT id, run, cell, value FROM main.out_user'): return {'cols': [], 'rows': list(LIVE['out'])}
        if s.startswith('SELECT (SELECT count(*) FROM main.label)'):
            st = ask('stats'); m = st['main']; x = st['sixth']
            if OPEN['rel'] is None: OPEN['rel'] = ((q('SELECT count(*) FROM main.rel') or {}).get('rows') or [[0]])[0][0]   # once per door: a count over the brain's own rel table
            return {'cols': [], 'rows': [[m['gates'], m['defined'], 0, m['shard_rows'], m['runs'], m['receipts'], 0, 0, 0, m['refused'], m['pending'], 0, 0, OPEN['rel'], 0, x['runs'], 0, x['refused'], m['returns']]]}
        if s.startswith('SELECT run, gate, shard, input FROM main.run_memory'): return {'cols': [], 'rows': list(LIVE['memrows'])}
        if s.startswith('SELECT m.run, m.gate, m.shard, m.input FROM main.run_memory m JOIN main.run r'):
            root = int(params[0]) if params else 0; roots = {r[0]: r[3] for r in LIVE['runs']}; return {'cols': [], 'rows': [m for m in LIVE['memrows'] if m[0] == root or roots.get(m[0]) == root]}
        last = int(params[0]) if params else 0; return {'cols': [], 'rows': [r for r in LIVE['rc'] if r[0] > last]}
    if s.startswith('SELECT p.kind, f.pull, f.rest, f.dx, f.dy, f.dz, f.mode FROM main.pull p'): return None   # the brain's own formula and pull tables answer by themselves (38 rows)
    d = bundle()
""")
# 4. /api/info tells the open set's state so a check can read it
sub("""                st = ask('stats'); return self.send(200, {'brain': 'nk main', 'sixth': 'nk sixth', 'sources': 'attached', 'sqlite': 'nk', 'started': STARTED, 'ready': True, 'error': None, 'busy': None, 'queued': 0, 'version': 'nk', 'stats': st})""",
    """                st = ask('stats'); return self.send(200, {'brain': 'nk main', 'sixth': 'nk sixth', 'sources': 'attached', 'sqlite': 'nk', 'started': STARTED, 'ready': True, 'error': None, 'busy': None, 'queued': 0, 'version': 'nk', 'stats': st, 'open': {'k': OPEN_K, 'built': OPEN['built'], 'roots': OPEN['adds'], 'receipts': len(LIVE['rc']), 'inputs': len(LIVE['inputs']), 'memrows': len(LIVE['memrows']), 'bundle_held': BUNDLE['d'] is not None}})""")
assert 'LIVE[\'memrows\']' in src
open(out, 'w', encoding='utf-8').write(src); print('patched', out, len(src), 'bytes')
# 5. the open set's memory rows live beside the receipts; a typed line already laid by the open set is not laid twice; the open set is read at the door's start
src = open(out, encoding='utf-8').read()
sub("""LIVE = {'base': None, 'rc': [], 'runs': [], 'inputs': [], 'out': [], 'first': {}, 'label': [], 'seen': set(), 'gates': set(), 'next': 1, 'n': 0}""",
    """LIVE = {'base': None, 'rc': [], 'runs': [], 'inputs': [], 'out': [], 'first': {}, 'label': [], 'seen': set(), 'gates': set(), 'next': 1, 'n': 0, 'memrows': []}""")
sub("""    open_set()   # tries/50: the open set exists without the bundle
    x = ask('run main %d' % r['run'])""", """    open_set()   # tries/50: the open set exists without the bundle; a typed line the open set already laid (the run count grew) is not laid twice
    if r['run'] in LIVE['seen']: return
    x = ask('run main %d' % r['run'])""")
sub("""    srv = http.server.ThreadingHTTPServer((BIND, PORT), H); srv.daemon_threads = True""",
    """    srv = http.server.ThreadingHTTPServer((BIND, PORT), H); srv.daemon_threads = True
    threading.Thread(target=open_set, daemon=True).start()   # tries/50: the open set read by key at the door's start, so the first page open does not wait on it""")
open(out, 'w', encoding='utf-8').write(src); print('patched again', out, len(src), 'bytes')
