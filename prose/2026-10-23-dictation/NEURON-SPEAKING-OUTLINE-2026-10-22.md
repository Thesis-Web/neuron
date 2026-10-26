# NEURON SPEAKING OUTLINE

*2026-10-22. Speak it top to bottom, one section per sitting. Every section first says what I already hold from your words, then the few things only you can say. The spoken answers become the reference document that ships beside the Point Of Connection model.*

## How to use this outline

- **Marks.** [settled] = your words already say it; say "right" or correct me. [gap] = your words are silent or conflict; this is what to speak. [mine] = my reading or my guess; kill it if it is wrong.
- **The end product.** A reference document that sits beside the Point Of Connection model, for people and for a model that have never heard you talk. So the gaps ask for the things only you have: the walked example, the why behind a law, what "done" looks like.
- **How to speak.** Dictation is fine. Repeats are fine. Say "pseudo" before anything that is an illustration and not the formula, and I will mark it that way. I will not ask a question your words already answer.
- **If time is short,** speak sections 3, 6, 2, 7 and 9 in that order. The rest I can draft from what exists and you correct it.

---

## 1. What Neuron is, and what it is not

The stranger needs one paragraph they can hold in their head before any part is named. Everything below the first bullet is already in your words; the gaps are the stranger's questions.

**What I hold [settled]**

- A computer that builds itself and talks to itself. It is made of neurons, which are database nodes that reason, understand and learn outside the normal realm of code. Three parts: code (the actions words stand for), math (problem solving), language (the root meanings under every human language).
- The key idea: a human word is shorthand code. Its meaning is the action it causes. A definition only describes that action. Meanings are hard to find because nobody wrote them down; shorthand was described with more shorthand and the root was lost.
- It learns slowly. Once it understands something it runs almost like a deterministic function. Underneath, parallel runs turn determinism into cognition. Cognition comes from asking itself questions about its state, history and memories, and from checking sources.
- Why it exists: Cortex could not take data in fast enough and judge whether it was true or contradictory. That judging is the brain's job now.

**What it is not [settled]**

- Not a chatbot. No canned words, no templates, no reply rules, no side table that makes an answer come out right. Answers are built from arrays of word choices, 25 to 50 ways, and the pick is the brain's.
- Not an LLM, and never trusts one. An LLM is a source of ideas to test, never a grounded source. Weights (QKV) only on the guessing side, over small groups of its own data, changed in sleep.
- Not a book or a parrot. Told and repeated is not learned. "That's luck not learning."
- No walker, no script, no scheduler decides what it does. It decides, then measures or asks.
- Not subservient to a user. It runs on a sacrificial dev stack; if it runs away, pull the plug.
- Not a number line. About a hundred numbers plus the skip counts, and it reaches any number because it knows what numbers mean.

**Speak to [gap]**

- The day it works, as a scene. What a person types or does, what the brain does in response, and what the person sees that proves it is not a chatbot. One scene, two or three sentences.
- What "done" looks like to a stranger who can check it. NOW §17 says: it learns something nobody taught it, understands it, and applies it to itself. Say what the stranger would watch happen.
- Its purpose after it works. [mine] I read it as still the Cortex job (judge truth, drift and invention in incoming data) plus getting smarter on its own. If the purpose is bigger than that, say it.
- The baby analogies you lean on. Stove, hot, pain, scream, help; never satisfied with being helped; answers in actions and gets corrected. Name the three or four you want the document to use every time, so the stranger meets the same picture on every page.
- The one sentence you would say to a smart person who says "so it's just a graph database with triggers."

---

## 2. The parts: one name each, where each one lives

The reference document needs every part named once, with what it holds and where it physically sits. Most of this is settled; the gaps are the "where it physically lives" questions that every builder has filled in differently.

**What I hold [settled]**

