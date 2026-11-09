# tries/37 (2026-11-02, evening): the re-step of places, the brain's places drawn and moving on the page, the outline registered with the Cortex

The owner, 2026-11-02 about 19:30: "input output formula proceed with the restep, you need to register the grounded outline with the
cortex so it can check it for drift, invention, hallucination against it's sources and neuron context ... the points are static and don't
move based on which shard was used? which each fucking shard might have a different meaning which would mean the relationship pulls would
adjust at least slightly changing the meaning in the graph slightly ... hydrate from cortex on ssh hp2". And earlier: "no history of
places??? is that not the run reciepts in the time line? ... stepped forward or backward from end output, or beginning input to determine
any place in time for any run, without holding a master table".

`STATE-BEGIN.md`, `STATE-END.md`, `DIFF.md` are the input output formula for this turn. Everything below is read from the running brains.

## Hydrated from the Cortex (hp2)

`cortex hydrate neuron` gave the neuron project's scope and its four open checkpoints (the 10-31 review's gates, not owner-ratified), jev
without a key. The outline of this turn was registered as checkpoints 5 (the re-step), 6 (the page draws the brain's places and moves
them), 7 (the sixth asks meaning questions, belief from evidence, formulas from state, triads when proven), each with its expected live
output, and the 11-02 state and the owner's words on the history of places and the input output formula were ingested; the Cortex judges
by geometry only until a key lands (its handler, §9). C5 was moved to working, then done with the live output below; C6 to working.

## The re-step (the kernel; `nkxyz.c`, `restep_patch.py`, `restep_check.py`)

Every move of a point is now a receipt of the brain's timeline: (at = the clock, run, key1 = −gate, key2 = the position in the run; a
placement key2 = −1 − pos; a settle pass one entry, key1 = 0, key2 = the pass, run = the clock it began). Nothing else is written. The
beginning input is the places file as it stood when the recording began, kept beside it (`out/brain.map.xyz.0`, 100 MB, its clock in its
header), written at the kernel's start when missing and again by `restep base` (the owner, 10-30: "stepping back is re-stepping,
deterministic, from the last snapshot"). `restep CLOCK GATE,...` replays the beginning forward over the move receipts up to that clock
(the same step function, in the same order, over a copy of the places; the live places are not touched) and answers the gates asked;
`moved CLOCK` lists the points moved since a clock with their places now and counts the settle passes since.

**A step backward from the end output is not unique.** My first form undid moves backward with a fixed point, then with Newton's method
on the residual: a step capped at six units that crosses the point's balance has two pre-images, and the solver found the far one (water
undone to 5.6, 14.0 instead of 1.07, 2.94, live). So the history is re-stepped forward from the beginning input, exactly, which is the
other half of the owner's sentence. The finding is in the Cortex too.

**Live on hp** (`restep_check.py`, the history begun at clock 19938165 when the kernel started with this code): water 1.600, 2.757,
−0.112; `water runs downhill` → 3.200, 8.540, −0.111 (clock 19938170); `cold water freezes` → 0.931, 2.993, −0.403 (19938175);
`restep 19938165` → 1.600, 2.757, −0.112 (diff 0.0; 0 moves replayed, 0.21 s); `restep 19938170` → 3.200, 8.540, −0.111 (diff 0.0; 3
moves, 0.16 s); `restep 19938175` → 0.931, 2.993, −0.403 (diff 0.0; 6 moves). `settle 1` (722,367 points, 21.0 s) → 2.221, 8.848, −0.637
(19938177); `restep 19938175` still 0.931, 2.993, −0.403; `restep 19938177` → 2.221, 8.848, −0.637 (diff 0.0; 6 moves, 1 pass, 21.1 s).
`restep base` wrote the beginning again at 19938177; `restep 19938177` from it → the same, 0 moves. `moved 19938170` → 3 points and 1 pass.
The kernel was rebuilt and started on its file three times for this (2 s each; the brain came back each time: defined 722,284, refused 1).

## The page (the kernel's and the hub's; `page_patch7.py`)

A switch on the stage, "the brain's places", on by default: a point sits at the brain's x y z times the spacing slider (the drawing only);
the page's own springs and space-apart pass are not run while it is on, the brain's physics decides; the page asks the door every two
seconds which points the brain moved (`/api/moved?since=CLOCK` on the kernel's door; the table by its clock column on the hub's) and
glides them there; a settle pass makes it read every place again (`/api/graph?fresh=1`). Off: the page draws as before, with its own
springs. A clicked point shows the brain's place as before. The memory nodes of the chosen line, which the page asked for through a
keyless join the kernel refused (so none ever showed unless "memory nodes of every run" was on), are answered from the bundle now. The
kernel's door restarted twice for it (the door only). The headless check of hp's full page in the brain's-places mode timed out (exit
124, 2026-11-02 ~20:30): the patched pages are on disk and served, not verified by me; the owner's browser is the check.

