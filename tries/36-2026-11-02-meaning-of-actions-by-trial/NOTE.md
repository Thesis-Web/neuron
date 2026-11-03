# tries/36 (2026-11-02): the meanings of the actions of points, learned by trial and error at the prompt, both brains

The owner, 2026-11-02 about 17:30: "you are sourcing formulas from my map, not teaching the brain to build them ... instead you should be
developing the process for the brain to build them by asking the brain questions and just telling it correct or incorrect.. you have the
answer, but you never tell it the answer, you wait for it to come up with the answer itself ... this brain should learn by trial and error,
correction, process development to make a new laid process.... that starts now by developing the correct meanings of the actions of the
points when heard in different contexts or dna shards ... some points will act against the silicon, some the timeline, some knowledge,
some sources, some against other points, some memories ... the elements have be laid, now you have to learn how to use them such that you
can teach the brain how to use them ... big turn give me the current state at the beginning of the turn and the ending state so it can be
diffed to show progress ... if the diff show degression you roll back".

`STATE-BEGIN.md` is the state before anything was typed, `STATE-END.md` after, `DIFF.md` the diff. Everything is read from the running
brains. The build, said plainly before it was typed: a question the brain answers about a point from its own rows, relationships and
definition; a mark of correct or incorrect on the rows it named, in the brain; a guess adopted when correct, the next leg when incorrect.
Nothing of mine names which point does what.

## What was there, and what the prose asks

`correct : N` and `incorrect : N` existed on both brains since v6 (10-28) and touched only the guessing brain's table (a ±0.25 on a
guess's belief). No table of the brain held a mark on its own runs or rows, and nothing recorded a leg tried. The owner's words that
govern: 10-08 "a guess ... can turn into a belief ... that confirmation or lack there of builds confidense or not in the processes that
determined that answer"; 10-23 "in How did you do that memory there is be an incorrect notation by that memory row, and it should start the
brain on a process as to why"; 10-05 "if that unknow has relationships, then it becomes a guess after that, and it can continue stepping
forward based on relationships ... those must remained labeled guess"; 10-05 "if the simalar run unchanged produces the expected outcome
then no change and adobt that run if change happens register the new formula as the key to this run"; draft 5.6 "memory, then state, then
sources, then a guess"; 10-18 "can we tell it correct and incorrect? what happens after we tell it correct?"; 10-28 "belief never over 50% on
first use"; 11-02 (the Cortex handler) "it doesn't decide the truth, it decides the confidence of the current state vs the prior state".

## The process, as the brain's own lines (MEANING-nk.txt on hp; HUB-MEANING-v7.txt on the hub, hub_meaning.py)

1. Two tables of the brain: `belief (gate, shard, correct, incorrect, at, run)`, a mark per function row; `tried (gate, other, outcome, run,
   at)`, the legs tried for a point and what came of each.
