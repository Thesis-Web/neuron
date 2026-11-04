import sys, json; sys.path.insert(0, "/home/james/cortex"); import cortex as c
def upd(kind, name, n, val): c.q("UPDATE main.cx SET value = ? WHERE kind = ? AND name = ? AND n = ?", val, kind, name, n)
cnt = {}; bad = 0
for (name,) in c.q("SELECT name FROM main.cx WHERE kind = 'project' AND name >= '' AND n = 0"):
    for kind in c.TEXT_KINDS:
        for (k, run, at, ts, v) in c.q("SELECT n, run, at, ts, value FROM main.cx WHERE kind = ? AND name = ? ORDER BY n", kind, name):
            if not v or not run: continue
            if c.line_text(run) != v: bad += 1; print("  differs:", kind, name, k, "|", v[:60], "|", c.line_text(run)[:60]); continue
            upd(kind, name, k, ""); cnt[kind] = cnt.get(kind, 0) + 1
    for (k, v) in c.q("SELECT n, value FROM main.cx WHERE kind = 'formula' AND name = ? AND n > 0 ORDER BY n", name):
        d = json.loads(v); ch = False
        for cp in d.get("checkpoints", {}).values():
            for f in ("text", "expected"):
                if f in cp: cp.pop(f); ch = True
        if ch: upd("formula", name, k, json.dumps(d)); cnt["formula"] = cnt.get("formula", 0) + 1
print("migrated:", cnt, "| rows left with text because the replay differed:", bad)
tot = c.q("SELECT sum(length(value)) FROM main.cx")[0][0]; by = {k: v for (k, v) in c.q("SELECT kind, sum(length(value)) FROM main.cx WHERE kind >= '' GROUP BY kind")}
print("index bytes %d; project %d checkpoint %d expected %d formula %d pair %d gate %d" % (tot, by.get("project", 0), by.get("checkpoint", 0), by.get("expected", 0), by.get("formula", 0), by.get("pair", 0), by.get("gate", 0)))
