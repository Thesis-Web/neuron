# serve8_patch_g38e.py (tries/50): the told read answers from newest before any bundle is built; the history holds the receipts of every run under
# a line that holds its own (same_as 0: the bundle's r->nrc rule; a run that repeats an earlier one borrows and lays none); ids from 1 as before.
import sys
p = sys.argv[1]; src = open(p, encoding='utf-8').read()
def sub(old, new):
    global src
    assert src.count(old) == 1, old[:70]; src = src.replace(old, new)
told = """    if s.startswith("SELECT 'told', t.run,"):
        rows = []
        for who, key in (('told', 'sixth'), ('asked main', 'main')):
            n = ask('newest ' + key + ' 400')
            for l in n.get('told', []): rows.append([who, l['run'], l['text'], None])
        return {'cols': [], 'rows': rows}
"""
sub(told, "")
sub("""    OPEN.setdefault('bundle_by', []).append(s[:90])
    d = bundle()
""", told + """    OPEN.setdefault('bundle_by', []).append(s[:90])
    d = bundle()
""")
sub("""    for h in x['hops']:   # the line's own receipts: the root run's (the bundle lays receipts only for runs holding their own; a called or spawned run's are process)
        if h[0] != root: continue""", """    own = set(t['id'] for t in x.get('tree', []) if not t.get('same_as'))   # the runs under the line that hold their own receipts (the bundle's rule, r->nrc); a run that repeats an earlier one borrows that run's and lays none
    for h in x['hops']:
        if h[0] not in own: continue""")
sub("""            LIVE['base'] = []; LIVE['next'] = (st.get('receipts') or 0) + 1   # ids after every receipt the kernel holds, so the ids only go forward""",
    """            LIVE['base'] = []; LIVE['next'] = 1   # the history's ids count from 1 as the bundle's did; a page open before this door restarted reads on from where it was""")
open(p, 'w', encoding='utf-8').write(src); print('patched', p)
