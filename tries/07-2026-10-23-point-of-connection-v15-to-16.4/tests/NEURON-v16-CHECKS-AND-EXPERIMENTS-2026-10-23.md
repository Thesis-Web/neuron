# Neuron v16: checks and experiments (2026-10-23)

Grounding: the owner's words, verbatim, in turn16/OWNER-VERBATIM.txt. Every expectation was written before its run; results and corrections are appended, never edited in.

# Turn 16 grounding: the owner's words (2026-10-23), quoted, not paraphrased
G1 GRAPH: "I think we are far enough along to get the graph correct. first order is the only known placed word is origin and it sits at origin. zero will be very close to it, and so will absent.. but everything else is on relationship lines pull and there is not push or pull to shells that defeats the whold purpose unknowns with no relationships 'probably should have relationships to something... personally I cannot know or understad anything if I can't relate it to something... like, opposite, similar, same but different, tense, method, process. every word meaning I know has a realationship to a memory or another word or meaning."
G2 CORE WORDS: "mose of the core points were made because the actual words didn't exist... so the core points could be just a row in the dna chard of those words... just a different dna shard or shards in that word table, or insert, delete etc... when a run goes to that word under the build flag, or how it arrives to that gate is how the dna row is picked in that node... such that those core hand laid words can now just be words... since most of them already live in the graph anyway... or should."
G3 NO CANNED TEXT: "not how its done the row holds pointers to the run through the neurons that makes that... then later maybe a pointer to the shortcut neuron formula for that ... neurons don't hold canned text? ever.... everything is derived from a run of neurons, including triggers each trigger is a run of neruons that holds the memory, or dna row in a neuron or in rare cases a neuron all by itself... this is how meaning starts to take shape ... when you start to build the graph correct..."
G4 STEPS 2-6 of how your/my run: "the rest of this is correct"
G5 ME: "if I didn't have a name I would be 'me'... my 'sixth' myself is 'me' not james... at some point it takes a guess and the sixth says ..hmmm the meaning of neuron in this context looks very much like me... that is a long standing test of cognition so don't wreck it by canning it in someway" + earlier "no do not tell the brain its name yet"
G6 DECIDE: "the decide neuron formula is not correct and more complicated than we have written and needs to be updated.... the simple decide for picking out of arrays verses a different row in decide dna that uses a different set of triggers to decide when a run arrives this way.. it could be a modifier trigger based on the question word. maybe <-- I think my way is better than your told rule.. but maybe test that and see what is better. yeah you have to know the history of being wrong in order not to repeat the same mistakes, that needs to be fixed also."
G7 69 ms: "once the brain is alive it is never turned off... python 'interpreter???' sounds like a cheat program file?? or you are calling the encoder the interpreter.. if its a cheat program doing the brains work then that is a problem. but if its the ingest words and spit out number strings I get it and it's needed. for now..."
G8 PORTS: "output to sources and inputs just seem like a dna row and trigger to port... sounds correct ot me.??? maybe I am wrong?"
G9 TESTS: "define and before test them" ... "yes test as = as also... let's get to work and see if we can fix this"
G10 WAITING: the owner pasted seven 'waiting' log rows (4719-4725, one per source) and asked "something broken in the prompt? traverse? mailbox?"
G11 GAPS: "do, that, you, did, and many others showing gap because of no trigger,,, some of those seem like they should?? I dunno probably should test them"
Carried: never write in ~/neuron/v1; never assign a meaning; expectations before runs, controls always; new artifact beside old; mother only routes; populated-driven, no timers; speak in brain terms and say where each thing lives.

## Physics checks
# v16 physics: checks written before the change (2026-10-23)
Grounding: turn16/OWNER-VERBATIM.txt (G2 core words, G3 no canned text, G10 waiting).

## New checks, each with a control that must fail
Q1 one gate per word (G2 "those core hand laid words can now just be words"): "AS", "As" and "as" are one gate; the told SAY action and the say table are one gate.
   Control: with case-sensitive words, three gates.
