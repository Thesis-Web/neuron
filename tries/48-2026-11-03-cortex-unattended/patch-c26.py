# C26 a claim that contradicts an owner line becomes a question: a claim whose shape differs from an owner-words run only by a value or a negation
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''def key_gates(name, run):
''', '''NEG_WORDS = set("not no never none nothing nor cannot without".split())
def owner_conflict(run):
    # C26: the owner's lines that share this claim's pairs; one that differs only by a value or a negation is a contradiction to ask about, never a verdict (the owner can be wrong by error)
    owners = [nm for (nm, band) in sources() if band == "owner"]
    if not owners: return None
    cand = {}
    for (a, b) in set(pairs_of(run)):
        for nm in owners:
            had = cx_get("pair", nm, pair_key(a, b))
            if had: cand[int(json.loads(had[3]).get("first", 0))] = nm
    ing = content_gates(run)
    for (r0, nm) in list(cand.items())[:12]:
        if not r0 or r0 == run: continue
        O = content_gates(r0)
        if not O or len(O) < 4: continue
        oa, ob = seq_diff(O, ing); diff = oa + ob
        if not diff or len(diff) > 3: continue
        if all(is_value(g) or sym_of(g) in TIME_WORDS or sym_of(g) in NEG_WORDS for g in diff) and any(is_value(g) or sym_of(g) in NEG_WORDS for g in diff):
            return {"source": nm, "run": r0, "line": line_text(r0)[:160], "differs": sorted(set(sym_of(g) for g in diff))}
    return None
def key_gates(name, run):
''')
rep('''    cells["pair_ground"] = pair_ground(name, run)
    return cells
''', '''    cells["pair_ground"] = pair_ground(name, run)
    cells["owner_conflict"] = owner_conflict(run)
    return cells
''')
rep('''    unknown = (cells.get("ground", {}).get("none") or []) + ([("pair: " + x) for x in pg.get("none", [])[:6]] if no_source else [])
    if (len(unknown) >= 2 or no_source) and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, unknown[:8], vrun)
''', '''    unknown = (cells.get("ground", {}).get("none") or []) + ([("pair: " + x) for x in pg.get("none", [])[:6]] if no_source else [])
    oc = cells.get("owner_conflict")
    if oc:
        print("  against an owner line (differs by %s): %s" % (",".join(oc["differs"]), oc["line"][:120])); unknown = ["against the owner line run %d (%s): %s" % (oc["run"], ",".join(oc["differs"]), oc["line"][:80])] + unknown
    asking = (name, n) not in NO_PARTS   # a session's narration judged for the record only asks no meaning questions
    if asking and oc and kind in ("completes", "progresses", "supersedes"): ask_question(name, n, run, unknown[:8], vrun)
    if asking and (len(unknown) >= 2 or no_source) and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, unknown[:8], vrun)
''')
open(p, "w").write(s); print("patched c26")
