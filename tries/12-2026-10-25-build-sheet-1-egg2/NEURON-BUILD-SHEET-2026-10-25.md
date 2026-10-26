# NEURON BUILD SHEET

2026-10-25. For you to build, by hand, at the prompt. Every block below was typed today exactly as shown, on the hub (SQLite 3.37.2) and on the hp (SQLite 3.46.1), and the outputs shown are what came back. Nothing here is from my notes. Where a step is your design, your words are quoted with the time you typed them (10-19/20, the night you built v1; the reference draft by §). Where a step is my choice, it says so, so you can strike it.

The files are in `NEURON-BUILD-SHEET-2026-10-25\` (same folder as this sheet). The earlier LLM document `NEURON_BUILD_CHAIN_TO_ACCEPTANCE.md` is untouched; this sheet replaces it for the build.

## 0. What you are building

```
you type a line
   │
   ▼  ear: the line goes into table input. The encoder cuts it into tokens (a word; every digit,
   │       space and punctuation mark is its own token), gives each new token a gate number, and
   │       hands the run to hop: from heard, to the first gate, with the rest of the line as gates.
   ▼
 gate N  (a view: the neuron's entry)  ──trigger tN──▶  DNA table gN: hit the row (arrival, remainder)
   │                                                   if it exists, write it if not (shard = next number)
   ▼
  hop  ──▶ receipt (run, gate, shard)
       ──▶ if the row's trigger column names a neuron: fire = type that neuron's memory run as a sub-run
       ──▶ if this is the second BUILD of a pair: build = the words between go to mother → SQL prompt → output
       ──▶ if the next gate has no neuron: born = write the cells, fire born's memory run (the born run)
       ──▶ land on the next gate (through mother, because a table named by a value needs the SQL prompt)
       ──▶ no next gate: land on end
   ▼
 mother: runs the text she is handed. Answers ok, the rows, or error: ... . Carries what the source
         brains put in their outboxes into secondary input. Decides nothing.
```

Your words for the whole: "prompt ---> encoder ---> brain" (10-25). "THE PHYSICS OUTSIDE THE DATABASE IS A HANDLER THAT JUST TAKES AN INPUT FROM A SPECIFIC OUTPUT OF THE DATABASE... AND WRITES IT TO SQL... SO THE FIRST THING WE NEED IS TO BE ABLE TO BUILD A TABLE... I NEED TO HAND LAY A TABLE IN SQL, THAT IS FINE, BUT THE VERY NEXT THING, IS THAT WE WILL HAND LAY ALL THOSE SAME WORDS AS NODES SO THE BRAINS CAN LAY IT'S OWN TABLES" (10-19 21:20).

What this build passes, of the four tests from your words: a neuron is its own table (yes); a run assembles the SQL and mother pastes it, births included (yes: the born run is a typed line, replayed); mother decides nothing (yes: she runs text, returns what came back, carries outboxes); only the table-making neurons, hop and trigger are hand-laid (yes, with the list in §1). What it does not pass yet: the brain still holds words in `input`, `sheet`, `secondary` and `output`. The DNA tables, the receipt and the nodes hold only numbers.

## 1. What is hand-laid, and whose it is

| Hand-laid | What it is | Your words |
|---|---|---|
| `input` | the ear: id, text, parent, gates, answer | "make a bottom that takes an input and writes that input into the brain.db" (21:04) |
| the encoder | `encoder(gate, word)`; the ear's trigger cuts a line into tokens and gives new ones a gate. A word is letters and `_`; every digit, space and punctuation mark is its own token | "we need to make the decoder encoder, and the prompt" (20:55); "every punctuation, special char, all of it has to have it's own neuron" (23:08); "create, table, x, (, a, ), ; --> prompt to encoder comes out goes to gate create, space remainder, to gate space" (01:22) |
| `shards(n)` | one counter for the whole brain | "shard numbers are sequential" (00:34) |
| 88 neurons, each: DNA table `g<N>`, gate view `"<N>"`, trigger `t<N>`, definition node, memory node, first shard pointing at the definition node | 7 physics words (heard, said, hop, born, fire, end, build) and 81 words: BUILD, var, the digits 0-9, g t d m, the SQL words you named, and every token of the born run | "EACH NEURON HAS A GATE... THAT IS THE ENTRY TO THE NEURON..... IN SIDE THAT NEURON IT HAS DNA" (21:14); "( , integer , primary, key, arrival, interger, remainder, next, trigger, =, and new, ., trigger, end, ; ... all neurons of their own" (23:03); "every new neuron first dna chard is the definition... a new gate, new dna table and new defintion node is born all at the same time" (23:40); "does it have a memory node for a definition created at the same time? and a memory node" (21:31) |
| the gate trigger (one per neuron, same text for all, only the number differs) | hit the DNA row if (arrival, remainder) exists, write it if not, hand the run to hop | "if chard exists hits the chard, if not writes it" (01:22); "each neuron has one table and one trigger" (23:27) |
| `hop`, `born`, `fire`, `build` | the physics neurons' gates: views with their trigger. hop writes the receipt, fires, closes BUILD, births, lands. born writes the cells and fires born's run. fire types a neuron's memory run as a sub-run. build decodes and pastes | "hop should be it's own neuron... every action is its own nueron" (23:00); "triggers born, if table doesn't exist" (01:22); "a column in the dna chard table just pointed to that trigger neuron" (23:27); "IT WILL FINISH AT BUILD THAT WILL TRIGGER TO THE PY... AND THE OUTPUT OF THE RECIEPT WILL BE THE RUN" (21:52) |
| `receipt` | run, gate, shard, in order | "the run reciept should be... we need to know the gate before and after" (00:31) |
| `sheet` | the cells: run, name, value. `var a` in a line reads cell a | "if create table (var a) .. then it would create a table of what ever is sitting at the newest memory at var a" (23:08) |
| `secondary` | what the source brains sent back | draft §2.6: mother "carries what comes back into the brain" |
| `output` | what a run said; the prompt prints it | "the py on the back end is just get the output and print it" (23:59) |
| `later` | a statement SQLite refused mid-run (a DROP), run when the line ends | "we need a DROP NEURON now also" (23:27); SQLite refuses a DROP while the run is still executing |
| mother | one C function, ~60 lines: run the text, answer ok / rows / error, carry outboxes, write a refusal into the run's output, queue a refused DROP | §0: "the bottom is permitted to have a sql output that inputs an error, or a response from sql back to the neuron graph"; v1's mother.c |

**Not hand-laid, typed by you:** the born run (step 5), the binding of a run to a neuron's memory node (step 6), the trigger column of a DNA row (step 10), every formula (step 10 on), the memory and timeline runs (§0's next: "the runs that input the timeline, the memory nodes, write the dna, read, write, move, copy").

**My choices in the egg, for you to keep or strike:**
1. The gate is a view and the DNA is a table under it. A view can take a landing without storing it, so a landing writes nothing but the DNA row and the receipt.
2. Names: DNA table `g<N>`, gate `"<N>"`, trigger `t<N>`; the definition node and memory node are neurons too, with their own gate numbers, named `<word>.definition` and `<word>.memory` in the encoder.
3. The cells born writes: `gate`, `dna`, `trig`, `def`, `defgate`, `mem`. The cells fire writes: `at`, `before`, `after`, `next`, `prev` (the word the row fired at, the gate before and after it, and the first non-space word each way). The ear writes `run`.
4. `var a` reads the newest cell `a` of the run itself, else the newest `a` of any run.
5. Inside the hop, each write goes to mother as its own statement. SQLite keeps an INSERT's cursor open until its statement ends; a chain 2,000 hops deep would hold thousands open and every hop would walk them. Measured today: 2,400 hops in 106 s before, 3.7 s after.
6. The first shard's trigger column points at the definition node; the hop does not fire it (the definition node has no memory node).
7. mother carries outboxes and writes refusals. Both are "a response from sql back to the neuron graph" (§0).

## 2. Tools

- `sqlite3` 3.37 or newer (hub 3.37.2, hp 3.46.1). `gcc`. `python3` for the prompt only.
- Make a folder, copy the files of `NEURON-BUILD-SHEET-2026-10-25\` into it, open a terminal there. On the hp: `scp -r` the folder, then the same.

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

You should see `ok`, then `error: table t already exists`, then `2`. Mother is the whole bottom. Her C is in appendix A; she runs the text, returns what SQLite says, and carries. She parses nothing and chooses nothing.

## 4. Lay the egg

```
sqlite3 brain.db
.load ./mother
.read egg.sql
SELECT type, count(*) FROM sqlite_master GROUP BY type;
SELECT count(*) FROM encoder;  SELECT n FROM shards;
.quit
```

You should see `index|4`, `table|272`, `trigger|93`, `view|92`; `264` gates; `88` shards (each neuron's first shard, pointing at its definition node). The gate numbers that matter: heard 1, hop 7, born 10, born's memory node g12, fire 13, end 16, build 19, BUILD 22, var 25, space 118.

One hand-laid neuron, BUILD, as SQLite holds it (`SELECT sql FROM sqlite_master WHERE name IN ('g22','22','t22','g23','g24')`):

```sql
CREATE TABLE g22 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER)
CREATE VIEW "22" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g22
CREATE TRIGGER t22 INSTEAD OF INSERT ON "22" BEGIN
  SELECT mother ( 'INSERT INTO g22 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' )
                  || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g22 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ;
  SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g22 WHERE shard = n + 1 )' ) ;
  INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 22 , NEW.arrival , NEW.remainder , NEW.rest ) ; END
