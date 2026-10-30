# diff_brains.py: every table of two brains compared row for row (the time-of-day columns left out), so a change to the hop is judged by
# what the brain holds afterwards, not by anyone's word. usage: python3 diff_brains.py A.db B.db
import sqlite3, sys, hashlib
A, B = sys.argv[1], sys.argv[2]
SKIP_COLS = {'moment', 'at'}          # the wall clock and the clock count differ when work interleaves differently; everything else must match
def rows(db, table, cols):
    order = ', '.join(cols)
    return [tuple(r) for r in db.execute(f'SELECT {", ".join(cols)} FROM "{table}" ORDER BY {order}')]
a = sqlite3.connect(A); b = sqlite3.connect(B)
tables_a = {r[0] for r in a.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
tables_b = {r[0] for r in b.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
only_a, only_b = sorted(tables_a - tables_b), sorted(tables_b - tables_a)
same = 0; differ = []; skipped = ('hop', 'land', 'hit', 'step', 'secondary', 'out_mother', 'refused', 'input', 'third', 'out_user', 'complete', 'ended', 'build_span')
for t in sorted(tables_a & tables_b):
    if t in skipped: continue      # the transient tables: the hop's own working rows and mailboxes, which the lean hop shapes differently on purpose
    cols = [r[1] for r in a.execute(f'PRAGMA table_info("{t}")') if r[1] not in SKIP_COLS]
    cols_b = [r[1] for r in b.execute(f'PRAGMA table_info("{t}")') if r[1] not in SKIP_COLS]
    cols = [c for c in cols if c in cols_b]
    if not cols: continue
    ra, rb = rows(a, t, cols), rows(b, t, cols)
    if ra == rb: same += 1
    else:
        sa, sb = set(ra), set(rb)
        differ.append((t, len(ra), len(rb), list(sa - sb)[:3], list(sb - sa)[:3]))
print(f'tables compared: {same + len(differ)}; identical: {same}; differing: {len(differ)}')
if only_a: print('tables only in A:', only_a[:10], '...' if len(only_a) > 10 else '')
if only_b: print('tables only in B:', only_b[:10], '...' if len(only_b) > 10 else '')
for t, na, nb, da, db_ in differ: print(f'  {t}: {na} rows vs {nb}; only in A e.g. {da}; only in B e.g. {db_}')
