# serve8_patch_g38b.py (tries/50): the open set lays only a run's own receipts (a repeated run borrows the receipts of the run it repeats and the
# bundle lays none for it: nkio.c do_bundle, r->nrc), and the memory rows of every run under a line in one keyed read (the bundle's rule: has_mem,
# not same_as).
import sys
p = sys.argv[1]; src = open(p, encoding='utf-8').read()
def sub(old, new):
    global src
    assert src.count(old) == 1, old[:70]; src = src.replace(old, new)
sub("""    for h in x['hops']:
        if h[1] == 0 and h[0] not in LIVE['first']: LIVE['first'][h[0]] = h[2]
        LIVE['rc'].append([LIVE['next'], h[0], h[2], h[3]]); LIVE['next'] += 1
    for g, v in (x.get('gates') or {}).items():
        g = int(g)
        if g not in LIVE['gates']: LIVE['gates'].add(g); LIVE['label'].append([g, v.get('s')])
    LIVE['inputs'].append([who, mail_id, run])""", """    own = set(t['id'] for t in x.get('tree', []) if t.get('kept'))   # a run's own receipts; a repeated run borrows the receipts of the run it repeats and the page replays those once, under the kept run
    for h in x['hops']:
        if h[0] not in own: continue
        if h[1] == 0 and h[0] not in LIVE['first']: LIVE['first'][h[0]] = h[2]
        LIVE['rc'].append([LIVE['next'], h[0], h[2], h[3]]); LIVE['next'] += 1
    for g, v in (x.get('gates') or {}).items():
        g = int(g)
        if g not in LIVE['gates']: LIVE['gates'].add(g); LIVE['label'].append([g, v.get('s')])
    LIVE['inputs'].append([who, mail_id, run])
    ids = [t['id'] for t in x.get('tree', [])]
    if ids:   # the memory rows of every run under the line, one keyed read (the kernel answers run_memory by run)
        mr = q('SELECT run, gate, shard, input FROM main.run_memory WHERE run IN (%s)' % ','.join(str(i) for i in ids[:400]), [])
        for m in (mr or {}).get('rows') or []: LIVE['memrows'].append(m)
        if (mr or {}).get('error'): OPEN['memerr'] = mr['error']""")
sub("""    for c in x.get('cells') or []:   # the line's output: its root's sheet cells with a value (the owner, 10-26: output to the user comes from the same memory table)
        if c[1] == 1 and c[2] is not None: LIVE['out'].append([LIVE['next'], root, c[0], c[2]]); LIVE['next'] += 1
    for m in (q('SELECT run, gate, shard, input FROM main.run_memory WHERE run = ?', [root]) or {}).get('rows') or []: LIVE['memrows'].append(m)
""", """    for c in x.get('cells') or []:   # the line's output: its root's sheet cells with a value (the owner, 10-26: output to the user comes from the same memory table)
        if c[1] == 1 and c[2] is not None: LIVE['out'].append([LIVE['next'], root, c[0], c[2]]); LIVE['next'] += 1
""")
sub("""'memrows': len(LIVE['memrows']), 'bundle_held': BUNDLE['d'] is not None}""", """'memrows': len(LIVE['memrows']), 'memerr': OPEN.get('memerr'), 'bundle_held': BUNDLE['d'] is not None}""")
open(p, 'w', encoding='utf-8').write(src); print('patched', p)
