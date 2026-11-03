# C18 (the owner, 11-03 15:0x): the cortex holds the remainder and names the next work; the capture judges every ingest even when every checkpoint is done
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
# the remainder: typed lines on a checkpoint; the index keeps run, order, satisfied
rep('''def v_mark(name, run, kind, why=""):
''', '''GATED = ("kernel", "owner")   # a remainder part naming the kernel or the owner waits on them; the first part naming neither is the front door's next work
def remainders_of(name, n):
    had = cx_get("remainder", name, n)
    return json.loads(had[3]) if had else []
def next_work(name):
    for (cn, run, at, ts, ctext) in cx_list("checkpoint", name):
        for r in remainders_of(name, cn):
            if r.get("satisfied"): continue
            t = line_text(r["run"])
            if not any(g in t for g in GATED): return cn, r["k"], t
    return None
def v_remainder(name, n=None, text=None, k=None, note=None):
    # cortex remainder <name> <n> : <part left not satisfied>   |   cortex remainder <name> <n> <k> satisfied [: by what]   |   cortex remainder <name>
    ensure_cx()
    if n is None:
        tot = open_ = 0
        for (cn, run, at, ts, ctext) in cx_list("checkpoint", name):
            for r in remainders_of(name, cn):
                tot += 1; open_ += 0 if r.get("satisfied") else 1
                print("C%d.%d %s%s" % (cn, r["k"], line_text(r["run"])[:140], (" [satisfied %s: %s]" % (time.strftime("%m-%d %H:%M", time.localtime(r.get("satisfied_ts", 0))), r["satisfied"])) if r.get("satisfied") else ""))
        nw = next_work(name)
        print("%d remainder parts of %s, %d not satisfied. NEXT WORK: %s" % (tot, name, open_, ("C%d.%d %s" % nw) if nw else "none that is the front door's; the rest wait on the kernel or the owner"))
        return
    if not cx_get("checkpoint", name, n): raise SystemExit("no such checkpoint: %s %d" % (name, n))
    rs = remainders_of(name, n)
    if k is not None:
        hit = [r for r in rs if r["k"] == k]
        if not hit: raise SystemExit("no remainder part %d on %s C%d" % (k, name, n))
        hit[0]["satisfied"] = note or "yes"; hit[0]["satisfied_ts"] = int(time.time())
        cx_put("remainder", name, n, hit[0]["run"], clock(), json.dumps(rs)); print("remainder %s C%d.%d satisfied: %s" % (name, n, k, note or "yes")); return
    r = typed("cortex remainder %s %d : %s" % (name, n, text)); run = r["run"]; key_gates(name, run)
    rs.append({"k": len(rs) + 1, "run": run, "ts": int(time.time()), "satisfied": None})
    cx_put("remainder", name, n, run, clock(), json.dumps(rs)); print("remainder %s C%d.%d run %d: %s" % (name, n, len(rs), run, text[:120]))
def v_mark(name, run, kind, why=""):
''')
# the formula prints the remainder parts of every checkpoint and names the next work
rep('''    rem = [n for n in cps if n not in done]
    print("CONTRACT, REMAINDER (%d of %d):" % (len(rem), N))
    for n in rem:
        c = cps[n]; miss = []
        if c["parts"] == 0: miss.append("no accepted part")
        if not c["verdicts"].get("completes"): miss.append("no completes verdict")
        print("  C%s [%s] expected: %s | missing: %s" % (n, c["state"], c["expected"][:110] or "(none)", ", ".join(miss)))
''', '''    rem = [n for n in cps if n not in done]
    parts_left = [(int(n), r) for n in cps for r in remainders_of(name, int(n)) if not r.get("satisfied")]
    print("CONTRACT, REMAINDER (%d checkpoints open, %d parts left not satisfied):" % (len(rem), len(parts_left)))
    for n in rem:
        c = cps[n]; miss = []
        if c["parts"] == 0: miss.append("no accepted part")
        if not c["verdicts"].get("completes"): miss.append("no completes verdict")
        print("  C%s [%s] expected: %s | missing: %s" % (n, c["state"], c["expected"][:110] or "(none)", ", ".join(miss)))
    for (n, r) in parts_left: print("  C%d.%d left: %s" % (n, r["k"], line_text(r["run"])[:130]))
    nw = next_work(name)
    print("NEXT WORK (the first part left that names neither the kernel nor the owner): %s" % (("C%d.%d %s" % nw) if nw else "none; what is left waits on the kernel or the owner"))
''')
# the hydration shows the remainder when nothing is open, and the next checkpoint's own remainder when one is
rep('''    else: lines.append("DO NOW: nothing; every checkpoint is done. Say so.")
''', '''    else:
        lines.append("DO NOW: nothing; every checkpoint is done. Say so.")
        left = [(cn, r) for (cn, run, at, ts, ctext) in cx_list("checkpoint", name) for r in remainders_of(name, cn) if not r.get("satisfied")]
        if left: lines.append("REMAINDER (the contract's parts left not satisfied, from the brain; the owner's word makes one a checkpoint): " + "; ".join("C%d.%d %s" % (cn, r["k"], line_text(r["run"])[:100]) for (cn, r) in left[:10]))
        nw = next_work(name)
        if nw: lines.append("NEXT WORK (the first part left that names neither the kernel nor the owner): C%d.%d %s" % nw)
''')
rep('''        qs = open_questions(name, nxt, 5)
''', '''        left = [r for r in remainders_of(name, nxt) if not r.get("satisfied")]
        if left: lines.append("REMAINDER of C%d (parts left not satisfied): " % nxt + "; ".join("%d %s" % (r["k"], line_text(r["run"])[:100]) for r in left[:6]))
        qs = open_questions(name, nxt, 5)
''')
# the capture judges against the newest checkpoint when none is open
rep('''    nxt = next_checkpoint(name)
    if nxt is None: return
    try:
        kinds = judge_many(name, nxt, new[-20:]); print("judged against C%d: %s" % (nxt, " ".join(kinds)))
''', '''    nxt = next_checkpoint(name); newest = False
    if nxt is None:
        cps = cx_list("checkpoint", name, desc=True, limit=1)
        if not cps: return
        nxt = cps[0][0]; newest = True   # every checkpoint done: the truth matrix still runs, against the newest one (the owner, 11-03: scan every ingress)
    try:
        kinds = judge_many(name, nxt, new[-20:]); print("judged against C%d%s: %s" % (nxt, " (every checkpoint done; the newest)" if newest else "", " ".join(kinds)))
''')
# usage and dispatch
rep('''  questions <name> [n]                     the open meaning questions: words of judged claims that no receipt, owner line or reference holds
''', '''  questions <name> [n]                     the open meaning questions: words of judged claims that no receipt, owner line or reference holds
  remainder <name> [<n> : <text>]          the contract's parts left not satisfied, typed on their checkpoint; <name> alone lists them and names the next work
  remainder <name> <n> <k> satisfied [: by what]
''')
rep('''    elif v == "questions": v_questions(a[0], int(a[1]) if len(a) > 1 else None)
''', '''    elif v == "questions": v_questions(a[0], int(a[1]) if len(a) > 1 else None)
    elif v == "remainder":
        if len(a) == 1: v_remainder(a[0])
        elif len(a) >= 4 and a[3] == "satisfied":
            s3 = " ".join(a); note = s3.split(" : ", 1)[1] if " : " in s3 else None; v_remainder(a[0], int(a[1]), None, int(a[2]), note)
        else: k3, t3 = split_colon(a); v_remainder(k3[0], int(k3[1]), t3)
''')
open(p, "w").write(s); print("patched c18")
