# tries/61, the owner 05:2x: if the brain changes a run (SELECT ... FROM shard WHERE gate = what), does the new code reach the SQL prompt,
# on the first run and through the repeat shortcut? And does a new row on a SQL neuron inside an already-repeated run ever get a turn?
# TEST brain only (door 8059). EXPECTED, written before: (1) the changed run lands (new symbols, no memory), mother is handed the new text and
# answers "error: no such table: shard"; (2) the next print dna repeats that new run and mother answers the same; (3) a valid change answers
# the new columns, also on its repeat; (4) by the code (dedupe_check reads only the shards on the old receipts), a NEW row laid on where for the
# context (dna, gate) does NOT fire while the run repeats; (5) a run with other symbols lands and the same row fires; restore at the end.
import sys, json, time, urllib.request; sys.path.insert(0, ".")
from nkdoor import Door
door = sys.argv[1]; d = Door(door); W = sys.stdout.write
def stats():
    m = json.load(urllib.request.urlopen(door + "/api/info", timeout=30))["stats"]["main"]; return {k: m[k] for k in ("runs", "hops", "pastes", "deduped_runs", "refused")}
def text(run, n=200):
    r = d.q("SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos )", [run]); t = (r[0][0] or "") if r else ""; return t[:n]
def typed(line, show_kids=True):
    b = stats(); r = d.typed(line, quiet=True); a = stats(); run = r["run"]
    W("\n>>> %s\n    run %s | %s\n" % (line[:150], run, ", ".join("%s +%d" % (k, a[k] - b[k]) for k in a)))
    if show_kids:
        for k in d.q("SELECT id, kind, replay_src, same_as FROM run WHERE parent = ? ORDER BY id", [run]):
            if k[1] != 1 or k[2] == 19937672: continue
            own = d.q("SELECT count(*) FROM run_receipt WHERE run = ?", [k[0]])[0][0]
            W("    called run %s replays %s | %s\n" % (k[0], k[2], ("REPEAT of %s: no landings, its recorded BUILD marks fired" % k[3]) if k[3] else ("landed: %d receipts of its own" % own)))
            for kk in d.q("SELECT id, kind, replay_src, arrival FROM run WHERE parent = ? ORDER BY id", [k[0]]):
                if kk[1] == 3: W("       mother answered: %s\n" % text(kk[0], 160))
                else: W("       KID run %s kind %s replays %s (a shard on the called run's path fired)\n" % (kk[0], kk[1], kk[2]))
    say = d.sheet(run).get(25)
    if say: W("    say cell 25: %s\n" % (str(say[1].get("text") if isinstance(say[1], dict) else say)[:200]))
    return run
P = d.gate("print"); WH = d.gate("where"); DNA = d.gate("dna"); GT = d.gate("gate")
W("print gate %s rows: %s\n" % (P, d.q("SELECT shard, before, trigger, call FROM dna WHERE gate = ?", [P])))
old = text(826, 5000)
A = old.replace("FROM dna WHERE gate = what", "FROM shard WHERE gate = what"); assert A != old
B = old.replace("SELECT shard , before , trigger , call , spawn , times FROM dna WHERE gate = what", "SELECT shard , call FROM dna WHERE gate = what"); assert B != old
B3 = B.replace("ORDER BY shard ;", "ORDER BY shard DESC ;"); assert B3 != B
W("\n== 1. the brain's changed run A typed as a line (its spans run once at typing with their holes unfilled)\n")
ra = typed(A, show_kids=False)
W("   mother's answers at typing: %s\n" % [text(k[0], 80) for k in d.q("SELECT id FROM run WHERE parent = ? AND kind = 3 ORDER BY id", [ra])])
typed("change call : print from 826 to %d" % ra, show_kids=False)
W("   print rows now: %s\n" % d.q("SELECT shard, before, trigger, call FROM dna WHERE gate = ?", [P]))
W("\n== 2. print dna through the changed run, first time, then a repeat\n")
typed("print dna : leap"); typed("print dna : jump")
W("\n== 3. a valid change B: SELECT shard , call FROM dna\n")
rb = typed(B, show_kids=False); typed("change call : print from %d to %d" % (ra, rb), show_kids=False)
typed("print dna : step"); typed("print dna : leap")
W("\n== 4. a NEW row on where, keyed (dna, gate) as it lands in B's span 2, call = run 1; then print dna again (B repeats)\n")
typed("BUILD INSERT INTO dna ( gate , shard , before , trigger , call , spawn , times ) VALUES ( %d , NULL , %d , %d , 1 , NULL , 0 ) ; BUILD" % (WH, DNA, GT), show_kids=False)
W("   where rows now: %s\n" % d.q("SELECT shard, before, trigger, call, spawn, times FROM dna WHERE gate = ?", [WH]))
typed("print dna : stride")
W("\n== 5. a run with other symbols B3 (ORDER BY shard DESC): it must land, and the where row should fire\n")
rb3 = typed(B3, show_kids=False); typed("change call : print from %d to %d" % (rb, rb3), show_kids=False)
typed("print dna : pace")
W("   where rows now: %s\n" % d.q("SELECT shard, before, trigger, call, spawn, times FROM dna WHERE gate = ?", [WH]))
W("\n== 6. restore: print's call back to 826, the where row's call to none, then print dna as before\n")
typed("change call : print from %d to 826" % rb3, show_kids=False); typed("change call : where from 1 to 0", show_kids=False)
W("   print rows: %s | where rows: %s\n" % (d.q("SELECT shard, before, trigger, call FROM dna WHERE gate = ?", [P]), d.q("SELECT shard, before, trigger, call, times FROM dna WHERE gate = ?", [WH])))
typed("print dna : step")
W("\n== 7. which tables can carry a trigger: the triggers in the brain's own SQL files and the sources\n")
for sch in ["main", "sixth", "wikt"]:
    W("   %s triggers: %s\n" % (sch, [r[0] for r in d.q("SELECT name FROM %s.sqlite_master WHERE type = 'trigger'" % sch)]))