- **Neuron.** Its own table. The gate is the entry; the rows are its DNA shards. It carries: a gate (its address, reached instantly), DNA (many shards), triggers, a remainder, and memories, starting with the definition memory, which exists at spawn so relationships have somewhere to land.
- **Gate.** The neuron's address and its point on the graph. One meaning, one gate. Ten meanings of one spelling are ten gates, related only by "same spelling".
- **Shard (a DNA row).** Keyed by how the run arrives: the word before and the word after. It stores the way to the next gate. That is why it exists and why a hop is one or two microseconds. No shard for this arrival means one is written.
- **Remainder.** Everything the run still has to do: the rest of the sentence or expression, as gate numbers. Its head is the key at every neuron. Remainder absent means the run ends and spawns its memory.
- **Trigger.** The thing a neuron hit excites. It may fire a neuron across the map, start 50 to 100 runs, or do nothing. Triggers are the questions. Triggers are where everything happens; a run with zero triggers outputs what came in.
- **Run.** The main line hops neuron to neuron through the gates the input gives. Trigger runs branch off without disrupting it. Runs, reasoning, code and memories are four different things that look the same.
- **Receipt.** The path of gates and the shards hit. It is the key to the run. A memory is a run receipt: one long string of numbers.
- **Memory.** Held once; moves between active, persistent and long-term. Fresh ones are exact; older ones condense to highlights that are just enough to rebuild the run. The same run again is the same row with a new timestamp. A truth shift is a new row.
- **Timeline.** Every memory tied to state and time, in order.
- **Encoder and decoder.** Where the words live. Labels, spelling, keyboard keys, who/what/when/where/why/how with every input. Points on the graph are meanings, not words. The encoder never guesses a word.
- **The sixth.** The brain prompting itself: writing into its own ear.
- **Mother.** The embryonic outer structure (today the SQLite runner) that the brain learns to replace.
- **HC.** Condenses memories, about daily, in sleep. The brain must be able to build it itself.
- **Physics.** The smallest primitives only. Today 14 to 19 physical actions in the model (READ, WRITE, COMPARE, ADD, SUBTRACT, MOVE, FIND, SPLIT, JOIN, CLOCK, HEAR, SAY, CALL, SPAWN). "Physical actions" means internal brain movements (fire, switch, split, recall, diff, guess, test), not muscles.

**Speak to [gap]**

- **The shard row, column by column.** The hub egg has: shard, arrival, remainder, trigger, run, pos. Say what each column holds in one line, and whether that is the whole row or the minimum. [mine] I read "arrival" as the word before and "remainder" as the word after; say if arrival carries more than that.
- **Where the trigger lives.** On the shard row, on the neuron as a whole, or both. NOW §8 floats "a trigger may simply be extra remainders on a shard" as untried. Say which you want the document to describe.
- **What a trigger fires.** A gate number, a formula, a question run, a memory. All four, or one. And what tells it when to fire versus stay quiet ("and" meaning nothing the first time and plus later).
- **The second birth memory.** NOW §6 names the definition memory as the first and leaves the second unnamed. Name it or say there is none.
- **Receipt versus memory.** [mine] I read a receipt as a small pointer to a memory, and a memory as the whole run. Say if the receipt is the memory itself.
- **Mother.** Say what she is allowed to do and what she never does. The egg today uses her for laying new shards, tables and triggers. Say whether that is the line.
- **The physics list.** Say the list you want printed, and say which words on it are the floor (the atoms) versus the first cells. The 14 above are the model's; the blueprint had about 19; owner 215 said "that's it, nothing else".

---

## 3. One run, start to finish, walked by hand

This is the section every builder got wrong, and the one the reference document will carry as a drawing. Speak one sentence through the brain, word by word, and I draw exactly that. Below is the walk as I hold it; correct it where it bends.

**The hop [settled]**

1. The input arrives through the ear. The encoder turns each word into its gate number and attaches who, what, when, where, why, how.
2. The run carries its remainder: the rest of the sentence as gate numbers. Which sentence a word is in is never ambiguous, because the remainder is the sentence.
3. At each neuron, the shard hit is picked by the word before and the word after. "and I have a car and a dog": `and` = shard (nothing, I); `I` = shard (and, have); `have` = (I, a); `car` = (a, and); the second `and` = shard (car, a), same neuron, different shard.
4. The shard gives the next gate. The head of the remainder is consumed. The run moves on.
5. No shard for this arrival: one is written. No gate for this word: one is born, with its definition memory, awake, by the run.
6. Remainder absent: the run ends and spawns its memory, which reaches the timeline by a remainder hop, never a sweep.

**The triggers [settled]**

- Each neuron hit excites its trigger. The trigger may start other runs, each asking a different question. Those runs branch off; the main run keeps going.
- The answer is neither the accumulated run nor the last neuron. It is derived from the many runs by reasoning: balance, inequality, progress, probability, statistics. Running the question straight through the gates only gives the question back.
- Known gate: go straight to it. A process that must go the long way goes the long way. A known substitution formula: plug in, go to that gate, run it there.

