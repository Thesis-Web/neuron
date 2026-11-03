# patch-c15.py: cortex C15, the judge's key and our own judge. Exact anchors; nothing written unless every anchor is found.
import sys, re
P = "/home/james/cortex/cortex.py"; src = open(P).read(); orig = src
def rep(old, new, count=1):
    global src
    assert src.count(old) == count, "anchor not unique/found (%d): %r" % (src.count(old), old[:90])
    src = src.replace(old, new)
def region(start, end, new):
    global src
    i = src.index(start); j = src.index(end, i); src = src[:i] + new.rstrip("\n") + src[j:]

rep("import socket, json, sys, os, re, time, hashlib, subprocess, shutil, urllib.request, urllib.error",
    "import socket, json, sys, os, re, time, hashlib, subprocess, shutil, urllib.request, urllib.error, math, difflib")

SHAPE = r'''
# ---- the shape (the owner, 2026-11-03): an ingest is a run; its gates in order are its shape; the project rides in the shape; a number is its digit
#      gates; prior state against new ingest is two shapes compared, keyed by run; what is out of line is the judge's question ----
_SHAPE, _SYM, _COLON = {}, {}, []
def shape_of(run):
    if run not in _SHAPE: _SHAPE[run] = [g for (g,) in q("SELECT gate FROM main.seq WHERE run = ? ORDER BY pos", run)]
    return _SHAPE[run]
def sym_of(g):
    if g not in _SYM:
        rows = q("SELECT symbol FROM main.label WHERE gate = ?", g); _SYM[g] = rows[0][0] if rows else ""
    return _SYM[g]
def content_gates(run):
    # the gates after the line's prefix (cortex <kind> <name> [n] :) that carry content, in order: words not in STOP, and digits (value gates)
    if not _COLON: _COLON.append(gate_of(":"))
    gs = shape_of(run); i = gs.index(_COLON[0]) + 1 if _COLON[0] in gs else 0
    out = []
    for g in gs[i:]:
        s = sym_of(g)
        if s and (s.isdigit() or (len(s) >= 2 and s not in STOP and any(c.isalpha() for c in s))): out.append(g)
    return out
def is_value(g): return sym_of(g).isdigit()
def seq_diff(a, b):
    # the gates out of line between two shapes: replaced, inserted or deleted in the alignment of the two gate lists
    oa, ob = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal": oa += a[i1:i2]; ob += b[j1:j2]
    return oa, ob
TIME_WORDS = set("again now then later today tonight yesterday am pm".split())
def shape_cells(name, n, run, pr, ck, ex, parts):
    ing = content_gates(run)
    cells = {"shape_gates": len(ing), "shape_values": sum(1 for g in ing if is_value(g)), "shape_expected": 0.0, "shape_shared_project": 0, "values_out": 0, "words_out": [], "echo": False, "new_to_project": [], "supersedes_run": 0, "same_as": 0}
    if not ing: return cells
    rr = run_row(run); cells["same_as"] = (rr[1] or 0) if rr else 0
    words = set(g for g in ing if not is_value(g))
    proj = set()
    for row in (pr, ck, ex):
        if row: proj |= set(g for g in content_gates(row[0]) if not is_value(g))
    cells["shape_shared_project"] = len(words & proj)
    if ex:
        E = content_gates(ex[0]); Es = set(E)
        if Es:
            cells["shape_expected"] = round(len(set(ing) & Es) / len(Es), 3)
            _, out = seq_diff(E, ing)
            cells["values_out"] = sum(1 for g in out if is_value(g))
            cells["words_out"] = sorted(set(sym_of(g) for g in out if not is_value(g)))
            cells["echo"] = (not out) and cells["shape_expected"] >= 0.9
    new = []
    for g in words:
        k = cx_get("gate", name, g)
        if not k or int(json.loads(k[3]).get("first", run)) >= run: new.append(sym_of(g))
    cells["new_to_project"] = sorted(new)
    for p in parts:
        if not p.get("run") or p["run"] >= run: continue          # a shape supersedes only an older part
        P = content_gates(p["run"])
        if not P: continue
        oa, ob = seq_diff(P, ing); diff = oa + ob
        if diff and any(is_value(g) for g in diff) and all(is_value(g) or sym_of(g) in TIME_WORDS for g in diff): cells["supersedes_run"] = p["run"]; break
    return cells
def key_gates(name, run):
    # the (project, gate) key: the first run of this project that crossed the gate and how many times since (the owner: the project's metadata on the gate)
    for g in set(content_gates(run)):
        had = cx_get("gate", name, g)
        if had:
            d = json.loads(had[3]); d["times"] = d.get("times", 1) + 1; d["last"] = run; cx_put("gate", name, g, had[0], had[1], json.dumps(d))
        else: cx_put("gate", name, g, run, clock(), json.dumps({"first": run, "times": 1, "last": run}))
'''
rep('CLAUDE_BIN = shutil.which("claude")', SHAPE.lstrip("\n") + 'CLAUDE_BIN = shutil.which("claude")')

