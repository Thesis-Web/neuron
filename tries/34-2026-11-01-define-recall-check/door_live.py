#!/usr/bin/env python3
# g34/door_live.py (2026-11-01, 17:45). The page replays a history of receipts and asks for every receipt after the last id it saw. The door
# served that from its bundle, which is rebuilt every 600 s and after a typed line, with ids numbered from 1 each time: a line typed through
# the page never reached its history (measured: hits 56,616 before and after, the line itself 0.01 s at the kernel, the page 298 s). Now the
# history the door serves is the first bundle's receipts and then every line typed through this door, read from the kernel's own run record
# (its runs, receipts, symbols, out rows) and appended with ids that never go back. The bundle keeps its 600 s; a typed line no longer drops it.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34/hp/serve8.py'
s = open(P, encoding='utf-8').read()
pairs = [
    ("def bundle():\n    if BUNDLE['d'] is None or time.time() - BUNDLE['at'] > 600: BUNDLE['d'] = ask('bundle ' + os.environ.get('NK_BUNDLE_K', '2000')); BUNDLE['at'] = time.time()\n    return BUNDLE['d']\n",
     "LIVE = {'base': None, 'rc': [], 'runs': [], 'inputs': [], 'out': [], 'first': {}, 'label': [], 'seen': set(), 'gates': set(), 'next': 1, 'n': 0}\n"
     "def bundle():\n"
     "    if BUNDLE['d'] is None or time.time() - BUNDLE['at'] > 600:\n"
     "        BUNDLE['d'] = ask('bundle ' + os.environ.get('NK_BUNDLE_K', '2000')); BUNDLE['at'] = time.time()\n"
     "        if LIVE['base'] is None:   # the history the page replays: the first bundle's receipts, then every line typed through this door, appended; ids never go back\n"
     "            LIVE['base'] = BUNDLE['d']['receipts']; LIVE['next'] = (LIVE['base'][-1][0] if LIVE['base'] else 0) + 1\n"
     "            LIVE['seen'] = set(r[1] for r in LIVE['base']); LIVE['gates'] = set(l[0] for l in BUNDLE['d']['label'])\n"
     "    return BUNDLE['d']\n"
     "def live_add(r):\n"
     "    \"\"\"a line typed through this door: its runs, receipts, symbols and out rows, read from the kernel's run record, appended after the history served so far\"\"\"\n"
     "    if r.get('schema') != 'main' or not r.get('run'): return\n"
     "    bundle(); x = ask('run main %d' % r['run'])\n"
     "    if 'hops' not in x: return\n"
     "    root = (x.get('run') or {}).get('root') or r['run']\n"
     "    for t in x.get('tree', []):\n"
     "        if t['id'] in LIVE['seen']: continue\n"
     "        LIVE['seen'].add(t['id']); LIVE['runs'].append([t['id'], t['arrival'], t.get('parent'), root, t['kind'], t.get('cell') or None, t.get('about') or None, t['id']])\n"
     "    for h in x['hops']:\n"
     "        if h[1] == 0 and h[0] not in LIVE['first']: LIVE['first'][h[0]] = h[2]\n"
     "        LIVE['rc'].append([LIVE['next'], h[0], h[2], h[3]]); LIVE['next'] += 1\n"
     "    for g, v in (x.get('gates') or {}).items():\n"
     "        g = int(g)\n"
     "        if g not in LIVE['gates']: LIVE['gates'].add(g); LIVE['label'].append([g, v.get('s')])\n"
     "    LIVE['n'] += 1; LIVE['inputs'].append(['main', LIVE['n'], r['run']])\n"
     "    for o in r.get('out', []):\n"
     "        if o[0] == 'main': LIVE['out'].append([LIVE['next'], o[1], o[2], o[3]]); LIVE['next'] += 1\n"),
    ("    if s.startswith('SELECT gate, symbol FROM main.label'): return {'cols': ['gate', 'symbol'], 'rows': d['label']}\n"
     "    if s.startswith('SELECT id, arrival, parent, root, kind, cell, about, at FROM main.run'): return {'cols': [], 'rows': [r[:8] for r in d['runs']]}\n"
     "    if s.startswith(\"SELECT 'main', id, run FROM main.input\"): return {'cols': [], 'rows': d['inputs']}\n"
     "    if s.startswith('SELECT id, run, cell, value FROM main.out_user'): return {'cols': [], 'rows': d['out']}\n",
     "    if s.startswith('SELECT gate, symbol FROM main.label'): return {'cols': ['gate', 'symbol'], 'rows': d['label'] + LIVE['label']}\n"
     "    if s.startswith('SELECT id, arrival, parent, root, kind, cell, about, at FROM main.run'):\n"
     "        bs = set(r[0] for r in d['runs']); return {'cols': [], 'rows': [r[:8] for r in d['runs']] + [r for r in LIVE['runs'] if r[0] not in bs]}\n"
     "    if s.startswith(\"SELECT 'main', id, run FROM main.input\"): return {'cols': [], 'rows': d['inputs'] + LIVE['inputs']}\n"
     "    if s.startswith('SELECT id, run, cell, value FROM main.out_user'): return {'cols': [], 'rows': d['out'] + LIVE['out']}\n"),
    ("        last = int(params[0]) if params else 0; return {'cols': [], 'rows': [r for r in d['receipts'] if r[0] > last]}\n",
     "        last = int(params[0]) if params else 0; return {'cols': [], 'rows': [r for r in (LIVE['base'] if LIVE['base'] is not None else d['receipts']) if r[0] > last] + [r for r in LIVE['rc'] if r[0] > last]}\n"),
    ("'mem': d['mem'], 'first': d['first'], 'T': d['T'],",
     "'mem': d['mem'], 'first': dict(d['first'], **{str(k): v for k, v in LIVE['first'].items()}), 'T': d['T'],"),
    ("RUNS.append(r.get('run')); BUNDLE['d'] = None   # the page reads the brain again after its line: it must see this run\n",
     "RUNS.append(r.get('run')); live_add(r)   # the page reads the brain again after its line: this run, its receipts and symbols are appended to what it reads\n"),
]
for old, new in pairs:
    assert s.count(old) == 1, (s.count(old), old[:100])
    s = s.replace(old, new)
open(P, 'w', encoding='utf-8').write(s); print('patched', P, len(pairs))
