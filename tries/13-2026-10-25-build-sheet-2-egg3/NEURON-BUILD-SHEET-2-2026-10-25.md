# NEURON BUILD SHEET 2

2026-10-25, evening. For you to build by hand at the prompt, and for the audit team first. Every block below was typed today in this order, on the hub (SQLite 3.37.2) and on the hp (SQLite 3.46.1), and the outputs shown are what came back. Nothing here is from my notes or summaries. Where a step is your design, your words are quoted with the time you typed them (10-19/20 is the night you built v1; §n is the reference draft, NEURON-REFERENCE-DRAFT-1-2026-10-23.md; "handoff §0" is your own paragraph in NEURON_BUILDER_HANDOFF_2026-10-20.md). Where a step is mine, it says **mine**, so you can strike it.

All files are in `NEURON-BUILD-SHEET-2-2026-10-25\` beside this sheet and pasted in full in the appendices, so the sheet alone builds it. The 10-25 sheet and its folder are untouched.

## What changed since the 10-25 sheet, and whose words asked for it

| Change | Asked for by |
|---|---|
| `later` is gone. Mother runs the text and answers; she holds nothing back and queues nothing. | You, 10-26 00:41: "a2 ... why is the later queue needed". §2.6: "She works no data." |
| `output` and `secondary` are gone. What the SQL prompt answers to a BUILD, and what a source sends back, come into the brain as runs (rows of `input` with a parent), so the brain hears them the way it hears you. | Handoff §0: "the bottom is permitted to have a sql output that inputs an error, or a response from sql back to the neuron graph". You, 10-25 03:55: the return from a source is "delivered to the encoder then the encoder delivers the words as a run to that brain". |
| No table but the encoder holds a word. Every table a neuron owns is named by a gate number; the typed line's text is let go once it is encoded; cells hold numbers; replays are typed as gate numbers. Checked: no column outside `encoder` holds text with letters. | §2.5: "The shipped brain holds no words at all. You're just going to see numbers in a database and an encoder." Audit point A1. |
| A cell is read from the run itself, else from the run that fired it, and so up; an unresolved `var x` stays as typed and SQL refuses it. | Audit point A4; you, 10-19 23:08: "the newest memory at var a". |
| The runs after the bare core are in the sheet and were typed: the end run (memory + timeline), the write-the-dna line, the define run that writes the definition node. | You, 10-26 00:41: "I need those prompts from that point that creates the runs in the brain to create these Definition/memory/timeline". Handoff §0's order. |
| The egg is the core minimum: the ear, the encoder, one counter, the receipt, the sheet; seven physics neurons; BUILD, var, the digits, and the tokens of the born run. The extra SQL words (DROP, ALTER, DELETE, VALUES, INTO, ON, …) and the letters g t d m are out; they are born when typed. | You, 10-26 00:41: "spec says core min... not plus bloat, invention, drift". |
| Every rule inside every hand-laid trigger is listed one line at a time in §1b with your words or **mine** beside it. | You, 10-26 00:41: "build_go <-- ... explain???" |
| The negative control is written as a test with its rows (§17). | Audit, gate 3. |
| What the brain cannot do mid-run is stated as a measured fact with the test, and the way through is your words, not a work-around (§13). | You, 10-26 00:41: "you have fought me on all the things a database cannot do". Law 11: "An impossible output means ask how. Never work around it." |

Not changed: a neuron is its own DNA table with a gate view and one trigger; births are the born run replayed; BUILD…BUILD is the run's words handed to mother; the hop is hit-or-write on (arrival, remainder); shards are one sequence; spaces and punctuation are neurons.

## 0. What you are building

```
you type a line
   │
   ▼  ear: the line goes into input. The encoder is the conversion table: each word is looked up and
   │       gets its gate number, a new word a new number; a word ends where the next gate begins, and the
   │       space, every digit and every punctuation mark are gates. The text is let go; the numbers stay.
   │       The run hops from where it arrived (heard, said, a source, build) to its first gate.
   ▼
 gate N  (a view: the neuron's entry) ──trigger "N"──▶ DNA table (its own number): hit the row (arrival, remainder)
   │                                                     if it exists, write it if not (shard = next number)
   ▼
  hop  ──▶ receipt (run, gate, shard)
       ──▶ if the row's trigger column names a neuron: fire = type that neuron's bound run as a sub-run (arrives from said)
       ──▶ if this is the second BUILD of a pair: build = the words between go to mother → SQL prompt → her answer comes
           back as a run (arrives from build)
       ──▶ if the run has no remainder and arrived from heard or a source: fire end = type end's bound run (the memory run)
       ──▶ if the next gate has no neuron: born = write four numbers as cells, fire born's bound run (the born run)
       ──▶ land on the next gate (through mother, because a table named by a value needs the SQL prompt)
   ▼
 mother: runs the text she is handed, answers ok / the rows / error: … . When a source's outbox is written she carries
         its rows into input as runs arriving from that source. Decides nothing, keeps nothing.
```

Your words for the whole: "prompt ---> encoder ---> brain" (10-25). "THE PHYSICS OUTSIDE THE DATABASE IS A HANDLER THAT JUST TAKES AN INPUT FROM A SPECIFIC OUTPUT OF THE DATABASE... AND WRITES IT TO SQL... I NEED TO HAND LAY A TABLE IN SQL, THAT IS FINE, BUT THE VERY NEXT THING, IS THAT WE WILL HAND LAY ALL THOSE SAME WORDS AS NODES SO THE BRAINS CAN LAY IT'S OWN TABLES" (10-19 21:20).

What this sheet shows, and only this: the mechanism, line by line, with its rows. A neuron is its own table (§4, §9). A run assembles the SQL and mother pastes it, births included (§7-§9). Mother decides nothing (appendix A, 70 lines, read it). Only the table-making neurons, the hop and the trigger are hand-laid (§1). The memory and timeline are written by a run you type (§10). A definition node is filled by a run you type (§11). It does not show the brain finding a meaning, understanding it or applying it; nothing has (§9 of the draft).

## 1. What is hand-laid, and whose it is

| Hand-laid | What it is | Your words |
|---|---|---|
| `input` | the ear: id, parent, arrival, gates, text (text is NULL once encoded) | "make a bottom that takes an input and writes that input into the brain.db" (21:04); "every punctuation, special char, all of it has to have it's own neuron" (23:08); arrival = heard or said: §2.1 "The first word of a line arrives from the direction word" |
| `encoder` | gate ↔ word. The only table that holds words. A neuron's three tables are labelled here as `word.dna`, `word.definition`, `word.memory` (**the labels are mine**) | "we need to make the decoder encoder, and the prompt" (20:55); §2.5 "The encoder holds the words" |
| `shards` | one counter for the whole brain | "shard numbers are sequential" (00:34) |
| `receipt` | run, gate, shard, in order | "the run reciept should be... we need to know the gate before and after" (00:31) |
| `sheet` | the cells: run, name (a gate number: the cell's word), value. `var a` in a line reads cell a | "if create table (var a) .. then it would create a table of what ever is sitting at the newest memory at var a" (23:08); §3.3 "a table whose cells the triggers write to" |
| 72 neurons, each: gate view `"N"`, DNA table (own number), definition node (own number), memory node (own number), one trigger `"N"`, first shard → definition node | heard, said, hop, born, fire, end, build; BUILD, var, 0-9, and the other 53 distinct tokens of the born run | "EACH NEURON HAS A GATE... IN SIDE THAT NEURON IT HAS DNA" (21:14); "a new gate, new dna table and new defintion node is born all at the same time" (23:40); "does it have a memory node for a definition created at the same time? and a memory node" (21:31); "( , integer , primary, key, arrival, interger, remainder, next, trigger, =, and new, ., trigger, end, ; ... all neurons of their own" (23:03); digits: §3.9 "The brain holds the digits 0 to 9" |
| the landing on a gate (same text for every neuron, only the numbers differ; I wrongly called it "the gate trigger, one per neuron": triggers are on DNA rows, one, none or many) | hit the DNA row if (arrival, remainder) exists, write it if not, hand the run to hop | "if chard exists hits the chard, if not writes it" (01:22); "each neuron has one table and one trigger" (23:27) |
| `hop`, `born`, `fire`, `build` views and their triggers | the physics neurons' gates. §1b lists every statement in them | "hop should be it's own neuron... every action is its own nueron" (23:00); "triggers born, if table doesn't exist" (01:22); "a column in the dna chard table just pointed to that trigger neuron" (23:27); "IT WILL FINISH AT BUILD... THE OUTPUT OF THE RECIEPT WILL BE THE RUN" (21:52) |
| mother | one C function, 70 lines, appendix A | handoff §0: "the bottom is permitted to have a sql output that inputs an error, or a response from sql back to the neuron graph"; §2.6 "just a router and a traverser" |

**Not hand-laid, typed by you (all in this sheet):** the born run (§7), the binds (a run's number into a neuron's memory node), the write-the-dna lines (a row's trigger column), the timeline table, the end run (memory + timeline), the define run, and every formula after these.

### 1b. Every rule inside the hand-laid triggers

The audit's question was whether `build_go` and its kin are "a run through the neurons again" or code the brain cannot change. They are SQLite triggers inside brain.db (the brain can read them in `sqlite_master`, and could drop and recreate them through BUILD once a DROP can run, §10). But they are hand-laid, so each statement in them is listed here. Strike any line marked mine and I will take it out.

**The landing on gate `"N"`** (I called this "the gate trigger, one per neuron"; that name is wrong: triggers live on DNA rows, one, none or many per row. This is the landing physics, the same text for every neuron, typed by the born run):
1. Write the row (arrival, remainder) into the DNA table if it is not there, shard = counter + 1. Your 01:22 and 00:34.
2. Bump the counter if a row was written. Your 00:34 "sequential".
3. Hand the run to hop with run, gate, arrival, remainder, rest. Your 01:22 ("I probably forgot hop, but that's in there also").
Each write goes to mother as its own statement. **Mine, measured:** SQLite keeps an INSERT's cursor open until its statement ends; written inline, 2,400 hops took 106 s on 10-25 and 3.7 s this way.

**`hop_go`** (the hop neuron):
1. Receipt: the row's shard is written to receipt. Your 00:31.
2. Fire: if the row's trigger column is not NULL, fire gets (run, target, gate, arrival, remainder, rest, shard). Your 23:27 (the pointer column).
3. Build: if this gate is BUILD and the run has now hit BUILD an even number of times, build gets the run. Your 23:27 "add BUILD to front and end of prompt". **Mine:** counting by parity is how "front and end" is read.
4. End: if there is no remainder and the run arrived from heard or a source, fire gets target = end with this row's gate, arrival and shard. §3.4 "When the remainder is absent, the run ends and spawns its memory". **Mine:** a run that arrived from `said` (the brain's own replay) or from `build` (the SQL prompt's answer to the brain's own statement) does not fire end. Without this the memory run's own BUILD answers ended, fired end, whose BUILD answers ended, forever; measured today, both machines hung at the bind of the end run. My reading of §2.2: "Triggers may stay quiet when the brain speaks a word and fire when it hears".
5. Born: if the remainder names a gate with no view, born gets (run, remainder). Your 01:22 "triggers born, if table doesn't exist".
6. Land: INSERT INTO "remainder" with this gate as arrival, the next gate as remainder, the rest as rest. Your 01:22. Through mother, because SQLite cannot insert into a table named by a value.

**`build_go`** (the build neuron):
1. The words between the last two BUILD receipts of this run are read back in order through the encoder. Your 21:52 "THE OUTPUT OF THE RECIEPT WILL BE THE RUN".
2. `var x` is replaced by cell x: the newest in this run, else the newest in the run that fired this one, and so up the parents; if no cell, the text stays `var x`. Your 23:08; audit A4.
3. The text goes to mother; her answer is written into input as a run with parent = this run, arrival = build. Handoff §0 (a response from SQL back to the graph).

**`born_go`** (the born neuron):
1. Three encoder rows: `word.dna`, `word.definition`, `word.memory`, each getting the next gate number. **Mine:** the labels. Your 23:40 for the three things born together.
2. Four cells into the run: gate (the missing gate), dna, def, mem (the three new numbers). Your 21:52 "WITH THE ACTIVE REMAINDER BEING WRITTEN INTO THE FORMULA FOR THE CREATE TABLE"; the other three numbers are the same remainder's new tables. **Mine:** the cell names are the words gate, dna, def, mem.
3. If born's memory node holds a bound run, fire gets (run, target = born, gate). Your 10-21 19:44: the missing-shard run "reads the stored temporary run input table and writes" what is missing.

**`fire_go`** (the fire neuron):
1. Cells into the run: run, gate, arrival, remainder, rest, shard, for the values that are not NULL. **Mine:** the names are the hop's own column names; a NULL writes no cell (today a birth inside the define run wrote NULL over `rest` and the define run lost its word; fixed, retested).
2. The target neuron's bound run (the newest row of its memory node whose shard is NULL) is typed again as a run: its receipt's gates, parent = this run, arrival = said. §3.1 "formula shortcut: plug in, go to the gate, run it there"; 10-23 08:47 "the row holds pointers to the run through the neurons that makes that". **Mine:** "bound" = a memory-node row with shard NULL; a memory written by the end run carries the shard of the row that ended the run. How the brain tells its formula from its memories is yours (§13.4).

**`ear`** (on input):
1. If the line came as text: cut into tokens (a word is letters and `_`; every other character is one token), give new tokens a gate, write the gate list, set text to NULL, set arrival to heard if none was given. Your 23:08, 01:22; §2.5.
2. If the line came as gates (a replay): keep them.
3. Hop from the arrival gate to the first gate with the rest as rest.

**mother** (appendix A): run the text; answer ok / rows / error; when SQLite reports a row landed in an attached database's `outbox`, carry that outbox into input (text, parent = the asking run, arrival = the source's gate) and empty it. **Mine:** the carry is told by SQLite's update hook, so nothing is swept when nothing was written (today, sweeping seven source outboxes after every call made a birth take 7.5 s instead of 0.4 s). `NEURON_TRACE=1` prints every text she runs to stderr; the brain holds no log.

## 2. Tools

- `sqlite3` 3.37 or newer (hub 3.37.2, hp 3.46.1), `gcc`, `python3` (for the generator and the prompt only).
- Make a folder, copy the files of `NEURON-BUILD-SHEET-2-2026-10-25\` into it (or paste the appendices into files of those names), open a terminal there. On the hp: `scp -r` the folder.

## 3. Build mother

```
gcc -shared -fPIC -O2 -o mother.so mother.c -I.
```

Check, at the sqlite3 prompt:

```
sqlite3 :memory:
.load ./mother
SELECT mother('CREATE TABLE t ( a )');
SELECT mother('CREATE TABLE t ( a )');
SELECT mother('SELECT 1 + 1');
.quit
```

`ok`, then `error: table t already exists`, then `2`.

## 4. Lay the egg

`egg.sql` is written by `gen_egg3.py` (appendix B); run it once if you want to see it written, or use the egg.sql in the folder:

```
python3 gen_egg3.py
sqlite3 brain.db
.load ./mother
.read egg.sql
SELECT type, count(*) FROM sqlite_master GROUP BY type;
SELECT count(*) FROM encoder;  SELECT n FROM shards;
.quit
```

You should see `index|3`, `table|221`, `trigger|77`, `view|76`; `288` encoder rows (72 neurons × 4 labels); `72` shards (each neuron's first shard, pointing at its definition node). The numbers that matter later: heard 1, said 5, born.memory 16, end.memory 24, build 25, BUILD 29, var 33, space 77.

One hand-laid neuron, `heard`, as SQLite holds it (`SELECT sql FROM sqlite_master WHERE name IN ('1','2','3','4')`):

```sql
CREATE TABLE "2" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER )
CREATE VIEW "1" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "2"
CREATE TRIGGER "1" INSTEAD OF INSERT ON "1" BEGIN SELECT mother ( 'INSERT INTO "2" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "2" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "2" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 1 , NEW.arrival , NEW.remainder , NEW.rest ) ; END
CREATE TABLE "3" ( id INTEGER PRIMARY KEY , run INTEGER )                 -- heard.definition
CREATE TABLE "4" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) -- heard.memory
```

and its first shard: `SELECT * FROM "2";` gives `1||3`: shard 1, no arrival, no remainder, trigger 3 (the definition node). Every neuron the brain births has this text with other numbers, because the born run types it (checked in §12, C5).

## 5. Start the prompt

```
python3 bottom.py brain.db sources/wn.db sources/gcide.db sources/mw.db sources/mwt.db sources/moby.db sources/map.db sources/sqldoc.db
```

Each line you type goes into `input`. Then every run that line started is printed, read back through the encoder: the brain's own replays (arriving from `said`), what the SQL prompt answered (from `build`), what a source sent (from that source's name). Ctrl-D leaves; the brain stays in brain.db. To watch mother at the SQL prompt: `NEURON_TRACE=1 python3 bottom.py ...` (every text she runs, to stderr). To look at the tables after any line, in a second terminal: `sqlite3 brain.db ".read look.sql"`.

At the raw `sqlite3 brain.db` prompt you can do the same: `.load ./mother` then `INSERT INTO input (text) VALUES ('...');` with every `'` inside the line doubled.
## 6. First line: a word the brain has no neuron for