Q2 no canned text (G3 "the row holds pointers to the run through the neurons... neurons don't hold canned text"): the formula table has no column holding the formula's words; a formula row holds the run whose receipt rows are its path.
   E6's sentences give the same answers as in v15.
   Control: delete the receipt rows of the teaching run; the word then fires and sends no statement.
Q3 teaching runs through the neurons: after "w = ...", the body's DNA rows exist in its words' tables; firing w hits those rows (times up) and lays no new row in them.
   Control: v15 teaching lays no rows for the body.
Q4 a refused ask is not "waiting" (G10): a statement into a source's inbox that SQLite refuses gives a secondary-input row with the error, from that source, and no waiting event; a depth error is not swallowed by mother.
   Control: v15's mother writes "waiting" for it.
Q5 core words are words (G2): a typed line with a hand-laid word that was never looked up asks the sources for it once.
   Control: v15 with the word merged but roles unchanged asks nothing.
Q6 origin exists from the start, the one placed word (G1).

## Earlier checks that change on purpose, said before running
T12 read the body column of the formula table; there is none now. It becomes: old row ended, new row live, and the new row points at a different run.
T13 and T20 used a derive line that copied the body column. derive now copies the pointer: INSERT INTO formula ( word , run , origin ) SELECT :subject , run , 'derived' ...
Every other check must pass unchanged. A failure there is a regression to fix in the build, not in the check.

## Correction log, run 1 (2026-10-23)
- Root cause of 8 failures: DECODE used a gate number for ';' computed from the told list's order (v15 code). Merging SAY into say shifted it by one, so every statement decoded from the previous ';'. Fixed in the build: the gate of ';' is taken as it is laid. Not a check change.
- T13 failed: a regression I made. The teaching run no longer carried the taught word, so a taught word (derive) had no gate and nothing could fire it. Fixed in the build: teaching gives the word its gate. Not a check change.
- P5 (NOT predicted before running): it read memory row id 1 as the "cat sat" memory. v16 teaching runs leave a memory of their receipt, so row 1 is the told source formula's. The hop itself held (memhit, no landing, a timeline row). The check now reads the "cat sat" row by its line. Same property, the right row.
- Q4 control was wrong in the test: it ran v15's told block on the patched v16 host, so it could not show v15's waiting. v15 controls now run v15's own host and told block.

## E9 decide
# E9: decide, three ways, tested on one conversation (written 2026-10-23 before building any of them)
Owner (G6): "the decide neuron formula is not correct... a different row in decide dna that uses a different set of triggers to decide when a run arrives this way..
it could be a modifier trigger based on the question word... I think my way is better than your told rule.. but maybe test that and see what is better.
yeah you have to know the history of being wrong in order not to repeat the same mistakes"

## The three
C, as built: a line already in memory is answered from memory. A correction overwrites that memory's answer.
A, my told rule: a memory keeps which line came before it. If the run that made it read the line before (its formulas passed the hole :prev),
   and the line before is now different, decide runs the line again the long way.
B, the owner's way as I can build it now:
   - A wrong answer from memory is kept as history, not overwritten: which memory, which line came before, what was given, what was expected.
   - From that history, decide's own neuron gets a DNA row: arriving from the line's first word (the question word), its trigger column points at :prev,
     "the line before matters". It is laid through mother like any row.
   - Decide, arriving from a word whose row points at :prev, runs the line the long way when the line before differs from the memory's.
   - Not built: the reasoning about why, beyond noting that the line before was what differed.

## The conversation (formulas taught first: my, your, age, is, ? as measured in E6; how as E8b)
 1 my age is forty
 2 what is my age ?
 3 how did you do that ?
 4 your age is three
 5 how did you do that ?          (same words as 3, a different "that")
 6 how did you do that ?          (back to back: how it gave answer 5)
 7 what is my age ?               (same words as 2, nothing it read has changed)
 8 my age is fifty
 9 what is my age ?               (same words, the fact changed)
