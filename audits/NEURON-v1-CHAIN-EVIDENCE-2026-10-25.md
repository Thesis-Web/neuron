# V1-CHAIN: how the hand-built v1 brain works (read-only trace, 2026-10-25)

Source files (nothing in them was touched):

- `/home/exnulla/neuron/v1/egg.sql` (21 lines, 5570 bytes, mtime 2026-10-19 19:41:51 CDT)
- `/home/exnulla/neuron/v1/bottom.py` (21 lines, 806 bytes, mtime 19:00:38 CDT)
- `/home/exnulla/neuron/v1/kernel/mother.c` (18 lines) and `mother.so` (built 19:00:07 CDT)
- `/home/exnulla/neuron/v1/kernel/eval.c` (125 lines, stock SQLite `ext/misc/eval.c`) and `eval.so` — present but **never loaded** (no `eval` in egg.sql or bottom.py; egg.sql:1 and bottom.py:7 load only `mother`)
- `/home/exnulla/neuron/v1/kernel/sqlite3.h`, `sqlite3ext.h` — headers for building the two extensions
- `/home/exnulla/neuron/v1/brain.db` (143360 bytes, 35 pages of 4096, mtime 19:41:51 CDT) — queried only as the copy `/tmp/claude-1000/-home-exnulla-neuron-v1/95237a7f-7d7c-47a3-a249-06f9202b6633/scratchpad/traceB/brain_copy.db`

Replay evidence: running `egg.sql` (with the `.load` path made absolute) on a fresh scratch db and feeding the three lines recorded in `input` ids 5–7 through the same code path as bottom.py reproduced brain.db exactly: identical `label` (25 rows), `shards.n = 104`, identical `sqlite_master` order (46 entries). The raw statement trace of that replay is in `/tmp/claude-1000/-home-exnulla-neuron-v1/95237a7f-7d7c-47a3-a249-06f9202b6633/scratchpad/traceB/trace_raw.txt`.

Vocabulary used below is the brain's own: `label.word` for gates 1–5 is `read, hear, born, hop, BUILD` (egg.sql:10), so g1 = read, g2 = hear, g3 = born, g4 = hop, g5 = BUILD.

---

## 1. Every table

### 1a. Hand-laid by egg.sql

egg.sql first clears what it will re-lay (egg.sql:3–5), keeping `input`:

```sql
DROP TRIGGER IF EXISTS input;
DROP TABLE IF EXISTS label;
DROP TABLE IF EXISTS shards;
```

| table | egg.sql line | columns (verbatim) | purpose as evident from the code |
|---|---|---|---|
| `input` | 6 | `id INTEGER PRIMARY KEY, text TEXT NOT NULL, time TEXT DEFAULT CURRENT_TIMESTAMP, answer TEXT` | The prompt. bottom.py inserts the typed line into `text`; the brain writes back into `answer` (trigger g3/g4 write mother's `error:` text, trigger g5 writes mother's reply to a BUILD). `CREATE TABLE IF NOT EXISTS`, so it survives re-running egg.sql; `id` is the **run** number everywhere else. |
| `shards` | 7–8 | `n INTEGER NOT NULL`, one row, starts at 0 | A single global counter. Every row written into g2, g3, g4, g5 and every born gate table takes `n+1` as its `shard`. It is the brain's clock: shard order = firing order. |
| `label` | 9–10 | `gate INTEGER PRIMARY KEY, word TEXT NOT NULL UNIQUE` | word → gate number. `gate` is the rowid, so each new word gets the next number and that number names its table `g<gate>`. Seeded with `('read'), ('hear'), ('born'), ('hop'), ('BUILD')` = gates 1–5. |
| `g1` (read) | 11 | `shard INTEGER, arrival INTEGER, remainder INTEGER, trigger INTEGER, run INTEGER, pos INTEGER, rest TEXT, cur TEXT` | Character reader. `rest` = text not yet read, `cur` = the word being gathered. Rows are deleted when the line is fully read (egg.sql:17 last statement), so it is always empty at rest. |
| `g2` (hear) | 12 | `… base 6 …, word TEXT, gate INTEGER` | The heard tokens of each run, one row per token with `pos` 1..n and the token's `gate`. This is the only "sheet" the hop and BUILD read from. |
| `g3` (born) | 13 | `… base 6 …, word TEXT, said TEXT` | One row per word heard for the first time; `said` = mother's reply to the birth SQL (`ok` / `error: …`). |
| `g4` (hop) | 14 | `… base 6 …, said TEXT` | One row per hop; `arrival` = the gate just landed on, `remainder` = the gate to go to; `said` = mother's reply to the landing INSERT. |
| `g5` (BUILD) | 15 | `… base 6 …` (no extra columns) | The BUILD gate; its trigger is the only one that ends a run with a reply. |

"base 6" = `shard INTEGER, arrival INTEGER, remainder INTEGER, trigger INTEGER, run INTEGER, pos INTEGER` — every gate table has these six, in this order.

### 1b. Created later by runs (not in egg.sql)

