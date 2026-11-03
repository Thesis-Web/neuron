# DIFF: 14:40 -> 14:44 CST

| row | before | after | progress or degression |
|---|---|---|---|
| sentence text in the index | ingest, part, verdict, receipt rows carry it (268 KB) | none; every print replays the run's gates | progress |
| the prints the owner reads | | byte-identical before and after (16472 bytes) | no change, as required |
| index total | 1101934 | 970773 | progress |
| cortex | 17/17 | 18/18, C17 by receipt 0.741 | progress; the owner's `reject cortex 17 401652` undoes it |
| cost | | replay 1.1 ms per sentence, cached per process; migration 0.65 s once; load 0.12 | no degression |
| neuron | 7/15 | 7/15 | untouched |

No degression. Nothing rolled back.

## CONTRACT, balanced

| expected | SATISFIED by | REMAINDER |
|---|---|---|
| prints replay from gates, diff empty | IDENTICAL, 16472 bytes each | |
| rows without text, migrated in place | 634 + 94 + 184 + 26 + 3 rows; bytes as in STATE-END | |
| C17 closed | completes 0.741 by receipt, run 401652 | |
| | | checkpoint, expected, project rows and the formula snapshots still carry text (replayable the same way) |
| | | a digit inside a command argument in a sentence ("--at 1") is read as a value and fails the receipt; the judge cannot tell an argument from a measurement |
| | | the capture's receipts from a session's tool results; the per-hop ground (kernel); one sentence under many projects (kernel grammar) |
