# Point Of Connection 14: checks and experiments, 2026-10-22

Written before the build, from the owner's words in GROUNDING below. Every correction to a check is logged with its reason. Result at publish: 48 passed, 0 failed (38 checks, 10 controls).

## The checks

# v14 checks, written BEFORE the build. Each cites the owner's words in ../turn14/GROUNDING.md.
# A failing check is understood and the build fixed; a check is never edited to pass.

T1  (O16, P3) A formula holds SQL words. When the run reaches ";", the gates it passed decode to the statement, holes filled, and that text
    leaves through "output to sources"; mother runs exactly that text on real SQLite; the reply comes back through "secondary input"
    as a sub-input of the SAME run; it fills a cell named by the statement. who = SELECT value FROM state WHERE key = :object ; say :found
    then "who are you ? => a brain" then "who is you ?" says "a brain".
T2  (O16) No primitive run is code: the engine has no find/read/compare/join/write operations and no SQL statement written in JavaScript
    outside the told physics schema, the stand-in satellites, and mother's own pickup. Without a taught "who", "who is you ?" sends no statement.
T3  (O6) A fresh brain asks NO source: "define store" -> zero mother routes, zero mailbox events; a gap says no formula says where to look.
T4  (O6) After "source = INSERT INTO wn.inbox ( word ) VALUES ( :subject ) ;" -> "define store" asks wn only (one ask per new word), never gcide, mw, mwt, moby, map, sqldoc.
T5  (P2) Populated-driven: the satellite's own trigger does the work when the ask lands; its outbox trigger tells mother it is populated;
    mother picks up and empties the outbox. Event order: output to sources, mother, satellite work, populated, pickup, secondary input.
    No setTimeout or setInterval anywhere in the engine. Outbox row count after pickup = 0.
T6  (O3) Every secondary input is checked with three questions, each answered with a reason: asked for? needed? asked wrong?
    Real case "as": Webster 1913 sends "So" first -> not what I asked; Merriam-Webster sends As:1, As:2, AS, as- -> not what I asked;
    their rows are set aside, the "as" rows kept.
T7  (O3) An empty reply: needed = no; asked wrong = the question is asked; a gap names it.
T8  (O3, owner: "steps back to the decision that picked this path and takes a different row") When a formula's ask fails the check, the run
    steps back to the neuron that fired it and takes another row of that neuron whose trigger names a different formula, if one exists.
    who = state ask; what = memory ask; "who are -> what" lays a second row in who; "sky is blue => blue"; "who is sky ?" -> state has no
    sky -> step back -> the row pointing at what -> memory -> says "blue".
T9  (O4) A line answered from memory is part of the word's meaning: meaningOf counts it as a recalled context (memory id, times), measured
    as the run that made that memory plus the recall. Nothing is dropped.
T10 (O1) AS: the SQLite docs satellite holds what AS does (CREATE TABLE AS, CAST, WITH). In the brain, measured against E1:
    (a) BUILD SELECT 'a brain' AS who ; BUILD against the same line without AS: same column name, same row (E1b: SQLite reads the name by position);
    (b) BUILD SELECT CAST ( '7' AS INTEGER ) ; BUILD against the line without AS: with AS the reply is 7; without it, a syntax error.
    The meaning record carries the columns and the outputs, with and without.
    CORRECTION LOG: T10 as first written expected (a) to change the column name. That contradicted E1b, measured earlier in this turn. The test
    was wrong, not the build: corrected before the engine existed, to the measured fact.
T11 (P7, O6) Relation lines come only from the brain's runs: no relation before "like" has a formula; after
    like = INSERT INTO relation ( a , rel , b ) VALUES ( :subject , :head , :object ) ; and a source formula that includes map,
    "define store" writes relations through mother, and the relation table's own trigger draws them.
T12 (owner: truth shift = new row, old ended) Teaching writes a row in the formula table; teaching the same word again ends the old row and adds a new one.
T13 derive in SQL copies a related word's formula to a word that has none, marked derived (a guess); born fires derive.
T14 (O13-O15) Layout: satellites at the far edge on mother's side; mother between them and the brain; output to sources and secondary input
    on mother's side; output to use, primary input and encoder on the opposite side.
