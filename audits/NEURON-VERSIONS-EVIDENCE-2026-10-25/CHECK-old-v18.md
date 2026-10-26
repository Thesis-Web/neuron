# CHECK: the old v18 build (/home/exnulla/neuron/v18-saved/), read-only forensic

Checked 2026-10-25 on copies under
/tmp/claude-1000/-home-exnulla-neuron-v1/95237a7f-7d7c-47a3-a249-06f9202b6633/scratchpad/chk4/src/
(nothing under /home/exnulla/neuron/ was touched). File:line below are relative to /home/exnulla/neuron/v18-saved/.
A live replay was run on a scratch copy (chk4/live/), results in section 7.

Dating (from timestamps stored inside the databases, not file mtimes, which are all the 10-19 copy):
- 10-15 10:40 to 23:05: brain_copy.db (teach_one.sql physics), callout/b.db, kern/*.db experiments
- 10-16 00:05 to 04:25: v18copy/brain.db (neuron.does template + eval)
- 10-16 04:44 to 05:20: own.txt, other.txt (owner's words that set the design below)
- 10-16 06:28/06:29: v18env/, final/ (first build of the word-run physics; persistent triggers)
- 10-16 06:44: v18_deleted_20261016T064420Z (= final/, copied before deletion)
- 10-16 06:47: v2 (TEMP physics); 07:04 to 07:26: v3, brain_v18_before_zero, v18_before_formulas
- 10-16 09:07 to 09:21: v4 (abandoned variant), v5, v6 (= brain_v18_before_try), brain_v18_before_newneuron
- lastnum = 367, n380 = 380: prose counters only (owner prose 363 was saved at 04:47, other.txt:28)

The phrases "the most correct we ever had" and "the cheat" do NOT occur anywhere in this folder
(grep over *.txt *.sql *.sh *.md: no "cheat"; "more correct" only in 352.txt:1 and 356.txt:1, both questions
about other things). The owner's verdict on THIS build (v6/final) is in a later session, not here.

---

## 1. What skull.sql, bones.sql, physics.sql, formulas.sql lay

### v6/skull.sql (4 lines) and final/skull.sql (3 lines): the environment, no tables
```
v6/skull.sql:1  .load ./kernel/eval
v6/skull.sql:2  .load ./kernel/mother
v6/skull.sql:3  PRAGMA recursive_triggers = ON;
v6/skull.sql:4  .read physics.sql
```
final/skull.sql is lines 1-3 only (its physics is persistent, see below). `eval` is loaded but never called by
any physics.sql (grep "eval(" over all .sql outside v19copy: none). Only `mother(` is called.

### v6/bones.sql (16 lines): 4 tables, 1 index, 24 word rows, 0 triggers; laid once, persistent
```
v6/bones.sql:1  -- the bones: laid by hand ONCE. The brain's first run needs them, so it cannot write them itself.
v6/bones.sql:3  -- the word neurons: the only neurons with words. Each word is one neuron; its number is its gate.
v6/bones.sql:4  CREATE TABLE code (id INTEGER PRIMARY KEY, word TEXT NOT NULL UNIQUE);
v6/bones.sql:5  INSERT INTO code (word) VALUES ('CREATE'), ('TABLE'), ('('), (')'), (','), (';'), ('INTEGER'), ('PRIMARY'), ('KEY'), ('TEXT'), ('NOT'), ('NULL'), ('DEFAULT'), ('CURRENT_TIMESTAMP'), ('UNIQUE'), ('TIMELINE'), ('neuron'), ('id'), ('at'), ('gate'), ('born'), ('receipt'), ('words'), ('/build');
v6/bones.sql:8  CREATE TABLE dna (id INTEGER PRIMARY KEY, neuron INTEGER NOT NULL, key INTEGER NOT NULL, dest INTEGER NOT NULL, times INTEGER NOT NULL DEFAULT 1);
v6/bones.sql:9  CREATE INDEX dna_hop ON dna (neuron, key);
v6/bones.sql:12 CREATE TABLE receipt (id INTEGER PRIMARY KEY, path TEXT NOT NULL UNIQUE);
v6/bones.sql:15 CREATE TABLE memory (id INTEGER PRIMARY KEY, receipt INTEGER NOT NULL, neuron INTEGER NOT NULL, result TEXT, times INTEGER NOT NULL DEFAULT 1,
```
Tables: code, dna, receipt, memory. Index: dna_hop. 24 hand-laid word neurons (ids 1-24; 24 = '/build').

### v6/physics.sql (121 lines): 5 TEMP tables, 5 TEMP triggers; re-laid in RAM at every open
```
v6/physics.sql:1  -- the physics: laid by the skull at EVERY open, in RAM. Working rows (ear, need, step, said) never go into the file.
v6/physics.sql:2  CREATE TEMP TABLE ear (id INTEGER PRIMARY KEY, line TEXT NOT NULL, heard TEXT NOT NULL DEFAULT '');
v6/physics.sql:3  CREATE TEMP TABLE need (id INTEGER PRIMARY KEY, word TEXT NOT NULL);
v6/physics.sql:4  CREATE TEMP TABLE step (id INTEGER PRIMARY KEY, run INTEGER, neuron INTEGER NOT NULL, remainder TEXT NOT NULL);
v6/physics.sql:5  CREATE TEMP TABLE said (run INTEGER PRIMARY KEY, receipt INTEGER, line TEXT, result TEXT);
v6/physics.sql:60 CREATE TEMP TABLE frun (id INTEGER PRIMARY KEY, formula INTEGER NOT NULL, word INTEGER NOT NULL, vals TEXT NOT NULL, moment INTEGER, line TEXT, result TEXT, receipt INTEGER);
```
Triggers: `listen` (L9, AFTER INSERT ON ear), `hop` (L22, AFTER INSERT ON step), `end_of_run` (L37, AFTER INSERT
ON step WHEN remainder = ''), `hear_formula` (L63, AFTER INSERT ON ear), `formula_run` (L83, AFTER INSERT ON frun).

### final/physics.sql (62 lines): persistent (non-TEMP) version of the first three; 1 INSERT, 5 tables, 1 index, 3 triggers
```
final/physics.sql:2   INSERT INTO code (word) VALUES ('/build');
final/physics.sql:5   CREATE TABLE step (... remainder TEXT NOT NULL, said TEXT NOT NULL DEFAULT '', result TEXT, at ...);
final/physics.sql:8   CREATE TABLE dna (...);          final/physics.sql:9  CREATE INDEX dna_hop ON dna (neuron, key);
final/physics.sql:12  CREATE TABLE memory (id, run, neuron, said TEXT NOT NULL, result TEXT, times, first_at, last_at, ended_at);
final/physics.sql:17  CREATE TABLE ear (... first INTEGER, at ...);   final/physics.sql:18  CREATE TABLE need (id, ear, word, at);
final/physics.sql:22  CREATE TRIGGER listen ...   :36  CREATE TRIGGER hop ...   :52  CREATE TRIGGER end_of_run ...
```
final/ has no bones.sql; its brain.db got `code` (22 words) typed by hand before step 3 (brain_v18_before_step3.db
= code only, 22 rows). v18env/ and v18_deleted_20261016T064420Z/ carry byte-identical physics.sql (diff: IDENTICAL).

### v6/formulas.sql (13 lines): 2 TEMP scratch tables, 3 rows INSERTed into `formula`
```
v6/formulas.sql:1  -- the formula nodes, told once: from a word, by a key, a head (the long run) and a row with its holes (var, now)
v6/formulas.sql:3  INSERT INTO fw VALUES ('new', 'word',   'INSERT INTO code ( word ) VALUES',            '( var )'),
v6/formulas.sql:4                        ('new', 'neuron', 'INSERT INTO neuron ( gate , born ) VALUES',   '( var , now )'),
v6/formulas.sql:5                        ('now', NULL,     'SELECT max ( id ) + 1 FROM TIMELINE',         NULL);
v6/formulas.sql:8  INSERT INTO formula (neuron, KEY, head, row)
```
The `formula` table itself is not in formulas.sql; it was built by a typed run (run_step.sh:8, receipt 3 below).

### Per-neuron vs shared: NO table is per-neuron in this build
All tables are shared. A word neuron is a ROW of `code` ("Each word is one neuron; its number is its gate",
bones.sql:3). A graph neuron is a ROW of `neuron`. A neuron's DNA is its rows in the one `dna` table, keyed
(neuron, key). The only per-thing tables anywhere in the folder are the 10-15 scratch experiments
kern/t.db `mem_7`, kern/u.db `mem_9`, callout/b.db `memory_xyz`, made by the `does`-template approach (sec 2d).
The parallel session argued against per-neuron tables in the owner's own paste, 350.txt:12:
"The 'dna inside a neuron' is that neuron's rows. The same goes for 'each memory its own table' [334]: you'd be
typing every CREATE yourself forever, which is exactly the trap you're describing."

Tables the brain built itself (sqlite_master in v6/brain.db keeps the run's spacing, one space around every token):
```
table|TIMELINE|CREATE TABLE TIMELINE ( id INTEGER PRIMARY KEY , at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP , receipt INTEGER , words TEXT )
table|neuron|CREATE TABLE neuron ( id INTEGER PRIMARY KEY , gate TEXT UNIQUE , born INTEGER )
table|formula|CREATE TABLE formula ( id INTEGER PRIMARY KEY , neuron INTEGER NOT NULL , KEY INTEGER , head TEXT NOT NULL , row TEXT )
```
versus the hand-laid `CREATE TABLE code (id INTEGER PRIMARY KEY, word TEXT NOT NULL UNIQUE)` (bones spacing).

---

## 2. How a new neuron is created when an unknown word arrives

Short answer: an unknown word does NOT create a neuron. It becomes a `need` row and listening stops. A new word
neuron is born only when the brain is TOLD `new word X /build`, which is a formula run. Tables and the first graph
neuron (zero) were built by mechanism (a): a typed line of word-neurons, hopped word by word into the `step` table,
concatenated back into a string at the end of the run, and handed to the C function `mother(sql)` which executes it.
But the hand-off is a function call INSIDE the end_of_run trigger, and two places hand the mother a template filled
inside the trigger (b). The typing itself was done by the builder's shell script (c).

### (a) the run assembles the string, the mother executes it
Encoder = `listen` trigger. Space is the hop; a known word becomes its number; unknown word -> need:
```
v6/physics.sql:7-8   -- listen: take the first word off the line (the space is the hop). ... A known word becomes its number;
                     -- an unknown word is a need and listening stops; a last word of /build starts the run at /build with everything heard.
v6/physics.sql:13-15   INSERT INTO need (word)
                         SELECT substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1)
                         WHERE NOT EXISTS (SELECT 1 FROM code WHERE word = substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1));
v6/physics.sql:16-17   INSERT INTO step (neuron, remainder)
                         SELECT c.id, NEW.heard FROM code c WHERE c.word = '/build' AND NEW.line = '/build' AND NEW.heard <> '';
```
Run table = `step`; the line is put back together from the run's steps and given to the mother:
```
v6/physics.sql:34-35 -- end: nothing remains. The receipt is written once (the run's numbers); the line is put together once from the run's words;
                     -- a run that began at /build hands it to the mother.
v6/physics.sql:41        (SELECT group_concat(w, ' ') FROM (SELECT c.word AS w FROM step s JOIN code c ON c.id = s.neuron WHERE s.run = NEW.run ORDER BY s.id));
v6/physics.sql:42-43   UPDATE said SET result = mother(line)
                         WHERE run = NEW.run AND (SELECT neuron FROM step WHERE id = NEW.run) = (SELECT id FROM code WHERE word = '/build');
```
final/physics.sql accumulates the said text hop by hop instead (final/physics.sql:45 `ltrim(NEW.said || ' ' || c.word)`)
and hands it over at final/physics.sql:53 `UPDATE step SET result = mother(NEW.said)`.

Evidence in the data (v6/brain.db, receipt decoded to words; memory.result = mother's answer):
```
receipt 1: CREATE TABLE TIMELINE ( id INTEGER PRIMARY KEY , at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP , receipt INTEGER , words TEXT ) ; CREATE TABLE neuron ( id INTEGER PRIMARY KEY , gate TEXT UNIQUE , born INTEGER ) ;   -> memory 1 result ok (07:04:21)
receipt 2: INSERT INTO neuron ( gate , born ) VALUES ( 0 , ( SELECT max ( id ) + 1 FROM TIMELINE ) ) ;   -> memory 2 ok; neuron row 1|0|2 (zero born at moment 2, 07:26:58)
receipt 3: CREATE TABLE formula ( id INTEGER PRIMARY KEY , neuron INTEGER NOT NULL , KEY INTEGER , head TEXT NOT NULL , row TEXT ) ;   -> ok
```
Who typed those lines: the builder's script, run_step.sh:8-9 and :13, not a person at the prompt:
```
run_step.sh:7   "INSERT INTO code (word) VALUES ('var'), ('now'), ('new'), ('code'), ('word'), ('formula'), ('head'), ('row');" \
run_step.sh:8   "INSERT INTO ear (line) VALUES ('CREATE TABLE formula ( id INTEGER PRIMARY KEY , neuron INTEGER NOT NULL , KEY INTEGER , head TEXT NOT NULL , row TEXT ) ; /build');" \
run_step.sh:13  "INSERT INTO ear (line) VALUES ('new word read write end find count forget same if do again hear say hold get put /build');"
```
run_step.sh:7 is a direct INSERT into `code` (8 word neurons laid by SQL, not by a run).

### (b) templates inside triggers, executed by the host function
The timeline row is a printf template in the physics trigger itself:
```
v6/physics.sql:51  SELECT mother(printf('INSERT INTO TIMELINE (receipt, words) VALUES (%d, %Q)', s.receipt,
```
The formula shortcut fills holes (`var`, `now`) by string replace inside the trigger, then hands it to the mother:
```
v6/physics.sql:80-81 -- the formula run. The long way once: the first time, its words are walked one by one (shards, a receipt, a memory).
                     -- Then the shortcut: the head, and one row per value with var = the value and now = this run's moment, handed to the mother.
v6/physics.sql:94        SELECT trim(replace(replace(' ' || rw.w || ' ', ' var ', ' ' || quote(v.value) || ' '), ' now ', ' ' || fr.moment || ' ')) AS x
v6/physics.sql:102   UPDATE frun SET result = mother(line) WHERE id = NEW.id AND line IS NOT NULL;
```
This is how word neurons 25-60 and graph neurons at gates 5 and 7 were born: receipt 6 `new word /build : read write end find count forget same if do again hear say hold get put` -> ok (15 word rows); v5/brain.db receipt 9 `new neuron /build : 5` -> neuron 2|5|9; v5 receipt 7 `new word /build : dog` -> code 57 dog, and a second `new word dog` -> memory 12 `error: UNIQUE constraint failed: code.word` with memory 7 ended_at set (a refusal remembered, a truth ended).

### (c) outside code
No Python or JS anywhere (find *.py *.js: 0). C: only mother.c/eval.c (exec, sec 4). Shell: run_step.sh (the builder
typing the runs and swapping physics files, lines 5 and 11), and the older callout/hand.sh:
```
callout/hand.sh:2  # the hand: runs whatever SQL the brain wrote into call, in order, then marks it done. decides nothing.
callout/hand.sh:6  sqlite3 "$db" "SELECT sql || ';' FROM call WHERE done IS NULL AND id <= $max ORDER BY id" | sqlite3 -bail "$db" \
```
callout/b.db (10-15 23:05) is that variant: a `fire` trigger writes a `printf('CREATE TABLE %s ...', NEW.carry)` row into
`call`, the shell runs it. Abandoned before other.txt.

### (d) the earlier variants kept in the folder
- brain_copy.db / teach_one.sql (10-15): `excite` trigger births a neuron by gate arithmetic, no SQL string at all:
  teach_one.sql:5-7 `INSERT OR IGNORE INTO neuron (gate, born) SELECT CAST(CAST(n.gate AS INTEGER) + NEW.remainder AS TEXT) ...`.
  3 neurons at gates 0,1,2; 3 dna; 8 steps. This is what the owner rejected in 362.txt ("you are short cutting the run").
- v18copy/brain.db (10-16 00:05-04:25): one trigger `excite AFTER INSERT ON step BEGIN ... SELECT eval(replace(does, ':S:', NEW.id)) FROM neuron WHERE id = NEW.neuron AND does IS NOT NULL; END` with neuron 1's `does` =
  `INSERT OR IGNORE INTO neuron (gate, born) SELECT CAST(value AS TEXT), (SELECT max(id) FROM TIMELINE) FROM step WHERE id = :S:` -- the exact line the owner quotes in other.txt:56. Pure (b): a code string stored on the neuron row, run by eval from inside the trigger. Neuron 3 at gate 0 born this way at 04:25.
- kern/t.db, u.db, v.db: same `fire`/`eval(replace(does, '$', NEW.carry))` pattern with `/table`, `/remember`, `/grow`, `/on`, `/off`, `/attach`, `/longterm` neurons; u.db has 100,007 hits (a speed test). These are the "neuron that calls out and writes sql" the owner asked about in 350.txt:51-52.

---

## 3. The hop

One hand-laid trigger for the whole brain, recursive through `PRAGMA recursive_triggers = ON` (skull.sql:3). Not per
row, not per neuron, no C walker, no shell loop.
```
v6/physics.sql:20-21 -- hop: the key is the head of the remainder. A shard from here by that key: walk it again (times + 1). No shard: lay it.
                     -- Land on its next gate with the rest of the remainder.
v6/physics.sql:22  CREATE TEMP TRIGGER hop AFTER INSERT ON step WHEN NEW.remainder <> '' BEGIN
v6/physics.sql:23-24   UPDATE dna SET times = times + 1
                         WHERE neuron = NEW.neuron AND key = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER);
v6/physics.sql:25-28   INSERT INTO dna (neuron, key, dest)
                         SELECT NEW.neuron, c.id, c.id FROM code c
                         WHERE c.id = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER)
                           AND NOT EXISTS (SELECT 1 FROM dna WHERE neuron = NEW.neuron AND key = c.id);
v6/physics.sql:29-31   INSERT INTO step (run, neuron, remainder)
                         SELECT coalesce(NEW.run, NEW.id), d.dest, ltrim(substr(NEW.remainder, instr(NEW.remainder || ' ', ' ') + 1))
                         FROM dna d WHERE d.neuron = NEW.neuron AND d.key = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER);
```
Reading: the remainder is the typed line as numbers; each hop bites off the head, bumps or lays the dna row
(neuron, key), inserts the next step on `dest`, and the insert fires `hop` again. Note L26: `dest = c.id = key`:
the destination is always the key word itself, so the dna row never changes where the run goes; the typed remainder
alone decides the path. The dna in this build is a trace of word-after-word (74 rows in v6, e.g. `/build->CREATE x2,
CREATE->TABLE x3, ( -> id x5`), not a chooser. A line of N words costs N nested trigger levels; SQLite stops at 1000
(344.txt:2 mentions the limit); untested here.

run_step.sh is NOT a hop loop: it is a one-shot teaching sequence (3 ear lines + `.read formulas.sql`, then swaps in the
formula physics and types one 16-word line). The 10-15 `excite` trigger (teach_one.sql:3-15) was the earlier hop: numeric
remainder added to the gate, one hop then stop (`SELECT dest, NULL, ...` at :14).

---

## 4. kernel/

v6/kernel/ = final/kernel/ = v2..v5/kernel/ (diff: IDENTICAL): mother.c (18 lines), eval.c (125 lines), sqlite3.h,
sqlite3ext.h, mother.so, eval.so (x86-64 ELF). eval.c is SQLite's stock ext/misc/eval.c ("2014-11-10 ... implements SQL
function eval() which runs SQL statements recursively", v6/kernel/eval.c:1-15). It is loaded by skull.sql:1 but never
called by any physics. mother.c, whole function:
```
v6/kernel/mother.c:1-2  /* mother(sql): the brain hands SQL text to the mother. She runs it and answers
                           'ok' or 'error: ...'. She never stops the brain, so a refusal can be felt and remembered. */
