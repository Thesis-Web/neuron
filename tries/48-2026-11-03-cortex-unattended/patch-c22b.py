# C22b: a rounding of a printed value is not a value the machine never printed: 71 for 71.3, 1.2 million for 1200125; it is counted in and named as rounded
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''CMD_NOISE = set(''', '''SCALE = {"thousand": 1e3, "k": 1e3, "million": 1e6, "m": 1e6, "billion": 1e9}
def num_value(tok, text=""):
    m = re.match(r"^(\\d+(?:\\.\\d+)?)([a-z%]*)$", tok)
    if not m: return None, ""
    v, unit = float(m.group(1)), m.group(2)
    if text:
        mm = re.search(r"\\b" + re.escape(tok) + r"\\s+(thousand|million|billion)\\b", text.lower())
        if mm: v *= SCALE[mm.group(1)]; unit = ""
    return v, unit
def rounding_of(tok, printed, text=""):
    # the claim's number is a rounding of a printed one: same unit, within half a percent or within the last kept digit
    v, u = num_value(tok, text)
    if v is None: return None
    for pt in printed:
        w, pu = num_value(pt)
        if w is None or (u and pu and u != pu) or w == v: continue
        dec = len(tok.split(".")[1]) if "." in tok else 0
        if abs(w - v) <= max(abs(w) * 0.005, 0.5 * 10 ** (-dec)) : return pt
    return None
CMD_NOISE = set(''')
rep('''        cells["numbers_in"] = [t for t in cells["numbers"] if t in rnums]; cells["numbers_out"] = [t for t in cells["numbers"] if t not in rnums]
        cells["numbers_in_ext"] = [t for t in cells["numbers"] if t in rnums_ext]
''', '''        cells["numbers_in"] = [t for t in cells["numbers"] if t in rnums]; cells["numbers_out"] = [t for t in cells["numbers"] if t not in rnums]
        cells["numbers_in_ext"] = [t for t in cells["numbers"] if t in rnums_ext]
        cells["numbers_rounded"] = {}
        for t in list(cells["numbers_out"]):
            pt = rounding_of(t, rnums, text)
            if pt: cells["numbers_rounded"][t] = pt; cells["numbers_out"].remove(t); cells["numbers_in"].append(t); (cells["numbers_in_ext"].append(t) if rounding_of(t, rnums_ext, text) else None)   # C22b: a rounding is the printed value, said shorter
''')
rep('''",".join(cells.get("numbers_in", [])) or "-", ",".join(cells.get("numbers_out", [])) or "-", (" | newest print: " + cells["receipt_newest"]) if cells.get("receipt_newest") else ""))''', '''",".join(cells.get("numbers_in", [])) or "-", ",".join(cells.get("numbers_out", [])) or "-", ((" | rounded: " + ", ".join("%s for %s" % kv for kv in cells["numbers_rounded"].items())) if cells.get("numbers_rounded") else "") + ((" | newest print: " + cells["receipt_newest"]) if cells.get("receipt_newest") else "")))''')
open(p, "w").write(s); print("patched c22b")