Each word heard for the first time births two tables and one trigger (see §3a): `g<N>` (the gate, base 6 columns, plus trigger `g<N>`) and `g<N+1>` (its `.definition` table). The `.definition` schema, from egg.sql:19:

```
id INTEGER PRIMARY KEY, source TEXT, entry TEXT, sense TEXT, class TEXT, text TEXT, example TEXT, origin TEXT, first_use TEXT, synonyms TEXT, antonyms TEXT, times INTEGER, first_at TEXT, last_at TEXT, ended_at TEXT
```

All eleven `.definition` tables in brain.db are **empty**; nothing in v1 writes a definition.

### 1c. Creation order (sqlite_master rowid in the copy)

```
rowid type    name                      rootpage
 1    table   input                     2      <- egg.sql:6  (survived from before; see §5)
 2    table   shards                    3      <- egg.sql:7
 3    table   label                     4      <- egg.sql:9
 4    index   sqlite_autoindex_label_1  6      <- UNIQUE on label.word
 5-9  table   g1 g2 g3 g4 g5            7-11   <- egg.sql:11-15
10-15 trigger input g1 g2 g3 g4 g5             <- egg.sql:16-21
16/17 table+trigger g6   (' ')          14     <- run 5, born
18    table   g7   (' .definition')     15
19/20 table+trigger g8   (CREATE)       16
21    table   g9   (CREATE.definition)  17
22/23 table+trigger g10  (TABLE)        19
24    table   g11                       20
25/26 table+trigger g12  (x)            21
27    table   g13                       22
28/29 table+trigger g14  ('(')          23
30    table   g15                       24
31/32 table+trigger g16  (a)            25
33    table   g17                       26
34/35 table+trigger g18  (')')          27
36    table   g19                       28
37/38 table+trigger g20  (';')          29
39    table   g21                       31
40    table   x                         32     <- run 5, built by BUILD (CREATE TABLE x(a)); plain table, no gate
41/42 table+trigger g22  (hello)        33     <- run 6
43    table   g23
44/45 table+trigger g24  (world)        5      <- reused a freed page
46    table   g25
```

Mechanical check: all 14 CREATE statements in egg.sql are byte-identical to the stored `sqlite_master.sql` (only `IF NOT EXISTS` is dropped by SQLite). Everything from rowid 16 on is run-created.

---

## 2. The hop

### 2a. The line enters: trigger `input` (egg.sql:16)

```sql
CREATE TRIGGER input AFTER INSERT ON input BEGIN INSERT INTO g1(run, pos, rest, cur) VALUES (NEW.id, 0, NEW.text, ''); END;
```

The whole line becomes one g1 row: `run` = input.id, `pos` = 0 (tokens emitted so far), `rest` = the text, `cur` = ''.

### 2b. Reading characters into tokens: trigger `g1` (egg.sql:17), verbatim

```sql
CREATE TRIGGER g1 AFTER INSERT ON g1 WHEN NEW.rest IS NOT NULL BEGIN INSERT INTO g1(run, pos, rest, cur) SELECT NEW.run, NEW.pos, substr(NEW.rest, 2), NEW.cur || substr(NEW.rest, 1, 1) WHERE NEW.rest <> '' AND substr(NEW.rest, 1, 1) GLOB '[A-Za-z0-9_]'; INSERT INTO g2(run, pos, word) SELECT NEW.run, NEW.pos + 1, NEW.cur WHERE NEW.cur <> '' AND NOT (NEW.rest <> '' AND substr(NEW.rest, 1, 1) GLOB '[A-Za-z0-9_]'); INSERT INTO g2(run, pos, word) SELECT NEW.run, NEW.pos + 1 + (NEW.cur <> ''), substr(NEW.rest, 1, 1) WHERE NEW.rest <> '' AND NOT substr(NEW.rest, 1, 1) GLOB '[A-Za-z0-9_]'; INSERT INTO g1(run, pos, rest, cur) SELECT NEW.run, NEW.pos + 1 + (NEW.cur <> ''), substr(NEW.rest, 2), '' WHERE NEW.rest <> '' AND NOT substr(NEW.rest, 1, 1) GLOB '[A-Za-z0-9_]'; SELECT mother('INSERT INTO g' || (SELECT gate FROM g2 WHERE run = NEW.run AND pos = 1) || '(run, pos, arrival, remainder) VALUES (' || NEW.run || ', 1, 0, ' || coalesce((SELECT gate FROM g2 WHERE run = NEW.run AND pos = 2), 'NULL') || ')') WHERE NEW.rest = '' AND EXISTS (SELECT 1 FROM g2 WHERE run = NEW.run AND pos = 1); DELETE FROM g1 WHERE run = NEW.run AND NEW.rest = ''; END;
```

The same trigger split into its six statements, with what each does:

