# judge_guesses.py (tries/55): the teacher's judgement of the formula's guesses with the owner's own tools (tries/36): meaning : X asks the brain
# (it answers from memory now, its own rows), correct : N confirms (belief correct +1), incorrect : N marks against (belief incorrect +1) and the
# brain re-asks on that line; when the re-ask proposes a root the teacher holds right for the word, correct : <that run>. A word the teacher cannot
# judge from the tool's sense is left as the brain's guess (belief 0/0). The judgements, by the sense each tool uses, written before the run:
import json, sys, urllib.request
door = sys.argv[1]
RIGHT = {  # the guess stands: the word, in the sense the tool uses, does what the root does
 'become': 'change', 'deform': 'change', 'exchange': 'change', 'interchange': 'change', 'modulate': 'change', 'reform': 'change', 'restructure': 'change', 'reverse': 'change', 'shift': 'change', 'transfigure': 'change', 'transpose': 'change', 'translate': 'change', 'convert': 'change',
 'assemble': 'create', 'compound': 'create', 'constitute': 'create', 'design': 'create', 'forge': 'create', 'manufacture': 'create', 'sculpt': 'create',
 'determine': 'define', 'intent': 'meaning', 'mimeograph': 'print', 'overprint': 'print', 'reissue': 'print', 'inscribe': 'print'}
WRONG = {  # the guess is wrong: another sense tied them (movement, manners, a noun, a photograph)
 'advance': 'change', 'assimilation': 'change', 'break': 'change', 'chop': 'change', 'difference': 'change', 'go': 'change', 'make': 'change', 'move': 'change', 'relief': 'change', 'return': 'change', 'revolution': 'change', 'run': 'change', 'swerve': 'change', 'tergiversate': 'change', 'travel': 'change', 'veer': 'change', 'vicissitude': 'change',
 'chasten': 'correct', 'decent': 'correct', 'emend': 'correct', 'mannerly': 'correct', 'received': 'correct', 'rectify': 'correct',
 'cut': 'create', 'do': 'create', 'prepare': 'create', 'rude': 'incorrect', 'resolve': 'meaning', 'blowup': 'print',
 'get': 'step', 'peg': 'step', 'proceeding': 'step', 'remove': 'step', 'rung': 'step', 'stair': 'step', 'stamp': 'step'}
ALSO_RIGHT = {'make': 'create'}   # if the re-ask proposes this root, it is right
# left as guesses (the teacher cannot judge from the tool's sense alone): commutation commute conversion modification mutation reversal transformation transition variation just nice model organize raise sculpture tailor construction designation blueprint footstep leap
def post(path, body):
    r = urllib.request.Request(door + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r, timeout=600))
def q(sql, params=()):
    j = post('/api/q', {'sql': sql, 'params': list(params)}); return j.get('rows') if not j.get('error') else 'ERR ' + j['error']
def run_of(rid): return json.load(urllib.request.urlopen(door + '/api/run?schema=main&id=%d' % rid, timeout=120))
def gate(s): r = q('SELECT gate FROM label WHERE symbol = ?', [s]); return r[0][0] if r else None
def sym(g): r = q('SELECT symbol FROM label WHERE gate = ?', [int(g)]); return r[0][0] if r else '?'
def typed(line): return post('/api/type', {'line': line})['result']
HOW = {'426': 'memory', '11865': 'relationship', '276': 'definition', '947': 'none'}
def proposal(rid):
    cells = {c[0]: c for c in run_of(rid).get('cells') or []}
    how = HOW.get(str(cells[534][2]) if 534 in cells else '', None); guess = cells[15][2] if 15 in cells and cells[15][2] not in (None, '') else None
    return how, (sym(guess) if guess and str(guess).isdigit() else None)
laid = q('SELECT gate, other FROM tried WHERE outcome = 2')
words = {sym(g): sym(k) for g, k in laid}
confirmed = marked = left = 0; recovered = []
for w, root in sorted(words.items()):
    if w in RIGHT and RIGHT[w] == root:
        r = typed('meaning : ' + w); how, gs = proposal(r['run']); c = typed('correct : %d' % r['run']); confirmed += 1
        print('%-14s %-9s meaning answered %s %s -> correct : %d' % (w, root, how, gs, r['run']))
    elif w in WRONG and WRONG[w] == root:
        r = typed('meaning : ' + w); how, gs = proposal(r['run']); i = typed('incorrect : %d' % r['run']); marked += 1
        how2, gs2 = proposal(i['run'])
        extra = ''
        if how2 == 'relationship' and gs2 and ALSO_RIGHT.get(w) == gs2:
            typed('correct : %d' % i['run']); recovered.append((w, gs2)); extra = '; the re-ask proposed %s -> correct : %d' % (gs2, i['run'])
        else: extra = '; the re-ask: %s %s (left)' % (how2, gs2)
        print('%-14s %-9s meaning answered %s %s -> incorrect : %d%s' % (w, root, how, gs, r['run'], extra))
    else:
        left += 1; print('%-14s %-9s left as the brain\'s guess' % (w, root))
print('\nconfirmed %d, marked wrong %d, left as guesses %d, recovered by the re-ask: %s' % (confirmed, marked, left, recovered))
print('belief now: rows %s, correct>0 %s, incorrect>0 %s, 0/0 %s' % (q('SELECT count(*) FROM belief')[0][0], q('SELECT count(*) FROM belief WHERE correct > 0')[0][0], q('SELECT count(*) FROM belief WHERE incorrect > 0')[0][0], q('SELECT count(*) FROM belief WHERE correct = 0 AND incorrect = 0')[0][0]))
