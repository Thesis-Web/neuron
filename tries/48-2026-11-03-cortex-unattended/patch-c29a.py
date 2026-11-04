# C29a: the owner's prose is a voice too. the capture takes the session's user messages (the owner's own typing, pastes and command text left out) as ingests with the voice owner, judged like every other voice; the verdict line prints the voice
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''    raw = sys.stdin.read(); texts_all = []; hook = {}; cmds = {}; results = []
''', '''    raw = sys.stdin.read(); texts_all = []; hook = {}; cmds = {}; results = []; owner_texts = []
''')
rep('''        if d.get("type") != "assistant": continue
        c = d.get("message", {}).get("content")
''', '''        if d.get("type") == "user" and not d.get("isSidechain"):   # C29: the owner's own words in the session are a voice the judge scores too (the owner, 11-03: i should be judged also yes)
            cu = d.get("message", {}).get("content"); tu = cu if isinstance(cu, str) else "\\n".join(b.get("text", "") for b in cu if isinstance(b, dict) and b.get("type") == "text") if isinstance(cu, list) else ""
            tu = re.sub(r"(?s)<pasted_content[^>]*>.*?</pasted_content>", " ", tu); tu = re.sub(r"(?s)<system-reminder>.*?</system-reminder>|<command-[a-z-]+>.*?</command-[a-z-]+>|<local-command[^>]*>.*?</local-command[^>]*>", " ", tu)
            if tu.strip() and not tu.lstrip().startswith("<") and "This session is being continued" not in tu: owner_texts.append(tu.strip())
            continue
        if d.get("type") != "assistant": continue
        c = d.get("message", {}).get("content")
''')
rep('''    last = "\\n".join(texts_all); ing = v_ingest(name, last, quiet=True, repeat_to_kernel=False); new = [i for i in ing if not i["same_as"]]
''', '''    own = []
    if owner_texts:
        VOICE[0] = "owner"; own = v_ingest(name, "\\n".join(owner_texts), quiet=True, repeat_to_kernel=False); VOICE[0] = "hub:" + ((hook.get("session_id") or "")[:8] or "unknown")
    last = "\\n".join(texts_all); ing = v_ingest(name, last, quiet=True, repeat_to_kernel=False); new = [i for i in ing if not i["same_as"]] + [i for i in own if not i["same_as"]]
''')
rep('''    print("capture %s: %d texts, %d sentences, %d new, %d repeats, %d bytes%s" % (name, len(texts_all), len(ing), len(new), len(ing) - len(new), len(last.encode()), (", the turn's final message included (%d bytes)" % len(final_msg.encode())) if final_msg else ""))
''', '''    print("capture %s: %d texts, %d sentences, %d new, %d repeats, %d bytes%s%s" % (name, len(texts_all), len(ing), len(new), len(ing) + len(own) - len(new), len(last.encode()), (", the turn's final message included (%d bytes)" % len(final_msg.encode())) if final_msg else "", (", the owner's voice: %d messages, %d sentences" % (len(owner_texts), len(own))) if owner_texts else ""))
''')
# the verdict print names the voice
rep('''    print("  ground: %s | receipts %d (%s)%s numbers in %s out %s%s" % (''', '''    print("  voice: %s%s" % (iv.get("voice", "hand"), " (a labeled guess)" if iv.get("guess") else ""))
    print("  ground: %s | receipts %d (%s)%s numbers in %s out %s%s" % (''')
open(p, "w").write(s); print("patched c29a")