LEARN = r'''
# ---- our own judge (the owner, 11-03): not a language model; a few learned weights over the sheet's cells answering the seven questions as probabilities;
#      the marks are the labeled set (the owner is the checker); training is build time, an answer is a dot product ----
FEATS = ("words", "shared_scope", "shared_checkpoint", "shared_expected", "new_words", "known_words", "coverage_expected", "observed", "mark_met", "times", "shape_gates", "shape_expected", "shape_shared_project", "values_out", "n_words_out", "n_new", "echo")
LOGS = set(("words", "shared_scope", "shared_checkpoint", "shared_expected", "new_words", "known_words", "times", "shape_gates", "shape_shared_project", "values_out", "n_words_out", "n_new"))
LABEL_Q = {"completes": "completes", "progresses": "progresses", "regresses": "regresses", "supersedes": "supersedes", "drift": "off_scope", "invention": "invents", "hallucination": "contradicts"}
MARKS = set(LABEL_Q) | {"dupe", "noise", "unsettled"}
def feats(cells):
    c = dict(cells); c["mark_met"] = 1.0 if cells.get("expected_mark") == "met" else 0.0; c["n_words_out"] = len(cells.get("words_out", [])); c["n_new"] = len(cells.get("new_to_project", []))
    x = [1.0]
    for f in FEATS:
        v = float(c.get(f, 0) or 0); x.append(math.log1p(v) if f in LOGS else v)
    return x
def sigmoid(z): return 1 / (1 + math.exp(-max(-30.0, min(30.0, z))))
def weights():
    row = cx_get("weights", "judge", 0); return json.loads(row[3]) if row else None
def learned_answers(cells, W=None):
    W = W or weights()
    if not W: return None
    x = feats(cells); return {k: round(sigmoid(sum(a * b for a, b in zip(W["w"].get(k, []), x))), 3) for k in JUDGE_QUESTIONS}
def train_logistic(X, Y, iters=300, lr=0.5, l2=0.01):
    d = len(X[0]); w = [0.0] * d; n = float(len(X))
    for _ in range(iters):
        g = [0.0] * d
        for x, y in zip(X, Y):
            e = sigmoid(sum(a * b for a, b in zip(w, x))) - y
            for j in range(d): g[j] += e * x[j]
        for j in range(d): w[j] -= lr * (g[j] / n + l2 * w[j])
    return w
'''
rep("def decide(a):", LEARN.lstrip("\n") + "def decide(a):")

rep('''def v_project(name, scope):
    ensure_cx(); run, at, r = record("project", name, 0, clean(scope))''', '''def v_project(name, scope):
    ensure_cx(); run, at, r = record("project", name, 0, clean(scope)); key_gates(name, run)''')
rep('''    ensure_cx(); run, at, r = record("checkpoint", name, n, clean(text)); print("checkpoint %s %d run %d clock %d" % (name, n, run, at))
    if expected: run2, at2, _ = record("expected", name, n, clean(expected)); print("expected %s %d run %d" % (name, n, run2))''',
'''    ensure_cx(); run, at, r = record("checkpoint", name, n, clean(text)); key_gates(name, run); print("checkpoint %s %d run %d clock %d" % (name, n, run, at))
    if expected: run2, at2, _ = record("expected", name, n, clean(expected)); key_gates(name, run2); print("expected %s %d run %d" % (name, n, run2))''')