CREATE TABLE g23 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER)     -- BUILD.definition, gate 23
CREATE TABLE g24 (id INTEGER PRIMARY KEY, run INTEGER)                        -- BUILD.memory, gate 24
```

and its first shard: `SELECT * FROM g22;` gives `8||23`: shard 8, no arrival, no remainder, trigger 23 (the definition node). That is the whole neuron. Every neuron the brain births has this shape, with its own number, because the born run types this text.

## 5. Start the prompt

```
python3 bottom.py brain.db sources/wn.db sources/gcide.db sources/mw.db sources/mwt.db sources/moby.db sources/map.db sources/sqldoc.db
```

Each line you type goes into `input`; what the brain said comes back, for the line and for each sub-run it started; then anything in `later` is run. Ctrl-D leaves; the brain stays in brain.db.

You can also type at the raw `sqlite3 brain.db` prompt: `.load ./mother` then `INSERT INTO input (text) VALUES ('...');` and `SELECT answer FROM input ORDER BY id DESC LIMIT 1;`. There you must double every `'` inside the line, and run `later` yourself. The prompt below is bottom.py.

To see what happened after any line, in a second terminal: `sqlite3 brain.db ".read look.sql"`.

## 6. First line: a word the brain has no neuron for

```
dog
```

You should see:

