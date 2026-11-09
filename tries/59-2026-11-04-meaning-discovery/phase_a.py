# tries/59 Phase A: the actual starting state of the test brain (door 8059), by keyed reads; one write at the end: can the brain type a line into itself?
import json, sys, sqlite3; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1])
print('== A1. the grounded operations: points whose dna rows carry a call or spawn (belief + tried gates + the taught set), and what each call run is')
gates = set(r[0] for r in d.q('SELECT DISTINCT gate FROM belief')) | set(r[0] for r in d.q('SELECT DISTINCT gate FROM tried'))
for w in 'define print create change correct incorrect meaning type step true wrong why build describe alter write know remember shape seen merge'.split():
    g = d.gate(w)
    if g: gates.add(g)
acting = {}
for g in sorted(gates):
    rows = [r for r in d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g]) if r[3] or r[4]]
    if rows: acting[g] = rows
print('points with an acting row:', len(acting), 'of', len(gates), 'read')
calls = {}
for g, rows in acting.items():
    for r in rows:
        for c in (r[3], r[4]):
            if c: calls.setdefault(c, []).append((d.sym(g), r[1], r[2]))
print('distinct call/spawn runs:', len(calls))
def text(run, n=150):
    rows = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run])
    t = rows[0][0] if rows and rows[0][0] else ''
    return t[:n].replace('\n', ' ')
for c in sorted(calls):
    users = calls[c]; names = sorted(set(u[0] for u in users))
    print('  run %-9s used by %2d rows of %s: %s' % (c, len(users), ' '.join(names[:12]) + (' ...' if len(names) > 12 else ''), text(c)))
print('== A2. the relationship kinds (relmap, pull) and a sample point rel rows')
print('relmap:', d.q('SELECT marker, kind FROM relmap ORDER BY kind')[:40])
print('pull kinds:', d.q('SELECT kind, formula FROM pull ORDER BY kind')[:40])
g = d.gate('rewrite'); print('rewrite gate', g, 'nodes', d.q('SELECT count(*) FROM node WHERE gate = ?', [g]), 'dna', d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g]), 'rel', d.q('SELECT kind, other FROM rel WHERE gate = ?', [g])[:12])
print('== A3. the sense rows of a defined point are node rows from source 7 (wn) and 443 (wikt): how many points hold sense shards (sense_shard table)')
print('sense_shard rows:', d.q('SELECT count(*), count(DISTINCT gate) FROM sense_shard'))
print('== A4. the self-typing facility: a span that inserts into input types a line into the brain')
before = d.q('SELECT n FROM clock')[0][0]
r = d.typed("BUILD INSERT INTO input ( text ) VALUES ( 'define : rewrite' ) ; BUILD", quiet=True)
rep = d.sheet(r['run']).get(22); print('the typing line run', r['run'], 'reply:', rep[1].get('text') if rep and isinstance(rep[1], dict) else rep)
newest = d.q('SELECT id, text, run FROM input WHERE id > ( SELECT max ( id ) - 3 FROM input )')
print('newest input rows (id, text, run):', newest)
