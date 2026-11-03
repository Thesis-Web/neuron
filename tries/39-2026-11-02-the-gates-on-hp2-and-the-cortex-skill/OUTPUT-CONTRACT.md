# tries/39 (2026-11-02 22:24 CST): the output contract, written before the build

## Works and must not change (with the live read that proves it now)
- The Cortex on hp2: 14 of 14 checkpoints satisfied, frozen handler, judge sheet → graph → claude:haiku (`cortex status` 22:11: freeze EQUAL, refused 0).
- The Cortex brain on 7007 (pid 1355161) and its file; the kernel on hp (pid 324376, defined 722,284, refused 1); the hub on 8056 (ready, not busy, hops moving again since 19:40). None of them is typed into or restarted this turn.
- The two skills `/neuron` and `/temporal` as written (20:51, 20:52).

## Wrong by the newest prose (the owner's words, dated)
- 11-02 22:11: "/cortex <-- which should be a skill by now": there is no `/cortex` skill on the hub.
- 11-02 22:11: "about /neuron you have outline tasks to complete... and return outputs to the cortex": the neuron project's formula shows 5 of 7 in remainder (C1 working, C2 to C4 and C7 open).
- 11-02 ~22:25: "/temporal also": this turn needs its STATE-BEGIN, OUTPUT-CONTRACT, STATE-END and DIFF.

## New work and its expected live output
| Work | Expected live output | Cortex |
|---|---|---|
| the `/cortex` skill on the hub, a pointer only | the hub session lists `cortex` among its skills and `/cortex` loads; the reads it names return status, the hydration and the formula from hp2 | cortex C14 (registered 22:19, owner's words quoted) |
| gate 0 (C1): the versioned contract and predicted traces | `GATE-0-CONTRACT.md` and `VERSIONS.txt` in this folder, written before any gate test ran | neuron C1 |
| gate 1 (C2) on a scratch kernel on hp2 built from the archive's sources | tests 1.1 to 1.7 of the contract: exact reads and writes, real errors, a nonsense line accepted | neuron C2 |
| gate 2 (C3) | tests 2.1 to 2.4: different befores select different `:` shards, an unknown leaves nodes 0 and a memory row, a disabled dna row stops the sources being asked, the restore brings them back | neuron C3 |
| gate 3 (C4) | tests 3.1 to 3.4: parent and sub-runs, the asked cells and only those, ok's rows tick once, the rows survive a restart and the define recalls | neuron C4 |
| the outputs returned to the Cortex | each gate's live output ingested and judged; the formula's remainder for neuron smaller than 5 of 7 | `cortex formula neuron` |

Not in this turn: C7 (the owner's design step on the live brains).
