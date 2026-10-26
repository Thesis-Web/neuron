# Step 2: what each told word does to the silicon. Plan and predictions, frozen before any run
2026-10-24, turn 23. Written before the measuring script exists. Not changed after the runs; results go in a separate file.
Every prediction here is the builder's (Claude's), from what I know of SQLite's bytecode. None is the owner's.

## What is measured, and where
- Nothing here touches the brain or ~/neuron/v1. Everything runs in throwaway in-memory databases in the scratchpad.
- The brain under test: the 16.4 told block (physics16.json, 381 statements, 110 triggers), from NEURON-v16.4-SOURCES-2026-10-23.tar.gz.
- Two SQLites: the page's own (sql.js asm from the 16.4 sources, run in node) and this box's Python sqlite3 (3.37.2).

## Part A. The 40 told SQL words: bytecode with the word minus bytecode without it
- `EXPLAIN <statement>` prints the program SQLite runs (its bytecode, the layer between the SQL word and SQLite's C).
  Each opcode is one case in SQLite's C engine (vdbe.c).
- Test table, the same for every pair, fresh for every run: `t (a INTEGER, b TEXT)` with rows (1,'x'), (2,'y'), (3,'z').
- For each word: one line WITH it and the nearest line WITHOUT it (or with it swapped). The pairs are my choice; they are listed in the script exactly.
- Measured per line:
  1. the opcode multiset (names only; addresses, registers ignored);
  2. operand changes when the names are equal (P4/P5: sort order, compare flags, affinity);
  3. executed on a fresh copy: rows returned, rows changed, row count of t, tables in the schema.
- Statement verbs (SELECT INSERT UPDATE DELETE CREATE) cannot lose their verb: their whole program and its executed effect are shown.
- Words that cannot be removed without a syntax error (INTO, SET, TABLE, AS inside CAST, BY alone) are reported as "no pair" with SQLite's error.

## Part B. The 16 physics tables: what their triggers read, write, change, remove and call
- Measured by SQLite's own authorizer (sqlite3 set_authorizer) while it compiles one insert into each table that has triggers.
  The authorizer reports every read (table, column), insert, update, delete and function call, and names the trigger it belongs to.
  No parsing of SQL text.
- Static only: what mother is handed is built by value at run time, so it shows as "calls mother", not as what that SQL does.

## Part C. The 14 actions
- Fact already read (not a prediction): in the told block the 14 actions are gates with an empty DNA table and no formula.
  READ, WRITE, ... appear only as labels a builder wrote into the text of event rows (e.g. born's event says 'SPAWN WRITE CALL').
- Shown: each label next to what that trigger was measured to do in Part B, so the owner can see where a label fits and where it does not.

## Predictions (mine)
Statement verbs:
- SELECT a FROM t: OpenRead, Rewind, Column, ResultRow, Next. 3 rows out, 0 changes.
- INSERT INTO t VALUES (4,'w'): OpenWrite, NewRowid, MakeRecord, Insert. t +1 row.
- UPDATE t SET b='q' WHERE a=1: OpenWrite, Column, a compare, MakeRecord, Insert, no NewRowid. 1 change, t same size.
- DELETE FROM t WHERE a=1: OpenWrite, Delete, a compare. t -1 row.
- CREATE TABLE u (c): CreateBtree, ParseSchema, and a write into the schema table. Schema +1 table.
Clauses and operators:
- WITH: no opcode difference against the same query written as a subquery (it names, it does nothing).
- FROM: adds the table loop: OpenRead, Rewind, Next. Rows out 1 -> 3.
- WHERE a = 2: adds Column and one compare-and-jump. Rows out 3 -> 1.
- Compare operators against the base `WHERE a`: = gives Ne; <> and != give Eq; > gives Le; < gives Ge; IS gives Ne with a NULL-equal flag.
  So: <> and != compile to the identical program; = and <> are the two opposite jump opcodes; > and < are mirror opcodes.
- NOT a = 2: no opcode added; the compare flips Ne -> Eq.
- AND: one more Column + compare. OR: one more Column + compare and a different jump. Rows out stay 1.
- IN (1,2): ? an ephemeral table (OpenEphemeral) and a lookup. Rows 1 -> 2.
- LIKE: the compare is replaced by Function (like).
- EXISTS: ? not predicted.
- LIMIT 1: adds a counter: Integer + DecrJumpZero. Rows 3 -> 1.
- ORDER BY b: adds the sorter: SorterOpen, SorterInsert, SorterSort, SorterData, SorterNext. Rows same.
- DESC: same opcodes; only the sort order in the sorter's key (P4) differs.
- NULL: Integer -> Null.
- CAST(b AS INTEGER): adds Cast. INTEGER vs TEXT inside CAST: same opcodes, Cast's operand differs.
- AS (alias): no opcode change; only the column name.
- VALUES vs INSERT ... SELECT: the same or nearly the same program.
- instr: adds Function (instr). count, max, group_concat: add AggStep and AggFinal; rows 3 -> 1.
- ( ): no change. , : one more Column. ; : no change. * (all columns): one more Column. * (times): adds Multiply.
- ||: adds Concat.
Not told, measured for comparison (the owner asked about them): DROP TABLE u: Destroy and DropTable, schema -1.
EXCEPT: an ephemeral table; rows 3 -> 2. + Add, - Subtract, / Divide.
Opposites I expect the silicon to show by itself: INSERT/DELETE, CREATE/DROP, =/<>, >/<, +/-, * (times)// .

Physics (Part B):
- DELETE appears only in decide_go and lay_go (envelope) and in the source stand-ins' own triggers (inbox).
- mother is called by born_go, decide_go, lay_go, memwrong_go, bindrow_go, stmt_go.
- memory is written only by end_line, end_teach, memhit_go; timeline only by end_line and memhit_go.

## Controls (a result is not trusted unless these pass)
- C1 same line twice: identical program.
- C2 change only a literal (2 -> 3, 'y' -> 'z'): identical opcode names. The diff picks up words, not values.
- C3 the page's SQLite against Python's SQLite: report every pair whose diff differs between the two builds (version effects).
- C4 authorizer: a table with no triggers reports only its own insert; deleting a trigger removes exactly its rows from the report.

## What would count as a surprise worth stopping on
- A word whose with/without diff is empty in one build and not in the other.
- A label in Part C whose trigger was measured to do none of what the label says.
