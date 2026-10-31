#!/usr/bin/env python3
# agree.py (2026-10-30): the agreement test, line by line. The same sixty lines typed into v6 (tries/19 brain.db) and into the kernel; for each
# line, its run in each brain is compared by EFFECT, not by number: the text of the run, the receipts of the run itself (by symbol), the sheet
# (cells by name, a run-number value read back as that run's text), the runs under it (by kind, arrival and text; born runs counted apart,
# since the kernel's born line is one statement), the out rows. Then the whole brain: every neuron's shards by symbol with call and spawn
# read back as the text of the run they point at, the memories, the relationship rows, the definition nodes. Nothing is hidden: a line whose
# text was changed for the kernel (gate tables addressed as dna rows) is marked and its own receipts are not compared.
import sqlite3, sys, re
VA, VB, LA, LB, FA, FB, WHICH = sys.argv[1:8]   # v6 brain.db, kernel brain.db, v6 ledger, kernel ledger, v6 lines file, kernel lines file, main|sixth
a = sqlite3.connect(VA); b = sqlite3.connect(VB)
def rows(db, sql, *p): return [tuple(r) for r in db.execute(sql, p)]
syma = dict(rows(a, "SELECT gate, symbol FROM label")); symb = dict(rows(b, "SELECT gate, symbol FROM label"))
def ledger_runs(path):
    out = []
    for l in open(path, encoding='utf-8'):
        m = re.match(r'\| (\d+) \| (\w+) \| `?.*?`? \| (\d+) \|', l)
        if m: out.append((int(m.group(1)), m.group(2), int(m.group(3))))
    return out
ra, rb = ledger_runs(LA), ledger_runs(LB)
assert len(ra) == len(rb) == 60, (len(ra), len(rb))
def lines_of(path): return [l.rstrip('\n') for l in open(path, encoding='utf-8') if l.strip() and not l.startswith('#')]
la, lb = lines_of(FA), lines_of(FB)
PRELAID = {'INSERT', 'INTO', 'neuron', 'gate', 'VALUES', 'dna'}   # the kernel's egg hand-lays its born line's words, as v6's egg lays its own
def mask(t): return re.sub(r'\d+', '#', t)
class B:
    def __init__(s, db, sym, name): s.db, s.sym, s.name = db, sym, name; s._born_parents = []
    def S(s, g): return None if g is None else s.sym.get(g, f'?{g}')
    def text(s, run): return ''.join(s.S(g) for (g,) in rows(s.db, "SELECT gate FROM seq WHERE run = ? ORDER BY pos", run))
    def run(s, run): r = rows(s.db, "SELECT arrival, parent, kind, cell, about FROM run WHERE id = ?", run); return r[0] if r else None
    def canonical(s, run):
        # the kernel (2026-10-30, the owner's shape): a run that repeats an earlier identical run stores no receipts of its own and points at it
        try: r = rows(s.db, "SELECT same_as FROM run WHERE id = ?", run)
        except Exception: return run
        return r[0][0] if r and r[0][0] else run
    def receipts(s, run):
        run = s.canonical(run)
        out = [(p, s.S(g)) for (p, g) in rows(s.db, "SELECT pos, gate FROM run_receipt WHERE run = ? ORDER BY id", run)]
        # v6 bears INSERT, INTO ... with a born hop (pos p, 'born') before landing on them; the kernel's egg has them: that hop is left out of v6's list
        if s.name == 'v6':
            seqs = dict(rows(s.db, "SELECT pos, gate FROM seq WHERE run = ?", run)); out2 = []
            for i, (p, g) in enumerate(out):
                nxt = s.S(seqs.get(p + 1)); nxt2 = s.S(seqs.get(p + 2))
                if g == 'born' and i + 1 < len(out) and out[i + 1][1] in PRELAID and out[i + 1][0] == p + 1: continue
                if g == 'born' and i + 1 < len(out) and out[i + 1][1] == ' ' and i + 2 < len(out) and out[i + 2][1] in PRELAID: continue
                out2.append((p, g))
            out = out2
        return [(p, '#' if (g or '').isdigit() else g) for (p, g) in out]
    def value(s, cell, v):
        if v is None: return None
        c = s.S(cell)
        if c in ('me', 'above', 'reply', 'def', 'say', 'remember', 'shape') and str(v).isdigit() and int(v) > 0:
            r = s.run(int(v)); return f"<{s.S(r[0]) if r else '?'}: {mask(s.text(int(v))[:100])}>"
        if c in ('known', 'unknown'): return ' '.join(s.S(int(x)) for x in str(v).split())
        if c in ('what', 'newgate', 'from', 'to') and str(v).isdigit(): return s.S(int(v))
        return str(v)
    def sheet(s, run): return sorted((s.S(c), st, s.value(c, v)) for (c, st, v) in rows(s.db, "SELECT cell, state, value FROM run_sheet WHERE run = ?", run))
    def subtree(s, run):
        out = {}; s._born_parents = []
        for (i, arr, kind, par, cell) in rows(s.db, "SELECT id, arrival, kind, parent, cell FROM run WHERE root = ? AND id != ?", run, run):
            t = s.text(i); first = t.split(' ')[0] if t else ''
            born = first == 'BUILD' and ('CREATE TABLE "newgate"' in t or 'INSERT INTO neuron' in t or 'INSERT INTO sixth.neuron' in t)
            if born: s._born_parents.append(par)
            key = ('born run' if born else (kind, s.S(arr), s.S(cell), mask(t[:90])))
            out[key] = out.get(key, 0) + 1
        return out
    def outs(s, run): return [(s.S(c), s.value(c, v)) for (c, v) in rows(s.db, "SELECT cell, value FROM out_user WHERE run = ? ORDER BY id", run)]
