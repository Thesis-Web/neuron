# 09. Point Of Connection 16.7, 16.8, 16.9, 17, 17.1 (2026-10-24)

**Status: superseded by 17.2 (`../10`).** "The brain did not change for four versions" (versions audit, row 11): 16.7 to 17 carry 16.4's told block byte for byte; the page adds pull layouts, then a lab SQLite db with JS-solved places. 17.1 adds a `place` table, a `place_written` trigger and a "measured" source stand-in whose numbers are the lab's (384 statements): the first brain-held positions, from a stand-in source.

**The owner's words.** 10-24: "it...with springs and shells and artificial pulls to fill gaps.. instead up building it correctly". 10-24 (messages 27 to 30): everything after 16.4 was off rail; start from the bare core; add one word at a time; the main pulls may be what words do to the silicon (the C behind CREATE, not the word); 16.4's page is the base, new tools in tabs "think of like how freecad works"; trust about zero ("sabotage until caught, then expand the complexity"). 10-24 (message 35): teach by prompts he can hand type; ground meanings in the SQL docs source; "sqlite is the crutch", log the long form for the future kernel; "ask me if unsure". 10-25: "so the sql words are hand laid and don't need a dictionary look up, but instead need a sql doc look up". 10-25 (messages 38 to 40): "no I can't trust to build it".

**What was measured** (`tests/`):
- `NEURON-STEP2-EXPECT/RESULTS-2026-10-24.md` + `NEURON-STEP2-SOURCES-2026-10-24.tar.gz`: what each told SQL word and physics trigger does to the silicon (EXPLAIN bytecode diffs, the SQLite authorizer), predictions frozen first. The silicon's opposite of `>` is `<=`, not `<`; INSERT/DELETE and CREATE/DROP are the opposites it shows; `+`/`-` are separate opcodes with nothing marking them opposite; the brain's clock was the count of log rows; the 14 actions were empty gates whose names existed only in log text.
- `NEURON-UNDO-TEST-EXPECT/RESULTS-2026-10-24.md`: exact undo (INSERT→DELETE, CREATE→DROP…), one-way only (DELETE→INSERT gives a new rowid), no undo (read/write); `=` and `<>` are complements, a second kind of opposite.
- `NEURON-STEP3-EXPECT/RESULTS-2026-10-24.md`: x,y,z = rows, structure, text (the three undo pairs); the measured line kinds.
- `NEURON-TEACH-EXPECT/RESULTS-2026-10-24.md`: 17.1's teaching sheet (88 lines typed at the prompt): define from the SQL docs source, place from the measured source; 43 place rows written by the brain; places came from our measured source, "the brain does not yet find meaning"; a seen line is answered from memory and writes nothing.
- The SQLite long form logged that day: `../../research/NEURON-KERNEL-LONG-FORM-2026-10-24.md`.

**Mistakes recorded** (checklist #53 to #66): a stand-in ("closeness to READ") presented as a measurement; scoring against the wrong target; a "can't" stated without a test (a table name can come from the typed line); 16.4's hand-laid block inherited and its rules called "the told rules"; EXPECT files written as predictions of my own code.

**Files.** The five pages; `NEURON-v17.1-TOLD-BLOCK-2026-10-24.sql`; the sources tars for 16.7, 16.8, 16.9, 17, 17.1 (each carries the owner's verbatim messages of the turn, growing from 1 to 35; `../../prose/from-sources-tars/` has them extracted); `tests/`.

**Dropped as duplicates:** " - Copy" files of the 17.1 page, the 17 and 17.1 tars, the 17.1 told block, the TEACH expect and results (all byte-identical).