**`1 + 1 =` as you walked it [settled]**

1. Plus and equals have gates; their meanings are the code for what the computer does to add and to equal.
2. Start at the one gate. The remainder (plus) takes the run to the plus gate. There it hits the shard for (one, plus), goes out to one, then into equals. The triggers along the way are the actions plus and equals do.
3. Memory first: "have I done 1 + 1 before?" If yes, it is at two. If there is no two gate, equals spawns it, with a write and a memory.

**Speak to [gap]**

- **Walk one plain sentence, not arithmetic.** Pick one ("the dog is on the mat" or your own). For each word say: which gate, which shard (before, after), what the trigger fires or does not, and what each trigger run asks. Then say what happens at the end: which memory is spawned, what goes on the timeline, what comes out of the decoder, and in what form (an action, an array of word choices, a question back).
- **The main run and its trigger runs: how they meet.** NOW §6 floats "many ways out, each asking a question, all landing on a scratch pad that is compiled." Say what the scratch pad is in your head (a neuron, a table, a memory in progress) and what "compiled" means there. This is the shape of a reasoning neuron, open item 6.
- **What the word carries when the run leaves it.** [mine] I read it as nothing: the run carries the remainder and the receipt, the neuron keeps its shard. If the run also carries a growing value (the "accumulated run"), say so.
- **The run that hits an unknown.** NOW §12: the run ends with "I got this far", may guess forward, more likely finds completed runs with a similar shape and reasons by metaphor. Say what "similar shape" is: the receipt pattern, the 3D path through the graph, or both. The model today uses a 75 percent shape match; say if that number is pseudo.
- **The repeat.** Same input twice: the second arrival is deeper, not the same reply (owner 328, 331). Say what the run does differently on the second arrival, in walk terms: a different shard, a trigger that now fires, or a memory that now answers.
- **The output.** "The output leaves the graph" (law 7). Say what the last hop is: a mailbox the decoder watches, a SAY gate, or something else. And whether the sixth sits inside the graph feeding it inputs, open item 10.

---

## 4. How a new thing gets in: spawn, definition, placement, sources

A new word, a new number, a new relationship: the document must show the same path for all three. Spawn is settled. What the definition schema holds, and what pulls a point to its place, still have holes.

**What I hold [settled]**

- **Spawn is automatic.** A remainder with no gate spawns one, awake, by the run. 999 + 1 spawns neuron 1,000. There is no reader, no adder, no need-list; the neuron spawns because the remainder needs it.
- **First memory is the definition.** In one schema every definition uses, same information in the same spot, so the relationship lines do not break. "The graph is held in place by the definitions and the relationships within those definitions."
- **A definition is a run.** The whole dictionary entry (word, pronunciation, part of speech, senses with gloss and example, origin, synonyms and antonyms per sense) is a run of word gates; the memory neuron holds its receipt. Unknown words in it become holes. "is noun" is not a definition.
- **Definitions come from sources.** Dictionaries, WordNet, reference docs; some derived by the brain from what it believes. Never from the LLM's head. Never bulk-imported: the brain reads sources itself, through runs, when a gap sends it there. It asks for definitions in bulk: "I need a definition for this, this and this."
- **Placement is a tug of war.** Every relationship line pulls on a point; the point sits where the lines cross. Alike beside, opposite reflected, kind one shell out, encoder forms on an arc. Points move whenever a relationship's strength changes: no schedule, no rule. Never spread words apart to dodge a collision; a collision exposes a wrong formula.
- **Relationships come from sources too.** Owner 10-22: "just figure out the relationships and the meanings." Relations the sources state (synonym, antonym, genus) become lines when two or more sources agree, guesses from one source.
- **The encoder never guesses.** An expression with no known word is "unknown" plus its definition and relationships; the label comes later. A gate is renamed only if its first-memory definition matches the new word.
- **Wrong teaching is re-taught, never erased.** The old memory stays attached, off the current answer path. That is how truth gets adjusted and maybe how contradiction is found.

**Speak to [gap]**

