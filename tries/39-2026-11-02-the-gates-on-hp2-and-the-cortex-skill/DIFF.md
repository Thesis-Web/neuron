# tries/39 (2026-11-02): the measured progression, STATE-BEGIN (22:11) against STATE-END (22:33)

| Row | Before | After | Progress or degression |
|---|---|---|---|
| the `/cortex` skill | none | `~/.claude/skills/cortex/SKILL.md`, listed and loaded live; cortex C14 done by verdict (completes 0.80) | progress (the owner's "should be a skill by now") |
| the Cortex outline | 14 of 14 | 15 of 15 | progress; the frozen handler file unchanged, the new checkpoint in the brain with the owner's words quoted |
| neuron C1 (gate 0) | working, no part | done: `GATE-0-CONTRACT.md` + `VERSIONS.txt` written 22:24 before any test; completes 1.00 | progress |
| neuron C2 (gate 1) | open | done: exact reads (water → 2802 twice; unknown symbol → no row), exact writes (call 15607 → none → 15607), real errors (no query solution; no such table; unknown request), a nonsense line accepted; 3 parts | progress |
| neuron C3 (gate 2) | open | done: arrivals select shards (heard → 118, the sixth → 471, read from define's dna rows and the receipts); the unknown glorpfx left def open, nodes 0, a memory row; the disabled row cut `define : rock` from 2,228 hits to 257 and no def, the restore brought it back; 3 parts | progress |
| neuron C4 (gate 3) | open | done: run 260083's identity, its def cell filled once by return run 260091 (parent 260083, cell def, about stone, source wn), 524 node rows with the same parent and cell, the sheet unchanged across 23,000 of the brain's own runs, in complete once, the same rows after a stop and start, the define recalled in 0.03 s; 3 parts | progress |
| neuron C7 | open | open | not started (the owner's design step on the live brains) |
| neuron C8, C9 | absent | working (the hp builder session's) | theirs; not touched |
| the hub | ready, hops moving again since 19:40 | ready, hops +4,720 over the turn | no change by me |
| the kernel on hp | runs 19,938,171 | runs 19,938,171 | untouched |
| the Cortex brain | pid 1355161 | pid 1355161 | untouched by the scratch work |
| hp2 | one kernel | one kernel; a scratch brain file (469 MB on disk) stopped in `~/cortex/gates` | no degression; the scratch process is stopped |
| the predicted traces | 15 written | 11 met as written; 4 failed as written and were corrected by added checks (below) | progress: the failures named, the tests not changed |

## Predictions that failed as written (the contract, §4)

- 1.1: the second typing did not key `same_as` to the first (the first had born hops, so it is not a clean run a repeat can point at); the third typing keyed `same_as` 260052 and ticked the second's memory `again` 1 (added check 1.1b, predicted before it ran, met).
- 2.1 and 2.2: the `:` neuron has no dna rows; a line's function rows live on its first neuron, keyed by where the run arrived from (before) and the next symbol (trigger); the colon hop used the one hop shard 16 in every line. The chain's "different arrivals select correct shards" is shown on the define neuron's rows instead (heard → shard 118, the sixth → shard 471).
- 2.4, the nodes clause: a new word's birth spawns its own define (BORN-nk.txt), so nodes do not stay 0 with the define row disabled; and "rockfall" had already been defined by the brain's own sixth (remember: run 274753). The disable is shown by the hits and the def cell of `define : rock` instead (257 hits and no def while disabled; 2,228 hits and the def after the restore).
- 3.3: the ok neuron's rows tick for every cell any run populates, and the brain's own cascade populated thousands between my two reads, so the delta is not one line's. The isolated evidence is the run's own sheet (exactly the asked cells, unchanged after 23,000 other runs; added check 3.3b, met).
- The `secondary` table is not keyed by run (`no query solution`); the sub-runs were read by id from the def cell's value and from the point's node rows (added check 3.1b, met).

## The contract, balanced

| Expected output (OUTPUT-CONTRACT.md) | Satisfied / remainder |
|---|---|
| the `/cortex` skill on the hub, listed and loading, reading from hp2 | SATISFIED: listed by the harness and loaded in this session; the reads done over ssh this turn; cortex C14 done |
| gate 0: the versioned contract and predicted traces before code | SATISFIED: `GATE-0-CONTRACT.md`, `VERSIONS.txt` (22:24); neuron C1 done |
| gate 1 on the scratch kernel | SATISFIED: tests 1.1 to 1.7 (`GATES-LIVE-OUTPUT.txt`), 1.1b; neuron C2 done |
| gate 2 | SATISFIED in the brain's own rows (the reading marked [mine] in the contract): tests 2.1 to 2.4; neuron C3 done |
| gate 3 | SATISFIED: tests 3.1 to 3.4, 3.1b, 3.3b; neuron C4 done |
| the outputs returned to the Cortex; the neuron remainder smaller than 5 of 7 | SATISFIED: 12 ingests, 9 verdicts, 10 parts this turn; remainder 3 of 9 (C7 open, C8 and C9 the hp builder's) |
| C7 | REMAINDER: not started; the owner's design step on the live brains |