```
dog
```

Nothing comes back (`[0.01 s]`). The encoder gave `dog` gate 289. The hop from heard found no gate "289", so born gave dog's three tables their numbers and wrote the four cells; born's memory node holds no run yet, so nothing was fired; the landing on "289" was refused by SQLite (with `NEURON_TRACE=1` you see `sql< error: no such table: 289`). `.read look.sql` shows the cells and an empty receipt:

```
run  cell  value
1    gate  289
1    dna   290
1    def   291
1    mem   292
```

Your words: "THE NEURONS WILL HAVE TO HAVE THE RUNS FOR CREATE TABLE (IF REMAINDER GATE DOESN'T EXIST,) SUCH THAT A NEW TABLE FOR THAT REMAINDER GATE IS MADE... WITH THE ACTIVE REMAINDER BEING WRITTEN INTO THE FORMULA FOR THE CREATE TABLE" (21:52). The cells are that remainder and its three new numbers, written where the born run will read them. This line is also the control: with no run bound, nothing is built (§17, C1).

## 7. Second line: the born run, typed once

Paste this one line (`BORN-RUN.txt`, appendix E; 559 tokens; `var dna`, `var gate`, `var def`, `var mem` are the cells born writes):

```
BUILD CREATE TABLE "var dna" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ; CREATE VIEW "var gate" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "var dna" ; CREATE TRIGGER "var gate" INSTEAD OF INSERT ON "var gate" BEGIN SELECT mother ( 'INSERT INTO "var dna" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "var dna" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "var dna" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , var gate , NEW.arrival , NEW.remainder , NEW.rest ) ; END ; CREATE TABLE "var def" ( id INTEGER PRIMARY KEY , run INTEGER ) ; CREATE TABLE "var mem" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ; INSERT INTO "var dna" ( shard , trigger ) SELECT n + 1 , var def FROM shards ; UPDATE shards SET n = n + 1 ; BUILD
```

