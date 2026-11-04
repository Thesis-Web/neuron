# C32 the bands as numbers and the belief matrix (the owner, 11-03 21:5x): llm floor 0.20 ceiling 0.80; owner floor 0.50 ceiling 0.80; a reference alone 0.60, two sources agreeing 1.00;
# owner and a source agree = strong; llm and two sources = very strong; llm and owner with no source = 50/50; a voice climbs or falls inside its band; the machine's print is 1.00
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''def word_trust(voice, run):
''', '''BANDS_DEFAULT = {"llm": [0.2, 0.8], "owner": [0.5, 0.8], "reference_alone": 0.6, "reference_agree": 1.0, "owner_and_source": 0.85, "llm_and_two_sources": 0.95, "llm_and_owner": 0.5,
                 "note": "the owner, 2026-11-03 21:5x: llm ceiling 80 floor 20, turn dependent; owner ceiling .80 floor 50, informed guesses; reference 1.00 when true between sources, 60 alone; owner and source agree strong, llm and two sources very strong, llm and human without a source 50/50; the machine print is the ground"}
def bands():
    had = cx_get("bands", "judge", 0)
    if had:
        try: return json.loads(had[3])
        except ValueError: pass
    cx_put("bands", "judge", 0, 0, clock(), json.dumps(BANDS_DEFAULT)); return dict(BANDS_DEFAULT)
def belief_of(voice, name, kind, by, sc):
    # C32: the belief of a claim from who stands behind it: the machine's print, the sources agreeing, the owner, and the voice inside its band
    B = bands(); band = "owner" if voice == "owner" else "llm"; lo, hi = B[band]
    pt = project_trust(voice, name); had = cx_get("voice", voice, 0)
    obs = pt["trust"] if pt and pt["trust"] is not None else None
    if obs is None and had:
        d = json.loads(had[3]); t = d["confirmed"] + d["false"]; obs = (d["confirmed"] / t) if t else None
    banded = min(hi, max(lo, obs if obs is not None else (lo + hi) / 2))
    owner_srcs = set(nm for (nm, b) in sources() if b == "owner")
    conf = sc.get("confirm", []) if sc else []
    ref_conf = [x for x in conf if x not in owner_srcs]; owner_conf = any(x in owner_srcs for x in conf) or band == "owner"
    if by == "receipt" and kind in ("completes", "progresses", "supersedes"): return 1.0, "the machine's print"
    if len(ref_conf) >= 2: return (B["reference_agree"] if band == "owner" else B["llm_and_two_sources"]), "two sources agree"
    if len(ref_conf) == 1 and owner_conf: return B["owner_and_source"], "the owner and a source agree"
    if len(ref_conf) == 1: return B["reference_alone"], "a reference alone"
    if owner_conf and band == "llm": return B["llm_and_owner"], "llm and owner agree, no source"
    return round(banded, 2), "the voice alone, inside its band %.2f to %.2f" % (lo, hi)
def word_trust(voice, run):
''')
rep('''    vc = iv.get("voice", "hand"); pt = project_trust(vc, name); wt = word_trust(vc, run)
''', '''    vc = iv.get("voice", "hand"); pt = project_trust(vc, name); wt = word_trust(vc, run); bl, brule = belief_of(vc, name, kind, by, cells.get("sources") or {})
    print("  belief %.2f (%s)" % (bl, brule))
''')
# the part keeps the belief
rep('''    gr = dict(cells.get("ground") or {}); pg0 = cells.get("pair_ground") or {}
    if pg0.get("pairs"): gr["agree"] = len(pg0.get("agree", [])); gr["of"] = pg0.get("sources", 0)
''', '''    gr = dict(cells.get("ground") or {}); pg0 = cells.get("pair_ground") or {}
    if pg0.get("pairs"): gr["agree"] = len(pg0.get("agree", [])); gr["of"] = pg0.get("sources", 0)
    bl0, br0 = belief_of(iv0.get("voice", "hand") if (iv0 := (lambda rr: (json.loads(rr[0][0]) if rr and rr[0][0].startswith("{") else {}))(q("SELECT value FROM main.cx WHERE kind = 'ingest' AND name = ? AND run = ? AND n > 0", name, run))) else "hand", name, kind, by, cells.get("sources") or {}); gr["belief"] = bl0
''')
rep('''    if g.get("of"): items.append("agreement %d of %d" % (g.get("agree", 0), g["of"]))
''', '''    if g.get("of"): items.append("agreement %d of %d" % (g.get("agree", 0), g["of"]))
    if g.get("belief") is not None: items.append("belief %.2f" % g["belief"])
''')
# status prints the bands
rep('''    vs = voices()
    if vs: print("voices: "''', '''    B = bands(); print("bands: llm %.2f to %.2f, owner %.2f to %.2f, a reference alone %.2f, two sources %.2f; owner and source %.2f, llm and two sources %.2f, llm and owner %.2f (the owner, 11-03 21:5x; cx bands/judge)" % (B["llm"][0], B["llm"][1], B["owner"][0], B["owner"][1], B["reference_alone"], B["reference_agree"], B["owner_and_source"], B["llm_and_two_sources"], B["llm_and_owner"]))
    vs = voices()
    if vs: print("voices: "''')
open(p, "w").write(s); print("patched c32")
