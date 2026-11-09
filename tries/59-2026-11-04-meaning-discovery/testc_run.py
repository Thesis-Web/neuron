# tries/59 Test C (context discrimination) on the word the finder gave (assume): define lays its sense shards from the examples' contexts;
# derive fills each sense shard from its own sense's gloss (H1a); three lines typed: two in example contexts, one in a context no example holds.
# EXPECTED, written before any line (from testc-find2-hp.txt): sense 3 (form -> 929, create's run) on the shard keyed by "The gods assume human",
# sense 1 (true -> 19937779, correct's run) on the shard keyed by "I assume his"; "we assume nothing" lands on no sense shard and calls nothing.
import sys; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1]); w = 'assume'; g = d.gate(w)
def text(run, n=90):
    rows = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run]); return (rows[0][0] if rows and rows[0][0] else '')[:n]
def reply(run):
    c = d.sheet(run).get(22); return c[1].get('text') if c and isinstance(c[1], dict) else c
print('== assume gate', g, 'dna before:', d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g]))
r = d.typed('define : ' + w, quiet=True); print('define run', r['run'], 'hits', r.get('hits'))
ss = d.q('SELECT shard, run FROM sense_shard WHERE gate = ? ORDER BY shard, run', [g]); print('sense_shard rows:', len(ss))
for s, run in ss:
    row = d.q('SELECT before, trigger FROM dna WHERE gate = ? AND shard = ?', [g, s]); print('   shard %s key (%s, %s) sense %s: %s' % (s, d.sym(row[0][0]) if row else '?', d.sym(row[0][1]) if row else '?', run, text(run)))
r = d.typed('derive : ' + w, quiet=True); print('derive run', r['run'], 'hits', r.get('hits'))
print('derived rows (shard, ord, word, run_used, sense_run):', d.q('SELECT shard, ord, word, run_used, sense_run FROM derived WHERE gate = ? ORDER BY id', [g]))
print('dna after derive:', d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g]))
for line in ['The gods assume human or animal form in these fables', 'I assume his train was late', 'we assume nothing']:
    r = d.typed(line, quiet=True); rc = [x for x in d.q('SELECT pos, gate, shard FROM run_receipt WHERE run = ?', [r['run']]) if x[1] == g]
    kids = d.q('SELECT id, kind, replay_src FROM run WHERE parent = ?', [r['run']])
    print('typed %r run %s hits %s: the hit on assume %s; kids %s' % (line, r['run'], r.get('hits'), rc, kids))
    for k in kids: print('      kid', k, 'reply:', str(reply(k[0]))[:140])
print('dna at the end:', d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g]))
