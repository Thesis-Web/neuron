# tries/61: for each point with an acting row, the trial's record of where its rows came from (tried: gate, other, outcome) and the belief on each acting shard. Reads only.
import sys, json; sys.path.insert(0, ".")
from nkdoor import Door
d = Door(sys.argv[1]); j = json.load(open(sys.argv[2]))
L = {int(k): v for k, v in j["label"].items()}
out = {}
for g in sorted(set(r[0] for r in j["rows"])):
    tr = d.q("SELECT other, outcome, run FROM tried WHERE gate = ?", [g])
    out[g] = {"tried": [(L.get(o) or d.sym(o), oc, r) for o, oc, r in tr]}
for r in j["rows"]:
    b = d.q("SELECT correct, incorrect FROM belief WHERE gate = ? AND shard = ?", [r[0], r[1]]); out[r[0]].setdefault("belief", {})[r[1]] = b[0] if b else None
json.dump(out, open(sys.argv[3], "w")); print("points read:", len(out), "| with a tried row:", sum(1 for v in out.values() if v["tried"]), "| acting shards with a belief row:", sum(1 for v in out.values() for x in v.get("belief", {}).values() if x))
