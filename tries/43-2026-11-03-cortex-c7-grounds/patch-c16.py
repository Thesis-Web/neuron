# C16 (the owner, 11-03 13:3x): grounds for the judge: the receipt, the owner's words and reference material as sources; a gate with no ground is a question; every part carries its ground
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:80], s.count(old))
    s = s.replace(old, new)

# 1. the grounds, after key_gates
rep('''        else: cx_put("gate", name, g, run, clock(), json.dumps({"first": run, "times": 1, "last": run}))
''', '''        else: cx_put("gate", name, g, run, clock(), json.dumps({"first": run, "times": 1, "last": run}))
# ---- C16 (the owner, 11-03): the grounds. the receipt is the machine's own print piped in; the owner's words and reference material are sources, projects of typed lines;
#      every content gate of a claim is checked against them; a value is settled against the receipt; a gate with no ground is a question the cortex asks, not a guess ----
BANDS = ("owner", "reference")
NUM = re.compile(r"\\d[\\w.%]*")
def numbers(text):
    # the value tokens of a sentence (393g, 300, 9%); times and dates (13:19, 11-03) are not values
    return [t for t in NUM.findall(text.lower()) if ":" not in t and "-" not in t]
_SRC = []
def sources():
    if not _SRC:
        for (nm, v) in q("SELECT name, value FROM main.cx WHERE kind = 'source' AND n = 0 AND name >= ''"):
            try: _SRC.append((nm, json.loads(v).get("band", "reference")))
            except ValueError: pass
        _SRC.append(None)
    return [x for x in _SRC if x]
def receipts_of(name, n):
    had = cx_get("receipts", name, n)
    return json.loads(had[3]) if had else {}
def ground_cells(name, n, run, text, new_syms):
    # per word gate: which ground holds it (receipt, owner, reference, the project's own memory, none); per number: did the machine print it
    cells = {"receipt_runs": 0, "receipt_cmds": [], "numbers": numbers(text), "numbers_in": [], "numbers_out": [], "ground": {"receipt": 0, "owner": 0, "reference": 0, "memory": 0, "none": []}}
    rc = receipts_of(name, n); rnums, rwords = set(), set()
    for cmd, d in rc.items():
        cells["receipt_cmds"].append(cmd)
        for l in d.get("lines", []):
            cells["receipt_runs"] += 1; rnums |= set(numbers(l["t"])); rwords |= set(g for g in content_gates(l["run"]) if not is_value(g))
    if cells["receipt_runs"]:
        cells["numbers_in"] = [t for t in cells["numbers"] if t in rnums]; cells["numbers_out"] = [t for t in cells["numbers"] if t not in rnums]
    g = cells["ground"]; new = set(new_syms)
    for w in set(x for x in content_gates(run) if not is_value(x)):
        sym = sym_of(w); held = False
        if w in rwords: g["receipt"] += 1; held = True
        for (src, band) in sources():
            if band in BANDS and cx_get("gate", src, w): g[band] += 1; held = True
        if sym not in new: g["memory"] += 1; held = True
        if not held: g["none"].append(sym)
    g["none"] = sorted(set(g["none"]))
    return cells
def ground_str(g):
    if not g: return "no ground"
    items = ["%s %d" % (k, g[k]) for k in ("receipt", "owner", "reference", "memory") if g.get(k)]
    if g.get("none"): items.append("none: " + ",".join(g["none"]))
    return " ".join(items) or "no ground"
def v_receipt(name, n, cmd):
    # the machine's own print, piped in (df -h / | cortex receipt audit 1 df -h /): typed as receipt lines and kept as the checkpoint's ground; a model's hand never retypes it
    ensure_cx()
    if not cx_get("checkpoint", name, n): raise SystemExit("no such checkpoint: %s %d" % (name, n))
    lines = [clean(l) for l in sys.stdin.read().splitlines() if clean(l)]
    if not lines: raise SystemExit("receipt: nothing on stdin; pipe the command's output in")
    rc = receipts_of(name, n); got = []; t0 = time.time()
    for l in lines[:40]:
        body = "%s => %s" % (cmd, l)
        try: r = typed("cortex receipt %s %d : %s" % (name, n, body))
        except RuntimeError as e: print("receipt line refused: %s" % e); continue
        run = r["run"]; cx_put("receipt", name, text_key(body), run, clock(), json.dumps({"n": n, "cmd": cmd, "t": l, "ts": int(time.time())})); key_gates(name, run); got.append({"run": run, "t": l})
    rc[cmd] = {"ts": int(time.time()), "lines": got}   # the newest print of this command is the ground; older prints stay as typed lines in the brain
    cx_put("receipts", name, n, got[-1]["run"] if got else 0, clock(), json.dumps(rc))
    for x in got: print("receipt run %d %s C%d: %s => %s" % (x["run"], name, n, cmd, x["t"][:100]))
    print("receipt: %d lines typed in %.0f ms; %s C%d has receipts of: %s" % (len(got), (time.time() - t0) * 1000, name, n, ", ".join(sorted(rc))))
def v_source(name, band=None, text=None):
    # a source is a project of typed lines: cortex source <name> owner|reference : <what it is, where from, as of>; then cortex source <name> - types its lines from stdin (build time, no judge)
    ensure_cx()
    if band:
        if band not in BANDS: raise SystemExit("a source band is owner or reference (a receipt comes from cortex receipt)")
        run, at, _ = record("source", name, 0, "%s : %s" % (band, text)); cx_put("source", name, 0, run, at, json.dumps({"band": band, "text": text, "ts": int(time.time())}))
        print("source %s (%s) run %d: %s" % (name, band, run, text[:120])); return
    if not cx_get("source", name, 0): raise SystemExit("register the source first: cortex source %s owner|reference : <what it is, where from, as of>" % name)
    raw = sys.stdin.read(); t0 = time.time(); n_typed = dupes = noise = refused = 0
    for sent in sentences(raw):
        if is_noise(sent): noise += 1; continue
        k = text_key(sent)
        if cx_get("source", name, k): dupes += 1; continue
        try: r = typed("cortex source %s : %s" % (name, sent))
        except RuntimeError: refused += 1; continue
        run = r["run"]; cx_put("source", name, k, run, clock(), json.dumps({"t": sent[:300]})); key_gates(name, run); n_typed += 1
        if n_typed % 500 == 0: print("  %d typed, %.0f s" % (n_typed, time.time() - t0), flush=True)
    print("source %s: %d sentences typed, %d repeats, %d noise, %d refused, %.1f s" % (name, n_typed, dupes, noise, refused, time.time() - t0))
def ask_question(name, n, run, words, vrun):
    # the meaning question: the words of a claim that no receipt, owner line, reference or project line holds; asked once, recorded, answered by the owner (mark, accept, reject) or by a source
    if cx_get("question", name, run): return
    body = "C%d run %d: %s" % (n, run, ", ".join(words))
    try: qrun = typed("cortex question %s %d : %s" % (name, n, body))["run"]
    except RuntimeError: qrun = 0
    cx_put("question", name, run, qrun, clock(), json.dumps({"n": n, "words": words, "ts": int(time.time()), "verdict_run": vrun, "answered": None}))
    print("  question asked, no ground for: %s | answer: cortex mark %s %d <kind>, accept or reject it, or type a source that holds the words" % (", ".join(words), name, run))
def answer_question(name, run, how):
    had = cx_get("question", name, run)
    if not had: return
    d = json.loads(had[3])
    if d.get("answered"): return
    d["answered"] = how; d["answered_ts"] = int(time.time()); cx_put("question", name, run, had[0], had[1], json.dumps(d))
def open_questions(name, n=None, limit=20):
    out = []
    for (run, v) in q("SELECT n, value FROM main.cx WHERE kind = 'question' AND name = ? AND n > 0 ORDER BY n DESC LIMIT 300", name):
        d = json.loads(v)
        if d.get("answered") or (n is not None and d.get("n") != n): continue
        d["run"] = run; out.append(d)
    return out[:limit]
def v_questions(name, n=None):
    ensure_cx(); qs = open_questions(name, n, 300)
    for d in qs: print("C%s run %d (%s): %s" % (d["n"], d["run"], time.strftime("%m-%d %H:%M", time.localtime(d["ts"])), ", ".join(d["words"])))
    print("%d open questions of %s%s. answer: cortex mark %s <run> <kind> [: why] | cortex accept|reject %s <n> <run> | cortex source <src> - with text that holds the words" % (len(qs), name, (" at C%d" % n) if n is not None else "", name, name))
''')

