# tries/58 roots_apply.py: type ROOTS-nk.txt on a brain through its door, then the example lines; every reply read back.
import json, sys, time; sys.path.insert(0, '.')
from nkdoor import Door
d = Door(sys.argv[1]); mode = sys.argv[2]
lines = [l.rstrip('\n') for l in open('ROOTS-nk.txt', encoding='utf-8')]
runs = []
if mode in ('apply', 'all'):
    for l in lines:
        if not l.startswith('BUILD'): continue
        t = d.resolve(l, runs)
        if 'NOGATE' in t: print('NO GATE in', l[:80]); sys.exit(2)
        r = d.typed(t[:60] if False else t, quiet=True); runs.append(r.get('run'))
        rep = d.sheet(r['run']).get(22)
        print('run %s %-56s refused %s reply: %s' % (r.get('run'), t[:56], r.get('refused'), (rep[1].get('text') if isinstance(rep, (list, tuple)) and isinstance(rep[1], dict) else rep)))
    json.dump(runs, open('roots_runs.json', 'w'))
if mode in ('examples', 'all'):
    ex = json.load(open('roots_examples.json'))
    # a run to read and write cells of: define : scan typed once here; R2 a second line
    r0 = d.typed('define : scan', quiet=True); R = r0['run']; r1 = d.typed('define : lookup', quiet=True); R2 = r1['run']
    print('R =', R, '(define : scan)  R2 =', R2, '(define : lookup)')
    for w, noun, line in ex:
        line = line.replace('{R2}', str(R2)).replace('{R}', str(R))
        r = d.typed(line, quiet=True); sh = d.sheet(r['run']); g = 23
        kids = d.q('SELECT id FROM run WHERE parent = ?', [r['run']])
        reps = []
        for k in kids:
            c = d.sheet(k[0]).get(22)
            if c and isinstance(c[1], dict): reps.append(str(c[1].get('text'))[:90])
        print('%-40s run %s hits %s  cell 23 = %s | replies: %s' % (line, r['run'], r.get('hits'), (str(sh.get(g))[:120] if sh.get(g) else 'absent'), reps[:3]))
