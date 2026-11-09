# tries/38 (2026-11-02): the output contract, written before the build

## Works now and must not change (the live read that proves it)

- The kernel on hp: defined 722,284, runs 19,938,171, refused 1, pending 0 (`/api/info` 22:16); the re-step of places exact (tries/37).
- The hub's brain: clock 4,757,254; `xyz_go` writes a move receipt into the timeline (2,745 rows at 22:16); water moved by `water flows
  under here` (run 4752742); the sixth's cascade running (hops growing).
- Both pages' look and the brain's-places switch (page_patch7, on disk and served).

## Wrong by the newest prose

- The owner, 22:10: "you found the problem on the hub ... fix it???". The door's `serve()` serves reads on the brain's one connection
  until its queue is empty, so a page polling faster than its reads finish stops the hops for good (19:39:58 to 22:14 today); the page
  re-reads its whole bundle every 120 s whether or not anything changed and whether or not the last re-read is still running.
- The owner, 22:10: "why is the html of the kernel not wired properly?? so that I can see it work correctly, or am I reading the html wrong
  and not seeing the relationship lines, or the parallel runs?" Unverified since tries/37: whether hp's page draws the relationship lines
  and the memory nodes, and what of the parallel runs it can show (sub-run receipts are process and go by the owner's order of 11-01).
- The owner, 22:10: "you build live... you do not need a fucking twin". The twin is deleted; no copy of a brain is made again for a trace.

## The new work and its expected live output

| # | Built | Expected live output |
|---|---|---|
| C8a | the page (hub's and hp's file): a re-read only when the brain's newest run changed and never while one is in flight; one poll at a time; a door without `/api/moved` is remembered, not asked again | with the hub page open in a browser, `routers.main.hops` keeps growing and a typed line returns in seconds; `door job` seconds no longer grow at wall-clock rate |
| C8b | `bottom7.py`: `serve()` serves one read between two hops; a read whose requester gave up is dropped, not run; `until_ended` waits 1 s between asks | in force at the owner's next restart of the door (I may not stop 8056): the same reads as above measured then |
| C9 | hp's `/full` seen in a headless browser: the brain's places on, the points, the springs drawn, XYZ entries, the memory nodes of a chosen point, a screenshot in `tries/38` | the counts printed from the page's own state; the screenshot; a plain account of what the history can and cannot show |