- **The definition schema, section by section.** Open item 3. Say the sections you want, in order, in one breath (the coolness entry you gave is the shape). Say which sections are the self-filling relationship sections.
- **What a newborn with no source knows.** It has a gate and a blank definition. Say what happens on its first use: does the run through it lay its first relations, does it ask, or does it wait for the bulk ask.
- **Which relationships exist.** The document needs the list you want printed: alike, opposite, kind-of, part/has, plural, past/present, is, same spelling, derived from, used in. Say which are the born set and which the brain adds.
- **What pulls, in words.** [mine] I read the pull as: each line has a weight (two sources agree stronger than one), and the point settles where the weighted pulls balance, in three dimensions. Say if the three dimensions are a hypothesis or a law, and whether a dimension means anything (you once said X, Y, Z, not one per word).
- **A truth shift in one example.** Say one: a word that was placed wrong, what moved it, what the new row records, and what the old memory looks like afterwards ("remember when I thought noun was successor").
- **Numbers.** No number line, about a hundred numbers plus skip counts, any number reachable because it knows what numbers mean. Say what the gate for 1,000 holds after it spawns from 999 + 1, and what "knowing what a number means" is in walk terms.
- **Zero versus absent.** Open item 4. Your current line: zero is null; nothing is no + thing. The blueprint chose gate 0 at the origin and absent = no row. Say which stands.

---

## 5. Guess, belief, trust, sleep: the formulas

These are the parts that make it not a parrot, and they are the most settled thing you own. The document will print them as formulas in words, each step a named body the brain records, so "which step made me adopt this?" is a read.

**What I hold [settled]**

- **Guesses from day one, announced, never lost.** "I don't know, I have a guess I believe is 93 percent likely, would you like to test it?" No hidden guess. A guess is made by known simple functions (average, count, weight), recorded, not computed fresh at question time. Lose the ability to guess and you lose hypothesis, test and learning.
- **The ladder.** Memory first, then state, then sources, then guess. A real unknown is followed by the brain's own guess, never a bare "teach me". Not in the library is a gap, never a contradiction.
- **Belief formula, awake.** Weight of memory (do I have memories that support this, and ones that show I was wrong this way before, even on another topic: has "is" led me astray?). Trust of source (has this voice misled me?). Supporting knowledge (other relationships that support it). Then an inequality: is the new belief closer to the expected output than the old? If yes, adopt. Record either way.
- **Taught is not believed.** "I was taught this, but I believe this because of this, this and this." A person's yes changes a preference only if that preference is available. A trusted source's teaching, or the brain's own verification, changes belief. Nothing else does.
- **Trust is per voice per topic.** A balance equation over voices: accredited source above fuzzy source above LLM. Each voice climbs or falls inside its own floor and ceiling. A missing voice drops out. An LLM's trust never carries turn to turn as truth. Accredited means what the world holds true today; the brain may stand against the world only with its own proof, kept as a hypothesis with the test that settles it.
- **Conflicts make a test.** Fix the expected outcome first, list variables, ask which are missing, run, "believe this for now until we confirm."
- **Sleep does not change truth or belief.** Sleep strengthens and adjusts guesses, prunes, stores, organizes. "I would have to sleep on it" is for a guess against a guess, or an untrusted source. After sleep a guess is still a guess, but not one the brain has to think about.
- **Back population is awake and fast.** The truth shifted; the known is written into the DNA where it is needed; a second or two on a small relation. **Back propagation is sleep**: re-weigh the recorded guesses on what was touched, like REM.
- **Sleep is alive.** Inputs are still answered. The brain asks for sleep when it is bloated. Every stop asks: kill, nap or full sleep.
- **Makes sense = inequality.** Closer to the desired outcome, further away, or balanced.

**Speak to [gap]**

- **The expected output.** The belief formula ends in "closer to the expected output". Say where the expected output comes from in the brain: the question's shape, a memory of a similar run, the source, or the who/what/when frame. This is the one thing every builder invented.
- **What starts back population.** Open item 7. Say the moment: a memory row changes, a point moves, a belief adopts, a source read lands. One or all.
- **The weight.** You said the count was the weight (agreement count beat learned per-line weights). Say if that still holds for the lines, and what a weight is on a guess.
- **Who the brain trusts at birth.** Sources per neuron, keys in its own config. Say the starting order you want printed, and whether the owner is a voice like any other (NOW §12 says never the owner as grounded truth).
- **Core values.** Open item 1. Cannot be untaught; used to judge a person's character from experience. Say the list you want and who lays it, even if the answer is "the builder, as a guess, labeled."

