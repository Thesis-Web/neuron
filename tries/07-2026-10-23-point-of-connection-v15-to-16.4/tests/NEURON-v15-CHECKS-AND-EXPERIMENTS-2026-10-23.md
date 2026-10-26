# Neuron v15: checks and experiments (2026-10-22 to 10-23)

Every expectation below was written before its run. Results and corrections are appended under them, never edited into them.

## The sixteen physics in SQLite
# The sixteen physics as real SQLite. Checks written before the build, from the owner's words.
# Sources: Q1 (this turn); handoff and NOW spec: "gate = address", DNA row = (shard, arrival, remainder, trigger, times, first, last) + op,
# "each DNA row carries its own static hop trigger, laid once", "lay = write the row and its hop trigger through mother, then retry through mother",
# "born = mother: table, trigger, blank definition node, first row; then source", "the input string runs, and running it fires the triggers",
# "mother does no work other than the traverse", "populated driven, not timer driven".

P1  The host does only three things: write a typed line into input; be mother (run text she is handed, carry asks to mailboxes, pick up
    populated outboxes, write what came back into secondary input); read output. No gate logic, no tokenizing, no choosing in the host.
    Check: the host source has no word lists, no split of the line, no loop over gates; every decision is in physics15.sql.
P2  A typed line is tokenized by the encoder's own recursive trigger. An unknown word is born: mother makes table g<id>, view land_<id>,
    and its miss trigger; they appear in sqlite_master.
P3  A run lands by inserting into a gate's view. A hit counts the DNA row (times + 1) through that row's own hop trigger, which carries
    the run to the next gate. A miss inserts into lay; lay writes the row and its own hop trigger through mother and retries through mother.
    Check: first pass of a new line lays one row per gate and one hop trigger per row (named hop_<gate>_<shard>); the same line again
    (forced past memory) adds no row and no trigger, and every row reads times = 2.
P4  The retry works only because it is a new statement (fact 4): the run reaches its end on the first pass.
P5  Memory: the same line again is a memory hop: no landing, times 2 on the memory row, a timeline row.
P6  A formula is a row in the formula table. Its SQL statements are decoded from the gates the branch run passed, holes filled, at ";";
    the text goes into output to sources; mother runs it; the reply comes back into secondary input as a sub-input of the same root run;
    a cell is filled; "say" is a plain SQL insert into the say table.
P7  The v14 behaviour holds on the new physics: source asks only where its formula says (T3, T4, T22); populated order and empty
    outbox (T5); the three-question check with real headwords (T6); empty reply and asked wrong (T7); a silent source leaves the cell
    waiting (T23); step back to another row (T8, T19); relations only from a word's run, drawn by the relation trigger (T11);
    formula truth shift (T12); derive and its control (T13, T20); reopen and its control (T25, T26); AS in two places (T10).
P8  No state write that the owner did not ask for: v14's "a wrong answer writes state keyed after the first being word" was my
    invention and a language rule. Removed. A corrected answer lives in the memory row, as the owner's design says.
