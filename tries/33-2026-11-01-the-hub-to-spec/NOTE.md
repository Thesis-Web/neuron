# tries/33 (2026-11-01): the hub to the owner's words, what the kernel learned, live on 8056

The owner: "ok now ... taking what you learned from the kernal. fix the hub.... to be correct". The reading: the hub stays the owner's brain of tables and triggers on 8056 and the kernel's lessons are laid into it. The kernel was not swapped in; the owner said on 10-30 "I am not killing the hub build". No tests; the measure is the live brain.

## What the running hub did

| Live on 8056 | Before | After |
|---|---|---|
| `define : know` | 95 s | **1.03 s** |
| `define : truth` | | 0.82 s |
| Defines a minute | about 0.6 | **150** |
| Hops of a define | 38,911 | almost none after the first walk of each formula |
| Refused, main and sixth | 0, 0 | 0, 0 |
| The door's memory | 1.3 GB | 184 MB just after a restart |

The steps, each read live: 95 s; 4.8 s a define after returns went to the sheet and closed formulas fired; 137 a minute after `carry`; 1.03 s after the door's list read.

## What changed, each with its reason

- **The brain left `/tmp`.** It lived in a dead session's scratchpad. It is at `/home/exnulla/neuron/hub`. The old path in `tries/30/hub-apply-2026-10-31.sh` is dead.
- **Returns go to the sheet.** The owner: "pull the fucking information to the run data sheet". `secondary_go` no longer lands a return: the encoder gives its gates, the cell it was asked for is filled, the node row is written. No hops, no DNA rows, no memory row for a return.
- **A closed formula fires from its list.** Draft 3.2: "one hop to the memory. No rows fire, nothing is laid, and mother is not called." New: `run.src`, tables `closed`, `fire_ev`, `fire`, trigger `fire_go`. When a replay of a formula ends with no birth in it, `ended_go` stores its calls, spawns and BUILD spans. The next replay does not copy the formula into `seq` and does not walk it: it fires that list, holes filled from the sheets as before. `closed.again` counts the repeats on the first run.
- **The encoder is one function.** `secondary_go`, `input_go` and `third_go` cut text character by character in a recursive query, twice. `encode(schema, text)` in mother.so does it in one pass, the kernel's cut rule. Note: this is a function outside the tables. It is the encoder, draft 2.5.
- **`carry` by parameters.** Every source built a new SQL statement around each return's text, so SQLite compiled `secondary_go` from scratch about 230 times a define. This was the kernel's fix of 10-30 and the hub never had it: 688 ms to 58 ms a firing.
- **No flush on the sources.** The nine sources `synchronous = OFF`, the sixth `NORMAL` (it had been left at full).
- **The door between hops.** A typed line waited for whole batches, and the first line after a start re-read every typed line one statement at a time. The router now serves the door after every hop; the door reads the lines only when a line needs them; a list of gates is read in one read, not one read a symbol, which was 20 of 22 s.
- **The guesser out.** The hub's `why` was the guesser and nothing else, so why's shard was unbound. An unknown stays an unknown.
- **`define`:** known and unknown in one pass (run 498941). **The sixth:** four tree walks gone (run 18381).
- **A profile**, `/api/prof`, as the kernel has. It ended three wrong guesses of mine.
- **The page's graph read** finds a run's first symbol by key instead of sweeping 23 million `seq` rows.

## Faults of mine in this stretch

Blamed `sheet_fill` without reading; every read there was keyed. Left my twin on 8057 running for hours. Left the owner's live brain in `/tmp` for three days. `hub-apply` of 10-31 was mine and cost a typed line 18 hours before anyone asked why.

## Not done

- **Sheet values on the hub are still strings in a TEXT column**: numbers as text, and `2/5`. `run_memory.input` too. The kernel holds numbers; the hub does not yet. Text is not gone from the hub.
- **The trace stays:** 7 million `hit` rows, 7 million `land` rows, 23 million receipts, 3 GB. They no longer grow much. Deleting them is the owner's word.
- **A rebind inside a closed formula is not seen.** The list stores each call as it was. A formula's own symbols are not normally rebound; if one is, lay the formula again.
- **New `hit` and `land` rows of the first walk** of a formula are still written.
- **The hub's why asks no source for the lowercase spelling**, as the kernel's does. It does nothing now.
- **A return's symbols get a neuron only when they are defined.** The graph on the page shows defined points and lines typed, not every word a return used.
- **`seq` copies of the old replays stay**, 23 million rows.
- **`defined` is not meaning.** Draft 4.2's compare of the sources is not built here either.
