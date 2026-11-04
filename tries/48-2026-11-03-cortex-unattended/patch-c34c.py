# a rounding is a shorter form of the printed number: within half a unit of the claim's last kept digit, at the claim's scale; 392 is not a rounding of 393. Clock tokens count in the restate key.
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''def num_value(tok, text=""):
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
''', '''def num_value(tok, text=""):
    m = re.match(r"^(\\d+(?:\\.\\d+)?)([a-z%]*)$", tok)
    if not m: return None, "", 1.0
    v, unit, scale = float(m.group(1)), m.group(2), 1.0
    if text:
        mm = re.search(r"\\b" + re.escape(tok) + r"\\s+(thousand|million|billion)\\b", text.lower())
        if mm: scale = SCALE[mm.group(1)]; v *= scale; unit = ""
    return v, unit, scale
def rounding_of(tok, printed, text=""):
    # the claim's number is a shorter form of a printed one: same unit, fewer kept digits, within half a unit of the last kept digit at the claim's scale (71 for 71.3, 1.8 million for 1796202; 392 is not a rounding of 393)
    v, u, scale = num_value(tok, text)
    if v is None: return None
    dec = len(tok.split(".")[1]) if "." in tok else 0; tol = 0.5 * scale * 10 ** (-dec)
    for pt in printed:
        w, pu, _ = num_value(pt)
        if w is None or (u and pu and u != pu) or w == v: continue
        if len(pt.replace(".", "")) <= len(tok.replace(".", "")) and scale == 1.0: continue   # the print is not longer than the claim: not a rounding
        if abs(w - v) <= tol: return pt
    return None
''')
rep('''def wordset_key(s):
    return int(hashlib.sha256(" ".join(sorted(content_words(s) | set(numbers(s)))).encode()).hexdigest()[:15], 16)
''', '''def wordset_key(s):
    return int(hashlib.sha256(" ".join(sorted(content_words(s) | set(numbers(s, clock=True)))).encode()).hexdigest()[:15], 16)
''')
open(p, "w").write(s); print("patched c34c")
