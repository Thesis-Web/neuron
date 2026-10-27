# What was checked, 2026-10-26 evening: like and opposite taught at the prompt
On the hub, through a second door (`serve18.py` of tries/15, port 8019) on a copy of tries/11's `brain18.db` loaded into memory;
the file was not written. Python 3.10.12, SQLite 3.37.2. Scripts: `tests/check-like-2026-10-26.py`, `tests/check-opposite-2026-10-26.py`.

Before: 61 secondary rows, 997 runs, 2,004 label rows, 3 formulas (born, source, define).

| typed | said | seconds | what happened |
|---|---|---|---|
| teach like (1,714 characters) | nothing (a teaching line) | 13.0 | 12 tokens born (LIKE, OVER, PARTITION, ROWS, BETWEEN, UNBOUNDED, PRECEDING, FOLLOWING, %, di, d, t); formula row 4: like, run 998; no BUILD error |
| like : -> like | nothing (a bind) | 0.0 | like's DNA table: shard 4748 (arrival heard, remainder space) with trigger like |
| like : store | shop , outlet , mart | 0.3 | one formula run under the line; no source asked (store's definition node already held 3 map rows) |
| like : go | move | 1.2 | the map asked once: 2 return runs (like move; opposite of stay); go's definition node: 2 map rows |
| like : store | shop , outlet , mart | 0.3 | no ask |
| like : dog | nothing | 0.2 | the map asked, it has no dog line; the say cell is empty and the line prints nothing (the T8 question of RESULTS-v18.md, still the owner's) |
| teach opposite (1,726 characters) | nothing | 1.3 | every token had a gate after like's line; formula row 5: opposite, run 1022 |
| opposite : -> opposite | nothing | 0.0 | the bind row in opposite's DNA table |
| opposite : go | stay | 0.3 | no ask |
| opposite : can | cannot | 71.3 | can had no gate: the formula's born step bore it, and born_go asks every source for a word a line brought (as define's does): 17 return runs, 60 words born, can's definition node 17 rows best first (gcide 3.56, wn 3.36, ...; 3 from the map) |
| like : can | canister , crapper | 0.2 | no ask |
| like : is | am , are | 1.3 | the map asked once |
| opposite : store | nothing | 0.3 | the map has no "opposite of" line for store |

After: 82 secondary rows, 1,113 runs, 2,152 label rows, 5 formulas. No BUILD cell of any run under these lines holds an error.

## What is mine in the two lines, labelled
- They ask the map alone, and only when the word's definition node has no row from the map (define asks all eight sources, and only when the node is empty).
- The map's return runs are recorded in the definition node with score 0, where source records every return with its score.
- The say cell takes the map's lines that start with "like " (or "opposite of "), drops that head, and joins the rest with " , " in the order of the definition node's rows.
- When no such line exists nothing is said. What should be said is the owner's call (RESULTS-v18.md T8).
- The lines were written in the shape of the define line of sheet18.json and in v18's token grammar (a space around every punctuation mark), and tested as above. They are not derived from any rule of the owner's beyond "everything else is typed as runs" (CHANGE-OF-STATE, 10-25).

## Not checked
- These lines typed into the owner's own running brain (port 8018), or saved into any file.
- What the page draws for them beyond its lists (formulas, lines typed, runs): not looked at.
- A word the map holds under a different case (the sources match word COLLATE NOCASE; the label table does not).
