# tries/34 (2026-11-01, midday): does a define of a defined point recall? Checked live on hp, ten points

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

**The answer is no.** Every one of the ten asked all the sources again, exactly as a first define does, got back the same rows it already held, and wrote every one of them into the point's table again. The table doubles each time: hinge, typed four times today, holds four copies of its 188 rows. The 0.4 to 1.6 s is the sources answering and the returns being cut and written; the line itself is four hops. The sheet is filled (def, known, unknown, ok) and the run completes, so nothing on the sheet shows it was a relearn and not a recall.

## Why

Nothing in the define reads the point's own table before asking. The define formula's first span (`LINES-nk.txt` line 10, my SQL) writes `what` and then unconditionally replays the ask (line 8), which declares cell def and puts the symbol into every source's inbox. And `ended` in `nk.c` appends a definition row for every return that is about a point, with no regard for the rows the point already holds. The repeated typed line is counted as a repeat (hinge's run `same_as` its earlier one) and fires from memory, but the ask is a BUILD span, so firing it asks the sources again.

The owner's words that say what it should be: "run the fucking learning run in fucking ram ... from then on ...unless a point has to refucking learn something at that point .. ram doesn't ever have to touch that point cpu does, because the fucking data lives on disk"; "a defined word is a closed run, that closed run becomes a deterministic run on cpu". A define of a point that already has definition rows should answer from those rows (its def cell filled from the point's table, known and unknown from the same) and ask no source; the ask is for a point with no rows, or one told to relearn. That is one change in the ask line (ask the point first, the sources only when it has nothing) and a key on the definition row (the source's row) so the same row is never written twice. **Not laid**: the owner asked for the check and the report.

## A fault of mine found on the way

Since the door's restart at 11:23 (tries/32, third pass), no typed line reached the brain: the door matched typed lines to runs by reading the whole `input` table, a read with no key, which the kernel now refuses; the door answered `{"error": "'rows'"}` to every line. Fixed in `serve8.py` (`door_fix.py`): the typed lines come from the kernel's `newest` mailbox read. Door only; the kernel was not touched. The 11:10 `define : hinge` reads in tries/32 were typed before that restart and stand.

## Not done

- The define does not recall; see above. The ten points (and hinge from this morning) hold duplicate definition rows: deleting rows is the owner's word.
- The sixth's lines and the hub (8056) were not checked for this; the hub's define has the same shape (span 1 replays the ask).
