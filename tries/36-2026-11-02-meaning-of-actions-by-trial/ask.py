import json, urllib.request, time, sys
B="http://10.31.1.106:8058"
def post(path, obj, timeout=600):
    rq=urllib.request.Request(B+path, data=json.dumps(obj).encode(), headers={"Content-Type":"application/json"}); return json.load(urllib.request.urlopen(rq, timeout=timeout))
def q(sql, params=[]): r = post("/api/q", {"sql": sql, "params": params}); return r.get("rows") if "error" not in r else "ERR " + r["error"][:100]
CELLS = {534: "how", 15: "guess", 3722: "action", 775: "against", 421: "belief", 23: "what", 25: "say", 22: "reply"}
def typed(line):
    t0=time.time(); j=post("/api/type", {"line": line}); jid=j.get("id")
    while jid and not j.get("done") and time.time()-t0 < 600: time.sleep(0.5); j=json.load(urllib.request.urlopen(B+"/api/job?id=%s"%jid, timeout=60))
    r=j.get("result") or j; run = r.get("run")
    print("== %-22s run %s  %.3f s  runs %s hits %s" % (line, run, r.get("seconds", time.time()-t0), r.get("runs"), r.get("hits")))
    rr = json.load(urllib.request.urlopen(B+"/api/run?schema=main&id=%s" % run, timeout=120))
    for c in rr.get("cells", []):
        name = CELLS.get(c[0], str(c[0])); v = c[2]; x = c[3]
        if name in ("how", "guess") and v and str(v).isdigit():
            s = q("SELECT symbol FROM label WHERE gate = ?", [int(v)]); v = "%s (%s)" % (s[0][0] if s else "?", v)
        if name in ("how", "guess", "action", "against", "belief", "what", "say"): print("   %-8s state %s: %s%s" % (name, c[1], str(v)[:300], (" -> " + str(x.get("text", ""))[:80]) if isinstance(x, dict) and x.get("text") else ""))
    errs = [t for t in [u.get("text", "") for u in rr.get("tree", [])] if "error" in str(t)]
    if errs: print("   errors in the tree:", [e[:120] for e in errs][:3])
    return run
if __name__ == "__main__":
    for line in sys.argv[1:]: typed(line)
