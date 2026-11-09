# tries/63: the boolean points as they stand on a brain: born, rows, what each row's call and spawn run says. Keyed reads only, nothing laid.
import sys; sys.path.insert(0, "/mnt/d/Neuron/tries/58-2026-11-04-the-owners-way-once")
from nkdoor import Door
d = Door(sys.argv[1])
pts = "this that not both and any or either neither contrary contradictory equal is true yes on false no off unknown".split()
def text(run):
    rr = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run])
    return (rr[0][0] or "") if rr else ""
cache = {}
def rt(run):
    if run not in cache: cache[run] = text(run)
    return cache[run]
for p in pts:
    g = d.gate(p)
    if g is None: print("%-14s no gate" % p); continue
    n = d.q("SELECT born, nodes, shards, memories FROM neuron WHERE gate = ?", [g])
    rows = d.q("SELECT shard, before, trigger, call, spawn, times FROM dna WHERE gate = ?", [g])
    print("%-14s gate %-7d born,nodes,shards,memories %s  rows %d" % (p, g, n[0] if n else None, len(rows)))
    for s, b, t, c, sp, tm in rows:
        print("   #%s  %s | %s  call %s  spawn %s  times %s" % (s, d.sym(b) if b else "-", d.sym(t) if t else "-", c, sp, tm))
        for k, r in (("call", c), ("spawn", sp)):
            if r: print("      %s r%s: %s" % (k, r, rt(r)[:220].replace("\n", " ")))
