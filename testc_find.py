# tries/59 Test C finder: the first headword (word order) with two or more WordNet verb senses whose glosses name different first grounded
# points, both senses holding a quoted example (so C21 lays a sense shard per example context), the headword a defined point with no acting row
import json, re, sqlite3, sys; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1]); acting = {int(g) for g in json.load(open('acting.json'))}
con = sqlite3.connect('file:sources/wn.db?mode=ro', uri=True)
by = {}
for word, text in con.execute("SELECT word, text FROM corpus WHERE text LIKE 'verb %' ORDER BY word, id"):
    if '_' in word or '-' in word: continue
    m = re.match(r'verb (\d+): (.*)', text); gloss = re.split(r' \[|; "', m.group(2))[0]
    has_example = '; "' in m.group(2)
    words = re.findall(r"[a-z]+", gloss.lower())
    by.setdefault(word, []).append((m.group(1), gloss, words, has_example))
found = 0
for word in sorted(by):
    senses = by[word]
    if len(senses) < 2: continue
    g = d.gate(word)
    if not g: continue
    firsts = []
    for n, gloss, words, ex in senses:
        gr = [x for x in words if d.gate(x) and d.gate(x) != g and d.gate(x) in acting]
        if gr and ex: firsts.append((n, gr[0], gr, gloss[:70]))
    if len(set(f[1] for f in firsts)) >= 2:
        rows = d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g])
        if any(r[3] or r[4] for r in rows): continue
        print(word, g, firsts); found += 1
        if found >= 6: break
