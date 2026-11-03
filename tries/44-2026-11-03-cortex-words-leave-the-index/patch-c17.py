# C17 (the owner, 11-03 14:xx: words do not live in the brain): every print replays the sentence from its run's gates; ingest, part, verdict and receipt rows keep no text
import re
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
# the replay
rep('''def is_value(g): return sym_of(g).isdigit()
''', '''def is_value(g): return sym_of(g).isdigit()
_TXT = {}
def line_text(run):
    # the sentence of a run, replayed from its gates (the owner, 11-03: words do not live in the brain; the space is a gate too, so the replay is exact); the body after the typed prefix
    if run not in _TXT:
        r = "".join(sym_of(g) for g in shape_of(run)); _TXT[run] = r.split(" : ", 1)[1] if " : " in r else r
    return _TXT[run]
def receipt_line(l): return line_text(l["run"]).split(" => ", 1)[-1]
''')
# receipts: no text kept
rep('''            cells["receipt_runs"] += 1; rnums |= set(numbers(l["t"])); rwords |= set(g for g in content_gates(l["run"]) if not is_value(g)); newest = max(newest, l["run"])
''', '''            cells["receipt_runs"] += 1; rnums |= set(numbers(receipt_line(l))); rwords |= set(g for g in content_gates(l["run"]) if not is_value(g)); newest = max(newest, l["run"])
''')
rep('''" / ".join(l["t"][:60] for l in d.get("lines", [])[1:3] or d.get("lines", [])[:1])''', '''" / ".join(receipt_line(l)[:60] for l in d.get("lines", [])[1:3] or d.get("lines", [])[:1])''')
rep('''json.dumps({"n": n, "cmd": cmd, "t": l, "ts": int(time.time())})); key_gates(name, run); got.append({"run": run, "t": l})''', '''json.dumps({"n": n, "cmd": cmd, "ts": int(time.time())})); key_gates(name, run); got.append({"run": run})''')
rep('''    for x in got: print("receipt run %d %s C%d: %s => %s" % (x["run"], name, n, cmd, x["t"][:100]))
''', '''    for x in got: print("receipt run %d %s C%d: %s => %s" % (x["run"], name, n, cmd, receipt_line(x)[:100]))
''')
rep('''" / ".join(l["t"][:70] for l in d.get("lines", [])[:3])''', '''" / ".join(receipt_line(l)[:70] for l in d.get("lines", [])[:3])''')
# ingests: the index keeps the key and the count
rep('''            t, times = ingest_text(had[3]); times += 1
''', '''            times = ingest_text(had[3])[1] + 1
''')
rep('''            cx_put("ingest", name, k, had[0], had[1], json.dumps({"t": t, "times": times}))
''', '''            cx_put("ingest", name, k, had[0], had[1], json.dumps({"times": times}))
''')
rep('''                    t, times = ingest_text(first[3]); cx_put("ingest", name, int(had[3]), first[0], first[1], json.dumps({"t": t, "times": times + 1}))
''', '''                    cx_put("ingest", name, int(had[3]), first[0], first[1], json.dumps({"times": ingest_text(first[3])[1] + 1}))
''')
rep('''        cx_put("ingest", name, k, run, at, json.dumps({"t": s, "times": 1})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run)
''', '''        cx_put("ingest", name, k, run, at, json.dumps({"times": 1})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run)
''')
rep('''        text = ingest_text(rows[0][0])[0]
''', '''        text = line_text(run)
''')
rep('''    text = ingest_text(rows[0][0])[0]; r = add_part(name, n, run, text, None, "owner")''', '''    text = line_text(run); r = add_part(name, n, run, text, None, "owner")''')
rep('''feats(sheet_cells(nm, d["n"], run, ingest_text(ing[0][0])[0], pr, ck, ex))''', '''feats(sheet_cells(nm, d["n"], run, line_text(run), pr, ck, ex))''')
# parts: no text kept; rows re-put by their own key
rep('''json.dumps({"t": text, "n": n, "run": run, "times": 1, "p": p, "by": by, "ground": ground, "ts": int(time.time())})); return "added"''', '''json.dumps({"n": n, "run": run, "times": 1, "p": p, "by": by, "ground": ground, "ts": int(time.time())})); return "added"''')
rep('''    for (ts, v) in q("SELECT ts, value FROM main.cx WHERE kind = 'part' AND name = ? AND n > 0 ORDER BY ts DESC LIMIT 200", name):
        d = json.loads(v)
        if d.get("run") == old_run and d.get("n") == n and (new_run == "owner" or not d.get(why)):
            d[why] = new_run; cx_put("part", name, text_key(d["t"]), d["run"], clock(), json.dumps(d)); return True
''', '''    for (k, ts, v) in q("SELECT n, ts, value FROM main.cx WHERE kind = 'part' AND name = ? AND n > 0 ORDER BY ts DESC LIMIT 200", name):
        d = json.loads(v)
        if d.get("run") == old_run and d.get("n") == n and (new_run == "owner" or not d.get(why)):
            d[why] = new_run; cx_put("part", name, k, d["run"], clock(), json.dumps(d)); return True
''')
rep('''    for (v,) in q("SELECT value FROM main.cx WHERE kind = 'part' AND name = ? AND n > 0 ORDER BY ts DESC LIMIT 200", name):
        d = json.loads(v)
        if d.get("n") == n and d.get("superseded_by") == run:
            d.pop("superseded_by"); cx_put("part", name, text_key(d["t"]), d["run"], clock(), json.dumps(d));''', '''    for (k, v) in q("SELECT n, value FROM main.cx WHERE kind = 'part' AND name = ? AND n > 0 ORDER BY ts DESC LIMIT 200", name):
        d = json.loads(v)
        if d.get("n") == n and d.get("superseded_by") == run:
            d.pop("superseded_by"); cx_put("part", name, k, d["run"], clock(), json.dumps(d));''')
