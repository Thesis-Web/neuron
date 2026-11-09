# tries/43 (2026-11-03, 13:56): the state at the end of the turn, read live

| What | Read |
|---|---|
| the kernel door (hp, `serve8.py` restarted on its file at 13:53, pid 332084, the kernel untouched) | `GET /api/stream?tab=` answers `data: {"hello": "the kernel door tells", "clock": 19938177, "runs": 19938171}` and holds the response open; `POST /api/hold` answers `{"tab": "t1", "held": 3}`; after every line `/api/type` passes, `tell('type')` reads the moves since the clock last told and the run count and puts them on every open stream |
| hp's page, headless (`hp-stream-headless.png`) | ready in 8 s; `stream live`; 1,364 gates loaded, 1,465 points; thirty seconds of silence: **0 requests made by the page**; `cold water freezes` typed through the door: answered in under a second as run 19938172; **the stream told the page 852 ms later: 5 run ends** (19938172 to 19938176, the line and its called runs); the page read them by id and the light bundle again (31 requests, then quiet); no moves (a repeat landing moves nothing); no page exceptions |
| the hub's page, headless (`hub-stream-headless.png`; the page file is served per request, so this is live on 8056 now) | ready in 5 s; the line under the readout reads `stream none: the door has no stream yet (the door needs its restart); nothing is asked on a clock`; 534 gates loaded, 606 points; thirty seconds of silence: **0 requests made by the page**; no exceptions |
| the hub door's files on disk (`bottom7.py` v7.3, `serve7.py` with `/api/stream` and `/api/hold`) | syntax checked and imported without opening the brain; the tell statement proven on the live brain by one read at 13:45; **not running**: pid 530833 is still the door started 11-02 (1 day 9 h, 102 % of a core, 1.2 GB), the owner's restart pending |
| hub `/api/prof` door job | 30,354 jobs, 25,824.6 s (was 30,166 / 25,791.5 at 13:45: the owner's open tab with the old page text still polls the old door until it is reloaded) |
| hub `/api/info` | routers main hops 2,434,502 (was 2,402,013), sixth 2,096,484, neither idle, queued 0: the hub hops on |
| hp `/api/info` | runs 19,938,176 (was 19,938,171: the typed line and its called runs), hops 33,914,827, deduped 6,260,539 (+2: the repeat), pending 0, refused 1 |
| timers left on the pages | none that asks the brain on a clock. Left: the typed line's job poll (every 2 s while the owner's own line runs, until the door says done) and the startup retry while a door opens (1 s, 3 s) |
| the brains | nothing changed in either brain's rows by this turn except the one repeat line typed on hp for the check (runs 19938172 to 19938176) |
| the Cortex | C15 working with the live outputs ingested; C14 open (the brain's tension, the owner's word) |
