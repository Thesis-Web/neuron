# Step 2 results: what each told word does to the silicon
2026-10-24, turn 23. Measured in throwaway in-memory databases in the scratchpad. Nothing in ~/neuron/v1 or in any brain changed.

- Plan and predictions were frozen at 19:06 before any run: NEURON-STEP2-EXPECT-2026-10-24.md (sha256 starts 0d4136a0c60f). The predictions are mine, not yours.
- Two SQLites: the page's own (sql.js, SQLite 3.39.3) and this box's Python (SQLite 3.37.2). Tables below are the page's unless marked.
- Every number below is read from the measurement files by report23.py. The words around them are mine.

**Check one row yourself (10 seconds).** Paste this; the 5th word of the program is the compare the silicon uses for ">" (Le):
```
sqlite3 :memory: "CREATE TABLE t (a, b); EXPLAIN SELECT a FROM t WHERE a > 2;" | awk '{print $2}' | tr '\n' ' '
```
Swap `a > 2` for `NOT a > 2` and for `a <= 2`: both give Gt. The silicon's opposite of ">" is "<=".

## Controls

| Control | Page | Python |
|---|---|---|
| same line twice: identical program | identical | identical |
| literal only, 2→3: same opcodes | same opcodes | same opcodes |
| literal only, 'y'→'z': same opcodes | same opcodes | same opcodes |
| literal only, LIMIT 1→2: same opcodes | same opcodes | same opcodes |
| authorizer: a table with no triggers reports only its own insert | — | passed |
| authorizer: remove one trigger (agree_go), only its rows disappear | — | passed |

So a word's bytecode diff shows the word, not the values typed with it. Where a diff shows "Integer" or "String8", that is the literal typed with the word (the 2 in `a > 2`) being loaded, not the word itself.

## A. The told SQL words
### A1. The statement words, whole (every program also has Init, Halt, Goto, Transaction; left out here)

| Word | Line | Bytecode | Run on t (3 rows) |
|---|---|---|---|
| SELECT | `SELECT a FROM t` | OpenRead Rewind Column ResultRow Next | 3 out |
| INSERT | `INSERT INTO t VALUES (4, 'w')` | OpenWrite Integer String8 NewRowid MakeRecord Insert | 0 out, 1 changed, t 3→4 |
| UPDATE | `UPDATE t SET b = 'q' WHERE a = 1` | Null Noop OpenWrite Rewind Column Ne Rowid IsNull Column String8 MakeRecord Insert Next Integer | 0 out, 1 changed |
| DELETE | `DELETE FROM t WHERE a = 1` | Null OpenWrite Rewind Column Ne Rowid Delete Next Integer | 0 out, 1 changed, t 3→2 |
| CREATE | `CREATE TABLE u (c)` | ReadCookie If SetCookie SetCookie CreateBtree OpenWrite NewRowid Blob Insert Close Close Null Noop OpenWrite SeekRowid Rowid IsNull String8 String8 String8 SCopy String8 MakeRecord Insert SetCookie ParseSchema | 0 out, tables 1→2 |
| DROP (not told) | `DROP TABLE u` | Null OpenWrite Rewind Column Ne Column Eq Rowid Delete Next Destroy Null OpenEphemeral IfNot OpenRead Rewind Column Ne Rowid Insert Next OpenWrite Rewind Rowid NotExists Column Column Column Integer Column MakeRecord Insert Next DropTable SetCookie String8 String8 | 0 out, tables 2→1 |
| DELETE (no WHERE) (not told) | `DELETE FROM t` | Clear | 0 out, 3 changed, t 3→0 |

### A2. Every word: bytecode WITH it minus WITHOUT it

