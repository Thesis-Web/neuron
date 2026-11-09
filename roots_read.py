# tries/63: what the live brain holds for the six compute roots and the boolean words: gate, dna rows, definition rows, and the source rows that name
# computing, logic or mathematics, and an etymology line. Reads only, by key.
import sys, re; sys.path.insert(0, ".")
from nkdoor import Door
d = Door(sys.argv[1]); SRC = {d.gate(s): s for s in ["wn", "gcide", "wikt", "mwt", "moby", "map", "sqldoc", "measured"]}
def text(run):
    r = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run]); return (r[0][0] or "") if r else ""
for w in sys.argv[2].split(","):
    g = d.gate(w)
    if not g: print("%-8s no gate" % w); continue
    dna = d.q("SELECT shard, before, trigger, call, spawn, times FROM dna WHERE gate = ?", [g])
    rows = [(SRC.get(s, s), text(r)) for i, s, r in d.q("SELECT id, source, run FROM node WHERE gate = ? ORDER BY id", [g])]
    comp = [(s, t) for s, t in rows if re.search(r"\((computing|computer science|computer|logic|mathematics|electronics|programming)", t, re.I)]
    ety = [(s, re.search(r"\[etymology[^\]]*?: ([^\]]{0,160})", t).group(1)) for s, t in rows if re.search(r"\[etymology[^\]]*?: ", t)]
    print("%-8s gate %-7s dna rows %d, acting %d | definition rows %d | computing or logic senses %d | etymology lines %d" % (w, g, len(dna), sum(1 for x in dna if x[3] or x[4]), len(rows), len(comp), len(ety)))
    for s, t in comp[:3]: print("     %-6s %s" % (s, t[:170]))
    for s, t in ety[:1]: print("     etym %-6s %s" % (s, t[:170]))
