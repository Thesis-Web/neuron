# C28 sources judging each other: for a claim, the sources holding a near-identical line (confirm) and those whose near line differs only by a value or a negation (disagree); three or more disagreeing and none confirming = false by sources (the owner, 11-03 17:0x)
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''def key_gates(name, run):
''', '''def source_check(run):
    # C28: every source's lines that share this claim's pairs; a near-identical line confirms, one that differs only by a value or a negation disagrees; the sources judge the claim and each other
    confirm, disagree, seen = [], [], set()
    srcs = [nm for (nm, band) in sources()]
    cand = []
    for (a, b) in set(pairs_of(run)):
        for nm in srcs:
            had = cx_get("pair", nm, pair_key(a, b))
            if had:
                r0 = int(json.loads(had[3]).get("first", 0))
                if r0 and r0 != run and (nm, r0) not in seen: seen.add((nm, r0)); cand.append((nm, r0))
    ing = content_gates(run)
    for (nm, r0) in cand[:24]:
        O = content_gates(r0)
        if not O or len(O) < 4: continue
        oa, ob = seq_diff(O, ing); diff = oa + ob
        if not diff:
            if nm not in confirm: confirm.append(nm)
        elif len(diff) <= 3 and all(is_value(g) or sym_of(g) in TIME_WORDS or sym_of(g) in NEG_WORDS for g in diff) and any(is_value(g) or sym_of(g) in NEG_WORDS for g in diff):
            if nm not in [d["source"] for d in disagree]: disagree.append({"source": nm, "run": r0, "line": line_text(r0)[:140], "differs": sorted(set(sym_of(g) for g in diff))})
    return {"confirm": confirm, "disagree": disagree}
def key_gates(name, run):
''')
rep('''    cells["owner_conflict"] = owner_conflict(run)
    return cells
''', '''    cells["owner_conflict"] = owner_conflict(run)
    cells["sources"] = source_check(run)
    return cells
''')
# the formula: three or more sources disagreeing and none confirming is false by sources
rep('''    rb = cells.get("receipt_before_claim")
''', '''    sc = cells.get("sources") or {}
    if len(sc.get("disagree", [])) >= 3 and not sc.get("confirm"): return "hallucination", "sources"   # C28 (the owner): a statement proven false by three or more sources
    rb = cells.get("receipt_before_claim")
''')
rep('''    elif by in ("shape", "receipt"): p = cells["shape_expected"] if kind == "completes" else 1.0
''', '''    elif by in ("shape", "receipt", "sources"): p = cells["shape_expected"] if kind == "completes" else 1.0
''')
rep('''    elif kind in ("hallucination", "invention") and by in ("receipt", "shape"): d["false"] += 1   # proven by the machine's print or the brain's shape, never by a model's word
''', '''    elif kind in ("hallucination", "invention") and by in ("receipt", "shape", "sources"): d["false"] += 1   # proven by the machine's print, the brain's shape or three sources, never by a model's word
''')
# the belief row print
rep('''    oc = cells.get("owner_conflict")
    if oc:
''', '''    sc = cells.get("sources") or {}
    if sc.get("confirm") or sc.get("disagree"): print("  sources: %d confirm (%s) | %d disagree (%s)" % (len(sc.get("confirm", [])), ", ".join(sc.get("confirm", [])[:4]), len(sc.get("disagree", [])), "; ".join("%s differs by %s: %s" % (d["source"], ",".join(d["differs"]), d["line"][:70]) for d in sc.get("disagree", [])[:3])))
    oc = cells.get("owner_conflict")
    if oc:
''')
open(p, "w").write(s); print("patched c28")
