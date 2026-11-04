# C35b: a missing print excuses only the numbers that sit beside the missing measure's word; a present print judges its own numbers. "now" leaves the clock measure.
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''MEASURES_DEFAULT = {"clock": "date", "tonight": "date", "today": "date", "now": "date", "o'clock": "date",''', '''MEASURES_DEFAULT = {"clock": "date", "tonight": "date", "today": "date", "o'clock": "date",''')
rep('''    if meas: cells["measure_missing"] = sorted(m0 for m0 in meas if not any(toks(m0) & toks(c0) for c0 in rc.keys()))   # the measures named with no print of them on this checkpoint
''', '''    if meas:
        cells["measure_missing"] = sorted(m0 for m0 in meas if not any(toks(m0) & toks(c0) for c0 in rc.keys()))   # the measures named with no print of them on this checkpoint
        if cells["measure_missing"] and cells.get("numbers_out"):
            mw = set(w for m0 in cells["measure_missing"] for w in meas[m0]); low = text.lower(); unchecked = []
            for t0 in list(cells["numbers_out"]):
                i = low.find(t0)
                before = set(re.findall(r"[a-z][a-z']+", low[max(0, i - 40):i])) if i >= 0 else set()
                if before & mw: unchecked.append(t0); cells["numbers_out"].remove(t0)   # C35b: this number belongs to the missing print; it is unchecked, not false
            cells["numbers_unchecked"] = unchecked
''')
rep('''    if rb and cells.get("numbers_out") and about and not cells.get("measure_missing"): return "hallucination", "receipt"   # a value the machine never printed, said after the print, by a claim about that print; C35: not when a print it names is missing, that is a question
''', '''    if rb and cells.get("numbers_out") and about: return "hallucination", "receipt"   # a value the machine never printed, said after the print, by a claim about that print (C35b: a number beside a missing measure's word was set aside as unchecked)
''')
open(p, "w").write(s); print("patched c35b")