T15 (O18) Relation lines are visible: your map's lines drawn at opacity >= 0.3 by kind; the brain's own lines brighter.
T16 (O19) Two sidebars: left = graph modifiers; right = prompt, steps, run details. Touching a toggle, a slider, or typing a line does not move either sidebar.
T17 The page declares utf-8, so a copy opened from Downloads shows no garbled characters.
T18 (O20) v13.1 is untouched: its file hash stays c40426ec55df96af, its artifact and Downloads copies are not republished.

CORRECTION LOG, T6 (run 1): the check 'the as rows are kept' read every kept row, but the line "define as" births two words and both are asked, so define's rows are rightly kept too. The test now reads the as ask only. The build's behaviour was right; the test read too wide.
RUN 1 FAILURES THAT WERE THE BUILD: T2 (the memory neuron's read sat outside the physics block: moved, test unchanged); T11 (a word born inside a definition row was never looked up when a typed line later needed it: restored from v13's rule); OOM (replays never closed their databases: closed now; and the growable-memory SQLite build is used).

# Negative controls, written after run 2 passed and before any change for them. Each removes the thing a passing check credits; the check's effect must vanish.
T19 (control for T8) Without the row "who are -> what", "who is sky ?" does NOT say "blue"; a gap says who has no other row to take.
T20 (control for T13) Without the relation row wb like wa, derive copies nothing: wb has no formula row.
T21 (control for T1) Teach who with a different statement: the text that leaves through output to sources changes with the row. The text comes from the row, not from code.
T22 (control for T4) A source formula naming two satellites asks exactly those two for each new word.
T23 (control for T5, P2) A satellite that never signals populated: mother picks nothing up, the run does NOT treat the ask as answered; the cell stays open and the check says nothing came back. No timer fills it.
T24 (control for T9) A word that is not in a recalled line gets no recalled context.
T25 (owner, 10-21: a memory written with gaps must not hide them) "define store" on a fresh brain writes a memory with the gap "where to look". After source gets a formula, "define store" runs again the long way (decide says why) and asks the source.
T26 (control for T25) Without teaching source, the second "define store" is a memory hop.

## Experiment E1: AS

# E1, AS. Predictions written before running.
Hypothesis (owner O1): AS has a meaning, an action, not a syntax mark.
E1a: the SQLite docs hold at least one sentence saying what AS does (CREATE TABLE ... AS SELECT, CAST(expr AS type), WITH name AS, column alias). Last turn's claim "AS appears only in the syntax" would then be wrong.
E1b: remove AS and measure, per context:
  - column alias `SELECT value AS who FROM state`: prediction: SQLite also accepts `SELECT value who` (implicit alias). If so, AS changes nothing measurable there.
  - `CAST('7' AS INTEGER)`: prediction: without AS, syntax error.
  - `CREATE TABLE t2 AS SELECT ...`: prediction: without AS, syntax error.
  - `WITH q AS (SELECT ...)`: prediction: without AS, syntax error.
E1c: AS against no AS at all: `SELECT value FROM state` vs `SELECT value AS who FROM state`: prediction: same rows, column name changes from value to who.
A failure of any prediction is reported as a failure, not re-worded.

Result: every prediction held. Doc sentences:
- A "CREATE TABLE ... AS SELECT" statement creates and populates a database table based on the results of a SELECT statement. (sqlite.org/lang_createtable.html)
- A CAST expression of the form "CAST( expr AS type-name )" is used to convert the value of expr to a different storage class specified by type-name . (sqlite.org/lang_expr.html)
- A SELECT statement is recursive if its FROM clause contains exactly one reference to the CTE table (the table named on the left-hand side of the AS clause). (sqlite.org/lang_with.html)

## Experiments E2 and E3: the router

