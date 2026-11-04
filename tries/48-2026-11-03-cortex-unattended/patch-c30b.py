p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''    cps = cx_list("checkpoint", name)
    for (n, run, at, ts, text) in cps:
        st = cx_get("state", name, n)
        if st and st[3] == "working": return n
    for (n, run, at, ts, text) in cps:
        st = cx_get("state", name, n)
        if not st or st[3] == "open": return n
    return None
'''
new = '''    cps = cx_list("checkpoint", name)
    for (n, run, at, ts, text) in cps:
        st = cx_get("state", name, n)
        if st and st[3] == "working" and not parked(name, n): return n
    for (n, run, at, ts, text) in cps:
        st = cx_get("state", name, n)
        if (not st or st[3] == "open") and not parked(name, n): return n
    return None
'''
assert s.count(old) == 1; s = s.replace(old, new); open(p, "w").write(s); print("patched c30b")
