# tries/37 (2026-11-02, 21:16): the state at the end of the turn, read live

The before is `STATE-BEGIN.md` (19:40). Read at 21:16 from the running brains, the door, the process and a read-only connection on the
hub's brain file (`hubread`, nothing written); the Cortex on hp2.

| What | Read at 21:16 |
|---|---|
| hp `/api/info` | ready, busy none, queued 0; defined 722,284; runs 19,938,171; refused 1; pending 0; heap 29 MB; `nk` pid 324376 up 52 min (started 20:23 on its file with the re-step code, the third start of the turn), the door `serve8.py` up 49 min; load 0.00 |
| the places on hp | the re-step live: `restep CLOCK GATE,...` replays the beginning (`out/brain.map.xyz.0`) forward over the move receipts and answers the places; `moved CLOCK` lists the points moved since; exact on water at four clocks (NOTE) |
| the timeline on hp | an entry per ended run, plus since clock 19938165 an entry per move of a point by a landing (at, run, −gate, pos) and one per settle pass (key1 0, key2 the pass) |
| hp's test kernel | `nk.new` pid 294586 on port 7008 (`out/agree2`) has been running 2 days 4 h beside the live kernel: a leftover of tries/28's agreement runs, 1.6 MB resident, idle |
| the hub's door (8056) | busy: job 568, the `BUILD DROP TRIGGER xyz_go ; CREATE TRIGGER xyz_go ...` line, 4,787 s, not begun; job 569 queued (the previous script's next line); `routers.main.hops` 1,197,396 and `sixth.hops` 828,854, unchanged since 19:40; `serve7.py` pid 530833 at 100 % of one core, 2.1 GB resident |
| the hub's brain file | WAL last written 19:39:58.466 (sixth's 19:39:58.480); nothing committed since; clock 4,752,733; main.hop 0 rows and sixth.hop 1 row (the landing at pos 1 of `seen : 4752717`) as of that commit; label 795,996; rel 3,310,406; xyz 82,790; timeline 598,283 rows, 0 move rows; `xyz_go` the trigger of tries/35 (4,770 characters, no timeline write): the line of this turn never ran |
| the hub's last committed work | `define : cerebellopontine` (main run 4752717, arrival the sixth, 19:39:56 to 19:39:58: 2 call replays, 1 spawn, returns from mother and from wikt (gate 3369) about 207135; its `def` cell left empty, `unknown` 5 gates) ended, memory 598283, told the sixth `seen : 4752717` (sixth run 944536) |
| the router since 19:39:58 | one open transaction (the batch that took the `seen : 4752717` landing) and inside `serve()` ever since: the door's reads, queued faster than they finish (the page's 120 s re-read of the whole bundle: the graph 204 MB, the run table 4,752,732 rows, label, out_user, the counts; pollMoved every 2 s; the typed line's 0.2 s polls); `door job` 23,288 → 23,835 jobs and 7,377 → 10,375 s between 20:41 and 21:34; 150 to 300 MB/s of page reads and a 375 MB block built and freed every ~46 s (the run table into Python and JSON); no hop, no commit. The brain's own chain from that hop drains in 21 s on the twin (1,064 hops, slowest 0.53 s) |
| the pages | hp's page and the hub's page file (20:25) carry `page_patch7.py` (the brain's places drawn and moved, the memory nodes from the bundle); the headless check timed out (exit 124); unverified by me |
| the Cortex (hp2) | neuron project: C5 done (the re-step), C6 working (the page), C7 open; cortex C5 working; the hub finding ingested (run 264997, 21:15); jev still without a key, verdicts by sheet and geometry |
| the archive | `tries/37`: NOTE, STATE-BEGIN, STATE-END, DIFF, `nkxyz.c`, `restep_patch.py`, `restep_check.py`, `page_patch7.py`, `HUB-XYZ-TIMELINE-v7.txt`; `llm/skills/` the two skills `/neuron` and `/temporal` (live copies in `~/.claude/skills`) |