# E2 and E3, the router. Predictions written before running.
E3a: a trigger stored in the main brain cannot name a table in another (attached) database. Prediction: CREATE TRIGGER fails. If so, the brain cannot reach a satellite itself, and the traverse is exactly what mother is for (P1).
E3b: a trigger stored in a satellite fires when the main connection writes into the satellite's inbox. Prediction: yes, it fires at once, in the same statement. That is populated-driven, no timer (P2): the satellite does its own work the moment its mailbox is written.
E3c: a TEMP trigger CAN name an attached table. Prediction: yes (SQLite allows it). Honest note either way, because it is a second route that is not mother.
E2a speed, in one process: mother writes the ask into the satellite inbox, the satellite's trigger fills its outbox, mother reads the outbox. Prediction: well under 1 ms per round trip.
E2b speed, satellite as its own process (a daemon holding its database open), reached over a local socket. Prediction: about 0.05 to 0.5 ms per round trip.
E2c speed, a fresh process per ask (the "ssh or launch each time" way). Prediction: tens of ms per ask, 100x or more slower than E2b. ssh to hp or hp2 is NOT run: those machines are the owner's.
Run 1 stalled (stopped after 120 s): the outbox was never emptied and had no index, so each pickup scanned every earlier reply. Lesson kept: mother's pickup must empty the mailbox it picked up from. Run 2 below empties on pickup; predictions unchanged.

Result:

```
{
 "E3a": "refused: qualified table names are not allowed on INSERT, UPDATE, and DELETE statements within triggers",
 "E3b_rows_in_outbox_at_once": 2,
 "E3c": "refused: qualified table names are not allowed on INSERT, UPDATE, and DELETE statements within triggers",
 "E2a_ms_per_round_trip": 0.0109,
 "E2b_ms_per_round_trip": 0.2165,
 "E2c_ms_per_ask": 69.07,
 "E2c_over_E2b": 319
}
```

E3c prediction failed: a TEMP trigger is refused too. mother is the only way out of a brain.

## Grounding: the owner's words this turn

# Grounding for this turn: the owner's words, verbatim. Every check below cites one of these.