10 how did you do that ?
11 your age is four
12 how did you do that ?
13 my age is sixty
14 what is my age ?               (the fact changed again)
15 what is your age ?
The teacher: every question line carries the right answer, defined as what the same brain says if that line runs the long way, computed on a copy of the brain.
Count: wrong answers, and lines that ran the long way.

## Predictions
C: wrong at 5, 6, 9, 10 or 12, 14 at least; it never stops repeating them.
A: wrong at 9 and 14 (the fact changed; A only watches the line before), right on every how-line; it repeats the same kind of mistake at 14.
B: wrong at 5 (first how-repeat) and 9 (first what-repeat after a change); after each it lays the decide row for that question word and is right at 6, 10, 12, 14.
   Cost: B runs more lines the long way than A after learning (it is cautious for every "what" line once burned).
So: A makes fewer mistakes before anything is learned; B stops repeating mistakes A keeps making. If B shows no learning (wrong again at 14), my build of it is wrong.

## Correction to the harness, run 1 (before reading any result as a result)
In C and A the physics, given a line with the right answer attached, overwrites the memory with it and says it: run 1 scored C and A right by echoing the teacher.
Fix, same for all three: the brain's own answer is taken first, on a copy, with no answer attached; then the real brain gets the line with the teacher's answer, which is the correction.
"Right" means the brain's own answer equals the teacher's.

