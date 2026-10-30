# Where the time goes in a v6 define (2026-10-29, 22:10 to 22:40)

**The owner's question (22:05):** "each process was taking 3-7 micro seconds... for something to take 40s doesn't add up, either you installed a timer, or you have something the brain is doing that can be more efficient? ... I have seen this before in tries where as the brain grows runs start taking longer and longer, it has been traced back to sweeps, timers ... perhaps the standing question is sweeping all of memory ... we have to figure out a way for that process to match patterns or find just the word, such that it's not sweeping the entire memory on every call."

**Method.** One define typed on a copy of the live brain with every statement SQLite ran on the connection traced (statements inside mother and inside the triggers included; `tries/24/profile_define.py`); the gap from one statement's start to the next charged to the first. Then each suspect timed by itself on the copy. Then the fixes as lines typed on a second copy, the same define timed on a third copy without them (the control). Nothing was typed into the live brain.

## The profile: `define : able`, 50.1 s, 1,130,960 statement starts, 45,373 hits (`tries/24/PROFILE-define-able-BEFORE.txt`)

| Seconds | What | Why |
|---|---|---|
| 21.5 (inside the 16 s charged to the hit insert and the rest) | The hop's test "does the next symbol have a table yet": `EXISTS (SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ...)` in land_go, on every hit | A scan of the whole schema catalogue, 10,623 rows, 474 µs a hit. **Grows with every neuron born** (two catalogue rows each). This is the sweep. |
| 12.2 | The define run's span 3 (known and unknown): `EXISTS (SELECT 1 FROM run k WHERE k.kind = 3 AND k.about = s.gate ...)` | Evaluated once per return row joined (tens of thousands), each a scan of the run table (15,075 rows): `SCAN k`. **Grows with every run and every return.** |
| 11.0 | Mother's pump per hop: `PRAGMA database_list` (1.3 s), the names (0.4 s), a poll of every attached brain's hop table (sixth 8.5 s, main 0.6 s), the delete (0.2 s) | mother.c lists the databases and polls each one's hop table after every hop. Constant per hop; not a sweep; host code. |
| ~16 | The hop's own statements: land_go's four mother calls (each recomputing before and next with two to four seq subqueries), hit_go's ten statements, the shard insert, the times update, the shards counter | About 20 statements a hit at 15 to 30 µs each: the floor of this hop as laid. |
| 1.4 (+ hidden) | 351 births: `CREATE TABLE "N"` and `"N.node"` | 5.9 ms a table with 10,623 catalogue rows; grows with the catalogue. |
| 0.03 | The three standing questions (know, remember, shape), heard's row 0 | 5 ms a line. **Not the cause.** |
| 0.3 | The sixth's observing line (with the collection of unknowns) and the why line's corpus push | Small now; the corpus push rereads every return's words on every why line, so it will grow. |

No timer exists anywhere in the brain, mother or the door.

## The fixes, as lines (`tries/24/SPEED-LINES-2026-10-29.txt`), tried on a copy

1. main's land_go laid again (its own text from sqlite_master, dropped and created, as the underscore relay of tries/21) with the one change: the question asked of the schema's hash, `EXISTS (SELECT 1 FROM pragma_table_info(CAST(NEW.next AS TEXT), 'main'))`, 20 µs instead of 474.
2. The sixth's land_go, the same, with 'sixth'.
3. `CREATE INDEX run_about ON run ( about )` and `CREATE INDEX run_kind_arrival ON run ( kind , arrival )`: "is there a return about this gate" and "how many source returns" find their rows instead of scanning (the define's span 3, the sixth's counts, the why line). Measured alone: the known test 1.33 s to 0.001 s.

| Copy | `define : able` | Runs, hits, born |
|---|---|---|
| Control, no change (`LEDGER-CONTROL-...`) | 51.3 s | 981, 52,701, 419 |
| After the three lines (`LEDGER-TRIAL-...`) | 32.6 s | 981, 52,701, 419 |

The three lines answered ok; 0 refused in both brains; the work identical. The owner's to type (they change the hop trigger, a hand-laid row of the core, and add two indexes to a hand-laid table).

## What remains after them (`tries/24/PROFILE-define-only-AFTER.txt`: `define : only`, 46.5 s traced, 75k hits, 613 births)

0.34 ms a hit in the hit insert and hit_go's ten statements; 8 s in the pump; 1.6 s in the new table test; 2 s in births; 0.45 ms a hit all in, against the owner's 3 to 7 µs. The rest is not a sweep but the count of statements per hit (about 20) and the pump's bookkeeping per hop, both in the hand-laid core and in mother.c. To reach microseconds a hit, the hop would have to be one or two prepared statements that the cache can reuse (today each statement names the gate's table, so the cache holds one entry per gate) and the pump would have to stop re-listing the databases and polling every hop table on every hop. Those are the owner's design calls: the egg's triggers (which the brain can lay again through the prompt, as tonight) and mother.c (host code).

Two smaller things that will grow: the shard lookup in a gate's table (`WHERE before IS ? AND trigger IS ?`, no index) as a word gains hundreds of contexts; and the why line's push of every return's words into the guessing brain's corpus on every why.
