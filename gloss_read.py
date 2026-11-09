# tries/62: for every point with an acting dna row (except the 316 birth rows), the first WordNet verb sense the brain holds (else the first sense),
# read from its node rows by key; the run its row calls. Reads only.
import sys, json; sys.path.insert(0, ".")
from nkdoor import Door
d = Door(sys.argv[1]); j = json.load(open(sys.argv[2])); L = {int(k): v for k, v in j["label"].items()}
WN = d.gate("wn")
def text(run):
    r = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run]); return (r[0][0] or "") if r else ""
calls = {}
for g, sh, b, t, c, s, tm in j["rows"]:
    if s == 19936999 and not c: continue
    calls.setdefault(g, []).append((L.get(b) if b else None, L.get(t) if t else None, c, s))
out = {}
for g in sorted(calls, key=lambda x: L[x].lower()):
    rows = d.q("SELECT id, source, run FROM node WHERE gate = ? ORDER BY id", [g])
    wn = [text(r[2]) for r in rows if r[1] == WN]
    verb = [x for x in wn if x.startswith("verb")]; noun = [x for x in wn if x.startswith("noun")]
    first = (verb or wn or [text(rows[0][2])] if rows else [""])[0] if (verb or wn or rows) else ""
    out[L[g]] = {"gate": g, "rows": calls[g], "wn_first_verb": verb[0][:220] if verb else None, "wn_first": (wn[0][:220] if wn else None), "wn_verbs": len(verb), "wn_nouns": len(noun)}
    print("%-14s %s | verb senses %d, noun senses %d | %s" % (L[g], sorted(set((r[2], r[3]) for r in calls[g])), len(verb), len(noun), (verb[0] if verb else (wn[0] if wn else "no wn row"))[:170]))
json.dump(out, open(sys.argv[3], "w"))
