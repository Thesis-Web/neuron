# tries/34 (2026-11-01): does a define recall? Midday: no, checked on ten points. Afternoon: the hop made one shard, the recall laid in the brain's own lines, the page measured

Two passes in one folder. The first is the check the owner asked for at midday (below, unchanged). The second, from 13:30 to 17:00, is the work the owner ordered on its back: "what is this neuron that has a ridiculas amount of shards????? ... the function of the hop is one dna shard, it basically = spacebar in a sentance"; "standing questions ... essentially grep (this run string or run reciept) does it exist in my memory if yes go there.. this is not code outside the brain this is the nueron triggers making it happen"; "it is illegal for you to put code outside the db to fix anything"; "you learn the long way, then you apply the shortcut"; "also my 8058 / full still doesn't work"; "do not stop until finished and correct ... live outcomes are the only proof".

Everything below is read from the running brain on hp (10.31.1.106, kernel socket 7007, door 8058). Nothing is a test.

## Second pass: the hop as one shard

**What was there.** The main brain held 20,048,959 DNA rows, the sixth 2,023. All but about a hundred were pass records: one row laid per (symbol before, symbol after) pair every time a run passed a point, each with its own shard id (hinge's HUD showed shard 5,858,959). The biggest holders: `:` 1,894,664 rows, `;` 1,006,973, `,` 973,060, `.` 397,773, `]` 391,442, `of` 386,481, `the` 354,287. The owner's words: the hop "is just a substitution shard... that is one shard that accepts the before and remainder as two variables"; "you do not need 10 million shards of dna to do that one action".

**The kernel's physics changed** (`hop_patch.py`, applied on hp at 14:00; sources in `tries/28/kernel`): a landing that finds no DNA row for its key lays none and counts on the one hop shard, the space's own row (id 17); `shard_by_id` answers the hop shard for its id so every receipt that names it still reads; a DNA row is laid only by a binding line (`UPDATE dna ... WHERE gate = G AND before = B AND trigger = T` lays the row when absent, as before); `shard_rows` in stats counts the rows that exist (`shards` is the id counter and never comes down). A `hop` request back-populates a brain that already holds the pass rows: it keeps every row with a call or spawn, the ok neuron's rows, the hop shard and the core's birth rows, folds the rest (their times onto the hop shard), rebuilds the key tables, then walks every run once and points each receipt, memory row and firing that named a folded row at the hop shard.

**The first pass hung the kernel for 1 h 40 min.** My bug: the fold rebuilt each neuron's key table with a size of twice its kept rows, and the table's probe masks with size minus one, which is only right for a power of two; with 504 kept rows (size 1,008) the mask reaches a 16-slot cycle, it filled, and `hmap_put` probed forever. No gdb on hp: a 20-line ptrace sampler (`rip.c`) read the instruction pointer eight times, every sample inside `hmap_put` under `do_hop`. Every line typed into hp between 14:03 and 15:56 waited on that pass and never ran, the owner's `print : who` among them. Fixed (the size is the next power of two), the kernel killed and started again on its file (the file's ready flag is set at start, never cleared), and the pass rerun.

**The pass, 216 s wall** (`out/hop.json` on hp): main 14,351,937 rows (the aborted pass had already folded 5.7 million) → 118 kept, 14,351,819 folded, times moved 170,975,687, the hop shard's times 420,652,191, receipts repointed 10,860,011, memory rows 2,118,551, firings 58, 134 s; sixth 2,023 → 21 kept, receipts repointed 18,405,155, 81 s. The hop shard's times undercounts: the rows the aborted pass folded before it hung carried their times with them and those are gone (about 5.7 million rows' worth; the kernel's total landings are 33,875,492 receipts kept).

