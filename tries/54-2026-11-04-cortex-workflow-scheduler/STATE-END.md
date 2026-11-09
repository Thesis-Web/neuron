# STATE-END (cortex formula 06:16) and DIFF

## STATE-END
47 checkpoints, 46 done, 1298 ingests, 554 verdicts, 70 parts. Open: C28 (parts together cover 0.53; the three-source rule waits for sources that hold a claim's line). Remainder: C15.3 the marks (the owner). Brain: gates 137420, runs 2176353, hops 12592009. Hydration: cortex 10,863 bytes, neuron 11,864 (from 26,091 and 17,257 at 04:xx, carrying more of what matters). Captures: cortex 06:12 (2 sentences, 1 judged, 0 recorded only). hp2 commits: c81549e, 891cfb5, 1aab15d, 57393b3, 6b0247d.

## DIFF against STATE-BEGIN (05:55: 40 checkpoints, 39 done, 1283 ingests, 542 verdicts, 63 parts)
checkpoints +7 (C40 to C46), done +7, ingests +15, verdicts +12, parts +7. Every new checkpoint closed by its own verdict from piped receipts; no accept. No degression. The sample project: 0 to 5 checkpoints by `cortex plan`; the builds closed C1, C2, C4 (run 3), parked C3 and C5, both decided; run 4 (06:16): 2 turns in 53 s, C3 and C5 done by their verdicts, every checkpoint done, nothing unblocked; the sample formula 5 of 5 done, 93 ingests, 83 verdicts, 26 parts.

## CONTRACT
| checkpoint | satisfied by |
|---|---|
| C40 judging only candidates; no flooding | a hand capture: judged 2 of 5, 3 recorded; status prints judged and recorded; LAST MOVES only; questions --prune (completes 0.80 by receipt) |
| C41 the hydration gives enough | hydrate prints done checkpoints one line, the open one whole with named prints, parts, remainder, questions, needs, the receipts rule, the ending lines; 10,494 bytes (completes 0.85) |
| C42 the state history | cortex at prints the states and changes with their times (completes 1.00) |
| C43 plan from a repo | 5 checkpoints with expected prints from the sample README (completes 0.95) |
| C44 the build scheduler | run 3: 6 turns in 144 s, C1 C2 C4 closed by verdicts, a FLAW parked C5, the formula shows the moves (completes 0.72) |
| C45 hand-backs and decide | handbacks listed; decide 1 and 2 reject unparked C1 C2; the build continued (completes 0.80) |
| C46 sources | Rosenblatt 1958 in; Zadeh 1965 and Dempster 1967 refused, named (completes 0.89) |
Remainder: C28 (the three-source rule), C15.3 (the marks).

## What the blink taught, as rules now
The worker's whole context was the hydration (2 to 5 KB) and it built the tool. It could not close a checkpoint until it restated the expected in its own words with the observed values after piping the print; a paraphrase never closes. A backticked number is a value. A `$ command` segment's digits are arguments. A worker's NEEDED is carried until the liaison clears it, or workers echo it forever. The hydration must tell the next worker why the last turn did not close the checkpoint. A hand-back on no progress is usually a judge or hydration fault to read before deciding; a FLAW from a worker can be real (the plan's own grep needed -E).
