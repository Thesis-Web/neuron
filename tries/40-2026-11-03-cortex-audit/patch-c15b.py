P = "/home/james/cortex/cortex.py"; src = open(P).read(); orig = src
def rep(old, new):
    global src
    assert src.count(old) == 1, "anchor (%d): %r" % (src.count(old), old[:80]); src = src.replace(old, new)
rep('''    if kind == "completes" and p >= THRESH:
        st = cx_get("state", name, n)''', '''    if kind == "completes" and p >= THRESH and by != "shape": moved = " | a judgment cell's completes does not move the state: the shape or the owner's accept does"
    if kind == "completes" and p >= THRESH and by == "shape":
        st = cx_get("state", name, n)''')
rep('''    elif "completes" in kinds:
        v_state(name, nxt, "done"); n2 = next_checkpoint(name)
        if n2 is not None: v_state(name, n2, "working")
        print("C%d done; next C%s" % (nxt, n2))''', '''    elif "completes" in kinds: print("C%d has a completes from a judgment cell, not from the shape: the state waits for the shape or the owner's accept" % nxt)''')
rep('''        if p >= THRESH:
            r0 = run_[0]["run"] if run_ else 0; add_part(name, nxt, r0, out[:300]); v_state(name, nxt, "done"); n2 = next_checkpoint(name)
            if n2 is not None: v_state(name, n2, "working")
            print("C%d done by the judgment (%.2f); next C%s" % (nxt, p, n2))''', '''        if p >= THRESH:
            r0 = run_[0]["run"] if run_ else 0; add_part(name, nxt, r0, out[:300], p, "judgment")
            if out.startswith("judgment by graph"):
                v_state(name, nxt, "done"); n2 = next_checkpoint(name)
                if n2 is not None: v_state(name, n2, "working")
                print("C%d done by the judgment (%.2f); next C%s" % (nxt, p, n2))
            else: print("C%d holds %.2f by a model; the state waits for the owner's accept" % (nxt, p))''')
rep('''        d = json.loads(had[3]); d["times"] = d.get("times", 1) + 1; d.pop("rejected_by", None)   # accepted again: back in the state (a superseded part stays superseded)''',
    '''        d = json.loads(had[3])
        if d.get("rejected_by") == "owner": return "refused (rejected by the owner)"
        d["times"] = d.get("times", 1) + 1; d.pop("rejected_by", None)   # accepted again: back in the state (a superseded part stays superseded)''')
rep('''        if d.get("run") == old_run and d.get("n") == n and not d.get(why):''', '''        if d.get("run") == old_run and d.get("n") == n and (new_run == "owner" or not d.get(why)):''')
rep('''MODEL_BY_KIND = {"read": "haiku"''', '''def v_reject(name, n, run):
    # the owner's word, the counterpart of accept: that sentence is not a part of C n's state whatever the judge said; it stays as history and is never re-accepted
    ensure_cx()
    if retire_part(name, n, run, "owner", "rejected_by"): print("part of run %d rejected from %s C%d by the owner" % (run, name, n))
    else: raise SystemExit("no part of run %s in %s C%d" % (run, name, n))
MODEL_BY_KIND = {"read": "haiku"''')
rep('''    elif v == "accept": v_accept(a[0], int(a[1]), int(a[2]) if len(a) > 2 else None)''', '''    elif v == "accept": v_accept(a[0], int(a[1]), int(a[2]) if len(a) > 2 else None)
    elif v == "reject": v_reject(a[0], int(a[1]), int(a[2]))''')
rep('''  mark <name> <run> <kind> [: <why>]''', '''  reject <name> <n> <run>                  the owner's word: that sentence is not a part of C n's state, whatever the judge said
  mark <name> <run> <kind> [: <why>]''')
open(P, "w").write(src); print("patched b: %d -> %d" % (len(orig), len(src)))