# 2. the ground cells on the sheet
rep('''    cells.update(shape_cells(name, n, run, pr, ck, ex, parts))
    return cells
''', '''    cells.update(shape_cells(name, n, run, pr, ck, ex, parts))
    cells.update(ground_cells(name, n, run, text, cells["new_to_project"]))
    return cells
''')

# 3. the formula: the receipt settles values; the shape no longer settles a value where a receipt exists
rep('''    if cells.get("echo"): return "dupe", "shape"                                      # the expected sentence's own shape with nothing out of line: words, no observation
    if cells.get("supersedes_run"): return "supersedes", "shape"                      # the same shape as an accepted part, only value or time gates out of line
''', '''    if cells.get("echo"): return "dupe", "shape"                                      # the expected sentence's own shape with nothing out of line: words, no observation
    if cells.get("receipt_runs") and cells.get("numbers_out") and cells.get("shape_expected", 0) >= 0.5: return "hallucination", "receipt"   # a value the machine never printed
    if cells.get("supersedes_run"): return "supersedes", ("receipt" if cells.get("receipt_runs") and cells.get("numbers_in") else "shape")   # the same shape as an accepted part, only value or time gates out of line
''')
rep('''    if cells.get("shape_gates") and cells["shape_expected"] >= 0.7 and cells["values_out"] >= 1 and len(cells["new_to_project"]) <= 1: return "completes", "shape"   # the expected's shape plus a value out of line
''', '''    if cells.get("receipt_runs") and cells.get("numbers_in") and not cells.get("numbers_out") and cells["shape_expected"] >= 0.7: return "completes", "receipt"   # the expected's shape and every value printed by the machine
    if cells.get("shape_gates") and cells["shape_expected"] >= 0.7 and cells["values_out"] >= 1 and len(cells["new_to_project"]) <= 1 and not cells.get("receipt_runs"): return "completes", "shape"   # the expected's shape plus a value out of line, no receipt to check it against
''')