rep("def v_ingest(name, text, quiet=False):", "def v_ingest(name, text, quiet=False, repeat_to_kernel=True):")
rep('''            t, times = ingest_text(had[3]); times += 1
            cx_put("ingest", name, k, had[0], had[1], json.dumps({"t": t, "times": times}))
            out.append({"run": had[0], "clock": had[1], "born": 0, "seconds": 0.0, "same_as": had[0], "again": times, "text": s})
            if not quiet: print("ingest run %d again %d (a repeat; nothing typed): %s" % (had[0], times, s[:100]))''',
'''            t, times = ingest_text(had[3]); times += 1
            kr = typed("cortex ingest %s : %s" % (name, s)) if repeat_to_kernel else None   # the kernel ticks its own counter: same_as the first run, no second memory row (the owner, 11-03)
            cx_put("ingest", name, k, had[0], had[1], json.dumps({"t": t, "times": times}))
            out.append({"run": had[0], "clock": had[1], "born": 0, "seconds": 0.0, "same_as": had[0], "again": times, "text": s})
            if not quiet: print("ingest run %d again %d (a repeat%s): %s" % (had[0], times, (", kernel run %d same_as %s" % (kr["run"], (run_row(kr["run"]) or [0, 0])[1])) if kr else "; nothing typed", s[:100]))''')
rep('''        cx_put("ingest", name, k, run, at, json.dumps({"t": s, "times": 1})); cx_put("restate", name, wordset_key(s), run, at, str(k))''',
    '''        cx_put("ingest", name, k, run, at, json.dumps({"t": s, "times": 1})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run)''')

region("def add_part(name, n, run, text):", "\n# ---- the judge as a run data sheet", r'''def add_part(name, n, run, text, p=None, by=None):
    k = text_key(text); had = cx_get("part", name, k)
    if had:
        d = json.loads(had[3]); d["times"] = d.get("times", 1) + 1; d.pop("rejected_by", None)   # accepted again: back in the state (a superseded part stays superseded)
        cx_put("part", name, k, had[0], had[1], json.dumps(d)); return "tick %d" % d["times"]
    cx_put("part", name, k, run, clock(), json.dumps({"t": text, "n": n, "run": run, "times": 1, "p": p, "by": by, "ts": int(time.time())})); return "added"
def retire_part(name, n, old_run, new_run, why):
    # a part leaves the accepted state: superseded_by a newer value, or rejected_by a re-judgment; the row stays as history
    for (ts, v) in q("SELECT ts, value FROM main.cx WHERE kind = 'part' AND name = ? AND n > 0 ORDER BY ts DESC LIMIT 200", name):
        d = json.loads(v)
        if d.get("run") == old_run and d.get("n") == n and not d.get(why):
            d[why] = new_run; cx_put("part", name, text_key(d["t"]), d["run"], clock(), json.dumps(d)); return True
    return False
def parts_of(name, n, limit=5, history=False):
    out = []
    for (ts, v) in q("SELECT ts, value FROM main.cx WHERE kind = 'part' AND name = ? AND n > 0 ORDER BY ts DESC LIMIT 200", name):
        d = json.loads(v)
        if d.get("n") != n: continue
        if not history and (d.get("superseded_by") or d.get("rejected_by")): continue
        d.setdefault("ts", ts); out.append(d)
    return out[:limit]
def accepted_state(name, n):
    ps = parts_of(name, n)
    return " | ".join(p["t"] for p in reversed(ps)) if ps else "(nothing accepted yet)"
''')
rep('''    for p in parts_of(name, n, 1000): known |= content_words(p["t"])''', '''    parts = parts_of(name, n, 1000)
    for p in parts: known |= content_words(p["t"])''')
rep('''    cells["observed"] = bool(OBS.search(text))
    return cells''', '''    cells["observed"] = bool(OBS.search(text))
    cells.update(shape_cells(name, n, run, pr, ck, ex, parts))
    return cells''')

region("def formula(cells, answers):", "\ndef v_judge(", r'''def formula(cells, answers):
    # the substitution formulas over a full sheet, in order: what the shape settles, then the deterministic word cells, then the judgment cells
    if cells["noise"]: return "noise", "sheet"
    if cells.get("same_as"): return "dupe", "shape"                                   # the kernel's own repeat of an earlier run
    if cells.get("echo"): return "dupe", "shape"                                      # the expected sentence's own shape with nothing out of line: words, no observation
    if cells.get("supersedes_run"): return "supersedes", "shape"                      # the same shape as an accepted part, only value or time gates out of line
    if cells.get("shape_gates", 0) >= 4 and cells["shape_shared_project"] == 0: return "drift", "shape"   # no word gate shared with the scope, checkpoint or expected
    if cells["words"] >= 4 and cells["shared_scope"] == 0 and cells["shared_checkpoint"] == 0 and cells["shared_expected"] == 0 and not cells["observed"]: return "drift", "sheet"
    if cells.get("shape_gates") and cells["shape_expected"] >= 0.7 and cells["values_out"] >= 1 and len(cells["new_to_project"]) <= 1: return "completes", "shape"   # the expected's shape plus a value out of line
    if cells["words"] >= 4 and cells["new_words"] == 0 and cells["known_words"] >= 3 and not cells["observed"]: return "dupe", "sheet"   # a restatement with nothing new and nothing observed
    if answers: return decide(answers), "judgment"
    return "unsettled", "sheet"
''')

