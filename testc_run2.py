# tries/59 Test C, second pass after the per-sense statements were re-formed: derive : assume again (the sense shards hold no call yet), then three
# new lines in the same contexts (a repeated line is a memory hop and never hops again, so the words differ). EXPECTED, written first: the shard
# keyed (gods, human) takes form -> 929 and the line "The gods assume human form" runs 929 under it; the shard (I, his) takes true -> 19937779 and
# "I assume his car was late" runs 19937779; "they assume nothing" lands on no sense shard and runs nothing but the heard row.
import sys; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1]); w = 'assume'; g = d.gate(w)
def reply(run):
    c = d.sheet(run).get(22); return c[1].get('text') if c and isinstance(c[1], dict) else c
r = d.typed('derive : ' + w, quiet=True); print('derive run', r['run'], 'hits', r.get('hits'), 'reply of the derive run:', [str(reply(k[0]))[:80] for k in d.q('SELECT id, kind, replay_src FROM run WHERE parent = ?', [r['run']])])
print('derived rows (shard, ord, word, run_used, sense_run):', d.q('SELECT shard, ord, word, run_used, sense_run FROM derived WHERE gate = ? AND run > ? ORDER BY id', [g, r['run'] - 50]))
print('dna after derive:', d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g]))
for line in ['The gods assume human form', 'I assume his car was late', 'they assume nothing']:
    r = d.typed(line, quiet=True); rc = [x for x in d.q('SELECT pos, gate, shard FROM run_receipt WHERE run = ?', [r['run']]) if x[1] == g]
    kids = d.q('SELECT id, kind, replay_src FROM run WHERE parent = ?', [r['run']])
    print('typed %r run %s hits %s: the hit on assume %s; kids %s' % (line, r['run'], r.get('hits'), rc, kids))
    for k in kids: print('      kid', k, 'reply:', str(reply(k[0]))[:140])
