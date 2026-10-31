#!/usr/bin/env python3
# hub-drive.py (2026-10-31): types lines files through a v7 door (the hub or its twin), waits for each line's run to end, fills {run:k}
# from the door's answers, and reads counts back. It decides nothing. usage: hub-drive.py PORT lines FILE [FILE...] | hub-drive.py PORT watch SECONDS | hub-drive.py PORT type "LINE"
import sys, json, time, urllib.request
PORT = int(sys.argv[1]); BASE = "http://localhost:%d" % PORT
def get(path):
    with urllib.request.urlopen(BASE + path, timeout=600) as r: return json.load(r)
def post(path, body):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r: return json.load(r)
def q(sql):
    try:
        r = post("/api/q", {"sql": sql}); return r.get("rows", r)
    except Exception as e: return "q failed: %s" % e
def type_line(line, prompt):
    t = time.time(); j = post("/api/type", {"line": line, "prompt": prompt})
    while not j.get("done"): time.sleep(0.5); j = get("/api/job?id=%d" % j["id"])
    return j, time.time() - t
def run_of(j):
    r = j.get("result") or {}
    for k in ("run", "id"):
        if isinstance(r, dict) and k in r: return r[k]
    return None
def watch(seconds, step=20):
    t0 = time.time(); last = None
    while time.time() - t0 <= seconds:
        info = get("/api/info"); hops = info["routers"]["main"]["hops"]
        row = (int(time.time() - t0), hops, q("SELECT count(*) FROM hop")[0][0], q("SELECT count(DISTINCT about) FROM run WHERE kind = 3")[0][0], q("SELECT count(*) FROM sixth.asked")[0][0], q("SELECT sent, count(*) FROM sixth.spawned GROUP BY sent"), info["busy"] and info["busy"].get("line"))
        print("+%4ds hops %9d | mailbox %6d | points with a return %6d | asked %6d | spawned %s | busy %s" % row, flush=True); time.sleep(step)
mode = sys.argv[2]
if mode == "watch": watch(int(sys.argv[3]))
elif mode == "type":
    j, dt = type_line(sys.argv[3], "sixth" if sys.argv[3].startswith("6> ") else "main"); print("%.1f s run %s result %s" % (dt, run_of(j), str(j.get("result"))[:300]))
else:
    runs = {}; n = 0
    for f in sys.argv[3:]:
        for raw in open(f, encoding="utf-8"):
            line = raw.rstrip("\n")
            if not line.strip() or line.startswith("#"): continue
            n += 1
            for k, v in runs.items(): line = line.replace("{run:%d}" % k, str(v))
            prompt = "sixth" if line.startswith("6> ") else "main"
            j, dt = type_line(line, prompt); r = run_of(j); runs[n] = r
            res = j.get("result"); err = j.get("error")
            print("%2d %-5s %6.1f s run %-7s %s %s" % (n, prompt, dt, r, (("ERROR " + str(err)) if err else ""), str(res)[:260].replace("\n", " ")), flush=True)
