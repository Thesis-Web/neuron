# Forensic trace: Point Of Connection 17.3 (read-only, 2026-10-25)

Files traced (nothing modified):

- `HTML` = /mnt/c/Users/AdLibitumVita/Downloads/NEURON-POINT-OF-CONNECTION-v17.3-2026-10-25.html (6203 lines)
- `SQL`  = /mnt/c/Users/AdLibitumVita/Downloads/NEURON-v17.2-TOLD-BLOCK-2026-10-25.sql (1042 lines, 633 statements)
- `PY`   = /mnt/c/Users/AdLibitumVita/Downloads/NEURON-PROMPT-2026-10-25/host15.py (85 lines)
- `NP`   = /mnt/c/Users/AdLibitumVita/Downloads/NEURON-PROMPT-2026-10-25/neuron_prompt.py (30 lines)
- `SHEET`= /mnt/c/Users/AdLibitumVita/Downloads/NEURON-PROMPT-2026-10-25/sheet173.json (181 lines)

Extracted copies (line numbers inside each copy are prefixed with the ORIGINAL html line number):
/tmp/claude-1000/-home-exnulla-neuron-v1/95237a7f-7d7c-47a3-a249-06f9202b6633/scratchpad/traceA/{head_1-466.txt, engine_467-565.txt, engine_577-804.txt, worker_805-947.txt, main_951-6203.txt, line950_TOLD.js}

## 0. Map of the HTML file

| HTML lines | what |
|---|---|
| 1-466 | HTML + CSS + the page's prose (rails, notes, "mother, all of her" code listing at 374-427) |
| 467-804 | `<script type="text/plain" id="engine-src">`: sql.js (lines 480-684, incl. the 2.4 MB asm/wasm blob on lines 566-576) followed by the hand-written **host** at 686-804 (`// HOST-START` ... `// HOST-END`, then `reopenBrain`/`exportBrain`/`restoreBrain` 788-803) |
| 805-947 | `<script type="text/plain" id="worker-src">`: the Web Worker (hand-written) |
| 948 | three.js from cdnjs |
| 949-6203 | main `<script>`: line 950 is one 2.27 MB line `var TOLD = {...}, SAT = {...}, SLICE = {...}, READINGS = null, MAP = {...}, LAB = {` ; 951-5166 LAB data; 5167-5348 `SHEET = [...]` (= sheet173.json); **5349-6201 the page IIFE (hand-written)** |

`TOLD` on HTML:950 is byte-identical to NEURON-PROMPT-2026-10-25/physics172.json (114,422 chars). Its 410 `statements` are every statement of the .sql file (0 misses). Its other keys: `physics` (16 names), `actions` (14), `sqlroots` (40), `arrivals` (heard, said, start), `ports` ("output to sources", "secondary input", "OUTPUT", "mother", "SQL prompt"), `sats` (wn gcide mw mwt moby map sqldoc measured).

The engine-src is loaded in two places: as a Blob Worker (HTML:5363 `new Worker(URL.createObjectURL(new Blob([$('engine-src').textContent + '\n' + $('worker-src').textContent]...` ) and, when a line nests too deep, on the main thread via `(0, eval)($('engine-src').textContent)` (HTML:5417).

---

## 1. A word with no neuron: who creates its table, view and trigger

Path, typed line to CREATE executed:

1. Page: `typeLine()` HTML:5704 → `send([v])` HTML:5703 → `worker.postMessage({ type: 'lines', lines })`.
2. Worker: HTML:896 `o = brain.type(l);`
3. Host "bottom": HTML:772-777 (`PY`:79-83 identical)
   ```js
   Brain.prototype.type = function (line, direction) {
     var before = this.q("SELECT coalesce(max(id), 0) FROM output")[0][0];
     this.db.run("INSERT INTO input (line, direction) VALUES (?, ?)", [line, direction || 'heard']);
     var r = this.q("SELECT text FROM output WHERE id > ? ORDER BY id DESC LIMIT 1", [before]);
   ```
4. SQL:741 `CREATE TRIGGER input_run AFTER INSERT ON input WHEN NOT (... ' = ' ... '=>' ...) AND NOT (... ' -> ' ...) BEGIN INSERT INTO run (...)`
5. SQL:750 `CREATE TRIGGER run_go AFTER INSERT ON run BEGIN ... INSERT INTO encode (run, text) VALUES (NEW.id, NEW.line); END;` (SQL:760)
6. SQL:767-773 `encode_word` peels the first word off `NEW.text` with `substr(trim(NEW.text) || ' ', 1, instr(trim(NEW.text) || ' ', ' ') - 1)` and:
   ```sql
   INSERT INTO born (word, run, why) SELECT substr(...), NEW.run, CASE ... END
     WHERE NOT EXISTS (SELECT 1 FROM encoder WHERE word = substr(...));
   ```
   then re-inserts the remainder into `encode` (recursion; `PRAGMA recursive_triggers = ON` SQL:1).
7. SQL:781-789 `born_go AFTER INSERT ON born`:
   ```sql
   INSERT INTO encoder (word, role, born) VALUES (NEW.word, CASE WHEN NEW.word LIKE ':%' THEN 'var' WHEN NEW.word GLOB '[0-9]*' OR NEW.word LIKE '''%' OR NEW.word LIKE '%''' THEN 'literal' ELSE 'word' END, ...);
   SELECT mother('CREATE TABLE g' || (SELECT gate FROM encoder WHERE word = NEW.word) || ' (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER)', NULL, NULL);
   SELECT mother('CREATE VIEW land_' || (SELECT gate FROM encoder WHERE word = NEW.word) || ' AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g' || (SELECT gate FROM encoder WHERE word = NEW.word), NULL, NULL);
   SELECT mother('CREATE TRIGGER miss_' || ... || ' INSTEAD OF INSERT ON land_' || ... || ' WHEN NOT EXISTS (SELECT 1 FROM g' || ... || ' WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (' || ... || ', NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END', NULL, NULL);
   INSERT INTO definition (word, src) VALUES (NEW.word, 'node');
   INSERT INTO event (...) VALUES ('born', NEW.word, NEW.run, 'mother', 'born ' || NEW.word || ' (gate ' || ... || '): mother makes its table, its gate and its trigger, and a blank definition node' ...
   ```
8. `mother` is a SQL scalar function registered by the host, not a table or trigger: HTML:696 `db.create_function('mother', function (text, run, stmt) { return self.mother(text, run, stmt); });` (`PY`:10 `self.con.create_function('mother', 3, self.mother)`). Its body HTML:720-769 / PY:30-76. With `run === null` (as above) it does:
   ```js
   st = free.length ? free.pop() : db.prepare(text);      // HTML:729
   cols = st.getColumnNames(); while (st.step()) rows.push(st.get());
   ...
   if (run === null) { if (err) throw new Error(err); return rows.length && rows[0].length ? rows[0][0] : lastid; }   // HTML:740-743
   ```
   PY:39 `cur = con.execute(text)`; PY:47-50 same return rule.

Verdict for Q1:

