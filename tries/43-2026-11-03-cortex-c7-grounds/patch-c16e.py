p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''        run = r["run"]; cx_put("source", name, k, run, clock(), json.dumps({"t": sent[:300]})); key_gates(name, run); n_typed += 1
'''
new = '''        run = r["run"]; cx_put("source", name, k, run, clock(), "{}"); key_gates(name, run); n_typed += 1   # the words are not stored again (the owner, 11-03: words do not live in the brain); the run's gates replay the sentence
'''
assert s.count(old) == 1; s = s.replace(old, new); open(p, "w").write(s); print("patched c16e")
