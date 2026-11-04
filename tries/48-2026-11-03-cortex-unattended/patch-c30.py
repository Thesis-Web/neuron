# C30 one sentence, many projects: an ingest is typed once without a project in its prefix; each project attaches itself to that run in the index with its own time and count.
# Also: the hydration's DO NOW skips a checkpoint parked on the owner or the kernel (every part left says so) so the rail moves on.
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
# 1. the typed line carries no project; the index does
rep('''        line = "cortex ingest %s : %s" % (name, s); r = typed(line); run = r["run"]; at = clock()
        cx_put("ingest", name, k, run, at, json.dumps({"times": 1, "voice": VOICE[0], "guess": bool(GUESS.search(s))})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run); key_pairs(name, run)
        out.append({"run": run, "clock": at, "born": r["born"], "seconds": r["seconds"], "same_as": 0, "again": 1, "text": s})
        if not quiet: print("ingest run %d clock %d born %d %.3fs: %s" % (run, at, r["born"], r["seconds"], s[:100]))
''', '''        held = cx_get("line", "*", k)   # C30: the sentence may already be a run, typed once by another project
        if held:
            run, at = held[0], clock(); d0 = json.loads(held[3]); d0["projects"] = sorted(set(d0.get("projects", []) + [name])); cx_put("line", "*", k, run, held[1], json.dumps(d0))
            cx_put("ingest", name, k, run, at, json.dumps({"times": 1, "voice": VOICE[0], "guess": bool(GUESS.search(s)), "attached_from": d0.get("first")})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run); key_pairs(name, run)
            out.append({"run": run, "clock": at, "born": 0, "seconds": 0.0, "same_as": 0, "again": 1, "text": s})
            if not quiet: print("ingest run %d attached to %s (typed once under %s; now %s): %s" % (run, name, d0.get("first"), ",".join(d0["projects"]), s[:100]))
            continue
        line = "cortex ingest : %s" % s; r = typed(line); run = r["run"]; at = clock()   # C30: one run, no project in the prefix; the projects live in the index
        cx_put("line", "*", k, run, at, json.dumps({"first": name, "projects": [name]}))
        cx_put("ingest", name, k, run, at, json.dumps({"times": 1, "voice": VOICE[0], "guess": bool(GUESS.search(s))})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run); key_pairs(name, run)
        out.append({"run": run, "clock": at, "born": r["born"], "seconds": r["seconds"], "same_as": 0, "again": 1, "text": s})
        if not quiet: print("ingest run %d clock %d born %d %.3fs: %s" % (run, at, r["born"], r["seconds"], s[:100]))
''')
# the repeat path types the same prefix-less line so the kernel ticks its own counter
rep('''            kr = typed("cortex ingest %s : %s" % (name, s)) if repeat_to_kernel else None''', '''            kr = typed("cortex ingest : %s" % s) if repeat_to_kernel else None''')
# 2. DO NOW skips a parked checkpoint
rep('''def next_checkpoint(name):
''', '''def parked(name, n):
    # a checkpoint whose every part left says it waits on the owner or the kernel: the rail moves past it (the owner, 11-03: keep it working)
    left = [r for r in remainders_of(name, n) if not r.get("satisfied")]
    return bool(left) and all(any(g in line_text(r["run"]) for g in GATED) for r in left)
def next_checkpoint(name):
''')
import re
m = re.search(r"def next_checkpoint\(name\):\n(.*?)\n(?=def |[A-Z_]+ = )", s, flags=re.S)
assert m, "next_checkpoint body not found"
body = m.group(1); print("next_checkpoint body:\n" + body)
open(p, "w").write(s); print("patched c30 (part 1; the parked skip needs the body above)")
