# Commands results: learn, define, run, test, build, find meaning, print run, run backpop (2026-10-25)
Predictions frozen at 01:37 before any run: NEURON-COMMANDS-EXPECT-2026-10-25.md (sha256 7608171ab907...); learn : X predictions written at 01:07: NEURON-LEARN-EXPECT-2026-10-25.md (5fa24157dcdc...).
Run in node on the page's real brain code (worker16.js, host15.js, sql.js 3.39.3): run 1 as built, run 2 after two fixes. Then typed through the page 17.2 prompt in a real browser.

## The 17.2 told block (5 changes over 17.1; every change is in TOLD-BLOCK-17.2.sql)
1. A returned definition runs as a line headed by modifier gates: "return from <the asking line> from <source> /build <definition>".
2. Its end writes the word's definition memory ("definition from <source>") and a cell "<source> <word>" = that memory's id in the asking run's data sheet.
3. A run of kind test is its own root, runs the long way, and its end writes ":test" = balanced / shift / no memory into the asking run's sheet.
4. The source gates are neurons (table, view, miss trigger). Found in testing: the header put a source's gate in the run, and the sources were names only ("no such table: land_79"); every line failed until this.
5. Inside a returned answer's run, a row's trigger column does not fire (returned information is not a command). Added after run 1, where print: and meaning: fired 8 times each inside returns.

## Run 1 and run 2 (node), command lines

| Line | Predicted | Run 1 said | Run 2 said |
|---|---|---|---|
| `learn : store` | 8 | 8 | 8 |
| `print run :` | the path and the data sheet | path learn : store sheet wn learn=11;gcide learn=12;mw learn=13;mw lea | path learn : store sheet wn learn=11;gcide learn=12;mw learn=13;mw lea |
| `define : store` | WordNet's first sense | a mercantile establishment for the retail sale of goods or services he | a mercantile establishment for the retail sale of goods or services he |
| `build : store` | 16 | None | 16 |
| `find meaning : store` | store place none definitions 16 formula none | store place none definitions 16 formula none | store place none definitions 16 formula none |
| `learn : dog` | count (<= 8) | 8 | 8 |
| `define : dog` | WordNet's first sense | a member of the genus canis that has been domesticated by man since pr | a member of the genus canis that has been domesticated by man since pr |
| `learn : INSERT` | 2 | 5 | 5 |
| `learn : DELETE` | 2 | 2 | 2 |
| `run backpop` | 2 (INSERT, DELETE placed) | 2 | 2 |
| `find meaning : INSERT` | INSERT place 10,0,0 definitions 2 formula none | INSERT place 10.0,0.0,0.0 definitions 5 formula none | INSERT place 10.0,0.0,0.0 definitions 5 formula none |
| `test : define : store` | balanced: (the definition) | balanced: a mercantile establishment for the retail sale of goods or s | balanced: a mercantile establishment for the retail sale of goods or s |
| `run : define : store` | the definition (from memory) | run? : define? : store? | run? : define? : store? (memory) |
| `learn : zork` | 0 | 0 | 0 |

### Against the predictions
- Held: learn : store (8), print run :, define : store, find meaning : store, learn : dog (8), define : dog, learn : DELETE (2), run backpop (2 places: INSERT 10,0,0 and DELETE -10,0,0), find meaning : INSERT (place 10,0,0), test : define : store (balanced), learn : zork (0).
- build : store: run 1 said nothing; it had computed 16 but the line stopped after the formula. Cause: the formula fires in the middle of the line's hop and spawns return runs whose header ("return from build : store") laid the DNA row the line needed next; a trigger laid mid-run fires only for a later statement (the reference's Appendix B, fact 4), so the line found the row and could not see its hop trigger. Fixed in build:'s taught line (its header leaves out the ":"); run 2 said 16.
- learn : INSERT said 5, not 2: your relation map source holds 3 rows for INSERT. My prediction missed that source.
- run : define : store said "run? : define? : store?", not the definition: the sub-line was answered from memory, but its answer does not carry up to the line that asked. Open: should a sub-line's answer be the asking line's answer?
- L5 (no command fires inside a returned answer): failed in run 1 (print: 8, meaning: 8: a three-word key matches its own row inside the header that copies the asking line); held in run 2 after change 5. The told source formula still fired once inside a return, because a definition contained the word "source" (16.4's rule: a word's own formula fires in definition rows). Yours to decide.
- Not predicted: the command words themselves (learn, define, run, test, meaning, print) were looked up in the dictionaries the first time they were typed, as the told rule does for every new word in a typed line; each now holds 8 English definition memories.

