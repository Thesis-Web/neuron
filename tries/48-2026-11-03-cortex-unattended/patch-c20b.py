p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''    last = (hook.get("last_assistant_message") or "").strip()
    if last and (not texts_all or texts_all[-1].strip() != last): texts_all.append(last)
'''
new = '''    final_msg = (hook.get("last_assistant_message") or "").strip()
    if final_msg and (not texts_all or texts_all[-1].strip() != final_msg): texts_all.append(final_msg)
'''
assert s.count(old) == 1; s = s.replace(old, new)
old2 = '''(", the turn's final message included (%d bytes)" % len(last.encode())) if last else ""))'''
new2 = '''(", the turn's final message included (%d bytes)" % len(final_msg.encode())) if final_msg else ""))'''
assert s.count(old2) == 1; s = s.replace(old2, new2)
old3 = '''"session": (hook.get("session_id") or "")[:8], "final": bool(last)}))'''
new3 = '''"session": (hook.get("session_id") or "")[:8], "final": bool(final_msg)}))'''
assert s.count(old3) == 1; s = s.replace(old3, new3); open(p, "w").write(s); print("patched c20b")
