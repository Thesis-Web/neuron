#!/usr/bin/env python3
# geo1.py (2026-10-30): a first measured step on the owner's geometry with the brain's own relationship rows, nothing drawn.
# 1. positions from relationships alone: the three leading eigenvectors of the normalized Laplacian of the "like" graph (a deterministic choice
#    of mine, not the brain's); 2. do the kinds have a geometric signature? distances and angles for like pairs, opposite pairs, random pairs;
# 3. can a point be located from its relationships without searching the points? hold a word's own position out, place it by least squares
#    from its neighbours' positions at the typical like-distance, and ask the rank of the true position among all points (1 = found).
#    The leak, said plainly: the held-out word's edges shaped its neighbours' positions a little when the graph was embedded whole.
import json, sys, numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla
from scipy.spatial import cKDTree
from scipy.optimize import least_squares
d = json.load(open(sys.argv[1])); rel = d['rel']; lab = {int(k): v for k, v in d['label'].items()}
kinds = {}
for g, k, o in rel: kinds.setdefault(lab.get(k, str(k)), []).append((g, o))
print('kinds:', {k: len(v) for k, v in kinds.items()})
like = kinds.get('like', []); opp = kinds.get('opposite', [])
# the like graph, undirected, its largest connected component
import collections
adj = collections.defaultdict(set)
for g, o in like: adj[g].add(o); adj[o].add(g)
seen = set(); best = []
for s in adj:
    if s in seen: continue
    comp = []; stack = [s]; seen.add(s)
    while stack:
        x = stack.pop(); comp.append(x)
        for y in adj[x]:
            if y not in seen: seen.add(y); stack.append(y)
    if len(comp) > len(best): best = comp
nodes = sorted(best); idx = {g: i for i, g in enumerate(nodes)}; N = len(nodes)
print(f'like graph: {len(adj)} points, largest connected piece {N} points, {sum(len(adj[g]) for g in nodes)//2} like lines')
rows, cols = [], []
for g in nodes:
    for o in adj[g]:
        if o in idx: rows.append(idx[g]); cols.append(idx[o])
A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))
deg = np.asarray(A.sum(axis=1)).ravel(); Dm = sp.diags(1 / np.sqrt(deg))
L = sp.identity(N) - Dm @ A @ Dm
vals, vecs = sla.eigsh(L, k=4, sigma=-1e-6, which='LM')
order = np.argsort(vals); vals = vals[order]; vecs = vecs[:, order]
P = Dm @ vecs[:, 1:4]; P = P / np.std(P) * 10     # three coordinates per point, scaled to a readable size
print(f'eigenvalues {np.round(vals, 5)}; positions for {N} points in 3 dimensions')
pos = {g: P[idx[g]] for g in nodes}
def dist(a, b): return float(np.linalg.norm(pos[a] - pos[b]))
def cos(a, b): return float(np.dot(pos[a], pos[b]) / (np.linalg.norm(pos[a]) * np.linalg.norm(pos[b]) + 1e-12))
rng = np.random.default_rng(1)
like_in = [(g, o) for g, o in like if g in idx and o in idx and g != o]; opp_in = [(g, o) for g, o in opp if g in idx and o in idx and g != o]
rand = [(nodes[i], nodes[j]) for i, j in rng.integers(0, N, size=(4000, 2)) if i != j]
def stats(pairs): ds = np.array([dist(a, b) for a, b in pairs]); cs = np.array([cos(a, b) for a, b in pairs]); return len(pairs), np.median(ds), np.mean(ds), np.median(cs)
for name, pairs in (('like', like_in), ('opposite', opp_in), ('random', rand)):
    n, md, mn, mc = stats(pairs); print(f'{name:9s} pairs {n:6d}: distance median {md:7.3f} mean {mn:7.3f}; angle (cosine) median {mc:+.3f}')
d_like = np.median([dist(a, b) for a, b in like_in])
tree = cKDTree(P)
# the locate test: hold out a word's position; place it from its like neighbours at the like distance; rank its true position
cands = [g for g in nodes if len(adj[g] & set(idx)) >= 3]; rng.shuffle(cands); cands = cands[:300]
ranks = []; dists = []
for g in cands:
    nb = [o for o in adj[g] if o in idx]; Q = np.array([pos[o] for o in nb])
    def resid(x): return np.linalg.norm(Q - x, axis=1) - d_like
    x0 = Q.mean(axis=0) + rng.normal(0, 1e-3, 3)
    sol = least_squares(resid, x0); x = sol.x
    k = min(N, 2000); dd, ii = tree.query(x, k=k)
    r = next((rk + 1 for rk, i in enumerate(ii) if nodes[i] == g), None)
    ranks.append(r if r else k + 1); dists.append(float(np.linalg.norm(x - pos[g])))
ranks = np.array(ranks); dists = np.array(dists)
print(f'locate test on {len(cands)} words with 3+ like neighbours: the true point is the nearest in {np.mean(ranks == 1)*100:.0f}%, within the nearest 3 in {np.mean(ranks <= 3)*100:.0f}%, within 10 in {np.mean(ranks <= 10)*100:.0f}%; median rank {int(np.median(ranks))}; median distance to the true point {np.median(dists):.3f} (like distance {d_like:.3f}); chance of rank 1 by luck 1 in {N}')
# the same by a plain centroid of the neighbours (no distances), for comparison
r2 = []
for g in cands:
    nb = [o for o in adj[g] if o in idx]; x = np.mean([pos[o] for o in nb], axis=0); dd, ii = tree.query(x, k=min(N, 2000)); r = next((rk + 1 for rk, i in enumerate(ii) if nodes[i] == g), None); r2.append(r if r else 2001)
r2 = np.array(r2); print(f'the neighbours\' centroid alone: nearest in {np.mean(r2 == 1)*100:.0f}%, within 10 in {np.mean(r2 <= 10)*100:.0f}%, median rank {int(np.median(r2))}')
# a few located words and what sits nearest to the located point
for g in cands[:6]:
    nb = [o for o in adj[g] if o in idx]; Q = np.array([pos[o] for o in nb]); x = least_squares(lambda v: np.linalg.norm(Q - v, axis=1) - d_like, Q.mean(axis=0)).x; dd, ii = tree.query(x, k=5)
    print(f'  {lab.get(g, g)!r} from {len(nb)} neighbours ({", ".join(lab.get(o, str(o)) for o in nb[:5])}): nearest to the located point {[lab.get(nodes[i], nodes[i]) for i in ii]}')
