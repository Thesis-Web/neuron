# Gate 0 contract (tries/39, 2026-11-02 22:24 CST): the baseline, frozen before any gate test runs

Checkpoint C1 of the neuron project in the Cortex: "gate 0 baseline (the 10-31 review's proposal, not owner-ratified): freeze owner authority, source versions, first negative tests, test-machine footprint". Expected output: "a versioned contract and predicted traces are written before code". This file is that contract. The predicted traces of §4 were written before any of the tests ran; the live outputs go in `STATE-END.md`, never here.

[mine] The "10-31 review" the checkpoint names is the build chain of 10-25 (`specs/current/NEURON_BUILD_CHAIN_TO_ACCEPTANCE.md`, "not yet owner-ratified"), whose gates 0 to 3 I typed into the Cortex on 11-02 as C1 to C4. The owner's words of 11-02 22:11 ("about /neuron you have outline tasks to complete... and return outputs to the cortex") are the order to complete them as they stand in the Cortex. Nothing here ratifies the chain; it records what is tested and against what.

## 1. Authority, frozen (the owner's order of 10-25, as `specs/current/NOTE.md` holds it)

1. The owner's words: `prose/`, the 10-23 dictation, the corrections of 10-24 to 11-02 in `CHANGE-OF-STATE.md` §1 and in each try's NOTE.
2. `specs/current/NEURON-REFERENCE-DRAFT-1-2026-10-23.md`.
3. The Thesis (`specs/current/Neuron-Thesis-2026-10-15/`): explains, does not override.
4. Existing builds are evidence about those builds, not law; builder ideas are hypotheses until approved.

