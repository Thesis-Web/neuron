import sys, json; sys.path.insert(0, "/home/james/cortex"); import cortex as c
# rebuild the voice tallies from every verdict row that carries a voice, per project and per gate (build time)
for (vn,) in c.q("SELECT name FROM main.cx WHERE kind = 'voice' AND name >= '' AND n = 0"): c.q("DELETE FROM main.cx WHERE kind = 'voice' AND name = ? AND n = 0", vn)
c.q("DELETE FROM main.cx WHERE kind = 'vgate' AND name >= ''")
n = 0
for (pj,) in c.q("SELECT name FROM main.cx WHERE kind = 'project' AND name >= '' AND n = 0"):
    for (run, v) in c.q("SELECT n, value FROM main.cx WHERE kind = 'verdict' AND name = ? AND n > 0 ORDER BY n", pj):
        d = json.loads(v)
        if "voice" not in d: continue
        c.tally_voice(d["voice"], d["kind"], d.get("judge") if d.get("judge") in ("receipt", "shape", "sources") else "judgment", bool(d.get("guess")), pj, run); n += 1
print("tallied %d verdicts with a voice" % n)
