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

## The owner's correction (22:05) and the compare, read, not laid

"why are we constraining to two sources??? it's not a race... tied? meaning they said the same thing, or the value of what they said is
the same thing, then we look to our meanings, which of the words returned actually have meanings in the graph... also relationships..
which words returned have defined relationships already... these would help in finding the mathematical formula for the meaning later".

The three measures as a keyed read over every source's rows of a point (`compare_pick.py`, `compare_pick2.py`, the prints beside): for
each row, of its letter symbols, how many another source's row also holds (agreement), how many are defined points (meanings), how many
hold relationship rows (relationships). What the read shows (`compare-pick-hp.txt`, `compare-pick-shares-hp.txt`):

- By the raw counts the longest rows win: what → a Singlish particle sense with 346 words (its examples), can → "a chamber pot" with 229,
  do → the head row with its derived terms, the → a usage note. Agreement in words grows with length; the function words every row
  shares (the, of, a) count as agreement, meanings and relationships alike.
- By the shares (each count over the row's words) the shortest rows win: why → Moby's "like from what cause" (4 words, 1.00 on all
  three), when → mwt's "like so long as", how and what → a quotation of Shakespeare's or Spenser's, who and the → a head row.
- Cost: 12 ms to 11.7 s a point (a has hundreds of rows; the self-join over the point's words is quadratic); a read, not a recall-time
  span as it stands; the long way at define time with the result kept would be its shortcut.

So a count of words is not "the same thing said": the rows the sources agree on in words are the long and the trivial ones. What stays
live is RECALL-8 (the dictionary's first definition row), a first leg, not the compare. The legs the owner's words leave to decide:
whether agreement is counted among the rows that define (gcide's [definition: rows, Wiktionary's and WordNet's sense rows) and not
the quotations, heads and like-lines; whether a word every row holds says anything; and whether the definition is per use (C21), the
run's context picking the sense.

## Also

- A test copy of the brain was started and stopped: the map file's real data is tens of GB (19 GB copied in four minutes); the fix
  was staged on the live kernel instead, the rule rows first, the pick as a read, then the binds, with the rollback line ready.
- Nothing on the page; the C14 patches unapplied; the hub untouched.
