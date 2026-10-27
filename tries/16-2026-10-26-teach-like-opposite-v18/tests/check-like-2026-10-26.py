import json, urllib.request, time, sys
B = 'http://127.0.0.1:8019'
def q(sql, params=()):
    r = json.load(urllib.request.urlopen(B + '/api/q', data=json.dumps({'sql': sql, 'params': list(params)}).encode(), timeout=120))
    return r.get('rows', r)
def typeline(line, limit=900):
    j = json.load(urllib.request.urlopen(B + '/api/type', data=json.dumps({'line': line}).encode(), timeout=30))
    t0 = time.time()
    while True:
        v = json.load(urllib.request.urlopen(B + '/api/job?id=%d' % j['id'], timeout=30))
        if v['done']: return v
        if time.time() - t0 > limit: return {'error': 'timed out', 'elapsed': time.time() - t0}
        time.sleep(0.5)
line = open(sys.argv[1]).read().strip()
before = q("SELECT (SELECT count(*) FROM secondary), (SELECT count(*) FROM run), (SELECT count(*) FROM label), (SELECT count(*) FROM formula)")[0]
print('before: secondary %d, runs %d, labels %d, formulas %d' % tuple(before))
steps = [('teach like', line), ('bind', 'like : -> like'), ('like : store', 'like : store'), ('like : go', 'like : go'), ('like : store again', 'like : store'), ('like : dog', 'like : dog')]
for name, l in steps:
    v = typeline(l)
    r = v.get('result') or {}
    print('\n== %s ==' % name)
    print('  said:', repr(r.get('output'))[:300], '| %.1f s' % (r.get('seconds') or v.get('elapsed') or 0), '| error:', v.get('error'))
    # the newest line run and its tree
    run = q("SELECT id, kind, word FROM run WHERE parent IS NULL ORDER BY id DESC LIMIT 1")[0]
    tree = q("SELECT kind, count(*) FROM run WHERE root = ? GROUP BY kind", [run[0]])
    errs = q("SELECT s.run, substr(s.value, 1, 160) FROM sheet s JOIN run r ON r.id = s.run WHERE r.root = ? AND s.name = 'BUILD' AND s.value LIKE 'error%'", [run[0]])
    print('  root run', run, '| runs under it by kind:', tree, '| BUILD errors:', errs)
after = q("SELECT (SELECT count(*) FROM secondary), (SELECT count(*) FROM run), (SELECT count(*) FROM label), (SELECT count(*) FROM formula)")[0]
print('\nafter: secondary %d, runs %d, labels %d, formulas %d' % tuple(after))
print('formula rows:', q("SELECT f.id, l.word, f.run, f.ended FROM formula f JOIN label l ON l.gate = f.gate"))
print("like's DNA rows:", q("SELECT * FROM g597"))
print('bindq:', q("SELECT * FROM bindq"))
g = q("SELECT gate FROM label WHERE word = 'go'"); print('go gate:', g)
if g:
    dg = q("SELECT trigger FROM g%d ORDER BY shard LIMIT 1" % g[0][0])[0][0]
    print("go's definition node rows:", q("SELECT d.id, l.word, d.run, d.score FROM g%d d JOIN label l ON l.gate = d.source" % dg))
lk = q("SELECT id FROM run WHERE kind = 'formula' AND word = 'like' ORDER BY id")
print('like formula runs:', [r[0] for r in lk])
if lk:
    print('sheet of the first like run:', [(n, (v or '')[:60]) for n, v in q("SELECT name, value FROM sheet WHERE run = ? ORDER BY id", [lk[0][0]])])
    print('sheet of the go like run:', [(n, (v or '')[:60]) for n, v in q("SELECT name, value FROM sheet WHERE run = ? ORDER BY id", [lk[1][0]])] if len(lk) > 1 else '')
