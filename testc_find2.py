# tries/59 Test C finder, H1a: the first headwords (word order) with two or more WordNet verb senses whose glosses name different first
# believed points (belief correct > 0 on the live brain, read only on 8058), each of those senses holding a quoted example that contains the
# headword itself (so C21 lays a sense shard keyed by that example's context); the headword a defined point with no acting row
import re, sqlite3, sys; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1]); believed = set(g for g, in d.q('SELECT DISTINCT gate FROM belief WHERE correct > 0'))
con = sqlite3.connect('file:sources/wn.db?mode=ro', uri=True)
by = {}
for word, text in con.execute("SELECT word, text FROM corpus WHERE text LIKE 'verb %' ORDER BY word, id"):
    if not re.fullmatch(r'[a-z]+', word): continue
    m = re.match(r'verb (\d+): (.*)', text); body = m.group(2); gloss = re.split(r' \[|; "', body)[0]
    examples = re.findall(r'"([^"]+)"', body.split(' [')[0])
    own = [e for e in examples if re.search(r'\b' + word + r'\b', e)]
    by.setdefault(word, []).append((m.group(1), gloss, re.findall(r"[a-z]+", gloss.lower()), own))
found = 0
for word in sorted(by):
    senses = by[word]
    if len(senses) < 2: continue
    g = d.gate(word)
    if not g: continue
    firsts = []
    for n, gloss, words, own in senses:
        gr = [x for x in words if d.gate(x) and d.gate(x) != g and d.gate(x) in believed]
        if gr and own: firsts.append((n, gr[0], own[0][:60], gloss[:60]))
    if len(set(f[1] for f in firsts)) >= 2:
        if any(r[3] or r[4] for r in d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g])): continue
        print(word, g, firsts); found += 1
        if found >= 5: break