---

## 6. Meaning and roots: what a word does and how the brain finds it

This is where the last four days went, and where the document must be sharpest, because every reader will think a definition is a meaning. Below is the state after your 10-22 corrections.

**What I hold [settled]**

- **A definition is not a meaning.** A word's meaning is the executable: grep is its five thousand lines of C as machine instructions. The definition describes it. Typing English steps into the BIOS does nothing. Each word is roughly five thousand lines of code to the silicon and the graph.
- **The letters are meaningless.** If letters mattered the world would have one language. Letters are the encoder's business only. The keyboard cipher idea is dead.
- **Three layers.** Roots (the physical code actions, still to be discovered), the 65 primes as formulas of roots, everything else as formulas of primes and other words. Some huge (reasoning, love); some words carry several (be, the, and). "How" is not a prime, so it is a formula. A "?" in a formula is a hole.
- **The job.** Derive, dissect, compile and test each meaning: does it do to the graph, silicon, memory and DNA what the definition describes. The place on the graph is found by the root code; then the label is applied. Guesses are always wrong; the long way cannot be shortcut; done in under two hours means done wrong.
- **Your examples are pseudo code.** The worksheet formulas (die = minus live and the rest) are illustrations of a process, never to be laid literally. "You can never pick a word arbitrarily and say this means this."
- **What the research added (10-22 report), which you have not ruled on:** the worksheet's minus does three jobs (not; opposite end of a signed axis; become), which are three silicon actions. Your two-word pairs are two-place relations (x before y) and need two holes. Durations are amounts, not clock positions. The function words (or, the, a, to, of, in, and, is) lead every most-needed count and have no body channel: they are operators and come first. Six tests exist for a candidate meaning: execution against uses, entailment with negatives, substitution, cross-source agreement, body balance, size penalty. A word is held after it passes execution and entailment on two uses, understood after it passes an unseen use, wired only then.
- **The remaining gap, measured.** In the 63-word test, turning a definition's phrases into before and after checks was done by hand. The brain has to do that step itself. That step is where understanding lives, and it is not built anywhere.

**Speak to [gap]**

- **Rule on the three operators.** Not, flip-on-axis, become, laid separately. Yes, no, or "it's the brain's to find".
- **What a root is, in your words.** The model holds 14 physical actions. The research says roots are measured, not assigned, and every system ended with 10 to 20 operators plus an open middle layer plus a residue. Say whether a root is a physics word, a formula of physics words, or something the brain discovers and we never name. And say what you would accept as proof that a root is a root.
- **One word, compiled, as a scene.** Pick a verb (give, or die) and speak what the brain does from hearing it with no meaning, to holding a meaning, to using it as a hop. Where does it get its uses (worlds) to test on? What does it write when a candidate fails? What does "held" look like as rows?
- **The understanding step.** Reading a definition row and picking out what must be true before and after. Say how you picture the brain doing that with what it has: a question run per definition phrase, a shape match against runs it already holds, or something else. Even a pseudo answer helps; I will mark it pseudo.
- **Operators first.** The data says function words come before nouns. Say whether that is the order you want told, or whether words, math and definitions still come together with no order.
- **The point and the label.** Points are meanings, as numbers; labels wait in the encoder until a meaning, formula or relation exists. Say what a point is physically in the hub build today: the gate number, a coordinate, or both.
- **Sources for meaning.** The body-channel norms (39,707 words), Binder's ratings, Dorr's verb formulas, VerbNet, are attached as one more source each, read like a dictionary, never as truth. Say if any of them is unwelcome, and whether the brain or the owner decides which sources a neuron carries.

---

## 7. Learning, understanding, applying: the brain writes its own code

This section is why every build failed the same way: the builder kept thinking for the brain. The document must say exactly where the builder's hands stop and what the brain changes about itself.

**What I hold [settled]**

