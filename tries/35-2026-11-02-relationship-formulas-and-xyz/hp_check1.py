import json, urllib.request, time, socket
B="http://10.31.1.106:8058"
def post(path, obj, timeout=600):
    rq=urllib.request.Request(B+path, data=json.dumps(obj).encode(), headers={"Content-Type":"application/json"}); return json.load(urllib.request.urlopen(rq, timeout=timeout))
def q(sql, params=[]): return post("/api/q", {"sql": sql, "params": params}).get("rows")
def typed(line):
    t0=time.time(); j=post("/api/type", {"line": line}); jid=j.get("id")
    while jid and not j.get("done") and time.time()-t0 < 600: time.sleep(0.5); j=json.load(urllib.request.urlopen(B+"/api/job?id=%s"%jid, timeout=60))
    r=j.get("result") or j; out=[(o[2], str(o[3])[:90]) for o in (r.get("out") or []) if o[2] in ("def","known","unknown","ok")]
    print("  %-28s run %s  %.3f s  hits %s runs %s born %s  %s" % (line, r.get("run"), r.get("seconds", time.time()-t0), r.get("hits"), r.get("runs"), r.get("born"), [(c, v[:40]) for c, v in out][:4]), flush=True); return r
def gate(w): return q("SELECT gate FROM label WHERE symbol = ?", [w])[0][0]
def xyz(w): return q("SELECT x, y, z, shard, before, next, at, run, moved FROM xyz WHERE gate = ?", [gate(w)])
def nodes(w): return q("SELECT count(*) FROM node WHERE gate = ?", [gate(w)])[0][0]
print("== N2: the place moves when a shard with another meaning is used on the point")
print("water xyz before:", xyz("water"), "nodes", nodes("water"))
r = typed("define : water"); print("water xyz after define:", xyz("water"), "nodes", nodes("water"))
r = typed("define : water"); print("water xyz after the same line again:", xyz("water"))
r = typed("water is wet"); print("water xyz after 'water is wet':", xyz("water"), " wet:", xyz("wet"))
print("== K2: recalls")
for w in ["who", "stone", "bread", "hinge", "know"]: typed("define : " + w)
print("  nodes who", nodes("who"), "stone", nodes("stone"), "bread", nodes("bread"))
print("== K4: a never-seen word in a plain sentence")
import random; w = "quoxleb" + str(random.randint(100, 999))
g0 = q("SELECT max(gate) FROM label")[0][0]
r = typed("the %s is here" % w)
g = gate(w); print("  gate", g, "(max before %d)" % g0, "dna", q("SELECT shard, before, trigger, call, spawn, times FROM dna WHERE gate = ?", [g]), "nodes", nodes(w), "xyz", xyz(w), "rel", q("SELECT count(*) FROM rel WHERE gate = ?", [g]))
print("== a word the sources know, never seen: the long way then the short, with its relationships and place")
w2 = "takakkaw"; print("  takakkaw nodes", nodes(w2), "xyz", xyz(w2))
for w2 in ["nunavut", "zebu", "okapi"]:
    if nodes(w2) == 0 or True:
        r = typed("define : " + w2); print("  ", w2, "nodes", nodes(w2), "rel", q("SELECT l.symbol, m.symbol FROM rel r JOIN label l ON l.gate = r.kind JOIN label m ON m.gate = r.other WHERE r.gate = ? LIMIT 8", [gate(w2)]), "xyz", xyz(w2))
print("== info"); print(json.load(urllib.request.urlopen(B+"/api/info", timeout=60))["stats"]["main"])
