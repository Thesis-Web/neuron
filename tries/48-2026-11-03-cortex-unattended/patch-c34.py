# C34 (the owner, 11-03 23:3x: if date and today had actions, meaning, then this would be possible): a word that names a measure points at the print that settles it;
# a time is a value when the measure is a clock; a claim naming a measure with no print of it asks for the print. And two tokenizer faults the hp builder's prose exposed: "tries/51." and "2,188".
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
# 1. tokens: a trailing period or comma is punctuation; a thousands separator is not a break
rep('''def numbers(text):
    # the value tokens of a sentence (393g, 300, 9%); times and dates (13:19, 11-03) are not values
    t = re.sub(r"\\b\\d{1,2}:\\d{2}(:\\d{2})?\\b|\\b\\d{4}-\\d{2}-\\d{2}\\b|\\b\\d{1,2}-\\d{2}\\b", " ", text.lower())
''', '''def numbers(text, clock=False):
    # the value tokens of a sentence (393g, 300, 9%); times and dates (13:19, 11-03) are not values unless the claim is about a clock (C34)
    t = text.lower()
    t = re.sub(r"(?<=\\d),(?=\\d{3}\\b)", "", t)   # 2,188 is one number
    if not clock: t = re.sub(r"\\b\\d{1,2}:\\d{2}(:\\d{2})?\\b|\\b\\d{4}-\\d{2}-\\d{2}\\b|\\b\\d{1,2}-\\d{2}\\b", " ", t)
    else: t = re.sub(r"\\b(\\d{1,2}):(\\d{2})(?::\\d{2})?\\b", lambda m: " %s:%s " % (m.group(1), m.group(2)), t)
''')
rep('''    t = re.sub(r"`[^`]*`", " ", t); t = re.sub(r"--?[a-z][\\w-]*[ =]\\d+(\\.\\d+)?", " ", t)   # C22: a command in backticks or a flag's argument (--at 1, -m 300) is not a value
    return NUM.findall(t)
''', '''    t = re.sub(r"`[^`]*`", " ", t); t = re.sub(r"--?[a-z][\\w-]*[ =]\\d+(\\.\\d+)?", " ", t)   # C22: a command in backticks or a flag's argument (--at 1, -m 300) is not a value
    return [x.rstrip(".,;:") for x in (NUM_CLOCK if clock else NUM).findall(t) if x.rstrip(".,;:")]
NUM_CLOCK = re.compile(r"(?<![\\w.])\\d[\\w.%:]*")
''')
# 2. measures: a word that names a measure points at the print that settles it (data in the index, the defaults below)
rep('''def receipts_of(name, n):
''', '''MEASURES_DEFAULT = {"clock": "date", "time": "date", "tonight": "date", "today": "date", "now": "date", "o'clock": "date",
                    "mem": "free -m", "memory": "free -m", "free": "free -m", "swap": "free -m",
                    "disk": "df -h /", "avail": "df -h /", "filesystem": "df -h /", "df": "df -h /",
                    "load": "uptime", "uptime": "uptime",
                    "gates": "cortex status", "runs": "cortex status", "hops": "cortex status", "checkpoints": "cortex formula", "ingests": "cortex formula", "verdicts": "cortex formula", "voices": "cortex status", "trust": "cortex status"}
def measures():
    had = cx_get("measures", "judge", 0)
    if had:
        try: return json.loads(had[3])
        except ValueError: pass
    cx_put("measures", "judge", 0, 0, clock(), json.dumps(MEASURES_DEFAULT)); return dict(MEASURES_DEFAULT)
def measure_of(text):
    # C34: the words of a claim that name a measure, and the prints that settle them (the owner: if date and today had actions, meaning, this would be possible)
    M = measures(); ws = set(re.findall(r"[a-z][a-z']+", text.lower())); hit = {}
    for w in ws:
        if w in M: hit.setdefault(M[w], []).append(w)
    return hit
def receipts_of(name, n):
''')
# 3. the ground cells: times are values when the measure is a clock; a named measure with no older print asks for it
rep('''    cells = {"receipt_runs": 0, "receipt_cmds": [], "receipt_before_claim": False, "receipt_newest": "", "receipt_named": False, "numbers_in_ext": [], "numbers": numbers(text), "numbers_in": [], "numbers_out": [], "ground": {"receipt": 0, "owner": 0, "reference": 0, "memory": 0, "none": []}}
''', '''    meas = measure_of(text); is_clock = "date" in meas
    cells = {"receipt_runs": 0, "receipt_cmds": [], "receipt_before_claim": False, "receipt_newest": "", "receipt_named": False, "numbers_in_ext": [], "numbers": numbers(text, clock=is_clock), "numbers_in": [], "numbers_out": [], "measures": meas, "measure_missing": [], "ground": {"receipt": 0, "owner": 0, "reference": 0, "memory": 0, "none": []}}
''')
rep('''        for l in lines_older:
            nn = set(numbers(receipt_line(l))); rnums |= nn
''', '''        for l in lines_older:
            nn = set(numbers(receipt_line(l), clock=is_clock)); rnums |= nn
''')
rep('''    if cells["receipt_runs"]:
        cells["receipt_before_claim"] = older > 0   # at least one print the claim could have read
''', '''    if meas:
        have = set(toks(cmd0) for cmd0 in rc.keys()); cells["measure_missing"] = sorted(m0 for m0 in meas if not any(toks(m0) & toks(c0) for c0 in rc.keys()))
        if cells["measure_missing"]: pass
    if cells["receipt_runs"]:
        cells["receipt_before_claim"] = older > 0   # at least one print the claim could have read
''')
# a claim that names a measure also names the print, for the C22 rule
rep('''        if lines_older and (toks(cmd) & ct): cells["receipt_named"] = True   # C22: the claim names this print's command
''', '''        if lines_older and ((toks(cmd) & ct) or any(toks(cmd) & toks(m0) for m0 in meas)): cells["receipt_named"] = True   # C22: the claim names this print's command, or a measure that print settles (C34)
''')
# 4. the verdict asks for the missing print
rep('''    pg = cells.get("pair_ground") or {}
    if pg.get("pairs"):''', '''    if cells.get("measure_missing") and kind not in ("noise", "dupe") and (name, n) not in NO_PARTS:
        print("  no print to check this: it names %s, settled by %s; ask for that print (C34)" % (", ".join(w for m0 in cells["measure_missing"] for w in cells["measures"][m0]), ", ".join(cells["measure_missing"])))
        ask_question(name, n, run, ["no print of %s for a claim about %s" % (m0, ", ".join(cells["measures"][m0])) for m0 in cells["measure_missing"]], vrun)
    pg = cells.get("pair_ground") or {}
    if pg.get("pairs"):''')
open(p, "w").write(s); print("patched c34")
