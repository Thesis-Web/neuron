p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''        d["times"] = d.get("times", 1) + 1; d.pop("rejected_by", None)   # accepted again: back in the state (a superseded part stays superseded)
'''
new = '''        d["times"] = d.get("times", 1) + 1; d.pop("rejected_by", None)   # accepted again: back in the state (a superseded part stays superseded)
        if p is not None and d.get("p") is None: d["p"], d["by"] = p, by      # a part judged before C15 gets its confidence and judge on its next judgment
        if ground and not d.get("ground"): d["ground"] = ground               # and its ground (C16)
'''
assert s.count(old) == 1; s = s.replace(old, new); open(p, "w").write(s); print("patched c16d")
