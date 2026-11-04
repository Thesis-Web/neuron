# C23 the pair ground, a try at meaning: adjacent content-gate pairs keyed per source and project at build time; a claim's pairs held by which sources; a pair held nowhere is where the run leaves known ground
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''def key_gates(name, run):
''', '''def pair_key(a, b): return (a << 20) ^ b if a < (1 << 40) else int(hashlib.sha256(("%d,%d" % (a, b)).encode()).hexdigest()[:15], 16)
def pairs_of(run):
    # the adjacent content-gate pairs of a run (words only, digits left out): the hops a reader of the sentence takes between meanings
    ws = [g for g in content_gates(run) if not is_value(g)]
    return list(zip(ws, ws[1:]))
def key_pairs(name, run):
    # the (project or source, pair) key: how many lines of this project cross from gate a to gate b (C23, build time)
    for (a, b) in set(pairs_of(run)):
        k = pair_key(a, b); had = cx_get("pair", name, k)
        if had:
            d = json.loads(had[3]); d["times"] = d.get("times", 1) + 1; cx_put("pair", name, k, had[0], had[1], json.dumps(d))
        else: cx_put("pair", name, k, run, clock(), json.dumps({"a": a, "b": b, "first": run, "times": 1}))
def pair_ground(name, run):
    # per pair of the claim: the sources and projects that hold it; the pairs held nowhere are where the run leaves known ground
    held, none = {}, []
    srcs = [nm for (nm, band) in sources()] + [pj for pj in projects()]
    for (a, b) in pairs_of(run):
        k = pair_key(a, b); who = [nm for nm in srcs if cx_get("pair", nm, k) and not (nm == name and json.loads(cx_get("pair", nm, k)[3]).get("first") == run)]
        if who:
            for nm in who: held[nm] = held.get(nm, 0) + 1
        else: none.append("%s %s" % (sym_of(a), sym_of(b)))
    return {"pairs": len(pairs_of(run)), "held_by": held, "none": none}
def key_gates(name, run):
''')
# every typed line keys its pairs where it keys its gates
rep('''        run = r["run"]; cx_put("source", name, k, run, clock(), "{}"); key_gates(name, run); n_typed += 1''', '''        run = r["run"]; cx_put("source", name, k, run, clock(), "{}"); key_gates(name, run); key_pairs(name, run); n_typed += 1''')
rep('''        cx_put("ingest", name, k, run, at, json.dumps({"times": 1})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run)
''', '''        cx_put("ingest", name, k, run, at, json.dumps({"times": 1})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run); key_pairs(name, run)
''')
# the pair ground on the sheet and the question names the pairs held nowhere
rep('''    cells.update(ground_cells(name, n, run, text, cells["new_to_project"]))
    return cells
''', '''    cells.update(ground_cells(name, n, run, text, cells["new_to_project"]))
    cells["pair_ground"] = pair_ground(name, run)
    return cells
''')
rep('''    if len(cells.get("ground", {}).get("none", [])) >= 2 and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, cells["ground"]["none"], vrun)
''', '''    pg = cells.get("pair_ground") or {}
    if pg.get("pairs"): print("  pairs: %d, held by %s | held nowhere: %s" % (pg["pairs"], " ".join("%s %d" % kv for kv in sorted(pg["held_by"].items(), key=lambda kv: -kv[1])[:4]) or "no source", "; ".join(pg["none"]) or "-"))
    unknown = (cells.get("ground", {}).get("none") or []) + [("pair: " + x) for x in pg.get("none", []) if len(pg.get("none", [])) >= 2]
    if len(unknown) >= 2 and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, unknown[:8], vrun)
''')
# learn --pairs: the backfill over every source and project line
rep('''def v_learn(names=None, key_only=False):
''', '''def key_pairs_all(limit_s=None):
    # build time: the pair key for every source and project line not keyed yet (C23); prints progress; a time box in seconds
    t0 = time.time(); n = 0
    for nm in [nm for (nm, band) in sources()] + projects():
        had = cx_get("paired", nm, 0); upto = int(json.loads(had[3]).get("upto", 0)) if had else 0; top = upto
        kinds = ("source",) if nm in [x for (x, b) in sources()] else ("project", "checkpoint", "expected", "ingest", "receipt")
        for kind in kinds:
            for (k, run, at, ts, v) in cx_list(kind, nm, limit=100000):
                if not run or run <= upto: continue
                key_pairs(nm, run); n += 1; top = max(top, run)
                if n % 2000 == 0: print("  %d lines paired, %.0f s" % (n, time.time() - t0), flush=True)
                if limit_s and time.time() - t0 > limit_s: break
            if limit_s and time.time() - t0 > limit_s: break
        if top > upto: cx_put("paired", nm, 0, top, clock(), json.dumps({"upto": top, "ts": int(time.time())}))
        if limit_s and time.time() - t0 > limit_s: print("time box reached in %s" % nm); break
    print("pairs: %d lines keyed in %.0f s" % (n, time.time() - t0)); return n
def v_learn(names=None, key_only=False):
''')
rep('''    elif v == "learn": v_learn([x for x in a if not x.startswith("--")] or None, key_only="--key" in a)
''', '''    elif v == "learn":
        if "--pairs" in a: key_pairs_all(int(a[a.index("--box") + 1]) if "--box" in a else None)
        else: v_learn([x for x in a if not x.startswith("--")] or None, key_only="--key" in a)
''')
rep('''  learn [<name> ...] [--key]               the (project, gate) key for every line, then the judge's weights from the marks (leave-one-out accuracy printed); --key keys only
''', '''  learn [<name> ...] [--key]               the (project, gate) key for every line, then the judge's weights from the marks (leave-one-out accuracy printed); --key keys only
  learn --pairs [--box seconds]            build time: the (source or project, word pair) key for every line (C23: a claim's pairs held by which sources; a pair held nowhere is a question)
''')
open(p, "w").write(s); print("patched c23")