- The CREATE TABLE / CREATE VIEW / CREATE TRIGGER text is **composed inside a hand-laid SQL trigger (`born_go`, SQL:783-785) by string-concatenation templates** (`'CREATE TABLE g' || gate || ' (shard INTEGER PRIMARY KEY, ...)'`). It is **not** assembled by the neurons through gates filling a run sheet, and it is not composed in JS/Python.
- It is **executed by the host's JS/Python function `mother`** (`db.prepare(text)`/`con.execute(text)`), called from inside the trigger as `SELECT mother(...)`. No run, receipt, stmt row, var cell or run sheet is involved: `stmt`/`secondary` are bypassed because `run` is NULL (HTML:740 "a by-value step of the physics itself (a birth, a lay, a landing)").
- Same template mechanism for the per-row hop triggers: SQL:822-823 `lay_go` does `UPDATE lay SET shard = mother('INSERT INTO g' || NEW.gate || ' (arrival, remainder, trigger, times, first, last) VALUES (...)', NULL, NULL)` and `SELECT mother('CREATE TRIGGER hop_' || NEW.gate || '_' || shard || ' INSTEAD OF INSERT ON land_' || NEW.gate || ' WHEN NEW.arrival = ... BEGIN UPDATE g...; INSERT INTO receipt ...; INSERT INTO event (''hit'' ...); [INSERT INTO stmt ...]; INSERT INTO fire ...; [INSERT INTO "end" | INSERT INTO land_<remainder> ...]; END', NULL, NULL)`. The hop trigger body (~1,800 chars) is one template literal inside `lay_go`.
- The only path where SQL text that the **run** assembled is pasted is the `;` gate's hop trigger (SQL:823): `INSERT INTO stmt (run, text) SELECT NEW.run, (SELECT group_concat(w, ' ') FROM (SELECT CASE WHEN e.role = 'var' THEN quote(coalesce((SELECT value FROM var WHERE run = NEW.run AND name = e.word ...), (... parent ...), (... root ...))) ELSE e.word END AS w FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run AND r.id >= (... first SELECT/INSERT/UPDATE/DELETE/CREATE/WITH after the last ';' ...) ORDER BY r.id)) WHERE kind = 'formula'` → SQL:863-866 `stmt_go ... SELECT mother(NEW.text, NEW.run, NEW.id);`. That is the "run sheet" path. Births, lays, landings, bind lookups and step-back do not use it.

---

## 2. Every SQL execution site in the page's own JS and in host15.py

Legend: (a) loading the told block; (b) pasting text the brain assembled; (c) host-written SQL reading brain tables; (d) host-written SQL writing tables; (s) satellite ("source brain") databases the host builds; (L) the page's lab database (not the brain).

### 2.1 engine-src host (HTML:686-804)

| HTML line | call | class | note |
|---|---|---|---|
| 696 | `db.create_function('mother', ...)` | — | registers mother |
| 697 | `db.create_function('satwork', function (sat, ask, word, n) { self.populated.push([sat, ask, word, n]); return 1; })` | — | the "outbox is populated" signal is a JS array push |
| 701 | `db.run("ATTACH ':memory:' AS " + s)` | (s) | one attached db per source |
| 702-705 | `db.run("CREATE TABLE " + s + ".corpus ...; CREATE INDEX ...; CREATE TABLE " + s + ".inbox ...; CREATE TABLE " + s + ".outbox ...; CREATE TRIGGER " + s + ".work AFTER INSERT ON inbox BEGIN INSERT INTO outbox SELECT ...; SELECT satwork(...); DELETE FROM inbox WHERE ask = NEW.ask; END;")` | (s)(d) | host writes the source brains' schema and their one trigger |
| 706-707 | `db.prepare("INSERT INTO " + s + ".corpus VALUES (?, ?, ?, ?)")` / `st.run([...])` | (s)(d) | loads SAT data |
| 712 | `told.statements.forEach(function (st) { db.run(st); })` | (a) | told block |
| 715 | `ev()`: `db.run("INSERT INTO event (kind, gate, run, rowgate, text, roots) VALUES (?, ?, ?, ?, ?, ?)", ...)` | (d) | host writes narration rows into `event` |
| 729 | `st = free.length ? free.pop() : db.prepare(text);` + `st.step()` | **(b)** | `text` = 1st arg of `mother(...)`. Sources: `born_go` SQL:783-785 (CREATE templates), `decide_go` SQL:798 (`INSERT INTO land_N ... FROM envelope`), `memwrong_go` SQL:816 (`INSERT INTO g3 ...`), `lay_go` SQL:822 (`INSERT INTO gN ...`), SQL:823 (`CREATE TRIGGER hop_...`), SQL:826 (`INSERT INTO land_N`), `bindrow_go` SQL:843 (`SELECT shard FROM gN ...`), SQL:844 (`UPDATE gN SET trigger = ...`), `end_branch` SQL:965 (`SELECT trigger FROM gN ... LIMIT 1`), and `stmt_go` SQL:865 `mother(NEW.text, NEW.run, NEW.id)` where `stmt.text` came from the `;` hop trigger (SQL:823, receipt+encoder+var) or from `"BUILD".text` (SQL:1026 ← `end_line` SQL:994 `trim(substr(line, 7, length(line) - 12))` ← the typed line) |
| 733 | `db.getRowsModified()`; `db.exec('SELECT last_insert_rowid()')` | (c) | |
| 749 | `db.run("INSERT INTO secondary (run, stmt, src, value, cols, n, err, changes, last) VALUES (?, ?, 'sql', ?, ?, ?, ?, ?, 1)", ...)` | (d) | |
| 755 | `db.run("INSERT INTO secondary (run, stmt, src, err, n, last) VALUES (?, ?, ?, ?, 0, 1)", ...)` | (d) | refusal row |
| 756 | `db.run("INSERT INTO secondary (run, stmt, src, waiting, last) VALUES (?, ?, ?, 1, 1)", ...)` | (d) | waiting row |
| 761 | `db.prepare("SELECT word, hw, text, words FROM " + s + ".outbox WHERE ask = ?")` | (c)(s) | |
| 762 | `db.run("DELETE FROM " + s + ".outbox WHERE ask = ?", [ask])` | (d)(s) | |
| 764 | `db.run("INSERT INTO secondary (run, stmt, src, word, hw, value, words, last) VALUES (?, ?, ?, ?, ?, ?, ?, 0)", ...)` | (d) | one row per reply row |
| 765 | `db.run("INSERT INTO secondary (run, stmt, src, word, n, last) VALUES (?, ?, ?, ?, ?, 1)", ...)` | (d) | the "last" marker row the brain's triggers key on |
| 773 | `this.q("SELECT coalesce(max(id), 0) FROM output")` | (c) | |
| 774 | `this.db.run("INSERT INTO input (line, direction) VALUES (?, ?)", [line, direction || 'heard'])` | (d) | the bottom |
| 775 | `this.q("SELECT text FROM output WHERE id > ? ORDER BY id DESC LIMIT 1", [before])` | (c) | |
| 779 | `Brain.prototype.q`: `this.db.prepare(sql)` | (c) | generic read, used by the worker |
| 790-791 | `reopenBrain`: `create_function('mother'...)`, `create_function('satwork'...)` | — | after `export()` |
| 792 | `db.run('PRAGMA recursive_triggers = ON')` | (d) | re-set after export |
| 794-799 | ATTACH / CREATE satellites / INSERT corpus again | (s)(d) | same as 701-707 |
| 802 | `exportBrain`: `b.db.export()` then `reopenBrain` | — | snapshot after every line |
| 803 | `restoreBrain`: `new SQL.Database(bytes)` + `reopenBrain` | — | |

### 2.2 worker-src (HTML:805-947)

| HTML line | call | class |
|---|---|---|
| 816-829 | `bundle()`: SELECTs on event, encoder, formula+receipt+encoder (formula body "read back"), defword, proc, run, var LEFT JOIN sense (`WHERE v.name NOT IN (':head', ':line', ':run', ':prev', ':speaker') OR v.value IS NOT NULL`), gap, sense GROUP BY src, `need ... LIMIT 30`, definition, sqlite_master (trigger count, `g[0-9]*` table count) | (c) |
| 836 | `SELECT kind, gate, roots, rowgate FROM event WHERE id > ?` | (c) |
| 846 | `SELECT cols FROM secondary WHERE src = 'sql' AND last = 1 ORDER BY id DESC LIMIT 1` | (c) |
| 853-854 | `A.type(line)`, `B.type(without)` on **restored snapshot copies** | (d) on copies: host re-runs a line with a word removed |
| 858-879 | SELECTs on run, input, memory, formula+receipt, `definition ... LIMIT 8` | (c) |
| 896 | `brain.type(l)` | (d) input |
| 909 | `brain.type(d.line, 'said')` | (d) input, direction said (page never sends 'said') |
| 915 | `rows(brain, d.sql, d.params)` | (c) arbitrary SQL from the page ('query' messages) |
| 922-929 | atlas: encoder, sqlite_master, `SELECT ... FROM g<gate>`, triggers' `sql`, memory, formula, state, event | (c) |
| 937-938 | `LABDB.prepare(o[0])`/`st.run(p)`; `LABDB.exec(o[0], o[1])` | (L) lab database only |