1. `INSERT INTO g1 … substr(NEW.rest, 2), NEW.cur || substr(NEW.rest, 1, 1) WHERE … GLOB '[A-Za-z0-9_]'` — if the next character is a word character, move it from `rest` to `cur` (one g1 row per character; `PRAGMA recursive_triggers = ON`, egg.sql:2 / bottom.py:8, makes this self-insert re-fire g1).
2. `INSERT INTO g2(run, pos, word) SELECT NEW.run, NEW.pos + 1, NEW.cur WHERE NEW.cur <> '' AND NOT (next char is a word char)` — the gathered word is complete: hear it at `pos + 1`.
3. `INSERT INTO g2(run, pos, word) SELECT NEW.run, NEW.pos + 1 + (NEW.cur <> ''), substr(NEW.rest, 1, 1) WHERE next char is NOT a word char` — every non-word character (space, `(`, `)`, `;` …) is its own token at the next pos.
4. `INSERT INTO g1 … substr(NEW.rest, 2), '' WHERE next char is NOT a word char` — continue reading after the punctuation with an empty `cur`.
5. `SELECT mother('INSERT INTO g' || (gate of the token at pos 1) || '(run, pos, arrival, remainder) VALUES (' || run || ', 1, 0, ' || coalesce(gate of the token at pos 2, 'NULL') || ')') WHERE NEW.rest = '' AND EXISTS (token at pos 1)` — **when the line is fully read, start the hop**: land on the first token's gate with `arrival = 0` and `remainder` = the second token's gate. (A bare `SELECT mother(...)` inside a trigger: the function is called for its side effect, the return value is discarded.)
6. `DELETE FROM g1 WHERE run = NEW.run AND NEW.rest = ''` — clear the reader.

Because statement 1 recurses depth-first before statements 2–4 run at the same level, and statements 2–3 run before statement 4 descends, tokens are heard left to right (confirmed by shard order in §5). Every token is heard (shards 1–29 of run 5) **before** the first landing (shard 30).

### 2c. Hearing a token: trigger `g2` (egg.sql:18), verbatim

```sql
CREATE TRIGGER g2 AFTER INSERT ON g2 WHEN NEW.word IS NOT NULL BEGIN UPDATE shards SET n = n + 1; UPDATE g2 SET shard = (SELECT n FROM shards) WHERE rowid = NEW.rowid; INSERT INTO g3(run, pos, word) SELECT NEW.run, NEW.pos, NEW.word WHERE NOT EXISTS (SELECT 1 FROM label WHERE word = NEW.word); UPDATE g2 SET gate = (SELECT gate FROM label WHERE word = NEW.word) WHERE rowid = NEW.rowid; END;
```

Take a shard number; if the word has no label yet, hand it to g3 (born, §3a) which creates the label and the gate table; then fill `g2.gate` from `label`. After this, every token of the run has a gate.

### 2d. One hop: a gate trigger plus trigger `g4` (egg.sql:20)

A landing is an INSERT into the gate's table with `(run, pos, arrival, remainder)`. Each gate's trigger (born shape, identical in every g6…g24; this is g6 from sqlite_master rowid 17):

```sql
CREATE TRIGGER g6 AFTER INSERT ON g6 BEGIN UPDATE shards SET n = n + 1; UPDATE g6 SET shard = (SELECT n FROM shards) WHERE rowid = NEW.rowid; INSERT INTO g4(run, pos, arrival, remainder) SELECT NEW.run, NEW.pos, 6, NEW.remainder WHERE NEW.remainder IS NOT NULL; END
```

It does three things: take a shard; stamp the row; **if there is a remainder, ask hop (g4)** with `arrival = 6` (its own gate number, baked in at birth) and the remainder it was handed. g5's hand-laid trigger (egg.sql:21) does the same with the literal `5` and then adds the BUILD ending (§3b).

Trigger g4 (hop), verbatim:

```sql
CREATE TRIGGER g4 AFTER INSERT ON g4 WHEN NEW.remainder IS NOT NULL BEGIN UPDATE shards SET n = n + 1; UPDATE g4 SET shard = (SELECT n FROM shards) WHERE rowid = NEW.rowid; UPDATE g4 SET said = mother('INSERT INTO g' || NEW.remainder || '(run, pos, arrival, remainder) VALUES (' || NEW.run || ', ' || (NEW.pos + 1) || ', ' || NEW.arrival || ', ' || coalesce((SELECT gate FROM g2 WHERE run = NEW.run AND pos = NEW.pos + 2), 'NULL') || ')') WHERE rowid = NEW.rowid; UPDATE input SET answer = (SELECT said FROM g4 WHERE rowid = NEW.rowid) WHERE id = NEW.run AND (SELECT said FROM g4 WHERE rowid = NEW.rowid) LIKE 'error:%'; END;
```

So, per hop:

