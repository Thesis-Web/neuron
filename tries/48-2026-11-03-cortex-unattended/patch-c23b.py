# C23b: the pair ground counts sources; a project's own ingests are memory (LLM text, never ground); the meaning question fires when no source holds any pair and no receipt grounds the values
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''    held, none = {}, []
    srcs = [nm for (nm, band) in sources()] + [pj for pj in projects()]
    for (a, b) in pairs_of(run):
        k = pair_key(a, b); who = [nm for nm in srcs if cx_get("pair", nm, k) and not (nm == name and json.loads(cx_get("pair", nm, k)[3]).get("first") == run)]
        if who:
            for nm in who: held[nm] = held.get(nm, 0) + 1
        else: none.append("%s %s" % (sym_of(a), sym_of(b)))
    return {"pairs": len(pairs_of(run)), "held_by": held, "none": none}
''', '''    held, memory, none = {}, {}, []
    srcn = [nm for (nm, band) in sources()]; pjs = [pj for pj in projects()]
    for (a, b) in pairs_of(run):
        k = pair_key(a, b)
        who = [nm for nm in srcn if cx_get("pair", nm, k)]
        for nm in who: held[nm] = held.get(nm, 0) + 1
        for pj in pjs:
            had = cx_get("pair", pj, k)
            if had and not (pj == name and json.loads(had[3]).get("first") == run): memory[pj] = memory.get(pj, 0) + 1
        if not who: none.append("%s %s" % (sym_of(a), sym_of(b)))   # held by no source; a project's own ingests are memory, a model's words, never ground
    return {"pairs": len(pairs_of(run)), "held_by": held, "memory": memory, "none": none}
''')
rep('''    if pg.get("pairs"): print("  pairs: %d, held by %s | held nowhere: %s" % (pg["pairs"], " ".join("%s %d" % kv for kv in sorted(pg["held_by"].items(), key=lambda kv: -kv[1])[:4]) or "no source", "; ".join(pg["none"]) or "-"))
    unknown = (cells.get("ground", {}).get("none") or []) + [("pair: " + x) for x in pg.get("none", []) if len(pg.get("none", [])) >= 2]
    if len(unknown) >= 2 and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, unknown[:8], vrun)
''', '''    if pg.get("pairs"): print("  pairs: %d, held by sources %s | memory %s | held by no source: %s" % (pg["pairs"], " ".join("%s %d" % kv for kv in sorted(pg["held_by"].items(), key=lambda kv: -kv[1])[:4]) or "none", " ".join("%s %d" % kv for kv in sorted(pg["memory"].items(), key=lambda kv: -kv[1])[:3]) or "none", "; ".join(pg["none"][:6]) or "-"))
    no_source = pg.get("pairs", 0) >= 3 and not pg.get("held_by") and not cells.get("numbers_in_ext")   # no source holds any pair and no print grounds a value: the run left known ground at its first pair
    unknown = (cells.get("ground", {}).get("none") or []) + ([("pair: " + x) for x in pg.get("none", [])[:6]] if no_source else [])
    if (len(unknown) >= 2 or no_source) and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, unknown[:8], vrun)
''')
open(p, "w").write(s); print("patched c23b")