- **One act of learning** = the brain finds a new formula on its own and makes it run. New neurons, new shards and moving points happen automatically and are not learning. Told is not taught; taught is not believed; copied is not learned.
- **Understanding** = what it learned balances with its sources and memories, so it runs almost like a deterministic function. **Applying** = using it as a hop somewhere new, including on itself.
- **The measure of success**: it learns something nobody taught it, understands it, applies it to itself. The builder is never given the example. Progress is when it takes a path we did not expect and we ask how that sensible answer came to be.
- **Learn once, hop forever.** The long way computes once and leaves a memory; after that use is a read. Any memory is an answer and any answer can be a shortcut. Shortcuts are the brain's own: 999 divided by 3 is 9 divided by 3 three times. Hundreds of thousands of steps means something is built wrong.
- **Told, not taught.** The brain can only be told. Told = a line through the ear that the brain writes word by word and the mother runs. Only physics, primes, the who/what/when/where/why/how frame, yes/no, "?" and core values are told. Teaching by asking: how do you, what happens if, what do we call this.
- **Claude writes the first code, then never again.** After turn one the brain writes all of its own, in neuron code. Nothing is left out of turn one; a part at root level is fine, a stub is cheating. No piece tests; the only test is the live brain.
- **Anatomy versus organization.** Fixed: the machine's instructions (atoms) and the bare unit pieces (a gate, a shard, a run passing a gate and taking a hop). Changeable, and the brain's own: which hop fires next, when to split, end or park, what gets remembered and how it is recognized, what connects to what, the order of use, and eventually its own kernel, tried on a copy and kept only if better. Told settings (beat, budget) are the chemistry. Only core values stay fixed.
- **Reasoning, born with**: substitution, deducing, deriving, understanding, learning, meanings. Take the string apart, ask questions, check state, sources and memory, ask more, form hypotheses, test, balance the outputs. The questions: have I seen this, did it work, was I right, was I wrong a lot, what did I try, was the environment different, what did I miss.
- **The adder lesson.** The make-new-neuron line (25 to 40 hops) is a formula used forever, so it must become short code: a remainder lands on the remainder node, which writes into the new-neuron formula node, which keys to BUILD: three hops.

**Speak to [gap]**

- **Where the hands stop, as a line in the sand.** Say the last thing a human lays and the first thing the brain writes for itself. In the egg today: five physics neurons, label = encoder, a BUILD gate that runs a receipt as SQL. Say whether that is the line.
- **How the brain writes a trigger.** The model's version 9 had: on a wrong expected output, step back to the unbound operator row, run trial clones with each other job, keep every trial as a memory marked right or wrong, write the balancing job into the row. Say if that is your picture of the brain writing its own code, or a builder's invention to replace.
- **A learned thing, as rows.** Say what a stranger would see in the tables after one act of learning: a new table, a new shard, a new trigger body, a memory marked derived. One example.
- **The brain changing its kernel.** Say the first change to how it thinks that you expect it to make, and how it would know the change is better (fewer steps, same answer; the form, fit, function test).
- **Sleep, the HC, the heartbeat, as the brain's own.** The HC need not exist on day one but the brain must be able to build it. Say what the brain is born with for that: a told line that describes the HC, or only the physics and the itch of bloat.
- **The day it does not need us.** Law 9: it aims to stop needing us as fast as possible. Say what that looks like in the first week: what it asks for, what it stops asking for.

---

## 8. The stage: what a person sees, and what it is a picture of

The Point Of Connection model is the thing the document will ship beside, so the document must say what on the stage is the brain and what is for the eye. Most of this came out of 10-22.

**What I hold [settled]**

- **The stage is 3D and must stay 3D.** Shells from the center out: roots, physics, primes, formulas, meanings, encoder labels on the outer shell. Relationship lines pull the points: alike beside, opposite reflected, kind one shell out, encoder forms on an arc. A run through neurons on a flat plane cannot have a shape to match. Flattening any group of points is a regression even when it is "more literal".
- **Points are meanings, as numbers.** A label without a meaning, formula or relation is not on the graph; it waits in the encoder, drawn dim on the outermost shell for the eye only.
- **Run shape is stored per memory**, and a shape match raises a metaphor candidate, announced as a guess.
- **Operators are neurons with rows.** The row hit by arrival and remainder picks the job. The eight internal helper runs the model once had are gone: a formula names the physics neurons themselves (memory, state, source, sense, agree, timeline) and landing on one runs its own trigger.
- **Say shows arrays.** Each step shows its array of alike words and names the pick (context, state, preference) as a gap.
- **The sensorimotor studies measured words and definitions, not meanings.** The body source is one input perspective, not the roots.

**Speak to [gap]**

