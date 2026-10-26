# 01. Old v18 and v19 (2026-10-15 to 10-16)

**Status: superseded by v1 (`../03-...`), which kept its one right piece.**

**What it was** (versions audit, row 2). `bones.sql`: 4 tables (code, dna, receipt, memory) + 24 word rows; `physics.sql`: 5 temp tables + 5 triggers (listen, hop, end_of_run, hear_formula, formula_run). A neuron is a row of `code`; one shared `dna` table. One hand-laid recursive `hop` trigger for the whole brain. A typed line hops into `step`, is concatenated at end of run and handed to `mother(line)` when the run ends at `/build`. That built the TIMELINE, neuron and formula tables. An unknown word writes a `need` row and stops; a word is born only by the typed `new word X /build`. `kernel/mother.c`: 18 lines, exec, 'ok' or 'error'. Runs were typed by the builder's shell (`run_step.sh`); formulas by builder SQL.

**Scores:** one table per neuron: no (rows in shared tables). Run → mother: half (yes for typed lines; but the mother call sits inside the end_of_run trigger and the TIMELINE row and formula shortcuts are printf templates inside triggers). Mother exec-only: yes. Only hop and trigger hand-laid: half.

**The owner's words.** 10-15: "we have a single neuron yes, and it was hand laid, and the brain has learned nothing". 10-16, on the gate-arithmetic birth in `brain_copy.db`: "you are short cutting the run.. the neurons didn't excite to lay the chard, buil the nueron... the brain will not know how to build it's own neuron... it will know a Phase that builds a nueron". 10-19 21:55: "actually it was the most correct we ever had". The versions audit: "Its mother and its end-of-run paste were right. Its neurons were rows in shared tables, which is why v1 was built the next hour."

**v19.** Built by Claude in one turn on 10-15 "in the folder the owner gave it" (`v19copy/README.md`: plus, minus, times taught in long form; the brain lays the shortcut after a long run; study picks a formula among eight teacher-given shapes). The owner, 10-16 04:46: "you really wanted to just run away with it.. I gave you a chance and two turns in it failed with drift.. so we are back on 18, and honestly about to delete it and start over." v19 is drift, not a base. The session's own note at the time: "v19 was my drift and isn't the base... not to build on it or recommend it".

**What is in `v18-saved/`** (saved as one folder on 10-19 16:57; the numbered `v2` to `v6` inside it are the old v18's own iterations, not the October v1/v2/v3 line):

- `v2/`, `v3/`, `v4/`, `v5/`, `v6/`: bones.sql, physics.sql, skull.sql, brain.db, a kernel/ (v5, v6 add formulas.sql).
- `v18copy/`, `v18env/`, `final/`, `v18_before_formulas_20261016T090915Z/`, `v18_deleted_20261016T064420Z/`, and the snapshots `brain_v18_before_try_20261016T092157Z.db`, `brain_v18_before_newneuron_20261016T092919Z.db`, `brain_v18_before_step3.db`, `brain_v18_before_zero.db`, `brain_copy.db`, `q.db`.
- `v19copy/`: the v19 build (README, bones.sql, code/, teach/, kernel/, demo, say, look, grow, brains).
- `kern/`, `step1/`: SQLite's `eval.c` with one flag (SQLITE_DIRECTONLY) removed so a trigger can run a neuron's code, built to `eval.so`; test dbs.
- `own/`: `neuron.c` and its binary (an "own" program the brain was to run). `callout/`: `b.db`, `hand.sh`.
- `dl/`: the SQLite 3.37.2 amalgamation used to build the extensions.
- `run_step.sh`, `teach_one.sql`, `lastnum`, `n380`.

Moved out of this folder to `../../prose/`: his messages 343 to 362, `own.txt`, `other.txt` (to `prose/2026-10-15-to-16-old-v18-session/`) and the two sketches (to `prose/sketches/`).
