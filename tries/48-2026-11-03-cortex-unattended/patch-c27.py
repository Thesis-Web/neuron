# C27 the words leave the index for project, checkpoint and expected rows and the formula snapshots: the rows keep no text, cx_get and cx_list replay it from the run
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''def cx_get(kind, name, n):
    rows = q("SELECT run, at, ts, value FROM main.cx WHERE kind = ? AND name = ? AND n = ?", kind, name, n)
    return rows[0] if rows else None
def cx_list(kind, name, desc=False, limit=1000):
    return q("SELECT n, run, at, ts, value FROM main.cx WHERE kind = ? AND name = ? ORDER BY n %s LIMIT %d" % ("DESC" if desc else "ASC", limit), kind, name)
''', '''TEXT_KINDS = ("project", "checkpoint", "expected")   # C27: these rows keep no text; the typed line replays from its run
def cx_get(kind, name, n):
    rows = q("SELECT run, at, ts, value FROM main.cx WHERE kind = ? AND name = ? AND n = ?", kind, name, n)
    if not rows: return None
    r = rows[0]
    if kind in TEXT_KINDS and r[0] and not r[3]: return (r[0], r[1], r[2], line_text(r[0]))
    return r
def cx_list(kind, name, desc=False, limit=1000):
    rows = q("SELECT n, run, at, ts, value FROM main.cx WHERE kind = ? AND name = ? ORDER BY n %s LIMIT %d" % ("DESC" if desc else "ASC", limit), kind, name)
    if kind in TEXT_KINDS: rows = [(n, run, at, ts, (line_text(run) if run and not v else v)) for (n, run, at, ts, v) in rows]
    return rows
''')
rep('''    cx_put(kind, name, n if n is not None else run, run, at, body)
    return run, at, r
''', '''    cx_put(kind, name, n if n is not None else run, run, at, "" if kind in TEXT_KINDS else body)
    return run, at, r
''')
# the formula snapshot keeps no checkpoint text
rep('''        cps[str(n)] = {"state": st[3] if st else "open", "parts": len(parts_of(name, n, 1000)), "verdicts": vs.get(n, {}), "text": text, "expected": ex[3] if ex else ""}
''', '''        cps[str(n)] = {"state": st[3] if st else "open", "parts": len(parts_of(name, n, 1000)), "verdicts": vs.get(n, {})}
''')
rep('''        print("  C%s done: %s | part: %s" % (n, cps[n]["expected"][:100] or cps[n]["text"][:100], line_text(ps[0]["run"])[:110] if ps else "(no part recorded)"))
''', '''        ex = cx_get("expected", name, int(n)); ck = cx_get("checkpoint", name, int(n))
        print("  C%s done: %s | part: %s" % (n, (ex[3] if ex else "")[:100] or (ck[3] if ck else "")[:100], line_text(ps[0]["run"])[:110] if ps else "(no part recorded)"))
''')
rep('''        print("  C%s [%s] expected: %s | missing: %s" % (n, c["state"], c["expected"][:110] or "(none)", ", ".join(miss)))
''', '''        ex = cx_get("expected", name, int(n))
        print("  C%s [%s] expected: %s | missing: %s" % (n, c["state"], (ex[3] if ex else "")[:110] or "(none)", ", ".join(miss)))
''')
open(p, "w").write(s); print("patched c27")
