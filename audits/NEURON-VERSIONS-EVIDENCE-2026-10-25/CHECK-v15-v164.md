# Forensic check: Point Of Connection v15 -> v16.4 (2026-10-25, read-only)

Files checked (copies in this folder; Downloads untouched): v15.html, v16.html, v161.html, v162.html, v163.html, v164.html,
v16-told.sql (NEURON-v16-TOLD-BLOCK), src164/ (NEURON-v16.4-SOURCES tarball, extracted, exec bits stripped, nothing run from it).
Told blocks extracted to told_vNN_TOLD.json; statements numbered in stmts_vNN.sql ("[k]" below = statement index inside the one-line
`var TOLD = {...}` of each page); logic-only statements in nonrep_vNN.sql.

Page anatomy (every version): `<script id="engine-src">` = sql.js bundle + the Neuron host (Brain, mother, satellites) +
exportBrain/restoreBrain; `<script id="worker-src">` = the worker that owns the brain; one long line `var TOLD = {...}, SAT, SLICE,
READINGS[, MAP]` = the told block as a JSON list of SQL statements plus word lists; then the page thread (three.js drawing, presets, atlas).

## 0. What is identical across versions (measured by byte diff)

| | told block (TOLD) | host (engine-src non-bundle) | worker | page thread |
|---|---|---|---|---|
| v15 -> v16 | DIFFERS (see sec 6) | 12 lines changed | 6 lines | 164 lines |
| v16 -> v16.1 | identical | identical | identical | 54 lines (drawing) |
| v16.1 -> v16.2 | identical | identical | identical | 31 lines (drawing) |
| v16.2 -> v16.3 | identical | identical | identical | 83 lines (drawing, owner map) |
| v16.3 -> v16.4 | identical | identical | 11 lines (read-only `atlas` query) | 125 lines (atlas table, layout hooks) |

So the brain (told block + mother) has exactly two states in this range: **v15** and **v16 (= 16.1 = 16.2 = 16.3 = 16.4)**.
The told block generator is `src164/v16/gen_physics15.py` (v15) and `src164/v16/gen_physics.py` (v16); they run at build time only
(build15.py / build16.py embed `physics16.json` into the page). No Python runs in the browser.

Told-line page numbers: v15:833, v16:803, v16.1:834, v16.2:836, v16.3:840, v16.4:888.
Host page numbers (HOST-START / `Brain.prototype.mother` / `Brain.prototype.type`): v15 596/630/676; v16 558/592/644; v16.1 589/623/675;
v16.2 591/625/677; v16.3 595/629/681; v16.4 632/666/718.

## 1. How a new neuron (table) is created when an unknown word arrives

**Answer, all versions: (b)** - a string template inside a hand-laid SQL trigger, executed through the host-registered `mother()` UDF.
Not (a): no run of tokens assembles the CREATE; not (c): JS does not compose it (JS only executes the text it is handed).

