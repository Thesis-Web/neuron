# tries/53 (2026-11-04, 04:30 to 04:50 CST): the encoder keeps a word whole; the output is never cut; the cell parser named

The owner, 04:30 (quoted in STATE-BEGIN): the tiō split must be fixed now for other languages; the arrays are never cut and the cut should
have been lifted with the html work; the decode parser is invention; C26 accepted if truly completed; how and why are the sixth's questions
and meanings come first.

## Built (`~/nk-c27/`, a folder of its own, then the patches laid in `~/nk` with `.before-c27` copies)

- nk.c 112: `is_letter` = ASCII letters, `_`, and now any byte at or above 0x80. The three copies of the cut loop (cut2, val_set, cut_into)
  all call it, so a typed line, a value and a read all encode a word with any script's letters as one symbol. `_` stays a letter as it was
  (the kernel's own identifiers encode as one symbol; not asked for, left as found and named).
- nkio.c 121 (the output rows: `run N from mother: text`) and 211 (a say, def, reply or remember cell in a run read): the 160 and 300 limits
  gone. The run's own text fields in the run read keep their limits (400 the root, 120 the tree, 100 the back path): those are the lines'
  texts for the page's lists, not the output.
- Built with the same gcc line as run-on-hp.sh. Tested on port 7009 with a fresh egg in its own folder (never the live folder, 10-30's rule):
  abligurrītiō, tiō and h₂epó one gate each; a 454-character line's me cell read back whole. The test kernel: my first stop line killed the wrong process (pgrep -f matched the ssh shell, the tries/50 trap) and left it up; stopped at 04:52 by its exact pid 355497 (never `pkill -x nk`,
  which is the live kernel's name too).

## The restart, done on the owner's word at 05:03 ("you can do the restart")

`bash run-on-hp.sh up`: 6.1 s from stop to the door up; the brain back as it stopped (runs 19,939,022, defined 722,299, gates 1,317,489,
refused 1 before and after); then `define : spend` 0.207 s with its say read back whole (1,796 characters, no cut mark), and a typed line
with abligurrītiō, tiō and h₂epó born as one gate each. The owner's tab needs a reload. What follows from it is below.

## The owner's design for the hand-laid lines (05:00), C28 re-typed

"those build lines had to be that way and were that way on purpose so they would not be forgotten as the hand laid bastards... when that
word exists in the graph, insert, table, integer, etc, the hand laid neurons' dna tables and memories should merge with the correct neuron for
that word... the dna table of the real gate just adds the dna table of the hand laid, since the rows are numbered in sequence you don't even
have to change the dna shard numbers... the memory tables pointed to that shard follow." My 04:40 outline (retyping 56 lines) is withdrawn.
The first read (`hand-laid-twins-before-hp.txt`): of 43 uppercase SQL words of the build lines, 42 are gates with no definition row whose
lowercase twin is defined (SELECT 98 beside select 17434 with 200 rows; TABLE 31 beside table 410 with 488; INTEGER 35 beside integer 26685
with 63); INSERT 81 holds 19 rows itself. The egg's cells (me 19, above 20, what 23, say 25, know 26...) are already the same gate as the
word and hold definition rows: for them the chicken and the egg are one gate; what stays hand-laid there is the row-0 shards of heard, said,
mother, sixth, main, born and ok's 100 shards. The merge is the owner's design to lay; nothing merged.

## What follows from the restart

-  `bash run-on-hp.sh up` stops and builds and starts the kernel and the door (the tab is reloaded after). The brain is its stored
  file. What changes after it: a new text with non-ASCII letters encodes whole words as new gates (born, defined by the birth rule); the rows
  already laid keep their split symbols (ti 4923, ō 241 and the rest stay as gates); a recall of abligurition reads the held rows, so its suffix
  cell still says ti until the word is defined again from the sources. Whether to re-ask the sources for the words whose rows hold split
  symbols is a back population the owner decides.
- C28: the cell parser. nk.c `decode_span` (mine, v5 10-28, carried into the kernel) replaces a symbol that names a cell of the run, its parent
  or grandparent by that cell's value. The owner: a span should go out through the encoder's decode only, and read its own sheet by SQL; by
  the time the brain holds anything it is gates (the returns come in through the encoder as secondary input). The brain-native shape: mother
  knows the run it pastes for (`b->cur_run`); exposed as a one-row table like `clock`, a span reads `run_sheet` by (run, cell) for above 20,
  what 23, reply 22, newgate 21. The cost read on hp: about 56 of 110 taught BUILD lines use a hole word (LINES-nk 19 of 41, MEANING 4 of 8,
  TEACH-LINES 6 of 15, every RECALL, BORN and SHAPE line); each is retyped and rebound. The order against the meanings work is the owner's.

## Also

- C26 done on the owner's words of 04:30 ("then ok"); the ground is tries/52's receipts. C26.5 and C26.6 moved to C28 and C27.
- The owner's correction on how and why: they are the sixth's questions (why : run cell is already its line); C27 holds the encoder and the
  uncut output only.
- My tries/50 memory said the encoder folds case; it does not (Spent 34247, spent 6984; WHO 178, Who 191, who 120). Corrected.
