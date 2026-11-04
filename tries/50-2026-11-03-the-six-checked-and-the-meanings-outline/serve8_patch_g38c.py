# serve8_patch_g38c.py (tries/50): the history the page replays is the typed line's own receipts (the root run: the bundle lays receipts only for
# runs holding their own, r->nrc; a called or spawned run's receipts are process, the owner's order of 11-01, and the page reads them for a chosen
# line through the run request). The open set says when its first build finished and how long it took.
import sys
p = sys.argv[1]; src = open(p, encoding='utf-8').read()
def sub(old, new):
    global src
    assert src.count(old) == 1, old[:70]; src = src.replace(old, new)
sub("""    own = set(t['id'] for t in x.get('tree', []) if t.get('kept'))   # a run's own receipts; a repeated run borrows the receipts of the run it repeats and the page replays those once, under the kept run
    for h in x['hops']:
        if h[0] not in own: continue""", """    for h in x['hops']:   # the line's own receipts: the root run's (the bundle lays receipts only for runs holding their own; a called or spawned run's are process)
        if h[0] != root: continue""")
sub("""OPEN = {'runs_at': -1, 'built': 0, 'adds': 0, 'rel': None}""", """OPEN = {'runs_at': -1, 'built': 0, 'adds': 0, 'rel': None, 'done': 0, 'seconds': None}""")
sub("""        for who, l in lines: open_add(who, l['id'], l['run'])
        OPEN['runs_at'] = runs""", """        t0 = time.time()
        for who, l in lines: open_add(who, l['id'], l['run'])
        OPEN['runs_at'] = runs
        if not OPEN['done']: OPEN['done'] = 1; OPEN['seconds'] = round(time.time() - t0, 1)""")
sub("""'memerr': OPEN.get('memerr'), 'bundle_held'""", """'memerr': OPEN.get('memerr'), 'done': OPEN['done'], 'seconds': OPEN['seconds'], 'bundle_held'""")
open(p, 'w', encoding='utf-8').write(src); print('patched', p)