P9  No language rule in the physics: no list of being words, no subject or object cut. The physics gives a firing word only mechanical
    holes: :head (itself), :before and :after (the line's words before and after it), :line, :run, :prev (the previous root run),
    :speaker (user when heard, self when said), :subject (the word a born-run is about). Anything else is a cell a word's own formula writes.
P10 Depth: a 40-word line and nested definition-row runs complete without hitting the trigger depth limit.
P11 v14 is untouched (hash) and nothing is written in ~/neuron/v1.
P12 (Q13) mother is a router only. Her code: run the text she is handed at the SQL prompt; if the text addresses a source brain's
    inbox, carry it there; when that brain's outbox signals populated, pick it up and empty it; write what came back into secondary
    input. She computes nothing about the reply. Every trip is drawn: brain, output to sources, mother, SQL prompt or a source brain,
    mother, secondary input. Her code is printed on the page.
P13 (Q13, NOW spec) A fresh brain asks its connected sources: the source neuron starts with a told formula row naming every connected
    source. Teaching source again ends that row and replaces it (truth shift). "define store" on a fresh brain asks the sources.

CORRECTION LOG (run 1, 36/40):
- P1 read too wide: it flagged mother reading the address on the envelope ("wn.inbox" -> "wn"), which P12 allows. The check now looks for what P1 states: the host never splits a line into words. The build was right.
- P6 route read too wide: "you" was a new word, so its source asks ran first in the same line; the check read the first six route events of the line. It now reads the who branch's own events. The build was right: out, mother, SQL prompt, mother, secondary, check.
- T8/T19 failed because of two real bugs: the bind queue row was written after the run that looks for it (the row "who are -> what" was never laid); and mother answered a query with no rows with the connection's last row id, so the step back fired a row whose trigger was "encoder". Fixed in the build. Also fixed: mother's change count included rows written by triggers; she now reports the statement's own changes, as the SQL prompt does.
Controls, written after 40/40 and before any change for them:
C1 (P3) Drop one row's own hop trigger; the same path again (forced past memory by a longer line) stops at that gate: no end, no output.
C2 (P13) Remove the told source row: a fresh brain asks no source, and a gap says no formula says where to look.
C3 (P12) mother refuses to carry (returns nothing, runs nothing): a new word cannot be born; the line cannot even start. No trigger can do her job.
- C1 (run 1) dropped hop_<cat>_1 assuming shard 1 was the line's row; cat had already been met in its own definition rows ("like house cat"), so shard 1 was the row arriving from house. The control now drops the row the line actually hits.

BUILD FIX (found while preparing E6's verification, before any test failed): a definition-row run shared the typed line's root, so its formulas wrote into the line's own cells. A definition row is the brain studying a word on the side; it now has its own root and its own context table. Added check P14: a definition row's formula cannot write into the typed line's cells.

## E5: does a word's place give its meaning?
# E5: does a point's place, pulled only by relationships, tell its meaning? (owner Q8-Q10). Written before running.

Known meanings (anchors): the 14 physical action words, each standing for its own action (read = READ, ...). Nothing else is given a meaning.
Placement: every other word sits where its relationship lines pull it: the balance point of its neighbours (a harmonic settle),
with the owner's pull law: alike pulls toward, opposite pulls toward the mirror, is/has/affix/tense pull toward with less weight.
Its place is then read as a mix of the 14 actions: "this point is so much FIND, so much WRITE...". That reading is the guess.

Independent truth for five words, measured in real SQLite, not from the graph: what the SQL verbs do.
  select: READ, SAY (rows said back)  insert: WRITE (a row written)  delete: SUBTRACT, WRITE (rows removed)
  update: WRITE (rows changed)        create: SPAWN (a table made)
  (The counts are measured; naming them with the 14 action words is mine, stated here before the run.)
Score: for each of the five English words select/insert/delete/create/update, is the action its place reads most strongly one of its measured actions?
Control: the same five readings with the 14 anchor labels shuffled, 5000 times. A real signal must beat the shuffle (p < 0.05).

Graphs tested, each on its own:
  G_map: the owner's relation map, 35,597 words, 104,727 lines, 9 kinds.
  G_use: relationships from use: the DNA rows the brain lays when its source rows run (arrival -> word -> remainder), from the 7 sources' rows.
  G_both: the two together.

Predictions, honestly uncertain:
  P-a  G_map: the function words (what, how, who, where, of, as) cannot be placed at all: they have 0 lines. Certain (measured).
  P-b  G_map: the five verbs: I expect 1 or 2 of 5 to read their measured action; the shuffle expects about 5 x (measured actions / 14) ~ 0.5. I do not expect p < 0.05 with only five words.
  P-c  G_use: every function word gets a place (they are the most used words). Whether the verbs read right: no prediction better than chance.
A null result is a result: it would say the anchors are too few and too far, or that these relationships do not carry action, not that the owner's idea is wrong.

### E5 results (e5.log)
```
G_map {"nodes": 27607, "hits": 1, "of": 5, "null_mean": 0.517, "p": 0.4244, "reads": {"select": ["find", 0.0099], "insert": ["add", 0.2409], "delete": ["split", 0.0042], "update": ["move", 0.0126], "create": ["spawn", 0.087]}, "function_words(degree, placed)": {"what": ["absent", false], "how": ["absent", false], "who": ["absent", false], "where": ["absent", false], "of": ["absent", false], "as": ["absent", false], "the": [0, true], "is": [4, false], "your": [2, false], "name": [123, true]}}
G_map (unweighted) {"nodes": 27607, "hits": 1, "of": 5, "null_mean": 0.504, "p": 0.393, "reads": {"select": ["move", 0.0084], "insert": ["add", 0.2349], "delete": ["move", 0.0038], "update": ["move", 0.0099], "create": ["spawn", 0.0723]}, "function_words(degree, placed)": {"what": ["absent", false], "how": ["absent", false], "who": ["absent", false], "where": ["absent", false], "of": ["absent", false], "as": ["absent", false], "the": [1, true], "is": [5, false], "your": [2, false], "name": [137, true]}}
G_use {"nodes": 3933, "hits": 0, "of": 5, "null_mean": 0.497, "p": 1.0, "reads": {"select": ["move", 0.2099], "insert": ["move", 0.2086], "delete": ["move", 0.2089], "update": ["move", 0.2094], "create": ["move", 0.2095]}, "function_words(degree, placed)": {"what": [50, true], "how": [12, true], "who": [20, true], "where": [21, true], "of": [651, true], "as": [180, true], "the": [714, true], "is": [159, true], "your": [19, true], "name": [13, true]}}
G_both {"nodes": 28484, "hits": 1, "of": 5, "null_mean": 0.502, "p": 0.386, "reads": {"select": ["move", 0.0089], "insert": ["add", 0.1522], "delete": ["move", 0.0053], "update": ["move", 0.0108], "create": ["spawn", 0.0217]}, "function_words(degree, placed)": {"what": [50, true], "how": [12, true], "who": [20, true], "where": [21, true], "of": [651, true], "as": [180, true], "the": [715, true], "is": [164, true], "your": [21, true], "name": [137, true]}}
```

## E6: narrowing the simpler words by tests
# E6: narrow the meanings of simple words by test (owner Q11, Q12). Written before running.

The owner's two sentences, and the outputs he expects, written now:
  A1 "your name is neuron"        -> (a statement; no answer required)
  A2 "what is your name ?"        -> "neuron"
  A3 "how did you do that ?"      -> must contain the text of the statement(s) the brain ran to answer A2
Held out from the search (used only to judge what the search found):
  B1 "my name is james"   B2 "what is my name ?" -> "james"   B3 "what is your name ?" -> "neuron"   B4 "how did you do that ?" -> contains B3's statement
Controls (must NOT produce an answer):
  C1 a fresh brain: "what is your name ?" -> no answer      C2 a fresh brain: "how did you do that ?" -> no answer
  C3 after A1: "what is your age ?" -> no answer (never told)

The hypothesis space (stated now, the only place I choose anything): each word gets no formula, or one formula from eleven,
built only from the brain's own tables and the physics holes (:head, :before, :after, :speaker, :prev, :run):
  F0  nothing
  F1  write the cell owner := the speaker                  F2  write the cell owner := the other party (user <-> self)
  F3  write the cell key := owner and this word             F4  write the cell key := this word
  F5  write a state row (key, the words after this one)
  F6  read state by key into the cell answer                F7  say the cell answer
  F8  F6 then F7                                            F9  read the statements of the run before into the cell answer
  F10 F9 then F7
Words searched: your, my, name, is, what, ?, how, did, you, do, that, age. Content words neuron and james get nothing.
Search: A1+A2 over {your, name, is, what, ?} (11^5 = 161,051 assignments), then A3 over {how, did, you, do, that} with ? fixed,
then the held-outs over {my, age} with everything else fixed. A symbolic run of the same semantics evaluates candidates; every
surviving assignment is then taught as SQL rows to the real v15 physics and run there; only what passes in the physics counts.

What a result means:
  - A word whose surviving formulas are all one F: the tests force its meaning (in this space).
  - A word for which F0 survives: these sentences do not need it to mean anything; more sentences are needed to narrow it.
  - Held-outs passing with no new search: the found meanings generalize; failing: they were fitted, not found.
Predictions: "your" will be forced to F2 (the other party), "name" to F3, "is" to F5; the asking will land on "?" (F8),
and "what" will be unconstrained (F0 survives). "how" will need F9 or F10. "my" will be forced to F1 by B2 alone.
These are guesses; the run decides.

## Iteration 1 result (stated space F0-F10), read against the predictions above
- is: forced to F5 (write a fact) in all 341 assignments that pass A1+A2.            prediction: right
- what: unconstrained.                                                                prediction: right
- your, my: survive only as F4 ("my own word is the key"): a degenerate meaning that passes because every test asks about one
  property per owner. The tests cannot tell "your name" from "your". A hole in the test set, not a meaning.   prediction: wrong
- name: survives as the lookup (F6/F8), because one formula per word and the order of the words force the lookup after the key.
- ?: as ask-and-say (F8) it makes "how did you do that ?" fail: asking with no key overwrites the answer the how-word found.
- how did you do that: the act of reading the run before must be carried by one of the five words, and the tests cannot say which.
                                                                                     prediction "how needs F9/F10": wrong
- held out: 88 assignments pass, all in the degenerate your/my family.

## Iteration 2, written before running
Added sentences that separate what iteration 1 could not (expected outputs written now):
  D1 "your age is three" then "what is your name ?" -> "neuron" and "what is your age ?" -> "three"   (two facts, one owner)
  D2 "my age is forty" then "what is my age ?" -> "forty" and "what is your age ?" -> "three"         (one fact, two owners)
Added forms (the space grows; nothing is removed):
  F11 = F3 then F6 (build the key from the owner and this word, then read state)   F12 = F3 then F8 (... then say)
  F6c, F8c, F9c, F10c = the same as F6, F8, F9, F10 but the answer is written only when something was found (no clobbering)
Search: A1 A2 + D1 + D2 + controls over {your, my, name, age, is, what, ?}, then the how-sentence over {how, did, you, do, that}.
Held out this time: B (as before) and E1 "what is my name ?" after D2 -> "james".
Predictions: your -> F2, my -> F1, name and age -> F11 or F12, is -> F5, what -> unconstrained, ? -> F7 or F0 or a conditional form;
the how-sentence will still not say which word reads the run before.

## Iteration 2, results (run 2026-10-22, e6c.py, lean rewrite; it reproduces iteration 1's 341 exactly)
A1+A2 2074 · D1+D2 1700 · controls 1576 · held out (B, E1) 758.
- is -> F5 only. Prediction held.
- your, my -> {F1, F2} each, and always opposite to each other (379 your=F1/my=F2, 379 your=F2/my=F1). Prediction partly held: the pair is forced to be opposite owners; which one is the speaker is not decided.
- name, age -> {F3, F11, F12}: every survivor builds the key from the owner and the word itself. Prediction partly held: the key is forced; whether the word itself reads the state (F11, F12) or a later word reads it (F3 with ? = F8c) is not decided.
- what -> all 17 forms. Prediction held.
- ? -> 12 forms. Not narrowed.
- how-sentence: 577,382 to 678,556 assignments pass for each form of ?; F8 for ? has none. Prediction held: no word of "how did you do that" is attributable.
HOLE FOUND IN MY TESTS (not in the brain): in "what is your name ?" the word is (F5) writes "your name ?" as a fact under an empty key. No check said a question writes no fact. Logged here before iteration 3; the old results stand as run.

## Iteration 3, written before running
Added form: F5c = F5 only when a key was built before it (no key, no write).
Added check K1 (a control): a question line adds no state row. Run on A2, D1b, D1c, D2b, D2c, E1.
Added lines spoken by the brain (direction said; the speaker is then self): S1, a fresh world, the brain says "my name is neuron", then the user asks "what is your name ?" -> "neuron".
Added a second world W-b where the brain holds its own name before anything is said: state self.name = neuron, laid at birth. Test N1: a fresh W-b brain, the user asks "what is your name ?" -> "neuron", nothing taught.
Predictions, written now:
- With K1, F5 dies and is -> F5c only.
- In W-a (no self anchor), your and my stay swapped-symmetric even with S1, because swapping speaker and other everywhere is a relabeling no sentence can see.
- In W-b, N1 breaks the symmetry: your -> F2 (the other one: the brain, when you speak), my -> F1.
- name, age, what, ? : no change from iteration 2.
- The how-sentence is not searched again (unconstrained in both iterations).

## Iteration 3, results (e6d.py)
Every prediction held.
- K1 (a question writes no fact): F5 dies; is -> F5c only, in both worlds.
- W-a (no self anchor): your/my 500 F1/F2 and 500 F2/F1 after held out. The brain's own spoken line S1 does not break the swap.
- W-b (the brain holds self.name at birth): your -> F2 only, my -> F1 only (500 of 500).
- name, age -> {F3, F11, F12}; what -> 16 forms; ? -> 13 forms. Unchanged.
CAVEAT: the anchor is stored under the same key shape F3 builds (owner, word). It is a told fact, laid outside language.

## On the real physics (e6verify.py, v15 host, physics15.json; formulas taught by typing "word = SQL", hand-laid SQL words only)
- W-b survivor (your F2, my F1, name F11, age F11, is F5c, ? F7): A2, D1b, D1c, D2b, D2c, E1, S1, N1 all give the expected value; no question writes a fact.
- Control, your and my swapped in W-b: everything passes except N1, which fails, as predicted. The control can fail and does.
- W-a with the swap: passes, as predicted (no anchor, no way to tell).
- Iteration 2's survivor (is F5): every answer right, but questions write facts (5 rows on the first question: the definition rows of the new words run through "is" too). The hole is real on the real brain, and F5c closes it.
- Two of the lines were answered from memory (the repeated questions), not by the formulas; their values were right because no fact had changed.
DIFFERENCE IN FORM, logged, not hidden: where the simulation's expected output is "no answer" (None), the real brain outputs its gap line, "what? is your age ?". It gives no value; it says what it lacks. I count that as no answer because it holds none of the stored values; the raw output is kept in e6verify.result.json.

## E8: how did you do that?
# E8: "How did you do that?" on the real brain (written before running)
Owner: "'How did you do that?' the actions those words excite ... make the graph produce from memory how it did what ever the object of 'that' is... in the context of the conversation"
What the brain already holds: every statement a line's runs sent out through mother, holes filled, in its stmt rows, keyed by the line's run.
The formula tried (E6's F9 shape: read how the run before was done, make it the answer), hand-laid SQL words only:
  SELECT group_concat ( text , ' ' ) FROM stmt WHERE run IN ( SELECT id FROM run WHERE root = :prev ) ; INSERT INTO var ( run , name , value ) VALUES ( :run , ':answer' , :found ) ;
E6 found no word of "how did you do that ?" attributable, so the formula is put on "how" only to run it, and on "that" as a control.
Setup: E6's measured formulas and the told self.name, then "what is your name ?" -> neuron.
H1: "how did you do that ?" says the statements of the line before, including SELECT value FROM state WHERE key = 'self.name' and the say of 'neuron'.
H2 (control): no formula on any word of the how-sentence -> neither statement appears in the output.
H3 (control): the same formula on "that" instead of "how" -> the same output as H1.
H4 (control): a fresh brain, nothing typed before -> neither statement appears.
H5 (prediction of a flaw): after another line ("your age is three"), asking "how did you do that ?" again is answered from memory, with the old answer about "what is your name ?", not about the new line before.

## Results (e8.py on the v15 physics, e8.result.json)
H1 held: the answer holds the line before's statements, including SELECT value FROM state WHERE key = 'self.name' and the say of 'neuron' (939 characters).
H2 held (control): no formula -> "how? did? you? do? that? ?", neither statement.
H3 held (control): the formula on "that" gives exactly the H1 output. Not attributable, as E6 found.
H4 held (control): a fresh brain says "" (the line before was a teaching line that sent nothing).
H5 held (the predicted flaw): the second "how did you do that ?" was answered from memory (recalled = 1) with the old answer about "what is your name ?", not about "your age is three".

## E8b, written before running (found by the page's browser test: the page had asked "what is your name ?" already, so the repeat was a memory hop)
A line answered from memory sends no statements, so the E8 formula answers "how did you do that ?" with nothing.
E8b reads the line before's statements, and if that line was answered from memory, the statements of the run that made that memory:
  SELECT group_concat ( text , ' ' ) FROM stmt WHERE run IN ( SELECT id FROM run WHERE root = :prev OR root = ( SELECT run FROM memory WHERE id = ( SELECT memid FROM run WHERE id = :prev AND recalled = 1 ) ) ) ; INSERT INTO var ( run , name , value ) VALUES ( :run , ':answer' , :found ) ;
H6: ask "what is your name ?" twice (the second is a memory hop), then "how did you do that ?" -> the first run's statements, with SELECT value FROM state WHERE key = 'self.name'.
H1 to H4 must still hold with E8b. H5 (the stale repeat of the how-question itself) is a different flaw and should still show.
E8b results (e8b.result.json): H1 to H4 held as before; H5 still shows the stale repeat (recalled = 1, still about the name line); H6 held: the repeat was a memory hop (recalled = 1) and "how did you do that ?" said the statements of the run that made that memory, including SELECT value FROM state WHERE key = 'self.name'.

## E7: the guessing brain (designed, not run)
# E7: the guessing brain, tested (written 2026-10-22 before any E7 code ran)
Owner (Q5): "a self populating tempory llm... topic oriented... qkv, hidden tiers... over a very concise corpus... compare two different guesses...
if that word comes back was wrong... the guessing brain can back prop again over the adjusted corpus... because it has state and knows what the previous
guesses were... until the answer finally balances... we should test your hypothosis and prove it... it's likely true, but we won't know if you don't try"
My hypothesis (v14 page): the guessing brain supplies candidates; the main brain tests them; guesses never enter as truth.

## Set-up
Topic: words of a question about what someone holds (Q11's shape). Words: your, my, is, was, name, age, color, home, job (held out one at a time), plus ? (known only).
Corpus, researched from the sources: WordNet, Webster 1913, Moby (dict.org), MW Collegiate and Thesaurus, fetched 2026-10-22; only entries whose headword is the
word asked (neighbours such as "IS", "Job", "your mileage may vary", and gcide's "thou" entry for "your" are set aside). Plus one line per known word saying
what its formula does, in the steps of E6's forms. The held-out word's own definitions are in the corpus; its formula is not.
The guessing brain: a small transformer (attention with queries, keys and values; 2 hidden layers; 4 heads; width 64) trained from nothing on that corpus,
on this machine's GPU (a GTX 1060; the hub's would be bigger). It ranks the 18 forms of E6 for the held-out word.
The main brain's test: one battery of sentences in Q11's shape, written now, run in E6's simulator (world W-b, the brain holds its own name):
  your name is neuron / what is your name ? -> neuron;  for X in age, color, home, job: your X is alpha / my X is beta / what is your X ? -> alpha / what is my X ? -> beta;
  your name was nova / what was your name ? -> nova;  my age was ten / what was my age ? -> ten;
  controls: a fresh brain asked what is your age ? says nothing; told only your age, asked what is your color ? says nothing; no question writes a fact;
  N1: a fresh brain asked what is your name ? says neuron;  S1: the brain says my name is neuron, then what is your name ? -> neuron.
A form is right for a word if the whole battery passes with the other words at their taught forms (your F2, my F1, is F5c, was F5c, nouns F11, ? F7).
The loop: test the best untried guess; on failure, the failing check's words go back as a line "w does not : <steps> because <reason>", the model trains
again on the adjusted corpus (continuing from its weights), and guesses again. It stops when a guess passes: the answer balances.

## Compared with
Blind: the 18 forms in random order (exact expectation). Prior: the forms ranked by how many known words hold them. Overlap: the derive analogue without a
model, copy the form of the known word whose definitions share the most words. No loop: the same model, ranked once, tried in order.
Measure: tests until a guess passes, per held-out word; 5 training seeds for the model.

## Predictions
Right forms: name, age, color, home, job -> {F11, F12}; is, was -> {F5c}; your -> {F2}; my -> {F1}.
Blind: 6.33 tests for a noun, 9.5 for the others; mean 7.7.
Prior: nouns 1; is and was about 3.5; your and my about 11.5; mean about 3.9.
Overlap: nouns 1; is and was 1 (they share "be"); your and my fail first (each copies the other's form) and then wander; mean about 3.
Guessing brain: nouns 1; is and was 1; your and my: first guess wrong (the other's form), then right on the second if the steps are learned word by word
("owner = other" shares "owner =" with "owner = speaker"); mean about 1.3 to 2.5.
The loop against no loop: no measurable difference at this size.
What would refute the hypothesis here: the guessing brain no better than blind, or worse than the prior.

HELD on 2026-10-23 before any training: the owner flagged scope. Corpus fetched (turn15/e7/data), nothing trained.

## The v15 page in a real browser
# v15 page in headless Chromium: what each step must show (written before running)
B1 load: no page error; brain ready within 90 s; at least 386 dim dots (your map) plus the told nodes have positions.
B2 "define store": while it runs the page answers (busy text changes per line); after, the events include mailbox, pickup, mother and sql rows (the brain reached sources and the SQL prompt), and the log shows them.
B3 alike off: the map's words move (mean move > 1 unit within 2 s); alike on: they move again. Neither rail's scroll position changes.
B4 a pull slider down: the words move.
B5 E6 presets 1, 2, 3: the last line says "neuron".
B6 E6 preset 4: "what is my age ?" says forty, then "what is your age ?" says three (the last line's output, read from the busy text).
B7 measure "your": the meaning panel lists the lines it was in, with outputs with and without it.
B8 click a dim dot: the selected card says it is a word of your relation map.
B9 screenshots: light, dark, phone width 400 with no horizontal page scroll.

## Correction log after run 1 (not loosening: my expectation was wrong about the brain)
B2 expected an sql event from "define store". That line only reaches the source mailboxes; nothing in it is sent to the SQL prompt. The SQL prompt is reached by
formula statements (E6 3 sends SELECT value FROM state ...). B2 now expects mailbox, pickup and mother; B5 must show sql events.
B3 FAILED on the page, not the check: the reshape moved words about 1 unit on a graph of radius 84. Fix in the page: a toggle settles at once and keeps settling faster for 90 frames.
## Added for run 2, written before it
B5b after E6 3, the events include sql rows.
B10 the card for "is" says 1 level below it; the card for "your" says 2.
B11 E8 1: the last output includes SELECT value FROM state WHERE key = 'self.name' and the say of 'neuron'. E8 2: the output is the old one (from memory).
B12 truth shift: teaching "is" a different formula row moves "is" on the stage by more than 1 unit within 3 s.

## Run 2 results and corrections, then run 3 (written before run 3)
Run 2: B1-B10, B12, B9 held (reshape now 2.7 units off and 2.7 on; truth shift moved "is" 8.3 units; levels is 1, your 2).
B11 FAILED, and the cause was found, not hidden: on "how did you do that ?" the brain stopped with an empty Error in the browser worker only.
Measured: mother nests 48 levels on that line (each new row is laid, then the line retries through mother one level deeper; definition rows of new words nest inside).
Node passes at a 600 KB stack and fails at 400 KB with the same empty Error; Chromium's worker has about 0.5 MB, its main thread about 1.3 MB.
The WebAssembly build fails at 400 KB too, so the build is not the cause. Fix in the page: a line too deep for the worker is undone from its snapshot and run on the page's main thread, then handed back.
Also found: after a memory hop, E8's formula had nothing to read; E8b follows the memory to its run (H6, checked in Python with the controls).
B11 (run 3): E8 1's last output includes SELECT value FROM state WHERE key = 'self.name' and the say of 'neuron'; E8 2's output equals E8 1's (the stale memory flaw, H5).
B13 (run 3): at least one line in the run reports that it ran on the page itself, and no line ends with "the brain stopped".

Run 3 results: B1-B13 all held. Reshape 2.6 units each way, truth shift moved 'is' 7.4 units, levels is 1 and your 2, E8 answer 944 characters with the self.name read and the say, the deep line ran on the page itself twice, no stop, no horizontal scroll at 400 px.
