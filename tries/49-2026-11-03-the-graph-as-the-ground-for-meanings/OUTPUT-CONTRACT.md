# tries/49 (2026-11-03, 19:50): the output contract, before anything is done

## What works and must not change (the live read that proves it now)

- The kernel on hp: ready, busy none, runs 19,938,181, refused 1, pending 0 (`/api/info` at 19:46). No line is typed into it this turn.
- The hub on 8056: ready, the cascade hopping (main 2,759,078 → 2,759,162 in 5 s), refused 0. Not touched this turn; its door restart is the owner's.
- The kernel door's keyed reads: 2,325 reads in 2.5 s (`places_by_shard.py`), the bundle gated (tries/45).
- The two compiled kernel patches in `hp:~/nk-build-test-c14/` stay unapplied; the live kernel (pid 324376) and its brain untouched.
- The Cortex's neuron outline C1 to C17 as it stands; no accept, reject or mark typed by me (the owner is the checker).

## What is wrong by the newest prose (the owner, 11-03 19:45 and 03:20)

- "each point, dependant on dna shard, can be correlated to the graph point at a state in time": on the kernel a plain point (how) holds 0 DNA rows since the 11-01 fold made the hop one shard; its last shard is 0; nothing records which context it was heard in as a row of its own.
- "balancing relational pulls per dna shard": `pull (kind, formula)` has no shard; the landing rule (`nkxyz.c` 108 to 114) steps a point by every relationship row through its kind's formula whenever the context changed, the same step for every context.
- "a new shard used on a point changes its pull directions a little" (03:20): not held by any row.

## The new work this turn, with its expected live output

| Work | Expected live output |
|---|---|
| Hydrate on the three skills and report the next outline item from the Cortex | `cortex hydrate neuron` names DO NOW; `cortex remainder neuron` names the next work; both quoted in the report |
| The owner's words registered as an owner source | `cortex source owner-graph-meanings-11-03` prints the sentences typed |
| The outline item from the owner's words registered | `cortex status neuron` shows C18 open with the owner's words quoted |
| The graph read by key as the ground for meanings, before any pull is balanced | `places_by_shard.py` on hp prints the 19 known points' shards, last shard, place and clock, and the offsets per kind with n, mean length and coherence; piped as the receipt of C18; one sentence in its words judged |
| The discussion, in the owner's frame, with the questions the design leaves open | the report |

Not in the contract: a pull row per shard, a context row per plain point, a formula typed into either brain, the C14 patches live, the hub door restarted. Those wait on the owner's word.
