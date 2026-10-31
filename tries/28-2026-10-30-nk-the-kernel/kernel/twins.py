#!/usr/bin/env python3
# twins.py: copy P (8057) against the live brain (8056): the lines each was given, in order, and the order in which each one's sixth chose to define its unknowns
import json, urllib.request, time
def q(port, sql, timeout=600):
    req = urllib.request.Request(f'http://127.0.0.1:{port}/api/q', data=json.dumps({'sql': sql}).encode(), headers={'content-type': 'application/json'})
    t = time.time(); d = json.load(urllib.request.urlopen(req, timeout=timeout)); return d.get('rows', d), time.time() - t
DEC = "(SELECT group_concat(symbol, '') FROM (SELECT l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = i.run ORDER BY s.pos))"
R = {}
for name, port in (('live 8056', 8056), ('copy P 8057', 8057)):
    inp, t1 = q(port, f"SELECT i.id, i.run, {DEC} FROM input i ORDER BY i.id")
    sp, t2 = q(port, "SELECT p.id, l.symbol FROM sixth.spawned p JOIN label l ON l.gate = p.gate ORDER BY p.id")
    cnt, t3 = q(port, "SELECT (SELECT max(id) FROM run), (SELECT max(gate) FROM label), (SELECT n FROM shards), (SELECT count(*) FROM rel), (SELECT count(*) FROM sixth.spawned), (SELECT count(*) FROM third), (SELECT count(*) FROM run_memory), (SELECT count(*) FROM guess.guesses)")
    R[name] = (inp, sp, cnt[0]); print(f"{name}: {len(inp)} typed lines, {len(sp)} unknowns spawned, counts (runs, gates, shards, rel, spawned, third, memories, guesses) = {cnt[0]}  [{t1:.1f} + {t2:.1f} + {t3:.1f} s]")
A, B = R['live 8056'], R['copy P 8057']
la, lb = [x[2] for x in A[0]], [x[2] for x in B[0]]
i = 0
while i < min(len(la), len(lb)) and la[i] == lb[i]: i += 1
print(f"\ntyped lines identical for the first {i}; then:")
for k in range(i, min(i + 6, max(len(la), len(lb)))): print(f"  line {k+1}: live {la[k][:90] if k < len(la) else '(none)'!r}\n           P    {lb[k][:90] if k < len(lb) else '(none)'!r}")
only_a = [x for x in la if x not in lb]; only_b = [x for x in lb if x not in la]
print(f"lines only the live brain got ({len(only_a)}): {[x[:60] for x in only_a][:8]}")
print(f"lines only P got ({len(only_b)}): {[x[:60] for x in only_b][:12]}")
sa, sb = [x[1] for x in A[1]], [x[1] for x in B[1]]
j = 0
while j < min(len(sa), len(sb)) and sa[j] == sb[j]: j += 1
print(f"\nthe sixth's choice of unknowns to define, in order: identical for the first {j} of {len(sa)} / {len(sb)}; then live {sa[j:j+8]} | P {sb[j:j+8]}")
Sa, Sb = set(sa), set(sb); print(f"as sets: both {len(Sa & Sb)}, only live {len(Sa - Sb)} e.g. {sorted(Sa - Sb)[:10]}, only P {len(Sb - Sa)} e.g. {sorted(Sb - Sa)[:10]}")
pos_b = {w: k for k, w in enumerate(sb)}; shifts = [abs(k - pos_b[w]) for k, w in enumerate(sa) if w in pos_b]
import statistics; print(f"of the shared unknowns, the place in the order differs by a median of {statistics.median(shifts):.0f} positions, at most {max(shifts)}; {sum(1 for s in shifts if s == 0)} sit at the same place")