rep('''    return " | ".join(p["t"] for p in reversed(ps)) if ps else "(nothing accepted yet)"
''', '''    return " | ".join(line_text(p["run"]) for p in reversed(ps)) if ps else "(nothing accepted yet)"
''')
rep('''    for p in parts: known |= content_words(p["t"])
''', '''    for p in parts: known |= content_words(line_text(p["run"]))
''')
rep('''" | ".join("%s [%s%s | %s]" % (p["t"][:90], ''', '''" | ".join("%s [%s%s | %s]" % (line_text(p["run"])[:90], ''')
rep('''ps[0]["t"][:110] if ps else "(no part recorded)"''', '''line_text(ps[0]["run"])[:110] if ps else "(no part recorded)"''')
rep('''    part_texts = [json.loads(v).get("t", "") for (v,) in q(''', '''    part_texts = [line_text(json.loads(v).get("run") or 0) for (v,) in q(''')
s, k = re.subn(r'json\.loads\(v\)\.get\("text", ""\)\[:200\]', 'line_text(json.loads(v).get("run") or 0)[:200]', s); assert k == 1, k
# verdicts: no text kept; prints replay
rep('''"answers": answers, "sheet": cells, "part": part, "text": text[:300]}))''', '''"answers": answers, "sheet": cells, "part": part}))''')
rep('''            d = json.loads(v); lines.append("  C%s %s %.2f: %s" % (d.get("n"), d.get("kind"), d.get("p", 0), d.get("text", "")[:90]))
''', '''            d = json.loads(v); lines.append("  C%s %s %.2f: %s" % (d.get("n"), d.get("kind"), d.get("p", 0), line_text(n)[:90]))
''')
rep('''(d.get("text") or "")[:90]))''', '''line_text(run)[:90]))''')
rep('''d.get("judge"), d.get("text", "")[:70]))''', '''d.get("judge"), line_text(n)[:70]))''')
left = [l for l in s.splitlines() if ('["t"]' in l or 'get("text", "")' in l) and "b.get(\"text\"" not in l]; assert not left, left[:3]
open(p, "w").write(s); print("patched c17")
