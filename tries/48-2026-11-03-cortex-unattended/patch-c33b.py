# a receipt judges a claim only if that receipt line is older than the claim; a later receipt on the same checkpoint must not switch the older ones off
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''    rc = receipts_of(name, n); rnums, rnums_ext, rwords, newest = set(), set(), set(), 0; ct = toks(text)
    for cmd, d in rc.items():
        cells["receipt_cmds"].append(cmd)
        if toks(cmd) & ct: cells["receipt_named"] = True   # C22: the claim names this print's command
        for l in d.get("lines", []):
            cells["receipt_runs"] += 1; nn = set(numbers(receipt_line(l))); rnums |= nn
            if not is_self_print(cmd): rnums_ext |= nn   # a cortex print of its own verdicts and parts is circular ground for a sentence about them
            rwords |= set(g for g in content_gates(l["run"]) if not is_value(g)); newest = max(newest, l["run"])
    if cells["receipt_runs"]:
        cells["receipt_before_claim"] = newest < run   # a print the claim could have read; a later print is not evidence against an earlier claim, only a label
''', '''    rc = receipts_of(name, n); rnums, rnums_ext, rwords, older = set(), set(), set(), 0; ct = toks(text)
    for cmd, d in rc.items():
        cells["receipt_cmds"].append(cmd)
        lines_older = [l for l in d.get("lines", []) if l["run"] < run]   # C33b: only a print older than the claim judges it; a later print on the same checkpoint is a label, never a switch
        if lines_older and (toks(cmd) & ct): cells["receipt_named"] = True   # C22: the claim names this print's command
        cells["receipt_runs"] += len(d.get("lines", [])); older += len(lines_older)
        for l in lines_older:
            nn = set(numbers(receipt_line(l))); rnums |= nn
            if not is_self_print(cmd): rnums_ext |= nn   # a cortex print of its own verdicts and parts is circular ground for a sentence about them
            rwords |= set(g for g in content_gates(l["run"]) if not is_value(g))
    if cells["receipt_runs"]:
        cells["receipt_before_claim"] = older > 0   # at least one print the claim could have read
''')
open(p, "w").write(s); print("patched c33b")
