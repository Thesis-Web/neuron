# known_meanings.py (tries/50): the points that hold DNA rows with a call or spawn on the kernel, read by key over the first N gates (the
# hand-laid points and the first-run tools live low); prints each point, its rows, and the run each row calls. Reads only.
import json, sys, urllib.request, time
host = sys.argv[1]; N = int(sys.argv[2])
def q(sql, params):
    r = urllib.request.Request(host + "/api/q", data=json.dumps({"sql": sql, "params": params}).encode(), headers={"Content-Type": "application/json"})
    j = json.load(urllib.request.urlopen(r, timeout=120)); return j.get("rows") or []
t0 = time.perf_counter(); pts = 0; rows = 0; out = []
for g in range(1, N + 1):
    d = q("SELECT shard, before, trigger, call, spawn, times FROM dna WHERE gate = ? AND ( call IS NOT NULL OR spawn IS NOT NULL )", [g])
    if not d: continue
    s = q("SELECT symbol FROM label WHERE gate = ?", [g]); pts += 1; rows += len(d)
    out.append((g, s[0][0] if s else "?", len(d), [(r[1], r[2], r[3] or r[4], r[5]) for r in d]))
print("gates 1..%d: %d points hold %d dna rows with a call or spawn; %.1f s" % (N, pts, rows, time.perf_counter() - t0))
for g, s, n, d in out: print("%6d %-12s rows %d  (before, trigger, run, times): %s" % (g, s, n, " ".join("[%s %s %s %s]" % r for r in d[:6])))
