# the learned layer abstains while its leave-one-out accuracy is below 0.7: a coin flip must not label the owner's sentences
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''    cx_put("weights", "judge", 0, 0, clock(), json.dumps(rec)); cx_put("weights", "judge", v, 0, clock(), json.dumps(rec))
''', '''    rec["acc"] = round(hits / len(rows), 3) if rows else 0.0   # the leave-one-out accuracy travels with the weights; below 0.7 the judge does not use them
    cx_put("weights", "judge", 0, 0, clock(), json.dumps(rec)); cx_put("weights", "judge", v, 0, clock(), json.dumps(rec))
''')
rep('''            la = learned_answers(cells); lv = (weights() or {}).get("v", 0)
            if la is not None and decide(la) != "unsettled": answers, model = la, "learned v%d" % lv
''', '''            la = learned_answers(cells); W0 = weights() or {}; lv = W0.get("v", 0)
            if W0.get("acc", 1.0) < 0.7: la = None; print("  learned v%s abstains: %.2f on leave-one-out, below 0.7 (more marks needed)" % (lv, W0.get("acc", 0)))
            if la is not None and decide(la) != "unsettled": answers, model = la, "learned v%d" % lv
''')
rep('''        la = learned_answers(cells, W)
        if la is not None and decide(la) != "unsettled": given[i["run"]] = (la, "learned v%d" % W.get("v", 0))
''', '''        la = learned_answers(cells, W) if (W or {}).get("acc", 1.0) >= 0.7 else None
        if la is not None and decide(la) != "unsettled": given[i["run"]] = (la, "learned v%d" % W.get("v", 0))
''')
open(p, "w").write(s); print("patched c29b")