# 4. the verdict: p, the part's ground, the state move by receipt, the question
rep('''    elif by == "shape": p = cells["shape_expected"] if kind == "completes" else 1.0
''', '''    elif by in ("shape", "receipt"): p = cells["shape_expected"] if kind == "completes" else 1.0
''')
rep('''    part = add_part(name, n, run, text, p, judge) if accepting else ("rejected" if retire_part(name, n, run, vrun, "rejected_by") else "")
''', '''    part = add_part(name, n, run, text, p, judge, cells.get("ground")) if accepting else ("rejected" if retire_part(name, n, run, vrun, "rejected_by") else "")
''')
rep('''    if kind == "completes" and p >= THRESH and by != "shape": moved = " | a judgment cell's completes does not move the state: the shape or the owner's accept does"
    if kind == "completes" and p >= THRESH and by == "shape":
''', '''    if kind == "completes" and p >= THRESH and by not in ("shape", "receipt"): moved = " | a judgment cell's completes does not move the state: the receipt, the shape or the owner's accept does"
    if kind == "completes" and p >= THRESH and by in ("shape", "receipt"):
''')
rep('''    cx_put("verdict", name, run, vrun, at, json.dumps({"n": n, "run": run, "kind": kind, "p": p, "judge": judge, "answers": answers, "sheet": cells, "part": part, "text": text[:300]}))
    geo = cells["geometry"]
''', '''    cx_put("verdict", name, run, vrun, at, json.dumps({"n": n, "run": run, "kind": kind, "p": p, "judge": judge, "answers": answers, "sheet": cells, "part": part, "text": text[:300]}))
    geo = cells["geometry"]
    print("  ground: %s | receipts %d (%s) numbers in %s out %s" % (ground_str(cells.get("ground")), cells.get("receipt_runs", 0), ",".join(cells.get("receipt_cmds", [])) or "-", ",".join(cells.get("numbers_in", [])) or "-", ",".join(cells.get("numbers_out", [])) or "-"))
    if cells.get("ground", {}).get("none") and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, cells["ground"]["none"], vrun)
''')

# 5. parts carry their ground; the hydration prints it and the open questions
rep('''def add_part(name, n, run, text, p=None, by=None):
''', '''def add_part(name, n, run, text, p=None, by=None, ground=None):
''')
rep('''    cx_put("part", name, k, run, clock(), json.dumps({"t": text, "n": n, "run": run, "times": 1, "p": p, "by": by, "ts": int(time.time())})); return "added"
''', '''    cx_put("part", name, k, run, clock(), json.dumps({"t": text, "n": n, "run": run, "times": 1, "p": p, "by": by, "ground": ground, "ts": int(time.time())})); return "added"
''')
rep('''        if ps: lines.append("ACCEPTED SO FAR (parts of C%d's state, each with its time and confidence): " % nxt + " | ".join("%s [%s%s]" % (p["t"][:90], time.strftime("%m-%d %H:%M", time.localtime(p.get("ts") or 0)), (" p%.2f %s" % (p["p"], p.get("by") or "")) if p.get("p") is not None else "") for p in reversed(ps)))
''', '''        if ps: lines.append("ACCEPTED SO FAR (parts of C%d's state, each with its time, confidence and ground): " % nxt + " | ".join("%s [%s%s | %s]" % (p["t"][:90], time.strftime("%m-%d %H:%M", time.localtime(p.get("ts") or 0)), (" p%.2f %s" % (p["p"], p.get("by") or "")) if p.get("p") is not None else "", ("the owner's word" if p.get("by") == "owner" or (p.get("by") is None and p.get("p") is None) else ground_str(p.get("ground")))) for p in reversed(ps)))
        qs = open_questions(name, nxt, 5)
        if qs: lines.append("OPEN QUESTIONS (words of C%d's claims that no receipt, owner line or reference holds; the owner answers them, a worker never guesses them): " % nxt + "; ".join("run %d: %s" % (d["run"], ", ".join(d["words"])) for d in qs))
''')