You should see:

```
run 3 (build, in run 2): error: near "gate": syntax error
[0.40 s]
```

Every token of this line is a hand-laid neuron, so the run hops 559 gates and writes 559 new DNA rows (shards 73 to 631). At the second BUILD the words between were read back and handed to mother, and SQL's refusal came back as run 3. It was refused because a line you type has no cells: cells belong to the run that fired a sub-run, and nobody fired this one. That is right. The line exists now as run 2, which is what the next line needs. (Any births inside a hand-typed line leave that line their own cells, so a hand-typed line's BUILD can also run with stray values; §8 shows one.)

## 8. Third line: give born its run

Born's memory node is "16". Write the pointer:

```
BUILD INSERT INTO "16" ( run ) VALUES ( 2 ) ; BUILD
```

```
run 5 (build, in run 4): ok
run 6 (said, in run 5): BUILD CREATE TABLE "var dna" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , tri...
run 7 (build, in run 6): ok
[0.41 s]
```

Run 5 is SQL's `ok` coming back into the brain as a run. Its word `ok` had no neuron, so born fired run 2 for it (run 6, arriving from `said`: the brain typing to itself), and run 7 is SQL's `ok` for that CREATE. From now on, when a landing finds no gate, born fires run 2 with that gate's cells. A neuron's bound run is the run in its memory node with shard NULL; this is "write the dna" done by hand, through BUILD.

## 9. Births are automatic now

```
dog
```

```
run 9 (said, in run 8): BUILD CREATE TABLE "var dna" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , tri...
run 10 (build, in run 9): ok
[0.38 s]
```

Check: `sqlite3 brain.db "SELECT gate, word FROM encoder WHERE word LIKE 'dog%'; SELECT type, name FROM sqlite_master WHERE name IN ('289','290','291','292'); SELECT * FROM \"290\";"`

```
289|dog            table|290       286|||291
290|dog.dna        view|289        287|1||
291|dog.definition trigger|289
292|dog.memory     table|291
                   table|292
```

Dog's first shard is 286 → 291 (its definition node, your 23:40 "every new neuron first dna chard is the definition"). The second row, 287, is the landing of this line: arrival 1 (heard), no remainder. `dog` itself said nothing: it has no bound run, and a run through the gates with nothing to say says nothing ("the chatbot answer is wrong", §3.2).

```
cat
```

```
run 12 (said, in run 11): BUILD CREATE TABLE "var dna" ( ...
run 13 (build, in run 12): ok
[0.37 s]
```

```
BUILD CREATE TABLE things ( a ) ; BUILD
```

```
run 15 (said, in run 14): BUILD CREATE TABLE "var dna" ( ...      ← things born
run 16 (build, in run 15): ok
run 17 (said, in run 14): BUILD CREATE TABLE "var dna" ( ...      ← a born
run 18 (build, in run 17): ok
run 19 (build, in run 14): ok                                       ← your CREATE TABLE things
[0.74 s]
```

`sqlite3 brain.db ".tables things"` shows the table. Your BUILD line reached the SQL prompt through the neurons, as v1's did, and SQL's answer came back as run 19.

## 10. The end run: memory and timeline, typed by you

Your order (handoff §0): "After you lay the run that builds the neuron node and the run that serves as the hop, then you will have to build the runs that input the timeline, the memory nodes, write the dna". Nothing is written when a run ends until you type these. The hook is the `end` neuron: when a run that arrived from heard or a source has no remainder left, the hop fires end with the row that ended it (its gate, arrival, shard) as cells (§1b, hop_go rule 4). End's memory node ("24") is empty, so nothing happens yet.

First the timeline table, through BUILD:

```
BUILD CREATE TABLE timeline ( id INTEGER PRIMARY KEY , run INTEGER , clock DEFAULT CURRENT_TIMESTAMP ) ; BUILD
```

Four births (timeline, id, clock, DEFAULT; CURRENT_TIMESTAMP is one word, born too), then `ok`. **Mine:** the columns. Your words: the timeline "only gets the reciept number as a pointer, and a couple key words" (10-16 06:40); `run` is the receipt pointer; the key words are not written (yours to design); `clock` is SQLite's own time, because "build the clock time line runs so that they build the clock" (23:40) is not built: this is the crutch for it.