**After, live:** `shard_rows` 118 main / 21 sixth (121 main by 16:22, after the binding lines below); `print : who` run 19936397: 479 receipts, every pass names shard 17 (`print` pos 1, `:` pos 3, `who` pos 5, every symbol of the per-line sheet run's text); `refused` 1 as before; the ok neuron's 85 rows intact; the page's HUD reads the hop shard on every pass. `print : who` is not a form this brain holds: `print` has rows for `print dna`, `print memory`, `print node`, `print sheet`, `print table` only; the line passes through and the sheet completes in 9 ms.

## Second pass: the recall, laid as the brain's own lines

Three typed lines, nothing outside the brain (`RECALL-2-nk.txt`; `RECALL-nk.txt` typed at 16:02 was replaced at 16:14: its ask named `mw.inbox`, which is not attached on hp, so the mother stopped at that statement and a never-defined point would have been asked of wn and gcide only, and it left out wikt and used an older known/unknown span):

1. The ask (the shape of run 1092): first the standing question, a keyed read of the point's own definition table (`node WHERE gate = what`). Yes: def, known and unknown of the run that learned it are copied onto this sheet and no source is asked. No: the point's symbol goes into the eight attached sources' inboxes, as before.
2. The define run (run 6459431's three spans): span 1 replays the ask above; span 3 (known and unknown from this run's returns) runs only when this run has source returns, so a recall keeps the cells it copied.
3. define's row 557 (heard before, `:` after) calls the new define run (19936582).

A typed BUILD line replies `error: no such column: above` at typing time; 25 earlier typed BUILD lines in the ledgers did the same and worked when called.

**Live, before the shape line below** (`recall_check.py`, `probe2.py`): the ten points all recalled: hinge, know, truth, water, house, river, stone, bread, horse, tree, 0.16 to 0.33 s wall through the door, 0.155 to 0.170 s at the kernel, 11 runs under each, no source asked, definition rows unchanged (hinge 752 → 752), def on the sheet and printed to the out mailbox (`run 19933360 from wn: noun 1: a joint that holds two parts together...`), known and unknown as learned, ok; `defined` 722,272 and `returns` 1,468,446 unchanged across all ten.

**The long way still runs, then the short:** `takakkaw` (gate 961121, 0 definition rows, in WordNet): asked of all eight sources, WordNet answered, 1 row laid, def `a waterfall in southeastern British Columbia...`, known 27, unknown 0, ok, 0.175 s, `defined` +1. Typed again: recalled in 0.154 s, no source asked, 1 row. The owner's "asked a definition, looked it up, wrote it, and then asked again it should recall what it has learned": live.

**Where the time went:** the kernel's counters for one recall: 16 hops in 4 ms, 7 pastes in 146 ms, no returns. Its statement profile: one span 138,781 µs per paste, the per-line sheet run (run 7, cells know 26, remember 27, shape 28) that heard's row calls on every line; its shape cell read the `hit` table of the line's first symbol, every landing that symbol ever had (define: about 1.4 million), newest first, for the call of the row it landed on. `SHAPE-nk.txt`, two lines: the same run with the shape cell read from the DNA row itself (the first symbol's row keyed by heard before and the next non-space symbol after), and heard's row bound to it (run 19936643). After: `print : who` 9 ms at the kernel (3 pastes, 1 ms); recalls 10 to 14 ms at the kernel, 31 to 40 ms wall through the door, 18 hops, 7 pastes in 2 ms. The shape cell now names the current define run (19936582) where the hit read gave the stale 6459431.

The owner's figure was "like 7 hops done... probably 20 microseconds.... maybe a ms because of the standing question and the encoder". What stands: 18 hops, 10 ms. The 10 ms is the per-line floor: the sheet run's three pastes, the define run's three and the ask's one, the ok returns, and the sixth being told the line.

## Second pass: the page (hp:8058/full)

**Why about 200 points showed:** a point is drawn once a receipt in the history reached it, and since tries/32 a return's receipts are process and go when its line completes, so a definition's words never reached the history; only the newest lines' own symbols were present.

**Changed:** a definition word is present from the hit that reached its point (the bundle sends `defw`, the words of the newest 400 lines' points' definitions, read through the encoder); a relationship row carries its run and is present from the start of the history's window when it was laid before it (the bundle sent 0, so no relationship line was ever drawn); the bundle sends the definition-row and memory counts for the included points only (1.77 million entries → 131 thousand; 51.6 MB → 40.1 MB); the door drops its cached bundle when a line is typed through it (the page reads the brain again after its line and saw none of it for up to 600 s); K 400 → 2,000 newest lines. The look is untouched.

**Measured in headless Chromium** (`cdp3.js`, `cdp4.js`, `cdp6.js`): 70,799 points sent, 19,759 drawn at the end of the history, 71,017 lines between them; the page ready in 88.6 s on a fresh bundle, 50.6 s on a cached one; a step at the end 195 to 324 ms; play from the start about 13 hits a second; play at the end does nothing because nothing follows the last hit. The bundle itself costs the kernel 1.9 s. The profiler's account of the load and a line typed through the page's own prompt: see the paragraph below.

## Not done, and the owner's calls

