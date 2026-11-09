import sys, time; sys.path.insert(0, ".")
from nkdoor import Door
d = Door(sys.argv[1]); n = int(sys.argv[2])
t = time.time()
rows = d.q("WITH RECURSIVE g(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM g WHERE x < ?) SELECT d.gate, d.shard, d.before, d.trigger, d.call, d.spawn, d.times FROM g JOIN dna d ON d.gate = g.x WHERE d.call IS NOT NULL OR d.spawn IS NOT NULL", [n])
print("gates 1..%d: %d acting rows in %.2f s" % (n, len(rows), time.time() - t)); print(rows[:5])
