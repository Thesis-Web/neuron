# define_walk.py (tries/51): one define, printed as it happened. Picks the first word given that holds no definition row yet, types define : word
# through the kernel door, then prints every source return in the order it came back (by run id), in full, and the sheet cells of the line's run
# with their names. Nothing else is typed.
import json, sys, urllib.request
door = sys.argv[1]
def post(path, body):
    r = urllib.request.Request(door + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r, timeout=600))
def q(sql, params=()): return post('/api/q', {'sql': sql, 'params': list(params)}).get('rows') or []
def run_of(rid): return json.load(urllib.request.urlopen(door + '/api/run?schema=main&id=%d' % rid, timeout=120))
names = {7: 'wn', 8: 'gcide', 10: 'mwt', 11: 'moby', 12: 'map', 13: 'sqldoc', 14: 'measured', 15: 'guess', 443: 'wikt'}
fresh_words = []
for w in sys.argv[2:]:
    g = q('SELECT gate FROM label WHERE symbol = ?', [w])
    n = q('SELECT count(*) FROM node WHERE gate = ?', [g[0][0]])[0][0] if g else 0
    print('%-14s gate %-8s definition rows %d' % (w, g[0][0] if g else 'none (not a symbol yet)', n))
    if not n: fresh_words.append(w)
word = None
for w in fresh_words:
    j = post('/api/type', {'line': 'define : ' + w}); r = j['result']; x = run_of(r['run'])
    srcs = set(t['arrival'] for t in x['tree'] if t['kind'] == 3 and t['arrival'] in names)
    print('tried define : %s -> run %s, %d runs, %d born, returns from %s' % (w, r['run'], r['runs'], r['born'], sorted(names[a] for a in srcs)))
    if len(srcs) >= 2: word = w; break
if word is None: word = fresh_words[0] if fresh_words else sys.argv[2]
fresh = word is not None
if word is None: word = sys.argv[2]; print('every candidate is defined already; the first is typed and its rows are printed in the order they came back')
print('\nthe define walked through: define : %s' % word)
print('the line ran: run %s, %s runs, %s hits, %s born, %s refused, %.3f s' % (r['run'], r['runs'], r['hits'], r['born'], r['refused'], r['seconds']))
rets = [t for t in x['tree'] if t['kind'] == 3 and t['arrival'] in names]
rets.sort(key=lambda t: t['id'])
if not rets:   # a recall: no source was asked; the rows the point holds are the returns of the define that learned it, by run id
    g = q('SELECT gate FROM label WHERE symbol = ?', [word])[0][0]
    rets = [{'id': n[2], 'arrival': n[1]} for n in q('SELECT id, source, run FROM node WHERE gate = ?', [g])]; rets.sort(key=lambda t: t['id'])
    print('(a recall: the point already holds its rows; these are the returns of the define that learned it, in the order they came back)')
print('\nthe returns as they came back (%d), by run id; every one lands in cell 24 (def):' % len(rets))
for k, t in enumerate(rets, 1):
    full = run_of(t['id'])['run'].get('text') or ''
    print('%3d. %-8s run %-9d %s' % (k, names[t['arrival']], t['id'], full.replace('\n', ' ')))
print('\nthe sheet cells of the line (run %d), the definition schema:' % r['run'])
for c in sorted(x.get('cells') or [], key=lambda c: c[0]):
    nm = q('SELECT symbol FROM label WHERE gate = ?', [c[0]]); nm = nm[0][0] if nm else '?'
    v = c[2]; d = c[3]
    shown = (('run %s from %s: ' % (d.get('run'), names.get(d.get('arrival'), d.get('arrival'))) + (d.get('text') or '')[:120]) if isinstance(d, dict) and d.get('run') else (d.get('text')[:120] if isinstance(d, dict) and d.get('text') else str(v)[:160]))
    print('  cell %-4d %-10s state %d  value: %s' % (c[0], nm, c[1], shown))
other = [t for t in x['tree'] if not (t['kind'] == 3 and t['arrival'] in names)]
print('\nthe other runs under the line (%d): %s' % (len(other), ', '.join('%d (arrival %d kind %d: %s)' % (t['id'], t['arrival'], t['kind'], (t.get('text') or '')[:40]) for t in other[:12])))
