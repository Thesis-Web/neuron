# 25. v7: mother as a router, the pump gone, the sixth on its own connection (2026-10-29 night)

**Status: built and measured on copies of the live brain at the owner's word ("ok do it ... let's make it happen", "make this v7 ... so that if we need to roll back we can"). Not switched live: the 8056 door and the live brain are v6, untouched. A v7 door runs on a copy at http://localhost:8057/ for the owner to look at.** The chain of every choice, five columns, is `CHAIN-v7-2026-10-29.md`.

## What v7 is

Three files beside the unchanged brain files: `brain/mother7.c`, `brain/bottom7.py`, `page/serve7.py`. The egg, the triggers, the taught lines and the brain files are those of v6.

- **mother7**: mother(text, ...) pastes one text at SQLite's prompt and answers ok, the rows, or the error. The pump is gone: in v5 and v6 she went on, inside the typed line's statement, to drain every attached brain's hop table herself, newest first, so a whole line was one statement, one transaction and one door job, and nothing could touch the brain until it ended. She keeps a memory of texts already prepared, per connection.
- **bottom7**: a router loop per brain on its own connection. It takes the newest row of that brain's hop mailbox (one `DELETE ... RETURNING`), pastes it as a statement, keeps SQLite's refusal in that brain's refused table, commits every 64 hops or when the mailbox is empty, and then wakes the other brain, since a row written for it is visible only after the commit. A router with an empty mailbox waits for a wake; no timer. Newest first stays: hit_go writes a hit's steps so that a call or a birth finishes before the landing after it, and every formula taught relies on that. Both brain files are in WAL mode (set at open; stays on the file), which is what lets a reader never wait and makes a commit cheap. The sixth is its own connection and thread, the same core trained differently, with no sources attached (the owner: it calls the brain for source drops if it needs them).
- **serve7**: the door. A typed line is an insert on the typing connection and waits for its own run to end (its memory row), not for every mailbox to run out, so a cascade the brain starts does not hold the prompt; what the sixth fills later shows on the page's next read. Every read the page asks for (the graph, the lines, a SELECT) runs at once on a reading connection, while a run is going.

## Measured (`measure/`), the same three lines on fresh copies of the live brain

| | v6 (control) | v7, a commit each hop (first form) | v7, batched |
|---|---|---|---|
| `define : only` | 79.3 s | 112.0 s | 62.8 s |
| `print dna : who` | 2.2 s | 2.0 s | 1.8 s |
| `define unknown : 1` | 12.4 s | 19.8 s | 10.2 s |
| runs, hits, born, every cell | 1,464; 78,501; 650 | identical | identical |
| refused, both brains | 0 | 0 | 0 |

The first form committed on every hop and wrote every dirty page again each time; the batch of 64 is a buffer, not a choice of order (mine). Measured: 89,901 hops in 22,449 commits, about 4 a commit, because the mailbox empties often as the two brains hand each other lines; a better batch is open.

**The door on the copy at 8057:** `define : across` typed through it ran 49.2 s (747 runs, 46,613 hits, 324 born, 0 refused); three seconds in, a graph read (23,383 DNA rows over 4,531 tables) answered in 12.6 s and a SELECT at once, while the define was running. Under v6 both would have waited for the define to end.

**What v7 does not change:** the hop is still about twenty statements a hit (the egg's land_go and hit_go), the floor measured in `audits/NEURON-V6-TIME-PROFILE-2026-10-29.md`; the three speed lines of `tries/24` (the hop's table test through the schema's hash; two indexes on run) are still the owner's to type and would stack with v7.

## The cascade under v7, on the copy (`measure/CASCADE-DEMO-ON-THE-V7-COPY-2026-10-29.log`, `measure/FEED-LINE-...`)

The owner (23:50): define one word and the unknowns define until they run out. The self-feeding observing line of tries/23 typed at the sixth on the v7 copy, then `define : word`. The sixth observes its own lines, so the cascade began at the bind's end: 6,766 define lines sent in fifteen minutes, 48 ended, 8,534 landings waiting, 0 refused, 4,531 to 11,592 gates; `define : word` ran and filled its def cell while the cascade went on; a graph read and a SELECT answered meanwhile. Two faults found and fixed in the files: a read or a bookkeeping statement on a connection other than the router's met "database schema has changed" (every birth is a schema change every other connection must reload, 10,000 entries each time; SQLite gives up after 50 retries inside one step), so bottom7's `steady()` and serve7's read run the statement again; the routers' own hops were never refused. And the mailbox is a stack, so a send written most-shared first defines the rarest first: the send now writes most-shared last. The demo door is left running on the copy; stopping it leaves the mailbox as it is, and starting it again resumes the cascade.

## Run it

```
cd .../25-2026-10-29-v7-mother-as-router-the-pump-gone/brain && gcc -shared -fPIC -O2 -o mother.so mother7.c -I.    # sqlite3ext.h from tries/19/brain beside it
# put bottom7.py and mother.so beside a brain folder's brain.db and sixth.db (the sources folder beside, as v6), serve7.py in its page folder:
cd page && python3 serve7.py 8057        # the page is tries/19's; serve7 finds it beside itself or in tries/19
cd brain && ulimit -s unlimited && python3 bottom7.py            # the two prompts at the terminal; "6> " for the sixth
```
bottom7's SOURCES list is the live connection's of 10-29 night (wn, gcide, mwt, moby, map, sqldoc, measured, guess, wikt; mw out, see tries/22).

## To switch the live brain to v7, and to roll back

Switching: back up the live `brain.db` and `sixth.db` first; stop the 8056 door (the owner's word, by name); put `bottom7.py` and the compiled `mother.so` in the live brain folder beside bottom6.py and v6's mother.so (keep v6's as `mother6.so`), `serve7.py` in the page folder; start `serve7.py 8056`. The first open sets WAL on the files. Rolling back: stop serve7, put v6's mother.so back, start `serve6.py 8056`. A WAL-mode file is read and written by v6's connection as well, so nothing on the files has to be undone.

## What is mine, labelled

The router in the door's process rather than in mother.c; newest first kept; the batch of 64; the wake and idle events; WAL and synchronous normal, also on the source files; the sixth as a thread not a process; reads on their own connection while typed lines stay one at a time; 'fresh' left out of the door.