## In the page (real browser, typed through the prompt)

| Line | Seconds | The brain said |
|---|---|---|
| `learn : store` | 53.5 | 8 |
| `define : store` | 21.6 | a mercantile establishment for the retail sale of goods or services he bought it |
| `find meaning : store` | 35.8 | store place none definitions 8 formula none |
| `learn : INSERT` | 20 | 5 |
| `run backpop` | 50.3 | 1 |

The 9 formulas and 9 binds were typed the same way (3 to 35 s each). Places in the brain's own place table: INSERT 10,0,0 (only INSERT held measured rows in this pass); the stage drew it from that table.

## The taught lines (the teaching sheet; what each command does is the builder's reading of the owner's names)
```
learn: = INSERT INTO var ( run , name , value ) VALUES ( :run , ':x' , trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) ) ; INSERT INTO source ( word , run ) SELECT :x , :run WHERE NOT EXISTS ( SELECT 1 FROM definition WHERE word = :x AND src <> 'node' ) ; SELECT count ( * ) FROM memory WHERE mark LIKE 'definition%' AND run IN ( SELECT id FROM run WHERE kind = 'defrow' AND subject = :x ) ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
define: = INSERT INTO var ( run , name , value ) VALUES ( :run , ':x' , trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) ) ; SELECT substr ( line , instr ( line , '/build' ) + 7 ) FROM memory WHERE mark LIKE 'definition%' AND run IN ( SELECT id FROM run WHERE kind = 'defrow' AND subject = :x ) ORDER BY id LIMIT 1 ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
run: = INSERT INTO input ( line , direction , parent , kind ) SELECT trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) , 'heard' , :run , 'line' WHERE trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) <> '' ;
test: = INSERT INTO input ( line , direction , parent , kind ) SELECT trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) , 'heard' , :run , 'test' WHERE trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) <> '' ; SELECT value FROM var WHERE run = :run AND name = ':test' ORDER BY id DESC LIMIT 1 ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
build: = INSERT INTO var ( run , name , value ) VALUES ( :run , ':x' , trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) ) ; INSERT INTO input ( line , direction , parent , kind , subject , word ) SELECT 'return' || char ( 32 ) || 'from' || char ( 32 ) || 'build' || char ( 32 ) || d.word || char ( 32 ) || 'from' || char ( 32 ) || d.src || char ( 32 ) || '/build' || char ( 32 ) || d.words , d.word , :run , 'defrow' , d.word , 'build:' FROM definition d WHERE d.word = :x AND d.src <> 'node' AND trim ( coalesce ( d.words , '' ) ) <> '' AND NOT EXISTS ( SELECT 1 FROM run r WHERE r.kind = 'defrow' AND r.subject = d.word AND substr ( r.line , instr ( r.line , '/build' ) + 7 ) = d.words ) LIMIT 8 ; SELECT count ( * ) FROM memory WHERE mark LIKE 'definition%' AND run IN ( SELECT id FROM run WHERE kind = 'defrow' AND subject = :x ) ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
meaning: = INSERT INTO var ( run , name , value ) VALUES ( :run , ':x' , trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) ) ; SELECT :x || char ( 32 ) || 'place' || char ( 32 ) || coalesce ( ( SELECT x || ',' || y || ',' || z FROM place WHERE word = :x AND ended = 0 ORDER BY id DESC LIMIT 1 ) , 'none' ) || char ( 32 ) || 'definitions' || char ( 32 ) || ( SELECT count ( * ) FROM memory WHERE mark LIKE 'definition%' AND run IN ( SELECT id FROM run WHERE kind = 'defrow' AND subject = :x ) ) || char ( 32 ) || 'formula' || char ( 32 ) || coalesce ( ( SELECT origin FROM formula WHERE word = :x AND ended = 0 ) , 'none' ) ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
print: = SELECT 'path' || char ( 32 ) || coalesce ( ( SELECT group_concat ( e.word , char ( 32 ) ) FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = :prev ) , '' ) || char ( 32 ) || 'sheet' || char ( 32 ) || coalesce ( ( SELECT group_concat ( name || '=' || coalesce ( value , '' ) , ';' ) FROM var WHERE run = :prev ) , '' ) ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
backpop: = INSERT INTO place ( word , x , y , z , t ) SELECT d.word , 10 * coalesce ( ( SELECT CAST ( m.text AS INTEGER ) FROM definition m WHERE m.word = d.word AND m.src = 'measured' AND m.hw LIKE d.word || ':rows' ORDER BY m.id LIMIT 1 ) , 0 ) , 10 * coalesce ( ( SELECT CAST ( m.text AS INTEGER ) FROM definition m WHERE m.word = d.word AND m.src = 'measured' AND m.hw LIKE d.word || ':structure' ORDER BY m.id LIMIT 1 ) , 0 ) , 10 * coalesce ( ( SELECT CAST ( m.text AS INTEGER ) FROM definition m WHERE m.word = d.word AND m.src = 'measured' AND m.hw LIKE d.word || ':text' ORDER BY m.id LIMIT 1 ) , 0 ) , ( SELECT coalesce ( max ( id ) , 0 ) FROM event ) FROM ( SELECT DISTINCT word FROM definition WHERE src = 'measured' ) d WHERE NOT EXISTS ( SELECT 1 FROM place p WHERE p.word = d.word AND p.ended = 0 ) ; SELECT count ( * ) FROM place WHERE ended = 0 ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
place: = INSERT INTO var ( run , name , value ) VALUES ( :run , ':x' , trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) ) ; INSERT INTO place ( word , x , y , z , t ) SELECT :x , 10 * coalesce ( ( SELECT CAST ( text AS INTEGER ) FROM definition WHERE word = :x AND src = 'measured' AND hw LIKE :x || ':rows' ORDER BY id LIMIT 1 ) , 0 ) , 10 * coalesce ( ( SELECT CAST ( text AS INTEGER ) FROM definition WHERE word = :x AND src = 'measured' AND hw LIKE :x || ':structure' ORDER BY id LIMIT 1 ) , 0 ) , 10 * coalesce ( ( SELECT CAST ( text AS INTEGER ) FROM definition WHERE word = :x AND src = 'measured' AND hw LIKE :x || ':text' ORDER BY id LIMIT 1 ) , 0 ) , ( SELECT coalesce ( max ( id ) , 0 ) FROM event ) ;
learn : -> learn:
define : -> define:
run : -> run:
test : -> test:
build : -> build:
find meaning : -> meaning:
print run : -> print:
run backpop -> backpop:
place : -> place:
```

## What this shows, and what it does not
- Shows: commands typed at the prompt, each firing only on the row its key lands on; a source's answer coming back as a run headed by the owner's modifiers, filling the asking run's data sheet with pointers to the word's definition memories; the brain reading its own rows to define, print its last run, report a word's meaning, re-test a line against memory, build the definitions the told limit skipped, and back-populate places.
- Does not show: understanding or learning in the owner's sense. Places still come from the measured source (ours). define says a definition's words; it does not reason over them.
- Learning is slow: 6.6 minutes for the 14 command lines in node; a command line takes 20 to 90 s in the page.
