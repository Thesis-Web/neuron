# tries/41 (2026-11-03, 01:55 to 02:30): the page loads what it shows

The owner, 2026-11-03 about 01:40: "think of it like google earth... zoomed way out all the information at zoomed all the way in is not
loaded... if a run is running, all the information of every neuron doesn't need to be there, just what the relationship pulls are doing,
the lines of the hops from point to point... when the graph isn't doing anything it should still be firing 2 gb of ram and 100% core???...
see what needs to be done without breaking it all to hell.. I really like the page". And at 02:05: "ok inform the cortex of your plan
give it your outline and get the fix done..".

`STATE-BEGIN.md`, `OUTPUT-CONTRACT.md`, `STATE-END.md`, `DIFF.md` are the formula for this turn. The outline went to the Cortex first
(neuron C10, C11, C12, working; the five pieces ingested at 02:10).

## What was built: `page_patch9.py`, applied to both page files (originals beside it)

No door was changed and no brain touched. The page's reads go through the doors' existing `/api/q`, by key:
1. **The light bundle.** `loadBundle()` reads the history as before (the typed lines' receipts: on hp the door's kept base, on the hub the
   newest 50,000), then only what those receipts touch: the runs by id (and on the hub the trees of the newest 40 roots, by the `run_root`
   index), the labels, the DNA rows, the definition-node counts, the rel rows by gate and by other, the places, the first gate of each
   run, the newest 300 typed lines, the newest 400 out rows, your map, the formulas. Two dialects by `/api/info`'s version: the hub has a
   table per gate (`"N"`, `"N.node"`: read 90 at a time in one UNION ALL statement), the kernel has `dna` and `node` keyed by gate. The
   'definition' and 'answered' lines come from the node rows of the loaded gates and the first symbols of those runs. The bundle handed to
   `absorb()` keeps its shape, so the drawing, the rails and the panels are untouched. The counts over every table are gone on the hub
   (maxima by rowid instead; memory, cells and rel show 0 there until a keyed count exists); on the kernel the door answers them from
   its stats as before.
2. **Waves.** The receipts of one line are ordered by the clock: its runs sorted by their start clock, one hit of each run alive per wave.
   One press of the hop button advances the whole wave (`advance(1)`), and the readout says how many runs are alive this hop. Play steps
   waves. The history slider still moves by single receipts.
3. **The stream.** The 10-minute whole re-read is gone. Every 2 s the page asks `/api/info` (not a read of the brain); when runs ended since
   its last look it reads them by id (keyed, up to 2,000) and re-reads its light bundle only if a new typed line ended or a run under a
   line it shows; then it draws. A run chosen, or a gate clicked, that the page has not loaded is read by key then (`loadGates`).
4. `window.__poc` gained `light`, `hist`, `waves`, `loaded` for checks; `__poc.ready()` is the readiness sign (it always was; tries/38's
   checks read the closure's variables and could not).

## Seen on the hub (headless, 02:01 to 02:02, `hub-light-headless.png`)

Ready in 42 s under the owner's open tab (the old text, still re-reading the whole brain through the old door): 2,988 gates loaded,
2,833 DNA rows, 3,053 nodes drawn, 72 springs (alike 49, opposite 21: the cascade's newest words share few rel rows among themselves),
50,000 receipts in the history; no page exceptions. The door's `door job` grew by 168 jobs for the whole load. Hops did not move in that
minute: the hub's door still runs the old `serve()` and the owner's tab the old page text; both wait on the owner (reload the tab,
`restart-hub.sh`). The waves on the hub are one hit each: the cascade's defines are closed formulas that fire without hits, so their
sub-runs leave no receipts to interleave; the wave test belongs to the kernel's page (STATE-END).

## Seen on the kernel (headless, 02:48, `hp-light-headless.png`), v2 of the patch

The first cut was not light on hp: the kernel's door answers some SQL prefixes from its own whole-brain cache (`from_bundle` in serve8.py:
label, run, xyz, memory rows), so the page got 212,328 labels back for a keyed question. v2 aliases those reads (`l.`, `r.`, `x.`) so they
reach the kernel, and fetches the sub-runs of the newest six lines (their ids follow the line's id) and their receipts by run, so the
waves hold every run of a line on both brains. Result: **ready in 3 s** (tries/38: 467 s), 1,364 gates loaded, 1,465 points drawn, 3,540
springs (alike 1,335, definition 797, answered 917, is 123, includes 124, ...), 90,861 receipts in the history (88,602 of the typed lines
plus 2,259 of the newest lines' sub-runs), 84,883 waves, no page exceptions. On `cold water freezes` (run 19938167, 4 hits, and its called
run 19938168, 253 hits): the first press of the hop button moved from `hop 0 of 3 in run 19938167` to `hop 0 of 252 in run 19938168 · 2
runs alive this hop`, the next to hop 1 of 252, each press two receipts, one of each run alive. That is C12's expected output.

## Remainder, by size

- The first read of a page is still the history's receipts (50,000 on the hub) and the gates they touch; "load what is in view" would
  start from the newest line alone and fetch older lines when the slider asks. Next if the owner wants it smaller.
- Zoom (piece 4 of the plan: rel lines of the points in view, labels and DNA rows closest) is not built: the page asks for the rel rows of
  every loaded gate once, by key.
- The hub's counts panel shows 0 for memories, cells and rel rows until a keyed count exists.
- The hub's door: the one-read-per-hop `serve()` is on disk since 22:19; in force at the owner's restart.
