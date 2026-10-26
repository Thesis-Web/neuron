# Step 3: lines between SQL words, and the first measured picture. Predictions frozen before any run
2026-10-24, turn 23. The builder's predictions (Claude's), not the owner's. Results go in a separate file; this one is not changed.
Everything runs in the page's own SQLite (sql.js 3.39.3) in node, on fresh throwaway databases.
Test table t (a INTEGER, b TEXT) rows (1,'x'), (2,'y'), (3,'z'); for the NULL check, the same plus (NULL, NULL).

## Points
- One point per told SQL word. Where step 2 measured one spelling doing two different things, it gets two points (the design: one meaning, one gate):
  "* (all columns)" and "* (times)"; "= (compare)" and "= (in SET)"; "AS (name)" and "AS (in CAST, WITH)"; "INTEGER (in CAST)" and "INTEGER (column type)".
  A line of kind "same spelling" ties each pair.
- Not-told words measured in step 2 are points too, shown only with a switch: DROP, substr, <>, !=, >=, <=, +, -, /, EXCEPT.

## A point's own place (the three default axes), measured by running its line
- x rows: +1 if its line adds a row to t, -1 if it removes one, else 0.
- y structure: +1 if its line adds a table, -1 if it removes one, else 0.
- z text: +1 if its output text is longer than every text that went in and holds each one (join), -1 if shorter than what went in (cut), 0 if its output is not text.
- Other views (a menu, never the default): read, test, number, gather = how many such steps its line adds over the line without it (step 2, table A2). Opcode families are listed in the code.

## Lines between points, one kind each, each a test
1. inverse: A then B puts the database or value back exactly. Predict: INSERT/DELETE; with not-told on: CREATE/DROP, ||/substr, +/-, * (times)// .
2. complement: on t, the rows A keeps and the rows B keeps together are all rows, and never the same row. Tested on every pair of =, <>, !=, >, <, >=, <=, IS.
   Predict: = with <>, = with !=, > with <=, < with >=, and no other pair. With a NULL row: = and <> are no longer complements (neither keeps the NULL row).
3. same program: A and B compile to the identical program in the same line. Predict: only <> and != .
4. negation: NOT A compiles to the identical program as B. Predict: NOT = is <> and !=, NOT <> is =, NOT > is <=, NOT < is >=, NOT >= is <, NOT <= is >. NOT is tied to each word it negates.
5. dual: NOT (p AND q) keeps the same rows as (NOT p) OR (NOT q), and NOT (p OR q) as (NOT p) AND (NOT q). Predict: both hold.
6. completes / modifies / no change, a word against the verb whose line it is in. Remove the word alone, and remove its clause (spans listed in the code):
   - completes: both removals make SQLite refuse the line;
   - modifies: removing its clause still runs, and the program or the result changes;
   - no change: removing it gives the identical program.
   Predict completes: FROM (SELECT and DELETE), INTO, VALUES, SET, = (in SET), TABLE, AS (in CAST, WITH) with WITH and CAST, INTEGER (in CAST) with CAST.
   Predict modifies: WHERE (SELECT, UPDATE, DELETE), ORDER, BY, DESC, LIMIT and , (SELECT), INTEGER (column type) with CREATE;
   inside WHERE: =, >, <, IS, IN, LIKE, AND, OR, NOT, EXISTS modify WHERE; in SELECT's columns: ||, * (times), * (all columns), CAST, instr, count, max, group_concat modify SELECT.
   Predict no change: AS (name), ( ) around a column, ; , WITH (against the same query as a subquery).
7. same spelling: the four pairs above (not a test; the spelling is the same).

## The first picture (all lines off, told words only)
- INSERT at +x, DELETE at -x, CREATE at +y, || and group_concat at +z. Every other told point (about 40 of 45) at origin, 0,0,0.
- With not-told on: DROP at -y, substr at -z; the rest of the not-told words at origin.
- With lines on, a point sits at the balance of its own place and the places of the points it is tied to (each line pulls equally; one slider sets how hard a point holds its own place). Nothing else moves it: no random start, no spacing push, no step cap, no compass directions, no across rule.

## What would stop me
- A test that cannot fail: each line kind must also find pairs it rejects (complement rejects > with <; same program rejects = with IS; completes rejects WHERE).
- The page's places not matching the solve run in node on the same rows.
