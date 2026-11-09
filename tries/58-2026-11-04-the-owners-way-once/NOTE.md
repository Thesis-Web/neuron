# tries/58 (2026-11-04, 17:4x to 19:07 CST CST): the told block, the owner's way, once, on a test brain

The owner's words are in OWNER-WORDS.md and the roots table in ROOTS-GIVEN-AGAIN.md. Nothing of this touched the live kernel or the hub.

## What was built, and where
A test brain in its own folder on hp (`~/nk-roots`): the live kernel's binary, a sparse copy of the stored brain (24 G real, 262 s), its own
copy of the nine sources, the kernel on port 7009 and a door on 8059 (setup.sh, setup.log). The counts after the copy equal the live brain's.

ROOTS-nk.txt (roots_gen.py writes it; roots_apply.py types it through the door and reads every mother reply): 65 BUILD lines, 34,906 bytes.
- Line 1: two tables the memory and timeline roots write (stored, history; the clock column named at_clock so no preposition stands in a span).
- Line 2: `after`, the inspection of the line (the owner, 10-28: the inspection run reads the input row, the symbols after this gate): a called
  run knows its caller from physics (run.from_run, run.from_ord, the line's receipts); it reads the words after the root onto the root run's
  sheet: cell 23 = the first word after the use noun; of, to, at, by = the word after each preposition; the word `it` = the line's cell 23.
- Lines 3 to 23: the 21 roots, the owner's definition quoted on each; one span that calls `after`, one span that does the one physical thing,
  written with those words bare (the kernel's cell parser decodes a cell's name in a span to its value); the result in the line's cell 23.
- The binds: each root at (heard, noun) and at (and, noun): two uses, so a root after `and` in a sentence acts too.

## What the test brain answered (roots-apply-3-hp.txt)
21 of 21 roots act from a typed sentence of plain words; three composed sentences act through `it`:
`find word scan and select dna it` lands scan's dna rows in the line's cell 23; `measure run N and compare value it to 4` gives 0;
`read cell 25 of N and write value it to 4921 of M` writes M's cell. A sentence with one root costs about 4,600 hits, with two about 8,950:
the long form; the inspection run's span is most of it.

## Found on the way, the trap at work
- The cascade merge rule of this morning (nk.c, C) folded FROM, AS, WITH, SET, SELECT, INSERT, UPDATE, DELETE, JOIN into their lowercase
  twins. The cell parser decode_span (nk.c, C) replaces any symbol naming a cell of the run, its parent or grandparent. Together: once a
  preposition `from` or `as` is a cell, every SQL FROM and AS in a span decodes to its value (the first prints: "near 1", "near wn").
  Routed around here by prepositions that are not SQL words (of, to, at, by) and by one result cell; the parser itself stays the C piece
  that needs the owner's word (C28's retirement outlined 11-04 04:30).
- A table column named like a preposition (at) decodes the same way: renamed at_clock.
- My generator replaced tokens inside REPLACE and ORDER on the first pass: fixed, the second pass is the record.

## Mine, for the owner to strike (said plainly)
The noun after the root keys the use (cell, word, value, point, run, dna, shard, link, key, line); the prepositions of, to, at, by carry the
operands; the result of a root is the line's cell 23 and `it` reads it; the example sentences. Compare orders text ('seven' > 'nine' = 1).

## Remainder, the owner's
Part 1, the experiment: scan from examples of the roots alone, not authored (nothing typed for it). Part 3, the shortcut by back population
with hop counts side by side. Part 4, the C rule out. Whether the told block goes on the live kernel. The cell parser.