A, Bk = B(a, syma, 'v6'), B(b, symb, 'kernel')
same_lines = 0; agree = {'receipts': 0, 'sheet': 0, 'subtree': 0, 'out': 0}; disagree = []
for k in range(60):
    (ka, pa, runa), (kb, pb, runb) = ra[k], rb[k]
    if pa != WHICH: continue
    changed = la[k] != lb[k]
    ta, tb = A.text(runa), Bk.text(runb)
    notes = []
    if not changed:
        same_lines += 1
        if mask(ta) != mask(tb): notes.append(f"text: v6 {ta[:80]!r} kernel {tb[:80]!r}")
        if A.receipts(runa) == Bk.receipts(runb): agree['receipts'] += 1
        else:
            x, y = A.receipts(runa), Bk.receipts(runb); d = next(((i, p, q) for i, (p, q) in enumerate(zip(x, y)) if p != q), ('len', len(x), len(y))); notes.append(f"receipts differ at {d}")
    sa, sb = A.sheet(runa), Bk.sheet(runb)
    if sa == sb: agree['sheet'] += 1
    else: notes.append(f"sheet: only v6 {[x for x in sa if x not in sb][:4]} only kernel {[x for x in sb if x not in sa][:4]}")
    ua, ub = A.subtree(runa), Bk.subtree(runb)
    if ua == ub: agree['subtree'] += 1
    else:
        dif = [(key, ua.get(key, 0), ub.get(key, 0)) for key in set(ua) | set(ub) if ua.get(key, 0) != ub.get(key, 0)]
        notes.append(f"subtree: v6 {sum(ua.values())} runs, kernel {sum(ub.values())}; differing {dif[:5]}")
    oa, ob = A.outs(runa), Bk.outs(runb)
    if oa == ob: agree['out'] += 1
    else: notes.append(f"out: v6 {oa[:6]} kernel {ob[:6]}")
    if notes: disagree.append((k + 1, 'changed text' if changed else 'same text', runa, runb, la[k][:70], notes))
print(f"{WHICH} lines: {sum(1 for x in ra if x[1] == WHICH)}; with the same text in both: {same_lines}; receipts identical on {agree['receipts']} of them; sheets identical on {agree['sheet']}; subtrees identical on {agree['subtree']}; out identical on {agree['out']} (of all main lines)")
for d in disagree: print(f"\nline {d[0]} ({d[1]}; v6 run {d[2]}, kernel run {d[3]}): {d[4]}"); [print('   -', n) for n in d[5]]
# the whole brain
def shards(X):
    out = []
    if X.name == 'v6':
        for (n,) in rows(X.db, "SELECT name FROM sqlite_master WHERE type = 'table' AND name GLOB '[0-9]*' AND name NOT GLOB '*.node'"):
            for (bf, tr, call, spawn, times) in rows(X.db, f'SELECT before, trigger, call, spawn, times FROM "{n}"'): out.append((X.S(int(n)), X.S(bf), X.S(tr), X.text(call)[:60] if call else None, X.text(spawn)[:60] if spawn else None, times))
    else:
        for (g, bf, tr, call, spawn, times) in rows(X.db, "SELECT gate, before, trigger, call, spawn, times FROM dna"): out.append((X.S(g), X.S(bf), X.S(tr), X.text(call)[:60] if call else None, X.text(spawn)[:60] if spawn else None, times))
    return out
