# tries/61 (2026-11-05): every dna row that carries a call or spawn, read by gate only (a read by the full key lays the shard),
# and the line of every run a call or spawn names. Reads only. argv: door, out.json
import sys, time, json, urllib.request; sys.path.insert(0, ".")
from nkdoor import Door
d = Door(sys.argv[1]); out = sys.argv[2]
info = json.load(urllib.request.urlopen(sys.argv[1] + "/api/info", timeout=30)); top = info["stats"]["main"]["gates"]
t = time.time()
rows = d.q("WITH RECURSIVE g(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM g WHERE x < ?) SELECT d.gate, d.shard, d.before, d.trigger, d.call, d.spawn, d.times FROM g JOIN dna d ON d.gate = g.x WHERE d.call IS NOT NULL OR d.spawn IS NOT NULL", [top])
print("gates 1..%d read by gate: %d dna rows with a call or spawn, %.2f s" % (top, len(rows), time.time() - t))
gates = sorted(set(r[0] for r in rows) | set(r[2] for r in rows if r[2]) | set(r[3] for r in rows if r[3]))
lab = {g: d.sym(g) for g in gates}
runs = sorted(set(x for r in rows for x in (r[4], r[5]) if x))
def text(run):
    rr = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run])
    return rr[0][0] if rr and rr[0][0] else ""
rtext = {r: text(r) for r in runs}
bel = {}
for r in rows:
    b = d.q("SELECT correct, incorrect FROM belief WHERE shard = ?", [r[1]]); bel[r[1]] = b[0] if b else None
print("distinct runs named:", len(runs), "| points with such a row:", len(set(r[0] for r in rows)))
json.dump({"door": sys.argv[1], "top": top, "rows": rows, "label": lab, "runs": rtext, "belief": bel}, open(out, "w"))
