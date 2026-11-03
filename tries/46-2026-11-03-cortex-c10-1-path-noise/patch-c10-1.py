# C10.1 (the cortex's NEXT WORK, 11-03 16:5x): the path rule drops a sentence that merely holds two slash tokens; markup leaks into kept sentences. And the receipt cap of 40 lines dropped a print's summary line.
p = "/home/james/cortex/cortex.py"; s = open(p).read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, ("not found or not unique", old[:100], s.count(old))
    s = s.replace(old, new)
# markup: emphasis and heading or bullet marks come off before the split, so "**contract.** satisfied: ..." splits into "contract." (too few words) and the sentence
rep('''    text = re.sub(r"```[a-zA-Z0-9_-]*\\n?(.*?)```", lambda m: "\\n\\x01" + " ; ".join(l.strip() for l in m.group(1).splitlines() if l.strip()) + "\\n", text, flags=re.S)
    parts = re.split(r"(?<=[.!?])\\s+|\\n+", text)
''', '''    text = re.sub(r"```[a-zA-Z0-9_-]*\\n?(.*?)```", lambda m: "\\n\\x01" + " ; ".join(l.strip() for l in m.group(1).splitlines() if l.strip()) + "\\n", text, flags=re.S)
    text = re.sub(r"\\*\\*|__|~~", "", text)                                   # emphasis marks are markup, not words (C10.1)
    text = re.sub(r"(?m)^[ \\t]*(?:#{1,6}|[-*\\u2022]|\\d{1,2}[.)])[ \\t]+", "", text)   # a heading or bullet mark in front of a sentence
    parts = re.split(r"(?<=[.!?])\\s+|\\n+", text)
''')
# the path rule: a path token has a word character next to its slash (a bare / or -h is not a path); a line is a path line when it starts with one,
# or when two or more paths leave fewer than four words beside them
rep('''    toks = t.split(); filey = [x for x in toks if "/" in x or re.match(r"^[\\w.-]+\\.(txt|py|sh|md|db|json|log|html|c|h|so|map|jsonl|service)$", x)]
    if toks and (toks[0] in filey or len(filey) >= 2): return "path"
''', '''    toks = t.split(); filey = [x for x in toks if ("/" in x and re.search(r"\\w/|/\\w", x)) or re.match(r"^[\\w.-]+\\.(txt|py|sh|md|db|json|log|html|c|h|so|map|jsonl|service)$", x)]
    if toks and toks[0] in filey: return "path"
    if len(filey) >= 2 and len(content_words(" ".join(x for x in toks if x not in filey))) < 4: return "path"   # C10.1: a sentence that names two paths among its words is a sentence
''')
# the receipt keeps up to 80 lines of a print (40 dropped the summary line of cortex verdicts --limit 40)
rep('''    for l in lines[:40]:
        body = "%s => %s" % (cmd, l)
''', '''    for l in lines[:80]:
        body = "%s => %s" % (cmd, l)
''')
open(p, "w").write(s); print("patched c10.1")
