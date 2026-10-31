#!/usr/bin/env python3
# geo3.py (2026-10-30): the owner's method, second cut. The first cut re-read each law from the layout it had made, which let the cloud run away
# (a law that follows the points anchors nothing). Here the laws are fixed through a settle run to rest with momentum, on the core of the graph
# (points with two or more lines). Then the test that carries information: for 300 words, their MORE-GENERAL (up) and ACROSS lines are taken out
# of the layout before it settles, so those words sit where their like lines alone put them; afterwards each word is plotted from the lines
# that were taken out, by the law, and we ask whether the plot lands on the word (rank among all points). The adjust: the up-step length and
# direction are chosen by that score, over a small set of values, settling again each time. A control plots from the same lines with no step.
import json, sys, numpy as np, collections
from scipy.spatial import cKDTree
d = json.load(open(sys.argv[1])); lab = {int(k): v for k, v in d['label'].items()}
def cls(tag):
    t = tag.lower()
    if t in ('like', 'syn', 'synonyms', 'similar to', 'similar', 'coordinate terms', 'related'): return 'near'
    if t in ('derived', 'derivationally related form', 'derived terms'): return 'derived'
    if t in ('opposite', 'antonym', 'antonyms'): return 'across'
    if t in ('hypernym', 'hypernyms', 'instance hypernym'): return 'up'
    if t in ('hyponym', 'hyponyms', 'instance hyponym'): return 'down'
    return None
edges = collections.defaultdict(set)
for g, k, o in d['rel']:
    c = cls(lab.get(k, ''))
    if c: edges[c].add((g, o))
for g, tag, o, src in d['tagged']:
    c = cls(tag)
    if c: edges[c].add((g, o))
for g, o in edges.pop('down', set()): edges['up'].add((o, g))
deg = collections.Counter()
for es in edges.values():
    for g, o in es: deg[g] += 1; deg[o] += 1
core = {g for g, n in deg.items() if n >= 2}
edges = {k: {(g, o) for g, o in es if g in core and o in core and g != o} for k, es in edges.items()}
gates = sorted(core); idx = {g: i for i, g in enumerate(gates)}; N = len(gates)
E = {k: np.array([(idx[g], idx[o]) for g, o in es], dtype=np.int64) for k, es in edges.items() if es}
print('core:', N, 'points;', {k: len(v) for k, v in E.items()})
rng = np.random.default_rng(11)
# the test words: at least two near lines and at least one up line
up_of = collections.defaultdict(list); near_of = collections.Counter()
for i, j in E['up']: up_of[i].append(j)
for i, j in E['near']: near_of[i] += 1; near_of[j] += 1
cands = [i for i in up_of if near_of[i] >= 2]; rng.shuffle(cands); TEST = cands[:300]; TS = set(TEST)
across_of = collections.defaultdict(list)
if 'across' in E:
    for i, j in E['across']: across_of[i].append(j); across_of[j].append(i)
# the layout's lines: the test words' up and across lines taken out
E_lay = dict(E)
E_lay['up'] = E['up'][~np.isin(E['up'][:, 0], TEST)]
if 'across' in E: E_lay['across'] = E['across'][~(np.isin(E['across'][:, 0], TEST) | np.isin(E['across'][:, 1], TEST))]
print('held out of the layout:', len(E['up']) - len(E_lay['up']), 'up lines and', (len(E['across']) - len(E_lay['across'])) if 'across' in E else 0, 'across lines of', len(TEST), 'test words')
GAP = 0.3
def settle(P, steps, law, E_use):
    V = np.zeros_like(P)
    for s in range(steps):
        F = np.zeros_like(P)
        for kind, rest, k in (('near', 1.0, 1.0), ('derived', 1.5, 0.4)):
            if kind not in E_use: continue
            i, j = E_use[kind][:, 0], E_use[kind][:, 1]; dv = P[j] - P[i]; L = np.linalg.norm(dv, axis=1) + 1e-9; f = (k * (L - rest) / L)[:, None] * dv; np.add.at(F, i, f); np.add.at(F, j, -f)
        if 'across' in E_use and len(E_use['across']):
            i, j = E_use['across'][:, 0], E_use['across'][:, 1]; np.add.at(F, i, 0.3 * (-P[j] - P[i])); np.add.at(F, j, 0.3 * (-P[i] - P[j]))
        if 'up' in E_use and len(E_use['up']):
            i, j = E_use['up'][:, 0], E_use['up'][:, 1]; step = law['step'] * law['u']; np.add.at(F, i, law['k'] * (P[j] - step - P[i])); np.add.at(F, j, law['k'] * (P[i] + step - P[j]))
        fl = np.linalg.norm(F, axis=1); p95 = np.percentile(fl, 95) + 1e-9; sc = min(1.0, 0.3 / p95)
        V = 0.85 * V + F * sc * 0.4; P = P + V
        if GAP > 0 and s % 3 == 0:
            cells = np.floor(P / GAP).astype(np.int64); key = cells[:, 0] * 73856093 ^ cells[:, 1] * 19349663 ^ cells[:, 2] * 83492791
            order = np.argsort(key); ks = key[order]; starts = np.flatnonzero(np.r_[True, ks[1:] != ks[:-1]]); ends = np.r_[starts[1:], len(ks)]
            for a, b in zip(starts, ends):
                if b - a < 2: continue
                ii = order[a:b]; c = P[ii].mean(axis=0); dv = P[ii] - c; L = np.linalg.norm(dv, axis=1) + 1e-9; P[ii] += ((GAP - L).clip(0) / 2)[:, None] * dv / L[:, None]
        P = P - P.mean(axis=0)
    return P, float(np.median(np.linalg.norm(V, axis=1)))