- **fires on**: `AFTER INSERT ON g4` (the gate just landed on inserted this row), only `WHEN NEW.remainder IS NOT NULL`.
- **reads**: `NEW.remainder` (the gate to go to), `NEW.arrival` (the gate it came from), `NEW.run`, `NEW.pos`, and **one lookup in g2**: `SELECT gate FROM g2 WHERE run = NEW.run AND pos = NEW.pos + 2` — the token two ahead, which becomes the next landing's remainder.
- **writes**: through `mother()` the text `INSERT INTO g<remainder>(run, pos, arrival, remainder) VALUES (<run>, <pos+1>, <arrival>, <gate at pos+2 or NULL>)`; mother's reply (`ok` / `error: …`) into `g4.said`; and `input.answer` only if the reply starts with `error:`.
- **how the next gate is chosen**: it is not chosen at hop time — it is `NEW.remainder`, the gate number the previous landing carried, which was itself read from `g2` by position (`pos + 2`) one hop earlier, or by `pos = 2` in g1's starting call. The hop is a strict left-to-right walk over the heard tokens of this run; nothing about the gate's own content or history enters the choice.
- **nesting**: the INSERT that mother runs fires the next gate's trigger, which inserts into g4 again, which calls mother again — the whole chain is one nested call stack inside the original `INSERT INTO input`. Each mother call is a fresh top-level statement, so SQLite's trigger depth (limit 1000) does not accumulate across hops: a 979-landing chain ran on the scratch copy (3.44 s); only g1's per-character self-recursion is depth-limited (a 1010-character line is refused with `too many levels of trigger recursion`; 990 characters pass).
- **end**: when a landing arrives with `remainder = NULL` (no token at pos+2 existed), the gate trigger's `WHERE NEW.remainder IS NOT NULL` fails and nothing more happens. `input.answer` stays NULL unless g5's ending applies (§3b).

Verbatim mother text of run 6 (`hello world`) from the replay trace:

```
INSERT INTO g22(run, pos, arrival, remainder) VALUES (6, 1, 0, 6)     <- from g1, statement 5 (gate 22 = hello, 6 = ' ')
INSERT INTO g6(run, pos, arrival, remainder) VALUES (6, 2, 22, 24)    <- from g4 (gate 24 = world)
INSERT INTO g24(run, pos, arrival, remainder) VALUES (6, 3, 6, NULL)  <- from g4; remainder NULL ends the run
```

(The replay used run id 2; brain.db's rows for this line are run 6, shards 62–66 — see §5.)

---

## 3. How a new table gets built — two different mechanisms

### 3a. A new **neuron** is born by trigger `g3`, not by a run of tokens (egg.sql:19), verbatim

```sql
CREATE TRIGGER g3 AFTER INSERT ON g3 WHEN NEW.word IS NOT NULL BEGIN UPDATE shards SET n = n + 1; UPDATE g3 SET shard = (SELECT n FROM shards) WHERE rowid = NEW.rowid; INSERT INTO label(word) VALUES (NEW.word); INSERT INTO label(word) VALUES (NEW.word || '.definition'); UPDATE g3 SET said = mother('CREATE TABLE g' || (SELECT gate FROM label WHERE word = NEW.word) || '(shard INTEGER, arrival INTEGER, remainder INTEGER, trigger INTEGER, run INTEGER, pos INTEGER); CREATE TRIGGER g' || (SELECT gate FROM label WHERE word = NEW.word) || ' AFTER INSERT ON g' || (SELECT gate FROM label WHERE word = NEW.word) || ' BEGIN UPDATE shards SET n = n + 1; UPDATE g' || (SELECT gate FROM label WHERE word = NEW.word) || ' SET shard = (SELECT n FROM shards) WHERE rowid = NEW.rowid; INSERT INTO g4(run, pos, arrival, remainder) SELECT NEW.run, NEW.pos, ' || (SELECT gate FROM label WHERE word = NEW.word) || ', NEW.remainder WHERE NEW.remainder IS NOT NULL; END; CREATE TABLE g' || (SELECT gate FROM label WHERE word = NEW.word || '.definition') || '(id INTEGER PRIMARY KEY, source TEXT, entry TEXT, sense TEXT, class TEXT, text TEXT, example TEXT, origin TEXT, first_use TEXT, synonyms TEXT, antonyms TEXT, times INTEGER, first_at TEXT, last_at TEXT, ended_at TEXT); INSERT INTO g' || (SELECT gate FROM label WHERE word = NEW.word) || '(trigger) VALUES (' || (SELECT gate FROM label WHERE word = NEW.word || '.definition') || ');') WHERE rowid = NEW.rowid; UPDATE input SET answer = (SELECT said FROM g3 WHERE rowid = NEW.rowid) WHERE id = NEW.run AND (SELECT said FROM g3 WHERE rowid = NEW.rowid) LIKE 'error:%'; END;
```

Path: g2 hears an unlabeled word → inserts into g3 → g3 takes a shard, inserts the word and `word || '.definition'` into `label` (two consecutive gate numbers N, N+1), then assembles **one four-statement SQL text by string concatenation inside the trigger** and hands it to mother:

```
CREATE TABLE gN(shard INTEGER, arrival INTEGER, remainder INTEGER, trigger INTEGER, run INTEGER, pos INTEGER);
CREATE TRIGGER gN AFTER INSERT ON gN BEGIN UPDATE shards SET n = n + 1; UPDATE gN SET shard = (SELECT n FROM shards) WHERE rowid = NEW.rowid; INSERT INTO g4(run, pos, arrival, remainder) SELECT NEW.run, NEW.pos, N, NEW.remainder WHERE NEW.remainder IS NOT NULL; END;
CREATE TABLE gN+1(id INTEGER PRIMARY KEY, source TEXT, entry TEXT, sense TEXT, class TEXT, text TEXT, example TEXT, origin TEXT, first_use TEXT, synonyms TEXT, antonyms TEXT, times INTEGER, first_at TEXT, last_at TEXT, ended_at TEXT);
INSERT INTO gN(trigger) VALUES (N+1);
```

The last INSERT is the neuron's first row — its only row with `trigger` set (= its definition table's gate) and `run/pos/arrival/remainder` NULL. The new gN trigger fires on it, takes a shard, and does not hop (remainder NULL). This birth happens **during hearing**, i.e. while the line is still being read (shards 3–4 for `' '`, 6–7 for `CREATE`, in run 5), before any hop. The template text (table shape, trigger shape, definition shape) lives inside trigger g3; the only variable parts are the two gate numbers. mother's reply goes to `g3.said`; if it is an error it is also copied to `input.answer`.

