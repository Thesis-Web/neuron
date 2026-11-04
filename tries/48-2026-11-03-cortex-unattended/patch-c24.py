# C24 sources agreeing, the belief row: per claim, how many sources hold at least half of its pairs, printed as agreement k of m and kept on the part
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''    return {"pairs": len(pairs_of(run)), "held_by": held, "memory": memory, "none": none}
''', '''    np_ = len(pairs_of(run))
    agree = sorted([nm for nm, c in held.items() if np_ and c * 2 >= np_])   # a source agrees with a claim when it holds at least half of its pairs (C24: the belief row weighs sources agreeing)
    return {"pairs": np_, "held_by": held, "memory": memory, "none": none, "agree": agree, "sources": len(srcn)}
''')
rep('''    if pg.get("pairs"): print("  pairs: %d, held by sources %s | memory %s | held by no source: %s" % (pg["pairs"], " ".join("%s %d" % kv for kv in sorted(pg["held_by"].items(), key=lambda kv: -kv[1])[:4]) or "none", " ".join("%s %d" % kv for kv in sorted(pg["memory"].items(), key=lambda kv: -kv[1])[:3]) or "none", "; ".join(pg["none"][:6]) or "-"))
''', '''    if pg.get("pairs"): print("  pairs: %d, held by sources %s | memory %s | held by no source: %s | agreement %d of %d sources%s" % (pg["pairs"], " ".join("%s %d" % kv for kv in sorted(pg["held_by"].items(), key=lambda kv: -kv[1])[:4]) or "none", " ".join("%s %d" % kv for kv in sorted(pg["memory"].items(), key=lambda kv: -kv[1])[:3]) or "none", "; ".join(pg["none"][:6]) or "-", len(pg.get("agree", [])), pg.get("sources", 0), (" (" + ", ".join(pg["agree"][:4]) + ")") if pg.get("agree") else ""))
''')
rep('''    part = add_part(name, n, run, text, p, judge, cells.get("ground")) if accepting else ("rejected" if retire_part(name, n, run, vrun, "rejected_by") else "")
''', '''    gr = dict(cells.get("ground") or {}); pg0 = cells.get("pair_ground") or {}
    if pg0.get("pairs"): gr["agree"] = len(pg0.get("agree", [])); gr["of"] = pg0.get("sources", 0)
    part = add_part(name, n, run, text, p, judge, gr) if accepting else ("rejected" if retire_part(name, n, run, vrun, "rejected_by") else "")
''')
rep('''    if g.get("none"): items.append("none: " + ",".join(g["none"]))
    return " ".join(items) or "no ground"
''', '''    if g.get("none"): items.append("none: " + ",".join(g["none"]))
    if g.get("of"): items.append("agreement %d of %d" % (g.get("agree", 0), g["of"]))
    return " ".join(items) or "no ground"
''')
open(p, "w").write(s); print("patched c24")
