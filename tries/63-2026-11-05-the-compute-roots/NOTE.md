# tries/63 (2026-11-05, 15:2x CST): the compute roots, read and reported; nothing typed into a brain

## The six roots, what is physically done today (nk.c read; roots-read-live.txt)
| root | silicon | the kernel's C | in the brain |
|---|---|---|---|
| address | a location put on the address lines | a gate number; a shard's key; hmap_get hashes a key to a slot | the landing: the symbol's gate, before and after select the shard |
| read | load from memory to a register | cell_get, a shard's fields, the virtual tables' column reads | a landing reads its shard's call and spawn; a span's SELECT |
| write | store a register to memory | cell_set, shard_lay, dna_update | a span's INSERT or UPDATE through mother; a return filling its cell |
| test | compare, set a flag | if: is the shard there, is the run a repeat, is the gate born | the key match at a landing; a span's WHERE, CASE, EXISTS |
| advance | step the program counter or a pointer | the hop to the next non-space symbol; the stack's next step | the hop |
| fire | jump or call | hit pushes a call or spawn as a new run; a closing BUILD hands its span to mother | a shard's call or spawn |
The kernel's own find (hmap_get, nk.c line 17) is the owner's formula: address = the key's hash, read the slot, test the key, advance one slot if not. Copy = a call's replay of a run's line; bind = cell_set; join = a rel row.
As points on the live brain: none of the six holds an action of its own (write carries print's copied rows; join only the birth row); the sources give a computing sense for address (wn noun 1), read (wikt verb 12), write (wikt noun 2, verb 8) and join (databases), none for test, advance, fire.

## The boolean words on the live brain
0 and 1 are points (gates 58, 59) with no definition rows and no dna rows. not, and, or, false, true, on hold only the birth's define row; this, that, any, either, neither, nor, equal, both, no, yes, off, xor, nand, xnor hold none. The sources carry the logic senses: not (mathematics, logic), and (logic, 4 rows), or (logic, computer science), false and true (electronics: logic 0, logic 1), nor (Reinterpreted as not + or), nand (a binary operator composite of not and), xor (if either A or B, but not if both), xnor (blend of exclusive + NOR).

## The math, for the owner's first test (facts, not laid)
Two arithmetics hide behind the same marks. Boolean algebra (1 + 1 = 1): * and, + or, - and not (a but not b), / the residual of and, which is implication (if a then b), a root is a itself (a and a = a). Binary arithmetic mod 2 (1 + 1 = 0): * and, + xor, - xor, / only by 1, not a = 1 + a. NAND is functionally complete (not a = a nand a; a and b = (a nand b) nand (a nand b)); in CMOS silicon nand and nor are the single-stage gates and an and is a nand followed by a not. English: nor is neither (the brain's row: not + or); nand has no single common word, its plain form is not both.

## Sources found (not fetched)
Trench, On the Study of Words (1851), Project Gutenberg 6480; Skeat, An Etymological Dictionary of the English Language (1882, 1898), scans on archive.org; Pokorny, Indogermanisches etymologisches Wörterbuch (1959), online at indo-european.info and Academia Prisca, the base of DERBi PIE with Rix's verbs; Etymological Wordnet (de Melo 2013, mined from Wiktionary, TSV); MorphoLex-en (68,624 words, roots and affixes, GitHub); UniMorph English (inflection). Bréal's Semantics (1900) not found online in this search.

## The owner's question on physics (15:4x), answered by a test (the test brain, door 8059)
The kernel's C is 1,594 lines in the five files it is built from (nk.c 394, nkvt.c 356, nkio.c 440, nkmap.c 75, nkxyz.c 191, nk.h 138; mother.c 148 is not in the build). Its functions are instances: each does one thing to the brain's own tables. The general layer is under it (the processor's few instructions, memory, the operating system's file calls) and mother's route to SQLite, which runs any SQL the brain writes. Reading outside the database is not there: SELECT readfile('/etc/hostname') answered "no such function: readfile"; fsdir answered "no such table: fsdir"; load_extension is listed as a function, not tested. So the brain cannot read a book, a file or a folder by itself today; every book in it came in as a source database loaded by a program outside the brain.

## 2026-11-06 15:25: what this session read, nothing changed in either brain

- Gate 81 INSERT: the birth path does birth it (test brain run 19949444, newgate 81, mother "ok"), then my C28 merge rule at every span's closing (nk.c 256-262) merges it into insert 10441 again and sets it unborn (nk.c 383) before the run lands on it, so the landing is refused (12 refusals on the test brain, all from my tries/61 traces; live has 1 refusal ever, run 2 gate 87). The merge moved every row; the old runs hold the gate number 81 and never pass the encoder again; my do_relabel (nkio.c 137) re-read definition rows only, never a stored run.
- Live: 1,790,818 gates, 1,175,721 born, 722,306 with definition rows (born-count-live.txt); kinds in gate-kinds-live.txt, gate-glued-live.txt: 195,936 capital copies of a lowercase gate, 173,347 letters glued to a dash or curly quote (made before today's letter rule), 114,024 pronunciations.
- The boolean points on live (roots-points-live.txt): this, that, both, any, either, neither, equal, is, yes, no, off, unknown hold no rows; not, and, or, on hold only the birth row; true and false hold my tries/36 marking commands. Sources: contrary = nand, contradictory = xor, subcontrary = or (contrary-contradictory-sources.txt); the boolean glosses (boolean-glosses-sources.txt).
- Decisions in C that belong to the brain (mine): the merge rule, the dedupe, decode_span, the birth detour, the xyz move, the ok rows, the row laid by a full-key read, do_relabel. What only C does: hold, find by key, step, keep the firing order, hand text to the SQL prompt and return the answer as a run, the clock.
- The inside way for a stale address, untested: the refused table and a run's complete flag are readable from SQL, and a row's spawn runs after its call's run stalls.
- The owner, at the end: "I quit".
