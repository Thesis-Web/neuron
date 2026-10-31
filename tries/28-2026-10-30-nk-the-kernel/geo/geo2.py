#!/usr/bin/env python3
# geo2.py (2026-10-30): the owner's method on the brain's own rows. Every kind of line has a law (a pull to a rest distance, a push across the
# origin, a step in a direction); the layout settles under all the laws at once; then the reverse experiment: stand on a word whose alike,
# opposite, more-general and more-special words are known, plot from them where it should live, measure the miss, refigure the laws (rest
# distances and directions re-read from the layout), settle again, and so on. Measured each cycle: the kinds' signatures, and whether a word
# held out is found first at the place its relations plot (rank among all points). A control runs the same with like lines only.
import json, sys, numpy as np, collections
from scipy.spatial import cKDTree
d = json.load(open(sys.argv[1])); ONLY_LIKE = len(sys.argv) > 2 and sys.argv[2] == 'like-only'; CYCLES = int(sys.argv[3]) if len(sys.argv) > 3 else 12
lab = {int(k): v for k, v in d['label'].items()}; inv = {v: k for k, v in lab.items()}
KIND = {}
def cls(tag):
    t = tag.lower()
    if t in ('like', 'syn', 'synonyms', 'similar to', 'similar', 'coordinate terms', 'related'): return 'near'
    if t in ('derived', 'derivationally related form', 'derived terms'): return 'derived'
    if t in ('opposite', 'antonym', 'antonyms'): return 'across'
    if t in ('hypernym', 'hypernyms', 'instance hypernym'): return 'up'
    if t in ('hyponym', 'hyponyms', 'instance hyponym'): return 'down'
    if 'holonym' in t: return 'whole'
    if 'meronym' in t: return 'part'
    return None
edges = collections.defaultdict(set)
for g, k, o in d['rel']:
    c = cls(lab.get(k, '')); 
    if c: edges[c].add((g, o))
if not ONLY_LIKE:
    for g, tag, o, src in d['tagged']:
        c = cls(tag)
        if c: edges[c].add((g, o))
else:
    edges = {'near': edges['near']}
# down is up seen from the other end; part is whole seen from the other end
for a, b in (('down', 'up'), ('part', 'whole')):
    for g, o in edges.pop(a, set()): edges[b].add((o, g))
gates = sorted({g for es in edges.values() for e in es for g in e}); idx = {g: i for i, g in enumerate(gates)}; N = len(gates)
E = {k: np.array([(idx[g], idx[o]) for g, o in es], dtype=np.int64) for k, es in edges.items() if es}
print('kinds and lines:', {k: len(v) for k, v in E.items()}, '| points', N)
rng = np.random.default_rng(7); P = rng.normal(0, 1, (N, 3))
LAW = {'near': dict(k=1.0, rest=1.0), 'derived': dict(k=0.4, rest=1.6), 'across': dict(k=0.3), 'up': dict(k=1.0, step=1.2, u=np.array([0, 0, 1.0])), 'whole': dict(k=1.0, step=1.2, u=np.array([1.0, 0, 0]))}
GAP = 0.35
def settle(P, steps):
    for s in range(steps):
        F = np.zeros_like(P)
        if 'near' in E or 'derived' in E:
            for kind in ('near', 'derived'):
                if kind not in E: continue
                i, j = E[kind][:, 0], E[kind][:, 1]; dv = P[j] - P[i]; L = np.linalg.norm(dv, axis=1) + 1e-9; f = (LAW[kind]['k'] * (L - LAW[kind]['rest']) / L)[:, None] * dv
                np.add.at(F, i, f); np.add.at(F, j, -f)
        if 'across' in E:
            i, j = E['across'][:, 0], E['across'][:, 1]; k = LAW['across']['k']
            np.add.at(F, i, k * (-P[j] - P[i])); np.add.at(F, j, k * (-P[i] - P[j]))
        for kind in ('up', 'whole'):
            if kind not in E: continue
            i, j = E[kind][:, 0], E[kind][:, 1]; law = LAW[kind]; step = law['step'] * law['u']
            np.add.at(F, i, law['k'] * (P[j] - step - P[i])); np.add.at(F, j, law['k'] * (P[i] + step - P[j]))
        fl = np.linalg.norm(F, axis=1); p95 = np.percentile(fl, 95) if fl.size else 1; sc = min(1.0, 0.25 / (p95 + 1e-9))
        P = P + F * sc * 0.5
        # the space between points: a grid; points sharing a cell are pushed apart from the cell's mean
        if GAP > 0 and s % 2 == 0:
            cells = np.floor(P / GAP).astype(np.int64); key = cells[:, 0] * 73856093 ^ cells[:, 1] * 19349663 ^ cells[:, 2] * 83492791
            order = np.argsort(key); ks = key[order]; starts = np.flatnonzero(np.r_[True, ks[1:] != ks[:-1]]); ends = np.r_[starts[1:], len(ks)]
            for a, b in zip(starts, ends):
                if b - a < 2: continue
                ii = order[a:b]; c = P[ii].mean(axis=0); dv = P[ii] - c; L = np.linalg.norm(dv, axis=1) + 1e-9; push = ((GAP - L).clip(0) / 2)[:, None] * dv / L[:, None]; P[ii] += push
        P = P - P.mean(axis=0)
    return P
