# Teaching run results: define and place, typed at the prompt (2026-10-24)
Predictions frozen at 21:15 before the run: NEURON-TEACH-EXPECT-2026-10-24.md (sha256 3858b0c9181b...). The whole sheet (88 lines) was typed, one line at a time, into the page's real brain code (worker16.js, host15.js, sql.js 3.39.3) run in node; 10 of its lines were also typed in the page itself, in a real browser, through the prompt.

## The two taught lines (typed; the brain writes each as a formula row pointing at its teaching run)
```
define = SELECT text FROM definition WHERE word = :after AND src = 'sqldoc' ORDER BY id LIMIT 1 ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
place = INSERT INTO place ( word , x , y , z , t ) SELECT :after , 10 * coalesce ( ( SELECT CAST ( text AS INTEGER ) FROM definition WHERE word = :after AND src = 'measured' AND hw LIKE :after || ':rows' ORDER BY id LIMIT 1 ) , 0 ) , 10 * coalesce ( ( SELECT CAST ( text AS INTEGER ) FROM definition WHERE word = :after AND src = 'measured' AND hw LIKE :after || ':structure' ORDER BY id LIMIT 1 ) , 0 ) , 10 * coalesce ( ( SELECT CAST ( text AS INTEGER ) FROM definition WHERE word = :after AND src = 'measured' AND hw LIKE :after || ':text' ORDER BY id LIMIT 1 ) , 0 ) , ( SELECT coalesce ( max ( id ) , 0 ) FROM event ) ;
```
Then "define W" and "place W" for each of the 40 told SQL words, in the told block's order, then the same for DROP, substr and EXCEPT, which were never told or taught.

## Predictions against the results

| Prediction | Result | |
|---|---|---|
| P1 "define W" says W's first SQL doc line (41 words); no line: the line back with "?" | it said the doc line for every word that has one; for INTO, <, ( and the others it said the line back, without "?" (they are told words) | held; the form of the miss was wrong |
| P2 "place W" writes one live place row, x, y, z = 10 x measured rows, structure, text; equal to the lab's places | 43 live rows, all equal to the lab's places (largest difference 0); INSERT 10,0,0, DELETE -10,0,0, CREATE 0,10,0, group_concat and \|\| 0,0,10, all other told words 0,0,0 | held |
| P3 never told: DROP 0,-10,0; substr 0,0,-10; EXCEPT 0,0,0 | exactly (EXCEPT is stored as "except": a doc sentence gave the word birth in small letters first, and a gate keeps its first spelling) | held |
| P4 no place row for a word not placed | 43 place rows, 43 place statements sent by the formula's runs, 43 place log rows | held |
| P5 placing again keeps the old row | not tested by teaching: "place INSERT" a second time, and "place insert" in small letters, were answered from memory (same gates) in 0.4 and 0.3 s and wrote nothing. The told rule itself works when rows are written directly: a second place of INSERT ended the first | not tested as designed |
| P6 controls: "place store" 0,0,0; INSERT without its measured rows 0,0,0 | store [0, 0, 0]; INSERT without measured rows [0, 0, 0] | held |
| P7 define is slow, place is fast | both slow: median 9.1 s and 9.0 s; first lines 1-3 s, last lines 15-66 s (define EXCEPT 66 s); the whole sheet 17 minutes in node | WRONG: every new line lays new DNA rows, each a new trigger in a growing schema (1,984 triggers at the end) |

## In the page (real browser, typed through the prompt by clicking sheet lines and pressing run)

| Line | Seconds | The brain said |
|---|---|---|
| `define = SELECT text FROM definition WHE` | 4.5 |  |
| `place = INSERT INTO place ( word , x , y` | 8.7 |  |
| `define INSERT` | 8.2 | The INSERT statement comes in three basic forms. (sqlite.org/lang_insert.html) |
| `place INSERT` | 4.2 | place INSERT |
| `define DELETE` | 6.1 | The DELETE command removes records from the table identified by the qualified-ta |
| `place DELETE` | 4.3 | place DELETE |
| `place CREATE` | 9.3 | place CREATE |
| `place \|\|` | 10.4 | place \|\| |
| `define DROP` | 7.9 | The DROP TABLE statement removes a table added with the CREATE TABLE statement.  |
| `place DROP` | 5.1 | place DROP? |

Places the brain wrote into its own place table: INSERT 10,0,0; DELETE -10,0,0; CREATE 0,10,0; \|\| 0,0,10; DROP 0,-10,0. The stage drew exactly these, from that table.

## What this shows, and what it does not
- Shows: the brain can be taught, at the prompt, a process that defines a word from its SQL docs source and places it from its measured source, and the same two taught words place words it was never told (DROP, substr, EXCEPT). Every place is a row the brain wrote through its own run.
- Does not show: the brain finding a meaning. The numbers it places by are ours (steps 2 and 3), served by the "measured" source like a dictionary. A word that source does not hold is placed at 0,0,0 (store). For the brain to place a new SQL word by itself, it has to measure the word itself: run it (BUILD lines through mother already return rows and changes) or ask SQLite for its program (EXPLAIN: the brain drops it today; a told change).
- The memory hop stops re-teaching: a line the brain has seen, in any spelling, is answered from memory and runs nothing.

## Homework: the words the definitions use
The 76 SQL doc lines use 335 different words; 33 are SQL words. None has a meaning in the brain. The most used: the (71), of (41), a (36), to (21), are (16), operator (16), statement (14), for (14), clause (14), an (14), be (13), if (12), expression (11), each (10), one (10), may (9), can (9), row (8), input (8), either (8), returns (8), operators (8), result (7), more (7), rows (7), value (7), when (7), x (7), operands (7), function (7).

## The SQL docs source: the rule and its misses
- Rule: the first two sentences on the word's own SQLite doc page that hold the word (text from p, li, dd, td; filters drop navigation, contents entries, syntax fragments and lines that are mostly symbols; a symbol word's line must say operator, equals or not-equal).
- Misses: "-" got the \|\| sentence (a dash in the prose); "/" got the precedence table's introduction; "*" got a line using it as "all columns"; INTO, <, >, <=, >= and the punctuation have no line.

## Told changes in 17.1 (four statements; everything else is 16.4's told block byte for byte)
- CREATE TABLE place (id, word, x, y, z, t, ended); its trigger ends a word's older place (kept as history) and writes one log row with no action labels.
- The measured source: a gate for it, and the told source line asks it too.
- Not changed: 16.4's state trigger still writes "A formula wrote it" in its log text (true there: only taught formulas write state); yours to change.
