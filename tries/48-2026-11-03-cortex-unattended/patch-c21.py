# C21: the capture takes a session's tool results as receipts: each Bash tool_use command with its tool_result output, typed before the session's sentences so the prints precede the claims
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''    raw = sys.stdin.read(); texts_all = []; hook = {}
    for line in raw.splitlines():
        try: d = json.loads(line)
        except ValueError: continue
        if d.get("type") == "hook": hook = d; continue   # C20: the hook's own line: cwd, the turn's final message (transcript_path may lag it), session, event
        if d.get("type") != "assistant": continue
''', '''    raw = sys.stdin.read(); texts_all = []; hook = {}; cmds = {}; results = []
    for line in raw.splitlines():
        try: d = json.loads(line)
        except ValueError: continue
        if d.get("type") == "hook": hook = d; continue   # C20: the hook's own line: cwd, the turn's final message (transcript_path may lag it), session, event
        c0 = d.get("message", {}).get("content")
        if isinstance(c0, list):   # C21: the machine's own prints in the session: a Bash tool_use and its tool_result
            for b in c0:
                if not isinstance(b, dict): continue
                if b.get("type") == "tool_use" and b.get("name") == "Bash": cmds[b.get("id")] = str((b.get("input") or {}).get("command", ""))
                elif b.get("type") == "tool_result" and b.get("tool_use_id") in cmds:
                    cc = b.get("content"); txt = cc if isinstance(cc, str) else "\\n".join(x.get("text", "") for x in cc if isinstance(x, dict)) if isinstance(cc, list) else ""
                    if txt.strip(): results.append((cmds[b.get("tool_use_id")], txt))
        if d.get("type") != "assistant": continue
''')
rep('''    ensure_cx(); last = "\\n".join(texts_all); ing = v_ingest(name, last, quiet=True, repeat_to_kernel=False); new = [i for i in ing if not i["same_as"]]
''', '''    ensure_cx()
    nxt0 = next_checkpoint(name)
    if nxt0 is None:
        cps0 = cx_list("checkpoint", name, desc=True, limit=1); nxt0 = cps0[0][0] if cps0 else None
    nrec = 0
    if nxt0 is not None and results:
        for (cmd, txt) in results[-12:]:   # the newest twelve prints of the session, before its sentences, so a print precedes the claims that cite it
            cmdline = clean(cmd.strip().splitlines()[0] if cmd.strip() else "command")[:70]
            lines = [clean(l) for l in txt.splitlines() if clean(l)][:20]
            if not lines: continue
            rc = receipts_of(name, nxt0); got = []
            for l in lines:
                body = "%s => %s" % (cmdline, l)
                if cx_get("receipt", name, text_key(body)): continue   # the same print already a receipt
                try: r = typed("cortex receipt %s %d : %s" % (name, nxt0, body))
                except RuntimeError: continue
                run0 = r["run"]; cx_put("receipt", name, text_key(body), run0, clock(), json.dumps({"n": nxt0, "cmd": cmdline, "ts": int(time.time()), "session": (hook.get("session_id") or "")[:8]})); key_gates(name, run0); got.append({"run": run0})
            if got: rc[cmdline] = {"ts": int(time.time()), "lines": got}; cx_put("receipts", name, nxt0, got[-1]["run"], clock(), json.dumps(rc)); nrec += len(got)
        if nrec: print("receipts: %d lines typed from %d tool results for C%d" % (nrec, len(results[-12:]), nxt0))
    last = "\\n".join(texts_all); ing = v_ingest(name, last, quiet=True, repeat_to_kernel=False); new = [i for i in ing if not i["same_as"]]
''')
open(p, "w").write(s); print("patched c21")
