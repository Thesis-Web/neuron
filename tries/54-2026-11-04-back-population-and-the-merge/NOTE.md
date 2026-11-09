# tries/54 (2026-11-04, 05:00 to 06:45 CST): the back population of the splits and the merge of the hand-laid symbols

The owner, 05:00: "merge is not mine to lay... I instruct you to lay them"; "yes to the back population of splits"; "maybe track it down".

## The say difference, tracked down
The two say runs of spend differ in the etymology array alone (64 items before the restart, 56 after; gone: h, p, ndeti, bor, n, spent, provide,
dedicate). nk.c `nk_seq`: a return's symbols are not held; they are re-cut from the source row at every read with `cut_into`, which only looks
symbols up (`label_gate`). After the encoder change the fragments h, p, ndeti were no longer cut, and the whole words h₁éǵʰ, péndeti had never
been born, so they read as gate 0 and the label join dropped them. `why : 19939023 25` at the prompt filled the standing cells only (why is the
sixth's question about a cell). So the back population is not a rewrite of seqs: it is giving every symbol of every held row a gate.

## Built
- `relabel`, a kernel pass (nkio.c `do_relabel`, nk.c `nk_learn_text`): every point with node rows, every row's source text re-read and cut
  with `label_new`. Run once on the live kernel: 471,396 symbols born, about six minutes in disk wait (the source files read by rowid); the door
  blocked meanwhile and the request's socket timed out, so the pass's own print was lost. Lesson: a pass that long needs its print kept by the
  kernel (nk.log) and the door told, as the owner's rules on passes say.
- The letter rule, second form: the first form made every non-ASCII byte a letter and glued “quotes” to words (spend”). `letter_len` keeps the
  letters of other scripts and ends a word at their punctuation. Built and tested on 7009; live at the next restart, with a second `relabel`.
- `nk_merge(h, t)` (nk.c) and mother's `merge(h, t)` (nkio.c): the hand-laid gate's shards (ids kept), node rows, memories, about, hits and
  arrived lists into the twin; the hand-laid neuron born 0; the symbol names the twin in the encoder; the old gate keeps its text so the lines
  already laid still read. Typed as one BUILD line over the 58 uppercase SQL words of the taught lines (MERGE-nk.txt, then MERGE-2-nk.txt for
  INSERT, DROP, DELETE whose documentation rows moved with them). After it a new BUILD line encodes select, count, from (lowercase gates) and
  runs.

## What is mine, labelled
The pass and the merge are kernel physics (C), invoked by the brain's lines; the list of hand-laid words is read from the taught lines; the
exclusion of BUILD (the kernel's span mark, gate 29) and ME (a cell). Not laid: a cascade rule that merges an uppercase twin at define time;
which symbols count as hand-laid is the open leg (WHO 178 is a defined acronym's gate with no rows of its own; a rule by case alone would fold it).

## Remainder
The third restart (the letter rule) and the second pass; the owner's word on the cascade merge rule.