Chain: `input_run` [339 v15 / 340 v16] -> `run_go` [341/342] inserts the line into `encode` -> `encode_word` [343/344] peels one word
at a time and, if the word has no gate, inserts into `born`:
```
INSERT INTO born (word, run, why) SELECT substr(trim(NEW.text) || ' ', 1, instr(trim(NEW.text) || ' ', ' ') - 1), NEW.run, ...
  WHERE NOT EXISTS (SELECT 1 FROM encoder WHERE word = ...);
```
`born_go` [345 v15 / 346 v16] (v15.html:833, v16.html:803, v16.1:834, v16.2:836, v16.3:840, v16.4:888) composes the three objects by
string concatenation and hands each to mother:
```
CREATE TRIGGER born_go AFTER INSERT ON born BEGIN
  INSERT INTO encoder (word, role, born) VALUES (NEW.word, CASE WHEN NEW.word LIKE ':%' THEN 'var' WHEN NEW.word GLOB '[0-9]*' OR NEW.word LIKE '''%' OR NEW.word LIKE '%''' THEN 'literal' ELSE 'word' END, ...);
  SELECT mother('CREATE TABLE g' || (SELECT gate FROM encoder WHERE word = NEW.word) || ' (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER)', NULL, NULL);
  SELECT mother('CREATE VIEW land_' || (SELECT gate FROM encoder WHERE word = NEW.word) || ' AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g' || ..., NULL, NULL);
  SELECT mother('CREATE TRIGGER miss_' || ... || ' INSTEAD OF INSERT ON land_' || ... || ' WHEN NOT EXISTS (SELECT 1 FROM g' || ... || ' WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (' || ... || ', NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END', NULL, NULL);
  INSERT INTO definition (word, src) VALUES (NEW.word, 'node');
  INSERT INTO event (...) VALUES ('born', NEW.word, NEW.run, 'mother', 'born ' || NEW.word || ' (gate ' || ... || '): mother makes its table, its gate and its trigger, and a blank definition node' ...);
```
The same template is what the generator lays for the 73 told gates (`gen_physics.py` `gate_objects(k)` / `born_texts(idexpr)`: "The same
three objects as SQL text the brain builds itself, by value, for a born word, and hands to mother one statement at a time").

mother executes it in JS: v15.html:606 `db.create_function('mother', function (text, run, stmt) { return self.mother(text, run, stmt); });`
and v15.html:639-643 `st = free.length ? free.pop() : db.prepare(text); ... while (st.step()) rows.push(st.get());` with `run === null`
meaning "a by-value step of the physics itself (a birth, a lay, a landing): the SQL prompt's own answer goes straight back" (v15.html:647-649).

v16 adds a second birth path for taught words: `input_teach` [338] `INSERT INTO born (word, run, why) SELECT substr(NEW.line, 1,
instr(NEW.line, ' = ') - 1), NULL, 'a word given a formula' WHERE NOT EXISTS (...)` - same `born_go` template.

(c) exists only for the seven **source stand-ins** (not neurons): JS composes `CREATE TABLE <sat>.corpus/.inbox/.outbox`, an index and
`CREATE TRIGGER <sat>.work AFTER INSERT ON inbox ...` (v15.html:610-619; v16 570-577; v16.1 601-608; v16.2 603-610; v16.3 607-614;
v16.4 644-651, and again in `reopenBrain`).

## 2. The hop

**Answer, all versions: a per-DNA-row SQL trigger** (`hop_<gate>_<shard>`), one per laid row, plus one `miss_<gate>` trigger per
neuron; both are string templates run through `mother()`. No JS loop walks the gates.

- Landing = `INSERT INTO land_<gate>` (an INSTEAD OF INSERT view per neuron). If no row matches, `miss_<gate>` inserts into `lay`.
- `lay_go` [349 v15 / 351 v16] writes the DNA row and the row's own trigger:
```
UPDATE lay SET shard = mother('INSERT INTO g' || NEW.gate || ' (arrival, remainder, trigger, times, first, last) VALUES (' || NEW.arrival || ', ' || coalesce(NEW.remainder, 'NULL') || ', ' || coalesce(NEW.trig, 'NULL') || ', 0, ' || ... || ')', NULL, NULL) WHERE id = NEW.id;
SELECT mother('CREATE TRIGGER hop_' || NEW.gate || '_' || (SELECT shard FROM lay WHERE id = NEW.id) || ' INSTEAD OF INSERT ON land_' || NEW.gate || ' WHEN NEW.arrival = ' || NEW.arrival || ' AND NEW.remainder IS ' || coalesce(NEW.remainder, 'NULL') || ' BEGIN '
  || 'UPDATE g' || NEW.gate || ' SET times = times + 1, last = ... WHERE shard = ' || ... || '; '
  || 'INSERT INTO receipt (run, gate, shard) VALUES (NEW.run, ' || NEW.gate || ', ' || ... || '); '
  || 'INSERT INTO event (...) VALUES (''hit'', ' || quote(word) || ', NEW.run, ..., ''COMPARE WRITE''); '
  || CASE WHEN NEW.gate = (SELECT gate FROM encoder WHERE word = ';') THEN 'INSERT INTO stmt (run, text) SELECT NEW.run, (SELECT group_concat(w, '' '') FROM (... receipt r JOIN encoder e ...)) WHERE (SELECT kind FROM run WHERE id = NEW.run) = ''formula''; ' ELSE '' END
  || 'INSERT INTO fire (run, gate, shard, trig, rest) VALUES (NEW.run, ' || NEW.gate || ', ' || ... || ', (SELECT trigger FROM g' || NEW.gate || ' WHERE shard = ' || ... || '), ...); '
  || CASE WHEN NEW.remainder IS NULL THEN 'INSERT INTO "end" (run) VALUES (NEW.run); ' ELSE 'INSERT INTO land_' || NEW.remainder || ' (arrival, remainder, run, rest) VALUES (' || NEW.gate || ', (SELECT gate FROM encoder WHERE word = substr(trim(NEW.rest) ...)), NEW.run, trim(substr(trim(NEW.rest) ...))); ' END || 'END', NULL, NULL);
...
SELECT mother('INSERT INTO land_' || NEW.gate || ' (arrival, remainder, run, rest) SELECT arrival, remainder, run, rest FROM envelope WHERE id = (SELECT max(id) FROM envelope)', NULL, NULL) WHERE NEW.run IS NOT NULL;
```
So: hop between existing rows = pure SQL (`hop_*` body does `INSERT INTO land_<remainder>`); a miss lays the row, creates its trigger via
mother, then "the landing is retried through mother" (event text, [349]). The run is started by `decide_go` [346/347]:
`SELECT mother('INSERT INTO land_' || (SELECT gate FROM encoder WHERE word = <first word>) || ' ... FROM envelope ...')`.
Each retry nests one JS->SQLite level deeper; the worker catches stack overflow and the page thread re-runs the line with a bigger stack
(v15.html:878-885, v16 851-858, v16.1 882-889, v16.2 884-891, v16.3 888-895, v16.4 936-943) - still the same SQL triggers, not a JS hop.

The hop template bakes in a numeric gate id for `;` in the statement decode (`... AND gate = 66 AND id < ...` in v15 [349];
`gate = 65` in v16 [351]). v16's own correction log (v16-checks.md "Correction log, run 1") records that v15's number shifted when SAY
merged into say and "every statement decoded from the previous ';'" - fixed by re-deriving the number at build, not by reading it live.

## 3. Mother (where defined, what she does beyond run-and-return)

Defined in JS: `Brain.prototype.mother = function (text, run, stmt)` v15.html:630-673 (v16 592-633, v16.1 623-664, v16.2 625-666,
v16.3 629-670, v16.4 666-707); registered as a SQLite function at v15.html:606 and again in `reopenBrain` (v15.html:694).
Comment at v15.html:627-629: "she runs the text she is handed at the SQL prompt. If it is addressed to a source brain's inbox she carries it
there ... She decides nothing and computes nothing about the reply." Beyond executing text and returning rows/errors she does:

1. **Regex routing** (v15.html:632): `(text.match(/\b(\w+)\.inbox\b/g) || []).forEach(... if (self.SATS.indexOf(s) >= 0 ...) addressed.push(s))`.
2. **Event narration** written into the brain's `event` table (6 kinds, canned English): 'mother carries it into the inbox of X / to the SQL
   prompt' (633), 'the SQL prompt runs it / refuses it' (652), 'mother carries the reply back' (653), 'the ask for "w" lands in its inbox; its own
   trigger does its work at once' (663), 'its outbox is populated with n row(s), and it says so' (664), 'mother picks up n row(s) ... and empties
   that outbox' (667).
3. **Silent by-value mode** (646-650): when `run === null` no events, no secondary rows; returns `rows[0][0]` else `last_insert_rowid()` -
   this is how `lay_go` gets the shard (`UPDATE lay SET shard = mother(...)`), `bindrow_go` gets `found`, `end_branch` gets `alt`.
4. **Formatting** of the reply (654): rows joined `' | '`, cells `' '`, NULL -> ''.
5. **Writing secondary rows** (655, 660, 668, 669): `INSERT INTO secondary (run, stmt, src, value, cols, n, err, changes, last)` for the SQL
   prompt; `... waiting, last) VALUES (?, ?, ?, 1, 1)` when a source did not call `satwork`; per-row and summary rows for each source.
6. **Statement cache** (637-642): compiled statements pooled per text, max 4.
7. **Picks up the outboxes herself** (665-666): `SELECT word, hw, text, words FROM <sat>.outbox WHERE ask = ?` then `DELETE FROM <sat>.outbox`.
8. v16+ only: **rethrows deep recursion** (v16.html:609-612 `if (e instanceof RangeError || !e.message || /call stack|recursion/i.test(err)) throw e;`)
   and **writes a refused row** when a source ask is refused (v16.html:627 `INSERT INTO secondary (run, stmt, src, err, n, last) VALUES (?, ?, ?, ?, 0, 1)`).

Host/worker policy outside mother that also acts on the brain (all versions): the worker **rolls the brain back to a snapshot** when a line
throws (v15.html:800 "the brain as it stood before this line comes back from its snapshot; nothing of the failed line is kept"; v16.4 844);
`KEEP = 24` snapshots; **JS measures meaning** by re-running a line with and without a word and diffing event ledgers (`contrast`,
`meaningOf`, v15.html:749-781; v16.4 793-825) - reads only, but the measuring is JS, not the brain.
The page thread never writes brain tables; it posts typed lines (`type: 'lines'`) and read-only queries (`type: 'query'`, v16.4 `'atlas'`).
Presets on the page are hand-written SQL formula lines typed in as lines (v15.html:1119-1133; v16 1078-1092; v16.1 1134-1148;
v16.2 1155-1169; v16.3 1193-1207; v16.4 1245-1259), e.g. `"your = INSERT INTO var ( run , name , value ) SELECT :run , ':owner' , 'self' WHERE :speaker = 'user' ; ..."`,
`'BUILD CREATE TABLE things ( a ) ; BUILD'`.

## 4. Counts and hard-coded rules in the told block

| | v15 | v16 = 16.1 = 16.2 = 16.3 = 16.4 |
|---|---|---|
| statements | 377 | 381 |
| CREATE TABLE | 110 (73 `gN` + 37 physics/bookkeeping) | 111 (+ `memwrong`) |
| CREATE TRIGGER | 107 (73 `miss_N` + 34 logic) | 110 (73 + 37: + `memwrong_go`, `secondary_refused`, `end_teach`) |
| CREATE VIEW | 73 (`land_N`) | 73 |
| encoder rows (told gates) | 85 (16 physics, 14 root, 40 sqlroot, 3 arrival, 5 port, 7 sat; ports/sats have no table) | 85 |
| other | 1 PRAGMA, 1 `INSERT INTO formula` (canned 'source' body) [376] | 1 PRAGMA, 1 `INSERT INTO input` ('source = ...' typed line) [380] |
| `INSERT INTO event` (canned narration) | 32 | 34 |
| LIMIT n | 8x LIMIT 1, 1x LIMIT 8, 1x LIMIT 14 | 11x LIMIT 1, 1x LIMIT 8, 1x LIMIT 14 |
| JS-laid (host) | 7 sats x (3 tables + 1 index + 1 trigger) = 21 tables, 7 indexes, 7 triggers; 2 UDFs (mother, satwork) | same, corpus `COLLATE NOCASE` |

Hard-coded rules (statement index v15 / v16):
1. Teach syntax [337/338]: `instr(NEW.line, ' = ') > 1 AND instr(NEW.line, '=>') = 0 AND instr(<head>, ' ') = 0 AND NEW.line NOT LIKE 'BUILD %'`.
2. Bind syntax [338/339]: `instr(NEW.line, ' -> ') > 0`; `bind_go` [351/353] parses at most "a b -> f" by nested substr.
3. Expected answer [339/340]: split on `' => '`; build flag `(NEW.line LIKE 'BUILD % BUILD')`.
4. Speaker rule [341/342]: `:speaker` = `CASE direction WHEN 'said' THEN 'self' ELSE 'user' END`; fixed hole set :head :after :before :subject :line :run :prev :speaker.
5. Sourcing rule [343/344]: only `e.role IN ('word', 'sqlroot')` (v16: `('word', 'sqlroot', 'root', 'physics')`), `sourced = 0`, no live formula, `build = 0`.
6. Role classification [345/346]: `LIKE ':%'` -> var; `GLOB '[0-9]*' OR LIKE '''%' OR LIKE '%'''` -> literal; else word.
7. **Memory exact-match** [346/347]: `memid = (SELECT m.id FROM memory m WHERE m.list = run.gates AND m.direction = run.direction AND m.ended = 0 ORDER BY m.id DESC LIMIT 1)`; a hit skips the gates entirely ("No rows fire, no lay, no mother", [348/349]).
8. Reopen rule [346/347]: only gaps of kind word/source/defrows, with hard list `f.word IN ('like', 'opposite', 'kind')`; v16 adds the `:prev` rule: reopen if decide's own `g3` has a row `arrival = <first gate> AND trigger = (gate of ':prev')` and the previous line's gates differ.
9. **Expected-answer overwrite** v15 [348]: `UPDATE memory SET output = expected, answer = expected, mark = 'corrected' WHERE ... expected IS NOT coalesce(answer, output)`. v16 [349] replaces it with `INSERT INTO memwrong (memid, run, first, prevgates, given, expected)` (history kept); but both keep in `end_line` [371/375] `CASE WHEN mark = 'wrong' THEN expected ELSE output END` as the memory's output.
10. v16 only [350] `memwrong_go`: `SELECT mother('INSERT INTO g3 (arrival, remainder, trigger, ...) SELECT ' || NEW.first || ', NULL, ' || <gate of ':prev'> ...)` - a told rule lays decide's DNA row ("the line before matters"), event text canned.
11. Hop template [349/351]: SQL-verb list `('SELECT','INSERT','UPDATE','DELETE','CREATE','WITH')` marks where a statement starts; numeric `gate = 66` (v15) / `gate = 65` (v16) for `;`; decode only `WHERE kind = 'formula'`.
12. Fire rules [354/356]: no firing while a SQL verb is open since the last `;`; never fire the run's own word or its parent's; **depth cap** `count(*) ... kind = 'formula') < 3`; v16 adds `kind <> 'teach'`.
13. Sense judgments [356-360 / 358-363]: canned 'yes:/no:/partly:/maybe I asked wrong' strings; "needed" decided by `text LIKE 'SELECT%' OR LIKE 'WITH%'` vs `changes > 0`; `lower(hw) = lower(word)` -> 'same letters, different case'.
14. Waiting [358/361]: no satwork -> event 'the ask sits in its inbox ... no timer fills it', gap kind 'wait', `run.failed = 1`. v16 [358] refused -> 'the ask never reached its inbox'.
15. Source [366/369]: `LIMIT 8` definition rows become `defrow` inputs; hard words 'source', 'like', 'opposite', 'kind', 'derive', 'deduce'.
16. Agree [367/370]: `count(DISTINCT src) >= 2`, `length(w) > 1`, `LIMIT 14` in the event text.
17. Proc status [368/371 + 375/379]: 3 identical receipts -> 'learned', then 'automated'; step-back picks another row via `mother('SELECT trigger FROM g... LIMIT 1')`.
18. Output composition [371/375]: var 'output' else the words passed, with `'?'` appended to formula-less words; BUILD text = `trim(substr(line, 7, length(line) - 12))` (raw substring of the typed line).
19. Mark rule [371/375]: right/wrong/balanced/shift/unchecked by `output = expected` or last memory.
20. Broken-word gap [372/376]: canned text 'the run passes it and nothing happens. No formula. A broken word.'
21. Canned 'source' formula: v15 [376] `INSERT INTO formula (word, body, ...) VALUES ('source', 'INSERT INTO wn.inbox ( word ) VALUES ( :subject ) ; ... sqldoc.inbox ...')`; v16 [380] the same text typed as a line `INSERT INTO input (line, direction) VALUES ('source = INSERT INTO wn.inbox ...', 'heard')`.
22. v16 only [374] `end_teach`: formula row = pointer `INSERT INTO formula (word, run, origin, t) VALUES (<word>, NEW.run, 'told', ...)`, plus a memory row marked 'told'.
23. Action labels on events ('HEAR WRITE', 'CALL MOVE', 'SPAWN WRITE CALL', 'FIND COMPARE', ...) and all 32/34 narrations are hand-written strings.

Rule-group count: v15 = 21 (items 1-9, 11-21, 23); v16.x = 23 (drops the overwrite, adds 10, 22, the :prev reopen, teach-no-fire, refused).

## 5. Does a run through gates ever assemble SQL text that mother pastes?

**Yes, one path, all versions - the `;` gate inside a formula branch run.** The hop trigger laid on the `;` gate (template in `lay_go`
[349/351]) decodes the receipt rows of the run back into words and writes a `stmt` row:
```
INSERT INTO stmt (run, text) SELECT NEW.run, (SELECT group_concat(w, ' ') FROM (SELECT CASE WHEN e.role = 'var' THEN quote(coalesce((SELECT value FROM var WHERE run = NEW.run AND name = e.word ...), (... parent ...), (... root ...))) ELSE e.word END AS w
  FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run AND r.id >= (SELECT min(r2.id) FROM receipt r2 JOIN encoder e2 ... WHERE ... e2.word IN ('SELECT','INSERT','UPDATE','DELETE','CREATE','WITH') AND r2.id > <last ';'>) ORDER BY r.id))
  WHERE (SELECT kind FROM run WHERE id = NEW.run) = 'formula';
```
then `stmt_go` [355/357]: `INSERT INTO event (...) VALUES ('out', 'output to sources', NEW.run, 'output to sources', 'output to sources: the gates
the run passed decode to "' || NEW.text || '". Mother picks it up.', 'READ SAY', ...); SELECT mother(NEW.text, NEW.run, NEW.id);`.
This is the owner's "string of sql ... put together by the neurons from the run table and outputed as the string to the mother".

Limits of that path:
- Only runs of `kind = 'formula'` (branch runs started by `fire_go` [354/356] from a taught formula). A primary line's `;` writes nothing.
- The words are the ones a human typed after `w = ...`; the brain fills holes (`:run`, `:subject`, ...) from `var` but composes nothing new.
- v15 re-reads the formula from stored text `f.body` [354]; v16 re-reads it from the teaching run's receipts [356]
  `SELECT (SELECT group_concat(w, ' ') FROM (SELECT e.word AS w FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = f.run ORDER BY r.id)) ...`.
- **Neuron birth never uses it**: `born_go` composes CREATE TABLE/VIEW/TRIGGER by template (sec 1); `lay_go` composes the hop trigger by template (sec 2).
  A typed formula `w = CREATE TABLE ... ;` or a `BUILD CREATE TABLE ... BUILD` line would reach mother, but the brain does not do this on its own.
- `BUILD ... BUILD` [371/375 -> `build_go` 373/377] pastes `substr(line, 7, length(line) - 12)`: the typed text, not the gates (the words did pass the gates first).

## 6. Verdicts per version

**v15** (v15.html; told at 833, host 596-707, worker 709-830)
Creation (b) born_go [345] template via mother; hop = per-row `hop_g_s` trigger laid by lay_go [349] template via mother + miss_N per neuron;
mother routes by regex, narrates 6 event kinds, formats, caches, writes secondary/waiting rows, has a silent by-value mode;
run-assembled path exists only for `;` in formula branch runs (stmt_go [355]); 21 hard rule groups, formula bodies stored as text [376],
memory exact-match + expected-answer overwrite [348].
Verdict: real SQLite triggers do all runtime deciding (no JS routing of words), but the brain's births and hops are hand-laid string templates
fired by triggers through mother, formulas hold canned text, and decide/memory/sense are told rules - partially meets the criteria; fails
"a trigger cannot create" and "neurons don't hold canned text".

**v16** (v16.html; told at 803, host 558-675, worker 677-800) - changed from v15:
told block: `formula.body` removed, `formula.run` pointer written by new `end_teach` [374]; teaching runs through the neurons (input_teach
[338] -> run kind 'teach', direction 'start'); fire_go re-reads words from receipts [356]; expected overwrite replaced by `memwrong` history
[349] + `memwrong_go` [350] laying decide's `:prev` row (through a mother template); `secondary_refused` [358]; `COLLATE NOCASE` on words (one gate
per word); 'source' told as a typed line [380]; `;` gate renumbered 66->65 (baked). Host: rethrow on deep recursion (609-612), refused row (627);
worker reads formulas back from receipts. Creation/hop/mother otherwise unchanged (b, per-row trigger).
Verdict: closer on canned text (formula = pointer to a run) and on "history of being wrong", but births, hop triggers and the new decide row
are still trigger-fired templates via mother; 23 hard rule groups - partially meets.

