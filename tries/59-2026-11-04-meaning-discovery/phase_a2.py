# tries/59 Phase A2: each grounded word's acting shards as (before, trigger) words with the call; the text of the main programs; the self-typing check
import json, sys; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1])
gates = set(r[0] for r in d.q('SELECT DISTINCT gate FROM belief')) | set(r[0] for r in d.q('SELECT DISTINCT gate FROM tried'))
for w in 'define print create change correct incorrect meaning type step true wrong why build describe alter write know remember shape seen merge read find move copy link split join select insert update delete store recall stamp append compare set measure fetch run'.split():
    g = d.gate(w)
    if g: gates.add(g)
acting = {}
for g in sorted(gates):
    rows = [r for r in d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g]) if r[3] or r[4]]
    if rows: acting[g] = rows
json.dump({g: rows for g, rows in acting.items()}, open('acting.json', 'w'))
print('== A1b. acting words with their shard keys (before > trigger) and calls')
for g in sorted(acting, key=lambda g: d.sym(g)):
    keys = ['%s>%s:%s%s' % (d.sym(r[1]), d.sym(r[2]), r[3] or '', ('/s' + str(r[4])) if r[4] else '') for r in acting[g]]
    print('  %-14s %7d  %s' % (d.sym(g), g, ' '.join(keys)[:220]))
def text(run, n):
    rows = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run])
    return (rows[0][0] if rows and rows[0][0] else '')[:n].replace('\n', ' ')
print('== A1c. what the main programs do (their text)')
for r in [826, 847, 870, 889, 910, 929, 950, 989, 1008, 1027, 1052, 1132, 19938846, 1302, 19937767, 19937779, 19937787, 19937222, 19942415, 6281755]:
    print('  run %s: %s' % (r, text(r, 700)))
    print()
print('== A4b. did the self-typed line define : rewrite run? rewrite 9728: nodes, sense_shard rows, about runs')
print('nodes', d.q('SELECT count(*) FROM node WHERE gate = 9728'), 'sense_shard', d.q('SELECT count(*) FROM sense_shard WHERE gate = 9728'), 'dna', d.q('SELECT shard, before, trigger, call FROM dna WHERE gate = 9728'))
try: print('about runs', d.q('SELECT id, arrival, kind, at FROM run WHERE about = 9728')[-5:])
except Exception as e: print('about read refused:', e)