Trace of the birth of `hello` (gate 22) as mother ran it, from the replay:

```
CREATE TABLE g22(shard INTEGER, arrival INTEGER, remainder INTEGER, trigger INTEGER, run INTEGER, pos INTEGER);
CREATE TRIGGER g22 AFTER INSERT ON g22 BEGIN UPDATE shards SET n = n + 1; UPDATE g22 SET shard = (SELECT n FROM shards) WHERE rowid = NEW.rowid; INSERT INTO g4(run, pos, arrival, remainder) SELECT NEW.run, NEW.pos, 22, NEW.remainder WHERE NEW.remainder IS NOT NULL; END;
CREATE TABLE g23(id INTEGER PRIMARY KEY, source TEXT, entry TEXT, sense TEXT, class TEXT, text TEXT, example TEXT, origin TEXT, first_use TEXT, synonyms TEXT, antonyms TEXT, times INTEGER, first_at TEXT, last_at TEXT, ended_at TEXT);
INSERT INTO g22(trigger) VALUES (23);
```

### 3b. A **typed** `BUILD … BUILD` line: tokens hop through their gates, then g5 pastes them into mother (egg.sql:21), verbatim

```sql
CREATE TRIGGER g5 AFTER INSERT ON g5 BEGIN UPDATE shards SET n = n + 1; UPDATE g5 SET shard = (SELECT n FROM shards) WHERE rowid = NEW.rowid; INSERT INTO g4(run, pos, arrival, remainder) SELECT NEW.run, NEW.pos, 5, NEW.remainder WHERE NEW.remainder IS NOT NULL; UPDATE input SET answer = mother((SELECT group_concat(word, '') FROM (SELECT word FROM g2 WHERE run = NEW.run AND pos > 1 AND pos < NEW.pos ORDER BY pos))) WHERE id = NEW.run AND NEW.remainder IS NULL AND (SELECT word FROM g2 WHERE run = NEW.run AND pos = 1) = 'BUILD'; END;
```