**v16.1** (told 834, host 589-706): brain byte-identical to v16; only drawing changed (labels keep screen size, axes, spacing slider). Verdict = v16.
**v16.2** (told 836, host 591-708): brain identical to v16; drawing adds point gap/spaceApart, zoom range. Verdict = v16.
**v16.3** (told 840, host 595-712): brain identical to v16; page adds the owner's full map (35,597 names, 314,181 edges) as drawing lines, pull
directions per relation kind, 'does' lines. Verdict = v16.
**v16.4** (told 888, host 632-749, worker 751-885): brain identical to v16; worker adds a read-only `atlas` message (866-876) that reads
encoder/gN/sqlite_master/memory/formula/state; page adds the atlas table and layout test hooks. Verdict = v16.

## Compact table

| version | creation | hop | mother extras | run-assembled path? | hard rules | verdict |
|---|---|---|---|---|---|---|
| v15 | (b) born_go [345] template -> mother(); page line 833 | per-DNA-row `hop_g_s` + per-neuron `miss_N`, laid by lay_go [349] via mother(); line 833 | regex `.inbox` routing (632), 6 canned events (633-667), reply formatting (654), secondary/waiting rows (655-669), stmt cache (637-642), silent by-value mode (646-650) | yes, `;` gate in formula runs -> stmt_go [355] -> mother; not for births; BUILD pastes raw text [371] | 21 | SQL does the runtime deciding; births/hops are trigger-fired templates via mother; formulas are canned text; memory overwrite |
| v16 | (b) born_go [346]; also input_teach [338] births the taught word; line 803 | same, lay_go [351]; `;` id 65 baked; line 803 | as v15 (592-633) + rethrow deep (609-612) + refused row (627) | yes, [351]/[357]; formula words re-read from receipts [356]; BUILD raw [375] | 23 | formula = run pointer, wrong-history kept, decide row laid by a told template [350]; births/hops still templates |
| v16.1 | = v16 (line 834) | = v16 | = v16 (623-664) | = v16 | 23 | = v16; drawing only |
| v16.2 | = v16 (line 836) | = v16 | = v16 (625-666) | = v16 | 23 | = v16; drawing only |
| v16.3 | = v16 (line 840) | = v16 | = v16 (629-670) | = v16 | 23 | = v16; owner map drawn |
| v16.4 | = v16 (line 888) | = v16 | = v16 (666-707) + read-only atlas query in worker (866-876) | = v16 | 23 | = v16; atlas added |