```
run 1 said: error: no such table: 265
```

What happened: the encoder gave `dog` gate 265. The hop from heard found no gate "265", so born wrote the cells and looked for born's run; there is none yet. Mother tried to land the run on "265", SQLite refused, and mother put the refusal in the run's output. Nothing is hidden: the one line that failed says why. `.read look.sql` shows the cells born wrote:

```
run  name     value
1    run      1
1    gate     265
1    dna      g265
1    trig     t265
1    defgate  266
1    def      g266
1    mem      g267
```

Your words: "THE NEURONS WILL HAVE TO HAVE THE RUNS FOR CREATE TABLE (IF REMAINDER GATE DOESN'T EXIST,) SUCH THAT A NEW TABLE FOR THAT REMAINDER GATE IS MADE... WITH THE ACTIVE REMAINDER BEING WRITTEN INTO THE FORMULA FOR THE CREATE TABLE" (21:52). The cells are that remainder, written where the born run will read them.

## 7. Second line: the born run, typed once

Paste this one line (it is `BORN-RUN.txt`; 541 tokens; the cells `var dna`, `var gate`, `var trig`, `var def`, `var mem`, `var defgate` are the ones born just wrote):

```
BUILD CREATE TABLE var dna ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ; CREATE VIEW "var gate" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM var dna ; CREATE TRIGGER var trig INSTEAD OF INSERT ON "var gate" BEGIN SELECT mother ( 'INSERT INTO var dna ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM var dna WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM var dna WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , var gate , NEW.arrival , NEW.remainder , NEW.rest ) ; END ; CREATE TABLE var def ( id INTEGER PRIMARY KEY , run INTEGER , secondary INTEGER ) ; CREATE TABLE var mem ( id INTEGER PRIMARY KEY , run INTEGER ) ; INSERT INTO var dna ( shard , trigger ) SELECT n + 1 , var defgate FROM shards ; UPDATE shards SET n = n + 1 ; BUILD
```

