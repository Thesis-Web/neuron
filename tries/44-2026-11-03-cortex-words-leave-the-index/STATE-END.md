# STATE-END: the words leave the index (cortex C17), 2026-11-03 14:44 CST (raw: c17-close-reads.txt)

| read (live) | value |
|---|---|
| `cortex formula cortex` | 18 checkpoints, 18 done, 384 ingests, 14 verdicts, 20 parts; C17 working->done by receipt 0.741 (run 401652, 141 ms) |
| migration (`migrate-c17.py`, 0.65 s) | ingest 634, part 94, verdict 184, receipt 26, receipts 3 rows rewritten in place, ts kept |
| index bytes | total 1101934 -> 970773; ingest 91051 -> 7608, part 21996 -> 3881, verdict 154804 -> 130631 (the sheets stay), receipt text gone (1483 left: keys, cmd, ts) |
| the prints | `diff /tmp/c17-before.txt /tmp/c17-after.txt` empty: IDENTICAL, 16472 bytes each (hydrate audit --at 1, --at 2, hydrate cortex --at 16, verdicts audit, verdicts cortex, status audit) |
| the one part that changed meaning | probe C2 run 261541 now reads its run's true text "expected: met" instead of the synthetic judgment text the old judgment step had stored |
| C17's first sentence | hallucination 1.000 by receipt: it contained "--at 1" and the 1 was read as a value not in any receipt; reworded without the command argument, completes 0.741 by receipt |
| brain | gates 37342, runs 401666, hops 1093954, refused 0; load 0.12; mem used 615 MB |
| neuron | 15 checkpoints, 7 done; untouched |