Then the end run, one line, three BUILD pairs. Pair A writes the cell `mem`: the memory node of the neuron whose row ended the run (`var gate` is that neuron; its memory node is the encoder's `word.memory`). Pair B writes the memory: the run and the shard of the row that ended it, into that node. Pair C writes the timeline row.

```
BUILD INSERT INTO sheet ( run , name , value ) SELECT var run , ( SELECT gate FROM encoder WHERE word = 'mem' ) , gate FROM encoder WHERE word = ( SELECT word FROM encoder WHERE gate = var gate ) || '.memory' ; BUILD BUILD INSERT INTO "var mem" ( run , shard ) VALUES ( var run , var shard ) ; BUILD BUILD INSERT INTO timeline ( run ) VALUES ( var run ) ; BUILD
```

Typed by hand it says, among its births, `run 44 (build, in run 30): error: near "shard": syntax error` for pair B: its births left it cells for `run` and `gate` but no `shard`, so pairs A and C ran with stray values (one timeline row for run 30) and B was refused. It exists as a run now. After exactly the lines above it is run 30 (the prompt prints the number; read it, do not assume).

Bind it to end's memory node:

```
BUILD INSERT INTO "24" ( run ) VALUES ( 30 ) ; BUILD
```

Now every line you type writes its memory when it ends:

```
cat
```

```
[0.08 s]
```

`cat` has nothing to say, but `sqlite3 brain.db "SELECT * FROM \"<cat.memory>\"; SELECT * FROM timeline;"` (cat.memory is 307 after exactly these lines) shows:

```
cat.memory (id|run|shard)        timeline (id|run|clock)
1|60|289                          1|30|2026-10-26 01:31:18    ← the hand-typed end run's stray pair C
                                  2|54|2026-10-26 01:31:18    ← the bind line
                                  3|60|2026-10-26 01:31:18    ← cat
```

The memory of run 60 sits in cat's memory node with shard 289, the row (heard, no remainder) that ended the run. §2.4: "The memory of that run goes to a memory table for the DNA row that ended it." The run id is the pointer to its receipt, its cells and every run it started. What is NOT written: the brain's own replays (arriving from said) and SQL's answers (from build) write no memory (§1b, hop_go rule 4, **mine**). What the memory holds beyond the pointer, condensing, and bloat are yours (§2.4 [Open]).

## 11. Teach a word: define

Your words (10-25): "define is a run through the neurons like everything else... it has a run data sheet like every other run... compare your sources and give me the best definition... it's the first memory of that neuron... if the neuron doesn't exist create it and then print the definition memory". This sheet does the run, the data sheet, the sources and the definition node; it does not compare (yours, §14.7).

First type `define dog` once so that define is born, then read its numbers:

```
define dog
```

`define` is born (a sub-run of this line) and nothing else happens. `sqlite3 brain.db "SELECT gate, word FROM encoder WHERE word LIKE 'define%'"` gives four numbers; after exactly the lines above: define 365, define.dna 366, define.definition 367, define.memory 368. Read them.

The define run, one line, four BUILD pairs. The cells it reads were written by fire when define's row fired: `run` (the line being run), `rest` (the gates after the space: the word to define is the first of them, hence `CAST ( var rest AS INTEGER )`).

- Pair 0: if the word has no gate view, ask born for it (born writes its cells and fires the born run). Your "if the neuron doesn't exist create it".
- Pair A: write the cell `def` = that word's definition node (the encoder's `word.definition`).
- Pair B: put the word in WordNet's inbox. WordNet's own trigger answers into its outbox; mother carries each row into input as a run arriving from `wn`, parent = this line. Each is printed. That is "print the definition".
- Pair C: the definition node gets one row per return run: a pointer to the run, not text. 10-23 08:47: "the row holds pointers to the run through the neurons".

```
BUILD INSERT INTO born ( run , gate ) SELECT var run , CAST ( var rest AS INTEGER ) WHERE NOT EXISTS ( SELECT 1 FROM sqlite_master WHERE type = 'view' AND name = CAST ( var rest AS INTEGER ) ) ; BUILD BUILD INSERT INTO sheet ( run , name , value ) SELECT var run , ( SELECT gate FROM encoder WHERE word = 'def' ) , gate FROM encoder WHERE word = ( SELECT word FROM encoder WHERE gate = CAST ( var rest AS INTEGER ) ) || '.definition' ; BUILD BUILD INSERT INTO wn . inbox ( run , word ) SELECT var run , word FROM encoder WHERE gate = CAST ( var rest AS INTEGER ) ; BUILD BUILD INSERT INTO "var def" ( run ) SELECT id FROM input WHERE parent = var run AND arrival = ( SELECT gate FROM encoder WHERE word = 'wn' ) ; BUILD
```

Typed by hand: births, and refusals for the pairs whose cells it does not have. It is run 72 after exactly the lines above (read it).

Bind it to define's memory node, and write the dna: the row `define dog` hit is (arrival heard, remainder space), because the first word of a line arrives from heard and the next gate is the space. Point that row's trigger column at define:

```
BUILD INSERT INTO "368" ( run ) VALUES ( 72 ) ; BUILD
BUILD UPDATE "366" SET trigger = 365 WHERE arrival = 1 AND remainder = 77 ; BUILD
```

`sqlite3 brain.db 'SELECT * FROM "366"'` shows define's rows: the first shard → its definition node, and the row (1, 77) with trigger 365. Now:

```
define dog
```

```
run 115 (wn, in run 111): a member of the genus Canis (probably descended from the common wolf) that has been domesticated by ...
run 172 (wn, in run 111): a dull unattractive unpleasant girl or woman; "she got a reputation as a frump"; "she's a real dog"
run 203 (wn, in run 111): informal term for a man; "you lucky dog"
run 218 (wn, in run 111): someone who is morally reprehensible; "you dirty dog"
run 235 (wn, in run 111): a smooth-textured sausage of minced beef or pork usually smoked; often served on a bread roll
run 268 (wn, in run 111): a hinged catch that fits into a notch of a ratchet to move a wheel forward or prevent it from moving...
run 301 (wn, in run 111): metal supports for logs in a fireplace; "the andirons were too hot to touch"
run 324 (wn, in run 111): go after with the intent to catch; "The policeman chased the mugger down the alley"; "the dog chased...
[67.76 s]
```

What happened: the hop hit define's row (1, 77), whose trigger column names define; fire wrote the cells (run 111, gate define, arrival heard, remainder space, rest "289", shard) and typed run 72 as a sub-run; pair 0 found dog's view and did nothing; pair A wrote `def` = 291; pair B asked WordNet for `dog`; WordNet's trigger filled its outbox with eight rows; SQLite told mother; mother carried the eight rows into input as runs 115 to 324 arriving from `wn`; each ran through the neurons (every new word born on the way: that is the 70 s, about 100 births), each ended and wrote its own memory and a timeline row (the hp took 66 s); pair C wrote eight pointers into dog's definition node:

```
sqlite3 brain.db 'SELECT * FROM "291"'
1|115  2|172  3|203  4|218  5|235  6|268  7|301  8|324
```

A word the brain has never seen, and the source has not either:

```
define bird
```

```
[1.60 s]
```

bird is born by pair 0 (its five objects exist: table 798, view 797, trigger 797, tables 799 and 800), WordNet was asked, and nothing came back: the 470-word WordNet slice holds no `bird` (`SELECT count(*) FROM corpus WHERE word = 'bird'` in sources/wn.db gives 0). The definition node stays empty and the brain says nothing. What it should do when no source holds a word is yours (§14.7).

A word the brain has never seen that the slice does hold (`above`, found with `SELECT word FROM wn.corpus WHERE word NOT IN (SELECT word FROM encoder)`):

```
define above
```

```
run 429 (wn, in run 423): at an earlier place; "see above" [syn: {above}, {supra}] [ant: {below}] 2: in or to a place that is ...
run 468 (wn, in run 423): appearing earlier in the same text; "flaws in the above interpretation"
[16.61 s]
```

above was born by pair 0, the birth the define run itself asked for; two returns came back; above's definition node ("819") holds 2 pointers, 429 and 468. The 16 s are the births of the returns' new words. The same line again:

```
define above
```

```
run 493 (wn, in run 489): at an earlier place; "see above" [syn: {above}, {supra}] [ant: {below}] 2: in or to a place that is ...
run 498 (wn, in run 489): appearing earlier in the same text; "flaws in the above interpretation"
[0.67 s]
```