### 2.3 page IIFE (HTML:5349-6201)

No direct database calls; everything goes through worker messages: `init` 5413, `lines` 5703, `adopt` 5404, `restart` 5722, `query` 5770/5990/6084/6130/6162, `atlas` 5927, `measure` 5790, `lab` 5986/5995/6000/6132. On a 'deep' failure the page itself runs the brain: HTML:5401-5404 `b = restoreBrain(SQL, TOLD, SAT, d.bytes)... out = b.type(d.line); bytes = exportBrain(b, SAT); ... worker.postMessage({ type: 'adopt', bytes ... })`. `window.__poc.rawRows(sql)` HTML:6162 forwards **any** SQL (writes included) to the brain via 'query'.

### 2.4 host15.py

| PY line | call | class |
|---|---|---|
| 10-11 | `create_function('mother', 3, self.mother)`, `create_function('satwork', 4, lambda ...: self.populated.append(...) or 1)` | — |
| 16 | `con.execute(f"ATTACH ':memory:' AS {s}")` | (s) |
| 17-20 | `con.executescript(f"""CREATE TABLE {s}.corpus ...; CREATE INDEX ...; CREATE TABLE {s}.inbox ...; CREATE TABLE {s}.outbox ...; CREATE TRIGGER {s}.work AFTER INSERT ON inbox BEGIN ... SELECT satwork(...); DELETE FROM inbox ...; END;""")` | (s)(d) |
| 22 | `con.executemany(f"INSERT INTO {s}.corpus VALUES (?, ?, ?, ?)", ...)` | (s)(d) |
| 24-25 | `for st in told['statements']: self.con.execute(st)` | (a) |
| 34 | `INSERT INTO event (...) VALUES ('mother', 'mother', ?, 'mother', ?, 'CALL MOVE')` | (d) |
| 39 | `cur = con.execute(text)` | **(b)** same sources as HTML:729 |
| 52 | `INSERT INTO event ... ('sql', 'SQL prompt', ?, 'SQL prompt', ?, '')` | (d) |
| 53 | `INSERT INTO event ... ('mother', 'mother', ?, 'mother', 'mother carries the reply back', 'CALL MOVE')` | (d) |
| 55 | `INSERT INTO secondary (run, stmt, src, value, cols, n, err, changes, last) VALUES (?, ?, 'sql', ...)` | (d) |
| 62 | `INSERT INTO secondary (run, stmt, src, err, n, last) VALUES (?, ?, ?, ?, 0, 1)` | (d) |
| 65 | `INSERT INTO secondary (run, stmt, src, waiting, last) VALUES (?, ?, ?, 1, 1)` | (d) |
| 68-69 | `INSERT INTO event ... ('mailbox' ...)`, `('populated' ...)` | (d) |
| 70 | `SELECT word, hw, text, words FROM {s}.outbox WHERE ask = ?` | (c)(s) |
| 71 | `DELETE FROM {s}.outbox WHERE ask = ?` | (d)(s) |
| 72 | `INSERT INTO event ... ('pickup', 'mother' ...)` | (d) |
| 74-75 | `INSERT INTO secondary (... last) VALUES (..., 0)` per row; `(..., 1)` marker | (d) |
| 80, 82 | `SELECT coalesce(max(id), 0) FROM output`; `SELECT text FROM output WHERE id > ? ORDER BY id DESC LIMIT 1` | (c) |
| 81 | `INSERT INTO input (line, direction) VALUES (?, ?)` | (d) |
| 85 | `q()`: `con.execute(sql, params).fetchall()` | (c) |
| NP:11, 14 | `src.backup(b.con, name='main')`, `b.con.backup(dst, name='main')` | load/save brain.db |

### 2.5 (d) summary: every table the host writes

Brain (main schema):
- `input` (HTML:774; PY:81) — the typed line
- `event` (HTML:715 via `ev()` at 723, 746, 747, 759, 760, 763; PY:34, 52, 53, 68, 69, 72) — 6 kinds of narration rows: 'mother', 'sql', 'mailbox', 'populated', 'pickup'
- `secondary` (HTML:749, 755, 756, 764, 765; PY:55, 62, 65, 74, 75)
- via `mother` executing trigger-composed text (HTML:729; PY:39): `g<N>` tables (CREATE, INSERT, UPDATE), `land_<N>` views (CREATE, INSERT-through-view), `miss_<N>` and `hop_<N>_<shard>` triggers (CREATE), `g3` (INSERT, from memwrong_go)
- via `mother` executing run-assembled `stmt.text`: whatever the formula says (`var`, `source`, `say`, `input`, `place`, `relation`, `formula`, `bindrow`, `state`, `memory` UPDATE, `<sat>.inbox` — see SHEET), and whatever a `BUILD ... BUILD` line says (e.g. `CREATE TABLE things`, HTML:5718)
- `PRAGMA recursive_triggers` after export (HTML:792)

Attached source databases (host-built stand-ins), per sat in wn, gcide, mw, mwt, moby, map, sqldoc, measured:
- `<sat>.corpus` (+ index `cw`), `<sat>.inbox`, `<sat>.outbox` schema and trigger `<sat>.work` (HTML:701-705, 794-799; PY:16-20)
- `<sat>.corpus` rows (HTML:706-707, 799; PY:22)
- `<sat>.outbox` DELETE (HTML:762; PY:71)

Page-owned lab database (`LABDB`, worker HTML:935-938; schema at HTML:5978-5981): `point`, `effect`, `line`, `axis`, `added`, `place`, view `own` — written at HTML:5982-5984, 5993-5994, 6000.

Snapshot copies: `contrast()` HTML:853-854 types lines into restored copies (`A.type(line)`, `B.type(without)`).

---

## 3. Decisions and rules made outside the brain (host JS / py), with citations

Count: 41 items.

Engine host / mother (HTML:686-804; PY:1-85):

