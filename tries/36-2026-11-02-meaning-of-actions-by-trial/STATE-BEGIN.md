# tries/36 (2026-11-02, 17:40): the state at the beginning of the turn, read live

The owner, 2026-11-02 about 17:30: "triads and larger should be laid if they are proven ... belief system should be starting to take shape,
based on actions to the silicon, actions to state and time memories, reactions to outcomes of correct and incorrect prior states and current
states ... it has to learn how to write a formula from its state ... no history of places??? is that not the run receipts in the time line?
... you are sourcing formulas from my map, not teaching the brain to build them ... instead you should be developing the process for the
brain to build them by asking the brain questions and just telling it correct or incorrect.. you have the answer, but you never tell it the
answer ... this brain should learn by trial and error, correction, process development to make a new laid process.... that starts now by
developing the correct meanings of the actions of the points when heard in different contexts or dna shards ... big turn give me the current
state at the beginning of the turn and the ending state so it can be diffed to show progress ... if the diff show degression you roll back".

Everything below is read from the running brains before anything of this turn was typed. The ending state is `STATE-END.md`; the diff is
`DIFF.md`.

## The kernel (hp, 10.31.1.106)

| What | Read |
|---|---|
| `/api/info` | defined 722,283; gates 1,317,441; runs 19,937,745; hops 33,909,779; refused 1; pending 0; shard_rows 137 main / 21 sixth; heap 32 MB |
| the points that act (DNA rows with a call or spawn, among the core and the keys) | heard, born, define, why, correct, incorrect, print, create, change, step: 10 points; the ok neuron 86 listener rows |
| `correct` (gate 419) | one row [1412, before heard, trigger `:`, call 773]: `UPDATE guess.guesses SET correct = correct + 1, solved = solved + 1, belief = min(1.0, belief + 0.25) WHERE asked_by = N`; used once (times 1) |
| `incorrect` (gate 423) | one row [1415, heard, `:`, call 789]: the same on the guess table, belief − 0.25; times 2 |
| `meaning` (gate 321) | no rows; `change meaning : X from A to B` exists under `change` (row 1809, trigger 321, call 1052) |
| `step` (gate 460) | one row [2031, heard, trigger `back` 453, call 1302]: walks a run's making back to the line that started it (mine, tries/28) |
| `why` (gate 417) | one row [1330, before the sixth, `:`, call 6281755]: the sixth's why; times 754,812 |
| `define` (156) | [557, heard, `:`, call 19937222 (the recall define)]; [1867, the sixth, `:`, call 19937222]; [1931, heard, `unknown` 155, call 1132] |
| the guessing brain's table `guess.guesses` | 14,420 rows; correct 0, incorrect 1 (summed over all rows); belief average 0.362, 6,721 rows at 0.5 or more; the newest rows are word-count guesses from before the cut (tries/31) |
| belief as the brain's own record | none: no table of the brain holds correct or incorrect marks on its runs or rows; `correct : N` and `incorrect : N` touch the guess table only |
| tried legs | none: nothing records which candidate was tried for a point and what came of it |
| the standing question's contexts by key | `hit WHERE gate = ? AND call IS NOT NULL`: define's newest hits [19937730, pos 1, before heard, next `:`, shard 557, call 19937222] and two more; print's and hinge's lists empty (the hits lists of the keys bound before the stored file hold nothing) |
| a key's action from its own rows | print: 5 rows, triggers dna 86, memory 426, node 47, sheet 427, table 410, calls 826, 847, 870, 889, 910; each call's text begins `BUILD INSERT OR REPLACE INTO run_sheet ...` |
| what a formula touches (its text's table symbols, read by key) | the recall define 19937222: run_sheet, run, seq, replay, rel, label, node, and the source wikt |
| the relationships of a point, strongest first, with whether the other acts | hinge: like of, to, in, be, with, point (pull 1.0), none of which has a function row |
| points related to the keys (rel.other = the key) | print: type, terms, published, mark, point, case, set, back, given, body, letter, found (all `like`); define: term, name, tag, title, mark, point, set, take, found, line, call, ground; create: head, do, author, form, make, get, set, work, better, think, found, turn; change: alternative, make, mark, go, put, don, back, better, run, turn, money |
| the formulas and places (tries/35) | formula 18, pull 38; xyz 722,333 placed, moved by landings; rel 4,024,000+ in 15 kinds |
| the tables of the main brain | label neuron dna node run seq run_sheet run_receipt run_memory timeline input third secondary out_user refused hit hop land clock shards complete replay rel relmap defwords xyz formula pull |
| a memory row (define : water, 19937719) | source heard, gate 1694 (water), shard 17, at 19937719, again 0 |
| a repeated line | `define : who` 19937383 same_as 19937236 (fired from memory); 19937686 (after SHAPE-2 rebound heard's row) ran its own receipts |

## The hub (8056)

| What | Read |
|---|---|
| `/api/info` | ready; routers main hops 894,076 / sixth 551,538; refused 0 / 0 |
| `correct` (233) | one row [894, heard, `:`, call 405], the same guess-table update; `incorrect` (237) [897, heard, `:`, call 421] |
| `meaning` (265) | no rows; `change meaning` under `change` (row 1319, trigger 265, call 702) |
| `guess.guesses` | 556 rows; correct 0, incorrect 1; belief average 0.337; 374 at 0.5 or more |
| belief, tried | none |
| define (153) | [587, heard, `:`, 4254380]; [18574, the sixth, `:`, 4254380, times 167,173]; [18664, heard, unknown, 11254] |
| formulas, places, relationships | formula 18, pull 38; xyz 71,546; rel 3,301,054 in 14 kinds |

## The Cortex on hp2 (read, not touched)

`/home/james/cortex`: the owner's Cortex front door (`cortex.py`, `CORTEX-HANDLER.md` of 2026-11-02, a copy of the kernel educated from hp's
line files as its store: 32,250 gates, 264,064 runs, socket 7007, page 8058, user services). Its handler carries the owner's words of
2026-11-02 on the guessing brain, the judge ("it doesn't decide the truth, it decides the confidence of the current state vs the prior
state"), "learning is more similar to a build time, and the then once learned the action more similar to a runtime", "a brain that has a
slow buildtime (learning) but deterministic runtime is the answer ... fill a cell of the rundata sheet ... once full data sheet other
deterministic substitution formulas can fire and complete the diff, contra, reasoning, drift, meaning checks", "new state is defined slowly
over time ... accept the parts that improve the state and reject the dupes, or degressions". Its law 7: hp's kernel and brain are never
touched by it.