Path for `BUILD CREATE TABLE x(a); BUILD` (brain.db run 5; the replay's run 1 produced identical text):

1. read/hear: 13 tokens at pos 1–13: `BUILD`, ` `, `CREATE`, ` `, `TABLE`, ` `, `x`, `(`, `a`, `)`, `;`, ` `, `BUILD`. Eight of them are new words and are born by g3 (gates 6–21), all before the first hop.
2. g1 starts the hop: `INSERT INTO g5(run, pos, arrival, remainder) VALUES (5, 1, 0, 6)`.
3. Twelve hops, each gate trigger → g4 → mother, exactly these texts (replay trace, run id 1 there):

```
INSERT INTO g5(run, pos, arrival, remainder) VALUES (1, 1, 0, 6)
INSERT INTO g6(run, pos, arrival, remainder) VALUES (1, 2, 5, 8)
INSERT INTO g8(run, pos, arrival, remainder) VALUES (1, 3, 6, 6)
INSERT INTO g6(run, pos, arrival, remainder) VALUES (1, 4, 8, 10)
INSERT INTO g10(run, pos, arrival, remainder) VALUES (1, 5, 6, 6)
INSERT INTO g6(run, pos, arrival, remainder) VALUES (1, 6, 10, 12)
INSERT INTO g12(run, pos, arrival, remainder) VALUES (1, 7, 6, 14)
INSERT INTO g14(run, pos, arrival, remainder) VALUES (1, 8, 12, 16)
INSERT INTO g16(run, pos, arrival, remainder) VALUES (1, 9, 14, 18)
INSERT INTO g18(run, pos, arrival, remainder) VALUES (1, 10, 16, 20)
INSERT INTO g20(run, pos, arrival, remainder) VALUES (1, 11, 18, 6)
INSERT INTO g6(run, pos, arrival, remainder) VALUES (1, 12, 20, 5)
INSERT INTO g5(run, pos, arrival, remainder) VALUES (1, 13, 6, NULL)
 CREATE TABLE x(a);                                                   <- g5's last statement, through mother
```

4. The final landing on g5 has `remainder = NULL` and the token at pos 1 is `BUILD`, so g5's last statement runs: `group_concat(word, '')` over `g2` rows with `1 < pos < 13` in pos order = `' CREATE TABLE x(a); '` (leading and trailing space are the space tokens at pos 2 and 12). `mother()` runs it and its reply is written straight into `input.answer`: `ok` for run 5, `error: table x already exists` for run 7.

So: **the typed CREATE is not built by a trigger and not assembled in any cell or sheet of its own**. The gates the tokens pass through do nothing to the text (a landing row holds no word; the word stays in g2). The "sheet" is g2 itself; the assembly is a `group_concat` of the heard tokens between the two BUILD markers; mother is the one that pastes the text into SQLite. The BUILD markers are matched exactly (`= 'BUILD'`; lowercase `build` just hops and builds nothing — tested on the scratch copy). Anything SQL can be pasted this way: on the scratch copy `BUILD CREATE TABLE y(b); INSERT INTO y VALUES(1); BUILD` answered `ok` and y held `(1,)`; `BUILD SELECT 1 BUILD` answered `ok` (results discarded — mother returns only ok/error); `BUILD DROP TABLE y BUILD` answered `error: database table is locked` (the DROP runs while the trigger chain on the same connection still holds cursors open; CREATE/INSERT inside the chain are fine).

Note the two different things named `x` in brain.db: gate 12 (`label.word = 'x'`, table g12 with a trigger, born by g3) and the plain table `x(a)` at sqlite_master rowid 40 (no gate, no trigger, made by BUILD).

---

## 4. bottom.py and kernel/: every function, classified

### bottom.py (21 lines) — defines no functions; a flat loop

```python
#!/usr/bin/env python3
# bottom.py: each line typed is written into brain.db (table input); what the brain answers is printed. Ctrl-D leaves.
import os, sqlite3
here = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(here, 'brain.db'), isolation_level=None)
db.enable_load_extension(True)
db.load_extension(os.path.join(here, 'kernel', 'mother'))
db.execute('PRAGMA recursive_triggers = ON')
while True:
    try:
        line = input('> ')
    except EOFError:
        break
    try:
        run = db.execute('INSERT INTO input(text) VALUES(?)', (line,)).lastrowid
    except sqlite3.Error as e:
        print('refused:', e)
        continue
    answer = db.execute('SELECT answer FROM input WHERE id = ?', (run,)).fetchone()[0]
    if answer is not None:
        print(answer)
```

| line | statement | class |
|---|---|---|
| 3–5 | import; `here`; `sqlite3.connect(... 'brain.db', isolation_level=None)` | other: plumbing (autocommit connection; every typed line is its own transaction) |
| 6–7 | `enable_load_extension(True)`; `load_extension(.../kernel/mother)` | other: plumbing — gives the brain its `mother()` function |
| 8 | `PRAGMA recursive_triggers = ON` | other: plumbing — required for g1's self-insert to re-fire and for the nested hop; a per-connection setting, so egg.sql:2 does not carry over |
| 11–13 | `input('> ')`, break on EOF | other: terminal I/O |
| 15 | `INSERT INTO input(text) VALUES(?)` with the raw line | **this is the only write**; it is not an encoder — the text is passed untouched, the brain's g1 does the reading |
| 16–18 | catch `sqlite3.Error`, print `refused:` | other: reports a refusal (observed cause on the copy: `too many levels of trigger recursion` for a line over ~1000 characters) |
| 19–21 | `SELECT answer FROM input WHERE id = ?`; print if not NULL | other: output routing — only back to the terminal |

There is **no** encoder (text → ids) in Python, no mother (Python never assembles or runs SQL text other than the one INSERT and one SELECT), no parsing, choosing, templating, and no writing of any brain table other than `input.text`. The brain's reply goes only to the terminal; nothing routes it to sources or back in.

### kernel/mother.c (18 lines) — one function, the "mother"

```c
/* mother(sql): the brain hands SQL text to the mother. She runs it and answers
   'ok' or 'error: ...'. She never stops the brain, so a refusal can be felt and remembered. */
static void motherFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const char *sql = (const char*)sqlite3_value_text(argv[0]);
  char *err = 0;
  if(!sql){ sqlite3_result_text(ctx, "error: nothing to run", -1, SQLITE_STATIC); return; }
  if(sqlite3_exec(sqlite3_context_db_handle(ctx), sql, 0, 0, &err) != SQLITE_OK){
    char *msg = sqlite3_mprintf("error: %s", err ? err : "unknown");
    sqlite3_result_text(ctx, msg, -1, sqlite3_free); sqlite3_free(err); return;
  }
  sqlite3_result_text(ctx, "ok", -1, SQLITE_STATIC);
}
int sqlite3_mother_init(sqlite3 *db, char **e, const sqlite3_api_routines *pApi){
  SQLITE_EXTENSION_INIT2(pApi);
  return sqlite3_create_function(db, "mother", 1, SQLITE_UTF8, 0, motherFunc, 0, 0);
}
```

- `motherFunc` (mother.c:5–14): **mother**. Takes one text argument, runs it as SQL on the same connection with `sqlite3_exec` (multi-statement allowed; any result rows are discarded), returns `'ok'`, or `'error: <sqlite message>'`, or `'error: nothing to run'` for NULL. It never raises, so the calling trigger continues and the error text can be stored (g3.said, g4.said, input.answer). It decides nothing and does not parse: the SQL text is composed entirely by the triggers.
- `sqlite3_mother_init` (mother.c:15–18): registers the SQL function `mother(1 arg)`. Exported symbol confirmed with `nm -D`.

### kernel/eval.c (125 lines) — stock SQLite extension, unused

- `callback` (eval.c:34–63): accumulates result-row text with a separator.
- `sqlEvalFunc` (eval.c:71–102): `eval(X)` / `eval(X, sep)` — runs SQL text and **returns the result rows as text**; on error it raises an SQL error (unlike mother).
- `sqlite3_eval_init` (eval.c:108–125): registers `eval`.
- Not loaded anywhere (egg.sql:1 and bottom.py:7 load only mother; `grep eval` finds nothing). It would be the "mother that answers with rows" if a later build needed one; v1 does not use it.

---

## 5. What brain.db (copy) actually contains

Row counts: `input 7, shards 1 (n=104), label 25, g1 0, g2 29, g3 10, g4 26, g5 4, g6 10, g8 3, g10 3, g12 3, g14 3, g16 3, g18 3, g20 3, g22 2, g24 2, x 0`; every `.definition` table (g7 g9 g11 g13 g15 g17 g19 g21 g23 g25) 0.

### input (the only log of prompts and answers; times are UTC, box is CDT = UTC-5)

```
id  text                             time (UTC)           answer
1   insert table                     2026-10-19 21:07:07  NULL
2   BUILD CREATE TABLE x(a); BUILD   2026-10-20 00:00:44  ok
3   hello world                      2026-10-20 00:00:44  NULL
4   BUILD CREATE TABLE x(a); BUILD   2026-10-20 00:00:44  error: table x already exists
5   BUILD CREATE TABLE x(a); BUILD   2026-10-20 00:41:51  ok
6   hello world                      2026-10-20 00:41:51  NULL
7   BUILD CREATE TABLE x(a); BUILD   2026-10-20 00:41:51  error: table x already exists
```

Runs 1–4 have **no** rows in g2/g3/g4/g5 and their words (`insert`, `table`) are not in `label`: they were run against an earlier laying (00:00:44 UTC = 19:00:44 CDT, the minute bottom.py and mother.so were written). egg.sql drops `label`, `shards` and the `input` trigger but keeps `input` (`IF NOT EXISTS`), so the prompts survived while everything else was re-laid at 19:41:51 CDT (egg.sql and brain.db mtimes) and runs 5–7 were fed within the same second — the brain in the file is exactly the product of egg.sql plus those three lines (replay in §0 reproduces it).

### label (25 gates)

```
1 read  2 hear  3 born  4 hop  5 BUILD            <- egg.sql:10
6 ' '   7 ' .definition'   8 CREATE  9 CREATE.definition  10 TABLE  11 TABLE.definition
12 x    13 x.definition   14 (      15 (.definition      16 a      17 a.definition
18 )    19 ).definition   20 ;      21 ;.definition                       <- run 5
22 hello 23 hello.definition  24 world 25 world.definition                <- run 6
```

### Three neurons as examples (all rows)

g6 = `' '` (space). Row 1 is its DNA/birth row; the rest are landings:

```
rowid shard arrival remainder trigger run pos
1     4     NULL    NULL      7       NULL NULL   <- born: trigger = 7 = gate of ' .definition'
2     32    5       8         NULL    5    2      <- run 5: came from BUILD(5), going to CREATE(8)
3     36    8       10        NULL    5    4
4     40    10      12        NULL    5    6
5     52    20      5         NULL    5    12     <- going to the closing BUILD
6     64    22      24        NULL    6    2      <- run 6: hello -> world
7     82    5       8         NULL    7    2
8     86    8       10        NULL    7    4
9     90    10      12        NULL    7    6
10    102   20      5         NULL    7    12
```

g8 = `CREATE`:

```
1  7    NULL NULL  9    NULL NULL   <- born; trigger 9 = CREATE.definition
2  34   6    6     NULL 5    3      <- landed from ' ' going to ' '
3  84   6    6     NULL 7    3
```

g22 = `hello` and g24 = `world`:

```
g22: 1  57  NULL NULL 23 NULL NULL | 2  62  0  6    NULL 6 1   (arrival 0 = first landing of the run)
g24: 1  61  NULL NULL 25 NULL NULL | 2  66  6  NULL NULL 6 3   (remainder NULL = end of the run)
```

A neuron's "DNA" in v1 is therefore exactly one row: `trigger = <gate of its .definition table>`, everything else NULL; the definition table it points to is empty. Nothing else is stored about a word except its `label` row and the gate trigger with its own number baked in.

### Firing order of run 5 reconstructed from shard numbers (every row in the db, sorted by shard)

```
 1 g2 pos1 'BUILD'        | 2 g2 pos2 ' '   3 g3 ' ' ok   4 g6 born(trigger 7)
 5 g2 pos3 'CREATE'  6 g3 ok  7 g8 born(9) | 8 g2 pos4 ' ' | 9 g2 pos5 'TABLE' 10 g3 ok 11 g10 born(11)
12 g2 ' ' | 13 g2 'x' 14 g3 15 g12 born(13) | 16 g2 '(' 17 g3 18 g14 born(15) | 19 g2 'a' 20 g3 21 g16 born(17)
22 g2 ')' 23 g3 24 g18 born(19) | 25 g2 ';' 26 g3 27 g20 born(21) | 28 g2 pos12 ' ' | 29 g2 pos13 'BUILD'
30 g5 land pos1 arr0 rem6 | 31 g4 arr5 rem6 ok | 32 g6 pos2 arr5 rem8 | 33 g4 | 34 g8 pos3 | 35 g4 | 36 g6 pos4 | 37 g4
38 g10 pos5 | 39 g4 | 40 g6 pos6 | 41 g4 | 42 g12 pos7 | 43 g4 | 44 g14 pos8 | 45 g4 | 46 g16 pos9 | 47 g4
48 g18 pos10 | 49 g4 | 50 g20 pos11 | 51 g4 | 52 g6 pos12 rem5 | 53 g4 arr6 rem5 ok | 54 g5 land pos13 arr6 remNULL -> mother(' CREATE TABLE x(a); ') -> input.answer='ok'
```

Run 6 = shards 55–66 (hello born 56–57, world born 60–61, hops 62–66). Run 7 = shards 67–104 (no births; 13 landings + 12 hops; the final paste answers `error: table x already exists`). The g4 rows carry `said = 'ok'` for all 26 hops; the g3 rows carry `said = 'ok'` for all 10 births.

Evidence of the typed CREATE: sqlite_master rowid 40 `CREATE TABLE x(a)` sits between the birth of `;` (rowid 39, g21) and the birth of `hello` (rowid 41, g22), i.e. it was created at the end of run 5 and before run 6, which matches `input.answer` for ids 5 and 7. There is no separate receipt table or assembled-text cell: the only places the BUILD text ever exists are `input.text` (typed), the `g2.word` tokens, and the transient argument to `mother()`.

### Observed limits on the scratch copy (not in brain.db)

- A single word of 990 characters reads fine; 1010 characters is refused (`too many levels of trigger recursion`, `.limit trigger_depth` = 1000): g1 recurses once per character.
- Hop chains are not depth-limited (979 landings ran) but time grows faster than linear: 299 landings 0.30 s, 659 → 1.60 s, 979 → 3.44 s (g4's `g2` lookup by `run, pos` has no index; each nesting level keeps its cursors open).
- An empty line hears 0 tokens and does not hop; a line of three spaces hears 3 tokens and hops through g6 three times.

---

## 6. The division between inside and outside

Inside the brain (SQLite file + the 6 hand-laid triggers + one born trigger per word) is everything that reads, hears, births, hops and builds: g1 reads the text character by character and emits tokens; g2 looks each token up in `label` and sends unknown ones to g3; g3 assigns the next two gate numbers, composes the CREATE TABLE/CREATE TRIGGER/CREATE TABLE/INSERT text for the new neuron by string concatenation and hands it to `mother()`; g1 then starts the walk and g4 carries it from gate to gate, each step a new `INSERT INTO g<next>` text handed to `mother()`, the next-next gate read from `g2` by position; g5 ends a `BUILD … BUILD` run by `group_concat`-ing the heard tokens and handing that text to `mother()`, whose `ok`/`error:` reply is written into `input.answer`. `mother()` is a 14-line C function registered into the same connection; it runs whatever text it is handed on that connection and reports ok or the error, deciding and parsing nothing. Outside the brain is bottom.py, which does only four things: open brain.db in autocommit, load `mother`, set `recursive_triggers`, and loop — insert the raw typed line into `input.text`, then read `input.answer` for that id and print it if not NULL. Python holds no encoder, no tokenizer, no walker, no templates, no table writes other than that one INSERT, and routes the answer nowhere but the terminal; the `eval` extension (which would return result rows) is compiled but never loaded. Every choice in v1 — what is a token, which gate a word is, which gate comes next, what SQL to run — is made by trigger SQL reading brain tables, with position (`g2.pos`, `pos + 2`) as the only ordering device and the global `shards.n` counter as the only clock.
