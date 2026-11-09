---
name: temporal
description: "The owner's input output formula for a Neuron turn: the state at the beginning, the state at the end, the measured progression as a diff, and the output contract with each part satisfied or left as remainder; the next turn's before is this turn's after. Use when the owner types /temporal or says input output formula."
---

# /temporal: the input output formula

The owner, 2026-11-02: "input output formula = before/after + progression = diff output + before and after states + progression = expected completed output contract satisfying completed parts and remainder parts left not satisfied. I mean the start of the state, finish of state, measured progression." And: "if the diff show degression you roll back and start over until you show progress grounded in the prose."

Every Neuron turn that builds anything runs this, in this order. The records go in the turn's folder `/mnt/d/Neuron/tries/NN-YYYY-MM-DD-name/`.

## 1. BEFORE: STATE-BEGIN.md, read live before anything is typed

- The before is the last turn's STATE-END, read again where it matters, plus what the owner saw and said (quoted, with the time).
- A table of reads from the running brains, not from notes: hub `/api/info` and `/api/prof`, hp `/api/info`, the rows the turn will touch (counts, the newest run, the trigger text as it stands), the pages as they answer now.
- The Cortex's before: `ssh hp2 ~/.local/bin/cortex formula neuron` (its BEFORE is the last formula's AFTER).

## 2. OUTPUT-CONTRACT.md, before the build

Three lists: what works and must not change (with the live read that proves it now), what is wrong by the newest prose (the owner's words, dated), the new work with its expected live output. Register the new work with the Cortex so it can check for drift:

```
ssh hp2 ~/.local/bin/cortex checkpoint neuron N : <what is built> '||' <the live output that proves it>
ssh hp2 ~/.local/bin/cortex state neuron N working
```

## 3. Build, one piece at a time, each used before the next

Live output only. Read every mother reply. A test never shares a folder with a running brain. A statement that runs longer than a minute is a fault to trace, not to wait on.

## 4. AFTER: STATE-END.md, read live after

The same table as STATE-BEGIN, re-read. Then ingest the sentences that state the live output:

```
ssh hp2 ~/.local/bin/cortex ingest neuron <one sentence of observed output>
ssh hp2 ~/.local/bin/cortex accept neuron N <run>      # the owner's word only: the sentence is a part of C N's state
ssh hp2 ~/.local/bin/cortex formula neuron
```

## 5. DIFF.md: the measured progression

Row by row, STATE-BEGIN against STATE-END: what moved, what was added, and for each row whether it is progress or degression. A degression is rolled back and the turn starts over from the before; it is never written up as progress.

## 6. The contract, balanced

A table: each expected output of OUTPUT-CONTRACT, SATISFIED with the live part that satisfied it (the run, the row, the read), or REMAINDER with what is missing. Nothing is called done without its live part. The remainder is the next turn's first work unless it is gated on something not mine (then say what).

## 7. The report to the owner, in this shape

STATE-BEGIN, STATE-END, the DIFF, the contract with satisfied and remainder. Short. The next turn's before is this turn's after.
