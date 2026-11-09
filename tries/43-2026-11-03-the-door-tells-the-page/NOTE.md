# tries/43 (2026-11-03, 13:45 to 13:56): the door tells the page

The owner, 13:00: "could it not just be an action of the db to notify the middleware a point moved? thus instead of needing huge batches
'snapshots' everything trickles in in real time? ... a simple trigger add on the runs that is basically a relationship of the relationships
... it would just be reporting a change ... the way I read the current state you are waiting for a lot of stuff to happen then taking a big
picture of and trying to figure out what changed, instead of everytime something changes it's reported to the middleware". And 13:30, on
my answer: "basically a timer and a sweep,,, both which just won't work in a system like this.... a webpage with two users, one is the back
end and one is the user on the front end, both are doing things and reporting or calling to the other... user control surfaces either just
talk to the front end ... unchecking a relationship pull , or adjusting the slider... but it can also talk to the backend via the prompt.
something like adjust the pull of alike for shard 3456 to 20% on run 456,678,587,945 ... we need to get these relationships more correct
and the ability for me to see the graph in a more true state, so that we can start working on the process of learning the actual meaning
triggers.... formulas so the brain can start building out more accurately... /temporal proceed". In full in `STATE-BEGIN.md`.

`STATE-BEGIN.md`, `OUTPUT-CONTRACT.md`, `STATE-END.md`, `DIFF.md` are the formula for this turn.

## What was found first (the owner's two questions)

- **The 1.2 M rel cap is mine.** `enum { CAP = 1200000, MAXR = 120000 }` in `do_bundle` (nkio.c, commit c55074c, 2026-11-01, tries/32): a
  bound on the one JSON answer the old page asked for when it took the brain whole. `like` rows fill it in table order, so the other kinds
  never arrived. Nothing in either brain needs it; after this turn no path the page takes reaches it.
- **The owner's way was half built, in the brain's rows.** The hub's trigger `xyz_go` lays a `timeline` row at the landing that moved a
  point (key1 = -gate, key2 = -1-pos) and `memory_go` lays one at a run's end (key1 = first gate, key2 = last); the kernel's `tl_move` and
  `ended()` lay the same shape in C. 442,664 move receipts in the hub's 1,136,168 timeline rows. What was not the owner's way was my door
  and page: the page asked on a clock, the hub's door answered by scanning `xyz` by `at` (0.86 s a job, 30,166 jobs since 11-02), the
  kernel page re-read the whole brain after a pass.

## Built

1. **`bottom7.py` v7.3** (`bottom7-before-v7.3.py` beside it): `Router.tell()` after each hop while a page listens: one keyed statement,
   `SELECT t.id, t.at, t.run, t.key1, t.key2, x.x, x.y, x.z FROM main.timeline t LEFT JOIN main.xyz x ON x.gate = -t.key1 WHERE t.id > ?
   ORDER BY t.id`, the rows put on every subscriber's queue (a full queue drops that subscriber); `Env.subscribe()` begins at the newest
   timeline id now; `prof['told']` counts rows and seconds. Proven on the live brain by one read (rows 1136161.. with places).
2. **`serve7.py`** (`serve7-before-stream.py`): `GET /api/stream?tab=` holds one response open per tab (server-sent events) and writes
   `{"moves": [[gate, x, y, z, at, run]...], "ends": [[run, at, first, last]...], "id"}` as the router tells; `POST /api/hold {tab, add|gates}`
   names the gates a tab holds, so its stream carries moves of those gates only (every run's end always). Live at the owner's restart.
3. **`serve8.py` on hp** (`serve8-before-stream.py`, `serve8-after-stream.py`; restarted on its file at 13:53, the kernel untouched): the
   same two paths; `tell('type')` after every line `/api/type` passes: `moved <clock last told>` and `stats` once, the event
   `{moves, passes, runs, runs_before, clock}` to every open stream. The kernel is asked only because the door itself passed a line.
4. **`page_patch11.py`** on both pages (`hub-page-before-patch11.html`, `hp-page-before-patch11.html`): `setInterval(pollMoved)` and
   `setInterval(watch)` gone; one `EventSource` per tab; `onMoves` glides held points; a run's end → `watch(ids)` reads those runs by id and
   re-reads the light bundle when one is a typed line or under a line shown; `onPass` re-reads the held gates' places by key; `hold(gates)`
   after each `loadGates`; a line under the readout says the stream's state (on the hub, until its restart: "the door has no stream yet");
   `FETCHN` counts the page's own requests; `window.__poc` gains `stream, told, fetches, streamCounts, tab`.

## Seen (`cdp_stream.js`, both screenshots)

hp: ready 8 s, `stream live`, 0 requests in 30 s of silence; `cold water freezes` typed through the door: answered at once (run 19938172),
the stream told the page 5 run ends 852 ms later, the page read them by id and the light bundle again (31 requests), then quiet; no moves
(a repeat landing moves nothing). The hub: ready 5 s, the stream line says the door needs its restart, 0 requests in 30 s of silence.

## Remainder

- The owner's restart of 8056 (`~/neuron/restart-hub.sh`) and a reload of both tabs; then `/api/prof` on the hub shows `told` growing
  with the hops and `door job` only by the page's keyed reads.
- The kernel's own tell: its loop pumps pending work between accepts and tells nobody; a run that ends after the door's line returned,
  or a line typed on the kernel's socket without the door, is not told. A few lines in nkio.c's loop (a registered tell client written to
  when the timeline grows), a rebuild, a 2 s restart: on the owner's word.
- The typed line's job poll on the page (every 2 s while the owner's own line runs) can end by the stream's run end instead.
- The prompt as the back end's control surface ("adjust the pull of alike for shard 3456 to 20% on run ...") is a formula design for the
  brain's rows when the meaning triggers are defined: the owner's.
- C14, the brain's own tension (neighbours react per shard), still the next build in the brain on the owner's word.
