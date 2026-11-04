# tries/51 (2026-11-03, 21:25 to 22:00): define with the dictionaries primary, live on the kernel

The owner, 21:20: "define : who needs to be fixed; on a define dictionaries are primary and the other secondary, but in a relationship
wordnet, moby, and other compare like indexes would be primary; how do I accept them; YES the graph is so much better this way"; and on
C13: no opinion, no change to the graph.

## What was wrong, read from the rows

`define : who` printed "noun 1: a United Nations agency..." because the ask (RECALL-7 part 1) sends the word to every source's inbox with
the definition cell 24, the first return to arrive fills the cell, and WordNet is the first source attached; on a recall the ask copied
that cell from the learning run. The 40 rows of who are all held (gcide 23, wn 2, wikt 16; `tries/50/who-node-rows-hp.txt`): gcide's
sense 1 is run 197, "Originally, an interrogative pronoun, later, a relative pronoun also".

## The fix, as the brain's own rows and lines (`RECALL-8-nk.txt`, typed through the door by `recall8_apply.py`, 0 refused)

- Part 0, the owner's rule as rows: `ranks (cell, source, rank)`: for the definition cell 24, gcide 8 and wikt 443 rank 1, wn 7, mwt 10,
  moby 11, map 12, sqldoc 13, measured 14 rank 2, the guesser 15 rank 3; for the relationship rows (the gate of `rel`, 126) wn, moby, mwt
  and map rank 1, gcide and wikt rank 2 (recorded; the rel span of part 2 already reads WordNet's and Wiktionary's markers and every
  source's like and opposite lines, so no span reads the rel ranks yet).
- Part 1, the ask (run 19938193): when the point has definition rows, the definition cell is the first row of the highest-ranked source
  that is a definition row: it holds the symbol `definition` (gcide's mark; gate 276) or its first symbol is not `[` (wikt's sense rows
  begin with the part of speech, its head rows with `[word:`); within that, the lowest run, the source's first row. A return's first
  symbol is its lowest pos (the returns do not start at pos 0; found on the first check). Else the sources are asked as before.
- Part 2, the define run (run 19938199): RECALL-7's with the same pick over the returns once they are in, before the relationship rows
  are laid, so a first define also takes the dictionary's definition.
- Part 3, the binds (runs 19938207, 19938213): define's two rows, (heard, :) shard 557 and (the sixth, :) shard 1867, call 19938199.
  The rollback is one line each: `UPDATE dna SET call = 19937222 WHERE gate = 156 AND before = 1 AND trigger = 68` (and before = 5).

## Live (the recall path, 11 runs and 2,435 hits a line, 33 to 287 ms)

| line | the definition cell now |
|---|---|
| define : who | run 197, gcide sense 1: "Originally, an interrogative pronoun, later, a relative pronoun also; -- used always substantively..." |
| define : how | run 18424, gcide's head row with sense 1 inline: "In what manner or way; by what means or process" |
| define : why | run 19031, gcide sense 1: "For what cause, reason, or purpose; on what account; wherefore" |
| define : what | run 15901, gcide sense 1: "As an interrogative pronoun, used in asking questions regarding either persons or things" |
| define : where | run 17960, gcide's first entry, Wher: "Whether. [Obs.]" |
| define : when | run 17176, gcide sense 1: "At what time; -- used interrogatively" |
| define : selfie (Wiktionary only) | run 4963979, wikt: "noun 1: A photographic self-portrait..." |
| define : zymurgy (Wiktionary only) | run 4753672, wikt: "noun 1: Synonym of zymology" |

## The next leg is the owner's: which dictionary leads (`pick-gcide-vs-wikt-hp.txt`, a read, nothing typed)

With the two dictionaries tied, the tie goes to the lowest run, GCIDE's rows (laid before Wiktionary's in a define). GCIDE lists its
homographs in the 1913 order, so for several function words its first entry is an obsolete or minor one: the → "See Thee [Obs.]", do →
the musical syllable, can → "an obs. form of began", where → "Whether [Obs.]", a → the letter. With Wiktionary ranked first every one of
the eighteen words gives its common sense first: the → "article 1: Used before a noun phrase", do → "verb 1: (auxiliary) A syntactic
marker", can → "verb 1: (auxiliary verb, defective) To know how to", where → "adv 1: (interrogative) In, at or to what place", who →
"pron 1: (interrogative) What person or people". One typed line changes the ranks rows (wikt 1, gcide 2); the span reads them.
Which entry of a dictionary is the definition for a use is C21 (a definition's uses as DNA shards), the owner's design.

## Also

- A test copy of the brain was started and stopped: the map file's real data is tens of GB (19 GB copied in four minutes); the fix
  was staged on the live kernel instead, the rule rows first, the pick as a read, then the binds, with the rollback line ready.
- Nothing on the page; the C14 patches unapplied; the hub untouched.