born_words = set('CREATE TABLE " newgate ( shard INTEGER PRIMARY KEY , before trigger call spawn times ) ; . node id source run INSERT INTO neuron gate VALUES dna sixth'.split())
digit = lambda t: t is not None and t.isdigit()
sa = [(x[0], x[1], x[2], mask(x[3]) if x[3] else None, mask(x[4]) if x[4] else None, x[5]) for x in shards(A) if x[0] not in born_words and x[0] != ' ' and not digit(x[0]) and not digit(x[1]) and not digit(x[2])]; sb = [(x[0], x[1], x[2], mask(x[3]) if x[3] else None, mask(x[4]) if x[4] else None, x[5]) for x in shards(Bk) if x[0] not in born_words and x[0] != ' ' and not digit(x[0]) and not digit(x[1]) and not digit(x[2])]
Sa, Sb = set(sa), set(sb)
print(f"\nshards (born-line words, the space and the digits left out; call and spawn as the text of the run they point at, run numbers masked): v6 {len(sa)}, kernel {len(sb)}; same {len(Sa & Sb)}; only v6 {len(Sa - Sb)}; only kernel {len(Sb - Sa)}")
for x in sorted(Sa - Sb, key=str)[:12]: print('   only v6    ', x)
for x in sorted(Sb - Sa, key=str)[:12]: print('   only kernel', x)
ma = set((' '.join(A.S(int(x)) for x in inp.split()), src, A.S(g)) for (inp, src, g) in rows(a, "SELECT input, source, gate FROM run_memory") if inp); mb = set((' '.join(Bk.S(int(x)) for x in inp.split()), src, Bk.S(g)) for (inp, src, g) in rows(b, "SELECT input, source, gate FROM run_memory") if inp)
ma2 = set((mask(x[0]), x[1], x[2]) for x in ma if not x[0].startswith('BUILD CREATE TABLE " newgate')); mb2 = set((mask(x[0]), x[1], x[2]) for x in mb if not x[0].startswith('BUILD INSERT INTO neuron') and not x[0].startswith('BUILD INSERT INTO sixth . neuron'))
print(f"memories (born runs left out): v6 {len(ma2)} distinct, kernel {len(mb2)}; only v6 {len(ma2 - mb2)}, only kernel {len(mb2 - ma2)}")
for x in sorted(ma2 - mb2, key=str)[:6]: print('   only v6    ', (x[0][:70], x[1], x[2]))
for x in sorted(mb2 - ma2, key=str)[:6]: print('   only kernel', (x[0][:70], x[1], x[2]))
has_rel = lambda db: db.execute("SELECT 1 FROM sqlite_master WHERE name = 'rel'").fetchone()
rla = set((A.S(g), A.S(k), A.S(o)) for (g, k, o) in rows(a, "SELECT gate, kind, other FROM rel")) if has_rel(a) else set(); rlb = set((Bk.S(g), Bk.S(k), Bk.S(o)) for (g, k, o) in rows(b, "SELECT gate, kind, other FROM rel")) if has_rel(b) else set()
print(f"rel: v6 {len(rla)}, kernel {len(rlb)}; identical: {rla == rlb}; only v6 {sorted(rla - rlb)[:5]} only kernel {sorted(rlb - rla)[:5]}")
na = {}
for (n,) in rows(a, "SELECT name FROM sqlite_master WHERE name GLOB '[0-9]*.node'"):
    g = int(n.split('.')[0]); na[A.S(g)] = sorted((A.S(s), A.text(r)[:60]) for (s, r) in rows(a, f'SELECT source, run FROM "{n}"'))
nb = {}
for (g, s, r) in rows(b, "SELECT gate, source, run FROM node"): nb.setdefault(Bk.S(g), []).append((Bk.S(s), Bk.text(r)[:60]))
nb = {k: sorted(v) for k, v in nb.items()}; na = {k: v for k, v in na.items() if v}
print(f"definition nodes: v6 {len(na)} neurons with rows ({sum(len(v) for v in na.values())} rows), kernel {len(nb)} ({sum(len(v) for v in nb.values())} rows); identical: {na == nb}")
for k in sorted(set(na) | set(nb)):
    if na.get(k) != nb.get(k): print(f"   {k}: v6 {len(na.get(k, []))} rows, kernel {len(nb.get(k, []))}; only v6 {[x for x in na.get(k, []) if x not in nb.get(k, [])][:3]}; only kernel {[x for x in nb.get(k, []) if x not in na.get(k, [])][:3]}")
print(f"\nruns in all: v6 {rows(a, 'SELECT count(*) FROM run')[0][0]}, kernel {rows(b, 'SELECT count(*) FROM run')[0][0]}; symbols: v6 {len(syma)}, kernel {len(symb)}; only v6 {sorted(set(syma.values()) - set(symb.values()))}; only kernel {sorted(set(symb.values()) - set(syma.values()))}")