region("def v_judge(", "\ndef judge_many(", r'''def v_judge(name, n, run, text=None, answers_given=None, judge_name=None):
    ensure_cx()
    pr = cx_get("project", name, 0); ck = cx_get("checkpoint", name, n); ex = cx_get("expected", name, n)
    if not pr or not ck: raise SystemExit("no such project/checkpoint: %s %s" % (name, n))
    if text is None:
        rows = q("SELECT value FROM main.cx WHERE kind = 'ingest' AND name = ? AND run = ? AND n > 0", name, run)
        if not rows: raise SystemExit("ingest run %s is not in the index" % run)
        text = ingest_text(rows[0][0])[0]
    t0 = time.time(); cells = sheet_cells(name, n, run, text, pr, ck, ex)
    state = {"project": name, "scope": pr[3], "checkpoint": ck[3], "expected": ex[3] if ex else "(none)", "accepted_state": accepted_state(name, n), "ingest": text}
    answers, model = {}, None
    kind, by = formula(cells, {})
    if kind == "unsettled":
        if answers_given is not None: answers, model = answers_given, judge_name
        else:
            la = learned_answers(cells); lv = (weights() or {}).get("v", 0)
            if la is not None and decide(la) != "unsettled": answers, model = la, "learned v%d" % lv
            elif judge_route():
                try: got, model = judge_batch(state, [(run, text)]); answers = got.get(run, {})
                except (urllib.error.URLError, urllib.error.HTTPError, OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as e:
                    raise SystemExit("judge call failed, no verdict written: %s" % e)
            elif la is not None: answers, model = la, "learned v%d (abstained)" % lv
    if answers: kind, by = formula(cells, answers)
    judge = model if (by == "judgment" and model) else by
    if answers and by == "judgment": p = answers.get(kind, 0.0) if kind in answers else max(answers.values())
    elif by == "shape": p = cells["shape_expected"] if kind == "completes" else 1.0
    else: p = 1.0 if kind in ("noise", "drift", "dupe") else 0.0
    body = "%s %.3f %s" % (kind, p, judge)
    vrun, at, _ = record("verdict", name, run, body)
    accepting = kind in ("completes", "progresses", "supersedes")
    part = add_part(name, n, run, text, p, judge) if accepting else ("rejected" if retire_part(name, n, run, vrun, "rejected_by") else "")
    if kind == "supersedes" and cells.get("supersedes_run") and retire_part(name, n, cells["supersedes_run"], run, "superseded_by"): part += " | retired the part of run %d" % cells["supersedes_run"]
    moved = ""
    if kind == "completes" and p >= THRESH:
        st = cx_get("state", name, n)
        if not st or st[3] != "done":
            v_state(name, n, "done"); n2 = next_checkpoint(name)
            if n2 is not None and n2 != n:
                s2 = cx_get("state", name, n2)
                if not s2 or s2[3] != "working": v_state(name, n2, "working")
            moved = " | C%d done by this verdict; next C%s" % (n, n2)
    cx_put("verdict", name, run, vrun, at, json.dumps({"n": n, "run": run, "kind": kind, "p": p, "judge": judge, "answers": answers, "sheet": cells, "part": part, "text": text[:300]}))
    geo = cells["geometry"]
    print("verdict %s %d run %d: %s %.3f by %s in %.0f ms | shape gates %d expected %.2f shared project %d values out %d words out %s new to project %s supersedes %s same_as %s echo %s | words %d shared scope %d checkpoint %d expected %d new %d known %d coverage %.2f observed %s mark %s times %d | geometry mag %s rad %s%s" % (name, n, run, kind, p, judge, (time.time() - t0) * 1000, cells["shape_gates"], cells["shape_expected"], cells["shape_shared_project"], cells["values_out"], ",".join(cells["words_out"]) or "-", ",".join(cells["new_to_project"]) or "-", cells["supersedes_run"] or "-", cells["same_as"] or "-", cells["echo"], cells["words"], cells["shared_scope"], cells["shared_checkpoint"], cells["shared_expected"], cells["new_words"], cells["known_words"], cells["coverage_expected"], cells["observed"], cells["expected_mark"], cells["times"], geo.get("magnitude"), geo.get("radians"), (" | part " + part) if part else ""))
    if moved: print(" " + moved.strip(" |"))
    if answers: print("  answers " + " ".join("%s=%.2f" % kv for kv in sorted(answers.items())))
    elif kind == "unsettled": print("  judgment cells empty: no weights learned yet (cortex learn) and no model judge")
    return kind
''')

