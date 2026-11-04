# C28b: a value is a run of digit gates, so a changed value may differ by many gates; the rule is: every differing gate is a value, a time word or a negation, with at most one negation word
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''        elif len(diff) <= 3 and all(is_value(g) or sym_of(g) in TIME_WORDS or sym_of(g) in NEG_WORDS for g in diff) and any(is_value(g) or sym_of(g) in NEG_WORDS for g in diff):
            if nm not in [d["source"] for d in disagree]: disagree.append({"source": nm, "run": r0, "line": line_text(r0)[:140], "differs": sorted(set(sym_of(g) for g in diff))})
''', '''        elif value_or_negation_diff(diff):
            if nm not in [d["source"] for d in disagree]: disagree.append({"source": nm, "run": r0, "line": line_text(r0)[:140], "differs": sorted(set(sym_of(g) for g in diff))})
''')
rep('''        if not diff or len(diff) > 3: continue
        if all(is_value(g) or sym_of(g) in TIME_WORDS or sym_of(g) in NEG_WORDS for g in diff) and any(is_value(g) or sym_of(g) in NEG_WORDS for g in diff):
            return {"source": nm, "run": r0, "line": line_text(r0)[:160], "differs": sorted(set(sym_of(g) for g in diff))}
''', '''        if not diff: continue
        if value_or_negation_diff(diff):
            return {"source": nm, "run": r0, "line": line_text(r0)[:160], "differs": sorted(set(sym_of(g) for g in diff))}
''')
rep('''def source_check(run):
''', '''def value_or_negation_diff(diff):
    # the two shapes differ only by values (runs of digit gates), time words, or one negation: the same statement with another value or its denial
    if not diff or not all(is_value(g) or sym_of(g) in TIME_WORDS or sym_of(g) in NEG_WORDS for g in diff): return False
    negs = sum(1 for g in diff if sym_of(g) in NEG_WORDS)
    return (negs <= 1) and (negs == 1 or any(is_value(g) for g in diff))
def source_check(run):
''')
open(p, "w").write(s); print("patched c28b")
