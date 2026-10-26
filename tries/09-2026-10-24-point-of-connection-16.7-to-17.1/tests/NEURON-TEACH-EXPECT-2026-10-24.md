# Teaching run: define and place, typed at the prompt. Predictions frozen before the run (the builder's, not the owner's)
2026-10-24, turn 23. Results go in a separate file; this one is not changed.

## What is told (changes to the told block, in 17.1; the owner asked for the 3D place table)
1. A place table in the brain: place (id, word, x, y, z, t, ended). Its own trigger ends the word's old row when a new one is
   written (the old kept as history, the truth-shift rule) and writes one log row for the page (no action labels).
   The page's SQLite has no R*Tree module, so places are plain x, y, z columns. Native SQLite has R*Tree; an index can be added there.
2. A new source brain, "measured": step 2 and 3's measured numbers and lines, served through its mailbox like any source.
   One row per measured number: headword WORD:kind (rows, structure, text, read, test, number, gather, write), text "value . how".
   One row per measured line: headword WORD:kind (inverse, complement, ...), text "partner . how". Its rows carry no words, so they
   are never run as lines. The told source line asks it too.
3. The SQL docs source is rebuilt by one stated rule: the first two sentences on the word's own SQLite doc page that hold the word.

## What is taught (typed at the prompt; the brain writes each as a formula row pointing at its teaching run)
- define = SELECT text FROM definition WHERE word = :after AND src = 'sqldoc' ORDER BY id LIMIT 1 ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
- place = (an INSERT into place of the word after it, with x, y, z = 10 x its measured rows, structure, text; see TEACH lines)
Then, for each told SQL word in the told block's order: "define W", then "place W". Then three words that are not told and were
never taught: "define DROP", "place DROP", "define substr", "place substr", "define EXCEPT", "place EXCEPT".

## Predictions
P1. "define W" says W's first SQL doc line for the 41 words that have one. For INTO, <, >, <=, >= and the punctuation it says
    the line back with "?" marks (no doc line; the say gets nothing).
P2. "place W" writes one live place row whose x, y, z are 10 x W's measured rows, structure, text: INSERT 10,0,0; DELETE -10,0,0;
    CREATE 0,10,0; || 0,0,10; group_concat 0,0,10; every other told word 0,0,0. These equal the lab's own places with lines off.
P3. The words never told or taught, through the same two lines: DROP 0,-10,0; substr 0,0,-10; EXCEPT 0,0,0.
P4. No place row for any word that was not placed (no doc line holds "define", "place" or "source").
P5. Placing a word again keeps the old row (ended 1) and adds a new live row.
P6. Controls: (a) "place store" (no measured rows) gives 0,0,0; (b) with INSERT's measured rows taken out of the source,
    "place INSERT" gives 0,0,0. So the place comes from the measured source, not from anything else.
P7. Learning is slow: each "define W" line that sources a word with doc lines takes seconds (the doc lines run as lines and birth
    their words); "place W" after it is fast.

## What would stop me
- A place row the brain did not write from its own run (every place row must come from a formula run's statement through mother).
- A define answer that is not one of the source's lines.
