# tries/43 (2026-11-03): the measured progression, STATE-BEGIN (13:45) against STATE-END (13:56)

| Row | Before | After | Progress or degression |
|---|---|---|---|
| how the page learns a point moved | asks the door every 2 s (hp: `/api/moved`; the hub: a scan of `xyz` by `at`, 135,805 rows, no index, on the brain's connection) | the door writes it down one open stream per tab the moment the brain laid the receipt; the page holds the stream and asks nothing in silence (0 requests in 30 s on both pages, headless) | progress by the owner's word: no timer, no sweep |
| how the page learns a run ended | asks `/api/info` every 2 s, then runs by id when the count grew | the stream carries the run's end (hub: the timeline row; kernel: the run count before and after the line); the page reads those runs by id and re-reads the light bundle when one is a typed line or under a line shown (hp: told 852 ms after the line, 31 keyed requests, then quiet) | progress |
| after a settle pass | the kernel page re-read the whole brain through the capped bundle | the held gates' places are re-read by key (`onPass`) | progress; the 1.2 M cap is no longer in any path the page takes |
| the hub door | serves the page's polls to exhaustion between hops (old process) | v7.3 on disk: `tell()` after each hop while a page listens, one keyed statement on `timeline` joined to `xyz`; `/api/stream`, `/api/hold`; live at the owner's restart | progress in the file; no change in the running process until the restart (the owner's) |
| the kernel door | `/api/moved` on request only | restarted on its file in 2 s: `/api/stream`, `/api/hold`, `tell` after every line it passes; the kernel binary untouched | progress |
| the hub page in the owner's tab | the old text, polling the old door (door jobs still growing: 30,166 → 30,354 in eleven minutes) | the new text is served on reload; the stream line says the door needs its restart; the polls stop on reload | progress on reload; the old tab's polls are the only load left on the old door |
| the brains | nothing typed | one repeat line on hp for the check | no degression (a repeat: no memory row, a tick, the shared receipts) |

## The contract, balanced (neuron C15)

| Expected output | Satisfied / remainder |
|---|---|
| 1. the hub door tells: `told` grows with the hops in `/api/prof`, `door job` only by keyed reads after a run shown ended | REMAINDER until the owner restarts 8056 (`~/neuron/restart-hub.sh`): the files are on disk, syntax checked and imported, the tell statement proven on the live brain by one read; the running door is the one from 11-02 |
| 2. the kernel door tells: a typed line arrives on the page's stream as its run's end within the same second; no request of the page's own in thirty seconds of silence | SATISFIED: headless on hp, `stream live`, 0 requests in 30 s, `cold water freezes` → run 19938172, 5 run ends told 852 ms after the door answered, the page re-read by id and redrew |
| 3. the page never polls; a door without the stream is said so; `__poc.stream()` and the fetch counter | SATISFIED on both: hp `live`, the hub `none: the door has no stream yet (the door needs its restart)`; 0 fetches in 30 s on both; the two timers and the table scan are gone from both page files |
| named remainder: the kernel tells nobody when its own pending work ends a run after the door's line returned, or when a line is typed on its socket without the door | REMAINDER: a kernel-side tell (a few lines in nkio.c's loop: a registered tell client written to when the timeline grows), a rebuild and a 2 s restart, on the owner's word; the typed line's job poll on the page (every 2 s while the owner's own line runs) can end the same way, by the stream's run end |