| Word | With | Without | Added | Removed | Operands that changed (without → with) | Run: with / without |
|---|---|---|---|---|---|---|
| WITH | `WITH c AS (SELECT a FROM t) SELECT a FROM c` | `SELECT a FROM (SELECT a FROM t)` | — | — | nothing differs | 3 out / 3 out |
| FROM | `SELECT 1 FROM t` | `SELECT 1` | Goto Next OpenRead Rewind Transaction | — |  | 3 out / 1 out |
| WHERE | `SELECT a FROM t WHERE a = 2` | `SELECT a FROM t` | Column Integer Ne | — |  | 1 out / 3 out |
| = | `SELECT a FROM t WHERE a = 2` | `SELECT a FROM t WHERE a` | Integer Ne | IfNot |  | 1 out / 3 out |
| > | `SELECT a FROM t WHERE a > 2` | `SELECT a FROM t WHERE a` | Integer Le | IfNot |  | 1 out / 3 out |
| < | `SELECT a FROM t WHERE a < 2` | `SELECT a FROM t WHERE a` | Ge Integer | IfNot |  | 1 out / 3 out |
| IS | `SELECT a FROM t WHERE a IS 2` | `SELECT a FROM t WHERE a = 2` | — | — | Ne: 84 → 196 | 1 out / 1 out |
| NOT | `SELECT a FROM t WHERE NOT a = 2` | `SELECT a FROM t WHERE a = 2` | Eq | Ne |  | 2 out / 1 out |
| AND | `SELECT a FROM t WHERE a = 2 AND b = 'y'` | `SELECT a FROM t WHERE a = 2` | Column Ne String8 | — |  | 1 out / 1 out |
| OR | `SELECT a FROM t WHERE a = 2 OR b = 'x'` | `SELECT a FROM t WHERE a = 2` | Column Eq String8 | — |  | 2 out / 1 out |
| IN | `SELECT a FROM t WHERE a IN (1, 2)` | `SELECT a FROM t WHERE a = 1` | Eq Integer | — |  | 2 out / 1 out |
| LIKE | `SELECT a FROM t WHERE b LIKE 'y'` | `SELECT a FROM t WHERE b = 'y'` | Function IfNot | Ne |  | 1 out / 1 out |
| EXISTS | `SELECT EXISTS (SELECT 1 FROM t WHERE a = 2)` | `SELECT (SELECT 1 FROM t WHERE a = 2)` | Integer | Null |  | 1 out / 1 out |
| LIMIT | `SELECT a FROM t LIMIT 1` | `SELECT a FROM t` | DecrJumpZero Integer | — |  | 1 out / 3 out |
| ORDER BY | `SELECT a FROM t ORDER BY b` | `SELECT a FROM t` | Column×2 MakeRecord OpenPseudo SorterData SorterInsert SorterNext SorterOpen SorterSort | — |  | 3 out / 3 out |
| DESC | `SELECT a FROM t ORDER BY b DESC` | `SELECT a FROM t ORDER BY b` | — | — | SorterOpen: k(1,B) → k(1,-B) | 3 out / 3 out |
| NULL | `SELECT NULL` | `SELECT 1` | Null | Integer |  | 1 out / 1 out |
| CAST | `SELECT CAST(b AS INTEGER) FROM t` | `SELECT b FROM t` | Cast | — |  | 3 out / 3 out |
| AS | `SELECT a AS k FROM t` | `SELECT a FROM t` | — | — | nothing differs | 3 out / 3 out |
| INTEGER | `SELECT CAST(b AS INTEGER) FROM t` | `SELECT CAST(b AS TEXT) FROM t` | — | — | Cast: 66 → 68 | 3 out / 3 out |
| INTEGER | `CREATE TABLE u (c INTEGER)` | `CREATE TABLE u (c)` | — | — | String8: CREATE TABLE u (c) → CREATE TABLE u (c INTEGER) | 0 out, tables 1→2 / 0 out, tables 1→2 |
| VALUES | `INSERT INTO t VALUES (4, 'w')` | `INSERT INTO t SELECT 4, 'w'` | — | EndCoroutine Goto InitCoroutine Yield×2 |  | 0 out, 1 changed, t 3→4 / 0 out, 1 changed, t 3→4 |
| INTO | `INSERT INTO t VALUES (4, 'w')` | `INSERT t VALUES (4, 'w')` | cannot be removed: SQLite says *near "t": syntax error* | | | 0 out, 1 changed, t 3→4 / error |
| SET | `UPDATE t SET b = 'q' WHERE a = 1` | `UPDATE t b = 'q' WHERE a = 1` | cannot be removed: SQLite says *near "b": syntax error* | | | 0 out, 1 changed / error |
| TABLE | `CREATE TABLE u (c)` | `CREATE u (c)` | cannot be removed: SQLite says *near "u": syntax error* | | | 0 out, tables 1→2 / error |
| instr | `SELECT instr(b, 'y') FROM t` | `SELECT b FROM t` | Function String8 | — |  | 3 out / 3 out |
| count | `SELECT count(a) FROM t` | `SELECT a FROM t` | AggFinal AggStep Copy Null | — |  | 1 out / 3 out |
| max | `SELECT max(a) FROM t` | `SELECT a FROM t` | AggFinal AggStep CollSeq Copy Null | — |  | 1 out / 3 out |
| group_concat | `SELECT group_concat(b) FROM t` | `SELECT b FROM t` | AggFinal AggStep Copy Null | — |  | 1 out / 3 out |
| ( ) | `SELECT (a) FROM t` | `SELECT a FROM t` | — | — | nothing differs | 3 out / 3 out |
| , | `SELECT a, b FROM t` | `SELECT a FROM t` | Column | — |  | 3 out / 3 out |
| ; | `SELECT a FROM t;` | `SELECT a FROM t` | — | — | nothing differs | 3 out / 3 out |
| * (all columns) | `SELECT * FROM t` | `SELECT a FROM t` | Column | — |  | 3 out / 3 out |
| * (times) | `SELECT a * 2 FROM t` | `SELECT a FROM t` | Integer Multiply | — |  | 3 out / 3 out |
| \|\| | `SELECT b \|\| 'x' FROM t` | `SELECT b FROM t` | Concat String8 | — |  | 3 out / 3 out |
| = (in SET) | `UPDATE t SET b = 'q' WHERE a = 1` | `UPDATE t SET b 'q' WHERE a = 1` | cannot be removed: SQLite says *near "'q'": syntax error* | | | 0 out, 1 changed / error |
| <> (not told) | `SELECT a FROM t WHERE a <> 2` | `SELECT a FROM t WHERE a` | Eq Integer | IfNot |  | 2 out / 3 out |
| != (not told) | `SELECT a FROM t WHERE a != 2` | `SELECT a FROM t WHERE a` | Eq Integer | IfNot |  | 2 out / 3 out |
| >= (not told) | `SELECT a FROM t WHERE a >= 2` | `SELECT a FROM t WHERE a` | Integer Lt | IfNot |  | 2 out / 3 out |
| <= (not told) | `SELECT a FROM t WHERE a <= 2` | `SELECT a FROM t WHERE a` | Gt Integer | IfNot |  | 2 out / 3 out |
| EXCEPT (not told) | `SELECT a FROM t EXCEPT SELECT 1` | `SELECT a FROM t` | Close Column IdxDelete IdxInsert Integer MakeRecord Next OpenEphemeral Rewind | — |  | 2 out / 3 out |
| + (not told) | `SELECT a + 2 FROM t` | `SELECT a FROM t` | Add Integer | — |  | 3 out / 3 out |
| - (not told) | `SELECT a - 2 FROM t` | `SELECT a FROM t` | Integer Subtract | — |  | 3 out / 3 out |
| / (not told) | `SELECT a / 2 FROM t` | `SELECT a FROM t` | Divide Integer | — |  | 3 out / 3 out |
| substr (not told) | `SELECT substr(b, 1, 1) FROM t` | `SELECT b FROM t` | Function Integer×2 | — |  | 3 out / 3 out |