# 6. the owner's word answers a question
rep('''    text = ingest_text(rows[0][0])[0]; r = add_part(name, n, run, text); print("part %s for %s C%d from run %d: %s" % (r, name, n, run, text[:90]))
''', '''    text = ingest_text(rows[0][0])[0]; r = add_part(name, n, run, text, None, "owner"); answer_question(name, run, "accept"); print("part %s for %s C%d from run %d: %s" % (r, name, n, run, text[:90]))
''')
rep('''    if retire_part(name, n, run, "owner", "rejected_by"): print("part of run %d rejected from %s C%d by the owner" % (run, name, n))
    else: raise SystemExit("no part of run %s in %s C%d" % (run, name, n))
''', '''    answer_question(name, run, "reject")
    if retire_part(name, n, run, "owner", "rejected_by"): print("part of run %d rejected from %s C%d by the owner" % (run, name, n))
    else: raise SystemExit("no part of run %s in %s C%d" % (run, name, n))
''')
rep('''    n = json.loads(v[3]).get("n"); cx_put("mark", name, run, run, clock(), json.dumps({"kind": kind, "n": n, "why": why, "ts": int(time.time())}))
''', '''    n = json.loads(v[3]).get("n"); cx_put("mark", name, run, run, clock(), json.dumps({"kind": kind, "n": n, "why": why, "ts": int(time.time())})); answer_question(name, run, "mark:" + kind)
''')

# 7. verdicts list: the ground column; status: the judge order; usage; dispatch
rep('''    print("%-7s %-4s %-13s %-5s %-22s %-11s %-12s %-12s %s" % ("run", "C", "verdict", "p", "judge", "when", "part", "mark", "sentence"))
''', '''    print("%-7s %-4s %-13s %-5s %-22s %-11s %-12s %-12s %-24s %s" % ("run", "C", "verdict", "p", "judge", "when", "part", "mark", "ground", "sentence"))
''')
rep('''        print("%-7d C%-3s %-13s %-5.2f %-22s %-11s %-12s %-12s %s" % (run, d.get("n"), d.get("kind"), d.get("p") or 0, (d.get("judge") or "")[:22], time.strftime("%m-%d %H:%M", time.localtime(ts)), st, mk, (d.get("text") or "")[:90]))
''', '''        print("%-7d C%-3s %-13s %-5.2f %-22s %-11s %-12s %-12s %-24s %s" % (run, d.get("n"), d.get("kind"), d.get("p") or 0, (d.get("judge") or "")[:22], time.strftime("%m-%d %H:%M", time.localtime(ts)), st, mk, ground_str((d.get("sheet") or {}).get("ground"))[:24] if (d.get("sheet") or {}).get("ground") else "(judged before c16)", (d.get("text") or "")[:90]))
''')
rep('''judge: shape, learned v%s, then %s | index rows %d" % (''', '''judge: receipt, shape, learned v%s, then %s | index rows %d" % (''')
rep('''  verdicts <name> [n] [--limit k]          every judged line of the project (or of checkpoint n), newest first: run, verdict, p, judge, when, part, mark, sentence
''', '''  verdicts <name> [n] [--limit k]          every judged line of the project (or of checkpoint n), newest first: run, verdict, p, judge, when, part, mark, ground, sentence
  receipt <name> <n> <command ...>         the machine's own print on stdin (df -h / | cortex receipt audit 1 df -h /): the checkpoint's ground for values
  source <name> owner|reference : <text>   register a source (the owner's words, a textbook, code docs; say where from and as of); then
  source <name> -                          type the source's sentences from stdin (build time, no judge); a claim's words are then checked against it
  questions <name> [n]                     the open meaning questions: words of judged claims that no receipt, owner line or reference holds
''')
rep('''    elif v == "status": v_status(a[0] if a else None)
''', '''    elif v == "receipt": v_receipt(a[0], int(a[1]), " ".join(a[2:]))
    elif v == "source":
        if len(a) >= 2 and a[1] == "-": v_source(a[0])
        else:
            s2 = " ".join(a); k2, t2 = split_colon(a); v_source(k2[0], k2[1] if len(k2) > 1 else None, t2)
    elif v == "questions": v_questions(a[0], int(a[1]) if len(a) > 1 else None)
    elif v == "status": v_status(a[0] if a else None)
''')
open(p, "w").write(s); print("patched c16")