v6/kernel/mother.c:9    if(sqlite3_exec(sqlite3_context_db_handle(ctx), sql, 0, 0, &err) != SQLITE_OK){
v6/kernel/mother.c:13   sqlite3_result_text(ctx, "ok", -1, SQLITE_STATIC);
```
Exec-only. No parsing, no choosing, no walking, no table of her own. She does not route or traverse either: the
traversing is the `hop` trigger; she is a sink that runs a string on the same connection and returns ok/error.

Other C in the folder: step1/eval.c (16 lines) and kern/eval.c (17 lines), minimal `eval(sql)` wrappers (exec, return 1);
own/neuron.c (17 lines) is the "own kernel" idea from 354.txt: `/* neuron.c: functions compiled INTO the brain's own
sqlite3. Today: eval. Later: neuron functions. */` using `sqlite3_auto_extension` so "every connection gets eval"
(own/neuron.c:16); own/neuron is a built sqlite3 3.37.2 binary with `EXTRA_INIT=neuron_init` (strings). Also exec-only.
dl/ holds the sqlite-amalgamation-3370200 it was built from.

---

## 5. How formulas were taught

By SQL written by the builder, not by typed runs through neurons.
- The formula TABLE: a typed run (run_step.sh:8 -> receipt 3 -> mother -> `CREATE TABLE formula ( ... )` in sqlite_master).
- The formula ROWS: v6/formulas.sql:3-5 lists head/row as text, :6-7 tokenizes with json_each into code ids, :8-12 INSERTs
  3 rows into `formula`; executed by `.read formulas.sql` (run_step.sh:10). The 8 words those rows need (`var now new code
  word formula head row`) were INSERTed straight into `code` (run_step.sh:7), not born by a run.
- Resulting rows (v6/brain.db, decoded): `new|word|INSERT INTO code ( word ) VALUES|( var )`;
  `new|neuron|INSERT INTO neuron ( gate , born ) VALUES|( var , now )`; `now||SELECT max ( id ) + 1 FROM TIMELINE|`.
- Using a formula afterwards is a run: hear_formula (v6/physics.sql:63-78) picks the formula by first word + key, strips
  ' /build' by `length(r1) - 6` (:69-70); formula_run (:83-121) walks the head+row words once "the long way" (:84-87,
  receipt 5 `INTO code ( word ) VALUES ( var )`, memory 5 result NULL) and then fills the template and calls mother (:89-102).
- teach_one.sql is not a formula file: it is the 10-15 physics (step table + excite trigger), identical to brain_copy.db's
  schema. Its name refers to teaching one hop.

---

## 6. The owner's own words in this folder

Which numbered files are what: 343-362 are all owner prose "extracted verbatim from the session .jsonl" (footer on each),
session 69692be7 (neuron-v18 hand-build), 10-15 14:52 to 23:44. Three carry pasted replies of the parallel session plus
the owner's words: 350 (paste + "I think we should delete..." + a question), 351 (paste only, "the owner words + a quoted
line of the parallel session"), 355 (paste; owner's words are the last line "you need to read this..."). 354 and 361 begin
with a quoted line of Claude's reply. 347 contains a pasted sqlite transcript. None is a pure log. other.txt is 11
messages 10-16 04:45-05:20; own.txt is two short owner lines saved 04:44.

Judgements of the state of the build at the time (10-15, before v6 existed):
- 343.txt:1 "I think if you use a walker you are telling the brain what to do.... and from that point on it can only do what its told,,,, it cannot think for itself, choose and decide"
- 348.txt:1 "the point is we have a single neuron yes, and it was hand laid, and the brain has learned nothing.... it doesn't understand not one thing about how to do that process" ... "in order to make the zero node, it should have been told by it's neurons to build it... not me or you hand typing in the sqlite"
- 350.txt:45 "I think we should delete the neuron 17 and start over.. because we started wrong, and will forever try to fix it.. instead of building it correct the first time"
- 350.txt:51-52 "are you saying it's impossible to have a neuron that calls out and writes sql? why not?"
- 352.txt:1 "so one of you is saying temp trigger and one of you is saying eval... which is more correct to the scope of the project? is there yet another way..."
- 360.txt:1 "there is exactly one way to build it correct and we don't know it. so your guesses build it incorrect every time."
- 361.txt:1 "are you saying it can't be built in sql? do we need to build our own db? kernal? ... let's get back to v 18.. where are we at there?"
- 362.txt:1 (on the excite/arithmetic neuron, brain_copy.db) "you laid the first neuron and you chose to do it incorrectly because we just don't know the correct way to do it.. but in reality ... I thing it will still be wrong... because you are short cutting the run.. the neurons didn't excite to lay the chard, buil the nueron... ... the brain will not know how to build it's own neuron... it will know a Phase that builds a nueron.. a means something, neuron means something, is means something, born means something ..."

The design words that v2-v6 were built from (10-16 morning):
- other.txt:19 "you really wanted to just run away with it.. I gave you a chance and two turns in it failed with drift.. so we are back on 18, and honestly about to delete it and start over. but in a good way"
- other.txt:33 "the first neurons actually don't live "in" the graph.. they are the physics... the just live.... first neurons will be hand laid"
- other.txt:56 "I see this as we need /insert /or /ignore /into /NEURON<---because it's a skill.... /( /gate /, /born /) /select ... <--- ok use slash here for emphsis on the code as neurons.... ... each one of those / is a neuron + /space <-- just the space bar input... ... if I were to insert /build INSERT OR IGNORE INTO neuron (gate, born) SELECT ... as a prompt to the brain.. The brain would write that output to the sqlite and build it's own neuron? yes we would have to hand lay all those neurons... and /build <--- or whatever it needs to be... but it's meaning is everthing after this is code that you will lay outside to sql.. maybe /space is "hop" ? ... I don't think the call out code at first fits into the "graph".. its essentially the mother, even though it's inside the db... it's a must have to start the process. am I wrong? do we need env to do this?"
- other.txt:85 "so correct neuron form - INSERT OR IGNORE INTO neuron (gate, born) SELECT CAST(value AS TEXT), (SELECT max(id) FROM TIMELINE) FROM step WHERE id = :S: /build ... the /build tail in the encoder is the switch to pass through those word gates as words. ... no slash build = hit the graph, with /build hits the code??? maybe it works. ... I think we are close? we know everthing but the hop?"
- own.txt:1-5 "try it" (line 2191) / "ok you need to be cleared, but i need you ready for it" (line 2222)

The later verdict words ("most correct we ever had", "bones.sql and physics.sql are the cheat") are not in this folder.
What the folder shows is consistent with that later reading: bones.sql and physics.sql are the parts a person wrote
(4 tables, 5 triggers with the encoder, the hop, the end-of-run, the formula matcher and the template fill), and
"the cheat" fits sec 2b/5: matching, templating and the mother call live in those hand-written triggers.

---

## 7. Verdict against the four criteria, and the database evidence

1. prompt -> encoder -> brain: PARTLY. Prompt = the sqlite3 shell (`INSERT INTO ear (line) VALUES (...)`), encoder = the
   `listen` trigger inside SQLite (space = hop, word -> number, unknown -> need), brain = shared tables. But a neuron is a
   ROW (code / neuron), not a table per neuron; dna rows are (neuron, key, dest, times), the remainder rides on the step
   row; no "arrival" column. And the typing was done by the builder's script (run_step.sh), not by the owner at the prompt.
2. "A trigger cannot create... a string of sql happens as a run put together by the neurons from the run table and
   outputed as the string to the mother": HALF. The string IS assembled from the run table (step -> group_concat of the
   words, v6/physics.sql:41; final/physics.sql:45 word by word) and IS what the mother runs. But the hand-off is
   `mother(line)` CALLED FROM INSIDE the end_of_run trigger (:42, final:53): the trigger makes it happen. Two more places
   hand the mother a template the trigger filled itself (:51 printf for TIMELINE; :89-102 var/now replace for formulas).
3. Mother "just a router and a traverser... works no data, decides nothing": she decides nothing and works no data
   (mother.c:9-13, exec + ok/error). But she neither routes nor traverses: the hop trigger traverses, the listen trigger
   routes (word vs formula vs need). She is less than the owner's mother (a bare executor), and she is a C host
   function, not SQL.
4. Only hand-laid: run table, hop, trigger; everything else by typed runs; no outside code thinking: PARTLY. Hand-laid
   here: 4 bones tables + index + 24 words (bones.sql), 5 temp tables + 5 triggers (physics.sql), 8 more words and 3
   formula rows by direct SQL (run_step.sh:7, formulas.sql), 2 C functions (exec only), and the shell that typed the
   runs. Brain-built by runs: TIMELINE, neuron, formula tables; neuron zero (and gates 5, 7 in tests); 32 word rows
   (code 25-56 via `new word`, 57-60); all dna rows; receipts, memories. No Python/JS anywhere. The thinking that does
   exist (word lookup, formula pick by key, hole filling, printf) is in the hand-written triggers, which is the owner's
   362 objection in SQL form: the brain knows a phrase, not how to build the phrase.

### Database copies (internal timestamps; counts = rows)
| copy | when (10-) | physics | tables | counts | run-built tables / neurons |
|---|---|---|---|---|---|
| brain_copy.db | 15 10:40-22:56 | excite, gate arithmetic (teach_one.sql) | neuron, TIMELINE, definition, dna, step | n3 t5 def0 dna3 step8 | neurons 2,3 born by trigger arithmetic; no SQL string |
| callout/b.db | 15 23:05 | fire -> call rows, hand.sh runs them | call, neuron, hit, memory_xyz | call2 n2 hit1 mem1 | memory_xyz + trigger grew by shell hand |
| kern/t,u,v.db | 15 | fire -> eval(replace(does,'$',carry)) | neuron, hit, mem_7 / mem_9 / plain | u: hit 100007, plain 100000, mem_9 100002 | per-thing tables by does template |
| v18copy/brain.db | 16 00:05-04:25 | excite -> eval(replace(does,':S:',id)) | TIMELINE, neuron(does), step | t3 n3 step2 | neuron 3 at gate 0 by template on neuron 1 |
| v18env/brain.db | 16 06:28:59 | final/ physics, persistent | code step dna memory ear need + TIMELINE neuron | code23 dna29 ear120 step117 mem2 need1 | TIMELINE+neuron by run 1 (ok); same line typed 3x -> 'error: table TIMELINE already exists' x2, memory 1 ended, memory 2 times 2; 'CREATE TABLE dog' -> need dog |
| final/brain.db = v18_deleted | 16 06:29:22 / 06:44 | same | same | code23 dna29 ear39 step39 mem1 n0 t0 | TIMELINE+neuron built; zero never born |
| v2/brain.db | 16 06:47:37 | TEMP physics v2 | code dna receipt memory + TIMELINE neuron | code24 dna33 rec1 mem2 t3 n0 | run 1 ok, then 2 errors (line retyped) |
| brain_v18_before_zero.db | 16 07:04:21 | v6-type | + TIMELINE neuron | code24 dna33 rec1 mem1 t1 n0 | TIMELINE+neuron built, zero not yet |
| v3 / v18_before_formulas | 16 07:04-07:26 | v2/v3 physics (no formulas) | + TIMELINE neuron | code33 dna54 rec2 mem2-3 t2-3 n1 | neuron 1|0|2 (zero born at moment 2 by typed INSERT run) |
| v4/brain.db | 16 | variant: neuron table in bones, 32 word neurons | neuron code dna receipt memory TIMELINE | n33 code32 dna46 rec2 mem2 t2 | abandoned (bones differ, v4/bones.sql:3-14) |
| v5/brain.db | 16 09:07-09:08 | v6 physics + formulas | + formula | code57 dna77 rec11 mem12 t12 n2 | neuron 2|5|9 via `new neuron 5`; word dog; UNIQUE error remembered, memory 7 ended |
| v6/brain.db = brain_v18_before_try | 16 09:09:07 / 09:09:15 | v6 physics + formulas | code dna receipt memory TIMELINE neuron formula | code56 dna74 rec6 mem6 t6 n1 f3 | TIMELINE, neuron, formula built by runs; 15 words via `new word` |
| brain_v18_before_newneuron | 16 09:21:57 | same | same | code60 dna74 rec9 mem9 t9 n1 f3 | + `now /build` -> 'now 8'; `new word UPDATE SET DELETE WHERE` |
| q.db | - | - | a | 1 | scratch |

### Live replay on the scratch copy (chk4/live, from v6; sqlite3 3.37.2, mother.so/eval.so load fine)
- `CREATE TABLE cat ( id INTEGER PRIMARY KEY , born INTEGER ) ; /build` with `cat` unknown: need = cat; no table, no run.
- `new word cat zork /build`: code 57=cat, 58=zork; TIMELINE 7 `new ok`; receipt 7 `36 38 24 : cat zork`.
- `new neuron 7 /build`: long walk once (receipt 8 `INTO neuron ( gate , born ) VALUES ( var , now )`, TIMELINE 8 `INSERT`),
  then neuron 2@7 born 9.
- `now /build`: `now 11`.
- Retyped the CREATE cat line: sqlite_master now has `CREATE TABLE cat ( id INTEGER PRIMARY KEY , born INTEGER )`;
  TIMELINE 12 `/build ok`; new dna shards `TABLE->cat`, `cat->(`. Typed once more: memory 13 `error: table cat already
  exists`, memory 12 ended_at set, TIMELINE 13 `/build error`. The physics behaves exactly as its comments say.
