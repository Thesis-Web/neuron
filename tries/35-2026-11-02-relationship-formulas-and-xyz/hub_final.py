import json, urllib.request, time, sys
sys.path.insert(0, '/mnt/d/Neuron/tries/35-2026-11-02-relationship-formulas-and-xyz'); import hub_g35 as H
info = lambda: json.load(urllib.request.urlopen(H.B + "/api/info", timeout=60))
def gate(w): r = H.q("SELECT gate FROM label WHERE symbol = ?", [w]); return r[0][0] if r else None
def xyz(w): return H.q("SELECT round(x,2), round(y,2), round(z,2), shard, before, next, run, moved FROM xyz WHERE gate = ?", [gate(w)])
def nodes(w): g = gate(w); return H.q('SELECT count(*) FROM main."%d.node"' % g)[0][0] if g else None
print("== H1 info:", info()["routers"])
print("== H2 recalls on the hub (with xyz_go, the catalog rows, after the back-populations):")
for w in ["stone", "bread", "who", "water"]:
    n0 = nodes(w); t0 = time.time(); run, rep = H.typed("define : " + w, quiet=True); dt = time.time() - t0
    print("  define : %-6s run %s  %.1f s  node rows %s -> %s  returns under it %s  xyz %s" % (w, run, dt, n0, nodes(w), H.q("SELECT count(*) FROM run WHERE root = ? AND kind = 3 AND arrival IN (7, 3369)", [run]), xyz(w)))
print("== H4 the space's row, define's rows:", H.q('SELECT shard, times FROM main."3"'), H.q('SELECT shard, before, trigger, call, times FROM main."153"'))
print("== H6 born's row:", H.q('SELECT shard, before, trigger, call, times FROM main."16"'))
print("== H7 the sixth's newest lines in main:", H.q("SELECT id FROM run WHERE arrival = 5 ORDER BY id DESC LIMIT 2"))
print("== N1:", H.q("SELECT count(*) FROM formula"), H.q("SELECT count(*) FROM pull"))
print("== N2 places on the hub:", H.q("SELECT count(*), sum(moved > 1), max(moved) FROM xyz"))
for w in ["water", "ice", "stone", "bread", "hinge", "origin", "takakkaw"]: print("  %-9s" % w, xyz(w))
print("  water's is relations' places:", H.q("SELECT m.symbol, round(o.x,1), round(o.y,1), round(o.z,1) FROM rel r JOIN label l ON l.gate = r.kind JOIN label m ON m.gate = r.other JOIN xyz o ON o.gate = r.other WHERE r.gate = ? AND l.symbol = 'is' LIMIT 6", [gate("water")]))
print("== N3 rel kinds:", H.q("SELECT l.symbol, c FROM (SELECT kind, count(*) c FROM rel GROUP BY kind) r JOIN label l ON l.gate = r.kind ORDER BY c DESC"), H.q("SELECT count(*) FROM rel"))
print("== N5 takakkaw's table:", H.q('SELECT shard, before, trigger, call, spawn, times FROM main."%d"' % gate("takakkaw")), "nodes", nodes("takakkaw"))
print("== hub prof top:", [(round(v[1], 1), v[0], round(v[1] / max(v[0], 1), 3), k[:40]) for k, v in list(json.load(urllib.request.urlopen(H.B + "/api/prof", timeout=60)).items())[:4]])
print("== info end:", info()["routers"])