1. **Route by regex over the SQL text**: HTML:722 `(text.match(/\b(\w+)\.inbox\b/g) || []).forEach(...)` ; PY:32 `re.findall(r'\b(\w+)\.inbox\b', text)`. A statement is "addressed to a source" iff the host's regex finds `<sat>.inbox` in it.
2. **Two modes by `run` nullness**: HTML:740 `if (run === null) { ... return rows[0][0] : lastid }` vs the statement path; PY:47-50. The host decides whether a result is "a by-value step of the physics" or "secondary input".
3. **Return-value rule**: first column of first row, else `last_insert_rowid()` (HTML:733, 743, 750; PY:43, 50, 57). This value becomes `lay.shard` (SQL:822), `bindrow.found` (SQL:843), `stepq.alt` (SQL:965).
4. **Reply formatting**: HTML:748 `rows.map(r => r.map(v => v === null ? '' : String(v)).join(' ')).join(' | ')`; PY:54. The host joins a result set into one string that the brain later says.
5. **Error classification**: HTML:737 `if (e instanceof RangeError || !e.message || /call stack|recursion/i.test(err)) throw e;` else the error becomes a "refusal" row; PY:49 raises for by-value steps.
6. **Refused / waiting / delivered per satellite**: HTML:755-756 `if (err) {...secondary err...}; if (!got.length) {...waiting = 1...}`; PY:60-66.
7. **Narration written into `event`** by the host: HTML:723 `'mother carries it ' + (addressed.length ? 'into the inbox of ' + addressed.join(', ') : 'to the SQL prompt')`; 746 `'the SQL prompt ' + (err ? 'refuses it: ' + err : 'runs it')`; 747 `'mother carries the reply back'`; 759 `s + ': the ask for "' + word + '" lands in its inbox; its own trigger does its work at once'`; 760 `s + ': its outbox is populated with ' + n + ' row(s), and it says so'`; 763 `'mother picks up ' + out.length + ' row(s) from ' + s + ' and empties that outbox'`. PY:34-35, 52-53, 68-69, 72 identical. The root labels `'CALL MOVE'`, `'FIND READ WRITE'`, `'WRITE'`, `'MOVE CALL'` are assigned by the host too.
8. **The `secondary` marker protocol** (`last` = 0 per row, 1 for the summary row; `n`, `cols`, `changes`, `waiting`, `err`): HTML:749, 755, 756, 764, 765; PY:55, 62, 65, 74, 75. The brain's `secondary_*` triggers (SQL:868-892) fire on these host-chosen marks.
9. **The source brains are host-built**: schema + trigger `work` in HTML:702-705 / PY:17-20; the "says when its outbox is populated" is `satwork` pushing into a JS array `this.populated` (HTML:697, 724, 739, 753; PY:11, 36, 46, 59). Mother "picks up" from that array, not from anything the brain holds.
10. **Statement cache** (pool per text, max 4 free statements): HTML:727-732.
11. **`type()`**: default direction `'heard'` (HTML:774; PY:81); the answer is "the newest `output` row with id > before" (HTML:775; PY:82).
12. `restoreBrain` rebuilds satellites and re-registers mother on every snapshot restore (HTML:788-803).

Worker (HTML:805-947):

13. Snapshot after every line; `KEEP = 24` (HTML:808-810, 904) — the host's export of the whole db.
14. **Failure handling**: on exception, restore from snapshot and classify `deep` (regex `/call stack|recursion/i` or empty message) vs `failed` (HTML:895-901); the page then re-runs the line on the main thread (HTML:5397-5407) and the worker adopts the bytes (HTML:912-917).
15. `bundle()` decides what the page sees: filters `var` names (`NOT IN (':head', ':line', ':run', ':prev', ':speaker') OR v.value IS NOT NULL`, HTML:823), `need ... LIMIT 30` (826), formula body reconstructed by `group_concat` over receipt (819).
16. `ledger()`: `KINDS_GRAPH` maps event kinds to display buckets (HTML:833-844); `Q[e[1]]` counts "questions" from `input` events with `run === null`.
17. **Meaning measurement is a host experiment**: `contrast()` HTML:847-856 strips `=>` with `/\s*=>.*$/`, removes every token equal to the word, runs both variants on restored snapshots, diffs ledgers. `meaningOf()` HTML:857-881: skips bind/teach lines by regex (`/\s->\s/`, `/^\S+\s=\s(?!>)/`, 862); for recalled runs adds by hand `['FIND', 'COMPARE', 'WRITE'].forEach(k => rec.silicon[k] += 1); rec.graph['memory recalls'] += 1` (871); computes ratios (878); `definition ... LIMIT 8` (880).
18. `lastBuildCols` reads `secondary.cols` for BUILD lines (846, 853-854).
19. `atlas` message reads `sqlite_master` and every `g<gate>` table (921-930).
20. `lab` message: a second SQLite db (`LABDB`) built and written by the page (935-938).

Page IIFE (HTML:5349-6201):

21. `absorb()` maps event kinds to graph features and **renames relation words**: `REL_OF = { like: 'alike', kind: 'is', class: 'is', derived: 'derived-from', ... }` (5354) applied at 5371.
22. Display dictionaries the page authors: `SATNAME` (5353), `REL_TYPES` with weights/descriptions (5355-5358), `REST` lengths (5359), `NOTE` for input/encoder/OUTPUT/ports/mother/SQL prompt (5431), `HIDE` ports (5432), `DOERS` (5433), `roleText` (5763), `ROLETEXT` (5799-5800), `CATNAME` (5838).
23. Layout physics is the page's: springs, pull law (5516-5518), `placeNew` (5524-5531), `settle` with step limit p95→4, max 6 (5553-5555), `spaceApart` with `GAP = 15, ACROSS = .25, PASSES = 3` (5560), `DEFAULT_DIR` across for opposite/inverse/contradicts (5477).
24. `viewAt()` derives "does" and "carried" lines from event roots and kinds (5600-5601); counts "mother carries" as events of kind mother/pickup/born/lay (5603).
25. `route()` drops HIDE gates and dedups (5613).
26. `renderCounts` labels (`'hand-laid gates'`, `'gates born'`, `'DNA rows, each its own trigger'`, `'mother carries'`, ...) (5688).
27. `renderProcs` labels every `PHYSICS` word `told` and defaults status to `'taught'` (5696-5697).
28. **Builder-authored formulas offered as buttons**: `SAYF`, `LIKE` (5706-5707), `E6PRESETS` (5708: `your = ...`, `my = ...`, `age = ...`, `is = ...`, `? = ...`, `how = ...`, `define = ...`, `before = ...`, `after = ...`), `PRESETS` (5710-5720: `derive = INSERT INTO formula ... LIMIT 1`, `deduce = ...`, `source = ...` for three sats, `who = ...`, `what = ...`, `who are -> what`, `sky => blue`, BUILD lines). `E6MEASURED` hand-written meanings (5709).
29. Busy/narration strings written by the page: 5703 `'the brain is running ... the physics is SQLite, so a line that brings new words, which sources answer, takes seconds'`; 5392-5394 `'line k of n ran ... and said ...'`; 5398 deep-nesting explanation; 5403; 5409 `'SQLite refused the line ...'`.
30. `levels()` computes "levels of formula below it" by recursion over formula bodies, treating `:x`, quoted, numeric, and `ROOTROLES` as depth 0 (5774-5784).
31. Atlas "meaning in the brain" is a page classification by role/formula presence (5822-5829), e.g. `r.meaning = 'none in the brain yet: no formula row, no told job'`.
32. `readingHTML` asserts "E5: not yet better than chance, p = 0.42" (5788).
33. Lab constants: `AXES = ['rows','structure','text']`, `LRULE = 'share'`, `LPULL = 0.5` (5961), `MKINDS` (5954-5958), `EFFS` (5960), `eligible()` by `told` flag (5972).
34. **`LabPlace.solve` computes every measured place in JS** (5907-5949) and `labUpdate` writes them into `lab.place` then reads them back (5999-6002).
35. `window.__poc` test hooks: `rawRows(sql)` runs arbitrary SQL on the brain (6162); `setParam` changes layout constants (6156); `step` (6157).
36. `mainEngine()` evals the engine on the page thread (5417) and `adopt` swaps the worker's brain for bytes produced on the main thread (5404, 912-917).
37. `SHEET` click fills the prompt (6122-6123) — the sheet text itself (5167-5348 / sheet173.json) is builder-authored SQL containing `LIMIT 1`, `LIMIT 5`, `LIMIT 8`, `CASE :kind WHEN 'memory' ... WHEN 'formula' ... WHEN 'definition' ... WHEN 'relation' ... WHEN 'place' END` (SHEET:76), `rel IN ( 'like' , 'alike' , 'similar' )` (SHEET:92), `substr ( :after , instr ( :after , ':' ) + 1 )` splitting on ':' (SHEET:4, 8, 12, 16, 20, 24, 36, 80, 84, 88), `instr ( line , '/build' ) + 7` (SHEET:8, 76, 84, 88).
38. The 1-of-1 told formula in the block, SQL:1042: `source = INSERT INTO wn.inbox ( word ) VALUES ( :subject ) ; ... measured.inbox ...` — the choice of which eight sources to ask is a hand-typed line, laid as the last told statement.

host15.py / neuron_prompt.py:

