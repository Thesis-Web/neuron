p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:90], s.count(old))
    s = s.replace(old, new)
# 1. times and dates are not values
rep('''    return [t for t in NUM.findall(text.lower()) if ":" not in t and "-" not in t]
''', '''    t = re.sub(r"\\b\\d{1,2}:\\d{2}(:\\d{2})?\\b|\\b\\d{4}-\\d{2}-\\d{2}\\b|\\b\\d{1,2}-\\d{2}\\b", " ", text.lower())
    return NUM.findall(t)
''')
# 2. the receipt judges only a claim made after it; the memory ground is the whole brain's cortex lines, not this project only; the newest print kept for the label
rep('''    cells = {"receipt_runs": 0, "receipt_cmds": [], "numbers": numbers(text), "numbers_in": [], "numbers_out": [], "ground": {"receipt": 0, "owner": 0, "reference": 0, "memory": 0, "none": []}}
    rc = receipts_of(name, n); rnums, rwords = set(), set()
    for cmd, d in rc.items():
        cells["receipt_cmds"].append(cmd)
        for l in d.get("lines", []):
            cells["receipt_runs"] += 1; rnums |= set(numbers(l["t"])); rwords |= set(g for g in content_gates(l["run"]) if not is_value(g))
    if cells["receipt_runs"]:
        cells["numbers_in"] = [t for t in cells["numbers"] if t in rnums]; cells["numbers_out"] = [t for t in cells["numbers"] if t not in rnums]
    g = cells["ground"]; new = set(new_syms)
    for w in set(x for x in content_gates(run) if not is_value(x)):
        sym = sym_of(w); held = False
        if w in rwords: g["receipt"] += 1; held = True
        for (src, band) in sources():
            if band in BANDS and cx_get("gate", src, w): g[band] += 1; held = True
        if sym not in new: g["memory"] += 1; held = True
        if not held: g["none"].append(sym)
''', '''    cells = {"receipt_runs": 0, "receipt_cmds": [], "receipt_before_claim": False, "receipt_newest": "", "numbers": numbers(text), "numbers_in": [], "numbers_out": [], "ground": {"receipt": 0, "owner": 0, "reference": 0, "memory": 0, "none": []}}
    rc = receipts_of(name, n); rnums, rwords, newest = set(), set(), 0
    for cmd, d in rc.items():
        cells["receipt_cmds"].append(cmd)
        for l in d.get("lines", []):
            cells["receipt_runs"] += 1; rnums |= set(numbers(l["t"])); rwords |= set(g for g in content_gates(l["run"]) if not is_value(g)); newest = max(newest, l["run"])
    if cells["receipt_runs"]:
        cells["receipt_before_claim"] = newest < run   # a print the claim could have read; a later print is not evidence against an earlier claim, only a label
        cells["numbers_in"] = [t for t in cells["numbers"] if t in rnums]; cells["numbers_out"] = [t for t in cells["numbers"] if t not in rnums]
        cells["receipt_newest"] = " ; ".join("%s => %s" % (cmd, " / ".join(l["t"][:60] for l in d.get("lines", [])[1:3] or d.get("lines", [])[:1])) for cmd, d in rc.items())
    g = cells["ground"]; new = set(new_syms)
    for w in set(x for x in content_gates(run) if not is_value(x)):
        sym = sym_of(w); held = False
        if w in rwords: g["receipt"] += 1; held = True
        for (src, band) in sources():
            if band in BANDS and cx_get("gate", src, w): g[band] += 1; held = True
        if sym not in new or any(cx_get("gate", pj, w) for pj in projects() if pj != name): g["memory"] += 1; held = True
        if not held: g["none"].append(sym)
''')
rep('''_SRC = []
def sources():
''', '''_PJ = []
def projects():
    if not _PJ: _PJ.extend(sorted(set(r[0] for r in q("SELECT name FROM main.cx WHERE kind = 'project' AND name >= '' AND n = 0"))))
    return _PJ
_SRC = []
def sources():
''')
# 3. the formula: the receipt rules need a print older than the claim; the hallucination guard is the receipt's own words or the expected's shape
rep('''    if cells.get("receipt_runs") and cells.get("numbers_out") and cells.get("shape_expected", 0) >= 0.5: return "hallucination", "receipt"   # a value the machine never printed
    if cells.get("supersedes_run"): return "supersedes", ("receipt" if cells.get("receipt_runs") and cells.get("numbers_in") else "shape")   # the same shape as an accepted part, only value or time gates out of line
''', '''    rb = cells.get("receipt_before_claim")
    if rb and cells.get("numbers_out") and (cells["ground"]["receipt"] >= 2 or cells.get("shape_expected", 0) >= 0.5): return "hallucination", "receipt"   # a value the machine never printed, said after the print
    if cells.get("supersedes_run"): return "supersedes", ("receipt" if rb and cells.get("numbers_in") and not cells.get("numbers_out") else "shape")   # the same shape as an accepted part, only value or time gates out of line
''')
rep('''    if cells.get("receipt_runs") and cells.get("numbers_in") and not cells.get("numbers_out") and cells["shape_expected"] >= 0.7: return "completes", "receipt"   # the expected's shape and every value printed by the machine
    if cells.get("shape_gates") and cells["shape_expected"] >= 0.7 and cells["values_out"] >= 1 and len(cells["new_to_project"]) <= 1 and not cells.get("receipt_runs"): return "completes", "shape"   # the expected's shape plus a value out of line, no receipt to check it against
''', '''    if cells.get("receipt_runs") and cells.get("numbers_in") and not cells.get("numbers_out") and cells["shape_expected"] >= 0.7: return "completes", "receipt"   # the expected's shape and every value printed by the machine (a later print confirming an earlier claim counts)
    if cells.get("shape_gates") and cells["shape_expected"] >= 0.7 and cells["values_out"] >= 1 and len(cells["new_to_project"]) <= 1 and not rb: return "completes", "shape"   # the expected's shape plus a value out of line, no print older than the claim to check it against
''')
# 4. a refused part (the owner's rejection) never retires the part it would have superseded; the question needs two groundless words
rep('''    if kind == "supersedes" and cells.get("supersedes_run") and retire_part(name, n, cells["supersedes_run"], run, "superseded_by"): part += " | retired the part of run %d" % cells["supersedes_run"]
''', '''    if kind == "supersedes" and cells.get("supersedes_run") and not part.startswith("refused") and retire_part(name, n, cells["supersedes_run"], run, "superseded_by"): part += " | retired the part of run %d" % cells["supersedes_run"]
''')
rep('''    print("  ground: %s | receipts %d (%s) numbers in %s out %s" % (ground_str(cells.get("ground")), cells.get("receipt_runs", 0), ",".join(cells.get("receipt_cmds", [])) or "-", ",".join(cells.get("numbers_in", [])) or "-", ",".join(cells.get("numbers_out", [])) or "-"))
    if cells.get("ground", {}).get("none") and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, cells["ground"]["none"], vrun)
''', '''    print("  ground: %s | receipts %d (%s)%s numbers in %s out %s%s" % (ground_str(cells.get("ground")), cells.get("receipt_runs", 0), ",".join(cells.get("receipt_cmds", [])) or "-", "" if not cells.get("receipt_runs") or cells.get("receipt_before_claim") else " all newer than the claim: no print at its time", ",".join(cells.get("numbers_in", [])) or "-", ",".join(cells.get("numbers_out", [])) or "-", (" | newest print: " + cells["receipt_newest"]) if cells.get("receipt_newest") else ""))
    if len(cells.get("ground", {}).get("none", [])) >= 2 and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, cells["ground"]["none"], vrun)
''')
# 5. the hydration shows the newest prints
rep('''        qs = open_questions(name, nxt, 5)
''', '''        rc = receipts_of(name, nxt)
        if rc: lines.append("RECEIPTS (the machine's own prints for C%d, the newest of each command): " % nxt + " | ".join("%s => %s [%s]" % (cmd, " / ".join(l["t"][:70] for l in d.get("lines", [])[:3]), time.strftime("%m-%d %H:%M", time.localtime(d.get("ts", 0)))) for cmd, d in rc.items()))
        qs = open_questions(name, nxt, 5)
''')
open(p, "w").write(s); print("patched c16b")