You should see `run 2 said: ok` (0.3 to 0.4 s). Every token of this line is a hand-laid neuron, so the run hops 541 gates, and at the second BUILD the words between the two BUILDs are read back with the cells filled and handed to mother. Check:

```
sqlite3 brain.db "SELECT name FROM sqlite_master WHERE name IN ('g265','265','t265','g266','g267'); SELECT * FROM g265;"
```

Five names, and dog's first shard `294||266` (shard 294, no arrival, no remainder, trigger 266 = dog's definition node). Why 294 and not 89: the born run's own 541 hops wrote their new DNA rows first, shards 89 to 293, and the last statement of the run wrote dog's first shard. Dog's neuron exists, made by a run the brain has a receipt of. Your words: "at the end of the run the run reciept will be all that you need to input that code directly into sql, but it will land at build which is the last step of the create new table run.. build will then send that run reciept to the py and py will forward it to sql" (21:52).

## 8. Third line: give born its run

The born run is run 2. Born's memory node is g12. Write the pointer:

```
BUILD INSERT INTO g12 ( run ) VALUES ( 2 ) ; BUILD
```

`run 3 said: ok`. A neuron's meaning is the run in its memory node; this is "write the dna" done by hand, through BUILD. From now on, when a landing finds no gate, born fires run 2 again with fresh cells.

## 9. Births are automatic now

```
cat
```

```
run 5 (sub-run of 4): BUILD CREATE TABLE var dna ( shard INTEGER PRIMARY KEY , arr...
run 5 (sub-run of 4) said: ok
```

The hop found no gate for cat (268), born wrote cells for 268, fired run 2 as sub-run 5, the sub-run built g268 / "268" / t268 / g269 / g270, and the hop landed on "268". `cat` itself said nothing: it has no formula, and a run through the gates with nothing to say says nothing. Your words: running the question straight through the gates and getting the question back is the chatbot answer, and "the chatbot answer is wrong" (draft §3.2).

```
BUILD CREATE TABLE things ( a ) ; BUILD
```

Two sub-runs (things, a are born), then `run 6 said: ok`, and `sqlite3 brain.db ".tables things"` shows the table. Your BUILD line reached the SQL prompt through the neurons, as v1's did.

A line of 1,000 known tokens runs in about 1 s on the hub and the hp; the same line again (every row a hit, nothing written) the same. 2,400 hops: 3.7 s hub, 4.1 s hp. The cost per hop does not grow with the line.

Shards: `SELECT n FROM shards` and the sum of rows over all `g<N>` DNA tables agree; one sequence, no gaps (checked after every test today).

## 10. Teach a word: define

Three lines, typed once. First type `define dog` once, so that define is born, then read its two gate numbers:

```
define dog
```

`define` is born (sub-run 10 of run 9). Nothing else: define has no run yet. Now `sqlite3 brain.db "SELECT gate, word FROM encoder WHERE word IN ('define', 'define.memory')"` gives the two numbers. After exactly the lines above, in order, they are 277 and 279 (dog 265, cat 268, things 271, a 274, define 277). Read them; do not assume.

Line A, the define run, typed once as a line. Two BUILD pairs: ask WordNet for the word after `define`, then read back what came:

```
BUILD INSERT INTO wn . inbox ( run , word ) VALUES ( var run , 'var next' ) ; BUILD BUILD SELECT text FROM secondary WHERE run = var run ; BUILD
```

Typed directly it says `ok` and `ok` (and births wn, inbox, word, text, secondary as sub-runs): no cell `next` exists yet, so WordNet was asked for the literal "var next" and got nothing. That is fine; the line exists as a run now. After exactly the lines above it is run 11 (the prompt prints the number; call it R).

