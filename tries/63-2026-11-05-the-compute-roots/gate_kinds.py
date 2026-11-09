# tries/63: what the live brain's 1.79 M gates are: each label sorted into one kind, counted by keyed reads (nothing laid). argv: door
import sys, time, json, urllib.request; sys.path.insert(0, "/mnt/d/Neuron/tries/58-2026-11-04-the-owners-way-once")
from nkdoor import Door
url = sys.argv[1]; d = Door(url)
top = json.load(urllib.request.urlopen(url + "/api/info", timeout=30))["stats"]["main"]["gates"]
KIND = """CASE
 WHEN s = '' THEN 'empty'
 WHEN s GLOB '*[^ -~]*' THEN CASE
    WHEN s GLOB '*[一-鿿]*' OR s GLOB '*[぀-ヿ]*' OR s GLOB '*[가-힯]*' THEN 'non-ascii: Chinese, Japanese, Korean'
    WHEN s GLOB '*[Ͱ-Ͽ]*' OR s GLOB '*[ἀ-῿]*' THEN 'non-ascii: Greek'
    WHEN s GLOB '*[Ѐ-ӿ]*' THEN 'non-ascii: Cyrillic'
    WHEN s GLOB '*[؀-ۿ]*' OR s GLOB '*[֐-׿]*' THEN 'non-ascii: Arabic, Hebrew'
    WHEN s GLOB '*[ऀ-෿]*' OR s GLOB '*[฀-࿿]*' THEN 'non-ascii: Indic, Thai, Tibetan'
    WHEN s GLOB '*[ɐ-ʯ]*' OR s GLOB '*[ˀ-˿]*' THEN 'non-ascii: IPA or phonetic'
    WHEN s GLOB '*[À-ɏ]*' OR s GLOB '*[Ḁ-ỿ]*' THEN 'non-ascii: Latin letters with marks'
    ELSE 'non-ascii: other' END
 WHEN s NOT GLOB '*[^0-9]*' THEN 'digits'
 WHEN length(s) = 1 THEN 'one ascii mark'
 WHEN s NOT GLOB '*[^a-z]*' THEN 'lowercase ascii'
 WHEN s NOT GLOB '*[^A-Z]*' THEN 'UPPERCASE ascii'
 WHEN s GLOB '[A-Z]*' AND substr(s, 2) NOT GLOB '*[^a-z]*' THEN 'Capitalized ascii'
 WHEN s NOT GLOB '*[^A-Za-z]*' THEN 'MiXed case ascii'
 WHEN s NOT GLOB '*[^A-Za-z0-9]*' THEN 'letters and digits'
 ELSE 'other ascii' END"""
KIND = " ".join(KIND.split("\n"))
SQL = ("WITH RECURSIVE g(x) AS (SELECT ? UNION ALL SELECT x + 1 FROM g WHERE x < ?) "
       "SELECT k, count(*), sum(born), sum(defd), group_concat(CASE WHEN rn <= 4 THEN s END, ' | ') FROM ("
       " SELECT s, born, defd, k, row_number() OVER (PARTITION BY k ORDER BY random()) AS rn FROM ("
       "  SELECT s, born, defd, " + KIND + " AS k FROM ("
       "   SELECT l.symbol AS s, n.born AS born, (n.nodes > 0) AS defd FROM g JOIN main.label l ON l.gate = g.x JOIN main.neuron n ON n.gate = g.x))) GROUP BY k")
def q(sql, p):
    j = d.post('/api/q', {'sql': sql, 'params': p})
    if j.get('error'): print('ERROR', j['error']); sys.exit(1)
    return j.get('rows') or []
t = time.time(); tot = {}
for a in range(1, top + 1, 200000):
    b = min(top, a + 199999)
    for k, c, bn, df, ex in q(SQL, [a, b]):
        x = tot.setdefault(k, [0, 0, 0, []]); x[0] += c; x[1] += bn or 0; x[2] += df or 0
        if len(x[3]) < 14 and ex: x[3] += ex.split(' | ')[:3]
print("live main gates 1..%d by kind, keyed reads, %.1f s" % (top, time.time() - t))
print("%-40s %10s %10s %10s  examples" % ("kind", "gates", "born", "defined"))
for k, (c, bn, df, ex) in sorted(tot.items(), key=lambda kv: -kv[1][0]):
    print("%-40s %10d %10d %10d  %s" % (k, c, bn, df, "  ".join(e[:24] for e in ex[:14])))
print("%-40s %10d %10d %10d" % ("all", sum(v[0] for v in tot.values()), sum(v[1] for v in tot.values()), sum(v[2] for v in tot.values())))