O1 AS: "so the meaning of As is a syntax symbol like ( or ) ; or somehting else? as has a meaning it would not be a code word symbol that is used if it did not a meaning, we humans would just not use it because it would be an ineffiecient use of our energy"
O2 WORDS AS CODE: "a word is a symbol the is entered into a compiler that transforms that word into the code or action of that word to the brain or its aux systems ... in this case we are specifically looking at brain function so motor skills, audible and visual or not of the concern"
O3 CHECK ON RETURNS: "I suppose this works if the brain knows its there, and can work the data after it returns... it seems to lack a system of check though,,, if it's direct placed fine, but what says ? if this the data I asked for? is this the data I asked for but is it the data I needed, did i ask wrong?"
O4 MEMORY IN MEANING: "2. must be fixed correctly" (item 2 = the meaning measure dropping lines answered from memory; owner earlier: "if I ask myself 'do I know the meaning of the word lay' that is a memory check? or state check?")
O5 ROUTER QUESTION: "I still think the mailbox system and router just make sense to me,,, do you think it will just be too slow... or there is a better way that we should do this? there are many ways to skin this cat with daemons, and many other things, thoughts on this."
O6 BRAIN DECIDES SOURCES: "the JavaScript still decides to ask every source.<--- that is wrong, the brains decide run should do this... based on its formula of runs behind it"
O7 SLICE: "again if fixed slice is the more true solution,, I don't know the answer there... ??? if the published artifact is part of a brain db, then the brains ablity to call is what is used to call out"
O8 SATELLITES: "the main brain is the cognition / reasoning / problem solving / state / history / time ... the satelite source brains have much of this, but are more forcused on the data, and the reasoning is more about understanding the ask and provided the correct sourced data from the corpus, where the main brain is primary about reasoning, understanding the scope of the primary input, asking the correct questions of itself and its aux sources to accumulate the correct amount of context to supply its scope of reasoning table with the correct varibles such that an output can be formed"
O9 OTHER BRAINS + SIXTH: "yet other brains can be more focused on testing, guessing or creating hypothosis or dreaming, observing (thinking the sixth here ... an observer that sparks questions and asks to the guessing brain ... does this meaning actually make sense? and based on the results the sixth then could make adjustments to the brain sql from outside the brain ... its basically the soul or the observer .. likely where the morals, ethics, checksums live that keep the brain honest, truthful, and of good moral and etheical character, along with the processes that inspire or drive growth, more effiecent processes, new finding of formulas"
O10 FINISH 5 AND 6: "5 and 6 need to be finished properly" (5 = Markdown copy of the hand-out in Downloads; 6 = the owner's review of the page, given in this message)
O11 MEANING: "we really really need to address the meaning situation,,,, what I see is a bunch of words that we don't know the meanings of because we have no clue what the meanings of the simple words are, or how to make a math expressions or a code word script of those words to mean other words, then use those new words plus a mix of the primes words or root words to give meanings to the more complex words and their modifiers, and then such using sentances of those now complex word ... to make expressions that have a meaning"
O12 COMPILER: "in terms of code you have root code 'think bios or binary' then you have the short hand code think grep to it's binary action, mixed with syntax operators and modifiers that all meet at a compiler to give the many different symbols their action to the graph or the silicon or sources or memories or state or belief or reasoning or understanding or balance or inequality .... or a ratio or mixture of all of them"
O13 LAYOUT SOURCES: "the mwt , mw , gcide, wn, sqldoc, map, moby node locations should be on the opposite side of the graph such that the traverse lines are brain to mother to sources back to mother back to brain, the visual of the mother speaking through the brain just looks off"
O14 LAYOUT OUTPUTS: "likewise output to use and output to sources... other brains , dbs , etc should be on the edge.. out put to source should be on the same side as the mother, and output to use the opposite side of the brain"
O15 LAYOUT INPUTS: "you should also have visually the encoder and the primary input to the brain better visually represented, and the secondary input back from the mother or the base or what ever it's called on that same side as the mother"
O16 NO CONTROLLER: "there is no walker, there is no or code controling anything outside a very very small traversal and routing program, mailbox system ---- everything else is controlled by the neurons and their runs.... and the output of those runs to give inputs to other db's or it's own db"
O17 METHOD: "before you start a task built the check of what that task should result in... then build the task, then check it,,, if it fails do not just adjust the test so it will pass.... understand why it failed... your grounding is in my words, not yours"
O18 RELATION LINES: "from what I see none of the relationship lines show up at all"
O19 SIDEBAR: "everytime you touch the slider or turn them on or off that sidebar jumps to the bottom.. so maybe that side bar should be split into a sidebar on the left of screen with the modifiers lines of the graph and the promt actions run details stuff on the right."

# Earlier owner words that still bind (from this session)
P1 MOTHER: "remember the mother does 'no' work other than the traverse... the brain cannot change the mother, so at this point the mother only does what the brain cannot do, which is traverse to and traverse back outside its db"
P2 POPULATED: "it's important that its not timer driven its populated driven,, its basically the mother is the router, and each other brain has a mailbox for output that the mother listens to and pickups from when it's populated and returns the information back to the main brain as a piece of the problem solving table 'cell' <--- the mother doesn't decide this,, the brain does"
P3 SUB-INPUT: "a mother that just takes the output and writes it to the sql prompt then returns the output as a sub input to the brain so the brain knows that input is not a new run its an information return from the run that it's working on already"
P4 CELLS: "if you think of the context table as a runs table of cells it needs populated in order to fill the varibles of the huge equations ... once that varible table is full then the substitution formula can plug in all the vairbles into the runs formula and then that formula can be run"
P5 SQL WORDS: "yes the sql words are hand laid and don't need a dictionary look up, but instead need a sql doc look up.... that is the source for code often is the code docs themselves"
P6 PULL: "the pull of relationships was a ratio based on the numbers of realationships pulling in a certain direction in the graph, the value of the trust of that relationship, and the closness of the meanings ... strong defined relationships like opposite, synomomn, antonomyn, class ... pull stronger, than relationships to topic, context, catogory, method, process use, before and after"
P7 NO ASSIGN: "you can never pick a word arbitrary and say This - means this or that... it's all deduced or derived from root"
P8 GRAPH SEES ITS RELATIONS: "these should be able to be turned on or off individually such that the brain can see it's relationships to other meanings , memories, state, history, long term memory, active memory , persistant memory"
O20 KEEP BOTH: "do not just over write the model I have also. create a new one , such that I can compare and diff the two on my own."
  -> v13.1 stays untouched: artifact https://claude.ai/artifact/F2G46EYz84HMbzUY6Zkt4C, file d2/point-of-connection-v12.html, Downloads NEURON-POINT-OF-CONNECTION-v13-2026-10-22.html and NEURON-POINT-OF-CONNECTION-2026-10-21.html. All new work lives in scratchpad v14/, publishes as a NEW artifact, and copies to Downloads under a NEW name.
