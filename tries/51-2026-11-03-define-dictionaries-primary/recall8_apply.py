# recall8_apply.py (tries/51): types the lines of RECALL-8-nk.txt through the kernel door, one at a time, filling {run:N} with the run of the
# N-th line typed here and {gate:X} with the gate of the symbol X, and reads every mother reply. Modes:
#   check <door> <file>            types part 0 (the ranks) only, then runs the pick read for the words given and prints what it picks
#   apply <door> <file>            types parts 1, 2, 3 (the ask, the define run, the binds) and prints each run and its refused count
#   define <door> <word> ...       types define : word for each and prints the def cell's run, its source and text
import json, sys, urllib.request
door = sys.argv[2]
def post(path, body):
    r = urllib.request.Request(door + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=600))
def q(sql, params=()): return post('/api/q', {'sql': sql, 'params': list(params)})
def gate(sym):
    r = q('SELECT gate FROM label WHERE symbol = ?', [sym]); rows = r.get('rows') or []
    if not rows: raise SystemExit('no gate for ' + sym)
    return rows[0][0]
def run_of(rid): return json.load(urllib.request.urlopen(door + '/api/run?schema=main&id=%d' % rid, timeout=120))
RUNS = []
def typed(line):
    j = post('/api/type', {'line': line}); r = j.get('result') or {}
    RUNS.append(r.get('run')); print('typed: run %s, %s runs, %s hits, %s born, %s refused, %.3f s, %s' % (r.get('run'), r.get('runs'), r.get('hits'), r.get('born'), r.get('refused'), r.get('seconds') or 0, (j.get('error') or '')[:100]))
    if r.get('refused'): print('  REFUSED; the line stops here'); sys.exit(2)
    return r.get('run')
def fill(line):
    import re
    line = re.sub(r'\{gate:([a-z]+)\}', lambda m: str(gate(m.group(1))), line)
    line = re.sub(r'\{run:(\d+)\}', lambda m: str(RUNS[int(m.group(1)) - 1]), line)
    return line
def parts(path):
    out = []
    for l in open(path, encoding='utf-8'):
        l = l.rstrip('\n')
        if l.startswith('BUILD'): out.append(l)
    return out
def pick_sql(g):
    return ("SELECT n.run, n.source FROM node n LEFT JOIN ranks p ON p.cell = 24 AND p.source = n.source WHERE n.gate = ? ORDER BY coalesce ( p.rank , 9 ) , "
            "CASE WHEN EXISTS ( SELECT 1 FROM seq s WHERE s.run = n.run AND s.gate = %d ) OR ( SELECT gate FROM seq WHERE run = n.run ORDER BY pos LIMIT 1 ) <> 143 THEN 0 ELSE 1 END , n.run LIMIT 1" % g)
mode = sys.argv[1]
names = {7: 'wn', 8: 'gcide', 10: 'mwt', 11: 'moby', 12: 'map', 13: 'sqldoc', 14: 'measured', 15: 'guess', 443: 'wikt'}
if mode in ('check', 'pick'):
    P = parts(sys.argv[3])
    if mode == 'check': typed(P[0])   # part 0: the ranks
    print('ranks rows:', q('SELECT cell, source, rank FROM ranks ORDER BY cell, rank, source').get('rows'))
    gdef = gate('definition'); print('gate of definition:', gdef)
    for w in sys.argv[4:]:
        g = gate(w); r = q(pick_sql(gdef), [g]); rows = r.get('rows') or []
        if r.get('error'): print(w, 'read error:', r['error']); continue
        if not rows: print(w, g, 'no node row'); continue
        rid, src = rows[0]; t = (run_of(rid)['run'].get('text') or '')[:140]
        print('%-6s gate %6d picks run %7d from %-6s: %s' % (w, g, rid, names.get(src, src), t))
elif mode == 'apply':
    P = parts(sys.argv[3]); RUNS.append(None)   # part 0 was typed by check; {run:2} is part 1, {run:3} is part 2
    for p in P[1:]: typed(fill(p))
    print('define rows now:', q('SELECT shard, before, trigger, call FROM dna WHERE gate = ? AND trigger = 68', [gate('define')]).get('rows'))
elif mode == 'define':
    for w in sys.argv[3:]:
        rid = typed('define : ' + w); x = run_of(rid); cells = {c[0]: c for c in x.get('cells') or []}
        c = cells.get(24)
        if not c or not c[2]: print('  %s: no def cell' % w); continue
        d = run_of(int(c[2]))['run']; print('  %-6s def = run %s from %s: %s' % (w, c[2], names.get(d.get('arrival'), d.get('arrival')), (d.get('text') or '')[:150]))