2. The answer run. On the sheet of the line above it: `how` = memory when the point has rows with a call or spawn; relationship when a
   point related to it (both ways of `rel`, the kinds' pull deciding the order, the legs found wrong left out) has such rows; definition
   when it has a definition node and no action; none otherwise. `guess` = the related point whose action is borrowed. `action` = the rows
   (before, trigger, the run called) of the point, or of the borrowed point. `against` = the tables and sources the called runs' own texts
   name (what the action touches: the silicon's tables, the sources, the memory). `belief` = correct minus incorrect over the point's rows.
3. The question `meaning : X` writes what = X and calls the answer; `meaning`'s row (heard, `:`) calls it.
4. `correct : N`: for the answer N, when it answered from memory, correct + 1 on each of the point's rows; when it answered by relationship,
   the borrowed point's rows are laid on the point (the guess adopted, "register the new formula as the key"), the leg recorded right, and
   the marks laid on the new rows; the guess table as before.
5. `incorrect : N`: incorrect + 1 on the rows when it answered from memory; the leg recorded wrong when by relationship; then the brain
   asks itself again about the same point under this line (the tried leg left out) and the new answer lands on this line's sheet.

The candidates come from the relationship rows the sources laid (tries/34, 35) and the pull formula rows (tries/35); the rows adopted are
the brain's own rows; the marks are the brain's own rows. I typed questions and the words correct or incorrect, nothing else.

## Live on hp (17 to 124 ms a question)

- `meaning : print` → memory; `heard dna 826 ; heard memory 847 ; heard node 870 ; heard sheet 889 ; heard table 910`; against
  `run_sheet, run, seq, dna, input, run_memory, label, node`. `correct` → belief 5 rows at 1.
- `meaning : define` → memory; its three rows (heard `:`, the sixth `:`, heard unknown); against `run_sheet, run, seq, replay, rel, label,
  node, wikt, third`. `correct` → 3 rows at 1.
- `meaning : hinge` → definition, no action. `meaning : INSERT` → none; after `define : INSERT` (from the sources, one row) → definition.
- `meaning : type` → relationship, guess print (the thesaurus says type is like print), print's five actions. `correct` → the five rows
  laid on type, `tried (type, print, right)`; `type dna : define` then printed define's three rows; `meaning : type` again → memory,
  belief 5.
- `meaning : money` → relationship, guess change (money is like change in the thesaurus). `incorrect` → `tried (money, change, wrong)`,
  and the brain's next answer on that line: definition (no other related point acts).
- `meaning : alter` → guess create (the lower gate of two kinds of equal pull). `incorrect` → the next leg: change. `correct` → the five
  change rows laid on alter (trigger, call, spawn, define, meaning), belief 5.
- `meaning : describe` → guess define; `correct` → define's three rows on describe; `describe : hinge` answered hinge's definition
  (def = run 19933360, no source asked). `meaning : write` → guess print; `correct`.
- After all of it: `define : who` 0.015 s, `define : stone` 0.026 s, node rows unchanged; refused 1; shard_rows 139 → 167 (18 adopted
  rows, the define rows of the lines' new symbols, meaning's row); no pass row laid.

## Live on the hub (2 to 4 s a question, its router's batches)

The same lines in the hub's dialect (a point's rows are its own table, read and written through mother; `json_each` over mother's list for
the rows' shards; the shard counter bumped per row laid): print, define, hinge as on hp; type → print adopted, `type dna : define` printed
`587 | 1 | 68 | 4254380 | | 108; 18574 | 5 | 68 | 4254380 | | 168087; 18664 | 1 | 152 | 11254 | | 2`; money → change wrong, then
definition; alter → create wrong, then change, adopted; describe → define adopted, `describe : hinge` answered the hub's first definition
row of hinge (Wiktionary's "name 1: A surname."; the hub's def is the newest learning run's def as it was laid). belief 21 rows at 1;
`define : stone` after it all 3.1 s with no source asked; refused 0 / 0.

## The owner's correction on the history of places, recorded

11-02: "no history of places??? is that not the run reciepts in the time line? then examine those for the rundata sheets cells at that
state and time? that could then be stepped forward or backward from end output, or beginning input to determine any place in time for any
run, without holding a master table that needs a grep, sweep, query". So: the receipts are the history; `xyz` holds the place now and the
run and clock of the last move; a place at an earlier state is the receipts re-stepped, not a stored row. The tries/35 NOTE's "not done"
line is corrected to say that. Not built this turn: the re-stepping of places backward from the receipts.

## What I did that the owner should know

I answered correct and incorrect myself this turn (print, define, type, describe, write, alter as change: correct; money as change, alter as
create: incorrect). They are my judgements, each recorded with its run number in `tried` and `belief`, so a wrong one is reversed by typing
the opposite word on the same run. The teacher is the owner.

## Not done, and the owner's calls

- Triads and larger: not laid; "should be laid if they are proven" needs the proving process (a formula over three points answered correct) that this turn's two-point process could grow into.
- "it has to learn how to write a formula from its state ... recognize dependent and independent variables ... combined ... subtracted ... divided": not started; the answer run's `against` cell (what a formula touches) and the `action` rows are the state such a process would read.
- The sixth does not yet ask `meaning` questions itself, and nothing yet weighs belief by the quantity and quality of evidence (sources agreeing, prior states); the marks are counts.
- `against` names the tables a formula's own text touches, not the runs it replays (the ask under define is a replay; its sources show only where the define's own text names one).
- The guessing brain's table is untouched; its design stays the owner's (tries/31).
- The hub's `describe : hinge` gives the hub's first definition row (a surname) because the hub's def cell copies the learning run's def as laid; hp's gives WordNet's.

## Files

`STATE-BEGIN.md`, `STATE-END.md`, `DIFF.md`; `MEANING-nk.txt` and its ledger `LEDGER-MEANING-nk.md` (hp); `HUB-MEANING-v7.txt`,
`hub_meaning.py` (the hub); `ask.py` (the questions through hp's door); `hp-teach-state.txt`, `hp-state-end.txt`, `hub-state-end.txt`
(the reads).