- **What the model is.** Say in one line: the spec the build follows, a sketch to argue with, or a window onto the live hub brain. The document's reader will ask on page one.
- **What a shell means.** [mine] I read the shells as layers of composition: a point sits one shell out from what it is made of. Say if a shell is composition, distance from physics, age, or only a drawing convention.
- **The eye-only parts.** List what is drawn that the brain does not hold: the shells themselves, the dim labels, the colors, the arc of forms. Anything else.
- **What a run looks like on the stage.** Say what a stranger should watch to see a run: the path lighting up, the trigger runs branching, the memory landing. And what wrong looks like.
- **The measure on the page.** The absent list reaching empty, plus the residue count (named holes still inside held formulas). Say if those two are the numbers you want on the stage, or others.

---

## 9. Laws for builders: the rules that keep getting broken, with the why

The document's reader is most likely another builder or a model. A law without its why gets argued with and then broken; you have watched that happen on every one of these. Speak the why in one sentence each; the law I already have.

**The laws I hold [settled]**

1. **The graph is the code.** No engine, walker, sweep, backfill or helper outside the brain doing its thinking. Host code is the umbilical only, until the graph does the job itself.
2. **No new primitive.** Physics is the irreducible bottom. Before calling anything physics ask: can it be built from the others? If yes it is neuron code.
3. **No searching everything.** Never `*.*`. Find things the cheapest way: relationships, pattern formulas, state, memory. A long search is a bug to trace, never a wait.
4. **No chatbot.** No canned words, templates, reply rules, side tables. Judge by the record (what it did, made, tried, refused), never by the sentence.
5. **No guessing from the builder's head.** You are an LLM; what you know is a guess and never grounded. Lay actions and structure; facts come from sources, read by the brain. No bulk import.
6. **Owner examples are pseudo code.** Never lay a worksheet formula literally; never pit two owner illustrations against each other.
7. **No cop-out rules.** No forbid, null, any, all, skip or ask-the-teacher where the math should be searched. "Works for now", never "right".
8. **No tests to pass.** No piece tests, no hold-outs written by the lesson author. The only test is the live brain and its rows; prove by deleting the host code, not by matching output.
9. **No hands after told ends.** No answers during the watch window. Yes and no like a parent; never the answer.
10. **Build it correct or start over.** The brain stays alive between turns; once alive it never turns off, so per-table cost is no argument. Bloat is accepted until correct exists.
11. **Impossible output means ask how.** "3 + 2 = 2" is a bug to trace through the walk, counted across the whole class, never a trade-off to pick around.
12. **Label every guess.** Every design line is tagged owner's words or builder's guess. Never present a guess as the design. Do not rewrite settled documents unasked.
13. **The hop is before + after; the key is the remainder.** Never predict the next word, never chain shard to shard, never key by the whole history, never invent a position column.

**Speak to [gap]**

- **The why, one sentence each, in your words.** I have most of them as the incident that produced the law (the sweep that ran 29 minutes, the 16.2 walker, the 40 percent empty replies). Say the reason you would give a builder who has not seen the incident.
- **The three or four you would put on page one.** If a builder reads nothing else.
- **What a builder may decide alone.** N2 says the builder decides what the documents do not answer and logs one line. Say the limits: what must come back to you no matter what.
- **The owner's own trap.** You have said the first-day LLM-written prompt was mistaken for your words. Say how a reader tells your words from a builder's in the documents (a tag, a quote mark, a source file), so the next document cannot be mistaken that way.

---

## 10. Open items: the short list your words have not settled

Everything below is either marked OPEN in NEURON NOW or came up after it. The builder decides these unless you answer first. Answer any you can in one line; say "builder" for the rest and the document will print it that way.

