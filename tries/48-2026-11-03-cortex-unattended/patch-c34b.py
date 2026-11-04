p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''    if meas:
        have = set(toks(cmd0) for cmd0 in rc.keys()); cells["measure_missing"] = sorted(m0 for m0 in meas if not any(toks(m0) & toks(c0) for c0 in rc.keys()))
        if cells["measure_missing"]: pass
'''
new = '''    if meas: cells["measure_missing"] = sorted(m0 for m0 in meas if not any(toks(m0) & toks(c0) for c0 in rc.keys()))   # the measures named with no print of them on this checkpoint
'''
assert s.count(old) == 1; s = s.replace(old, new); open(p, "w").write(s); print("patched c34b")
