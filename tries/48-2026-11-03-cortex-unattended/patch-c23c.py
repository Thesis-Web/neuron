# C23c: the pair question is for claims the shape or a print did not settle (unsettled, or a judgment cell's word); a hallucination by receipt or a completes by shape asks nothing
p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''    if asking and (len(unknown) >= 2 or no_source) and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, unknown[:8], vrun)
'''
new = '''    settled = by in ("shape", "receipt", "sources") and kind != "unsettled"   # the shape or a print already decided this claim; no meaning question
    if asking and not settled and (len(unknown) >= 2 or no_source) and kind not in ("noise", "dupe", "drift"): ask_question(name, n, run, unknown[:8], vrun)
'''
assert s.count(old) == 1; s = s.replace(old, new); open(p, "w").write(s); print("patched c23c")