39. `:sheet`, `:save`, `:q` commands; prints `l[:100] + '...'` (NP:27); prints `[seconds] out` (NP:19); on exception prints `'the brain refused the line:'` (NP:18).
40. README.md:3 claims "host15.py ... It decides nothing." (contradicted by items 1-9).
41. NP:11 restores `brain.db` into the fresh connection but the satellites are rebuilt by the host each session (PY:15-22), i.e. source data lives outside the saved brain.

Top 10 (by effect on what the brain is credited with): 1, 2, 3, 4, 7, 8, 9, 17, 34, 28.

---

## 4. The told block: every trigger, one line each, with marks

Counts: 121 `CREATE TRIGGER` (81 are the hand-laid `miss_<N> INSTEAD OF INSERT ON land_<N>` for gates 1-86 minus the 5 port gates 74-78, which have no table); 86 encoder rows (16 physics, 13 root, 40 sqlroot, 3 arrival, 1 word `origin`, 5 port, 8 sat); 11 `mother(...)` call sites.

Marks: [T] composes CREATE/INSERT text from a string template; [L] has a LIMIT; [W] hard-coded word/action list; [M] memory rule; [X] teacher's expected answer written into memory.

| SQL line | trigger | what it does |
|---|---|---|
| 77...727 | `miss_<N> INSTEAD OF INSERT ON land_<N>` (×81) | `WHEN NOT EXISTS (SELECT 1 FROM gN WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (N, ...)`: a landing with no row asks `lay` for one |
| 729 | `input_teach` | [W] `WHEN NEW.kind = 'line' AND instr(NEW.line, ' = ') > 1 AND instr(NEW.line, '=>') = 0 AND instr(substr(NEW.line, 1, instr(NEW.line, ' = ') - 1), ' ') = 0 AND NEW.line NOT LIKE 'BUILD %'`: a `word = ...` line births the word (`why` 'a word given a formula'), makes a `run` of kind 'teach' from the right side, direction 'start' |
| 736 | `input_bind` | [W] `WHEN ... instr(NEW.line, ' -> ') > 0`: splits on `' -> '` into `bindq (words, f)` and a run of kind 'bind' |
| 741 | `input_run` | [W] everything else: `run.line = ... CASE WHEN instr(NEW.line, ' => ') > 0 THEN substr(... ' => ' ...)`, `expected = trim(substr(NEW.line, instr(NEW.line, ' => ') + 4))`, `build = (NEW.line LIKE 'BUILD % BUILD')` |
| 750 | `run_go` | sets `root` (`CASE WHEN NEW.kind IN ('defrow', 'test') THEN NEW.id ELSE coalesce(parent.root, NEW.id)`), writes the formula-run holes `:head :after :before :subject :line :run :prev :speaker` into `var` (`:prev` = `max(id) FROM run WHERE kind = 'line' AND id < root`; `:speaker` = 'self' if direction 'said' else 'user'), then `INSERT INTO encode (run, text) VALUES (NEW.id, NEW.line)` |
| 763 | `run_said AFTER UPDATE OF root` | writes the 'input' narration event (`'primary input: "..."'`, `'said back: ...'`, `'... fires: its formula runs as a branch of run ...'`, `'a definition row of ... runs like any line'`, `'the words of a told line get their gates'`) |
| 767 | `encode_word` | peels one word; `INSERT INTO born ... WHERE NOT EXISTS (encoder.word)`; `INSERT INTO source` when `e.role IN ('word', 'sqlroot', 'root', 'physics') AND e.sourced = 0 AND kind = 'line' AND NOT EXISTS formula AND build = 0` [W]; appends gate to `run.gates`; recurses |
| 775 | `encode_done` | event `'encoder: <line> = gates <gates>'`; `INSERT INTO decide` (kind <> 'bind') or `INSERT INTO bindgo` |
| 781 | `born_go` | [T][W] role rule `CASE WHEN NEW.word LIKE ':%' THEN 'var' WHEN NEW.word GLOB '[0-9]*' OR NEW.word LIKE '''%' OR NEW.word LIKE '%''' THEN 'literal' ELSE 'word' END`; `SELECT mother('CREATE TABLE g' || gate || ' (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER)', NULL, NULL)`; `mother('CREATE VIEW land_' ...)`; `mother('CREATE TRIGGER miss_' ... ' INSTEAD OF INSERT ON land_' ... ' BEGIN INSERT INTO lay (...) VALUES (' || gate || ', NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END')`; blank `definition (word, 'node')`; event `'born X (gate N): mother makes its table, its gate and its trigger, and a blank definition node'`; `INSERT INTO source` if `why IS NULL` and role 'word' |
| 791 | `decide_go` | [M][L][W][T] memory lookup `UPDATE run SET memid = (SELECT m.id FROM memory m WHERE m.list = run.gates AND m.direction = run.direction AND m.ended = 0 ORDER BY m.id DESC LIMIT 1) WHERE ... kind = 'line' AND build = 0` (exact gate-sequence + direction match); reopen rule 1 (793): memory has no `answer` and a gap of the memory's run is now fillable (`g.kind = 'word' AND EXISTS formula ... OR g.kind = 'source' AND EXISTS formula 'source' OR g.kind = 'defrows' AND EXISTS formula IN ('like', 'opposite', 'kind')`); reopen rule 2 (794): `g3` has a row `arrival = first gate AND trigger = gate(':prev')` and `memory.prevgates <> previous line's gates`; `INSERT INTO memhit` if memid and not reopen; narration `'decide: not in memory. The line runs from its first word; each landing fires its row.'` / `'...was written with gaps and something it lacked now exists. It runs again the long way.'`; writes the first `envelope` (arrival = gate(direction), remainder = gate(2nd word), rest) and `SELECT mother('INSERT INTO land_' || gate(1st word) || ' (arrival, remainder, run, rest) SELECT arrival, remainder, run, rest FROM envelope WHERE id = (SELECT max(id) FROM envelope)', NULL, NULL)`; deletes the envelope |
| 804 | `memhit_go` | [M][X] `UPDATE memory SET times = times + 1, last = ...`; `INSERT INTO memwrong ... WHERE r.expected IS NOT NULL AND r.expected IS NOT (SELECT coalesce(answer, output) FROM memory ...)`; `UPDATE run SET recalled = 1, output = (SELECT coalesce(answer, output) FROM memory WHERE id = run.memid)` (the recall returns the teacher's `answer` first); event `'decide: this line is in memory (receipt ...). Do I know this? Yes: one hop to it, times N. No rows fire, no lay, no mother.'`; `INSERT INTO timeline`; `INSERT INTO output`; event 'say' |
| 815 | `memwrong_go` | [T][W] `WHEN gate(':prev') IS NOT NULL`: `SELECT mother('INSERT INTO g3 (arrival, remainder, trigger, times, first, last) SELECT ' || NEW.first || ', NULL, ' || gate(':prev') || ', 0, ... WHERE NOT EXISTS (SELECT 1 FROM g3 WHERE arrival = ' || NEW.first || ' AND trigger = ' || gate(':prev') || ')', NULL, NULL)`; event `'decide was wrong: memory N answered ... where ... was right. Kept as history, not overwritten. ...'` |
| 821 | `lay_go` | [T][L][W] `UPDATE lay SET shard = mother('INSERT INTO g' || NEW.gate || ' (arrival, remainder, trigger, times, first, last) VALUES (...)', NULL, NULL)` (host's lastrowid becomes the shard); `SELECT mother('CREATE TRIGGER hop_' || NEW.gate || '_' || shard || ' INSTEAD OF INSERT ON land_' || NEW.gate || ' WHEN NEW.arrival = ' || NEW.arrival || ' AND NEW.remainder IS ' || coalesce(NEW.remainder, 'NULL') || ' BEGIN UPDATE g' || NEW.gate || ' SET times = times + 1 ...; INSERT INTO receipt (run, gate, shard) VALUES (NEW.run, ...); INSERT INTO event (''hit'' ...); ' || CASE WHEN NEW.gate = (SELECT gate FROM encoder WHERE word = ';') THEN 'INSERT INTO stmt (run, text) SELECT NEW.run, (SELECT group_concat(w, '' '') FROM (SELECT CASE WHEN e.role = ''var'' THEN quote(coalesce((SELECT value FROM var WHERE run = NEW.run AND name = e.word ORDER BY id DESC LIMIT 1), (... parent ...), (... root ...))) ELSE e.word END AS w FROM receipt r JOIN encoder e ... WHERE r.run = NEW.run AND r.id >= (SELECT min(r2.id) ... WHERE e2.word IN (''SELECT'',''INSERT'',''UPDATE'',''DELETE'',''CREATE'',''WITH'') AND r2.id > coalesce((SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = 65 AND id < ...), 0)) ORDER BY r.id)) WHERE kind = ''formula''; ' ELSE '' END || 'INSERT INTO fire (run, gate, shard, trig, rest) VALUES (...); ' || CASE WHEN NEW.remainder IS NULL THEN 'INSERT INTO "end" (run) VALUES (NEW.run); ' ELSE 'INSERT INTO land_' || NEW.remainder || ' (...) VALUES (' || NEW.gate || ', (SELECT gate FROM encoder WHERE word = substr(trim(NEW.rest) || '' '', 1, instr(...) - 1)), NEW.run, trim(substr(...))); ' END || 'END', NULL, NULL)`; `gate = 65` is the hard-coded `;` gate; event `'X: no row for (A, B). lay writes row sN and mother lays its own hop trigger'`; re-lands through mother (826) |
| 832 | `bind_go` | parses `bindq.words` (two or three words) with nested `substr/instr` into (gate, arrival, remainder); `arrival` defaults to `gate(word = 'heard')` [W]; `trig = gate(bindq.f)`; writes `bindrow` |
| 842 | `bindrow_go` | [T] `UPDATE bindrow SET found = mother('SELECT shard FROM g' || NEW.gate || ' WHERE arrival = ' || NEW.arrival || ' AND remainder IS ' || coalesce(NEW.remainder, 'NULL'), NULL, NULL)`; `SELECT mother('UPDATE g' || NEW.gate || ' SET trigger = ' || NEW.trig || ' WHERE shard = ' || found, NULL, NULL)`; else `INSERT INTO lay (..., trig)` |
| 849 | `fire_go` | [W] decides which word fires: `UPDATE fire SET word = coalesce(CASE WHEN kind = 'defrow' THEN NULL ELSE word(NEW.trig) END, CASE WHEN EXISTS formula(word(NEW.gate)) THEN word(NEW.gate) END) WHERE ... NOT (EXISTS (receipt ... e.word IN ('SELECT','INSERT','UPDATE','DELETE','CREATE','WITH') AND r.id > last ';')) AND kind <> 'teach' AND ... IS NOT run.word AND ... IS NOT parent.word AND (count of formula runs in the 3-deep ancestry) < 3`; writes `gap` `'a formula for X'` when the trigger column points at a word without a formula; `INSERT INTO input (line, direction, parent, kind, word, fgate, fshard, subject, rest, before) SELECT (group_concat of the formula run's receipt words), 'start', NEW.run, 'formula', f.word, ...` — a formula run is a new input line rebuilt from receipts |
| 863 | `stmt_go` | event `'output to sources: the gates the run passed decode to "<text>". Mother picks it up.'`; `SELECT mother(NEW.text, NEW.run, NEW.id);` — the one true paste of run-assembled text |
| 868 | `secondary_refused` | `WHEN last = 1 AND src <> 'sql' AND err IS NOT NULL`: event 'refused', gap 'refused', `run.failed = 1` |
| 874 | `secondary_ask` | `WHEN last = 1 AND src <> 'sql' AND waiting = 0 AND err IS NULL`: counts kept/aside/total from `secondary` rows by `hw` prefix before ':' = word → `sense` |
| 879 | `secondary_sql` | `WHEN last = 1 AND src = 'sql'`: event `'secondary input: ...'`; `sense` row with `asked`/`needed` text (`'yes: N row(s) fill the cell'`, `'no: no row came back; the brain does not hold this'`, `'yes: N change(s) made'`, `'no: the statement changed nothing'`) chosen by `stmt.text LIKE 'SELECT%' OR LIKE 'WITH%'` [W] |
| 887 | `secondary_wait` | `WHEN waiting = 1`: event `'...The cell waits; no timer fills it.'`, empty `var` cell named by the stmt text, gap 'wait', `run.failed = 1` |
| 894 | `sense_ask` | `WHEN src <> 'sql'`: writes the asked/needed/wrong/setaside sentences; event 'check'; `var` cell `'<src>: <word>'` = `'N row(s)'`; **copies kept rows into `definition`**; gap 'ask' and `run.failed = 1` if kept = 0 |
| 909 | `sense_sql` | `WHEN src = 'sql'`: `ok = (needed LIKE 'yes%')`; `var` cell named by the stmt text with value = reply or `'ok, N change(s)'`; `var ':found' = secondary.value` when n > 0; `run.failed = 1` if needed not 'yes%' |
| 917 | `definition_split` | `WHEN src <> 'node' AND words IS NOT NULL`: seeds `defword` |
| 921 | `defword_next` | recursive word split of `defword.rest` |
| 925 | `say_go` | `var (root, 'output', NEW.text, 'say')`; event `'say: "<text>" goes to output to use'` |
| 930 | `relation_drawn` | event 'rel' with `a = NEW.b, b = rel || '|' || trust` (for the page's lines) |
| 935 | `formula_written` | `proc` upsert status `taught`/`derived`; event 'taught'/'derived' with the formula "read back from the run that taught it" |
| 942 | `source_go` | [L][W] `encoder.sourced = 1`; gap 'source' if no `source` formula; `INSERT INTO fire (... trig = gate('source'), rest = word, subject = word) WHERE EXISTS formula 'source'`; `INSERT INTO agree`; `INSERT INTO input (...) SELECT 'return from ' || line || ' from ' || d.src || ' /build ' || d.words, NEW.word, NEW.run, 'defrow', NEW.word FROM definition d WHERE ... LIMIT 8`; gap 'defrows' unless formulas `IN ('like', 'opposite', 'kind')`; fires `derive` and `deduce` if those formulas exist and the word has none |
| 954 | `agree_go` | [L] `need` upsert of defining words shared by `count(DISTINCT src) >= 2`, `length(w) > 1`; event `'agree: defining words two or more sources share for X: ...'` with `LIMIT 14` |
| 960 | `end_branch` | [T][L] `WHEN kind = 'formula'`: event `'substitution: the cells plug into X''s formula and it ran. Every ask came back with what it asked for.' / 'An ask came back without what it needed.'`; `procrun`; `proc.status` → 'learned' at `>= 3` identical receipts, 'automated' after; on failure `INSERT INTO stepq (run, alt) SELECT NEW.run, mother('SELECT trigger FROM g' || fgate || ' WHERE trigger IS NOT NULL AND trigger <> ' || gate(word) || ' AND shard IS NOT ' || fshard || ' LIMIT 1', NULL, NULL)` |
| 970 | `step_back` | event `'step back: X asked and the check failed. The run steps back to Y and takes its other row, whose trigger is Z'`; re-fires the parent with the alternate trigger; gap 'stepback' if none |
| 976 | `end_teach` | [M] `WHEN kind = 'teach'`: ends the word's old `formula` rows; `INSERT INTO memory (list, line, direction, receipt, output, answer, mark, ...) ... NULL, NULL, 'told'`; `INSERT INTO formula (word, run, origin) VALUES (word, NEW.run, 'told')` — the formula is a pointer to the run |
| 984 | `end_return` | [M][L] `WHEN kind = 'defrow'`: memory row marked `'definition from <sat>'` (first `role = 'sat'` receipt word, LIMIT 1); `var` cell in the parent run named `'<sat> <subject>'` = memory id; event 'memory' |
| 992 | `end_line` | [M][X][L][W] `WHEN kind = 'line'`: event 'end' with receipt; `INSERT INTO "BUILD" ... trim(substr(line, 7, length(line) - 12)) ... WHERE build = 1`; `run.output` = (build: last `secondary` value / 'error: ...' / 'ok') else `coalesce(var 'output', group_concat of receipt words with '?' appended to `role IN ('word', 'literal')` words lacking a formula)`; `run.mark` = `CASE WHEN expected IS NOT NULL THEN (output = expected → 'right' else 'wrong') WHEN EXISTS memory(list, direction) THEN (memory.output = output → 'balanced' else 'shift') ELSE 'unchecked'`; `proc.right/wrong` for formula words in the run; event `'makes sense: proposed "..." expected "...": wrong. The failed try stays in memory as wrong; the expected output is kept with it, so next time the hop answers it.'`; **`UPDATE memory SET ended = 1 WHERE list = gates AND direction = direction AND ended = 0`** (the old memory of the same gate list is ended); **`INSERT INTO memory (..., output, answer, mark, ..., prevgates) SELECT gates, line, direction, receipt, CASE WHEN mark = 'wrong' THEN expected ELSE output END, expected, mark, ...`** — the teacher's `expected` is written as the memory's `output` when the run was wrong and always as `answer`; `timeline`; `output`; event `'say: ... (corrected to "<expected>" for next time)'`; event 'gaps' |
| 1012 | `end_test` | [M] `WHEN kind = 'test'`: output as above; `var ':test'` in the parent = `'no memory' / 'balanced' / 'shift' || ': ' || output` by comparing to `max(id) FROM memory WHERE list = r.gates AND direction = 'heard' AND ended = 0 AND mark <> 'told'`; event 'test' |
| 1019 | `receipt_gap` | `WHEN kind = 'line' AND role = 'word' AND NOT EXISTS formula AND NOT EXISTS gap`: gap `'a meaning for X' / 'it does nothing when a run passes it...'`; event `'X: the run passes it and nothing happens. No formula. A broken word.'` |
| 1025 | `build_go` | `INSERT INTO stmt (run, text) VALUES (NEW.run, NEW.text)` — BUILD text goes to mother through stmt_go |
| 1029 | `state_written` | event `'state: key = value. A formula wrote it; the brain holds it now.'` |
| 1033 | `place_written` | ends older `place` rows of the word; event 'place' |
| 1038 | `proc_status AFTER UPDATE OF status` | event `'X has three memories of the same receipt: learned.'` / `'ran again after learned: automated.'` |
| 1042 | (not a trigger) the last told statement | [W] `INSERT INTO input (line, direction) VALUES ('source = INSERT INTO wn.inbox ( word ) VALUES ( :subject ) ; INSERT INTO gcide.inbox ...; mw; mwt; moby; map; sqldoc; measured ...', 'heard')` — the eight sources to ask are typed here |

Summary of the marked items:

- **[T] templates composing CREATE/INSERT text**: `born_go` 783-785 (`'CREATE TABLE g'`, `'CREATE VIEW land_'`, `'CREATE TRIGGER miss_'`), `lay_go` 822-823 (`'INSERT INTO g'`, `'CREATE TRIGGER hop_'`), `decide_go` 798 and `lay_go` 826 (`'INSERT INTO land_'`), `memwrong_go` 816 (`'INSERT INTO g3 (...) SELECT '`), `bindrow_go` 843-844 (`'SELECT shard FROM g'`, `'UPDATE g'`), `end_branch` 965 (`'SELECT trigger FROM g'`).
- **LIMIT**: 792 (`ORDER BY m.id DESC LIMIT 1` memory pick), 794, 806, 823 (×3 var lookup), 947 (`LIMIT 8` definition rows), 957 (`LIMIT 14` agree list), 965 (`LIMIT 1` alternate row), 986/988/989 (`LIMIT 1` first sat), 995 (×2), 997, 1002, 1013.
- **Hard-coded lists**: 823 & 851 `IN ('SELECT','INSERT','UPDATE','DELETE','CREATE','WITH')`; 793 & 949 `IN ('like', 'opposite', 'kind')`; 950-951 `word = 'derive'`, `word = 'deduce'`; 945 `word = 'source'`; 794/815-817 `word = ':prev'`; 823 `word = ';'` and literal `gate = 65`; 835 `word = 'heard'`; 770 `role IN ('word', 'sqlroot', 'root', 'physics')`; 995/1013 `role IN ('word', 'literal')`; 751 `kind IN ('defrow', 'test')`; 764 `kind IN ('line', 'teach', 'bind')`; 782 role rule by `LIKE ':%'` / `GLOB '[0-9]*'` / quotes; 729/741 the `' = '`, `'=>'`, `' => '`, `' -> '`, `'BUILD %'`, `'BUILD % BUILD'` grammar; 994 `substr(line, 7, length(line) - 12)`; 964 `>= 3`; 955 `count(DISTINCT src) >= 2`, `length(w) > 1`.
- **Teacher's expected answer into memory**: `end_line` 1002 `CASE WHEN mark = 'wrong' THEN expected ELSE output END, expected` (output column replaced by expected when wrong; answer column = expected always); 1001 ends the previous memory of the same gate list; `memhit_go` 807 `output = coalesce(answer, output)` returns the expected first; 806 writes `memwrong` only when `expected` disagrees. Nothing is overwritten in place; the old row is `ended = 1` and a new row carries the teacher's text.
- **Memory lookup rule**: `decide_go` 792 exact match on `memory.list = run.gates AND direction AND ended = 0`, newest first; reopen exceptions 793-794; `end_line` 997 same key for 'balanced'/'shift'; `end_test` 1015 same key with `mark <> 'told'`.

---

## 5. How "mother" appears in 17.3, and what she does

Where she appears:

- In the brain: an **encoder row only**: SQL:661 `INSERT INTO encoder (gate, word, role, born) VALUES (77, 'mother', 'port', 0);` (and SQL:663 `(78, 'SQL prompt', 'port', 0)`). No `g77` table, no view, no trigger (the five port gates 74-78 are the only encoder rows without tables; SQL has 81 `miss_` triggers for 86 gates). `event.rowgate = 'mother'` is written by `born_go` SQL:787 and by the host (HTML:723, 747, 763).
- Outside the brain: a **SQL scalar function registered by the host** — HTML:696 / 790 `db.create_function('mother', function (text, run, stmt) { return self.mother(text, run, stmt); })`; PY:10 `self.con.create_function('mother', 3, self.mother)` — implemented as `Brain.prototype.mother` HTML:720-769 and `Brain.mother` PY:30-76. The page prints that JS verbatim at HTML:374-427 under "mother, all of her".
- In the page's rail: `NOTE.mother` HTML:5431 `'mother: the one routine beside SQLite. She runs the text she is handed at the SQL prompt, or carries it into a source brain's inbox; when that brain says its outbox is populated she picks it up and empties it. She decides nothing. Her code is printed in the rail.'`

What she actually does (HTML lines; PY equivalents in §2.4):

1. Parses the SQL text with a regex to decide where it goes (722).
2. Executes the text on the **same connection** the trigger is running on (729 `db.prepare(text)`), inside the trigger's statement. There is no separate "SQL prompt" process or connection; "the SQL prompt" is a label on an event row (746).
3. Decides what the text's result *means* by the `run === null` test (740): physics step → returns a scalar (first column of first row, else `last_insert_rowid()`) that the trigger stores as `lay.shard` / `bindrow.found` / `stepq.alt`.
4. Formats a result set into one string with `' '` and `' | '` (748).
5. Writes narration rows into `event` (723, 746, 747, 759, 760, 763) with root labels (`'CALL MOVE'`, `'FIND READ WRITE'`, `'WRITE'`, `'MOVE CALL'`).
6. Writes the `secondary` rows and chooses their marks (`last`, `n`, `cols`, `changes`, `err`, `waiting`) (749, 755, 756, 764, 765). The brain's four `secondary_*` triggers and two `sense_*` triggers (SQL:868-915) then fire on those marks.
7. Classifies errors: stack-depth errors are rethrown to abort the whole line (737); other errors become a "refusal" (746, 755).
8. Reads the satellite outbox and empties it (761-762) — but the "populated" signal she reacts to is a JS array filled by the host-registered `satwork` function (697, 739, 753), not a brain table.
9. Keeps a compiled-statement pool (727-732).
10. The satellites she "carries into" are databases the host itself creates and populates (701-707, 794-799; PY:16-22).

Against the owner's definition ("just a router and a traverser... She works no data... paste and route"): items 1, 3, 4, 5, 6, 7 are data work and decisions. The run-sheet picture (neurons assemble SQL → mother pastes) holds only for `stmt_go` (SQL:865). For births, lays, landings, binds and step-back, the SQL is a template inside a hand-laid trigger and mother is the executor of that template (SQL:783-785, 798, 816, 822-823, 826, 843-844, 965).

---

## 6. Presented as the brain's, done by the host

1. **Step log rows written by JS/py** appear in the same `event` table and the same log as trigger-written rows, undistinguished: `'mother carries it into the inbox of ...'` (HTML:723), `'the SQL prompt runs it'` / `'refuses it: ...'` (746), `'mother carries the reply back'` (747), `'<sat>: the ask for "X" lands in its inbox; its own trigger does its work at once'` (759), `'<sat>: its outbox is populated with N row(s), and it says so'` (760), `'mother picks up N row(s) from <sat> and empties that outbox'` (763). `renderLog` HTML:5676 shows `e.kind`/`e.text` straight from the table; `renderCounts` HTML:5688 counts `'mother carries'` from `V.mother` = kinds mother/pickup/born/lay (5603), two of which are host-written. The silicon ledger (5691-5692) sums `roots` including the host-assigned `'CALL MOVE'` etc.
2. **"it says so"** (760): the satellite's trigger calls `satwork(...)`, a host function that pushes to a JS array (697). The sentence "its outbox is populated ... and it says so" is composed and written by the host, not by the source brain.
3. **The source brains** are presented as "a source brain: its own database, a corpus, an inbox, an outbox, and its own trigger. A stand-in, fetched 2026-10-22" (5763) and "Seven stand-in source brains" (HTML:446); their schema and trigger are host code (701-705; PY:17-20) and their data is the page's `SAT` blob (HTML:950) / sat172.json. The eighth source `measured` is labelled `'measured (steps 2, 3)'` (5353) and is page-supplied corpus text.
4. **"Meaning of a word, measured"** (rail HTML:257-259): computed by the worker's `contrast()`/`meaningOf()` (847-881), including hand-added `+1 FIND/COMPARE/WRITE` and `'memory recalls'` for recalled lines (871) and the ratio split (878). The brain holds none of it.
5. **Atlas**: "Everything in it is read from SQLite when it opens, except the position ... and the lines" (5797; rail HTML:276). The column "meaning in the brain" is a page classification (`r.meaning = ...`, 5822-5829; `CATNAME` 5838), and the "levels of formula below it" is `levels()` (5774-5784). The atlas summary does say positions are the page's (5883).
6. **Measured tab**: "x, y, z are read from the lab's place table in SQLite" (6100) and "The page solves the places with the rule above and writes them into place; the stage, the table and Selected read them back from SQLite" (HTML:201). The solve is `LabPlace.solve` in JS (5907-5949, called 5999); SQLite is a pass-through store (6000-6002). The brain-places mode (`LFROM === 'brain'`, 5990) reads the brain's `place` table, which is written by the taught `place:` / `backpop:` formulas (SHEET:32, 36) — those formulas' x,y,z are `10 * CAST(definition.text AS INTEGER)` from the `measured` source rows (page-supplied data).
7. **Relation names** shown on the stage are renamed by the page: `REL_OF` (5354) turns the brain's `relation.rel` 'like'→'alike', 'kind'→'is', 'class'→'is', 'derived'→'derived-from' (applied 5371).
8. **"the brain ... said ..."** busy text (5390-5394) and the deep/failed explanations (5398, 5403, 5409) are page prose.
9. **Presets** (5706-5720) and `E6PRESETS` (5708) are builder-written formulas presented as things to teach; `E6MEASURED` (5709) are builder-written meanings shown in the Selected card (5767) as "measured in E6".
10. **"mother ... decides nothing"** (5431; HTML:376 comment `// She decides nothing and computes nothing about the reply.`; README.md:3 "It decides nothing.") against §5 items 1-7.
11. **"The brain's told block and tables are unchanged"** (HTML:201) is true for the lab; but `reopenBrain` (788-801) runs `PRAGMA recursive_triggers = ON` and rebuilds the attached satellites on the brain's connection after every snapshot, and `__poc.rawRows` (6162) can run any SQL against the brain.
12. The hand-laid `born_go` event text (SQL:787) says `'mother makes its table, its gate and its trigger'` — in fact the trigger composes the CREATE text and `mother` only executes it; neither the neurons nor a run sheet made it.

---

## 7. Code outside the brain that simulates what the brain should do (facts, no softening)

- `Brain.prototype.mother` / `Brain.mother`: regex routing (HTML:722; PY:32), result-to-string formatting (748; 54), scalar return rule feeding `lay.shard`/`bindrow.found`/`stepq.alt` (743, 750; 50, 57), refused/waiting/delivered classification (755-756; 60-66), narration rows into `event` (723, 746, 747, 759, 760, 763; 34, 52, 53, 68, 69, 72), `secondary` marks (749, 755, 756, 764, 765; 55, 62, 65, 74, 75).
- `satwork` + `this.populated` array (HTML:697, 724, 739, 753; PY:11, 36, 46, 59): the "outbox is populated" message lives in host memory, not in a table.
- Host-built source brains and their `work` trigger (HTML:701-705, 794-799; PY:17-20).
- CREATE-text templates in hand-laid triggers executed by the host function: `born_go` SQL:783-785, `lay_go` SQL:822-823 (hop trigger body ~1.8 KB template), `memwrong_go` SQL:816, plus `decide_go` 798, `lay_go` 826, `bindrow_go` 843-844, `end_branch` 965. These bypass the run sheet (`stmt`/`secondary`), which is used only by `stmt_go` SQL:865.
- The `;` hop trigger's statement assembly with the three-level `var` fallback (run → parent → root) and the `IN ('SELECT','INSERT','UPDATE','DELETE','CREATE','WITH')` / `gate = 65` cut (SQL:823): a hand-laid parser inside the brain.
- Memory: exact gate-list match (SQL:792); teacher's `expected` written into the new memory's `output`/`answer` when wrong (SQL:1002) and returned first on recall (SQL:807).
- Worker `contrast()`/`meaningOf()` (HTML:847-881): re-runs lines on brain copies with a word deleted and scores the difference, adding counts by hand for recalls (871).
- Page `LabPlace.solve` (HTML:5907-5949) computes places; SQLite stores them (6000).
- Page `REL_OF` renaming (5354, 5371), `levels()` (5774-5784), atlas meaning categories (5822-5829).
- Main-thread fallback `(0, eval)(engine)` + `adopt` (5417, 5401-5404, 912-917): the host decides to re-run a failed line elsewhere and swap the brain's bytes.
- `window.__poc.rawRows(sql)` (6162): arbitrary SQL into the brain from outside.
- Builder-authored formulas: the eight-source `source =` line (SQL:1042), PRESETS/E6PRESETS (5706-5720), and every SHEET line (5167-5348 = sheet173.json) including `LIMIT 1/5/8`, `CASE :kind WHEN 'memory' ... 'place' END`, `rel IN ('like','alike','similar')`, splits on `':'` and `'/build'`.
