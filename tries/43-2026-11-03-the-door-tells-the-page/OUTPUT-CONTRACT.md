# tries/43 (2026-11-03, 13:50): the output contract, written before the build

## Works and must not change (live read that proves it now)

- The brains lay their receipts at the moment of the change: hub `timeline` row 1136168 is a move at clock 5483774 laid by `xyz_go`; the kernel's `tl_move` and `ended()` lay the same shape. Nothing in either brain is touched by this turn.
- The hub hops: main 2,402,013, sixth 2,066,324 at 13:45, neither router idle, queued 0.
- The light page opens by keyed reads (tries/41): hp ready in seconds, the hub in under a minute; the brain's places seed the points and the brain's moves glide them (tries/42, 10b); lines at 10 %.
- The kernel door answers `/api/moved?since=` from the timeline tail; `/api/type` waits until the typed line's run ended or nothing is pending.

## Wrong by the newest prose (the owner, 13:30)

"basically a timer and a sweep,,, both which just won't work in a system like this": `setInterval(pollMoved, 2000)` and `setInterval(watch, 2000)` on both pages; the hub's `xyz` scan by `at` every 2 s; the kernel page's whole-brain re-read after a pass. "two users, one is the back end and one is the user on the front end, both are doing things and reporting or calling to the other": the back end reports nothing; it is asked.

## The new work and its expected live output (neuron C15)

1. **The hub door tells** (`bottom7.py` v7.3 + `serve7.py`, files on disk; live at the owner's restart of 8056). After each hop, while a page listens, the router reads the timeline rows laid since the last id it told (one keyed statement, with the moved point's place joined by gate) and puts them on every open stream; a page that stops reading is dropped. `GET /api/stream` holds one connection per tab open (server-sent events); `POST /api/hold` names the gates a tab holds, so its stream carries moves of those gates only, and every run's end. Expected: with a page open, `/api/prof` shows `told` rows growing with the hops and `door job` growing only by the page's keyed reads after a run it shows ended.
2. **The kernel door tells** (`serve8.py` on hp, restarted on its file, the kernel untouched). The door passes every typed line; when the line's answer returns it reads the moves since the clock it last told and the run count, and puts them on every open stream. Expected: headless on hp, a line typed through the door arrives on the page's stream as its run's end within the same second and the page redraws; the page sends no request of its own in thirty seconds of silence.
3. **The page never polls** (`page_patch11.py` on both pages). The two timers and the table scan are gone; one `EventSource` per tab; moves glide the held points; a run's end is read by its id and, when it is a typed line or under a line shown, the light bundle is read again; after a pass the held gates' places are re-read by key, never the whole brain; a hold post after each `loadGates`. A door without the stream is said so in the readout (the hub until its restart), with no timer behind it. Expected: `window.__poc.stream()` reads `live` on hp and `none: the door has no stream yet` on the hub; a fetch counter in the headless page reads 0 over thirty seconds of silence on both.

Remainder named now, not built: the kernel tells nobody when its own pending work ends a run after the door's line returned, and a line typed on the kernel's socket without the door is not told; that is a kernel-side tell (a few lines in nkio.c's loop), on the owner's word.

Registered with the Cortex as neuron C15.