region("def judge_many(", "\ndef next_checkpoint(", r'''def judge_many(name, n, items):
    # the sheet and the shape for every sentence first; the learned weights for what they leave; one model call for the batch still unsettled; then every verdict written
    pr = cx_get("project", name, 0); ck = cx_get("checkpoint", name, n); ex = cx_get("expected", name, n)
    if not pr or not ck or not items: return []
    state = {"project": name, "scope": pr[3], "checkpoint": ck[3], "expected": ex[3] if ex else "(none)", "accepted_state": accepted_state(name, n)}
    W = weights(); given, pending = {}, []
    for i in items:
        cells = sheet_cells(name, n, i["run"], i["text"], pr, ck, ex)
        if formula(cells, {})[0] != "unsettled": continue
        la = learned_answers(cells, W)
        if la is not None and decide(la) != "unsettled": given[i["run"]] = (la, "learned v%d" % W.get("v", 0))
        else: pending.append((i["run"], i["text"]))
    got, model = {}, None
    if pending and judge_route():
        try: got, model = judge_batch(state, pending)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as e:
            raise SystemExit("judge call failed, no verdict written: %s" % e)
    out = []
    for i in items:
        r = i["run"]
        if r in given: out.append(v_judge(name, n, r, i["text"], given[r][0], given[r][1]))
        elif r in got: out.append(v_judge(name, n, r, i["text"], got[r], model))
        else: out.append(v_judge(name, n, r, i["text"]))
    return out
''')

rep('''        if ps: lines.append("ACCEPTED SO FAR (parts of C%d's state): " % nxt + " | ".join(p["t"][:90] for p in reversed(ps)))''',
    '''        if ps: lines.append("ACCEPTED SO FAR (parts of C%d's state, each with its time and confidence): " % nxt + " | ".join("%s [%s%s]" % (p["t"][:90], time.strftime("%m-%d %H:%M", time.localtime(p.get("ts") or 0)), (" p%.2f %s" % (p["p"], p.get("by") or "")) if p.get("p") is not None else "") for p in reversed(ps)))''')
rep('''ensure_cx(); last = "\\n".join(texts_all); ing = v_ingest(name, last, quiet=True); new = [i for i in ing if not i["same_as"]]''',
    '''ensure_cx(); last = "\\n".join(texts_all); ing = v_ingest(name, last, quiet=True, repeat_to_kernel=False); new = [i for i in ing if not i["same_as"]]''')