- The hub (8056) was not touched: it holds the same per-pair hop records and the define that always asks.
- The hop shard's times undercounts by the aborted pass's folded times (above).
- The sixth's define row (before the sixth, `:` after, 1,363,616 times) still calls the old define run 6459431: the sixth's own asks always ask.
- The duplicate definition rows from the midday check stand (deleting rows is the owner's word).
- The page draws about 20 thousand points at 200 to 300 ms a step; the brain holds 1,317,423. Drawing them all is a different drawing (instanced points), the owner's call.

---

# First pass (midday): does a define of a defined point recall? Checked live on hp, ten points

The owner: "now if you ask define : ??? <-- insert anyword that has a full known definition, it should respond with that definition at runtime speed... if it doesn't something is likely incorrect. or not setup correctly..... essentially if it does, for the first time the brain learned on it's own. asked a defintion, looked it up, wrote it, and then asked again it should recall what it has learned. check on about 10 words and report back".

Not a build. Ten `define : X` lines typed through the door on hp (10.31.1.106:8058), each point already holding a full definition (92 to 992 rows in its own table), each run read back live: `recall_check.py`, the output `recall-check.txt`.

## What the running brain did

| Point | Rows in its table before | Rows after | Seconds | Hops of the line | Returns from the sources under it | Sheet |
|---|---|---|---|---|---|---|
| hinge | 564 | 752 | 1.62 | 6 | 188 (wn, gcide, moby, wikt) | def, known 658, unknown 96, ok |
| know | 992 | 1,240 | 0.90 | 4 | 248 (wn, gcide, mwt, moby, map, wikt) | def, known 1,344, unknown 206, ok |
| truth | 132 | 264 | 0.48 | 4 | 132 | ok |
| water | 370 | 740 | 0.94 | 4 | 370 | ok |
| house | 465 | 930 | 0.86 | 4 | 465 | ok |
| river | 92 | 184 | 0.36 | 4 | 92 | ok |
| stone | 524 | 1,048 | 0.77 | 4 | 524 | ok |
| bread | 170 | 340 | 0.36 | 4 | 170 | ok |
| horse | 530 | 1,060 | 0.67 | 4 | 530 | ok |
| tree | 216 | 432 | 0.59 | 4 | 216 | ok |

`defined` stayed 722,272. `returns` rose by 2,935, the sum of the ten.

**The answer was no.** Every one of the ten asked all the sources again, exactly as a first define does, got back the same rows it already held, and wrote every one of them into the point's table again. The table doubles each time: hinge, typed four times today, holds four copies of its 188 rows. The 0.4 to 1.6 s is the sources answering and the returns being cut and written; the line itself is four hops. The sheet is filled (def, known, unknown, ok) and the run completes, so nothing on the sheet shows it was a relearn and not a recall.

## Why

Nothing in the define read the point's own table before asking. The define formula's first span (`LINES-nk.txt` line 10, my SQL) wrote `what` and then unconditionally replayed the ask (line 8), which declares cell def and puts the symbol into every source's inbox. And `ended` in `nk.c` appends a definition row for every return that is about a point, with no regard for the rows the point already holds. The repeated typed line is counted as a repeat (hinge's run `same_as` its earlier one) and fires from memory, but the ask is a BUILD span, so firing it asks the sources again.

The owner's words that say what it should be: "run the fucking learning run in fucking ram ... from then on ...unless a point has to refucking learn something at that point .. ram doesn't ever have to touch that point cpu does, because the fucking data lives on disk"; "a defined word is a closed run, that closed run becomes a deterministic run on cpu". Laid in the second pass above.

## A fault of mine found on the way

Since the door's restart at 11:23 (tries/32, third pass), no typed line reached the brain: the door matched typed lines to runs by reading the whole `input` table, a read with no key, which the kernel now refuses; the door answered `{"error": "'rows'"}` to every line. Fixed in `serve8.py` (`door_fix.py`): the typed lines come from the kernel's `newest` mailbox read. Door only; the kernel was not touched. The 11:10 `define : hinge` reads in tries/32 were typed before that restart and stand.

## Files

`recall_check.py`, `recall-check.txt` (midday); `hop_patch.py`, `hp-g34-hop.sh` (the hop); `RECALL-nk.txt`, `RECALL-2-nk.txt`, `SHAPE-nk.txt` (the lines, also in `tries/28/kernel`); `probe2.py`, `learn_probe.py`, `time_probe.py`, `read_runs.py` (live reads); `door_fix.py`, `page_patch2.py`, `serve8.py` (the door); `cdp3.js`, `cdp4.js`, `cdp6.js` (the page in headless Chromium). The kernel sources as they run: `tries/28-2026-10-30-nk-the-kernel/kernel/`; the page and door: `tries/28-2026-10-30-nk-the-kernel/door/`.
