# C31 trust per voice per topic (the owner, 11-03 21:3x): the topic is the project first (its last record is source one, deterministic), then the words the claim touches, then the sources; the checkpoint is not a topic.
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''def tally_voice(voice, kind, by, guess):
    # C25 (the owner, 11-03 17:0x): inputs are measured; a fact proven false lowers that voice's trust, a labeled guess does not; the count is a keyed row per voice
    had = cx_get("voice", voice, 0); d = json.loads(had[3]) if had else {"claims": 0, "confirmed": 0, "false": 0, "guesses": 0, "first_ts": int(time.time())}
    d["claims"] += 1
    if guess: d["guesses"] += 1
    elif kind in ("hallucination", "invention") and by in ("receipt", "shape", "sources"): d["false"] += 1   # proven by the machine's print, the brain's shape or three sources, never by a model's word
    elif kind in ("completes", "progresses", "supersedes") and by in ("receipt", "shape"): d["confirmed"] += 1
    d["last_ts"] = int(time.time()); cx_put("voice", voice, 0, 0, clock(), json.dumps(d))
''', '''def outcome_of(kind, by, guess):
    if guess: return "guesses"
    if kind in ("hallucination", "invention") and by in ("receipt", "shape", "sources"): return "false"   # proven by the machine's print, the brain's shape or three sources, never by a model's word
    if kind in ("completes", "progresses", "supersedes") and by in ("receipt", "shape", "sources"): return "confirmed"
    return None
def tally_voice(voice, kind, by, guess, name=None, run=None):
    # C25 (the owner, 11-03 17:0x): inputs are measured; a fact proven false lowers that voice's trust, a labeled guess does not.
    # C31 (the owner, 11-03 21:3x): the topic is the project first, then the words the claim touches; the checkpoint is not a topic. One keyed row per voice, one per (voice, gate).
    had = cx_get("voice", voice, 0); d = json.loads(had[3]) if had else {"claims": 0, "confirmed": 0, "false": 0, "guesses": 0, "first_ts": int(time.time())}
    oc = outcome_of(kind, by, guess); d["claims"] += 1
    if oc: d[oc] += 1
    if name:
        bp = d.setdefault("by_project", {}).setdefault(name, {"claims": 0, "confirmed": 0, "false": 0, "guesses": 0}); bp["claims"] += 1
        if oc: bp[oc] += 1
    d["last_ts"] = int(time.time()); cx_put("voice", voice, 0, 0, clock(), json.dumps(d))
    if run and oc in ("confirmed", "false"):
        for g in set(x for x in content_gates(run) if not is_value(x)):
            hg = cx_get("vgate", voice, g); e = json.loads(hg[3]) if hg else {"confirmed": 0, "false": 0}
            e[oc] += 1; cx_put("vgate", voice, g, run, clock(), json.dumps(e))
def word_trust(voice, run):
    # the voice's record on the words this claim touches: confirmed and false over those gates, and the trust they give
    c = f = n = 0
    for g in set(x for x in content_gates(run) if not is_value(x)):
        hg = cx_get("vgate", voice, g)
        if hg: e = json.loads(hg[3]); c += e.get("confirmed", 0); f += e.get("false", 0); n += 1
    return {"gates": n, "confirmed": c, "false": f, "trust": round(c / (c + f), 2) if (c + f) else None}
def project_trust(voice, name):
    had = cx_get("voice", voice, 0)
    if not had: return None
    bp = (json.loads(had[3]).get("by_project") or {}).get(name)
    if not bp: return None
    t = bp["confirmed"] + bp["false"]
    return {"claims": bp["claims"], "confirmed": bp["confirmed"], "false": bp["false"], "trust": round(bp["confirmed"] / t, 2) if t else None}
''')
rep('''    tally_voice(iv.get("voice", "hand"), kind, by, bool(iv.get("guess")))
''', '''    tally_voice(iv.get("voice", "hand"), kind, by, bool(iv.get("guess")), name, run)
''')
# the belief row in the owner's order: the project's own record first, then the words the claim touches, then the sources
rep('''    print("  voice: %s%s" % (iv.get("voice", "hand"), " (a labeled guess)" if iv.get("guess") else ""))
''', '''    vc = iv.get("voice", "hand"); pt = project_trust(vc, name); wt = word_trust(vc, run)
    rec = "held before" if cells.get("same_as") or cells.get("echo") else ("supersedes run %s" % cells["supersedes_run"]) if cells.get("supersedes_run") else "new to the project record"
    print("  voice: %s%s | belief row: 1 the project record: %s; 2 the words: %s on %d gates (%d confirmed, %d false); 3 the sources: %d confirm, %d disagree, agreement %d of %d | this voice on %s: %s" % (vc, " (a labeled guess)" if iv.get("guess") else "", rec, ("trust %.2f" % wt["trust"]) if wt["trust"] is not None else "no record", wt["gates"], wt["confirmed"], wt["false"], len((cells.get("sources") or {}).get("confirm", [])), len((cells.get("sources") or {}).get("disagree", [])), len((cells.get("pair_ground") or {}).get("agree", [])), (cells.get("pair_ground") or {}).get("sources", 0), name, ("trust %.2f over %d claims" % (pt["trust"], pt["claims"])) if pt and pt["trust"] is not None else "no record yet"))
''')
# status: per project trust beside the voice
rep('''    if vs: print("voices: " + "; ".join("%s claims %d, confirmed %d, false %d, guesses %d, trust %s" % (vn, d["claims"], d["confirmed"], d["false"], d["guesses"], ("%.2f" % t) if t is not None else "none yet") for (vn, d, t) in vs) + " | proven by receipt or shape only; a labeled guess is not counted (C25)")
''', '''    if vs: print("voices: " + "; ".join("%s claims %d, confirmed %d, false %d, guesses %d, trust %s%s" % (vn, d["claims"], d["confirmed"], d["false"], d["guesses"], ("%.2f" % t) if t is not None else "none yet", (" [" + " ".join("%s %s" % (pj, ("%.2f" % (b["confirmed"] / (b["confirmed"] + b["false"]))) if (b["confirmed"] + b["false"]) else "-") for pj, b in sorted(d.get("by_project", {}).items())) + "]") if d.get("by_project") else "") for (vn, d, t) in vs) + " | proven by receipt, shape or sources only; a labeled guess is not counted; per project in brackets, per word on the verdict line (C25, C31)")
''')
open(p, "w").write(s); print("patched c31")
