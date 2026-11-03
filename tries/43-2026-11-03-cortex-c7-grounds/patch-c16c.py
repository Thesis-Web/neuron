p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:90], s.count(old))
    s = s.replace(old, new)
# a line that differs from an earlier one only by its value is the change-of-state case: it must reach the judge, not die as a restatement
rep('''def wordset_key(s):
    return int(hashlib.sha256(" ".join(sorted(content_words(s))).encode()).hexdigest()[:15], 16)
''', '''def wordset_key(s):
    return int(hashlib.sha256(" ".join(sorted(content_words(s) | set(numbers(s)))).encode()).hexdigest()[:15], 16)
''')
# a true observation the machine confirms, outside the expected's shape, progresses the state by the receipt; a judgment cell never overrides a receipt
rep('''    if cells["words"] >= 4 and cells["new_words"] == 0 and cells["known_words"] >= 3 and not cells["observed"]: return "dupe", "sheet"   # a restatement with nothing new and nothing observed
''', '''    if cells["words"] >= 4 and cells["new_words"] == 0 and cells["known_words"] >= 3 and not cells["observed"]: return "dupe", "sheet"   # a restatement with nothing new and nothing observed
    if rb and cells.get("numbers_in") and not cells.get("numbers_out") and cells["ground"]["receipt"] >= 2: return "progresses", "receipt"   # every value printed by the machine and the receipt's own words, outside the expected's shape
''')
open(p, "w").write(s); print("patched c16c")
