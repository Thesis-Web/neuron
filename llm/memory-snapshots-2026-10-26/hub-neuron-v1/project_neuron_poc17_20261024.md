---
name: project_neuron_poc17_20261024
description: Point Of Connection 17 (2026-10-24, turn 23) = 16.4 + a "measured" tab - bare core, SQL words added one at a time, placed only by numbers measured in SQLite; measured word-to-word line kinds (inverse, complement, negation, dual, completes/modifies/no change, same spelling); places held in a lab SQLite db beside the brain
metadata:
  type: project
---
Owner msgs 31-32 (verbatim in t23/turn16/OWNER-VERBATIM.txt inside Downloads NEURON-v17-SOURCES-2026-10-24.tar.gz, messages 1-32): msg 31 "what do you think as a lab partner is the correct choice?", msg 32 = grammar complements + pasted math terms (inverse, complement, opposite, dual, conjugate, orthogonal, reciprocal, identity, negation), "try these three on x,y,z", "if you concur proceed", "stay to the point, speak in deterministic state"). Msgs 31-32 are in OWNER-VERBATIM inside NEURON-v17-SOURCES-2026-10-24.tar.gz (t23/turn16).

Built and measured:
- x,y,z = rows (write/remove), structure (spawn/destroy), text (join/cut): the three undo pairs. Other views (one-ended): read, test, number, gather, write = steps a word adds over its line without it.
- 44 told points (AS, INTEGER, =, * split by measured job) + 10 not-told. Lines off: 39 of 44 at 0,0,0; INSERT +x, DELETE -x, CREATE +y, || and group_concat +z (predicted, held).
- Lines (rel.js, sql.js 3.39.3): inverse 5, complement 6 (missed <>/IS, !=/IS: IS = = without NULL), same program 1 (<>/!=), negation 8, negates 7, dual 1, completes 15, modifies 38, no change 5, same spelling 4; with a NULL row no complements. INTEGER in CAST is NOT required (CAST(b AS) accepted) - prediction wrong. FROM completes SELECT only via "no such column".
- Placement rule (lab17.js): share (default, pull 0.5): place = (1-pull) own + pull avg(tied); sum rule (tried first) collapsed everything (INSERT 10 -> 1.5) - added share after seeing it, both on the page, disclosed.
- Lab db: own SQLite DB in the worker beside the brain (point, effect, line, axis, added, place, view own); not attached (brain snapshots drop attachments). Page solves, writes place, reads back.
- Browser check: places from SQLite = node solve, max diff 0, in 7 cases; 16.4 parts work; no phone overflow; no errors.

Where: artifact https://claude.ai/artifact/9kwVUYnMFeMKa471BnvqiH; Downloads NEURON-POINT-OF-CONNECTION-v17-2026-10-24.html (sha 6845f747f928), NEURON-STEP3-EXPECT/RESULTS-2026-10-24.md, NEURON-v17-SOURCES-2026-10-24.tar.gz (t23/: make17.py rebuilds from the 16.4 sources tarball).

**How to apply:** next versions patch 17 (= 16.4 + tab). Next experiment steps: the brain's own physics measured at runtime (spawn via mother), then add one non-SQL word whose meaning is a run of told words (cut = SELECT then DELETE) and predict its place first. Related: [[project_neuron_step2_silicon_20261024]], [[feedback_known_failures_checklist]].

Found 10-24 (owner msg 33-34 "can they be taught not told?", "what is our plan to teach it????"): 16.4's "Meaning of a word, measured" (worker16.js ledger/meaningOf) counts the builder-written action labels in event rows as "silicon" (a memory recall adds hard-coded FIND COMPARE WRITE). Its graph part counts event kinds. So the brain has no honest instrument for what a taught word does to the silicon. Plan given: A instrument (real row/table/bytecode diffs; EXPLAIN is dropped by DECODE, which starts statements at SELECT/INSERT/UPDATE/DELETE/CREATE/WITH: a told change), C teach write/read/erase/update/copy/cut on the state table one at a time with predictions from parts, D modifiers via cells first (a taught word inside a statement is emitted as text, never fired), E place taught words by the same rule, F teach one "measure" method so the brain learns meanings itself. Open: who writes the formulas.
