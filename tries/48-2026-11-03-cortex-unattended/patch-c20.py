# C20: the capture takes the hook line (cwd, last_assistant_message, session, event) from the stream; records the last capture per project; status prints it
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''    raw = sys.stdin.read(); texts_all = []
    for line in raw.splitlines():
        try: d = json.loads(line)
        except ValueError: continue
        if d.get("type") != "assistant": continue
''', '''    raw = sys.stdin.read(); texts_all = []; hook = {}
    for line in raw.splitlines():
        try: d = json.loads(line)
        except ValueError: continue
        if d.get("type") == "hook": hook = d; continue   # C20: the hook's own line: cwd, the turn's final message (transcript_path may lag it), session, event
        if d.get("type") != "assistant": continue
''')
rep('''    if not texts_all: print("capture: no assistant text in the tail"); return
    name = name or project_for_cwd(cwd)
''', '''    last = (hook.get("last_assistant_message") or "").strip()
    if last and (not texts_all or texts_all[-1].strip() != last): texts_all.append(last)
    cwd = cwd or hook.get("cwd")
    if not texts_all: print("capture: no assistant text in the tail"); return
    name = name or project_for_cwd(cwd)
''')
rep('''    print("capture %s: %d texts, %d sentences, %d new, %d repeats, %d bytes" % (name, len(texts_all), len(ing), len(new), len(ing) - len(new), len(last.encode())))
''', '''    print("capture %s: %d texts, %d sentences, %d new, %d repeats, %d bytes%s" % (name, len(texts_all), len(ing), len(new), len(ing) - len(new), len(last.encode()), (", the turn's final message included (%d bytes)" % len(last.encode())) if last else ""))
    cx_put("capture", name, 0, 0, clock(), json.dumps({"ts": int(time.time()), "texts": len(texts_all), "sentences": len(ing), "new": len(new), "event": hook.get("hook_event_name") or "stop", "session": (hook.get("session_id") or "")[:8], "final": bool(last)}))
''')
rep('''        print("freeze: brain %s file %s %s" % (fr[3][:16], now[:16], "EQUAL" if now == fr[3] else "DIFFERENT"))
''', '''        print("freeze: brain %s file %s %s" % (fr[3][:16], now[:16], "EQUAL" if now == fr[3] else "DIFFERENT"))
    caps = []
    for (nm,) in q("SELECT name FROM main.cx WHERE kind = 'capture' AND name >= '' AND n = 0"):
        c = cx_get("capture", nm, 0)
        if c:
            d = json.loads(c[3]); caps.append("%s %s (%s, %d sentences, %d new%s)" % (nm, time.strftime("%m-%d %H:%M", time.localtime(d.get("ts", 0))), d.get("event", "stop"), d.get("sentences", 0), d.get("new", 0), ", final message in" if d.get("final") else ""))
    print("captures: " + ("; ".join(caps) if caps else "none yet") + " | a stale time here is a failed or missing capture (C20)")
''')
open(p, "w").write(s); print("patched c20")
