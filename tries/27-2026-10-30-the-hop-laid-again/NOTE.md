# 27. The hop laid again: every effect kept, one paste where there were four (2026-10-30, 02:20 to 03:40)

**Status: checked on twin copies of the live brain, not typed into the live brain. The owner (02:15): "the hop is simple and cheap basically just the spacebar in a sentence... you have to keep the meanings intact, and the triggers still have to fire... check that for me." And: "make sure you don't lose any of the aspects of the scope in the process." The lines are `HOP-LINES-2026-10-30.txt`; the check is `measure/`.**

## What the hop did, and what it does now

A landing is an insert into `land`. Today's land_go hands mother four texts, each naming the gate's table, and computes the landing's key (the nearest symbols that are not the space, before and after) with two subqueries on seq in each of them: eight lookups of the same two values. The fourth text writes the hit row after a second lookup of the shard. hit_go then runs ten statements. About twenty statements a hit; three copies of the trace.

The hop laid again keeps every one of those effects: the shard laid if missing with the next number from the counter; the shard's times bumped; the hit row with before, next, via, had, shard, call and spawn; the receipt; the ended; the next landing; the birth path (the newgate cell, the landing on born, the via); the calls and spawns as replays; the build spans and the span to mother. What changes is only how: the landing carries its key (two new columns on `land` and `hit`, kb and kn, written by hit_go for the next landing from what it already knows, with one lookup on every other hop instead of eight on every hop); one paste through mother bumps the shard's times and brings back shard, call and spawn in the same answer (UPDATE ... RETURNING), kept in a one-row table `step`; the shard is laid and the counter bumped only when that answer was empty (two more statements, on the 2% of hops that lay a shard); the hit row is written from the answer by a plain statement, no second lookup; the test for the next symbol's table asks the schema's hash (pragma_table_info), not a scan of the catalogue. A landing written by the old hit_go (kb empty) is keyed the old way, so the mailbox's queued landings go on unchanged. The mailbox gets two more columns (p7, p8) because the next landing's row now carries seven values; the router reads them (`bottom7.py` here).

## The check (`measure/`)

Two copies of the live brain taken at 02:50, identical to the byte: U with the hop laid again, V as it was. On both the sixth was set to collect only (seen's call to run 1077), the mailbox cut to its five newest landings, so the work was finite and the same. Six lines typed on each: `define : across` (births, sources, the define's spans, the sixth's seen and why, the guesser), `print dna : who` (a tool, its call), `create neuron : zzyzx` (the born run through a tool), a BUILD span, a BUILD span at the sixth, `print sheet : 7`. Then every table of both brains compared row for row (`diff_brains.py`; the wall-clock columns left out; the hop's own working tables and the mailboxes left out, since the lean hop shapes those differently on purpose):

| | U, the hop laid again | V, as it was |
|---|---|---|
| runs, hits, born per line | identical (347 / 24,711 / 113 for define : across; 9 / 3,436 / 0 for print dna : who; ...) | identical |
| hops pasted: main, sixth; commits | 33,204; 3,217; 2,566 | 33,204; 3,217; 2,566 |
| refused, both brains | 0 | 0 |
| main brain tables compared / identical | 52,581 / 52,581 (every neuron's DNA rows, run_receipt, run_sheet, run_memory, rel, label, timeline, the node tables) | |
| the sixth's tables compared / identical | 296 / 296 | |
| receipts of the typed lines, row for row | 32,291 rows, same sums of gate, shard, pos | same |
| `define : across` | 183.9 s | 209.5 s |
| `print dna : who`, 3,436 hits | 1.14 s: **332 µs a hit** | 2.93 s: 853 µs a hit |

So the meanings are intact and the triggers fire: the brain holds the same rows after the same lines. The hop costs 2.6 times less. A define is dominated now by its births (113 CREATE TABLEs at 6 ms and more as the catalogue grows), the cutting of the returns and the define's own spans, not by the hop.

## What is mine, labelled

The two key columns and the one-row step table (SQLite's triggers cannot hold a value between statements, so the answer is kept in a row); UPDATE ... RETURNING as the one paste; the mailbox's two more columns; the parsing of mother's answer (shard | call | spawn); the test through pragma_table_info. The order of the hit's steps, the stack, the birth path, the receipt, the cells: unchanged and the owner's.

## Still not the spacebar, and why

The floor of a hop in this brain is one paste through mother (the neuron's table must be named by number, so the statement cannot be cached across gates), one receipt, the next landing queued and taken through the mailbox (SQLite cannot chain twenty thousand triggers deep), and hit_go's ten statements. That is about 100 µs at the least. The 2 to 4 µs of a row written inside a transaction, the spacebar, would need the shard found without naming a table (one DNA table with a gate column: a birth as a row, not a CREATE TABLE) and no mailbox. Both are the owner's design calls, not mine.

## To type it live

The sequence in `HOP-LINES-2026-10-30.txt`: the door stopped by the owner's word; the mailbox widened on both brain files at the terminal and this folder's `bottom7.py` put in place; the door started; then seven lines at the prompt. The three speed lines of `tries/24` are then partly done (the hop's table test) and partly still to type (the two indexes on run).
