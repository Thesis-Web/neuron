# C25 trust per voice: the ingest keeps its voice; per voice the claims proven false by receipt against the claims confirmed; a labeled guess is not counted; cortex status prints the voices
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''def v_ingest(name, text, quiet=False, repeat_to_kernel=True):
    ensure_cx(); out = []; t0 = time.time()
''', '''VOICE = ["hand"]   # who is speaking into the cortex: the hand (a builder's or the owner's ingest), or a session seen by the capture (hub:<session>)
GUESS = re.compile(r"\\b(i am guessing|i guess|my guess|a guess|guessing here|i think|maybe|perhaps|probably|not sure)\\b")
def v_ingest(name, text, quiet=False, repeat_to_kernel=True):
    ensure_cx(); out = []; t0 = time.time()
''')
rep('''        cx_put("ingest", name, k, run, at, json.dumps({"times": 1})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run); key_pairs(name, run)
''', '''        cx_put("ingest", name, k, run, at, json.dumps({"times": 1, "voice": VOICE[0], "guess": bool(GUESS.search(s))})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run); key_pairs(name, run)
''')
rep('''    cwd = cwd or hook.get("cwd")
    if not texts_all: print("capture: no assistant text in the tail"); return
''', '''    cwd = cwd or hook.get("cwd")
    VOICE[0] = "hub:" + ((hook.get("session_id") or "")[:8] or "unknown")   # C25: the voice of these sentences
    if not texts_all: print("capture: no assistant text in the tail"); return
''')
# the verdict keeps the voice and the guess mark; status prints trust per voice
rep('''    cx_put("verdict", name, run, vrun, at, json.dumps({"n": n, "run": run, "kind": kind, "p": p, "judge": judge, "answers": answers, "sheet": cells, "part": part}))
''', '''    irow = q("SELECT value FROM main.cx WHERE kind = 'ingest' AND name = ? AND run = ? AND n > 0", name, run); iv = {}
    try: iv = json.loads(irow[0][0]) if irow else {}
    except (ValueError, TypeError): iv = {}
    cx_put("verdict", name, run, vrun, at, json.dumps({"n": n, "run": run, "kind": kind, "p": p, "judge": judge, "answers": answers, "sheet": cells, "part": part, "voice": iv.get("voice", "hand"), "guess": bool(iv.get("guess"))}))
    tally_voice(iv.get("voice", "hand"), kind, by, bool(iv.get("guess")))
''')
rep('''NO_PARTS = set()''', '''def tally_voice(voice, kind, by, guess):
    # C25 (the owner, 11-03 17:0x): inputs are measured; a fact proven false lowers that voice's trust, a labeled guess does not; the count is a keyed row per voice
    had = cx_get("voice", voice, 0); d = json.loads(had[3]) if had else {"claims": 0, "confirmed": 0, "false": 0, "guesses": 0, "first_ts": int(time.time())}
    d["claims"] += 1
    if guess: d["guesses"] += 1
    elif kind in ("hallucination", "invention") and by in ("receipt", "shape"): d["false"] += 1   # proven by the machine's print or the brain's shape, never by a model's word
    elif kind in ("completes", "progresses", "supersedes") and by in ("receipt", "shape"): d["confirmed"] += 1
    d["last_ts"] = int(time.time()); cx_put("voice", voice, 0, 0, clock(), json.dumps(d))
def voices():
    out = []
    for (vn,) in q("SELECT name FROM main.cx WHERE kind = 'voice' AND name >= '' AND n = 0"):
        d = json.loads(cx_get("voice", vn, 0)[3]); tot = d["confirmed"] + d["false"]
        out.append((vn, d, (d["confirmed"] / tot) if tot else None))
    return out
NO_PARTS = set()''')
rep('''    print("captures: " + ("; ".join(caps) if caps else "none yet") + " | a stale time here is a failed or missing capture (C20)")
''', '''    print("captures: " + ("; ".join(caps) if caps else "none yet") + " | a stale time here is a failed or missing capture (C20)")
    vs = voices()
    if vs: print("voices: " + "; ".join("%s claims %d, confirmed %d, false %d, guesses %d, trust %s" % (vn, d["claims"], d["confirmed"], d["false"], d["guesses"], ("%.2f" % t) if t is not None else "none yet") for (vn, d, t) in vs) + " | proven by receipt or shape only; a labeled guess is not counted (C25)")
''')
open(p, "w").write(s); print("patched c25")
