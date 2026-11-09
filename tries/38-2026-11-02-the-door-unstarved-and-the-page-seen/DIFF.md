# tries/38 (2026-11-02): the measured progression, STATE-BEGIN (22:16) against STATE-END (22:24 and after)

| Row | Before | After | Progress or degression |
|---|---|---|---|
| the hub's door | free at 22:16 after 2 h 35 min of serving reads only; hops 1,206,328 | hops 1,209,284 at 22:24, then none to 22:52: starved again by a tab's reads (door job +1,725 s in 28 min, a trivial read waits 23.5 s) | no progress on the running door: its text is the old one and a tab keeps its queue full; the cause is removed in the served page text and in the door's code on disk, neither of which the running door and the open tab use until the owner reloads the tab and restarts the door |
| the hub's trigger of tries/37 | queued, never run | run 4752735, 2,215 hits, reply ok; `xyz_go` writes move receipts (2,745 at 22:16); water moved by `water flows under here` | progress: tries/37's hub remainder satisfied |
| the hub page | whole-bundle re-read every 120 s, unguarded; poll every 2 s, unguarded | re-read every 600 s, only when the door's counters moved, one at a time; poll one at a time, the missing `/api/moved` remembered; served; parses | progress; the remainder is the size of one re-read (~46 s of the one connection) |
| the hub's door code | `serve()` drains the whole queue between two hops; expired reads run anyway; `until_ended` every 0.2 s | one read between two hops; expired reads dropped and counted; 1 s | progress on disk; in force at the owner's restart (not mine to do) |
| the kernel on hp | defined 722,284, runs 19,938,171, refused 1 | the same; nothing typed; its page file carries the poll guard; served | no change, no degression |
| the kernel's page, seen | unverified (tries/37's check timed out) | the headless browser loads it and replays the history to its last hit (`hit 88602 of 88602`, `cold water freezes`) in about 8 minutes under software GL; the DOM read on the fourth run: 70,776 gates drawn, 42 kinds all on, the brain's places on, 1,200,000 rel rows in the bundle, no page exceptions; the screenshot saved (STATE-END) | progress: seen; the remainder is what the screenshot shows against what the owner expects (NOTE) |
| the twin | a 15 GB copy of the hub's brain | deleted | the owner's word; no copy again |
| the Cortex | C8, C9 working | C8 parts ingested (the pages, the door code, the drain and the trigger line); C9 open on the counts | progress |

## The contract, balanced

| Expected output | Satisfied / remainder |
|---|---|
| C8a: with the hub page open, hops keep growing and a typed line returns in seconds; door-job seconds stop growing at wall-clock rate | REMAINDER: the served page text is the bounded one, but the running door drains its queue whole and the open tab keeps it full: no hop from 22:24 to 22:52, door job at wall-clock rate; satisfied only once the tab is reloaded and the door restarted with the new `serve()` (the owner's), then measured |
| C8b: the door serves one read between two hops, drops expired reads (in force at the owner's restart) | SATISFIED on disk (`bottom7.py` v7.2); REMAINDER: not running until the owner restarts 8056 |
| C9: hp's `/full` seen headless with the counts and a screenshot; what the history can and cannot show | SATISFIED: the fourth run (23:14 to 23:24): the history at its last hit, 70,776 gates drawn, 42 kinds on, the brain's places on, the screenshot `hp-full-headless.png`; the account of lines, parallel runs and memory nodes in NOTE.md. The page's own point and spring counts are not reachable from outside its closure; the DOM's counts stand in |
| The hub usable at the owner's prompt (tries/37's remainder) | SATISFIED now (job 569 in 1.9 s at 22:14); fragile until the restart (a whole-bundle read still stalls hops ~46 s, once per load or per 10 min) |
| The sixth asks meaning questions itself (C7) | REMAINDER: not started |
