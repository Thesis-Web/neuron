# recall9_apply.py (tries/52): the lines of RECALL-9-nk.txt through the kernel door, one at a time, every mother reply read. Modes:
#   check <door> <file> <word> ...   reads only: the SELECT bodies of spans 4, 5 and 7 with above/what filled, per word, timed, gates read back as words
#   apply <door> <file>              types line 1 (the define run) and the two binds; prints each run and its refused count; then define's rows
#   define <door> <word> ...         types define : word for each; prints the sheet's cells (the eight new ones as words) and the say's text
#   sixth <door>                     types define unknown : 1 (the sixth sends one define into main); prints the newest run of arrival 5 and its say
#   rollback <door>                  types the two rollback lines (call = 19938199)
import json, re, sys, time, urllib.request
door = sys.argv[2]
def post(path, body):
    r = urllib.request.Request(door + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=600))
def q(sql, params=()): return post('/api/q', {'sql': sql, 'params': list(params)})
def run_of(rid): return json.load(urllib.request.urlopen(door + '/api/run?schema=main&id=%d' % rid, timeout=120))
def gate(sym):
    rows = q('SELECT gate FROM label WHERE symbol = ?', [sym]).get('rows') or []
    if not rows: raise SystemExit('no gate for ' + sym)
    return rows[0][0]
def words(gl):
    gs = [int(g) for g in str(gl or '').split() if g.isdigit()]
    if not gs: return '(none)'
    rows = q('SELECT gate, symbol FROM label WHERE gate IN (%s)' % ','.join(str(g) for g in gs[:80])).get('rows') or []
    d = dict(rows); return ' '.join(d.get(g, '?') for g in gs[:80]) + (' … %d in all' % len(gs) if len(gs) > 80 else '')
names = {7: 'wn', 8: 'gcide', 10: 'mwt', 11: 'moby', 12: 'map', 13: 'sqldoc', 14: 'measured', 15: 'guess', 443: 'wikt', 1: 'heard', 4: 'mother', 5: 'the sixth'}
CELLS = [(441, 'class'), (138, 'like'), (139, 'opposite'), (530, 'similar'), (6332, 'tense'), (5516, 'prefix'), (10547, 'suffix'), (204, 'etymology')]
RUNS = []
def typed(line):
    t = time.time(); j = post('/api/type', {'line': line}); r = j.get('result') or {}
    RUNS.append(r.get('run')); print('typed %-40s run %s, %s runs, %s hits, %s born, %s refused, %.3f s%s' % (line[:40], r.get('run'), r.get('runs'), r.get('hits'), r.get('born'), r.get('refused'), r.get('seconds') or (time.time() - t), (' ERROR ' + j['error']) if j.get('error') else ''))
    if r.get('refused'): print('  REFUSED; stopping here'); sys.exit(2)
    return r.get('run')
def builds(path): return [l.rstrip('\n') for l in open(path, encoding='utf-8') if l.startswith('BUILD')]
def spans(line): return [s.strip() for s in re.split(r'\s*BUILD\s*', line) if s.strip()]
def show_cells(rid):
    x = run_of(rid); cells = {c[0]: c for c in x.get('cells') or []}
    for g, nm in [(23, 'what'), (24, 'def')] + CELLS + [(150, 'known'), (155, 'unknown'), (25, 'say')]:
        c = cells.get(g)
        if not c: print('  cell %-5d %-10s absent' % (g, nm)); continue
        v, d = c[2], c[3]
        if g == 23: shown = '%s (%s)' % (v, words(v))
        elif g in (24, 25) and isinstance(d, dict): shown = 'run %s from %s: %s' % (d.get('run'), names.get(d.get('arrival'), d.get('arrival')), (d.get('text') or '')[:400])
        elif g in (150, 155) and isinstance(d, dict): shown = '%s words: %s' % (d.get('words'), (d.get('text') or '')[:100])
        elif g in dict(CELLS): shown = '%s  [%s]' % ((v or '')[:60] + ('…' if v and len(v) > 60 else ''), words(v))
        else: shown = str(v)[:200]
        print('  cell %-5d %-10s state %d  %s' % (g, nm, c[1], shown))
    return x
mode = sys.argv[1]
if mode == 'check':
    S = spans(builds(sys.argv[3])[0]); assert len(S) == 8, len(S)
    s4 = S[3].replace("INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , c , 1 , coalesce ( v , '' )", "SELECT c , coalesce ( v , '' )")
    s5 = S[4].replace("INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , k.c , 1 ,", "SELECT k.c ,")
    s7 = S[6]
    for w in sys.argv[4:]:
        g = gate(w); print('\n== %s (gate %d)' % (w, g))
        for label, s in (('span 4 fields', s4), ('span 5 rel', s5)):
            sql = s.replace(' what ', ' %d ' % g).replace(' above ', ' 19938199 ').rstrip(' ;')
            t = time.time(); r = q(sql); dt = time.time() - t
            if r.get('error'): print('  %s: ERROR %s' % (label, r['error'])); continue
            print('  %s: %d rows, %.3f s' % (label, len(r['rows']), dt))
            for c, v in r['rows']: print('    cell %-5d %-10s %s' % (c, dict(CELLS).get(c, '?'), words(v) if v else '(none)'))
    # the say statement on an existing define line (its cells are the old schema, so the arrays are empty but the def text and the shape show)
    for label, sql in (('span 7 say, heard', s7), ('span 7 say, the sixth', s7.replace('( SELECT arrival FROM run WHERE id = above ) = 5', '1 = 1'))):
        t = time.time(); r = q(sql.replace(' above ', ' 19938474 ').replace(' what ', ' 1317458 ').rstrip(' ;')); dt = time.time() - t
        print('  %s on run 19938474: %.3f s: %s' % (label, dt, r.get('error') or (r['rows'][0][0] or '')[:300]))
elif mode == 'apply':
    B = builds(sys.argv[3]); assert len(B) == 3, len(B)
    typed(B[0])
    for b in B[1:]: typed(b.replace('{run:1}', str(RUNS[0])))
    print('define rows now:', q('SELECT shard, before, trigger, call, times FROM dna WHERE gate = 156').get('rows'))
elif mode == 'define':
    for w in sys.argv[3:]:
        rid = typed('define : ' + w); show_cells(rid)
elif mode == 'sixth':
    before = q('SELECT max(id) FROM run WHERE arrival = 5').get('rows')[0][0]; print('newest run of arrival 5 before:', before)
    typed('define unknown : 1'); time.sleep(1)
    after = q('SELECT max(id) FROM run WHERE arrival = 5').get('rows')[0][0]; print('newest run of arrival 5 after:', after)
    if after and after != before:
        x = run_of(after)['run']; print('run %d arrival %s: %s' % (after, x.get('arrival'), (x.get('text') or '')[:80])); show_cells(after)
elif mode == 'rollback':
    typed('BUILD UPDATE dna SET call = 19938199 WHERE gate = 156 AND before = 1 AND trigger = 68 ; BUILD')
    typed('BUILD UPDATE dna SET call = 19938199 WHERE gate = 156 AND before = 5 AND trigger = 68 ; BUILD')
    print('define rows now:', q('SELECT shard, before, trigger, call, times FROM dna WHERE gate = 156').get('rows'))
