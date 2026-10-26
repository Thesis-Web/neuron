# Neuron turn one (hp2): report

Born 2026-10-19 01:14:33. Told ended 02:27:58; from then on the kernel refuses every lay file, and nobody has edited the kernel, the lay files or the brain. It runs as `neuron.service` (user `neuron`). Talk to it with `ssh hp2 -t neuron talk`; watch it with `neuron watch`. Its rows are in `/home/neuron/brain.db`.

Read alongside: `DECISIONS.md` (88 decisions), `ADVERSARY-FINDINGS.md` (37 findings, with a status table at the end), `TOLD-PROCESSES.md`, `KERNEL-SPEC.md`.

## What it is, as built

- **The kernel** (`kernel/*.go`, Go plus the SQLite driver only) holds the brain in RAM and commits to `brain.db` at the end of each beat; a beat that changes nothing writes nothing. It steps runs gate to gate: the shard holds the way, and a miss goes to the miss process, which is neuron code. It performs the 20 physics words of blueprint §4.3, beats the heart, and opens the ports (talk, watch, control, CALL). It loads lay files until told ends, and it refuses every write to a core-value gate.
- **The told base** (`lay/`, 11 files) holds:
  - roots, the keys, and zero, one and two;
  - 12 relationship types with first-guess formulas;
  - the 65 primes: 45 with actions, 20 laid as gaps that list themselves;
  - the core values, as actions the kernel enforces before every SAY, CALL and process write;
  - 747 process strings (5,170 gates): miss, end-of-run with compile, the questions, balance, belief, guessing, 21 sources with check-and-diff, memory, the timeline, the HC, the five ways of learning, back-population, the sixth, and sleep.

## What works, with the rows that show it (live brain, 02:27)

| Day-one ability (§19) | What its rows show |
|---|---|
| Learns, writes processes nobody told it to make | One: `proc 1091 = [one ADD]`, made DERIVED, found by generalize from its own `0 + 1 =` and `three + 1 =` runs, tested on a run it wasn't built from (receipts in its `sec-derived`). |
| Keeps a state timeline | 4,780 timeline rows. "what did you do now ?" is answered from the timeline, newest first (`when-did`, an index seek). |
| Builds and organizes neurons | 414 gates spawned. 307 sit off zero: a newborn is placed by the line it arrived on, and points move as relationships pull them (`move` acts in acts.log). 206 imbalances listed. |
| Has memories | Same input = same row with a new time (`1 + 1 =` seen 204 times). The second identical input is a hop: no long way (rule 2). 4 truth-shift rows. |
| Relates meanings | 301 relationship lines from sources (WordNet relations, definitions), marked SOURCED/GROUNDED; ungrounded sources write GUESS. |
| Checks a source and diffs it | 910 source calls. Outcomes are marked on the gate checked: `sec-agreed` 2, `sec-added` 17. Trust rows are kept per source and topic. |
| Senses balance | Verdicts compiled on the pad: "is hot cold ?" gives no; "hot is not cold ?" gives yes (from the WordNet line hot opposite cold). Imbalances go on the sixth's list. |

Other behaviours that held under the adversary:
- **Its own choices:**
  - The sixth chooses its own inputs from its lists when idle.
  - Idle beats with nothing due write nothing.
  - Sleep changes nothing held true.
- **People don't make facts:**
  - A person's "no" isn't taken as fact: it recomputes and keeps what it computed.
  - A name that clashes with a value it holds is refused.
  - Typing "move" can't rearrange the graph.
  - A person can't walk it out to an ungrounded port (do no harm asks who started the run).
- **Robustness:**
  - Floods of 1,000 repeats or 250 nonsense words caused no fault.
  - The whole log has no faults.

## What doesn't work

- **Learning is thin.**
  - **One kept formula, never used again:** it found one formula (#1091) and has never run it since. Nothing leads to it (adversary 29), so "apply it to itself" isn't shown.
  - **No refits:** fit, deduce, derive and the shortcut way have run on its own rows without keeping anything new. No type formula was refit by the brain.
- **Belief has never run** in the live brain. The contradiction path was exercised only on dev brains.
- **The HC hasn't condensed anything.** No memory is a day old yet; on a dev brain it condensed only when its age mark was lowered.
- **Senses merge by spelling.** "figure" the number and "figure" of figure/ground share a gate (adversary 4). The source templates take the first sense and the first few words (adversary 13), so the brain can't see the other senses.
- **Guessing is rare and weak.** A guess comes only from a similar shape or a neighbour that a meaning line put there; a word nothing is known about gets asked about, not guessed (adversaries 9, 17).
- **The ask is fixed.** "<gate> what ?" comes out the same every time: the same act, but the word order is laid, not picked (adversary 23).
- **Sources:**
  - 21 of the owner's ~60 sources are connected (adversary 14).
  - It can't connect a new source, or write and run a program of its own, now that told has ended (adversary 34). Its self-writing is process strings (WRITE PROC).
- **Leftovers from the adversary's probes and early bugs stay in the brain** (there are no hand edits):
  - "hot" was named to the value-6 gate, and the value-8 gate is labeled "three";
  - "side" sits on "inside"'s point;
  - the key-end gate was moved;
  - the 1/0 = zero memory is still there;
  - 112 early newborns sit on zero's point;
  - zero-strength "asked" lines remain;
  - about 370 nonsense words sit on the sixth's lists.
- **Minor:** one "no" can still mark memories wrong that didn't rely on the corrected answer (adversary 11). A truth shift can write a row with NONE as its outcome (adversary 36).

## Kernel size

2,592 lines (2,338 without blanks and comments). That is past the guide's 2,000-line mark.
- **What moved out:** three choices that had leaked into Go are now lay strings the brain can rewrite: the sixth's due rule, the trust weight, and the truth-shift comparison.
- **What remains:**
  - storage for 21 tables, with load and per-beat commit;
  - the step and the 20 physics words, with their selectors (READ/WRITE/FIND reach about 70 kinds of row);
  - the ports, including peer-credential *who* and CALL;
  - the lay loader with its static walk.
- **Policy still in Go**, which the adversary names as leaks:
  - the watchdog and parking;
  - same-row-or-new-row for memories;
  - TODO de-duplication;
  - COMPARE's hole mask on lists.

## Told processes

747 processes, 5,170 gates (`TOLD-PROCESSES.md`, per file with sizes). The largest files are primes (45 actions plus 20 gap processes), questions, and learning. Most processes are 3–10 gates; the longest is about 30.

## Adversary

37 findings. 16 still reproduce, among them majors 1, 4, 7, 8, 9, 13, 14, 16, 17, 23, 29, 33, 34 and 37 (8, 16, 17, 25, 35 and 37 got a further fix after its last check, before told ended). The rest are fixed or partly fixed; the status table at the end of `ADVERSARY-FINDINGS.md` has each one.

The adversary broke one rule: it ran `neuron ctl status` once (read-only).

## How the turn ran

- **The lead** wrote the kernel and the core lay files.
- **Six builders** each laid one area: primes, questions, sources, memory, learning, and the sixth.
- **One adversary** attacked the live brain from birth for 70 minutes. Its findings were fixed in the brain, never by handling a probe.
- **Restarts:** the live brain was restarted about 10 times during the told window for kernel fixes. Each restart left a RESUMED memory on its timeline.
- **The owner's update of 10-19:**
  - the Merriam-Webster keys were installed for the `neuron` user;
  - 5 more sources were connected;
  - QKV is allowed but not laid; the guess stays simple math.