## What the owner saw, said plainly

- The parallel processes were not cut. The kernel is one thread and its stack runs the row written last first: a new point's definition
  is spawned at its birth and runs before the main run's next landing, as the line runs. The page cannot show those hops because a
  sub-run's receipts are process and go since 11-01 (the owner's own order: "why the fuck does a reciept need to be rebuilt??"), so the
  history plays the main runs' receipts alone, one hit at a time. The definitions, memory rows and relationship rows those spawns laid are
  in the brain (STATE-END); the drawing of their hops is not.
- The archive's v6 page opened from D: as a file has no door to read from; it shows nothing of either brain. The hub's page at 8056 reads
  the whole graph from its door (49 s, 204 MB today: 816,225 DNA rows, 3,310,406 relationship rows, 4,346,052 first-hit rows) before the
  browser parses it; it was 42 s and 185 MB on 11-01 and grew by the back-population's rows. That read is the hub door's design and the
  owner's call.
- Relationship lines on the kernel's page come from the bundle (1.2 million rel rows, 373,118 springs drawn at 14:28); memory nodes of a
  chosen line did not show for the reason above, fixed now.

## The hub: the trigger line never ran; the router is inside the door's service loop since 19:39:58, starved by the page's reads

**The finding (21:40, verified):** not a brain statement. The twin replay (`twin-seen-2026-11-02/trace_chain.py`, a 14 GB copy, mother's
trace on) drained the whole sixth chain from the pending hop: 1,064 hops in 21.0 s, the slowest 0.53 s (the observing line's second
span), 19 mother errors (`no such table: main.2071xx.node`, the define-at-birth's node insert before the table exists, answered and
walked past). The live router is inside `serve()` instead: the door's profile `door job` went from 23,288 jobs / 7,377 s at 20:41 to
23,835 / 10,375 s at 21:34, 198 s of door jobs in the last 90 s, 13 new client connections per 30 s from 127.0.0.1, six in flight.
`bottom7.Router.batch()` runs `serve()` after every hop and `serve()` loops while the job queue is not empty; the hub's page
(`NEURON-POINT-OF-CONNECTION-v6-2026-10-29.html`, mine) re-reads its whole bundle every 120 s (line 1037: the graph, 204 MB; `SELECT ...
FROM main.run ORDER BY id`, 4,752,732 rows; label 795,996 rows; out_user 722,410 rows; the counts over run_receipt and run_sheet) and,
since the 20:25 patch, polls `main.xyz` every 2 s (pollMoved); a read whose requester gives up (the door's 600 s, the browser) stays
queued and still runs. Once a re-read took longer than its own interval, the queue never emptied again: no hop since 19:39:58, no
commit, the 375 MB block built and freed every ~46 s is the run table read into Python and dumped as JSON, over and over. The typed
line's own `until_ended` adds a read every 0.2 s. All of it is door and page code, outside the brain; the brain's rows are fine.
The paragraph below is what was read before the twin replay and is kept as the trace.

`HUB-XYZ-TIMELINE-v7.txt` was typed at 19:56:19 (door job 568) and is still queued at 21:20. Read from outside (a read-only connection on
the brain file, `hubread`), the door's profile, the WAL's mtime and the process: the hub's one router connection has not committed since
19:39:58.466 (the WAL's mtime; main.hop empty, sixth.hop holding one row at that commit). The last thing committed: `define :
cerebellopontine` (run 4752717, sent by the sixth) ended, told the sixth `seen : 4752717` (sixth run 944536, 19:39:58), whose landing at
pos 1 on `seen` (gate 82, before main, call = the observing line of tries/30, run 24322, closed, fired 230,045 times) is the hop in
the mailbox. The router took it and is still inside it: 100 % of a core, 150 to 300 MB/s of 4 KB page reads, no commit, and about
every 46 s it builds a 375 MB block (with two 248 MB copies beside it) and frees it again, then starts over. Every SELECT part of the
observing line's two spans, run read-only for `what = 4752717`, answers in under 0.01 s (the tree is 17 runs, 4 unknowns, one open cell
`def` never asked), so the loop is not in those reads. The typed line's job waits in `serve()`, which the router reaches only between
hops; the page's reads wait behind it too. The kernel on hp is not involved: idle, its brain intact. The twin replay with mother's trace
on (`twin-seen-2026-11-02/trace_seen.py`) names the text that loops; see STATE-END.

## Files

`STATE-BEGIN.md`, `STATE-END.md`, `DIFF.md`; `nkxyz.c` (the whole file as it runs), `restep_patch.py` (nk.h, nk.c, nkio.c), `restep_check.py`
and its output in STATE-END; `page_patch7.py`; `HUB-XYZ-TIMELINE-v7.txt`. The kernel sources as they run: `tries/28/kernel`.