MARKLEARN = r'''
def v_mark(name, run, kind, why=""):
    # the labeled set: the owner's (or the known-truth) word on what a judged sentence was; cortex learn trains the weights on these
    ensure_cx()
    if kind not in MARKS: raise SystemExit("a mark is one of: " + " ".join(sorted(MARKS)))
    v = cx_get("verdict", name, run)
    if not v: raise SystemExit("no verdict for run %s in %s; judge it first so the mark knows its checkpoint" % (run, name))
    n = json.loads(v[3]).get("n"); cx_put("mark", name, run, run, clock(), json.dumps({"kind": kind, "n": n, "why": why, "ts": int(time.time())}))
    print("mark %s run %d C%s: %s" % (name, run, n, kind))
def key_project(nm):
    # the (project, gate) key for every line of the project not keyed yet, in run order (build time, once per line)
    had = cx_get("keyed", nm, 0); upto = int(json.loads(had[3]).get("upto", 0)) if had else 0
    runs = set()
    for kind in ("project", "checkpoint", "expected", "ingest"):
        for (n, run, at, ts, value) in cx_list(kind, nm, limit=5000):
            if run and run > upto: runs.add(run)
    for run in sorted(runs): key_gates(nm, run)
    if runs: cx_put("keyed", nm, 0, max(runs), clock(), json.dumps({"upto": max(runs), "runs": len(runs), "ts": int(time.time())}))
    return len(runs)
def v_learn(names=None, key_only=False):
    ensure_cx(); t0 = time.time()
    names = names or sorted(set(r[0] for r in q("SELECT name FROM main.cx WHERE kind = 'project' AND name >= '' AND n = 0")))
    for nm in names: print("key %s: %d lines keyed in %.1f s" % (nm, key_project(nm), time.time() - t0))
    if key_only: return
    rows = []
    for nm in names:
        pr = cx_get("project", nm, 0)
        for (n, run, at, ts, value) in cx_list("mark", nm, limit=5000):
            d = json.loads(value); ck = cx_get("checkpoint", nm, d["n"]); ex = cx_get("expected", nm, d["n"])
            ing = q("SELECT value FROM main.cx WHERE kind = 'ingest' AND name = ? AND run = ? AND n > 0", nm, run)
            if not ing or not ck or not pr: continue
            rows.append((feats(sheet_cells(nm, d["n"], run, ingest_text(ing[0][0])[0], pr, ck, ex)), d["kind"], nm, run))
    if len(rows) < 6: print("learn: %d marks; at least 6 are needed" % len(rows)); return
    def fit(train): return {k: train_logistic([r[0] for r in train], [1.0 if LABEL_Q.get(r[1]) == k else 0.0 for r in train]) for k in JUDGE_QUESTIONS}
    hits, wrong = 0, []
    for i in range(len(rows)):
        W = {"w": fit(rows[:i] + rows[i + 1:])}; got = decide(learned_answers_x(rows[i][0], W)); want = rows[i][1] if rows[i][1] in LABEL_Q else "unsettled"
        if got == want: hits += 1
        else: wrong.append("%s run %d: marked %s, learned %s" % (rows[i][2], rows[i][3], rows[i][1], got))
    v = (weights() or {}).get("v", 0) + 1
    rec = {"v": v, "w": fit(rows), "feats": list(FEATS), "rows": len(rows), "loo": round(hits / len(rows), 3), "ts": int(time.time())}
    cx_put("weights", "judge", 0, 0, clock(), json.dumps(rec)); cx_put("weights", "judge", v, 0, clock(), json.dumps(rec))
    print("learn: weights v%d from %d marks; leave-one-out verdict accuracy %.2f (%d of %d) in %.1f s" % (v, len(rows), hits / len(rows), hits, len(rows), time.time() - t0))
    for w in wrong: print("   missed: " + w)
def learned_answers_x(x, W): return {k: round(sigmoid(sum(a * b for a, b in zip(W["w"].get(k, []), x))), 3) for k in JUDGE_QUESTIONS}
'''
rep("def v_status(name=None):", MARKLEARN.lstrip("\n") + "def v_status(name=None):")
rep('''| judge: sheet+graph, then %s | index rows %d" % (st["gates"], st["runs"], st["hops"], st["refused"], clock(), ''',
    '''| judge: shape, learned v%s, then %s | index rows %d" % (st["gates"], st["runs"], st["hops"], st["refused"], clock(), (weights() or {}).get("v", 0), ''')
rep('''  accept <name> <n> [run]                  the owner's word: with a run, that sentence is a part of C n's state; without, C n is done
"""''', '''  accept <name> <n> [run]                  the owner's word: with a run, that sentence is a part of C n's state; without, C n is done
  mark <name> <run> <kind> [: <why>]       the labeled set: what that judged sentence was (completes progresses regresses supersedes drift invention hallucination dupe noise unsettled)
  learn [<name> ...] [--key]               the (project, gate) key for every line, then the judge's weights from the marks (leave-one-out accuracy printed); --key keys only
"""''')
rep('''    elif v == "status": v_status(a[0] if a else None)''', '''    elif v == "mark":
        s = " ".join(a); why = ""
        if " : " in s: s, why = s.split(" : ", 1)
        k = s.split(); v_mark(k[0], int(k[1]), k[2], why)
    elif v == "learn": v_learn([x for x in a if not x.startswith("--")] or None, key_only="--key" in a)
    elif v == "status": v_status(a[0] if a else None)''')
assert src != orig
open(P, "w").write(src); print("patched: %d -> %d bytes" % (len(orig), len(src)))
