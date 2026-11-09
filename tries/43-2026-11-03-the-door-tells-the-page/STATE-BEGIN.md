# tries/43 (2026-11-03, 13:45): the state at the beginning of the turn, read live

## The owner's words (13:30, on the report of the cap and the polls)

"The page asks the door every two seconds whether anything moved <-- basically a timer and a sweep,,, both which just won't work in a
system like this.... on the html side you have to look at it like a webpage with two users, one is the back end and one is the user on
the front end, both are doing things and reporting or calling to the other... user control surfaces either just talk to the front end ...
unchecking a relationship pull , or adjusting the slider... but it can also talk to the backend via the prompt. something like adjust the
pull of alike for shard 3456 to 20% on run 456,678,587,945 . this would point to a specific point in time and space for the neuron to
adjust something... again later as the meanings true triggers are more defined..... we need to get these relationships more correct and
the ability for me to see the graph in a more true state, so that we can start working on the process of learning the actual meaning
triggers.... formulas so the brain can start building out more accurately... /temporal proceed"

And at 13:00, the question this answers: "could it not just be an action of the db to notify the middleware a point moved? thus instead of
needing huge batches 'snapshots' everything trickles in in real time? from the db? as it happens, in this case it's a simple trigger add on
the runs that is basically a relationship of the relationships? that relationship would not have a pull push it would just be reporting a
change? ... the way I read the current state you are waiting for a lot of stuff to happen then taking a big picture of and trying to
figure out what changed, instead of everytime something changes it's reported to the middleware".

## The last turn's after (tries/42 STATE-END), re-read where it matters

| What | Read at 13:45 |
|---|---|
| the hub door process | `serve7.py 8056`, up since 11-02, 102 % of a core, 1.2 GB resident: the OLD bottom7 (before v7.2) still runs; the owner's restart has not happened |
| hub `/api/info` | version v7, busy none, queued 0, routers main hops 2,402,013 and sixth 2,066,324, neither idle: the hub is hopping |
| hub `/api/prof` door job | 30,166 jobs, 25,791.5 s in them (0.86 s each): the page's reads on the brain's connection |
| hub `xyz` | 135,805 rows, no index on `at`; the page's `fromTable` poll scans it by `at` every 2 s (`SELECT gate, x, y, z, at FROM main.xyz WHERE at > ? ORDER BY at LIMIT 20000`) |
| hub `timeline` | 1,136,168 rows (id, at, run, key1, key2); 442,664 move receipts (key1 < 0, laid by the trigger `xyz_go` at the landing: key1 = -gate, key2 = -1-pos); run ends laid by `memory_go` (key1 = first gate, key2 = last gate). Of the newest 20,000 rows: 16,731 moves, 3,269 run ends |
| the tell statement, proven on the live brain by one read | `SELECT t.id, t.at, t.run, t.key1, t.key2, x.x, x.y, x.z FROM main.timeline t LEFT JOIN main.xyz x ON x.gate = -t.key1 WHERE t.id > ? ORDER BY t.id` answers rows 1136161.. with the moved point's place |
| hp `/api/info` | defined 722,284, runs 19,938,171, hops 33,914,820, pending 0, refused 1 |
| the kernel's timeline | the same shape in C (`Tl {at, run, key1, key2}`): a move `key1 = -gate` from `tl_move`, a run's end `key1 = seq[0], key2 = seq[last]` from `ended()`; `moved CLOCK` reads the tail newest first |
| the kernel's loop | one thread: `poll` on the socket, `accept`, one line in, one answer out; a typed line is pumped until its run ended or nothing is pending (nkio.c:140); pending work is pumped between accepts (nkio.c:421-422). The kernel tells nobody when a row lands |
| the kernel door | `serve8.py`: one socket connection per request (`ask`); `/api/moved?since=` reads the timeline tail; `/api/graph?fresh=1` the whole-brain bundle with my caps (`CAP = 1200000, MAXR = 120000` in nkio.c `do_bundle`, laid 11-01, commit c55074c) |
| the pages (both, patch8 + 9 v4 + 10 + 10b) | `setInterval(pollMoved, 2000)`: hp asks `/api/moved`, the hub scans `xyz`; on `passes` the hp page re-reads `/api/graph?fresh=1` whole; `setInterval(watch, 2000)`: `/api/info` then runs by id when the count grew, then the light bundle again. Three timers, two sweeps |
| the Cortex | 14 checkpoints, 7 done; C13 open (rejected), C14 open (the brain's tension, the owner's word); NEXT marked at C9 |

## What is wrong by the owner's words

A timer and a sweep. The page asks on a clock whether anything happened; the hub's door answers by scanning a table; after a settle pass
the kernel page takes the whole brain again. The brain already lays a receipt row the moment a point moves or a run ends, on both brains;
nobody carries it to the page until the page asks.