Notes on reading A2:
- IS: same compare as =, with a different flag: = carries 84 (includes 16, "jump if NULL"), IS carries 196 (includes 128, "NULL equals NULL").
- DESC: same bytecode; only the sorter's key changes, k(1,B) → k(1,-B).
- INTEGER in CAST: same bytecode; Cast's target changes, 66 (TEXT) → 68 (INTEGER). In CREATE TABLE it changes only the stored schema text.

### A3. The compare words: the jump each one compiles to
SQLite compiles a compare as "skip this row unless ...", so it uses the opposite jump. Base line: `SELECT a FROM t WHERE a <op> 2`.

| Word | Jump in the bytecode | Rows out (of 1,2,3) |
|---|---|---|
| = | Ne | 1 |
| <> (not told) | Eq | 2 |
| != (not told) | Eq | 2 |
| > | Le | 1 |
| <= (not told) | Gt | 2 |
| < | Ge | 1 |
| >= (not told) | Lt | 2 |

Identical programs (checked in Python's SQLite): `NOT a = 2` ≡ `a <> 2`; `NOT a > 2` ≡ `a <= 2`; `NOT a < 2` ≡ `a >= 2`; `NOT a <> 2` ≡ `a = 2`.
- <> and != are one program: one meaning, two spellings.
- The silicon's opposite pairs are =/<>, >/<=, </>=. ">" and "<" are mirror images (Le and Ge), not opposites.
- AND adds a compare that rejects (Ne); OR adds one that accepts (Eq).

### A4. Opposites the silicon shows by itself, and ones it does not

| Pair | What the silicon shows |
|---|---|
| INSERT / DELETE | Insert vs Delete opcode; rows in t 3→4 vs 3→2 |
| CREATE / DROP | CreateBtree + ParseSchema vs Destroy + DropTable; tables 1→2 vs 2→1 |
| = / <> , > / <= , < / >= | NOT of one is the identical program of the other |
| AND / OR | reject jump (Ne) vs accept jump (Eq) |
| + / - , × / ÷ | four separate opcodes (Add, Subtract, Multiply, Divide). Nothing in the bytecode marks them as opposites. That they are opposites is my belief, not measured. |
| NULL / a value | Null vs Integer |

### A5. Where the two SQLites differ
Every with/without diff in A2 is the same in both. Three whole programs differ: UPDATE, CREATE and DROP. Python's SQLite 3.37.2 adds one Delete opcode to each: it removes the old row and writes the new one. The page's SQLite 3.39.3 rewrites the row in place, with no Delete. So "update = delete + write" holds in one SQLite version and not in the other.

### A6. My predictions against the measurement

| Prediction (frozen 19:06) | Measured | |
|---|---|---|
| SELECT: OpenRead Rewind Column ResultRow Next; 3 out | exactly that | held |
| INSERT: OpenWrite NewRowid MakeRecord Insert; t +1 | that, + the literal loads | held |
| UPDATE: Column, compare, MakeRecord, Insert, no NewRowid | that, + Rowid IsNull; Python's SQLite also Delete | held; build difference not predicted |
| DELETE: OpenWrite Delete compare; t -1 | that; with no WHERE it is one Clear | held |
| CREATE: CreateBtree ParseSchema + schema write | that, + cookie reads and writes | held |
| WITH: no difference from a subquery | nothing differs | held |
| FROM: adds OpenRead Rewind Next | that, + Transaction: reading a table opens a read transaction | held + one not predicted |
| compare words: = Ne, <> != Eq, > Le, < Ge, IS = Ne with a flag | exactly | held |
| NOT: flips Ne to Eq, adds nothing | exactly | held |
| IN (1,2): an ephemeral table | two compares (Eq), no table | WRONG |
| EXISTS: not predicted | only the result's start value changes (Null → Integer 0) | — |
| LIMIT: Integer + DecrJumpZero | exactly | held |
| ORDER BY: the sorter | that, + OpenPseudo MakeRecord | held |
| DESC: only the sort key | exactly | held |
| AS (alias), ( ), ; : nothing | nothing | held |
| VALUES vs INSERT…SELECT: same or nearly | SELECT form adds a coroutine (5 opcodes) | held, roughly |
| count max group_concat: AggStep AggFinal | that, + Copy Null (max + CollSeq) | held |
| * (times) Multiply, \|\| Concat, + Add, - Subtract, / Divide | exactly | held |
| Opposites: INSERT/DELETE, CREATE/DROP, =/<> | shown | held |
| Opposites: > / < | mirror images; the opposite of > is <= | WRONG as an opposite |
| Opposites: + / -, × / ÷ | not shown by the silicon | WRONG: my belief |
| DELETE only in decide_go, lay_go and the stand-ins | exactly (+ mother's own host code empties outboxes) | held |
| mother called by born, decide, lay, memwrong, bindrow, stmt | also end_branch (step back) | WRONG: missed one |
| memory written only by end_line, end_teach, memhit_go | exactly | held |

## B. The physics: what each told trigger does
Two measures, both SQLite's own: the authorizer (which tables a trigger reads, writes, removes, which functions it calls) and the bytecode SQLite lists for each trigger (page SQLite).
"log" = writing the event table. The event table is in the brain's SQLite, but it is the narration the page draws from.

### B1. Per trigger

| Trigger | On | Reads | Writes (insert / update) | Removes | Calls | Bytecode: brain / log | Labels written in its log text |
|---|---|---|---|---|---|---|---|
| input_teach | insert input | encoder, input, run + clock | born, run |  |  | 142 / 35 | HEAR WRITE |
| input_bind | insert input | input + clock | bindq, run |  |  | 82 / 0 |  |
| input_run | insert input | input + clock | run |  |  | 115 / 0 |  |
| run_go | insert run | encoder, input, run + clock | encode, var, run.root |  |  | 541 / 0 |  |
| run_said | update run | run | **only its own log line** |  |  | 2 / 97 | HEAR WRITE |
| encode_word | insert encode | encode, encoder, formula, run | born, encode, source, run.gates |  |  | 320 / 0 |  |
| encode_done | insert encode | bindq, encode, run | bindgo, decide |  |  | 94 / 38 | READ FIND |
| born_go | insert born | born, encoder + clock | definition, encoder, source |  | mother | 233 / 40 | SPAWN WRITE CALL |
| decide_go | insert decide | decide, encoder, envelope, formula, g3, gap, memory, run | envelope, memhit, run.memid/reopen | envelope | mother | 548 / 57 | FIND COMPARE |
| memhit_go | insert memhit | memhit, memory, run, timeline + clock | memwrong, output, timeline, memory.last/times, run.output/recalled/t1 |  |  | 263 / 153 | FIND COMPARE WRITE; CLOCK WRITE; READ SAY |
| memwrong_go | insert memwrong | encoder, memwrong + clock | nothing itself; it hands its work to mother |  | mother | 94 / 48 | COMPARE WRITE |
| lay_go | insert lay | encoder, envelope, lay + clock | envelope, lay.shard | envelope | mother | 379 / 133 | COMPARE WRITE; WRITE SPAWN CALL |
| bind_go | insert bindgo | bindgo, bindq, encoder, run | bindrow |  |  | 967 / 0 |  |
| bindrow_go | insert bindrow | bindrow, encoder | lay, bindrow.found |  | mother | 110 / 109 | WRITE |
| fire_go | insert fire | encoder, fire, formula, receipt, run | gap, input, fire.word |  |  | 548 / 0 |  |
| stmt_go | insert stmt | stmt | nothing itself; it hands its work to mother |  | mother | 5 / 18 | READ SAY |
| secondary_refused | insert secondary | run, secondary | gap, run.failed |  |  | 69 / 18 | COMPARE |
| secondary_ask | insert secondary | secondary | sense |  |  | 132 / 0 |  |
| secondary_sql | insert secondary | secondary, stmt | sense |  |  | 87 / 41 | HEAR WRITE |
| secondary_wait | insert secondary | run, secondary, stmt + clock | gap, var, run.failed |  |  | 100 / 16 |  |
| sense_ask | insert sense | run, secondary, sense + clock | definition, gap, var, run.failed, sense.asked/needed/ok/setaside/wrong |  |  | 366 / 104 | HEAR WRITE; COMPARE FIND |
| sense_sql | insert sense | run, secondary, sense, stmt + clock | var, run.failed, sense.ok/wrong |  |  | 231 / 33 | COMPARE FIND |
| definition_split | insert definition | definition | defword |  |  | 18 / 0 |  |
| defword_next | insert defword | defword | defword |  |  | 43 / 0 |  |
| say_go | insert say | run, say + clock | var |  |  | 40 / 21 | SAY |
| relation_drawn | insert relation | relation, run + clock | **only its own log line** |  |  | 0 / 87 | WRITE |
| formula_written | insert formula | encoder, formula, proc, receipt, run + clock | proc, proc.status |  |  | 47 / 171 | WRITE |
| source_go | insert source | definition, encoder, formula, run, source | agree, fire, gap, input, encoder.sourced |  |  | 463 / 0 |  |
| agree_go | insert agree | agree, definition, defword, formula, need | need, need.n |  |  | 102 / 130 | READ COMPARE WRITE |
| end_branch | insert end | encoder, end, proc, procrun, receipt, run + clock | procrun, stepq, proc.status/uses, run.t1 |  | mother | 320 / 53 | READ WRITE |
| step_back | insert stepq | encoder, input, run, stepq | fire, gap |  |  | 141 / 123 | FIND COMPARE MOVE |
| end_teach | insert end | end, formula, memory, receipt, run + clock | formula, memory, formula.ended, run.memid/t1 |  |  | 285 / 0 |  |
| end_line | insert end | encoder, end, formula, gap, memory, proc, receipt, run, secondary, timeline, var + clock | BUILD, memory, output, timeline, memory.ended, proc.right/wrong, run.mark/memid/output/t1, var.src |  |  | 764 / 468 | READ JOIN WRITE; COMPARE FIND; FIND COMPARE WRITE; CLOCK WRITE; READ SAY |
| receipt_gap | insert receipt | encoder, formula, gap, receipt, run | gap |  |  | 112 / 36 |  |
| build_go | insert BUILD | BUILD | stmt |  |  | 10 / 0 |  |
| state_written | insert state | run, state | **only its own log line** |  |  | 0 / 44 | WRITE |
| proc_status | update proc | proc, run | **only its own log line** |  |  | 3 / 44 | COMPARE WRITE |
| miss_k (×73, one shape) | insert land_k (instead of) | g_k arrival, remainder | lay | | | 32 / 0 | |
| work (×7, each source stand-in) | insert inbox | corpus, inbox, outbox | outbox | inbox | satwork | 53 / 0 | |

### B2. The whole told physics (37 triggers), bytecode counted

| Opcode | Brain work | Log for the page |
|---|---|---|
| all | 7776 | 2117 |
| Insert (write a row) | 116 | 38 |
| Delete (remove a row) | 2 | 0 |
| Column (read a cell) | 951 | 124 |
| Ne | 212 | 25 |
| Eq | 23 | 3 |
| Le | 26 | 3 |
| Lt | 2 | 1 |
| Ge | 2 | 0 |
| Gt | 2 | 0 |
| Add | 28 | 0 |
| Subtract | 30 | 0 |
| Multiply | 0 | 0 |
| Divide | 0 | 0 |
| Concat (join text, \|\|) | 238 | 163 |
| Program (fire another trigger) | 43 | 0 |
| mother | 12 | 0 |
| substr (cut text) | 53 | 2 |
| instr (find in text) | 72 | 0 |
| trim | 103 | 0 |

### B3. One line in a bare brain (the told block's own last line, the source teaching line), real host
Mother was handed 121 texts:

| Kind | Count |
|---|---|
| INSERT INTO land_N | 32 |
| INSERT INTO gN | 31 |
| CREATE TRIGGER hop_N_N | 31 |
| CREATE TABLE gN | 9 |
| CREATE VIEW land_N | 9 |
| CREATE TRIGGER miss_N | 9 |
That is 9 new neurons (table, view, miss trigger each), 31 DNA rows, 31 hop triggers, and the landings.

What each DNA row's own hop trigger does (authorizer):

| Hop triggers | Reads | Writes | Functions |
|---|---|---|---|
| 29 | encoder, gN, land_N + clock | event, fire, land_N, receipt, gN (update) | coalesce, instr, max, substr, trim |
| 1 | encoder, gN, land_N, receipt, run, var + clock | end, event, fire, receipt, stmt, gN (update) | coalesce, group_concat, max, min, quote, trim |
| 1 | encoder, gN, land_N, receipt, run, var + clock | event, fire, land_N, receipt, stmt, gN (update) | coalesce, group_concat, instr, max, min, quote, substr, trim |

In words: count the hit on its own row, write the receipt, write a fire row, write the log line, and land the run on the next gate (or end it). The two on the ";" gate also decode the statement into output to sources.

### B4. The brain's clock
Every "now" in the told block is `(SELECT coalesce(max(id), 0) FROM event)`: the number of log rows written so far. The brain has no other clock. Its time is the length of the page's narration; if the log stopped being written, the brain's time would stop.

## C. The 14 actions
- In the told block each action (READ, WRITE, …, SPAWN) is a gate with an empty DNA table, a miss trigger, and no formula. Nothing runs when a line passes one.
- The action names appear only as labels a builder wrote into the text of log rows. Count of each label in the told triggers' log text, in the hop trigger text, and in mother's host code:

| Action | Told triggers | Each hop trigger | Mother (host code) |
|---|---|---|---|
| READ | 7 | 0 | 1 |
| WRITE | 20 | 1 | 2 |
| COMPARE | 12 | 1 | 0 |
| ADD | 0 | 0 | 0 |
| SUBTRACT | 0 | 0 | 0 |
| MOVE | 1 | 0 | 3 |
| FIND | 8 | 0 | 1 |
| SPLIT | 0 | 0 | 0 |
| JOIN | 1 | 0 | 0 |
| CLOCK | 2 | 0 | 0 |
| HEAR | 4 | 0 | 0 |
| SAY | 4 | 0 | 0 |
| CALL | 2 | 0 | 3 |
| SPAWN | 2 | 0 | 0 |

- ADD, SUBTRACT and SPLIT label nothing. The silicon does them anyway: the told physics has 28 Add and 30 Subtract opcodes (counters +1, and the word positions used to cut a line's first word off the rest) and 53 substr / 72 instr calls (that cut is the split).
- DELETE (removes a row: 2 in the told physics) and NOT EXISTS (the miss test in all 73 miss triggers) are done and not named, as found before.
- Four triggers write nothing but their own log line: run_said, relation_drawn, state_written, proc_status. Their labels (HEAR WRITE, WRITE, WRITE, COMPARE WRITE) describe the narration, not brain work.
- Compare each label with that trigger's row in B1 to judge it. I have not scored them: deciding what a label "should" measure would be me assigning meanings.

## D. Where the reference draft disagrees with today's measurements
NEURON-REFERENCE-DRAFT-1-2026-10-23.md. I rebuilt the original draft from the commands of the session that wrote it (23:27-23:31 UTC on 10-23, plus its one wording edit) and diffed it with today's file: exactly two changes, both yours, lines 243 and 489. Below are lines that today's measurements contradict. I have not edited the draft.

| Line | The draft says | Measured today |
|---|---|---|
| 276 | "14 physical actions: READ, WRITE, …" in the told block | Each is a gate with an empty DNA table and no formula; nothing runs when a line passes one. The names exist only as labels in log text (part C). ADD, SUBTRACT and SPLIT label nothing. |
| 277 | "16 physics tables with their triggers" | encoder, memory, timeline, var have no trigger of their own (other triggers write them). state's only trigger writes the log and nothing else. |
| 763, 780, 947 | positions exist only in the page | The same claim you corrected at line 489, three more times. It is true of what I built, but it is my gap against your design, written as if it were a plain fact. |
| (missing) | — | The brain's clock is the count of log rows (B4). The draft does not say this anywhere. |

## What this does not show
- Part A's test lines are my choice; they are all in the table. Another base line could add or remove an opcode or two (the frame, a literal load).
- B1 and B2 are static: what a trigger can do when it fires, not how often it fires. Only B3 is a real run, of one line.
- This measures the SQL words and the physics only. It says nothing yet about any other word, or about where anything sits in the graph. No graph was changed.

## Files
- NEURON-STEP2-EXPECT-2026-10-24.md: the plan and predictions, frozen before the runs.
- NEURON-STEP2-RESULTS-2026-10-24.md: this file.
- NEURON-STEP2-SOURCES-2026-10-24.tar.gz: the scripts, every measurement file, and README with the commands to rerun all of it.
