import sys; sys.path.insert(0, ".")
from nkdoor import Door
d = Door("http://127.0.0.1:8059")
print("test brain 8059: derived shards, belief rows and derived evidence, read by gate only")
for w in ["catalogue","plan","adapt","apologise","black","bribe"]:
    g = d.gate(w)
    dna = [r for r in d.q("SELECT shard, before, trigger, call, spawn, times FROM dna WHERE gate = ?", [g]) if r[3] or r[4]]
    bel = [d.q("SELECT shard, correct, incorrect, run FROM belief WHERE shard = ?", [r[0]]) for r in dna]
    der = d.q("SELECT ord, word, run_used, sense_run FROM derived WHERE gate = ? ORDER BY id", [g])
    print(w, "gate", g, "dna", dna, "belief", bel, "derived", der)
print("belief rows correct > 0:", d.q("SELECT count(*) FROM belief WHERE correct > 0")[0][0], "incorrect > 0:", d.q("SELECT count(*) FROM belief WHERE incorrect > 0")[0][0])
