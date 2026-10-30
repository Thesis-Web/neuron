# Handoff, 2026-10-30 00:15: v7 live, the brain completing its own unknowns

For the owner and the next session. Read `LLM-HANDLER.md`, then the two handoffs of 10-29, then this. It adds the night of 10-29 (tries 22 to 25).

## Where things stand

- **The live brain** is the same v6 brain files at the scratch path `w/19` (brain.db, sixth.db, sources/), now served by **v7's door** at http://localhost:8056/ (`page/serve7.py`, `brain/bottom7.py`, `brain/mother.so` built from `mother7.c`; v6's mother kept as `mother6.so`). Both brain files are in WAL mode. The owner types into it as before; the page reads while a run is going.
- **The pump is gone.** Mother pastes one text and answers. One router loop on one connection (v7.1, since 00:58) serves both brains' mailboxes in turn, newest row first, commits every 64 hops, and runs typed lines and the page's reads between batches. The first v7 gave each brain a connection of its own and failed within twenty minutes: the sixth starved for the write lock and died, and reads failed under the schema churn of births; the owner's three lines never reached the brain. The sixth keeps its own file and mailbox, with no sources, but not a connection of its own. `tries/25`, with the five-column chain.
- **The brain completes its own unknowns.** The sixth's observing line (sixth run 1140, seen's call) reads every define run's unknown list, collects what no define has asked about into `sixth.spawned`, and sends every pending one to main as `define : X` from the sixth (define's (the sixth, :) shard calls the define run 10516). The cascade started at 00:12 with 3,784 lines sent; it ends when no unknown is left unasked, which is days. It runs beside the owner: typed lines return at their own end, reads answer at once. `tries/23`.
- **The sources** are faithful (WordNet, GCIDE reloaded keeping all context; Wiktionary lean, attached as the ninth source, mw detached for the slot). `tries/22`. The full Wiktionary and the raw downloads are at `D:\Neuron-sources\`.
- **The speed lines** (`tries/24/SPEED-LINES-2026-10-29.txt`: the hop's table test through the schema's hash instead of a scan of sqlite_master; two indexes on run) are NOT typed. They halve a define (51 s to 33 s on a copy) and stack with v7. The owner's to type, or to say the word.
- **The backup** of both brain files as they were before v7: `D:\Neuron-sources\backups\before-v7-2026-10-30\`.

## How to stop the cascade, and how to roll back

- Stop the sending but keep collecting: at 6>, `BUILD UPDATE sixth."82" SET call = 1077 WHERE before = 6 AND trigger = 68 ; BUILD` (1077 is the collect-only observing run). The define lines already in the mailbox still run out; to drop them too, stop the door and clear `main.hop` with sqlite3 (the owner's call; they are the brain's rows).
- Roll back to v6's door: stop serve7 (the `python3 -u -I serve7.py 8056` process; its open batch rolls back, the mailbox keeps those rows), copy `mother6.so` back over `mother.so`, start `serve6.py 8056` in the page folder. WAL files suit v6's connection as they are. The brain's rows typed tonight stay (they are the brain's); to undo the self-feeding line only, the line above.

## The hc, begun (`tries/26`, 01:10 to 02:00)

The owner's words on it are in the NOTE. Measured: the memory table is 10 MB and 81% repeats (every ended run writes its own row; the owner's `again`, one row and count +1, is not laid); the bloat is the hop's trace in three copies (hit, land, receipt), 215 of 485 MB, growing with the cascade. The first nap is one line in `tries/26/NAP-LINE-2026-10-30.txt`: the landings and the call-less hits of ended runs go, the receipts stay; tried on a copy, identical answers after; the owner types it. The hc's own brain lays from the same egg (`egg7-hc.sql`) but has no attach slot: this SQLite attaches ten databases and the brain holds ten; either SQLite built with a higher SQLITE_MAX_ATTACHED preloaded into the door (the owner's; I was not permitted to fetch and build it), or the three small hand-laid sources in one file. The cores: four files, four processes, mail; main attached by nobody; the sixth retrained on mail. The owner's calls: the memory row's shape for `again` (a `times` column, keyed by content), the pointer to source on returns (a column on secondary and run from the carry trigger), the truth-shift depth.

## The hop laid again (`tries/27`, 02:20 to 03:40)

Checked, not typed. The owner asked why the hop costs 400 µs when it should cost the spacebar's 3, and that every meaning and trigger be kept. The hop as I laid it in v5 was four pastes through mother with the same key looked up eight times, then ten statements. Laid again: the landing carries its key, one paste finds the shard and brings back shard, call and spawn, the shard is laid only when missing, every effect kept. On twin copies after identical work every table is identical (52,581 in main, 296 in the sixth), 0 refused, 332 µs a hit against 853. `tries/27/HOP-LINES-2026-10-30.txt` has the seven lines and the door's two steps that come first (the mailbox widened at the terminal and the folder's bottom7.py in place, with the door stopped). The floor that remains is the named table and the mailbox, about 100 µs; the spacebar's few microseconds would need one DNA table and no mailbox, the owner's calls.

## Open, the owner's

The send inside `define unknown : N` still writes most-shared first, so within its N the rarest runs first (the self-feeding line was corrected; the tool was typed before the stack's order was understood). FIFO against LIFO for the mailbox (hit_go's order assumes a stack). The hop as ~20 statements a hit, and the births' cost (6 ms a table, growing with the catalogue). The sixth as its own process. 'fresh' (lay eggs again) is not in v7's door. The page replays the whole receipt table for its history: at a million hits it will be slow to open. The underscore lines of tries/21, still untyped.

## Faults of mine tonight, for the record

The pump of v5/v6 was mine and never said to the owner in words. My first cascade collection cost 200 s on every line (a scan per gate), caught on a copy. My first v7 committed on every hop and was slower than v6, caught on a copy. The self-feeding send wrote the most-shared first into a stack and the brain defined the rarest first, caught on the copy. Twice I stopped my own shell with a kill whose pattern my command line held. The door's bookkeeping failed under births until the reads were made to run again.
