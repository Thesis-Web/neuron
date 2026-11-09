# tries/59 Phase B, the selection method (documented in CRITERIA.md): over the test brain's own copy of WordNet (sources/wn.db, read only),
# every verb sense whose gloss (the text after 'verb N: ' up to the first bracketed field or quoted example) names two or more distinct
# grounded words (points with an acting dna row on the test brain, read by key), where the headword itself is a defined point with no
# acting row and no belief or tried row. Printed in order of the count, then the word. I name no word.
import json, re, sqlite3, sys; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1]); roots = set('read find write move copy link split join select insert update delete store recall stamp append compare set measure fetch run'.split())
acting = {int(g): rows for g, rows in json.load(open('acting.json')).items()}
labels = {d.sym(g): g for g in acting}
judged = set(r[0] for r in d.q('SELECT DISTINCT gate FROM belief')) | set(r[0] for r in d.q('SELECT DISTINCT gate FROM tried'))
grounded_live = set(w for w in labels if w not in roots); grounded_all = set(labels)
con = sqlite3.connect('file:sources/wn.db?mode=ro', uri=True)
out = []
for word, text in con.execute("SELECT word, text FROM corpus WHERE text LIKE 'verb %'"):
    m = re.match(r'verb (\d+): (.*)', text)
    if not m: continue
    gloss = re.split(r' \[|; "', m.group(2))[0]
    words = re.findall(r"[a-z]+", gloss.lower())
    hit_live = [w for w in words if w in grounded_live]; hit_all = [w for w in words if w in grounded_all]
    if len(set(hit_live)) >= 2 or len(set(hit_all)) >= 2: out.append((len(set(hit_live)), len(set(hit_all)), word, m.group(1), gloss[:90], hit_live, hit_all))
out.sort(key=lambda x: (-x[0], -x[1], x[2]))
print('verb senses with two or more grounded words in the gloss: %d (live-grounded only: %d)' % (len(out), sum(1 for o in out if o[0] >= 2)))
print('%-5s %-4s %-14s %-3s %-90s %s' % ('live', 'all', 'word', 'n', 'gloss', 'grounded words'))
kept = 0
for live, alln, word, n, gloss, hl, ha in out[:120]:
    g = d.gate(word); nodes = d.q('SELECT count(*) FROM node WHERE gate = ?', [g])[0][0] if g else 0
    act = any(r[3] or r[4] for r in d.q('SELECT shard, before, trigger, call, spawn FROM dna WHERE gate = ?', [g])) if g else False
    flag = 'ACTS' if act else ('judged' if g in judged else ('undef' if not g or nodes == 0 else 'ok'))
    print('%-5d %-4d %-14s %-3s %-90s %s | %s %s' % (live, alln, word, n, gloss, hl if live >= 2 else ha, flag, nodes))