Line B, bind the run to define's memory node (`g<define.memory>`, here g279; R, here 11):

```
BUILD INSERT INTO g279 ( run ) VALUES ( 11 ) ; BUILD
```

Line C, make define's DNA row fire it. The row that `define dog` hit is (arrival heard, remainder space): the first word of a line arrives from heard, and the next gate is the space. Point that row's trigger column at define itself (`g<define>`, here g277):

```
BUILD UPDATE g277 SET trigger = 277 WHERE arrival = 1 ; BUILD
```

Now:

```
define dog
```

```
run 19 (sub-run of 18): BUILD INSERT INTO wn . inbox ( run , word ) VALUES ( var run...
run 19 (sub-run of 18) said: ok
a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since prehistoric times; ...
a dull unattractive unpleasant girl or woman; "she got a reputation as a frump"; "she's a real dog"
informal term for a man; "you lucky dog"
someone who is morally reprehensible; "you dirty dog"
a smooth-textured sausage of minced beef or pork usually smoked; often served on a bread roll
a hinged catch that fits into a notch of a ratchet to move a wheel forward or prevent it from moving backward
metal supports for logs in a fireplace; "the andirons were too hot to touch"
go after with the intent to catch; "The policeman chased the mugger down the alley"; "the dog chased the rabbit"
```

What happened: the hop hit define's row (heard, space), whose trigger column names define; fire wrote the cells `at=define before=heard after=' ' next=dog` and typed define's memory run as a sub-run; its first BUILD asked WordNet for `'dog'` (the cell `next`); WordNet's own trigger filled its outbox; mother carried eight rows into secondary; the second BUILD read them back; mother returned the rows; they are the sub-run's output. `define cat` does the same for cat (two WordNet rows), through the same DNA row, because `define cat` also arrives from heard with the space next.

This is the pattern for every word you teach: type the run once; put its number in the word's memory node; point a DNA row's trigger at the word. Your words: "the formula should be able to be built by the brain, by taking the variables and inserting them into the formula.. then once done the brain outputs to /build and it gets built" (10-16 08:48). The variables are the cells; the formula is the run in the memory node; /build is BUILD.

## 11. The source brains

Each file in `sources/` is a brain of its own: `corpus(word, hw, text)`, `inbox(id, run, word)`, `outbox(id, run, word, hw, text)` and one trigger, `work`: an ask landing in the inbox is answered into the outbox at once. Mother carries the outbox into `secondary` after every statement she runs and empties it. The brain reaches a source only by naming its inbox in a BUILD line: `INSERT INTO wn . inbox ( run , word ) VALUES ( var run , 'dog' )`. To use a source, pass its file to bottom.py (it ATTACHes it under its file name).

The corpora here are the 470-word slices captured on 10-22/25 (WordNet, Webster 1913, Merriam-Webster, the MW thesaurus, Moby, your relation map, the SQLite docs). The full dictionaries are on the hp: WordNet 3.0 at `/usr/share/wordnet/`, Webster 1913 (GCIDE) in dictd at `/usr/share/dictd/gcide.*`, with a dictd server running. Loading those into a `corpus` table is a one-time import, not brain work; the schema is `sources/source-schema.sql`, and `.import` of a TSV (word, hw, text) fills it.

## 12. What you will hit next, in the order you will hit it

