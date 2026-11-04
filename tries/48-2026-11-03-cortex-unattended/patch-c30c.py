p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''            cx_put("ingest", name, k, had[0], had[1], json.dumps({"times": times}))
'''
new = '''            try: d1 = json.loads(had[3]) if had[3] and had[3].startswith("{") else {}
            except ValueError: d1 = {}
            d1["times"] = times; cx_put("ingest", name, k, had[0], had[1], json.dumps(d1))   # the tick keeps the row's voice, guess and attachment
'''
assert s.count(old) == 1; s = s.replace(old, new); open(p, "w").write(s); print("patched c30c")
