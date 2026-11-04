# C26b: negation words carry meaning and stay in the shape; an owner-line contradiction is asked about even when the claim is off this checkpoint's scope
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
rep('''        if s and (s.isdigit() or (len(s) >= 2 and s not in STOP and any(c.isalpha() for c in s))): out.append(g)
''', '''        if s and (s.isdigit() or (len(s) >= 2 and (s not in STOP or s in NEG_WORDS) and any(c.isalpha() for c in s))): out.append(g)   # C26: a negation changes the meaning, it stays in the shape
''')
rep('''    asking = (name, n) not in NO_PARTS   # a session's narration judged for the record only asks no meaning questions
    if asking and oc and kind in ("completes", "progresses", "supersedes"): ask_question(name, n, run, unknown[:8], vrun)
''', '''    asking = (name, n) not in NO_PARTS   # a session's narration judged for the record only asks no meaning questions
    if asking and oc and kind not in ("noise", "dupe"): ask_question(name, n, run, unknown[:8], vrun)   # a claim against the owner's words is asked about whatever its verdict here
''')
# NEG_WORDS must be defined before content_gates uses it: move the set next to STOP
rep('''NEG_WORDS = set("not no never none nothing nor cannot without".split())
def owner_conflict(run):
''', '''def owner_conflict(run):
''')
rep('''def content_words(s):
''', '''NEG_WORDS = set("not no never none nothing nor cannot without".split())
def content_words(s):
''')
open(p, "w").write(s); print("patched c26b")
