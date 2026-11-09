# tries/61: what each one-action row actually does. Types each line on the TEST brain (door 8059) and traces every run it makes:
# arrival, kind (0 typed, 1 call, 2 spawn, 3 return), the run it replays, same_as (a repeat: no landings of its own, only the recorded firings),
# landings (its own receipts), the hits that carried a call or spawn, mother's answers; and the kernel counters before and after.
import sys, json, time, urllib.request; sys.path.insert(0, ".")
from nkdoor import Door
door = sys.argv[1]; d = Door(door); W = sys.stdout.write
KIND = {0: "typed", 1: "call", 2: "spawn", 3: "return"}
def stats():
    m = json.load(urllib.request.urlopen(door + "/api/info", timeout=30))["stats"]["main"]
    return {k: m[k] for k in ("runs", "hops", "hops_run", "pastes", "returns", "deduped_runs", "refused", "shard_rows")}
def text(run, n=160):
    r = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run])
    t = (r[0][0] or "") if r else ""; return t[:n].replace("\n", " ") + ("…" if len(t) > n else "")
def show(run, depth, budget):
    if budget[0] <= 0: return
    budget[0] -= 1
    row = d.q("SELECT id, arrival, kind, cell, replay_src, same_as, from_ord FROM run WHERE id = ?", [run])[0]
    _, arr, kind, cell, src, same, ford = row
    own = d.q("SELECT count(*) FROM run_receipt WHERE run = ?", [run])[0][0]
    nseq = d.q("SELECT count(*) FROM seq WHERE run = ?", [run])[0][0]
    hits = d.q("SELECT pos, gate, before, next, shard, call, spawn FROM hit WHERE run = ?", [run])
    pad = "  " * depth
    W("%srun %s  %s from %s%s%s | symbols %d, landings of its own %d%s\n" % (pad, run, KIND.get(kind, kind), d.sym(arr),
      (", replays run %s" % src) if src else "", (", cell %s" % d.sym(cell)) if cell else "", nseq, own,
      (" | REPEAT of run %s: no landings, the kernel fires that run's recorded firings" % same) if same else ""))
    if kind == 3: W("%s   mother's answer: %s\n" % (pad, text(run)))
    elif kind in (1, 2): W("%s   its line: %s\n" % (pad, text(src or run, 120)))
    for h in hits:
        if h[5] or h[6]: W("%s   hit at pos %s on %s (before %s, after %s) shard %s: call %s spawn %s\n" % (pad, h[0], d.sym(h[1]), d.sym(h[2]) if h[2] else "-", d.sym(h[3]) if h[3] else "-", h[4], h[5], h[6]))
    if same:
        ev = [h for h in d.q("SELECT pos, gate, shard, call, spawn FROM hit WHERE run = ?", [same]) if h[3] or h[4]]
        nb = sum(1 for x in d.q("SELECT gate FROM run_receipt WHERE run = ?", [same]) if x[0] == 29)
        W("%s   run %s's recorded firings: %d calls or spawns, %d BUILD marks (every second one closes a span that mother runs)\n" % (pad, same, len(ev), nb))
    for k in d.q("SELECT id FROM run WHERE parent = ? ORDER BY id", [run]): show(k[0], depth + 1, budget)
def go(line):
    b = stats(); t = time.time(); r = d.typed(line, quiet=True); el = time.time() - t; a = stats()
    W("\n=== %r  run %s: %s runs, %s hits, %s born, %s refused, %.3f s at the door\n" % (line, r.get("run"), r.get("runs"), r.get("hits"), r.get("born"), r.get("refused"), el))
    W("    kernel counters: " + ", ".join("%s +%d" % (k, a[k] - b[k]) for k in a) + "\n")
    show(r["run"], 1, [60]); return r
r1 = go("print dna : glimmer")
go("print node : glimmer")
go("print table : pull")
go("print memory : glimmer")
go("print sheet : %d" % r1["run"])
kid = d.q("SELECT id FROM run WHERE parent = ? AND kind = 1 ORDER BY id", [r1["run"]])
go("step back : %d" % (kid[-1][0] if kid else r1["run"]))
go("create neuron : hlēapan")
go("change trigger : leap from back to back")
go("change call : leap from 1302 to 1302")
go("change spawn : leap from 0 to 0")
go("change define : leap like jump")
go("change meaning : leap from 0 to 0")
go("define unknown : 1")