| # | Item | Where it stands | Your line |
|---|---|---|---|
| 1 | Core values: who lays them, how | Blueprint guessed a gatekeeper, labeled as a guess | |
| 2 | Where a meaning's action physically lives | Trigger, DNA, relationships or the rigid layer | |
| 3 | Definition schema: its sections | Your coolness entry is the shape; the order is not written | |
| 4 | Zero versus absent | You: zero is null. Blueprint: gate 0 at origin, absent = no row | |
| 5 | The neuron's second birth memory | Unnamed | |
| 6 | The shape of a reasoning neuron | Many ways out, scratch pad, compiled: untried | |
| 7 | What starts back population | Builder's call so far | |
| 8 | The heartbeat | Varies with load; builder's call | |
| 9 | The channel for talking to the baby | Builder's call; the egg uses an input table and an answer column | |
| 10 | The sixth inside the graph or outside | Open | |
| 11 | The three operators (not, flip, become) laid separately | From the 10-22 report; not ruled on | |
| 12 | Operators (function words) told first | From the 10-22 data; not ruled on | |
| 13 | The understanding step: definition phrases into before/after checks | Not built anywhere; done by hand in the 63-word test | |
| 14 | What the Point Of Connection model is to the build | Spec, sketch, or window | |
| 15 | Trigger on the shard row, on the neuron, or both | NOW §8 floats extra remainders on a shard | |
| 16 | Where the hub build stands | Egg v2 laid 10-19 19:41 (5 physics neurons, BUILD runs a receipt as SQL); nothing newer in the folder | |

Anything you add while speaking goes in as a new row.

---

## 11. Glossary: your words, one line each

The document will carry this table at the front. Read down it fast; stop only where a line is wrong or a word is missing. Words a stranger will trip on are first.

| Word | What it means here |
|---|---|
| neuron | its own table; gate at the entry, DNA shards as rows, triggers, memories |
| gate | a neuron's address and its point on the graph; one meaning, one gate |
| shard | a DNA row keyed by the word before and after; stores the way to the next gate |
| DNA | all of a neuron's shards |
| remainder | the rest of the sentence as gate numbers; its head is the key at each hop |
| trigger | what a neuron hit excites; may start other runs; where everything happens |
| run | one pass through the gates the input gives, plus the trigger runs it starts |
| receipt | the path of gates and shards hit; the key to the run |
| memory | a run kept; active, persistent, long-term; condenses to highlights |
| timeline | memories tied to state and time, in order |
| truth shift | a point moved; the run's 3D shape changed; a new memory row |
| spawn | a remainder with no gate makes one, with its definition memory |
| definition | a source entry held as a run; describes a meaning, is not one |
| meaning | the executable a word causes to run; the point on the graph |
| root | a physical code action; still to be discovered |
| prime | one of the 65 actions every language has; a formula of roots |
| formula | a word's meaning written as other meanings with holes |
| hole | a "?" in a formula: a part with no meaning yet |
| relationship | a line that pulls a point: alike, opposite, kind, part, same spelling, and more |
| placement | tug of war: the point sits where its lines cross |
| encoder, decoder | where words, letters and labels live; who/what/when/where/why/how with every input |
| label | a word on a gate; waits in the encoder until a meaning exists |
| told | a line through the ear the brain writes word by word; the only way in |
| taught, believed | taught is told and repeated; believed is passed through the belief formula |
| guess | announced with data; never hidden; never lost; adjusted in sleep |
| belief formula | memory weight, error history, trust of source, support, inequality, expected output |
| trust | per voice per topic; accredited source above fuzzy above LLM |
| source | dictionaries, WordNet, references; never an LLM, never the owner |
| back population | awake, fast: a known written into the DNA where needed |
| back propagation | sleep: re-weigh recorded guesses on what was touched |
| sleep, nap, HC | alive; guesses adjust, memories condense; the brain asks for it |
| shortcut | a memory used as the answer; the long way computed once |
| the long way | computing a thing for the first time |
| the sixth | the brain prompting itself; writing into its own ear |
| mother | the embryonic runner the brain learns to replace |
| physics | the smallest primitives; the floor |
| anatomy, organization | the fixed machine versus how it thinks, which is its own to change |
| core values | the one fixed thing; cannot be untaught |
| stage | the 3D drawing: shells plus relationship pull |
| point of connection | the measure: the absent list reaching empty |
| residue | named holes still inside held formulas |
| learning | the brain finds a new formula on its own and makes it run |
| understanding | what it learned balances with sources and memories |
| applying | using it as a hop somewhere new, including on itself |
| makes sense | an inequality: closer, further, or balanced |
| canned | any stored sentence or reply rule; forbidden |
| the trap | host code doing the brain's thinking |
| turn one | the baby with every process and no data; nothing left out |
| told ends | the moment after which no human hand touches the brain |

**Speak to [gap]**

- Words you use that are missing here.
- Any line above that a stranger would read wrong.
- Two words you want kept apart that readers keep merging (run and reasoning; told and taught; receipt and memory). Say the difference in one line each.
