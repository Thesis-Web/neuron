# tries/62: WordNet's own sense 1 (verb 1, else noun 1, else adjective 1, else adverb 1) of every acting point, from the brain's node rows by key
import sys, json, re; sys.path.insert(0, ".")
from nkdoor import Door
d = Door(sys.argv[1]); G = json.load(open(sys.argv[2])); WN = d.gate("wn")
def text(run):
    r = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run]); return (r[0][0] or "") if r else ""
out = {}
for w, v in G.items():
    wn = [text(r[2]) for r in d.q("SELECT id, source, run FROM node WHERE gate = ? ORDER BY id", [v["gate"]]) if r[1] == WN]
    pick = None
    for cls in ("verb 1:", "noun 1:", "adjective 1:", "adjective satellite 1:", "adverb 1:"):
        for x in wn:
            if x.startswith(cls): pick = x; break
        if pick: break
    g = re.split(r' \[', pick or '')[0]
    out[w] = {"gate": v["gate"], "calls": sorted(set(str(r[2]) for r in v["rows"])), "sense1": g}
    print("%-14s calls %-34s | %s" % (w, ",".join(out[w]["calls"]), g[:150]))
json.dump(out, open(sys.argv[3], "w"))
