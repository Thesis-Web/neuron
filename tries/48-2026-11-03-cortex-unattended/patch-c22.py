# C22 receipt precision: a receipt judges only a claim that names its command or cites its values; a digit that is a command argument or sits in backticks is not a value; a cortex print of its own verdicts grounds no part by itself
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''    t = re.sub(r"\\b\\d{1,2}:\\d{2}(:\\d{2})?\\b|\\b\\d{4}-\\d{2}-\\d{2}\\b|\\b\\d{1,2}-\\d{2}\\b", " ", text.lower())
    return NUM.findall(t)
''', '''    t = re.sub(r"\\b\\d{1,2}:\\d{2}(:\\d{2})?\\b|\\b\\d{4}-\\d{2}-\\d{2}\\b|\\b\\d{1,2}-\\d{2}\\b", " ", text.lower())
    t = re.sub(r"`[^`]*`", " ", t); t = re.sub(r"--?[a-z][\\w-]*[ =]\\d+(\\.\\d+)?", " ", t)   # C22: a command in backticks or a flag's argument (--at 1, -m 300) is not a value
    return NUM.findall(t)
CMD_NOISE = set("ssh echo cat bash python3 hp2 tail head cut sed grep awk then done for do fi if else while read printf true false tee sort uniq wc tr xargs".split())
def toks(s):
    return set(w for w in re.findall(r"[a-z][a-z0-9_.-]*", s.lower()) if len(w) >= 2 and w not in STOP and w not in CMD_NOISE)
def is_self_print(cmd):
    return cmd.startswith("cortex ") or "/cortex " in cmd or cmd.startswith("cortex")
''')
rep('''    cells = {"receipt_runs": 0, "receipt_cmds": [], "receipt_before_claim": False, "receipt_newest": "", "numbers": numbers(text), "numbers_in": [], "numbers_out": [], "ground": {"receipt": 0, "owner": 0, "reference": 0, "memory": 0, "none": []}}
    rc = receipts_of(name, n); rnums, rwords, newest = set(), set(), 0
    for cmd, d in rc.items():
        cells["receipt_cmds"].append(cmd)
        for l in d.get("lines", []):
            cells["receipt_runs"] += 1; rnums |= set(numbers(receipt_line(l))); rwords |= set(g for g in content_gates(l["run"]) if not is_value(g)); newest = max(newest, l["run"])
    if cells["receipt_runs"]:
        cells["receipt_before_claim"] = newest < run   # a print the claim could have read; a later print is not evidence against an earlier claim, only a label
        cells["numbers_in"] = [t for t in cells["numbers"] if t in rnums]; cells["numbers_out"] = [t for t in cells["numbers"] if t not in rnums]
''', '''    cells = {"receipt_runs": 0, "receipt_cmds": [], "receipt_before_claim": False, "receipt_newest": "", "receipt_named": False, "numbers_in_ext": [], "numbers": numbers(text), "numbers_in": [], "numbers_out": [], "ground": {"receipt": 0, "owner": 0, "reference": 0, "memory": 0, "none": []}}
    rc = receipts_of(name, n); rnums, rnums_ext, rwords, newest = set(), set(), set(), 0; ct = toks(text)
    for cmd, d in rc.items():
        cells["receipt_cmds"].append(cmd)
        if toks(cmd) & ct: cells["receipt_named"] = True   # C22: the claim names this print's command
        for l in d.get("lines", []):
            cells["receipt_runs"] += 1; nn = set(numbers(receipt_line(l))); rnums |= nn
            if not is_self_print(cmd): rnums_ext |= nn   # a cortex print of its own verdicts and parts is circular ground for a sentence about them
            rwords |= set(g for g in content_gates(l["run"]) if not is_value(g)); newest = max(newest, l["run"])
    if cells["receipt_runs"]:
        cells["receipt_before_claim"] = newest < run   # a print the claim could have read; a later print is not evidence against an earlier claim, only a label
        cells["numbers_in"] = [t for t in cells["numbers"] if t in rnums]; cells["numbers_out"] = [t for t in cells["numbers"] if t not in rnums]
        cells["numbers_in_ext"] = [t for t in cells["numbers"] if t in rnums_ext]
''')
rep('''    if rb and cells.get("numbers_out") and (cells["ground"]["receipt"] >= 2 or cells.get("shape_expected", 0) >= 0.5): return "hallucination", "receipt"   # a value the machine never printed, said after the print
''', '''    about = cells.get("receipt_named") or cells.get("numbers_in_ext") or cells.get("shape_expected", 0) >= 0.5   # C22: the claim is about this print: names its command, cites its values, or states the expected
    if rb and cells.get("numbers_out") and about: return "hallucination", "receipt"   # a value the machine never printed, said after the print, by a claim about that print
''')
rep('''    if rb and cells.get("numbers_in") and not cells.get("numbers_out") and cells["ground"]["receipt"] >= 2: return "progresses", "receipt"   # every value printed by the machine and the receipt's own words, outside the expected's shape
''', '''    if rb and cells.get("numbers_in") and not cells.get("numbers_out") and cells["ground"]["receipt"] >= 2 and (cells.get("receipt_named") or cells.get("numbers_in_ext") or cells.get("shape_expected", 0) >= 0.3): return "progresses", "receipt"   # every value printed by the machine, by a claim about that print (C22: a cortex print of its own verdicts does not count)
''')
open(p, "w").write(s); print("patched c22")
