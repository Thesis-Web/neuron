# serve8_patch_g38d.py (tries/50): the door says which read made it build the bundle, so the last whole-brain read a page open makes can be found.
import sys
p = sys.argv[1]; src = open(p, encoding='utf-8').read()
def sub(old, new):
    global src
    assert src.count(old) == 1, old[:70]; src = src.replace(old, new)
sub("""    if s.startswith('SELECT p.kind, f.pull, f.rest, f.dx, f.dy, f.dz, f.mode FROM main.pull p'): return None   # the brain's own formula and pull tables answer by themselves (38 rows)
    d = bundle()
""", """    if s.startswith('SELECT p.kind, f.pull, f.rest, f.dx, f.dy, f.dz, f.mode FROM main.pull p'): return None   # the brain's own formula and pull tables answer by themselves (38 rows)
    OPEN.setdefault('bundle_by', []).append(s[:90])
    d = bundle()
""")
sub("""'done': OPEN['done'], 'seconds': OPEN['seconds'], 'bundle_held'""", """'done': OPEN['done'], 'seconds': OPEN['seconds'], 'bundle_by': OPEN.get('bundle_by', [])[:5], 'bundle_held'""")
open(p, 'w', encoding='utf-8').write(src); print('patched', p)