1. **A new DNA row has no trigger.** `define cat` worked because it hit the same row as `define dog`. A row the brain writes new has trigger NULL and fires nothing until you set it. Your words: "When a trigger fires, and when it stays quiet, is learned" (§2.2). How a new row gets its trigger is yours to decide; today you set it with a BUILD UPDATE.
2. **Cells are the newest of the run, else the newest anywhere.** A sub-run reads its parent's cells only because they are newest. Your 23:08 words are "the newest memory at var a". Per-run scoping is a change in `build_go` when you want it.
3. **Memory and timeline.** Nothing is written when a run ends but the receipt. §0's next runs: "the runs that input the timeline, the memory nodes, write the dna". The `end` neuron is where they hook: its memory node is empty; a run you type and bind there will fire at the end of every line.
4. **The definition node is empty.** `define` printed what came back; it did not write dog's definition node (g266). A third BUILD pair in the define run can: `INSERT INTO var def ( run , secondary ) SELECT run , id FROM secondary WHERE run = var run` needs the cell `def` of the word being defined, which born writes only at birth. Deciding where the sheet gets a word's node from is yours.
5. **Words in the brain.** `input`, `sheet`, `secondary`, `output` hold text. Your design holds numbers and an encoder. The DNA tables, receipt and nodes already do.
6. **Spaces double the hops.** Every space is a landing. That is your design (01:22); it is also why `after` is usually `' '` and `next` is the word.
7. **A DROP inside a run waits.** SQLite refuses `DROP` while the run is executing; mother queues it in `later` and the prompt runs it when the line ends (`run 13 said: later`, then `later: DROP TABLE things ; -> ok`).
8. **BUILD is exact.** `BUILD` upper case, paired. `build` is the physics neuron's word.
9. **Quotes at the raw sqlite3 prompt** must be doubled inside the line; bottom.py takes the line as typed.

## 13. Traps I fell into building this today, so you can see them coming

- I made mother silent for births and landings in 17.x so the log read clean. Here every mother call that is not `ok` lands in the run's output, and `look.sql` reads the tables; there is no log text.
- I first gave every DNA row its own SQL trigger (16.4 to 17.3). One gate trigger per neuron is your 23:27 words and is what the born run types.
- The first replay of the born run appended `end` to the text (the end landing's receipt row), which made a new word every time, which was born, which replayed it: a runaway at 100% CPU. The formula text now leaves out heard, said and end.
- The hop cost grew with depth (2,400 hops: 106 s). Three guesses were wrong (a primary key, a NOT NULL, an output cursor); the profiler named it: SQLite's INSERT keeps its cursor open until the statement ends, and in a trigger program that is the end of the whole nested chain. Every write inside the hop now goes to mother as its own statement; 2,400 hops: 3.7 s.
- SQLite 3.46 (the hp) refuses a function in a trigger unless it is marked innocuous; mother.c has the flag.

## Appendix A. mother.c

```c
/* mother(text) / mother(text, run): the brain hands SQL text to mother. She runs it at the SQL prompt and answers
   'ok', the rows a SELECT sent back, or 'error: ...'. She never stops the brain, so a refusal can be felt and remembered.
   After the text ran, she carries what the source brains put in their outboxes into the brain's secondary input and
   empties the outboxes. With a run given, what came back that was not 'ok' is written into that run's output.
   A statement SQLite refuses inside a run (a DROP) is queued in later. She decides nothing and works no data.
   Build:  gcc -shared -fPIC -O2 -o mother.so mother.c -I.      Load in sqlite3:  .load ./mother   */
```

The full file is `NEURON-BUILD-SHEET-2026-10-25\mother.c` (about 60 lines). `egg.sql` was written by `gen_egg2.py` in the same folder; read it to see every rule the egg holds, and nothing else holds any.

## Appendix B. Checks run today

| Check | Hub (3.37.2) | hp (3.46.1) |
|---|---|---|
| egg lays: 272 tables, 92 views, 93 triggers, 264 gates, 88 shards | yes | yes |
| `dog` → `error: no such table: 265`; cells written | yes | yes |
| born run → `ok`; g265 / "265" / t265 / g266 / g267 exist; first shard 294 → 266 | yes | yes |
| bind → `ok`; `cat` born by sub-run; `BUILD CREATE TABLE things ( a ) ; BUILD` → `ok`, table exists | yes | yes |
| a born neuron's trigger text equals the hand-laid form | yes | not re-checked |
| shards one sequence, no gaps, no duplicates (345 after the sequence) | yes | yes (374) |
| 1,000 tokens: 0.9 s; again (all hits): 0.8 s | yes | |
| 600 / 1,200 / 2,400 tokens: 0.7 / 1.7 / 3.7 s | yes | 2,400: 4.1 s |
| WordNet ask through BUILD → 8 secondary rows; `define dog` prints them; `define cat` births cat and prints 2 | yes | yes |
| `BUILD DROP TABLE things ; BUILD` → `later`, run by the prompt → `ok` | yes | |
