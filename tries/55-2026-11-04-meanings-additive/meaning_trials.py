# meaning_trials.py (tries/55): the owner's teaching process of tries/36 run for a set of candidate points, each a word the brain's own thesaurus rows
# relate to an acting point. For each: meaning : X (the brain proposes from its rows), the proposal read from the sheet (how 534, guess 15,
# action 3722); correct : N when the proposal is the acting point the teacher judges right by the word's sense, incorrect : N otherwise (the brain
# re-asks on that line); up to three legs. Then the adopted meaning is checked by live output: the candidate's line in the acting point's shape.
import json, sys, time, urllib.request
door = sys.argv[1]
def post(path, body):
    r = urllib.request.Request(door + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r, timeout=600))
def q(sql, params=()):
    j = post('/api/q', {'sql': sql, 'params': list(params)}); return j.get('rows') if not j.get('error') else 'ERR ' + j['error']
def run_of(rid): return json.load(urllib.request.urlopen(door + '/api/run?schema=main&id=%d' % rid, timeout=120))
def sym(g):
    r = q('SELECT symbol FROM label WHERE gate = ?', [int(g)]); return r[0][0] if r else '?%s' % g
def gate(s): r = q('SELECT gate FROM label WHERE symbol = ?', [s]); return r[0][0] if r else None
def typed(line):
    j = post('/api/type', {'line': line}); r = j.get('result') or {}
    if r.get('refused'): print('  REFUSED:', line); 
    return r
HOW = {'426': 'memory', '11865': 'relationship', '276': 'definition', '947': 'none'}
def proposal(rid):
    x = run_of(rid); cells = {c[0]: c for c in x.get('cells') or []}
    how = HOW.get(str(cells[534][2]) if 534 in cells else '', cells[534][2] if 534 in cells else None)
    guess = cells[15][2] if 15 in cells and cells[15][2] not in (None, '') else None
    action = cells[3722][2] if 3722 in cells else None
    return how, (int(guess) if guess and str(guess).isdigit() else guess), action
# candidate -> the acting point the teacher holds right for the sense the tool uses (judged from the sources' senses, written here before the run)
TRIALS = [
 ('wrong', 'incorrect'), ('false', 'incorrect'), ('mistaken', 'incorrect'), ('erroneous', 'incorrect'), ('untrue', 'incorrect'), ('inaccurate', 'incorrect'),
 ('make', 'create'), ('build', 'create'), ('produce', 'create'), ('generate', 'create'), ('construct', 'create'), ('form', 'create'), ('invent', 'create'),
 ('specify', 'define'), ('clarify', 'define'), ('explain', 'define'), ('interpret', 'define'), ('characterize', 'define'), ('delineate', 'define'),
 ('signification', 'meaning'), ('significance', 'meaning'), ('purport', 'meaning'), ('gist', 'meaning'), ('import', 'meaning'),
 ('modify', 'change'), ('vary', 'change'), ('transform', 'change'), ('convert', 'change'), ('adjust', 'change'), ('switch', 'change'),
 ('true', 'correct'), ('accurate', 'correct'), ('exact', 'correct'), ('precise', 'correct'),
 ('publish', 'print'), ('render', 'print'),
 ('list', 'type'), ('tabulate', 'type'), ('catalog', 'type'), ('transcribe', 'type'),
 # expected to be judged wrong by the teacher: the thesaurus relates them by another sense than the tool's
 ('kind', None), ('category', None), ('rectify', None), ('amend', None),
]
results = []
for word, want in TRIALS:
    g = gate(word)
    if not g: print('%-14s no gate' % word); continue
    if q('SELECT 1 FROM dna WHERE gate = ? AND call IS NOT NULL LIMIT 1', [g]): print('%-14s already acts; skipped' % word); continue
    legs = []; rid = None; outcome = 'no proposal'
    r = typed('meaning : ' + word); rid = r.get('run')
    for leg in range(3):
        how, guess, action = proposal(rid)
        gs = sym(guess) if guess else None
        legs.append('%s:%s' % (how, gs))
        if how != 'relationship' or not guess: outcome = 'no acting relative (%s)' % how; break
        if want and gs == want:
            c = typed('correct : %d' % rid); outcome = 'correct : %d adopted %s' % (rid, gs); break
        else:
            i = typed('incorrect : %d' % rid); rid = i.get('run'); outcome = 'incorrect, re-asked'
    rows = q('SELECT before, trigger, call FROM dna WHERE gate = ? AND call IS NOT NULL', [g])
    results.append((word, want, legs, outcome, rows))
    print('%-14s want %-9s legs %-45s -> %s; dna rows with a call now: %d' % (word, want, ' | '.join(legs), outcome, len(rows)))
print('\nadopted: %d of %d trials' % (sum(1 for r in results if r[3].startswith('correct')), len(results)))
json.dump(results, open('trials.json', 'w'))
