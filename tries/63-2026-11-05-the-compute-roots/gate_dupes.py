# tries/63: are gates repeated symbols? per chunk, the symbols of non-ascii gates grouped; the whole brain's distinct count. Keyed reads only.
import sys, time, json, urllib.request, collections; sys.path.insert(0, "/mnt/d/Neuron/tries/58-2026-11-04-the-owners-way-once")
from nkdoor import Door
url = sys.argv[1]; d = Door(url)
def q(sql, p):
    j = d.post('/api/q', {'sql': sql, 'params': p})
    if j.get('error'): print('ERROR', j['error']); sys.exit(1)
    return j.get('rows') or []
top = json.load(urllib.request.urlopen(url + "/api/info", timeout=30))["stats"]["main"]["gates"]
W = "WITH RECURSIVE g(x) AS (SELECT ? UNION ALL SELECT x + 1 FROM g WHERE x < ?) "
t = time.time(); na = collections.Counter(); asc = collections.Counter(); firstgate = {}
for a in range(1, top + 1, 200000):
    b = min(top, a + 199999)
    for s, c, mn in q(W + "SELECT l.symbol, count(*), min(g.x) FROM g JOIN main.label l ON l.gate = g.x GROUP BY l.symbol HAVING count(*) > 1 OR l.symbol GLOB '*[^ -~]*'", [a, b]):
        (na if any(ord(ch) > 126 for ch in s) else asc)[s] += c
        firstgate[s] = min(firstgate.get(s, 1 << 40), mn)
print("%.1f s" % (time.time() - t))
print("non-ascii gates %d, distinct symbols among them %d" % (sum(na.values()), len(na)))
print("most repeated non-ascii:", [(s, c, firstgate[s]) for s, c in na.most_common(12)])
rep = {s: c for s, c in asc.items() if c > 1}
print("ascii symbols held by more than one gate within a 200k chunk: %d symbols, %d gates" % (len(rep), sum(rep.values())))
print("most repeated ascii:", sorted(rep.items(), key=lambda kv: -kv[1])[:12])
