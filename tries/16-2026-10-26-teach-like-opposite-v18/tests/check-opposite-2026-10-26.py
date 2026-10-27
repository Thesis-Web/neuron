import json, urllib.request, time, sys
B = 'http://127.0.0.1:8019'
def q(sql, params=()):
    r = json.load(urllib.request.urlopen(B + '/api/q', data=json.dumps({'sql': sql, 'params': list(params)}).encode(), timeout=120)); return r.get('rows', r)
def typeline(line, limit=900):
    j = json.load(urllib.request.urlopen(B + '/api/type', data=json.dumps({'line': line}).encode(), timeout=30)); t0 = time.time()
    while True:
        v = json.load(urllib.request.urlopen(B + '/api/job?id=%d' % j['id'], timeout=30))
        if v['done']: return v
        if time.time() - t0 > limit: return {'error': 'timed out'}
        time.sleep(0.5)
line = open(sys.argv[1]).read().strip()
before = q("SELECT (SELECT count(*) FROM secondary), (SELECT count(*) FROM run), (SELECT count(*) FROM label)")[0]; print('before: secondary %d, runs %d, labels %d' % tuple(before))
for name, l in [('teach opposite', line), ('bind', 'opposite : -> opposite'), ('opposite : go', 'opposite : go'), ('opposite : can', 'opposite : can'), ('like : can', 'like : can'), ('like : is', 'like : is'), ('opposite : store', 'opposite : store')]:
    v = typeline(l); r = v.get('result') or {}
    run = q("SELECT id, kind, word FROM run WHERE parent IS NULL ORDER BY id DESC LIMIT 1")[0]
    tree = q("SELECT kind, count(*) FROM run WHERE root = ? GROUP BY kind", [run[0]])
    errs = q("SELECT s.run, substr(s.value, 1, 160) FROM sheet s JOIN run r ON r.id = s.run WHERE r.root = ? AND s.name = 'BUILD' AND s.value LIKE 'error%'", [run[0]])
    print('== %s == said: %s | %.1f s | error: %s | runs under it: %s | BUILD errors: %s' % (name, repr(r.get('output'))[:200], r.get('seconds') or 0, v.get('error'), tree, errs))
after = q("SELECT (SELECT count(*) FROM secondary), (SELECT count(*) FROM run), (SELECT count(*) FROM label)")[0]; print('after: secondary %d, runs %d, labels %d' % tuple(after))
print('formulas:', q("SELECT l.word, f.run FROM formula f JOIN label l ON l.gate = f.gate"))
c = q("SELECT gate FROM label WHERE word = 'can'")[0][0]; dg = q("SELECT trigger FROM g%d ORDER BY shard LIMIT 1" % c)[0][0]
print("can's definition node rows:", q("SELECT d.id, l.word, d.run, d.score FROM g%d d JOIN label l ON l.gate = d.source" % dg))
