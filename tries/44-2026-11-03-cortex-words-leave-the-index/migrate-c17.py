import sys, json; sys.path.insert(0, "/home/james/cortex"); import cortex as c
def upd(kind, name, n, val): c.q("UPDATE main.cx SET value = ? WHERE kind = ? AND name = ? AND n = ?", val, kind, name, n)
counts = {}; odd = []
for (name,) in c.q("SELECT name FROM main.cx WHERE kind = 'project' AND name >= '' AND n = 0"):
    for (k, run, at, ts, v) in c.cx_list("ingest", name, limit=5000):
        if k <= 0: continue
        t, times = c.ingest_text(v)
        if t is not None and (not isinstance(v, str) or '"t"' in v or not v.startswith("{")):
            upd("ingest", name, k, json.dumps({"times": times})); counts["ingest"] = counts.get("ingest", 0) + 1
    for kind, field in (("part", "t"), ("verdict", "text"), ("receipt", "t")):
        for (k, v) in c.q("SELECT n, value FROM main.cx WHERE kind = ? AND name = ? AND n > 0 ORDER BY n", kind, name):
            try: d = json.loads(v)
            except ValueError: continue
            if field in d:
                if kind == "part" and d.get("run") and c.line_text(d["run"]) != d["t"]: odd.append((name, d.get("n"), d["run"], d["t"][:80], c.line_text(d["run"])[:80]))
                d.pop(field); upd(kind, name, k, json.dumps(d)); counts[kind] = counts.get(kind, 0) + 1
    for (k, v) in c.q("SELECT n, value FROM main.cx WHERE kind = 'receipts' AND name = ? AND n >= 0 ORDER BY n", name):
        rc = json.loads(v); ch = False
        for cmd, d in rc.items():
            for l in d.get("lines", []):
                if "t" in l: l.pop("t"); ch = True
        if ch: upd("receipts", name, k, json.dumps(rc)); counts["receipts"] = counts.get("receipts", 0) + 1
print("migrated rows:", counts)
for o in odd: print("  part whose stored text differed from its replay: %s C%s run %d\n    stored: %s\n    replay: %s" % o)
tot = c.q("SELECT sum(length(value)) FROM main.cx")[0][0]
by = {k: v for (k, v) in c.q("SELECT kind, sum(length(value)) FROM main.cx WHERE kind >= '' GROUP BY kind")}
print("index bytes %d; ingest %d part %d verdict %d receipt %d receipts %d" % (tot, by.get("ingest", 0), by.get("part", 0), by.get("verdict", 0), by.get("receipt", 0), by.get("receipts", 0)))