def score(P, law, use_step=True):
    tree = cKDTree(P); ranks = []; miss = []
    for i in TEST:
        preds = [P[j] - (law['step'] * law['u'] if use_step else 0) for j in up_of[i]] + [-P[j] for j in across_of.get(i, [])]
        pred = np.mean(preds, axis=0); dd, ii = tree.query(pred, k=min(N, 1000)); r = next((rk + 1 for rk, x in enumerate(ii) if x == i), 1001); ranks.append(r); miss.append(float(np.linalg.norm(pred - P[i])))
    ranks = np.array(ranks); return float(np.mean(ranks == 1) * 100), float(np.mean(ranks <= 10) * 100), float(np.mean(ranks <= 100) * 100), int(np.median(ranks)), float(np.median(miss))
def signatures(P):
    out = {}
    for kind, arr in E.items():
        i, j = arr[:, 0], arr[:, 1]; L = np.linalg.norm(P[j] - P[i], axis=1); cs = np.einsum('ij,ij->i', P[i], P[j]) / (np.linalg.norm(P[i], axis=1) * np.linalg.norm(P[j], axis=1) + 1e-9); out[kind] = (round(float(np.median(L)), 3), round(float(np.median(cs)), 3))
    ri, rj = rng.integers(0, N, 4000), rng.integers(0, N, 4000); out['random'] = (round(float(np.median(np.linalg.norm(P[rj] - P[ri], axis=1))), 3), round(float(np.median(np.einsum('ij,ij->i', P[ri], P[rj]) / (np.linalg.norm(P[ri], axis=1) * np.linalg.norm(P[rj], axis=1) + 1e-9))), 3))
    return out
P0 = rng.normal(0, 1, (N, 3))
print(f"{'up step':>8} {'dir':>8} {'rest V':>7} | {'found 1st':>9} {'in 10':>6} {'in 100':>7} {'median':>7} {'miss':>6} | {'no-step control':>18}")
best = None
for step in (0.0, 0.6, 1.2, 2.4):
    for dname, u in (('z', np.array([0, 0, 1.0])), ('xyz', np.array([1.0, 1.0, 1.0]) / np.sqrt(3))):
        if step == 0 and dname == 'xyz': continue
        law = dict(k=1.0, step=step, u=u); P, v = settle(P0.copy(), 400, law, E_lay)
        r1, r10, r100, rm, miss = score(P, law); c1, c10, c100, cm, cmiss = score(P, law, use_step=False)
        print(f"{step:8.1f} {dname:>8} {v:7.4f} | {r1:8.1f}% {r10:5.1f}% {r100:6.1f}% {rm:7d} {miss:6.3f} | {c1:5.1f}% {c10:5.1f}% {cm:6d}")
        if best is None or r10 > best[0]: best = (r10, step, dname, P, law)
r10, step, dname, P, law = best
print('best law: step', step, 'along', dname, '| signatures at rest:', signatures(P))
ev = np.linalg.eigvalsh(np.cov(P.T)); print("the cloud's three extents:", np.round(np.sqrt(ev), 3))
tree = cKDTree(P)
for i in TEST[:6]:
    pred = np.mean([P[j] - law['step'] * law['u'] for j in up_of[i]] + [-P[j] for j in across_of.get(i, [])], axis=0); dd, ii = tree.query(pred, k=5)
    print(f"  {lab.get(gates[i])!r}: more general {[lab.get(gates[j]) for j in up_of[i][:3]]}{' opposite ' + str([lab.get(gates[j]) for j in across_of[i][:2]]) if i in across_of else ''} -> plotted beside {[lab.get(gates[x]) for x in ii]}")
