# tries/61: the acting rows of the live brain grouped by the run they fire; one action or several, by my reading of each run's statements (listed, to strike).
import json, collections
j = json.load(open("one-action-live.json")); F = {int(k): v for k, v in json.load(open("family-live.json")).items()}
L = {int(k): v for k, v in j["label"].items()}
ONE = {  # run: (domain, read/write, what its one statement does, the line that drives it)
 826:  ("graph",  "read",  "reads the dna rows of the point named and says them", "print dna : X"),
 870:  ("graph",  "read",  "reads the definition rows (node) of the point named and says them", "print node : X"),
 910:  ("graph",  "read",  "reads every row of the brain table the point names (mother runs SELECT * FROM it) and says them", "print table : X"),
 847:  ("memory", "read",  "reads the memory rows that ended on the point named and says them", "print memory : X"),
 889:  ("state",  "read",  "reads the sheet cells of the run named and says them", "print sheet : N"),
 1302: ("time",   "read",  "reads the chain of parent runs back from run N, with the hit that started each", "step back : N"),
 929:  ("graph",  "write", "births the point named if it is not born (replays run 1: INSERT INTO neuron), then reads it back", "create neuron : X"),
 950:  ("graph",  "write", "rewrites the trigger of the point's dna row from A to B", "change trigger : X from A to B"),
 989:  ("graph",  "write", "rewrites the call of the point's dna row from A to B", "change call : X from A to B"),
 1008: ("graph",  "write", "rewrites the spawn of the point's dna row from A to B", "change spawn : X from A to B"),
 1027: ("state",  "write", "writes one cell on the newest define sheet of the point", "change define : X cell value"),
 1052: ("state",  "write", "rewrites the meaning cell on the newest define sheet of the point from A to B", "change meaning : X from A to B"),
 1132: ("route",  "write", "takes N points from the sixth's list of unasked points and types define : X for each into the main brain's mailbox", "define unknown : N"),
 6281755: ("silicon", "write", "puts the point into the inbox of each of the eight sources; their triggers answer and mother carries the returns to the cell", "why : N to cell"),
}
MULTI = {
 19937672: "every typed line (heard): three cells, know (a definitions read), remember (a memory read), shape (a dna read)",
 19937007: "born: births the gate, lays its (define, :) spawn row, starts define",
 19936999: "the define laid at birth: relationship rows from the definitions plus three reads",
 19937222: "describe: the define of 11-02",
 19938846: "define with the dictionaries primary (RECALL-9): 8 spans",
 19942415: "determine: define plus the formula F (RECALL-11): 9 spans",
 19948363: "define with senses (RECALL-12): 11 spans",
 19937767: "meaning: passes the line to run 19937752, which picks the leg that answers and reads it",
 19937779: "correct: lays the borrowed rows, records tried, belief and the guess",
 19937787: "incorrect: marks belief, tried and the guess, then replays",
}
by = collections.defaultdict(list)
for g, sh, b, t, c, s, tm in j["rows"]:
    for kind, x in (("call", c), ("spawn", s)):
        if x: by[x].append((g, sh, L.get(b) if b else "-", L.get(t) if t else "-", kind, tm))
def fam(g):
    tr = F.get(g, {}).get("tried") or []
    src = sorted(set(o for o, oc, r in tr if oc)); return src
lines = []
P = lambda s="": lines.append(s)
P("# ONE ACTION (live brain hp:8058, read 2026-11-05 by gate)"); P()
for r, (dom, rw, what, line) in ONE.items():
    rows = by.get(r, []); pts = sorted(set(L[g] for g, *_ in rows), key=str.lower)
    keys = collections.Counter((b, t) for g, sh, b, t, k, tm in rows)
    P("## run %s | %s, %s | %s | typed as: %s" % (r, dom, rw, what, line))
    P("   %d rows on %d points, key (before, after): %s" % (len(rows), len(pts), dict(keys)))
    for g, sh, b, t, k, tm in sorted(rows, key=lambda x: L[x[0]].lower()):
        bel = F.get(g, {}).get("belief", {}).get(str(sh)); src = fam(g)
        P("   %-16s gate %-7s shard %-9s %s (%s, %s) hit %-4s belief %-8s %s" % (L[g], g, sh, k, b, t, tm, "%s/%s" % tuple(bel) if bel else "none", ("copied from " + ", ".join(src)) if src else ""))
    P()
P("# SEVERAL ACTIONS"); P()
for r, what in MULTI.items():
    rows = by.get(r, []); pts = sorted(set(L[g] for g, *_ in rows), key=str.lower)
    P("## run %s | %s | %d rows on %d points: %s" % (r, what, len(rows), len(pts), " ".join(pts[:30]) + (" ... (+%d)" % (len(pts) - 30) if len(pts) > 30 else "")))
left = set(by) - set(ONE) - set(MULTI); P(); P("runs not classified: %s" % sorted(left))
open("ONE-ACTION-POINTS.txt", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
