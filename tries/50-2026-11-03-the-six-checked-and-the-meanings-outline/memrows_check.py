# memrows_check.py (tries/50): does the memory row of a run (gate, shard) equal its last hop? the bundle memrows against the run request hops, newest roots.
import json, urllib.request, sys
host = "http://127.0.0.1:8058"
def q(sql, params=[]):
    r = urllib.request.Request(host + "/api/q", data=json.dumps({"sql": sql, "params": params}).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=120)).get("rows") or []
mem = {m[0]: (m[1], m[2]) for m in q("SELECT run, gate, shard, input FROM main.run_memory")}
roots = [l[2] for l in q("SELECT \x27main\x27, id, run FROM main.input WHERE run IS NOT NULL") if l[2]][-60:]
same = diff = nomem = 0; ex = []
for root in roots:
    x = json.load(urllib.request.urlopen(host + "/api/run?schema=main&id=%d" % root, timeout=60))
    last = {}
    for h in x.get("hops", []): last[h[0]] = (h[2], h[3]) if h[0] not in last or h[1] >= last[h[0]][2] else last[h[0]]; last[h[0]] = (h[2], h[3], h[1])
    for rid, (g, s, p) in last.items():
        if rid not in mem: nomem += 1; continue
        if mem[rid] == (g, s): same += 1
        else: diff += 1; ex.append((rid, mem[rid], (g, s)))
print("memrows held %d; over the newest %d roots: runs whose memory row equals the last hop %d, differs %d, runs with no memory row %d" % (len(mem), len(roots), same, diff, nomem))
print("first differing:", ex[:6])