Prohibited substitutions (the chain's step 3): no external cognitive engine, no host-language next-hop walker, no hard-coded meaning, no canned reply, no external semantic matcher, no fixed command list standing in for learning. The thirteen laws of draft §12 as `LLM-HANDLER.md` §2 lists them.

## 2. Versions (read live on hp2 into `VERSIONS.txt` beside this file)

- The archive: HEAD 8aec227 (tries/36, 11-02 18:14). The kernel sources as they run on hp = the uncommitted working tree of `tries/28-2026-10-30-nk-the-kernel/kernel` after tries/37: nk.c 2987f97a…, nk.h 7f77fe22…, nkio.c 8883f99d…, nkmap.c 03e8159b…, nkvt.c 30d670e0…, nkxyz.c 8de88772… (first 16 hex of sha256). Copied byte for byte to hp2 (the same shas there) and built with the archive's build line; the binary's sha 1fb03765….
- The line files: the twenty-two files that educated the Cortex brain on 11-02 15:03 (hp's own, copied 14:50), typed in the order hp's ledgers show; their shas and sizes in `VERSIONS.txt`.
- The sources: wn, gcide, mwt, moby, map, sqldoc, measured, wikt, plus the guesser's file present but out of define since 10-31 (tries/31); sizes and times in `VERSIONS.txt`.
- SQLite and the Linux kernel on hp2: in `VERSIONS.txt`.

## 3. Test-machine footprint

hp2 (2 cores, 7,834 MB, 395 GB free), folder `~/cortex/gates` (the kernel and line files, a copy of the sources, the brain), the scratch kernel on 127.0.0.1:7009 with `NK_MAP=~/cortex/gates/brain/brain.map`, educated by `educate-gates.sh` (the Cortex's `educate.sh` with the port, the folder, and no pkill). Not touched: the Cortex brain on 7007, the kernel on hp, the hub. The owner's law: a test never shares a folder with a running brain.

## 4. The first tests, with negative controls and predicted traces

The predictions are shapes with equalities; run ids and clocks are read live and written into `STATE-END.md`. A prediction that fails is written as failed; the test is not changed.

### Gate 1 (C2): the c substrate. Expected: the same prescribed physical actions produce exact read and write results and real errors.

| # | action (the door's request) | predicted trace | negative control |
|---|---|---|---|
| 1.1 | `type main gate one two`, twice | the first returns a run R1 with born 3; the second a run R2 > R1 with born 0, and `q SELECT id, same_as FROM main.run WHERE id = R2` shows same_as = R1 (a repeat is a tick on the first run, not a second memory row: R1's run_memory row shows again 2) | a line typed once has same_as 0 |
| 1.2 | `q SELECT gate FROM main.label WHERE symbol = 'water'`, twice | the same one row both times | `… symbol = 'nosuchsymbolqq'` → rows [] (an empty read, not a guess) |
| 1.3 | `q SELECT count(*) FROM main.label` | an error naming the refusal of a keyless read, no rows | the keyed read of 1.2 keeps answering after it |
| 1.4 | `q SELECT * FROM main.nosuchtable` | SQLite's own error text (no such table), no rows | — |
| 1.5 | `frobnicate` (a request the door does not know) | an error, no crash: `stats` answers after it | — |
| 1.6 | a typed line of nonsense symbols `glorpf snarb wibble` | accepted like English: a run id, born 3; the substrate attaches no meaning | — |
| 1.7 | a write in the brain's own REBIND form, `BUILD UPDATE dna SET call = 0 WHERE gate = G AND before = B AND trigger = T ; BUILD`, then `q SELECT call FROM main.dna WHERE gate = G AND before = B AND trigger = T` | the read shows call 0 exactly; the restore line puts the old value back and the read shows it | another row of the same gate reads unchanged |

### Gate 2 (C3): one actual neuron. Expected: different arrivals select correct shards; an unknown produces a recorded miss; disabling the dna disables the behavior.

[mine] In nk the arrival of a hop is the symbol before (the previous non-space symbol; at the first position the run's arrival), and a neuron's function rows are its dna rows keyed (gate, before, trigger). Those are the brain's own words for the chain's "arrival" and "shard". A recorded miss for an unknown: the new point's neuron row shows nodes 0 after its define, and the run's memory row holds the line.

| # | action | predicted trace | negative control |
|---|---|---|---|
| 2.1 | `q SELECT shard, before, trigger, call, spawn, times FROM main.dna WHERE gate = <gate of :>` | several rows with different `before` values (define, describe, meaning, why …) | — |
| 2.2 | `define : stone` then `describe : stone` (two lines arriving at `:` from different befores) | the run_receipt of each run shows the `:` hop on a different shard, each the dna row whose before is that line's first symbol; each row's times ticked by one | `define : rock` hits the same `:` shard as `define : stone` |
| 2.3 | `define : glorpfx` (never seen) | born 1; the sources return nothing: the point's neuron row shows nodes 0, the run's memory row exists (run_memory WHERE run = R) | `define : stone` shows nodes > 0 |
| 2.4 | disable: the REBIND form setting call = 0 on the dna row whose call the hits of `define : stone` show as the one that asks the sources; then `define : rock` | `main.secondary WHERE run = R` has 0 rows (no source asked) and rock's nodes stay 0; restore the call, `define : river` → secondary rows > 0, nodes > 0 | the restore is the other half of the control |

### Gate 3 (C4): run sheet and readiness. Expected: a wrong cell never resumes; the right cell resumes exactly once; it persists across a restart.

[mine] In nk a return is a sub-run (kind 3) under the asking run, keyed by that run and the cell it was asked for; when it ends it fills that cell on the parent (run_sheet: cell, state 1, value = the sub-run's id) and the ok neuron ticks a row per cell populated; the parent completes when no cell is open. So "the right cell resumes exactly once" = the asked cell is set once and the run is in `complete` once; "a wrong cell never resumes" = no cell the run did not ask for is set and the ok neuron's other rows do not tick.

| # | action | predicted trace | negative control |
|---|---|---|---|
| 3.1 | for R = `define : stone`: `q SELECT id, arrival, parent, root, kind, cell, about, ended FROM main.run WHERE id = R`, and each sub-run named by `main.secondary WHERE run = R` (its made column) read by id | the parent's identity and ending; every sub-run has parent R, kind 3, cell = the cell asked for, about = stone's gate, ended 1 | — |
| 3.2 | `q SELECT cell, state, value FROM main.run_sheet WHERE run = R` | the asked cells state 1 with sub-run ids as values; no cell outside the asked set | — |
| 3.3 | ok's rows before and after `define : river`: `q SELECT before, times FROM main.dna WHERE gate = <gate of ok>` | only the rows of the cells the define populates tick, by exactly 1 each; `main.complete WHERE run = R` has one row | — |
| 3.4 | stop the scratch kernel with SIGTERM, start it again on its file; repeat 3.1 and 3.2 for R; then `define : stone` again | the same rows after the restart; the define recalls with no source asked (secondary rows for the new run: 0) | the Cortex brain on 7007 is up throughout, same pid |

## 5. What this contract is not

Not a build: the kernel is the archive's as it runs on hp. Not the owner's ratification of the chain's gates. Where a clause of the chain's words has no row in nk, the test says so and the gap stays a gap. C7 (the sixth asks meaning questions itself; belief from evidence; formulas from state; triads when proven) is not in this contract: it is a design step on the live brains, the owner's, and not mine to start from here.