No births this time. WordNet was asked again and the definition node now holds 4 rows: the define run does not look in memory before asking (§14.7; the 10-25 sheet's decide rule that did is gone, as you asked). On the hp the same lines gave the same rows (runs 399 and 438 there).

This is the pattern for every word you teach: type the run once; put its number in the word's memory node; point a DNA row's trigger at the word. Your words: "the formula should be able to be built by the brain, by taking the variables and inserting them into the formula.. then once done the brain outputs to /build and it gets built" (10-16 08:48). The variables are the cells; the formula is the bound run; /build is BUILD.

## 12. The source brains

Each file in `sources/` is a brain of its own (appendix F): `corpus(word, hw, text)`, `inbox(id, run, word)`, `outbox(id, run, word, hw, text)` and one trigger, `work`: an ask landing in the inbox is answered into the outbox at once. The brain reaches a source only by naming its inbox in a BUILD line; mother carries the outbox back as runs. The corpora are the 470-word slices captured 10-22/25 (WordNet, Webster 1913, Merriam-Webster, the MW thesaurus, Moby, your relation map, the SQLite docs); the full WordNet and GCIDE are on the hp (`/usr/share/wordnet/`, `/usr/share/dictd/gcide.*`); loading them into a `corpus` is a one-time `.import` of a TSV (word, hw, text), not brain work. The sources are stand-ins I wrote; a source brain built your way is a brain.

## 13. What the brain cannot do mid-run, measured, and your way through

Tested today in a throwaway database (3.37.2) and in the chain (3.37.2 and 3.46.1):

| Statement typed inside a run (through BUILD, so nested in the line's own statement) | SQLite's answer |
|---|---|
| CREATE TABLE, CREATE VIEW, CREATE TRIGGER | ok (every birth does this) |
| INSERT, UPDATE (a row's trigger column), SELECT | ok |
| ALTER TABLE … ADD COLUMN | ok |
| DROP TABLE things | `error: database table is locked`; the table stays |
| the same DROP at the prompt, with no statement running | ok |

```
BUILD DROP TABLE things ; BUILD
run 382 (build, in run 379): error: database table is locked
```

So the brain can drop a table; it cannot while a statement of its own is still running, and inside a run every statement is nested in the typed line's. Your words (10-26 00:41): "how do you kill a db .exit, ctl d": the run ends first, then the statement. Your words for the mechanism (10-19 23:27): the brain "will either just autotype it in the sqlite at the end of the run when you add BUILD to front and end of prompt, or it makes the new neurons as it runs the run, then just autotypes into sqlite terminal after the run is done". That is: a BUILD text can be typed at the SQL prompt after the run is done, by the bottom, which "just get[s] the output and print[s] it" (23:59). This sheet does not build it, because where the brain says "after the run" rather than "now" is a decision (a word, a row, a run of yours), and mother must not make it (the 10-25 sheet's `later` queue made it, and is gone). Your call: §14.6.

Also measured: a gate made of the DNA table itself (one BEFORE INSERT trigger on the table, no view) crashes SQLite 3.37.2 (segmentation fault) when the trigger writes the row into its own table through mother. So the gate is a view over the DNA table, and a landing writes nothing but the DNA row and the receipt (my choice 1 of the 10-25 sheet, now with a reason).

## 14. Yours to decide (open), each with where it stands

1. **A new DNA row has no trigger.** `define cat` and `define bird` work because they hit the same row as `define dog`: (heard, space). A row the brain writes new has trigger NULL and fires nothing until it is set. §2.2 "When a trigger fires, and when it stays quiet, is learned." Today you set it with a BUILD UPDATE (the write-the-dna line). How the brain sets it is yours.
2. **Cells are read from the run, else its parents.** A hand-typed line has no parent, so its `var` holes stay as typed and SQL refuses them (§7, §10). Births inside a line leave the line their cells. Fire writes the hop's columns as cells; born writes the four numbers. The names and this scoping are mine.
3. **End stays quiet for said and build.** My reading of §2.2 that stops the memory of a memory of a memory (§1b, hop_go rule 4). If the brain's own sayings should also write memories, something else must stop that loop; I do not know what in your design does.
4. **A neuron's bound run is the memory-node row with shard NULL.** The end run writes memories with the ending row's shard. Fire reads the newest shard-NULL row. How the brain tells its formula from its memories is yours; §2.4 says the first memory is the definition, and here the definition is in the definition node (pointers to the return runs) while the formula is in the memory node.
5. **The timeline's clock and key words.** The clock is SQLite's CURRENT_TIMESTAMP; "build the clock" (23:40) is not built; the "couple key words" (10-16) are not written.
6. **A statement that must wait for the run to end (DROP).** §13. Your words give the mechanism (the bottom types a specific output after the run); what tells the brain to send a statement that way is yours.
7. **Compare, and asking again.** The define run writes every WordNet return into the definition node in arrival order, asks one source, and asks every time it runs (the node grows by the returns each time; `define above` twice gave 4 rows). "Compare your sources and give me the best definition" is not built; neither is asking several sources, nor looking in the definition node before asking, nor what to do when no source holds the word (`define bird`). Any order, choice or check I put in would be mine (the 10-25 and v18 "best" measures and the decide rule were, and are gone). §3.1's opening questions ("Do I have a memory of it?") are where this belongs, as runs you type.
8. **Spaces double the hops.** Every space is a landing (your 01:22); the word after `define` is the first gate of `rest`.
9. **The encoder's labels** `word.dna`, `word.definition`, `word.memory` are mine. The brain's tables are numbers; only the encoder says which is which. §2.5: "The encoder would be protected, open to the brain but not to a user".
10. **The ear's tokenizer** (letters and `_` make a word; every other character is a token) is mine, from your "every punctuation, special char" (23:08). A word with a digit in it (`g2`) is two tokens.
11. **Perspective.** A run's arrival is heard, said, build, or a source's gate (§2.1). Who, what, when, where, why, how are not attached (§2.5, open).
12. **Reading a run's words back for the prompt** is done by the prompt through the encoder (bottom.py, look.sql), never by the brain; the brain holds numbers only.

## 15. Traps I fell into building this today

- The carry as a sweep: mother checked all seven source outboxes after every call; with the sources attached a birth took 7.5 s instead of 0.4 s. Your rule is populated-driven, never a timer or a sweep; SQLite's update hook tells her when an outbox was written, and she carries only then.
- The memory loop: when the end run was bound, every `ok` that its three BUILDs got back came in as a run, ended, fired end, whose BUILDs got `ok` back, forever. Both machines hung at the bind. End now stays quiet for runs arriving from said and build (§14.3).
- A birth inside the define run (pair 0) fired born, and fire wrote NULL over the `rest` cell the define run still needed, so `define bird` lost its word. Fire writes no cell for a NULL value now.
- The table-as-gate design (no view) crashes SQLite 3.37.2; measured before building on it.
- A form SQLite 3.46 takes and 3.37 does not (`VALUES` as a table in FROM) broke fire_go on the hub only. Both versions are tested for every line in this sheet.
- My shard check matched only the hand-laid tables' spacing and reported a false "not one sequence"; the hand-laid text is now spaced exactly as the born run types it, and the check matches both.

## 16. Checks run today

Every line of §§6-13 was typed by `run_chain.sh` on both machines from a fresh egg; the two logs (`CHAIN-LOG.txt`, `CHAIN-LOG-hp.txt`, 513 lines each) differ in nothing but timings and clock values.

| Check | Hub (3.37.2) | hp (3.46.1) |
|---|---|---|
| egg lays: 221 tables, 76 views, 77 triggers, 288 encoder rows, 72 shards | yes | yes |
| `dog` with nothing bound: no tables, no receipt row, 4 cells | yes | yes |
| born run typed → refused (no cells); bound → `ok`; `dog` → 5 objects, first shard 286 → 291 | yes | yes |
| `cat`, `things`, `a` born by sub-runs; `BUILD CREATE TABLE things ( a ) ; BUILD` → ok; the table exists | yes | yes |
| timeline table through BUILD; end run bound; `cat` → cat.memory row (60, 289), timeline row | yes | yes |
| define run bound; dna written; `define dog` → 8 returns from wn, 8 pointers in dog.definition | yes | yes |
| `define bird` (not in the slice) → born, nothing back, empty node | yes | yes |
| `define above` (in the slice, new) → born by the define run, 2 returns, 2 pointers; again: 0.67 s, 4 pointers | yes | yes |
| `BUILD DROP TABLE things ; BUILD` → `error: database table is locked`; the table stays | yes | yes |
| shards one sequence: 842 rows over 205 DNA tables = counter 842, no gaps, no duplicates | yes | yes |
| no column outside `encoder` holds text with letters (every table, every column) | yes | not re-checked |
| a birth (the born run replayed, 559 hops, plus the `ok` run): 0.36-0.46 s | 0.60-0.65 s |
| `define dog` (8 returns, about 100 births): 68 s | 66 s |
| 592 / 1,200 / 2,400 known tokens, first time: 0.67 / 1.82 / 5.77 s; again, every row a hit: 0.66 / 1.82 / 6.80 s | hub | not timed |
| controls C1-C5 (§17) | yes | |

The cost per hop grows with what is left of the line: 1.1 ms at 600 tokens, 1.5 at 1,200, 2.4 at 2,400, because the remainder (the rest of the line as gate numbers, §2.3) is carried as text through every hop and every mother statement. The 10-25 sheet said the cost per hop does not grow; its own numbers (0.7 / 1.7 / 3.7 s) already grew, and that sentence was wrong. A hit costs the same as a write: the hop's cost is the statements, not the row.

## 17. Controls

Fresh egg, mother loaded, on a separate copy:

| Step | Rows after |
|---|---|
| C1 `dog`, no run bound | dog's tables: 0; receipts: 0; cells written by born: 4 |
| C2 born run typed (refused: no cells), bound, `dog` | dog's tables/view/trigger: 5 |
| C3 the pointer deleted (`DELETE FROM "16"`), `bird` | bird's tables: 0; cells written by born: 4 |
| C4 the pointer put back, `bird` | bird's tables/view/trigger: 5 |
| C5 a born neuron's gate trigger, numbers aside, equals heard's hand-laid one; its DNA, definition and memory tables equal heard's | identical |
## Appendix A. mother.c

```c
/* mother(text): the brain hands mother SQL text. She runs it at the SQL prompt and answers what SQLite answered:
   'ok', the rows a SELECT sent back (one row per line, columns parted by " | "), or 'error: <SQLite's reason>'.
   She never stops the brain: a refusal is an answer like any other. When a source brain's outbox says it is populated
   (SQLite tells her the moment a row lands there), she carries those rows into the brain's input as lines arriving
   from that source's gate, and empties the outbox. She parses nothing, decides nothing and keeps nothing.
   NEURON_TRACE=1 in the environment makes her print every text she runs to stderr, so you can watch the SQL prompt.
   Build:  gcc -shared -fPIC -O2 -o mother.so mother.c -I.      Load in sqlite3:  .load ./mother   */
#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

static int trace = -1;
static int populated = 0;   /* set by SQLite the moment a row lands in a source brain's outbox */

static void hook(void *p, int op, const char *dbname, const char *table, sqlite3_int64 rowid){
  if(op == SQLITE_INSERT && strcmp(table, "outbox") == 0 && strcmp(dbname, "main") != 0) populated = 1;
}

static void carry(sqlite3 *db){
  /* an outbox said it is populated: every attached database with an outbox has its rows become input lines of the
     main brain, arriving from that source's gate, and is emptied. Nothing is swept when nothing was written. */
  sqlite3_stmt *dbs = 0;
  if(!populated) return;
  populated = 0;
  if(sqlite3_prepare_v2(db, "SELECT name FROM pragma_database_list WHERE name NOT IN ('main','temp')", -1, &dbs, 0) != SQLITE_OK) return;
  while(sqlite3_step(dbs) == SQLITE_ROW){
    const char *src = (const char*)sqlite3_column_text(dbs, 0);
    char *q = sqlite3_mprintf(
      "INSERT INTO main.input (text, parent, arrival) SELECT text, run, (SELECT gate FROM main.encoder WHERE word = %Q) FROM \"%w\".outbox ORDER BY id; DELETE FROM \"%w\".outbox;",
      src, src, src);
    sqlite3_exec(db, q, 0, 0, 0);   /* a database with no outbox table is simply not a source brain */
    sqlite3_free(q);
  }
  sqlite3_finalize(dbs);
}

static int rows(void *p, int argc, char **argv, char **col){
  char **acc = (char**)p; int i;
  char *line = sqlite3_mprintf("%s", argc ? (argv[0] ? argv[0] : "") : "");
  for(i = 1; i < argc; i++){ char *t = sqlite3_mprintf("%s | %s", line, argv[i] ? argv[i] : ""); sqlite3_free(line); line = t; }
  if(*acc){ char *t = sqlite3_mprintf("%s\n%s", *acc, line); sqlite3_free(*acc); sqlite3_free(line); *acc = t; } else *acc = line;
  return 0;
}

static void motherFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const char *sql = (const char*)sqlite3_value_text(argv[0]);
  char *err = 0, *got = 0;
  sqlite3 *db = sqlite3_context_db_handle(ctx);
  if(trace < 0) trace = getenv("NEURON_TRACE") ? 1 : 0;
  if(!sql){ sqlite3_result_text(ctx, "error: nothing to run", -1, SQLITE_STATIC); return; }
  if(trace) fprintf(stderr, "  sql> %s\n", sql);
  if(sqlite3_exec(db, sql, rows, &got, &err) != SQLITE_OK){
    sqlite3_free(got);
    char *msg = sqlite3_mprintf("error: %s", err ? err : "unknown");
    if(trace) fprintf(stderr, "  sql< %s\n", msg);
    sqlite3_free(err);
    sqlite3_result_text(ctx, msg, -1, sqlite3_free);
    carry(db);
    return;
  }
  carry(db);
  if(got){ if(trace) fprintf(stderr, "  sql< %s\n", got); sqlite3_result_text(ctx, got, -1, sqlite3_free); return; }
  if(trace) fprintf(stderr, "  sql< ok\n");
  sqlite3_result_text(ctx, "ok", -1, SQLITE_STATIC);
}

#ifdef _WIN32
__declspec(dllexport)
#endif
int sqlite3_mother_init(sqlite3 *db, char **e, const sqlite3_api_routines *pApi){
  SQLITE_EXTENSION_INIT2(pApi);
  sqlite3_update_hook(db, hook, 0);
  return sqlite3_create_function(db, "mother", 1, SQLITE_UTF8 | SQLITE_INNOCUOUS, 0, motherFunc, 0, 0);
}
```

## Appendix B. gen_egg3.py (writes egg.sql and BORN-RUN.txt)

```python
#!/usr/bin/env python3
# gen_egg3.py: writes egg.sql, the hand-laid part of the brain, from the owner's words of 2026-10-19/20 and the
# reference draft. Hand-laid: the ear (input), the encoder, the shard counter, the receipt, the sheet; the physics
# neurons heard, said, hop, born, fire, end, build; and one neuron for every token of the born run, so the brain can
# type its own CREATE ("WE WILL HAND LAY ALL THOSE SAME WORDS AS NODES SO THE BRAINS CAN LAY IT'S OWN TABLES").
# Every table a neuron owns is named by a gate number; the encoder is the only table that holds a word.
# Every write that happens while a deeper hop is still running goes to mother as its own statement (SQLite keeps an
# INSERT's cursor open until its statement ends).
import re, sys

def tokens(s):
    return re.findall(r'[A-Za-z_]+|[^A-Za-z_]', s)

def gate_trigger(dna, gate):
    # the one trigger of a neuron, on its gate view: hit the DNA row (arrival, remainder) if it exists, write it if
    # not (shard = the next number of the one sequence), then hand the run to hop. Same text for every neuron.
    return (f'CREATE TRIGGER "{gate}" INSTEAD OF INSERT ON "{gate}" BEGIN '
            f"SELECT mother ( 'INSERT INTO \"{dna}\" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) "
            f"|| ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM \"{dna}\" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; "
            f"SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM \"{dna}\" WHERE shard = n + 1 )' ) ; "
            f'INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , {gate} , NEW.arrival , NEW.remainder , NEW.rest ) ; END')

# The born run, exactly as the owner types it (one line). "var x" reads cell x. The cells gate, dna, def, mem are the
# four gate numbers born wrote: the missing gate, its DNA table, its definition node, its memory node.
BORN = ('BUILD CREATE TABLE "var dna" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ; '
        'CREATE VIEW "var gate" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "var dna" ; '
        + gate_trigger('var dna', 'var gate') + ' ; '
        'CREATE TABLE "var def" ( id INTEGER PRIMARY KEY , run INTEGER ) ; '
        'CREATE TABLE "var mem" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ; '
        'INSERT INTO "var dna" ( shard , trigger ) SELECT n + 1 , var def FROM shards ; UPDATE shards SET n = n + 1 ; BUILD')

PHYSICS = ['heard', 'said', 'hop', 'born', 'fire', 'end', 'build']
word_neurons = []
for w in ['BUILD', 'var'] + list('0123456789') + tokens(BORN):
    if w not in word_neurons and w not in PHYSICS:
        word_neurons.append(w)

out = []
E = out.append
def sq(s): return "'" + s.replace("'", "''") + "'"
gate = {}
n = 0
def enc(word):
    global n
    n += 1; gate[word] = n
    E(f"INSERT INTO encoder (gate, word) VALUES ({n}, {sq(word)});")
    return n

def neuron(word):
    # a neuron: gate view "<N>" (the entry), DNA table "<N+1>", definition node "<N+2>", memory node "<N+3>", the one
    # gate trigger, and the first shard pointing at the definition node. Only the encoder knows which number is which.
    # The text is spaced exactly as the born run types it, so a hand-laid neuron and a born one read the same.
    g = enc(word); d = enc(word + '.dna'); df = enc(word + '.definition'); m = enc(word + '.memory')
    E(f'CREATE TABLE "{d}" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;')
    E(f'CREATE VIEW "{g}" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "{d}" ;')
    E(gate_trigger(d, g) + ' ;')
    E(f'CREATE TABLE "{df}" ( id INTEGER PRIMARY KEY , run INTEGER ) ;')
    E(f'CREATE TABLE "{m}" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;')
    E(f'INSERT INTO "{d}" (shard, trigger) SELECT n + 1, {df} FROM shards; UPDATE shards SET n = n + 1;')
    E('')
    return g

E('-- egg.sql: the hand-laid part of the brain. Laid once. Everything else is typed at the prompt.')
E("-- Made from the owner's words of 2026-10-19/20 (see the build sheet).")
E('PRAGMA recursive_triggers = ON;')
E('')
E('-- the ear, the encoder, the one shard counter, the receipt, the sheet')
E('CREATE TABLE input (id INTEGER PRIMARY KEY, parent INTEGER, arrival INTEGER, gates TEXT, text TEXT);')
E('CREATE TABLE encoder (gate INTEGER PRIMARY KEY, word TEXT NOT NULL UNIQUE);')
E('CREATE TABLE shards (n INTEGER NOT NULL);')
E('INSERT INTO shards VALUES (0);')
E('CREATE TABLE receipt (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER);')
E('CREATE INDEX receipt_run ON receipt (run, gate);')
E('CREATE TABLE sheet (id INTEGER PRIMARY KEY, run INTEGER, name INTEGER, value);')
E('CREATE INDEX sheet_name ON sheet (name, run);')
E('')
E('-- physics neurons: heard and said (where a line arrives from), hop, born, fire, end, build. Each is also a word')
H = neuron('heard'); S_ = neuron('said'); HOP = neuron('hop'); BORN_G = neuron('born'); FIRE = neuron('fire'); END = neuron('end'); BLD = neuron('build')
E('-- the gates of the physics: views with no table under them, so a hand-off holds no cursor open while the next hop runs')
E('CREATE VIEW hop AS SELECT NULL AS run, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest;')
E('CREATE VIEW born AS SELECT NULL AS run, NULL AS gate;')
E('CREATE VIEW fire AS SELECT NULL AS run, NULL AS target, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest, NULL AS shard;')
E('CREATE VIEW build AS SELECT NULL AS run;')
E('')
E('-- BUILD, var, the digits 0 to 9 (draft §3.9), and every token of the born run')
for w in word_neurons:
    neuron(w)
K = gate['BUILD']; SP = gate[' ']
BM = gate['born.memory']; EM = gate['end.memory']
C = {w: gate[w] for w in ['run', 'gate', 'dna', 'def', 'mem', 'arrival', 'remainder', 'rest', 'shard']}   # cell names are these words' gates
E('')

head = "substr(NEW.rest || ' ', 1, instr(NEW.rest || ' ', ' ') - 1)"
tail = "trim(substr(NEW.rest || ' ', instr(NEW.rest || ' ', ' ') + 1))"
nul = lambda x: f"coalesce({x}, 'NULL')"
dna_of = "(SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.dna')"
mem_of = lambda g: f"(SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = {g}) || '.memory')"
E("-- the hop: writes the receipt; fires what the row's trigger column names; closes a BUILD pair; at the end of a run that arrived from heard or a source (not from said, not from build) fires end; births a missing gate; lands on the next gate")
E(f"""CREATE TRIGGER hop_go INSTEAD OF INSERT ON hop BEGIN
  SELECT mother('INSERT INTO receipt (run, gate, shard) SELECT ' || NEW.run || ', ' || NEW.gate || ', shard FROM "' || {dna_of} || '" WHERE arrival IS ' || {nul('NEW.arrival')} || ' AND remainder IS ' || {nul('NEW.remainder')});
  SELECT mother('INSERT INTO fire (run, target, gate, arrival, remainder, rest, shard) SELECT ' || NEW.run || ', trigger, ' || NEW.gate || ', ' || {nul('NEW.arrival')} || ', ' || {nul('NEW.remainder')} || ', ' || coalesce(quote(NEW.rest), 'NULL') || ', shard FROM "' || {dna_of} || '" WHERE arrival IS ' || {nul('NEW.arrival')} || ' AND remainder IS ' || {nul('NEW.remainder')} || ' AND trigger IS NOT NULL');
  SELECT mother('INSERT INTO build (run) VALUES (' || NEW.run || ')') WHERE NEW.gate = {K} AND (SELECT count(*) FROM receipt WHERE run = NEW.run AND gate = {K}) % 2 = 0;
  SELECT mother('INSERT INTO fire (run, target, gate, arrival, remainder, rest, shard) SELECT ' || NEW.run || ', {END}, ' || NEW.gate || ', ' || {nul('NEW.arrival')} || ', NULL, NULL, shard FROM "' || {dna_of} || '" WHERE arrival IS ' || {nul('NEW.arrival')} || ' AND remainder IS NULL') WHERE NEW.remainder IS NULL AND (SELECT arrival FROM input WHERE id = NEW.run) NOT IN ({S_}, {BLD});
  SELECT mother('INSERT INTO born (run, gate) SELECT ' || NEW.run || ', ' || NEW.remainder || ' WHERE NOT EXISTS (SELECT 1 FROM sqlite_master WHERE type = ''view'' AND name = ''' || NEW.remainder || ''')') WHERE NEW.remainder IS NOT NULL;
  SELECT mother('INSERT INTO "' || NEW.remainder || '" (run, arrival, remainder, rest) VALUES (' || NEW.run || ', ' || NEW.gate || ', ' || coalesce(nullif({head}, ''), 'NULL') || ', ' || coalesce(quote(nullif({tail}, '')), 'NULL') || ')') WHERE NEW.remainder IS NOT NULL;
END;""")
E('')
E("-- build: the second BUILD of a pair landed. The words between the two BUILDs are read back with the var cells filled (this run's cells first, then its parents') and handed to mother; her answer comes back into the brain as a run")
E(f"""CREATE TRIGGER build_go INSTEAD OF INSERT ON build BEGIN
  SELECT mother('INSERT INTO input (text, parent, arrival) VALUES (' || quote(mother(t)) || ', ' || NEW.run || ', {BLD})') FROM (SELECT (
    WITH RECURSIVE up(id) AS (SELECT NEW.run UNION ALL SELECT i.parent FROM input i JOIN up ON i.id = up.id WHERE i.parent IS NOT NULL)
    SELECT group_concat(w, '') FROM (
      SELECT CASE WHEN p2 = 'var' AND p1 = ' ' THEN coalesce((SELECT value FROM sheet s WHERE s.name = g AND s.run IN (SELECT id FROM up) ORDER BY (s.run = NEW.run) DESC, s.id DESC LIMIT 1), 'var ' || word)
                  WHEN word = 'var' AND n1 = ' ' THEN '' WHEN p1 = 'var' AND word = ' ' THEN '' ELSE word END AS w
      FROM (SELECT e.word, e.gate AS g, lag(e.word, 1) OVER (ORDER BY r.id) AS p1, lag(e.word, 2) OVER (ORDER BY r.id) AS p2, lead(e.word, 1) OVER (ORDER BY r.id) AS n1, r.id
            FROM receipt r JOIN encoder e ON e.gate = r.gate
            WHERE r.run = NEW.run AND r.gate <> {K}
              AND r.id > (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {K} AND id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {K}))
              AND r.id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {K})) ORDER BY id)) AS t);
END;""")
E('')
E("-- born: a gate with no neuron. It gives the new neuron's three tables their gate numbers in the encoder, writes the four numbers as cells, then fires born's own run if one is bound")
E(f"""CREATE TRIGGER born_go INSTEAD OF INSERT ON born BEGIN
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.dna' FROM encoder WHERE gate = NEW.gate;
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.definition' FROM encoder WHERE gate = NEW.gate;
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.memory' FROM encoder WHERE gate = NEW.gate;
  INSERT INTO sheet (run, name, value) VALUES
    (NEW.run, {C['gate']}, NEW.gate),
    (NEW.run, {C['dna']}, (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.dna')),
    (NEW.run, {C['def']}, (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.definition')),
    (NEW.run, {C['mem']}, (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.memory'));
  SELECT mother('INSERT INTO fire (run, target, gate) SELECT ' || NEW.run || ', {BORN_G}, ' || NEW.gate || ' WHERE EXISTS (SELECT 1 FROM "{BM}" WHERE shard IS NULL)');
END;""")
E('')
E("-- fire: a DNA row's trigger column named a neuron (or the run ended: target end). The run, the row's gate, arrival, remainder, rest and shard are written as cells (a value that is NULL writes no cell); the neuron's formula, the newest run bound in its memory node (shard NULL), is typed again as a sub-run of this run, arriving from said")
E(f"""CREATE TRIGGER fire_go INSTEAD OF INSERT ON fire BEGIN
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['run']}, NEW.run WHERE NEW.run IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['gate']}, NEW.gate WHERE NEW.gate IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['arrival']}, NEW.arrival WHERE NEW.arrival IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['remainder']}, NEW.remainder WHERE NEW.remainder IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['rest']}, NEW.rest WHERE NEW.rest IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['shard']}, NEW.shard WHERE NEW.shard IS NOT NULL;
  SELECT mother('INSERT INTO input (gates, parent, arrival) SELECT (SELECT group_concat(gate, '' '') FROM (SELECT gate FROM receipt WHERE run = (SELECT run FROM "' || {mem_of('NEW.target')} || '" WHERE shard IS NULL ORDER BY id DESC LIMIT 1) ORDER BY id)), ' || NEW.run || ', {S_} WHERE EXISTS (SELECT 1 FROM "' || {mem_of('NEW.target')} || '" WHERE shard IS NULL)')
    WHERE EXISTS (SELECT 1 FROM encoder WHERE gate = {mem_of('NEW.target')});
END;""")
E('')
E("-- the ear: a line with text is encoded to gates (a word is a run of letters and _; every digit and every other character, space included, is its own neuron), new words get a gate, the text is let go; a line that comes as gates (a replay) keeps them. Then the run hops from where it arrived (heard, said, a source, build) to its first gate")
E(f"""CREATE TRIGGER ear AFTER INSERT ON input BEGIN
  INSERT OR IGNORE INTO encoder (word)
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c))
    SELECT group_concat(ch, '') FROM t WHERE NEW.text IS NOT NULL GROUP BY tok;
  UPDATE input SET gates = (
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c)),
    w AS (SELECT tok, group_concat(ch, '') AS word FROM t GROUP BY tok)
    SELECT group_concat(gate, ' ') FROM (SELECT e.gate FROM w JOIN encoder e ON e.word = w.word ORDER BY w.tok)), text = NULL, arrival = coalesce(NEW.arrival, {H}) WHERE id = NEW.id AND NEW.text IS NOT NULL;
  UPDATE input SET arrival = coalesce(NEW.arrival, {H}) WHERE id = NEW.id AND NEW.text IS NULL;
  INSERT INTO hop (run, gate, arrival, remainder, rest)
    SELECT NEW.id, arrival, NULL, CAST(substr(gates || ' ', 1, instr(gates || ' ', ' ') - 1) AS INTEGER), nullif(trim(substr(gates || ' ', instr(gates || ' ', ' ') + 1)), '') FROM input WHERE id = NEW.id AND gates IS NOT NULL AND gates <> '';
END;""")
open(sys.argv[1] if len(sys.argv) > 1 else 'egg.sql', 'w').write('\n'.join(out) + '\n')
open('BORN-RUN.txt', 'w').write(BORN + '\n')
print('egg:', len(out), 'lines;', n, 'gates;', 7 + len(word_neurons), 'neurons;', len(tokens(BORN)), 'tokens in the born run; heard', H, 'said', S_, 'hop', HOP, 'born', BORN_G, 'fire', FIRE, 'end', END, 'build', BLD, 'BUILD', K, 'var', gate['var'], 'space', SP, 'born.memory', BM, 'end.memory', EM, 'cells', C)
```

## Appendix C. bottom.py (the prompt)

```python
#!/usr/bin/env python3
# bottom.py: the prompt. Each line you type is written into brain.db (table input). Then every run that line started
# (the line itself, the runs the brain typed to itself, what the SQL prompt and the sources sent back) is printed,
# read back through the encoder, because the brain holds only gate numbers. Nothing else happens here.
# usage: python3 bottom.py brain.db [source.db ...]      Ctrl-D leaves. The brain stays in the file.
import os, sqlite3, sys, time
here = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(sys.argv[1], isolation_level=None)
db.enable_load_extension(True)
db.load_extension(os.path.join(here, 'mother'))
db.execute('PRAGMA recursive_triggers = ON')
for src in sys.argv[2:]:
    db.execute('ATTACH ? AS ' + os.path.splitext(os.path.basename(src))[0], (src,))
WORDS = ('SELECT id, parent, (SELECT word FROM encoder WHERE gate = i.arrival), '
         "(SELECT group_concat(word, '') FROM (SELECT e.word FROM json_each('[' || replace(i.gates, ' ', ',') || ']') j "
         'JOIN encoder e ON e.gate = j.value ORDER BY j.key)) FROM input i WHERE id >= ? ORDER BY id')
while True:
    try:
        line = input('> ')
    except EOFError:
        break
    if not line.strip():
        continue
    t = time.time()
    try:
        run = db.execute('INSERT INTO input (text) VALUES (?)', (line,)).lastrowid
    except sqlite3.Error as e:
        print('refused:', e)
        continue
    for rid, parent, arrival, words in db.execute(WORDS, (run,)):
        if rid == run:
            continue
        words = words or ''
        print(f'  run {rid} ({arrival}, in run {parent}): {words[:100]}{"..." if len(words) > 100 else ""}')
    print(f'  [{time.time() - t:.2f} s]')
```

## Appendix D. look.sql (your eyes)

```sql
-- look.sql: your eyes on the brain after a line. At the sqlite3 prompt: .read look.sql
-- Nothing here changes the brain; these are reads of its tables, with the encoder giving the numbers their words.
.mode column
.headers on
SELECT 'RUNS of the last typed line (the line, the runs it started, what came back)' AS section;
SELECT i.id, i.parent, (SELECT word FROM encoder WHERE gate = i.arrival) AS arrival,
       substr((SELECT group_concat(word, '') FROM (SELECT e.word FROM json_each('[' || replace(i.gates, ' ', ',') || ']') j JOIN encoder e ON e.gate = j.value ORDER BY j.key)), 1, 70) AS words
  FROM input i WHERE i.id >= (SELECT max(id) FROM input WHERE parent IS NULL) ORDER BY i.id;
SELECT 'RECEIPT of the last typed line: word(gate:shard) in order' AS section;
SELECT group_concat(e.word || '(' || r.gate || ':' || r.shard || ')', ' ') AS path
  FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = (SELECT max(id) FROM input WHERE parent IS NULL) ORDER BY r.id;
SELECT 'SHEET (cells) of the last typed line and its runs' AS section;
SELECT s.run, (SELECT word FROM encoder WHERE gate = s.name) AS cell, s.value FROM sheet s WHERE s.run >= (SELECT max(id) FROM input WHERE parent IS NULL) ORDER BY s.id;
SELECT 'NEW WORDS (gates above the egg''s 252, newest first)' AS section;
SELECT gate, word FROM encoder WHERE gate > 252 ORDER BY gate DESC LIMIT 12;
SELECT 'NEW TABLES, GATES, TRIGGERS (the last 12 made)' AS section;
SELECT type, name, substr(sql, 1, 80) AS sql FROM sqlite_master WHERE rowid > (SELECT max(rowid) - 12 FROM sqlite_master) ORDER BY rowid;
SELECT 'COUNTS' AS section;
SELECT (SELECT n FROM shards) AS shards, (SELECT count(*) FROM receipt) AS receipts, (SELECT count(*) FROM encoder) AS encoder_rows, (SELECT count(*) FROM sqlite_master WHERE type = 'table') AS tables, (SELECT count(*) FROM input) AS runs;
```

## Appendix E. BORN-RUN.txt (one line)

```
BUILD CREATE TABLE "var dna" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ; CREATE VIEW "var gate" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "var dna" ; CREATE TRIGGER "var gate" INSTEAD OF INSERT ON "var gate" BEGIN SELECT mother ( 'INSERT INTO "var dna" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "var dna" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "var dna" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , var gate , NEW.arrival , NEW.remainder , NEW.rest ) ; END ; CREATE TABLE "var def" ( id INTEGER PRIMARY KEY , run INTEGER ) ; CREATE TABLE "var mem" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ; INSERT INTO "var dna" ( shard , trigger ) SELECT n + 1 , var def FROM shards ; UPDATE shards SET n = n + 1 ; BUILD
```

## Appendix F. sources/source-schema.sql (a source brain)

```sql
CREATE TABLE corpus (word TEXT COLLATE NOCASE, hw TEXT, text TEXT);
CREATE INDEX cw ON corpus(word);
CREATE TABLE inbox (id INTEGER PRIMARY KEY, run INTEGER, word TEXT);
CREATE TABLE outbox (id INTEGER PRIMARY KEY, run INTEGER, word TEXT, hw TEXT, text TEXT);
CREATE TRIGGER work AFTER INSERT ON inbox BEGIN
  INSERT INTO outbox (run, word, hw, text) SELECT NEW.run, NEW.word, hw, text FROM corpus WHERE word = NEW.word;
  DELETE FROM inbox WHERE id = NEW.id;
END;
```
