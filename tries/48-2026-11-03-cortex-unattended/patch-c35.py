# C35 units are meaning, and a missing print is a question (the other claude, 11-04 00:4x: a sentence in my own words about a print scores false even when the fact is right; the owner: that is why the meaning gap is so huge):
# a number with a unit compares in a common unit (ms, s, min, h; b, kb, mb, gb); a claim naming a measure whose print is missing is unsettled and asks, never false; the capture keeps every print of the turn (forty at most), not the newest twelve
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
# 1. units
rep('''def num_value(tok, text=""):
    m = re.match(r"^(\\d+(?:\\.\\d+)?)([a-z%]*)$", tok)
    if not m: return None, "", 1.0
    v, unit, scale = float(m.group(1)), m.group(2), 1.0
    if text:
        mm = re.search(r"\\b" + re.escape(tok) + r"\\s+(thousand|million|billion)\\b", text.lower())
        if mm: scale = SCALE[mm.group(1)]; v *= scale; unit = ""
    return v, unit, scale
''', '''UNITS = {"ms": ("t", 1.0), "s": ("t", 1e3), "sec": ("t", 1e3), "secs": ("t", 1e3), "min": ("t", 6e4), "mins": ("t", 6e4), "h": ("t", 3.6e6), "hr": ("t", 3.6e6), "hrs": ("t", 3.6e6),
         "b": ("z", 1.0), "kb": ("z", 1e3), "k": ("z", 1e3), "mb": ("z", 1e6), "m": ("z", 1e6), "gb": ("z", 1e9), "g": ("z", 1e9), "tb": ("z", 1e12), "t": ("z", 1e12)}   # C35: a unit is meaning: the same quantity in another unit is the same value
def num_value(tok, text=""):
    m = re.match(r"^(\\d+(?:\\.\\d+)?)([a-z%]*)$", tok)
    if not m: return None, "", 1.0
    v, unit, scale = float(m.group(1)), m.group(2), 1.0
    if text:
        mm = re.search(r"\\b" + re.escape(tok) + r"\\s+(thousand|million|billion)\\b", text.lower())
        if mm: scale = SCALE[mm.group(1)]; v *= scale; unit = ""
        if not unit:
            mu = re.search(r"\\b" + re.escape(tok) + r"\\s*(ms|secs?|s|mins?|hrs?|h|kb|mb|gb|tb|b)\\b", text.lower())
            if mu: unit = mu.group(1)
    if unit in UNITS: kind, mult = UNITS[unit]; return v * mult, kind, scale * mult
    return v, unit, scale
''')
rep('''    for pt in printed:
        w, pu, _ = num_value(pt)
        if w is None or (u and pu and u != pu) or w == v: continue
        if len(pt.replace(".", "")) <= len(tok.replace(".", "")) and scale == 1.0: continue   # the print is not longer than the claim: not a rounding
        if abs(w - v) <= tol: return pt
    return None
''', '''    for pt in printed:
        w, pu, _ = num_value(pt, ptext.get(pt, "") if isinstance(ptext, dict) else "")
        if w is None or (u and pu and u != pu) or w == v: continue
        if len(pt.replace(".", "")) <= len(tok.replace(".", "")) and scale == 1.0: continue   # the print is not longer than the claim: not a rounding
        if abs(w - v) <= tol: return pt
    return None
def same_quantity(tok, printed, text, ptext):
    # C35: the claim's number equals a printed one once both carry their units (11.7 s is 11700 ms; 82 mb is a rounding of 82164 kb)
    v, u, _ = num_value(tok, text)
    if v is None or u not in ("t", "z"): return None
    for pt in printed:
        w, pu, _ = num_value(pt, ptext.get(pt, ""))
        if pu == u and w is not None and abs(w - v) <= 0.5 * (10 ** -(len(tok.split(".")[1]) if "." in tok else 0)) * (v / float(re.match(r"^(\\d+(?:\\.\\d+)?)", tok).group(1)) if float(re.match(r"^(\\d+(?:\\.\\d+)?)", tok).group(1)) else 1): return pt
    return None
''')
rep('''def rounding_of(tok, printed, text=""):''', '''def rounding_of(tok, printed, text="", ptext=None):''')
# the receipt lines keep their text beside each number, so a unit next to a printed number is seen
rep('''        for l in lines_older:
            nn = set(numbers(receipt_line(l), clock=is_clock)); rnums |= nn
''', '''        for l in lines_older:
            rl = receipt_line(l); nn = set(numbers(rl, clock=is_clock)); rnums |= nn
            for x in nn: ptext.setdefault(x, rl)
''')
rep('''    rc = receipts_of(name, n); rnums, rnums_ext, rwords, older = set(), set(), set(), 0; ct = toks(text)
''', '''    rc = receipts_of(name, n); rnums, rnums_ext, rwords, older = set(), set(), set(), 0; ct = toks(text); ptext = {}
''')
rep('''        cells["numbers_rounded"] = {}
        for t in list(cells["numbers_out"]):
            pt = rounding_of(t, rnums, text)
            if pt: cells["numbers_rounded"][t] = pt; cells["numbers_out"].remove(t); cells["numbers_in"].append(t); (cells["numbers_in_ext"].append(t) if rounding_of(t, rnums_ext, text) else None)   # C22b: a rounding is the printed value, said shorter
''', '''        cells["numbers_rounded"] = {}
        for t in list(cells["numbers_out"]):
            pt = rounding_of(t, rnums, text, ptext) or same_quantity(t, rnums, text, ptext)
            if pt: cells["numbers_rounded"][t] = pt; cells["numbers_out"].remove(t); cells["numbers_in"].append(t); (cells["numbers_in_ext"].append(t) if (rounding_of(t, rnums_ext, text, ptext) or same_quantity(t, rnums_ext, text, ptext)) else None)   # C22b, C35: a rounding or the same quantity in another unit is the printed value
''')
# 2. a missing print is a question, never a false
rep('''    about = cells.get("receipt_named") or cells.get("numbers_in_ext") or cells.get("shape_expected", 0) >= 0.5   # C22: the claim is about this print: names its command, cites its values, or states the expected
    if rb and cells.get("numbers_out") and about: return "hallucination", "receipt"   # a value the machine never printed, said after the print, by a claim about that print
''', '''    about = cells.get("receipt_named") or cells.get("numbers_in_ext") or cells.get("shape_expected", 0) >= 0.5   # C22: the claim is about this print: names its command, cites its values, or states the expected
    if rb and cells.get("numbers_out") and about and not cells.get("measure_missing"): return "hallucination", "receipt"   # a value the machine never printed, said after the print, by a claim about that print; C35: not when a print it names is missing, that is a question
''')
# 3. the capture keeps every print of the turn, forty at most; "time" and "free" leave the measures (too loose)
rep('''        for (cmd, txt) in results[-12:]:   # the newest twelve prints of the session, before its sentences, so a print precedes the claims that cite it''', '''        for (cmd, txt) in results[-40:]:   # the prints of the session, forty at most (C35: twelve cut the print a later sentence cited), before its sentences''')
rep('''        if nrec: print("receipts: %d lines typed from %d tool results for C%d" % (nrec, len(results[-12:]), nxt0))''', '''        if nrec: print("receipts: %d lines typed from %d tool results for C%d" % (nrec, len(results[-40:]), nxt0))''')
rep('''MEASURES_DEFAULT = {"clock": "date", "time": "date", "tonight": "date", "today": "date", "now": "date", "o'clock": "date",
                    "mem": "free -m", "memory": "free -m", "free": "free -m", "swap": "free -m",''', '''MEASURES_DEFAULT = {"clock": "date", "tonight": "date", "today": "date", "now": "date", "o'clock": "date",
                    "mem": "free -m", "memory": "free -m", "swap": "free -m",''')
open(p, "w").write(s); print("patched c35")
