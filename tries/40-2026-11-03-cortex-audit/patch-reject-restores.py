p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''    if retire_part(name, n, run, "owner", "rejected_by"): print("part of run %d rejected from %s C%d by the owner" % (run, name, n))
    else: raise SystemExit("no part of run %s in %s C%d" % (run, name, n))
'''
new = '''    if retire_part(name, n, run, "owner", "rejected_by"): print("part of run %d rejected from %s C%d by the owner" % (run, name, n))
    else: raise SystemExit("no part of run %s in %s C%d" % (run, name, n))
    # a part this run had superseded comes back: the newer value was never true, so the older one stands again
    for (v,) in q("SELECT value FROM main.cx WHERE kind = 'part' AND name = ? AND n > 0 ORDER BY ts DESC LIMIT 200", name):
        d = json.loads(v)
        if d.get("n") == n and d.get("superseded_by") == run:
            d.pop("superseded_by"); cx_put("part", name, text_key(d["t"]), d["run"], clock(), json.dumps(d)); print("part of run %d stands again in %s C%d (it was superseded by the rejected run)" % (d["run"], name, n))
'''
assert old in s and "stands again" not in s; s = s.replace(old, new, 1); open(p, "w").write(s); print("patched")