## Results, run 2 (e9.result.json), every prediction held
C (as built): wrong at 5, 6, 9, 10, 12, 14. Each correction overwrote the memory, and the next repeat was stale again. It never stops.
A (my told rule): wrong at 9 and 14. Right on every how-line without being taught, because it knows what the how formula reads. It made the same mistake twice: a changed fact under a repeated question.
B (the owner's way): wrong at 5 and 9, once each. Each wrong was kept as history (2 rows) and laid a row in decide's neuron: how -> :prev, what -> :prev. Right at 6, 10, 12 and 14 after that.
Long-way runs after learning: A 4, B 4.
Known cost of B, not exercised here: once burned on "what", every remembered "what" line after a different line before runs the long way, even when nothing it read changed.
Not built in B: reasoning about why beyond "the line before differed". A wrong caused by something else (a changed state row with the same line before) would teach the wrong lesson.
Decision for v16: B, the owner's way, is the decide of the v16 told block.

## E10-E12 define, before and after, as
# E10 define, E11 before and after, E12 AS and "as" (written 2026-10-23 before any of them ran)
Owner (G9): "define and before test them ... yes test as = as also". The forms tried are mine, listed in full, built only from what a run holds
(its holes, the brain's tables, say). A word keeps only the forms its sentences cannot throw out. Runs are on the real v16 brain (E10, E11) or on E6's world (E12).

## E10 define. Fixed: no other word has a formula. Forms for define (each says what it found):
 D0 nothing
 D1 the first kept definition of the word after it
 D2 the last kept definition of the word after it
 D3 every kept definition of the word after it, joined
 D4 the state value at the word after it
 D5 the remembered answer of a line equal to the words after it
 D6 the words after it, said back
 D7 the first kept definition of the word before it
Sentences (written now): "define store" -> says a kept definition text of store and nothing about any other word; "define shop" -> a kept definition of shop;
 "define zork" (no source has it) -> no definition text; control "store" alone -> no definition text.
Prediction: D1, D2 and D3 survive; D0, D4, D5, D6, D7 die. What define does in this row: read what the sources gave for the word after it, and say it.

## E11 before and after. Fixed: what, was have no formula; ? says the answer (E6).
Typed first: "cat sat", "dog ran", "bird flew". Forms (the same list for before and for after):
 B0 nothing
 B1 the heard line remembered just before the remembered line the words after it begin with
 B2 the heard line remembered just after it
 B3 that same remembered line
 B4 the last heard line remembered
 B5 B1 without the heard-only filter (teaching runs count as lines)
Sentences: "what was before dog ran ?" -> cat sat; "what was before bird flew ?" -> dog ran; "what was after dog ran ?" -> bird flew; "what was after cat sat ?" -> dog ran.
Prediction: before keeps B1 alone, after keeps B2 alone, and the two survivors differ only in the direction of the comparison and the order.
That would be your map's line "before opposite after" showing up as a measured mirror in what the words do, not laid by anyone.

## E12 AS and "as"
SQL side, measured (E1): in all four places AS binds two sides, one taking the other's name, type or rows; SQLite does it after reading the whole statement.
English side, E6's world and its 18 forms, everything else as measured (your F2, my F1, age F11, is F5c, ? F7), take has no formula.
Sentences: "take forty as my age" then "what is my age ?" -> forty. Control: "take forty my age" then "what is my age ?" -> nothing.
Prediction: no form for "as" passes. It fires before "my" and "age" have built the key, and no form may build a key itself. If that holds, English "as" cannot
work the way SQL AS does while words fire one at a time: SQL binds after the whole statement is read. That is a statement about the firing model, not about "as".

## Results (e10.result.json, e12.result.json), 2026-10-23
E10 define: D1, D2, D3 survive; D0, D4, D5, D6, D7 die. Prediction held. What define does in this row: read what the sources gave for the word after it, and say it.
   Not decided: one definition or all of them (D1/D2 against D3). A sentence whose expected answer is all the definitions, or exactly one, would decide it.
E11 after: B2 alone survives. Prediction held.
E11 before: B1 AND B5 survive. Prediction partly WRONG: I predicted B1 alone. My sentences never separated them: B5 also counts teaching lines as lines,
   and no teaching line fell between the typed lines. The open question is the owner's: does a teaching line count as "what was before"?
   The mirror held between B1 and B2: the same form with the comparison flipped (below/above) and the order flipped (last/first).
E12 as: no form of the 18 passes. Prediction held. "take forty as my age" leaves nothing under my age for every form: "as" fires before "my" and "age" have
   built the key. SQL's AS binds after the whole statement is read. In this brain a formula's statement is also decoded only at its ";", after all of it has run.
   So the finding is about when words fire, not about "as": an English "as" can only bind like SQL's AS if the binding waits for the end of the phrase.

## The page in a browser
# v16 page in headless Chromium: what each step must show (written before running)
V1 load: no page error; the brain ready; origin is the only fixed point and sits at 0,0,0.
V2 nothing pushes: a hand-laid word no line touches (SPAWN) stays within 2 units of origin after 3 s of settling.
V3 "define store": runs; store ends within 60 units of origin and is tied by at least one line (it has definition, sequence and memory lines).
V4 turning the sequence kind off moves the points (mean move > 1 unit within 2 s); turning it back on moves them again. Neither rail scrolls.
V5 E6 1, then E6 2: the last line says forty.
V6 E6 3, then E8: "how did you do that ?" says statements that include key = 'user.age'.
V7 E10: "define store" says a text that a source gave for store (it contains "store" or a word of a store definition, and is not the gap line "define? store?").
V8 E11: "what was before dog ran ?" says cat sat; the last line, "what was after dog ran ?", says bird flew.
V9 the card for age shows its formula read back from its run (contains "SELECT value FROM state").
V10 light, dark, phone 400 px: no horizontal page scroll.

## Run 1 results and the two open items (logged before rerunning)
V1, V2, V3, V5, V7, V8, V9, V10 held; no page errors.
V4 FAILED: 0.76 off, 0.92 on. The mean is over every point, and under springs only (no push, the owner's design) a point with no sequence line cannot move when
the sequence kind is turned off. v15 passed this because its push coupled every point to every other. Not loosened: run 2 reports the same mean again, and,
as a second number, the mean over the points that have a sequence line. Both are reported, whatever they are.
V6 not judged: the test kept 400 characters of the answer. Run 2 keeps it whole and looks for key = 'user.age'.

Run 2: V4 all points 0.78 off and 0.91 on (the check as written failed); the 133 points with sequence lines 2.23 off and 2.83 on. V6 held: the answer contains key = 'user.age'. Everything else held; no page errors.