def plot_from_relations(w, P):
    # where the word's relations say it should live, each by its law, averaged by the laws' strengths
    i = idx[w]; preds = []; wts = []
    for kind, arr in E.items():
        a = arr[arr[:, 0] == i]; b = arr[arr[:, 1] == i]; law = LAW[kind]
        if kind in ('near', 'derived'):
            for j in np.r_[a[:, 1], b[:, 0]]: preds.append(P[j]); wts.append(law['k'])
        elif kind == 'across':
            for j in np.r_[a[:, 1], b[:, 0]]: preds.append(-P[j]); wts.append(law['k'])
        else:
            for j in a[:, 1]: preds.append(P[j] - law['step'] * law['u']); wts.append(law['k'])
            for j in b[:, 0]: preds.append(P[j] + law['step'] * law['u']); wts.append(law['k'])
    if not preds: return None
    return np.average(np.array(preds), axis=0, weights=np.array(wts))
def refigure(P):
    # the laws re-read from where the layout put things: the rest distance of near lines, the step and direction of up and whole lines
    if 'near' in E: i, j = E['near'][:, 0], E['near'][:, 1]; LAW['near']['rest'] = float(np.median(np.linalg.norm(P[j] - P[i], axis=1)))
    if 'derived' in E: i, j = E['derived'][:, 0], E['derived'][:, 1]; LAW['derived']['rest'] = float(np.median(np.linalg.norm(P[j] - P[i], axis=1)))
    for kind in ('up', 'whole'):
        if kind not in E: continue
        i, j = E[kind][:, 0], E[kind][:, 1]; dv = P[j] - P[i]; m = dv.mean(axis=0); n = np.linalg.norm(m)
        if n > 1e-6: LAW[kind]['u'] = m / n; LAW[kind]['step'] = float(np.median(dv @ LAW[kind]['u']))
def signatures(P):
    out = {}
    for kind, arr in E.items():
        i, j = arr[:, 0], arr[:, 1]; dv = P[j] - P[i]; L = np.linalg.norm(dv, axis=1); cs = np.einsum('ij,ij->i', P[i], P[j]) / (np.linalg.norm(P[i], axis=1) * np.linalg.norm(P[j], axis=1) + 1e-9)
        out[kind] = (float(np.median(L)), float(np.median(cs)))
    ri, rj = rng.integers(0, N, 3000), rng.integers(0, N, 3000); out['random'] = (float(np.median(np.linalg.norm(P[rj] - P[ri], axis=1))), float(np.median(np.einsum('ij,ij->i', P[ri], P[rj]) / (np.linalg.norm(P[ri], axis=1) * np.linalg.norm(P[rj], axis=1) + 1e-9))))
    return out
deg = collections.Counter()
for arr in E.values():
    for a, b in arr: deg[a] += 1; deg[b] += 1
held = [gates[i] for i in sorted(deg) if deg[i] >= 3]; rng.shuffle(held); held = held[:300]
def locate(P):
    tree = cKDTree(P); ranks = []; miss = []
    for w in held:
        pred = plot_from_relations(w, P)
        if pred is None: continue
        dd, ii = tree.query(pred, k=min(N, 1000)); r = next((rk + 1 for rk, i in enumerate(ii) if i == idx[w]), 1001); ranks.append(r); miss.append(float(np.linalg.norm(pred - P[idx[w]])))
    ranks = np.array(ranks); return float(np.mean(ranks == 1) * 100), float(np.mean(ranks <= 10) * 100), int(np.median(ranks)), float(np.median(miss))
print(f"{'cycle':>5} {'near':>6} {'random':>6} {'across cos':>10} {'up step':>8} {'found 1st':>9} {'in 10':>6} {'median rank':>11} {'miss':>6}")
for cyc in range(CYCLES + 1):
    P = settle(P, 60 if cyc else 200)
    sig = signatures(P); r1, r10, rm, miss = locate(P)
    print(f"{cyc:5d} {sig.get('near', (0, 0))[0]:6.3f} {sig['random'][0]:6.3f} {sig.get('across', (0, 0))[1]:+10.3f} {LAW['up']['step'] if 'up' in E else 0:8.3f} {r1:8.0f}% {r10:5.0f}% {rm:11d} {miss:6.3f}")
    refigure(P)
ev = np.linalg.eigvalsh(np.cov(P.T)); print('the cloud\'s shape, its three extents (square roots of the covariance\'s eigenvalues):', np.round(np.sqrt(ev), 3), '| laws now:', {k: {kk: (vv.round(2).tolist() if hasattr(vv, 'round') else round(vv, 3)) for kk, vv in v.items()} for k, v in LAW.items() if k in E})
for w in held[:5]:
    pred = plot_from_relations(w, P); tree = cKDTree(P); dd, ii = tree.query(pred, k=5)
    print(f"  {lab.get(w)!r} ({deg[idx[w]]} lines): plotted from its relations, the nearest points are {[lab.get(gates[i]) for i in ii]}")
np.save(sys.argv[1].replace('.json', '-P.npy'), P); json.dump(gates, open(sys.argv[1].replace('.json', '-gates.json'), 'w'))
