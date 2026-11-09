# tries/38 (2026-11-02, 22:16): the state at the beginning of the turn

The before is tries/37's `STATE-END.md` (21:16, corrected 21:40), plus the owner's words of 2026-11-02 about 22:10: "why the fuck is there a
twin of the brain ???? you build live... this means you do not need a fucking twin!!!!! so you found the problem on the hub ... fix it???
so why is the html of the kernel not wired properly?? so that I can see it work correctly, or am I reading the html wrong and not seeing
the relationship lines, or the parallel runs? I am cunfused there. /temporal proceed". The twin folder (15 GB, my copy for the trace) was
deleted first.

| What | Read at 22:16 |
|---|---|
| the hub's door | **free**: busy none, queued 0; `routers.main.hops` 1,206,328 (was 1,197,396 at 21:53), sixth 835,120; the WAL written 22:14:50; door job 24,332 jobs / 12,563 s. The queue drained between 21:53 and 22:14 once the page's reads stopped arriving (the browser tab closed or the previous script ended); the hops resumed on their own |
| the hub's typed jobs | job 568 (the tries/37 trigger line) done: run 4752735, 6 runs, 2,215 hits, 0 refused, reply `run 4752740 from mother: ok`, know 258/3583, 7,438.9 s on the clock (7,420 of them waiting in the door's queue); job 569 `water flows under here` done: run 4752742, 5 runs, 5 hits, 1.9 s |
| the hub's places | `xyz_go` now 5,282 characters and writes the timeline; 2,745 move receipts (key1 < 0) already, the newest at 4757251 (`:` pos 3) and 4757244 (digits of a define's run number); water at −1.39, 7.43, −5.24, moved 8, at 4752746, by run 4752742 |
| the hub's brain | clock 4,757,254 (the sixth's cascade running again: +4,500 since 19:39:58); pending main 1, sixth 1 |
| the hub's page file | re-reads its whole bundle every 120 s (`function reread`, line 1037: the graph, the run table 4.75M rows, label, out_user, the counts) with no guard against a re-read still in flight; `pollMoved` every 2 s asks `/api/moved` (404 on the hub) and then the `xyz` table, no guard either |
| the hub's door code | `bottom7.Router.serve()` loops while the job queue is not empty; a job whose requester gave up (the door's 600 s) stays queued and runs; `until_ended` re-asks every 0.2 s |
| hp `/api/info` | ready, busy none; defined 722,284; runs 19,938,171; refused 1; pending 0; shard_rows 167 |
| hp's page as served (`/full`) | carries `page_patch7` (brainxyz switch, `/api/moved`, pollMoved); its bundle (`/api/graph?fresh=1`): dna 135 (sent), nodes 65,850, rel 1,200,000, xyz 65,933, formula 38, mem 68,036, first 30,944, clock 19938177; the same 120 s re-read and 2 s poll as the hub's page |
| what the owner sees | unverified by me: the headless check of tries/37 timed out; the owner asks whether the relationship lines and the parallel runs show, or whether they read the page wrong |
| the Cortex | neuron C8 (the door unstarved) and C9 (the kernel page seen) registered, working; the formula's before is its 21:21 after plus the 21:40 correction ingest |
