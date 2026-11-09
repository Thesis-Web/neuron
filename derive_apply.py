# tries/59 derive_apply.py: type DERIVE-nk.txt (mode lay), then the experiment (mode run): for each candidate, the expected written first,
# derive : X typed, the derived rows and the shard read; then X : who typed and its receipts and kids read; a negative control; Test C on a two-sense word.
import json, re, sqlite3, sys; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1]); mode = sys.argv[2]
def reply(run):
    c = d.sheet(run).get(22); return c[1].get('text') if c and isinstance(c[1], dict) else c
def say(run):
    c = d.sheet(run).get(25); return (c[1].get('text') if c and isinstance(c[1], dict) else c)
if mode == 'lay':
    runs = []
    for l in open('DERIVE-nk.txt'):
        if not l.startswith('BUILD'): continue
        t = d.resolve(l.rstrip('\n'), runs); r = d.typed(t, quiet=True); runs.append(r['run'])
        print('run', r['run'], 'refused', r.get('refused'), 'reply:', str(reply(r['run']))[:100])
    json.dump(runs, open('derive_runs.json', 'w'))
if mode == 'run':
    believed = {}
    for g, in d.q('SELECT DISTINCT gate FROM belief WHERE correct > 0'):
        rows = d.q('SELECT d.call FROM belief b JOIN dna d ON d.gate = b.gate AND d.shard = b.shard WHERE b.gate = ? AND b.correct > 0 AND d.call IS NOT NULL ORDER BY b.correct DESC, b.shard LIMIT 1', [g])
        if rows: believed[g] = rows[0][0]
    print('believed points (belief correct > 0 with a call):', len(believed))
    def text(run):
        rows = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run]); return rows[0][0] if rows and rows[0][0] else ''
    def expected(word):
        # the expected, written before the brain runs, by the stated rule: the first WordNet verb sense by node id; its gloss's believed points in order
        g = d.gate(word)
        for gate, nid, src, run in d.q('SELECT gate, id, source, run FROM node WHERE gate = ? ORDER BY id', [g]):
            if src != 7: continue
            t = text(run)
            m = re.match(r'verb (\d+): (.*)', t)
            if not m: continue
            gloss = re.split(r' \[|; "', m.group(2))[0]; words = re.findall(r"[a-z]+", gloss.lower())
            gr = [(x, d.gate(x)) for x in words if d.gate(x) and d.gate(x) != g and d.gate(x) in believed]
            return gloss, [(x, gg, believed[gg]) for x, gg in gr]
        return None, []
    results = {}
    for word in sys.argv[3:]:
        g = d.gate(word); print('==', word, 'gate', g, 'dna before:', d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g]))
        gloss, exp = expected(word); print('   EXPECTED (written first): gloss %r -> %s -> call %s spawn %s' % (gloss, [e[0] for e in exp], exp[0][2] if exp else None, exp[1][2] if len(exp) > 1 else None))
        r = d.typed('derive : ' + word, quiet=True); print('   derive run', r['run'], 'hits', r.get('hits'), 'say:', str(say(r['run']))[:300])
        rows = d.q('SELECT shard, ord, word, run_used, sense_run FROM derived WHERE gate = ? ORDER BY id', [g]); print('   derived rows:', rows)
        dna = d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g]); print('   dna after:', dna)
        line = word + ' : who'; r2 = d.typed(line, quiet=True)
        kids = d.q('SELECT id, kind, replay_src FROM run WHERE parent = ?', [r2['run']]); rc = d.q('SELECT pos, gate, shard FROM run_receipt WHERE run = ?', [r2['run']])
        print('   typed %r run %s hits %s receipts %s kids %s say: %s' % (line, r2['run'], r2.get('hits'), rc, kids, str(say(r2['run']))[:200]))
        for k in kids: print('      kid', k, 'reply:', str(reply(k[0]))[:120])
        results[word] = {'expected': exp, 'dna': dna, 'derived': rows, 'kids': kids}
    json.dump(results, open('derive_results.json', 'w'))
