# while using it: the capture against the newest checkpoint (every checkpoint done) must judge for drift, hallucination and dupes only, never add parts or move state; and the verdict names which source holds the words
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''def v_judge(name, n, run, text=None, answers_given=None, judge_name=None):
''', '''NO_PARTS = set()   # (name, n) pairs judged for the record only: no part added, no state moved (the capture against a done project's newest checkpoint)
def v_judge(name, n, run, text=None, answers_given=None, judge_name=None):
''')
rep('''    accepting = kind in ("completes", "progresses", "supersedes")
''', '''    accepting = kind in ("completes", "progresses", "supersedes") and (name, n) not in NO_PARTS
''')
rep('''    if kind == "completes" and p >= THRESH and by in ("shape", "receipt"):
        st = cx_get("state", name, n)
''', '''    if kind == "completes" and p >= THRESH and by in ("shape", "receipt") and (name, n) not in NO_PARTS:
        st = cx_get("state", name, n)
''')
rep('''        nxt = cps[0][0]; newest = True   # every checkpoint done: the truth matrix still runs, against the newest one (the owner, 11-03: scan every ingress)
''', '''        nxt = cps[0][0]; newest = True; NO_PARTS.add((name, nxt))   # every checkpoint done: the truth matrix still runs against the newest one, for the record only: no parts, no state (C18.2)
''')
# which source holds the words
rep('''        for (src, band) in sources():
            if band in BANDS and cx_get("gate", src, w): g[band] += 1; held = True
''', '''        for (src, band) in sources():
            if band in BANDS and cx_get("gate", src, w): g[band] += 1; held = True; g.setdefault("by_source", {}); g["by_source"][src] = g["by_source"].get(src, 0) + 1
''')
rep('''    items = ["%s %d" % (k, g[k]) for k in ("receipt", "owner", "reference", "memory") if g.get(k)]
''', '''    items = ["%s %d" % (k, g[k]) for k in ("receipt", "owner", "reference", "memory") if g.get(k)]
    if g.get("by_source") and len(g["by_source"]) > 1: items.append("(" + " ".join("%s %d" % kv for kv in sorted(g["by_source"].items(), key=lambda kv: -kv[1])[:4]) + ")")
''')
open(p, "w").write(s); print("patched c19a")
