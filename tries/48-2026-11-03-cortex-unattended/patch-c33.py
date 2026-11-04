# C33 (the owner, 11-03 22:4x): a value the machine printed holds, it is not progress by itself (progress needs the expected output); a guess is marked at the paragraph, not the sentence slice
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
# 1. holds: a printed value outside the expected's shape is true and adds no part; progresses by receipt needs the expected's shape
rep('''    if rb and cells.get("numbers_in") and not cells.get("numbers_out") and cells["ground"]["receipt"] >= 2 and (cells.get("receipt_named") or cells.get("numbers_in_ext") or cells.get("shape_expected", 0) >= 0.3): return "progresses", "receipt"   # every value printed by the machine, by a claim about that print (C22: a cortex print of its own verdicts does not count)
''', '''    if rb and cells.get("numbers_in") and not cells.get("numbers_out") and cells["ground"]["receipt"] >= 2 and (cells.get("receipt_named") or cells.get("numbers_in_ext") or cells.get("shape_expected", 0) >= 0.3):
        return ("progresses" if cells.get("shape_expected", 0) >= 0.3 else "holds"), "receipt"   # C33 (the owner): a printed value holds; it is progress only when it speaks to the expected output
''')
rep('''MARKS = set(LABEL_Q) | {"dupe", "noise", "unsettled"}''', '''MARKS = set(LABEL_Q) | {"dupe", "noise", "unsettled", "holds", "guess"}''')
rep('''    accepting = kind in ("completes", "progresses", "supersedes") and (name, n) not in NO_PARTS
''', '''    accepting = kind in ("completes", "progresses", "supersedes") and (name, n) not in NO_PARTS   # holds adds no part: true, not progress (C33)
''')
rep('''    if kind in ("completes", "progresses", "supersedes") and by in ("receipt", "shape", "sources"): return "confirmed"
''', '''    if kind in ("completes", "progresses", "supersedes", "holds") and by in ("receipt", "shape", "sources"): return "confirmed"
''')
rep('''    if by == "receipt" and kind in ("completes", "progresses", "supersedes"): return 1.0, "the machine's print"
''', '''    if by == "receipt" and kind in ("completes", "progresses", "supersedes", "holds"): return 1.0, "the machine's print"
''')
rep('''    elif by in ("shape", "receipt", "sources"): p = cells["shape_expected"] if kind == "completes" else 1.0
''', '''    elif by in ("shape", "receipt", "sources"): p = cells["shape_expected"] if kind in ("completes", "progresses") else 1.0
''')
# 2. the guess is marked at the paragraph: a paragraph that says it is guessing, or gives an example, marks every sentence in it
rep('''GUESS = re.compile(r"\\b(i am guessing|i guess|my guess|a guess|guessing here|i think|maybe|perhaps|probably|not sure)\\b")
''', '''GUESS = re.compile(r"\\b(i am guessing|i guess|my guess|a guess|guessing here|i think|maybe|perhaps|probably|not sure|likely|for example|an example|example|e\\.g\\.|hypothesis|hypothetically|should be able to)\\b")
GUESS_PARA = set()   # C33: the sentences of a paragraph that says it is guessing or gives an example; filled by v_ingest per text, read per sentence
''')
rep('''def v_ingest(name, text, quiet=False, repeat_to_kernel=True):
    ensure_cx(); out = []; t0 = time.time()
''', '''def v_ingest(name, text, quiet=False, repeat_to_kernel=True):
    ensure_cx(); out = []; t0 = time.time()
    GUESS_PARA.clear()
    for para in re.split(r"\\n\\s*\\n|\\n", text):
        if GUESS.search(para.lower()):
            for s0 in sentences(para): GUESS_PARA.add(text_key(s0))
''')
rep('''        cx_put("ingest", name, k, run, at, json.dumps({"times": 1, "voice": VOICE[0], "guess": bool(GUESS.search(s))})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run); key_pairs(name, run)
        out.append({"run": run, "clock": at, "born": r["born"], "seconds": r["seconds"], "same_as": 0, "again": 1, "text": s})
''', '''        cx_put("ingest", name, k, run, at, json.dumps({"times": 1, "voice": VOICE[0], "guess": bool(GUESS.search(s)) or (k in GUESS_PARA)})); cx_put("restate", name, wordset_key(s), run, at, str(k)); key_gates(name, run); key_pairs(name, run)
        out.append({"run": run, "clock": at, "born": r["born"], "seconds": r["seconds"], "same_as": 0, "again": 1, "text": s})
''')
rep('''            cx_put("ingest", name, k, run, at, json.dumps({"times": 1, "voice": VOICE[0], "guess": bool(GUESS.search(s)), "attached_from": d0.get("first")}))''', '''            cx_put("ingest", name, k, run, at, json.dumps({"times": 1, "voice": VOICE[0], "guess": bool(GUESS.search(s)) or (k in GUESS_PARA), "attached_from": d0.get("first")}))''')
open(p, "w").write(s); print("patched c33")
