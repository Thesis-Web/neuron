# Step 3 results: lines between SQL words, and the first measured picture (2026-10-24)
Predictions frozen at 20:02 before any run: NEURON-STEP3-EXPECT-2026-10-24.md (sha256 111bd3a7a5fb...). Measured in the page's own SQLite (sql.js 3.39.3) by rel.js. Numbers below come from lab.json, expect17.json and the browser check.

## Points
- 44 told points from the 40 told SQL words (AS, INTEGER, = and * each measured two different jobs, so two points each), and 10 not-told words for comparison.

## Lines found, by kind (each kind also rejected pairs it tested)

| Kind | Lines | Tested and rejected |
|---|---|---|
| inverse | 5: INSERT / DELETE; CREATE / DROP; + / -; * (times) / /; \|\| / substr | 3 |
| complement | 6: = (compare) / <>; = (compare) / !=; <> / IS; != / IS; > / <=; < / >= | 22 |
| same program | 1: <> / != | 27 |
| negation | 8: = (compare) / <>; = (compare) / !=; <> / = (compare); != / = (compare); > / <=; < / >=; >= / <; <= / > | 0 |
| negates | 7: NOT / = (compare); NOT / <>; NOT / !=; NOT / >; NOT / <; NOT / >=; NOT / <= | 1 |
| dual | 1: AND / OR | 0 |
| completes | 15: FROM / SELECT; INTO / INSERT; VALUES / INSERT; ( / INSERT; ) / INSERT; , / INSERT; SET / UPDATE; = (in SET) / UPDATE; FROM / DELETE; TABLE / CREATE; ( / CREATE; AS (in CAST, WITH) / WITH … | 0 |
| modifies | 38: WHERE / SELECT; ORDER / SELECT; BY / SELECT; DESC / SELECT; LIMIT / SELECT; , / SELECT; WHERE / UPDATE; WHERE / DELETE; INTEGER (column type) / CREATE; INTEGER (in CAST) / CAST; = (compare) / WHERE; > / WHERE … | 0 |
| no change | 5: AS (name) / SELECT; ( / SELECT; ) / SELECT; ; / SELECT; WITH / SELECT | 0 |
| same spelling | 4: AS (name) / AS (in CAST, WITH); INTEGER (in CAST) / INTEGER (column type); = (compare) / = (in SET); * (all columns) / * (times) | 0 |
| complement (NULL row) | 0 | 28 |
| same rows (control) | 0 | 1 |

Reading the table: negation tested NOT A against every other compare word and lists only the matches. completes, modifies and no change sort each tested word into exactly one of the three, so WHERE landing in modifies is completes rejecting it.

## Predictions against the measurement

| Prediction | Measured | |
|---|---|---|
| complement: only =/<>, =/!=, >/<=, </>= | also <>/IS and !=/IS: with no NULL row, IS keeps the same rows as = | WRONG (missed two) |
| with a NULL row, = and <> stop being complements | none of the 28 pairs is a complement with a NULL row | held |
| same program: only <> and != | only <> and != (27 other pairs rejected) | held |
| negation: NOT = is <> and !=, NOT <> is =, NOT > is <=, NOT < is >=, NOT >= is <, NOT <= is > | exactly these 8; NOT IS compiles to no other compare word | held |
| dual: De Morgan both ways | holds on 3 pairs p, q; control (AND keeps the same rows as OR) fails | held |
| inverse: INSERT/DELETE, CREATE/DROP, \|\|/substr, +/-, * (times)// | exactly; INSERT/UPDATE, SELECT/DELETE, +/* rejected | held |
| completes: FROM, INTO, VALUES, SET, = (in SET), TABLE, AS (in CAST, WITH), INTEGER (in CAST) | all but INTEGER (in CAST): SQLite accepts CAST(b AS) | WRONG for INTEGER in CAST |
| modifies: WHERE, ORDER, BY, DESC, LIMIT, , (SELECT), INTEGER (column type), the WHERE words, the SELECT functions | as predicted; also , ( ) in INSERT and ( ) in CREATE and CAST complete | held, plus findings |
| no change: AS (name), ( ) around a column, ;, WITH | exactly | held |
| first picture: INSERT +x, DELETE -x, CREATE +y, \|\| and group_concat +z, ~40 of 45 at origin | exactly; 39 of 44 told points at 0,0,0 | held |

Findings not predicted:
- FROM "completes" SELECT only because the columns name the table (SQLite says "no such column"), not by grammar.
- The same word completes one verb and modifies or changes nothing in another: , completes INSERT and modifies SELECT; ( ) completes INSERT, CREATE and CAST and changes nothing around a column. One spelling, different jobs by where it arrives.
- Among the told words alone there is no complement pair: the told compare words are =, >, <, IS, and their complements (<>, <=, >=) are not told.

## The placement rule, and a change I made after seeing a result
- Lines off: a point's place is its own measured numbers (10 brain units per unit). Lines on: the first rule I wrote (each line pulls 1 against a hold of 1) pulled every point into a ball near origin: INSERT went from 10 to 1.5, DELETE to -2.4, because a word like SELECT has about 25 lines.
- I added the proportional rule (a point keeps (1 - pull) of its own place, its lines share the rest equally) after seeing that. Both are on the page; the proportional one is the default, pull 0.5. With every kind on: INSERT 5.4, 0.1, 0.0; DELETE -4.3, 0.0, 0.0; CREATE 0.1, 5.9, 0.0; INTO 2.7, 0.0, 0.0; TABLE 0.1, 2.9, 0.0.
- Neither rule has a random start, spacing push, step cap, compass direction or across rule; the answer is the same whatever the order (checked).

## The page check (headless Chromium)

| Check | Result |
|---|---|
| places read back from SQLite against node, off | 44 of 44, largest difference 0 |
| places read back from SQLite against node, allShare | 44 of 44, largest difference 0 |
| places read back from SQLite against node, allSum | 44 of 44, largest difference 0 |
| places read back from SQLite against node, completes | 44 of 44, largest difference 0 |
| places read back from SQLite against node, rtg | 44 of 44, largest difference 0 |
| places read back from SQLite against node, notTold | 54 of 54, largest difference 0 |
| places read back from SQLite against node, afterRestart | 54 of 54, largest difference 0 |
| 16.4 parts | 15 premade runs; "the same line twice" said "cat? sat?"; typed "dog ran" said "dog? ran?" |
| back to the 16.4 view | 1193 points drawn, axes ['+x', '-x'] |
| sideways scroll, desktop / phone | 0 / 0 px |
| page errors | 0 |
