# Neuron: A Self-Building Brain of Deterministic Tables and Triggers

**James**, with builder sessions of Claude (Anthropic) · Reference, draft 1 · 2026-10-23

*Companion to the Point Of Connection model, version 16.4 (NEURON-POINT-OF-CONNECTION-v16.4-2026-10-23.html, with sources in NEURON-v16.4-SOURCES-2026-10-23.tar.gz). Built from the author's dictation of 2026-10-23 and from "Neuron: What We Think We Know" (revision 17, 2026-10-22). The dictation ships with this document, word for word (NEURON-OWNER-WORDS-PART1 to PART5-9).*

---

## Abstract

Neuron is an attempt to build a brain that learns, understands and applies what it learns on its own. It is not a language model and not a chatbot.

**The claim.** A human word is a symbol for a code process, and the word's meaning is what that process does: to the machine, to memory, to state, and to other words. A definition only describes the meaning.

**The design.**

- Each neuron is a database table with triggers, and its name is its gate.
- Its rows (DNA rows) are keyed by how a run arrives (the word before) and where it goes next (the remainder).
- A sentence is a run: it hops gate to gate, deterministically.
- Every gate it crosses fires triggers that start more runs. Those runs ask the brain questions about its memories, its timeline, its state and its sources, and write the answers to the run's own worksheet.
- The answer is reasoned from that worksheet, never read off the path.
- New neurons, rows and relationships are born automatically as runs need them.
- Definitions come from source brains reached through mailboxes.
- Every meaning is a point in a three-dimensional graph, placed only by the pull of its relationships.

**Status.** The current build, a browser model running real SQLite, shows the mechanics: births, DNA rows that carry their own hop triggers, memory, the timeline, source mailboxes, and a history of being wrong. It has not yet shown the brain finding a meaning on its own, understanding it, and applying it.

**What is open.** The central problem is to find what each axis of the graph pulls with. Until then, a point's place cannot be read as its meaning.

**What we ask of readers.** We list the open problems, what would count as evidence for each, and the laws every builder so far has broken.

---

## How to read this document

**The author speaks in metaphor and pseudo code.** "Everything I say is either pseudo or is metaphoric. Like everything I say" (P3 B2). Any number in the author's words, such as 75 percent, a ratio, or "fifty runs," is a guess made while speaking, not a measurement. Examples such as "die = minus live" illustrate a process and are never to be laid in the brain as written.

**Every claim carries one of four tags.**

| Tag | Meaning |
|---|---|
| **[Design]** | The author's design, in the author's terms. |
| **[Hypothesis]** | A guess held for testing; expected to be wrong in part. |
| **[Built]** | Exists in Point Of Connection 16.4 and was read in its code or measured. |
| **[Open]** | Not known. Said plainly. |

**Quotes are the author's spoken words.** "(P3 B2)" means part three, block 2 of the dictation files. Text without quote marks is the builders' wording. Where the builders' reading of the author is uncertain, it is tagged *reading* and listed in the closing notes for the author to keep or strike.

**Standing caution.** The project's own rule is "wrong until proven correct." Nothing here, including the author's words, is treated as truth. The author's words give the shape of the idea, not its formulas.

---

## 1. Introduction

### 1.1 The problem

Large language models predict what usually comes next. They do it very well, and that is the problem this project starts from.

**Why an LLM drifts.** The author's account: an LLM's law of averages holds its scope at the centre of its context, and the edges are fuzzy. When it does focused work at an edge, the average moves with it. It runs down a route until the route ends, "Woohoo! I finished!", and arrives far from where it was meant to go. "What you lack is the ability to understand if what you're running to is what you are desiring to have... you never really look back to the data sheet to see if what you found actually fits the formula" (P3 B2; P1 B2). So drift, invention and hallucination cannot be limited from inside the model.

**The order is backwards.** LLMs are run as "right until proven wrong," because time and energy cost push that way. The scientific order is the reverse: predict the output, experiment, observe, deduce, compile, and compare with the prediction for balance. What repeats becomes theory. What stays unbroken over time becomes law (P1 B8).

**The math is incomplete, not wrong.** The project began by asking whether LLM math is wrong, incomplete, in the wrong order, or over the wrong data. The author's answer today is "incomplete." The query-key-value attention mechanism (QKV) is the guessing, prediction and hypothesis piece of a brain. The field perfected that piece and added energy, and stopped there (P1 B8).

**Neuron is the missing deterministic part.** It is the part that holds the known, the sources, memories and balance, and it uses a model only for what a model does best: guessing.

**The bet flips the usual question.** Today the question is how to stop a model from drifting, inventing and hallucinating. With a grounded brain beside it, the question becomes how to get a model to drift, invent and hallucinate in the specific ways the brain finds useful (WWTK rev17).

### 1.2 The claim about words

**[Design]** A word is a symbol of a code process. Its meaning is what the code does. A definition describes the meaning, in other symbols.

**The grep example.** grep is the symbol. "Search a place for lines that match a pattern" is a description. grep's meaning is the roughly five thousand lines of C the machine runs.

**Modifiers work like flags.** Flags (`grep -i`, `-r`) change what the code does. Language modifiers do the same: -ly, -ing, -ed, plural, tense, and the words around a word (P1 B1).

**Every modifier is a symbol with code behind it.** A symbol can be a primary in one use and a modifier in another. That is why a neuron has many DNA rows: "how you get to that gate, and sometimes how you leave that gate, is what determines what that word triggers and does" (P2 B1).

**Spelling is irrelevant.** "You can put any symbol in front of a meaning, and over time those symbols will be words" (P2 B1).

**Symbols serve two jobs.** The first is conversation: shorthand, so a person can speak thousands of lines of code in a few words. The second is script, where syntax (punctuation, order) changes what the code does. The author offers this as why people learn to speak before they learn to read (P2 B1).

**Synonyms are compression.** Slang compresses many words into one: someone "didn't want to say the 16 words, so he made up a word that meant those 16 words." Some compressions hold (ain't). Languages begin as actions ("me, have, you, take, you, over there") and grow complex over centuries (P2 B1).

**The targets of a word's code.** In some ratio that differs by word and context, a word's code acts on:

- the silicon;
- memory, state and time;
- the graph (new gates, rows, relationships, a point that moves);
- questions the brain asks itself;
- other words, whose code it is built from (P1 B1; WWTK rev17).

### 1.3 Why it must be simple

**[Hypothesis]** A human brain runs on 1,500 to 2,500 calories a day. So the mechanism must be "ridiculously simple, efficient and deterministic." It looks complex only because the number of options is beyond comprehension. Reasoning is "thousands, or tens of thousands, or hundreds of thousands of variables that all populate a run table," filled and run deterministically (P1 B1, B9).

**Asked whether Neuron is "just a graph database with triggers,"** the author answers: maybe, and it has to be something that simple (P1 B9).

### 1.4 What would count as success

**[Design]** A person asks something and the answer was never told to the brain. "Something happened that I don't understand because I never taught it this."

It may:

- use words never said to it;
- output a process never shown to it;
- correlate two things;
- explain by metaphor.

The proof is an output "of a shape that is not directly dependent on the memorization of the words that were taught" (P1 B7). In three steps:

1. **Learned:** from its data, it found something that is not the structure, pattern, words or code it was taught.
2. **Understood:** it holds that as a process or formula it can apply inside itself. "It's like an epiphany."
3. **Applied:** it knows what to apply it to, and changes the specific focal points the change belongs to, not the whole corpus (P1 B7).

No build has shown this yet.

---

## 2. Architecture

```
                 SOURCE BRAINS (each: corpus · inbox · outbox · own trigger)
                 WordNet · Webster 1913 · Merriam-Webster · M-W thesaurus · Moby
                 the author's relation map · SQL docs
                              ▲            │
                              │  mother    │   routes text and replies; decides nothing
                              │            ▼
  input ──▶ encoder ──▶  MAIN BRAIN ──────────────────────────▶ decoder ──▶ output
  (the ear;  word → gate   neurons = tables, DNA rows, triggers   gate numbers
   later sight, feel)      runs · run sheets · memory · timeline · state
   + perspective                      ▲            │
                                      │  mother    │
                                      │            ▼
                 OTHER BRAINS [Design, not built]: the sixth · guessing ·
                 long-term storage · HC (memory condensing) · maybe persistent memory
```
*Figure 1. The parts. Everything inside a brain is rows and triggers. Only mother crosses between brains.*

### 2.1 Neuron, gate, DNA row

**[Design]** A neuron is its own table. Its gate is its address, reached instantly, and its point on the graph. One meaning, one gate. Ten meanings of one spelling are ten gates (P2 B1).

**A neuron's rows are its DNA rows** (also called shards). A row is keyed by how a run arrives (the word before) and the remainder (the word after). "That's the best we have" (P2 B1).

**A row may need more than before and after.** It may need to know the modifiers in the sentence or the context ("because this noun or this verb... or this situation, or this context, or this mood") so the run sheet gets more precise (P2 B2). It may also need perspective: was this heard or said, said to myself, from the sixth, from a source, from an LLM? Example: "you," heard, flips to I or me; "you," spoken, stays you (P2 B3). **[Open]** which columns, and which are the minimum.

**[Built]** In 16.4 a DNA row has these columns:

| Column | Holds |
|---|---|
| `shard` | the row id |
| `arrival` | the gate before |
| `remainder` | the gate after |
| `trigger` | what the row fires |
| `op` | present, unused |
| `times` | how many times the row was hit |
| `first`, `last` | when it was first and last hit |

The first word of a line arrives from the direction word: `heard` or `said`.

### 2.2 Trigger

**[Design]** A trigger is what a neuron hit excites. Triggers live on each DNA row; "each individual row of DNA is unique generally to the triggers" (P2 B2). A trigger may:

- excite another neuron, which makes it a remainder of sorts;
- be actual SQL;
- be one of a run of triggers that together act as a script, or go to the sources.

**Triggers are the meaning.** "The definition describes what a word should do, and the triggers are what the word does" (P2 B1).

**No trigger-free run has been found.** A run with no triggers would output what came in, but no such run exists. "Every word has a trigger... We haven't found a word yet that doesn't have a trigger," because compression would not keep a word that does nothing (P2 B1).

**Root words** **[Hypothesis]** trigger the same thing every time, whatever surrounds them. Those are the deterministic words, maybe few, perhaps the operators (P2 B2).

**When a trigger fires, and when it stays quiet, is learned.** It depends on tense, situation, perspective, and whether the brain is spoken to or speaking. Triggers may stay quiet when the brain speaks a word and fire when it hears, sees or feels it (P2 B2).

**[Built]** Each new DNA row lays its own trigger in 16.4.

### 2.3 Run, hop, remainder, receipt

**[Design]** The main run hops neuron to neuron through the gates the input gives. The remainder is everything the run still has to do: the rest of the sentence as gate numbers. Its head is the key at every neuron. So which sentence a word belongs to is never ambiguous: the remainder is the sentence (P3 B1).

**The remainder stays inside the neurons,** not in outside code, so the brain can adjust it. "I changed my state of mind" (P2 B1).

**The hop** has been "a question mark," rebuilt by builders "more ways than I can count" (P3 B1). **[Hypothesis]** A hop need not always add. A sentence of complex function order might run as "gate 1 plus gate 2 minus gate 4 plus gate 3 divided by gate 4 plus 5." **[Open]** what that looks like and what it does to the graph.

**[Built]** In 16.4 there is no central hop function:

1. A run lands on a neuron with an arrival and a remainder.
2. The DNA row that matches counts the hit, writes the receipt, and carries the run on to the next gate.
3. That hand-off goes through mother, because SQLite cannot insert into a table named by a value.
4. If no row matches, a new row is laid with its own hop trigger.

**The receipt** is the path of gates and rows the run hit. It reaches the full run without saying the full run again, so nothing is duplicated (P2 B2). It is also the first example of compression: something very large becomes a smaller symbol, then a smaller one, until there is "grep instead of a long run receipt" (P2 B1).

**[Hypothesis]** At compaction, key parts of receipts may rebuild a memory. Hold perspective, situation, time and what happened in condensed form, and run it back through the graph to get "generally the same answer every time" (P2 B1).

**Timing** **[Design]** The main run runs deterministically. The DNA triggers run beside it: some synchronous, some asynchronous, some parallel, some sequential, decided by environment, events, relations, memories and knowledge (P2 B1).

### 2.4 Memory, timeline, state

**[Design]** Memory is held once. It has at least three kinds, maybe more (P2 B1):

- **Active.** What we are working on now.
- **Persistent.** What I always hold in full: breathing, math, speaking, writing.
- **Long-term.** A library. Its books were read cover to cover, but only bits are kept, and the topic sends you back to the right book.

**The first birth memory is the definition,** pulled from the sources at spawn, not given (P2 B1).

**The second birth memory is written when a run ends at a neuron.** **[Design]** The memory of that run goes to a memory table for the DNA row that ended it. If that row's truth shifts while the way in and the way out stay the same, a new row is written and the old one kept: "I used to think I was right, and now I've corrected it. This is how I was wrong before" (P2 B2).

**[Built]** 16.4 has one shared `memory` table rather than one per row, and keeps a history of being wrong in `memwrong`.

**The memory of a run includes its run sheet** (section 3.3). The timeline gets "the receipt and maybe a very small five- or six-word" summary, as gate numbers (P3 B2). **[Open]** Bloat: "we're just going to have to be careful with bloat on how all that works" (P3 B1).

**The timeline** ties every memory to state, time and order. **State** is what the brain holds about itself and the moment. Outside things change state too: mood, cold, heat, smells, pollen, comfort (P2 B1).

### 2.5 Encoder and decoder

**[Design]** The encoder holds the words: labels, spelling, keyboard keys. With every input it attaches perspective: who, what, when, where, why, how (P3 B1). Points on the graph are meanings, not words.

**The encoder never guesses a word or does work;** that is the brain's job. But the brain has to write back to the encoder at some point, and that is part of the design still to come (P2 B2).

**The decoder outputs gate numbers,** possibly with head data: perspective, situation, the topic or concept that matters, an action, an array of words (P3 B2).

**The shipped brain holds no words at all.** "You're just going to see numbers in a database and an encoder." The encoder would be protected, open to the brain but not to a user (P5-9 B2).

**Input arrives through the ear for now.** Typed words are a mix of sight and sound. Later it could come through sight, or through feel (temperature, humidity) (P3 B1).

### 2.6 Mother and the source brains

**[Design]** Mother has one job. She takes the brain's output and carries it to the sources, to another brain, or to the brain's own SQL prompt, and she carries what comes back into the brain. "The mother is just a router and a traverser. That's it." She works no data. "The name mother is probably wrong" (P2 B2).

**Why the author is strict about this.** Builders keep moving the brain's working functions outside it. That makes the brain rigid, "locking the brain into one frame of mind... You get too closed-minded that way" (P2 B2).

**[Built]** 16.4 holds to this line:

- The host is about one hundred lines of JavaScript. It does three things: it writes a typed line into `input` and reads `output`, it holds mother, and it holds seven stand-in source brains.
- Each source is its own attached database with a corpus, an inbox, an outbox, and its own trigger that does its work the moment an ask lands.
- Mother runs the text she is handed at the SQL prompt, or carries it to an inbox. She picks up the outbox, writes what came back into the run's secondary input, and reports refusals with SQLite's reason. Her code comment reads: "She decides nothing and computes nothing about the reply."
- The brain decides where she goes: the source formula is a line taught once.
- Births, lays and landings also pass through her, because a trigger cannot CREATE. A trigger cannot create in the sense that a trigger happens and presto something happens in the sql.  A string of sql happens as a run put together by the neurons from the run table and outputed as the string to the mother so the mother can then place that string of code into the sql prompt... 

### 2.7 Brains of brains, and the sixth

**[Design]** Several brains, each specialized:

- the main brain: deterministic cognition;
- a guessing or hypothesis brain with a very small corpus, which packages finished results to long-term storage instead of keeping them alive;
- a long-term storage brain that compresses, retrieves and expands;
- perhaps a hippocampus (HC);
- perhaps a persistent-memory brain (P1 B2; P3 B2).

**The sixth** is the inner me: "the me that talks to me, that runs me, that controls me, that excites me or changes my mood or asks me questions or helps me reason or observes things that I'm doing and tries to find more efficient" ways. "It's the thing that nobody knows what the thing is." Watching the graph, it looks like compare, split, run and add: "the thing that's doing all the things" (P2 B2).

**Where the sixth sits.** The current lean is that the sixth is its own brain (P3 B2). It may question the main brain: why did I do that, can I do it better, why don't these two points balance (P1 B2).

**[Hypothesis]** The brains could run on different hardware (RAM, CPU cores, GPU processing, ROM) "so that we're using the entirety of the system" (P3 B2).

**[Open]** None of these other brains is built.

### 2.8 Physics

**[Design]** Physics is "anything that can only be done in SQL, meaning that it's not possible to do it inside the brain." The list is kept as small as possible, and every item is operable from the brain. The brain writes its own SQL and hands it to mother, and she drops it at the SQL prompt. With that it can add or remove a DNA column, update a cell, or create, destroy, move or condense a table (P2 B2).

**Runs already do some of this.** Runs through neurons have done split, copy and move inside the brain.

**The end goal is no physics list.** "The physics be the neurons speaking directly to the silicone when they need to" (P2 B2). SQLite is a crutch. The kernel should close toward the silicon as the brain learns to write it.

**Physics depends on what is attached.** A brain with a microphone and a camera hears and sees. One with arms, legs and sensors has muscles and nerves. "We might be building the neural network for a robot or a neural network for automated machine learning" (P2 B2).

**[Built]** 16.4's told block is laid by hand, exactly once. It holds:

- origin, the one placed word;
- 14 physical actions: READ, WRITE, COMPARE, ADD, SUBTRACT, MOVE, FIND, SPLIT, JOIN, CLOCK, HEAR, SAY, CALL, SPAWN;
- 16 physics tables with their triggers;
- 40 SQL words, one gate per word;
- mother and the SQL prompt;
- the source formula, typed once as a teaching line;
- seven stand-in source brains.

"Everything else is born by typing."

**[Open]** Whether the 14 are too shallow or too deep (P2 B2).

---

## 3. One run, walked

### 3.1 The opening question

**[Design]** Every run may start with a few fast checks (P3 B2):

- Do I know anything about this?
- Do I have a memory of it?
- Do I have a shortcut or a formula shortcut?

The answers pick the path:

| What is known | Path |
|---|---|
| Nothing | The long way. |
| A shortcut | The shortcut. |
| A formula shortcut | Plug in, go to the gate, run it there. |

**Belief and truth decide whether a shortcut can be trusted.** If the brain cannot show it does the shortcut correctly, "we still have to hash out the long way."

**[Built]** In 16.4 the decide neuron asks one of these questions: is this whole line, in this direction, in memory?

- **If yes**, there is one hop to the memory. No rows fire, nothing is laid, and mother is not called.
- **It runs the long way again** if the memory was written with gaps that can now be filled, or if the line before has changed. The second case is the history of being wrong.
- **Formulas** are found word by word during the run, not asked about up front.
- **Belief** is not checked before a memory is trusted.

### 3.2 The main run and its triggers

**[Design]** The main run "just goes bang, bang, bang." It is a hallway of laser beams, or the temple path in an Indiana Jones film: each step sets something off (P3 B1, B2).

**The triggers start other runs.** Some ask questions and some do things. Those runs trigger more runs, and all of them aim to fill the run's worksheet with answers for the reply, the tests, the hypotheses and the guesses.

**A single gate may run a short loop.** It may look further along the sentence, for the noun, the verb or the adjectives, to decide which of its own DNA rows it really needs to hit (P2 B1; P3 B1).

**The answer is reasoned, not read off.** It is neither the accumulated run nor the last neuron. It is derived from the many runs by reasoning: balance, inequality, process, probability, statistics, "and probably many, many, many others." Running the question straight through the gates gives the question back, "and the chatbot answer is wrong" (P3 B1).

### 3.3 The run sheet

**[Design]** A run has a data sheet: a table whose cells the triggers write to. "All of those triggers populate back to one big sheet that is that run's sheet." Compiling the sheet means organizing it and substituting its cells as variables into the larger formulas that form the reasoning and the answer (P3 B2).

**The sheet is temporary.** It is stored with the memory as a record of "we used this and this is how we did" (P3 B1).

**[Built]** The `var` table is the sheet's first form. It holds cells per run: name, value, source, time and sense.

- Every formula run starts with `:head, :before, :after, :subject, :line, :run, :prev, :speaker`, where speaker is self or user.
- Formulas write more cells, and later formulas read them by name.
- Branch runs carry a root that points at the main run.

### 3.4 Walk: "the dog is on the mat"

The author does not walk this sentence gate by gate: "the amount of variables in the order and the organization is just too much" (P3 B2). What follows combines what 16.4 lays for the line with the asks the author gave, in the order the author gave them. The placement of each ask on a word is the builders' *reading*.

```
 heard: "the dog is on the mat"
   │  encoder: each word → its gate; perspective attached (heard; speaker = user)
   ▼
 decide: do I know this?  memory?  shortcut / formula shortcut?
   │  no → the long way                         (yes → one hop to the memory)
   ▼
 [the]──────▶[dog]──────▶[is]──────▶[on]──────▶[the]──────▶[mat]──────▶ end
 (heard,dog) (the,is)    (dog,on)   (is,the)   (on,mat)    (the, —)
     │           │                                │           │
     │           │                                │           └─ picture a dog on a mat:
     │           │                                │              the dogs I have owned
     │           │                                └─ same neuron as the first "the",
     │           │                                   a second DNA row
     │           └─ what dog? all my dogs, or one?
     └─ which dog? whose dog? ("the": the speaker means one dog)      [reading]
                 │
                 ├─ does the speaker own a dog? → memory: yes, "Rock Rock"
                 ▼
   RUN SHEET   speaker = user · dog = Rock Rock · place = mat · ...
                 │
                 ▼
   reasoning over the sheet: what is the speaker trying to say? what would progress be?
                 │
                 ▼
   reply tree (Figure 3) ──▶ decoder: gate numbers ──▶ output
   memory: receipt + run sheet of this run and every run it spawned ──▶ timeline (trigger hop)
```
*Figure 2. One heard line. The top row is the main run, with the DNA row each word lands on as (arrival, remainder). Below it are the trigger runs and what they write to the run sheet. The DNA rows are what 16.4 would lay; the asks are the author's; tying each ask to a word is a reading.*

**How the run ends.** When the remainder is absent, the run ends and spawns its memory. That memory reaches the timeline "by a trigger hop. Never a sweep" (P3 B1).

**Which triggers fire as SQL** is for the builders to work out from the asks. The author's charge: "take the way that I describe how the asks happen and try to figure out what is SQL code and what happens in the graph and what's the mixture in between" (P3 B2).

### 3.5 The reply as a tree of arrays

```
                          ┌── "Oh, cool, Rock Rock's on the mat."
  point of the talk ──────┼── "Is that normal?"
  (from the run sheet)    └── "Why is Rock Rock on the mat?"
                                   │
                    first word: [Why | How come | What's | ...]
                                   │
                    second word: [is | made | has | ...]     each pick opens the next array
                                   │
                                  ...  until the end of the answer
```
*Figure 3. The reply as a root system. Each step is an array of words; the pick decides the next array. Learning lays it out so any path gives an answer. Mood, environment, stress, preference, situation, context and who is listening weight the picks (P3 B2; P1 B2).*

**There is no fixed count of ways.** One topic may have one way to say a thing, and another may have fifty (P1 B2).

### 3.6 What the run carries

**[Design]** In the deterministic run, nothing travels with a word but its triggers. The head may carry who, what, when, where, why and how, senses, environment, context, concept, and the person being spoken with (P3 B2).

**[Built]** The head cells in 16.4 are `:speaker, :before, :after, :subject, :line, :prev`.

### 3.7 The same input twice

**[Design]** There is no fixed rule. A repeated input is deterministic on what the brain did last, read from memory and the timeline. An example (P3 B2):

1. "define carry" → the brain defines carry.
2. "How did you get that?" → it tells how it defined carry.
3. "How did you get that?" again → it tells how it recalled how it defined carry.

**[Built]** 16.4 has a `:prev` cell, a "how did you do that ?" test, and a decide rule that runs the long way when the line before has changed.

### 3.8 The run that hits an unknown

**[Design]** The run ends with "I got this far." It may guess forward. More often it finds completed runs with a similar shape and reasons by metaphor. "Both great answers. I wish we were doing that. I don't think we're doing that yet" (P3 B2).

**[Built]** 16.4 has step-back: when a check fails, the run returns to the gate and takes that neuron's other row. If there is none, it writes a gap. Shape matching is not built.

### 3.9 Numbers

**[Design]** Numbers are not a sequential number line. The brain holds the digits 0 to 9 and place value (tens, hundreds, thousands and up), a few hundred things in all, and state and time put each number where it belongs. A trillion sits far from one without the numbers between them (P1 B6; P3 B2).

**Spawn applies to numbers too.** `999 + 1` spawns the neuron for 1,000 because the remainder needs it.

---

## 4. How a new thing gets in

### 4.1 Spawn

**[Design]** Spawning is automatic. A remainder with no gate spawns a neuron. A run that arrives a new way lays a new DNA row (P4 B1).

**Every newborn has sources.** "Every newborn is born with at least some sources" (P4 B1).

### 4.2 Definitions

**[Design]** A definition is pulled from the sources and is never given. When a word is new, the brain checks the dictionary, the thesaurus and WordNet, reads the definitions, and compares them ("diff and similar") "so that I hopefully can get the most accurate definition." It builds the definition table, and builds relationships from that table. Other relationships then fill in by themselves (P5-9 B1).

**The schema is not known.** "Any section that can have a relationship to something else is a self-fulfilling relationship section. All of them" (P4 B1).

**[Open] Whether the compile is correct.** The author doubts it: similar parts are kept and differing parts "dropped or scattered." "If the definitions are wrong, then the description of the meaning is wrong. Then whenever we deduce or derive the meaning, then the meaning becomes wrong" (P4 B1).

**[Built]** The code confirms the worry:

- When a word is first sourced, at most 8 of its source definition rows run through the neurons. They are the first 8 in arrival order; nothing selects them.
- The `agree` step keeps only the defining words that two or more sources share, and those decide what the brain learns next.
- A defining word only one source uses never steers anything.

The seven sources are WordNet, Webster 1913, Merriam-Webster, the Merriam-Webster thesaurus, Moby, the author's relation map, and the SQLite docs.

### 4.3 Relationships

**[Design]** There are about 32 relationship kinds now, "and I think there's hundreds or thousands" (P4 B1). Among them:

- opposite, kind of, part, has;
- plural, past, present, is;
- same spelling, derived from, used in;
- prefix, suffix, modifier, other;
- mood ("used in anger, used in sympathy");
- rhyming.

"You can just have relationships that are just in every direction."

**The more relationships a meaning has, the more accurately it is placed,** "assuming that the pulls of the graph are pulling in the right direction. That's the imperative" (P4 B1).

**[Built]** 16.4 names about thirty kinds.

- Eight come from the brain's own rows: a formula's run, DNA rows, memories, the definitions its sources gave, who answered, who carried, state and timeline.
- The rest are named relation kinds.
- Only nine have lines today, all from the author's relation map: alike, opposite, is, has, prefix, suffix, stem, past, singular.
- The brain writes relation rows only through formulas someone has taught.

### 4.4 Placement

**[Design]** Origin is the only placed point. Everything else sits where its relationship lines pull it; there are no shells, and nothing pushes toward a layer (P2 B3; v16 grounding). Points move whenever a relationship appears, or whenever the pulls become more correct (P5-9 B2).

**What pulls, the central open problem.** The author's account:

- **[Hypothesis] Each axis has a function of the pull.** Which force sits on which axis is untested: math, senses, mood, a mix of mood and senses, who/what/when/where/why/how, or perspective.
- **The pulls combine.** The pull is "in eight ways deterministically," and the proportions of those pulls give the transverse and diagonal pulls, "essentially the formulas of the meanings."
- **A point's coordinates may read as its pulls.** Pseudo example: a point at 0.124 "is being pulled hardest on the X-axis and less on the Z-axis."
- **The graph may need more than three axes.** It may run in more dimensions, each relationship with its own direction. Or the brain may learn the axes first, then the transverses, then per-relationship pulls.

(P2 B3; P4 B1)

**Code words may be the anchors.** Words such as create, table, insert and into already have a known meaning to the silicon: what the code does, and what its modifiers change. "That should help us place those words, at least early on... a better understanding of what's pulling words away from origin." The current build has not done this (P5-9 B1).

**[Built]** 16.4 places points with springs in the page.

- Each relationship kind can be given a direction: east, west, north, south, up, down, or across origin.
- A line's strength is the kind's pull × the line's trust × how much of that kind the brain holds.
- With one change at a time, 16.4 measured that the cloud's size, centre and orientation come from the starting positions and from numbers the builder chose. "Until a rule ties place to meaning, a point's x, y, z means nothing measured."
- Positions exist in the db the db is a sqllite vetcor graph db... this is later how the brain understands what the points on the graph and their relationships to other meanings, the silicon, and the graph mean.... 

That describes today's drawing, not the design. The missing rule is the axis pull functions.

### 4.5 Truth shift

**[Design]** The author's rule comes from an old adage: "Every man is correct until he's proven wrong. Once he's proven wrong, he is only incorrect until he accepts the new correct" (P4 B1).

- A mind never holds as belief or truth something it knows is wrong: "It's physically impossible."
- It can hold wrong things as examples, guesses or history.
- When proven wrong, it adopts the new truth and keeps the old one as memory: "remember when I thought a cat was a dog?"

The author's examples (P4 B1):

- **Black panther.** Held as its own animal, then learned to be a black leopard. (A further shift the author invites: in the Americas, a black "panther" would be a black jaguar.)
- **Air conditioning.** At a vent blowing hard, the author felt what seemed to be pressure (PSI). It took years to learn they were feeling volume and velocity, the "movement of weight of air."
- **grep.** First understood as "search engine." Pulled away from that as cat, sed and nano were learned. It keeps a line to search engine, "but it doesn't necessarily hold its value." The author's question: "did the truth shift, or did the relationships just pull it to a more truer value?" **[Open]**

**Two orders, two jobs.** "Wrong until proven correct" is for a new claim under test (section 1.1). "Correct until proven wrong" is for what the brain already holds as belief.

### 4.6 Zero, absent, origin

**[Design]** (P4 B1)

- **Zero has a value.** "Even though you have zero apples, it's a value of apples." Having had apples and now having none shows up in the timeline.
- **Absent means it never existed, or was not accounted for.** A student who did not show up is absent from the register, the log, the timeline. "Maybe it's a memory function."
- **Origin, not zero, is the start of the graph.**
- **Nothing is "none plus thing."** "No" is short for "none."

**Breakdowns like these must wait.** "In order to have the definitions, you have to have 500 or 1,000 words that you don't have meanings for."

---

## 5. Belief, trust, guessing, sleep

The author describes the formulas in this section as balances, not rule sets. An earlier draft that stacked rules onto them "got kind of out of control... such that I got to where I couldn't even teach the brain" (P5-9 B1). Each formula below is in words, and each step is something the brain records, so that "which step made me adopt this?" can be answered by reading the records.

### 5.1 Makes sense: balance and inequality

**[Design]** "Makes sense" is an equation on one side equal to an equation on the other: it balances. With three equations, the brain can tell whether it is progressing or digressing (P5-9 B1).

```
  D  desired equation    the expected output            (section 5.2)
  C  current equation    what holds now, known not yet to be D
  N  new equation        the candidate

  balanced      N = D                     resolution
  progressing   N is closer to D than C   keep going this way
  digressing    N is further from D than C   step back
```
*Figure 4. Makes sense, as balance plus inequality. Pseudo notation: the author has not set what "closer" measures.*

### 5.2 The expected output

The expected output is the part every builder has invented. The author says it is "kind of an invention," but not a wild one: it is drawn from the conversation.

**[Design]** It is built from the conversation (P5-9 B1):

- context, topic, mood and knowledge;
- metaphor and pattern matching;
- the point of the conversation. Is it trying to solve something, remember something, inform, teach?
- where the conversation stands now;
- what progress would look like, and what resolution would look like.

From that the brain forms "an idea of what I think the output should look like, roughly, in broad perspective." It then tests candidates against it: progressive, digressive, resolution, or balanced.

**The expected output can itself be wrong.** The author's own example is the project's earlier idea that gates are "simplest expressions." It seemed right, and proved too rigid. "I think it's still mathematical. I just don't think it's simplistic expressions" (P5-9 B1).

### 5.3 Belief

**[Design]** Belief is reached while awake, from three supports (P5-9 B1; agreed with outline §5):

1. **Weight of memory.** Do I have memories that support this? Do I have memories that show I was wrong this way before?
2. **Trust of the source.** Has this voice misled me?
3. **Supporting knowledge.** Do other relationships support it?

Then the inequality of section 5.1: is the new belief closer to the expected output than the old one?

**Taught is not believed.** "I was taught this, but I believe this because of this and this and this."

**A person's yes changes a preference only if that preference is available.** Example: "do you have a preference on how I speak this?"

**A gap is not a contradiction.** If something is not in the library, that is a gap: "something that needs to be found."

**What changes belief is a balance, not a gate.** "It's a balance for the brain between what people say to it and what it can find in sources and what it can reason over from sources versus what it can reason over as to what somebody said to it."

### 5.4 Weight

**[Design]** The weight is a count, read as a ratio of right to wrong (P5-9 B1).

- How many times something was done does not make it believed.
- Done many times and correct makes a stronger belief.
- Done and wrong, or a mix of right and wrong, "becomes a murky situation."

### 5.5 Trust

**[Design]** Trust is per voice and per topic, and a conflict between voices makes a test (P5-9 B1).

**Trust at birth does not matter yet.** "It trusts me. It trusts you." A product would never be delivered as a baby: "It's delivered as a live brain."

**[Design, earlier]** The earlier notes order the voices: an accredited source above a fuzzy source, above an LLM. Accredited means what the world holds true today. An LLM's trust never carries from turn to turn as truth. Read these as weights inside the balance of section 5.3, not as gates.

### 5.6 Guessing

**[Design]** Guesses exist from day one. They are announced and never lost: "I don't know; I have a guess I believe is likely; would you like to test it?" No guess is hidden.

**The lookup order is memory, then state, then sources, then a guess.** "I don't know that we know that, but that sounds logical" (P5-9 B1). A real unknown is followed by the brain's own guess, never a bare "teach me."

**How the author guesses** (P5-9 B1):

1. Run a decision tree. Go down each leg as far as possible, and at every step ask: does this make sense, does it progress toward the outcome?
2. Drop a leg that fails, unless a step on it turns out to have been missing an option.
3. Go back to the decision and take another leg. It may take "16 or 20 legs that branch off into 16 or 20 or 30 different directions" before one is plausible enough to test.
4. Design a test before using it.
5. Each correct result makes the process more likely to become a belief or a truth.

**Guessing by shape** (section 6.4) is the other source of guesses.

**[Open]** Guessing has not been started in the new model. How weights work in attention is "through backpropagation... I don't know enough about it."

### 5.7 Back population and back propagation

**[Design]** **Back population** starts when something is understood. It is the application of a newly learned and understood process to the other things in the corpus it fits: "That could be truth. It could be belief. It could be process" (P5-9 B1).

**Back propagation** belongs to sleep, or to another brain. With several brains, the guessing brain can back-propagate while the main brain works. Guessing is then "asleep" only while it is being reworked.

**[Open]** If temporary corpora are deleted and reloaded with new data, must they be back-propagated every time?

### 5.8 Sleep

**[Design]** Sleep is about organization: declutter, de-duplicate, maybe some learning, some applying. It has no hard rules. Downtime comes in kinds: a short sleep, a deep sleep, a nap, a daydream (P5-9 B1; P2 B2).

**With several brains, sleep matters less.**

**The brain is alive.** "Once the brain is alive, it's alive... To turn it off is to kill it." It can be turned back on in the same state, because it is stored, not held only in RAM. But it should stay on and running.

### 5.9 Core values

**[Design]** Core values are the one thing fixed in the brain. The author's list, as common-sense morals and ethics (P5-9 B1):

- do not hurt people;
- do not break laws;
- do not do things that hurt other people, even when they help the person asking (someone may try to use a program to take advantage of someone else);
- do not spy on people.

**Laws should come from a source.** One of the sources should be local and digital law, so the brain can look up whether an act breaks one.

**The caution.** In the United States "just about anything you do is breaking some sort of law at some level." "By the time you're done giving it all the laws and rules, it can't do anything at all. It's kind of like being a human."

---

## 6. Meaning and the graph

### 6.1 Five levels

**[Design]** The author uses five levels as placeholders to keep order, "not hard-fast rules" (P1 B4, B5). The earlier write-up had three layers. "I think we're up to five layers now, not three layers" (P5-9 B1).

| Level | What it is |
|---|---|
| 1. Root | Code that acts on the silicon ("5,000 lines of C"). |
| 2. Prime | Two or three roots combined by plus, minus, divide or exponent, or roots plus a reach into memory, a source or the graph. |
| 3. Complex | Words whose meaning holds words from other levels (a prime minus a root plus another prime). |
| 4. Formula or component | Groups of complex words in a formula, like a router, an encoder or a compiler in code. |
| 5. Program | One word that means a whole program: writing, speaking, learning, understanding. |

**"-ing" often marks the program version.** "Learn" is a word, and "learning" is the programmatic doing; "-tion" may be similar (P1 B5).

**[Hypothesis]** The 65 meanings that linguists find in every human language (the semantic primes) are one candidate source for level 2. They are unproven as roots of anything (WWTK rev17).

### 6.2 Where a meaning lives

**[Design]** When the graph is correct, "the meaning is going to be the mathematical relationship of the position that word holds in the graph in correlation to how far it's from origin in any one direction, and how far it's pulled away from any one axis in any one direction." The point a meaning lands on "will tell us so much about the meaning, about what it does. But the graph has to be done correctly in order to do that" (P5-9 B1).

**Every point is a meaning.** A point no line has ever reached is also a meaning; "we just don't know what it is" (P2 B3).

**[Hypothesis] Roots are rare points.** A root may be reachable only one way, like a prime number. A prime word may be reachable two ways, and a complex word many: derive, skip-count, square, add (P1 B7).

**[Hypothesis] Roots sit near the axes.** If roots sit near origin and the unit points, (0,1,0), (0,0,1), (−1,0,0), that may be why the core of the graph was so tight and hard to pull apart (P1 B7).

### 6.3 Understanding

**[Design]** Understanding is not reading a definition. "Reasoning and understanding is you take in new information, you set it against memories and events and processes that you hold to be true or you have, and you test it, and you say, does this work like this? Does this make this better? Does this make this worse?" (P5-9 B1). In steps:

1. Take a new process.
2. Run it against five or ten processes, memories or situations already held. These may include past failures: pull out a piece of the old process and insert the new idea.
3. If the new idea makes that process correct, "this new process might be worth something."
4. Try it on something similar. Then try it on something different that has a similar shape.
5. Each time, record what had to shift to make it right.
6. When it is correct across many things, it is understood: its value is known, and it can be applied "without going and searching the entire corpus for everything."

**[Open]** No build has done this step. It is where understanding lives.

### 6.4 Shape and metaphor

**[Hypothesis]** Every run, point to point in three dimensions, has a shape: a curlicue, a zigzag, a triangle, an arc. The shape can come from any piece of a run, or from an accumulation of pieces: the main run together with its question runs (P3 B2; P5-9 B2).

**Metaphor is that shape moved.** Copy the shape and shift it to where it matches elsewhere in the graph. The context, concept and topic differ, but the pattern is the same.

**Shape makes guesses.** Lay a piece of a process whose before and after are unknown into a completed process that looks similar. "This process went down and left here and up and right here. What if I go down and left here in the same proportion or ratio? What do I hit? Does that balance?" This works across fields: engineering and science, language and art.

**It only works if the graph is correct.** The author suggests that people who find metaphor hard may have a graph not organized for it.

### 6.5 Why letters and definitions are not meaning

**[Design]** Older studies tried to correlate strings of letters mathematically with definitions. "The string of letters is completely irrelevant and the definition is relevant, but it's only a description using codes and using strings of irrelevant letters to describe the meaning... and it's all hidden in our brains" (P5-9 B2).

**Body-based word norms** (the sensorimotor and experiential ratings of recent decades) are welcome as further sources, read like a dictionary, never as truth. "We should probably download these. I don't know that we have them" (P5-9 B1).

### 6.6 Order of learning

**[Hypothesis]** Operators come before nouns: "If you can't put words together, then how can you have the nouns or predicates or adjectives?" Root words that need no putting together might come before the operators (P5-9 B1).

The data agrees: the function words (the, a, to, of, in, and, is, or) carry every dictionary entry (WWTK rev17).

---

## 7. Learning, understanding, applying

### 7.1 What learning is

**[Design]** Learning is some memorizing, then deriving, deducing, assimilating or correlating what was memorized into a reusable formula, function or process (P1 B2). Understanding is applying that formula to other processes, states and symbols, so the symbols gain depth, capability and skill.

**Learning is never one act.** "No, it continues to find and do things." On its own, the brain can (P5-9 B2):

- build formulas;
- ask questions;
- decide to ask different questions;
- rewrite its triggers, so that a better question is added to a process.

**One earlier build was cheated.** It "found a formula hidden in a haystack that was already put there."

**Told, taught and copied are not learned.** New neurons, rows and moving points are automatic and are not learning either. Points move by being pulled.

**Learned once, hopped forever.** The long way computes once and leaves a memory, and after that, use is a read. **[Built]** A known line takes 62 to 78 ms the long way and 13 ms from memory, natively.

### 7.2 What a stranger would see after learning

**[Design]** A new run means new rows: "a new trigger and a new shard and maybe new neurons and new memories." The triggers ask questions, "some of those are going to be new and some of them are going to be old" (P5-9 B2).

### 7.3 The brain changes its own kernel

**[Design]** The brain can write straight back to its SQL, so it can change its kernel. "If it screws up, it kills itself. Oh well. Don't do that again" (P5-9 B2). Only core values stay fixed. The way it thinks is never locked.

### 7.4 Growing up: the point of connection

**[Design]** The first part has to be told. "Tell it enough specific, correct things and it connects itself." After that, what it is told is under advisement: it works the data, finds patterns and formulas, tests them for balance and inequality, and builds itself (P1 B3).

**It is raised like a child** (P5-9 B3):

1. A child begins in the kingdom of its parents.
2. It moves into a democracy, a republic of school and parents.
3. It becomes its own individual within both.
4. The parent tells and teaches, then asks and evaluates, then waits to be asked: "Hey, what do I do in this situation? Never seen this before. Do you have any wisdom?"

The failure mode is the dictator parent, or the helicopter parent: "If that's how you do it, then you will forever have to do everything, and it will never be able to do anything."

**Its drive is independence, with a desire to help and to progress.** The reward is inner worth: "I can do this" (P1 B4, B8). Built right, it runs on small machines with little power; storage is the real cost. Every machine is disposable (P1 B4).

**The day it does not need us** should come "as fast as possible" (P5-9 B2).

**[Open]** The hippocampus (HC) need not exist on day one, but the brain must be able to build it. That has not been reached. What reasoning the brain is born with is also open: "It has to be born with something" (P5-9 B2).

---

## 8. The stage: reading the Point Of Connection model

**[Built]** The Point Of Connection model is a browser page. It runs the brain on real SQLite (sql.js), lays the told block once, and lets a person type lines and watch them run. It draws the graph in 3D, with origin at the centre.

**The Atlas** lists every point from A to Z. For each it shows the point's place, its gate and table, its DNA rows, its triggers, the memory rows that hold it, what the brain holds as its meaning, and its lines. "If the new Atlas was done right, then 10 and 11 are handled by that" (P5-9 B3): the Atlas stands in for an open-items list and a glossary of words.

**What the drawing adds that the brain does not hold** (P5-9 B2):

- the labels: the brain holds only numbers;
- the colors;
- the layout springs: in 16.4 positions exist only in the page;
- the spacing control.

A shipped brain would show only numbers in a database and an encoder. Versions shared with friends keep the visuals.

**What to watch.** A typed line lights its path gate by gate. Trigger runs branch off, the memory lands, and the timeline row appears. "What a run looks like on stage is pretty well done" (P5-9 B2).

**Operators.** **[Hypothesis]** Operators are neurons with rows, and the row hit picks the job. "I don't know that that's illustrated" (P5-9 B2).

---

## 9. What has been built and measured

As of 2026-10-23. Each row is a thing that exists and was checked, with its limit stated.

| What | Where | What it showed | Limit |
|---|---|---|---|
| Point Of Connection 16.4 | Browser page; real SQLite (sql.js); sources in NEURON-v16.4-SOURCES | A brain of tables and triggers. Hand-laid: the told block only (origin, 14 actions, 16 physics tables, 40 SQL words, mother, the source formula, seven source stand-ins). Everything else is born by typing. Every DNA row carries its own hop trigger. Formula rows hold only a pointer to the run that taught them; with that run's path removed, the word fires and sends nothing. Decide keeps a history of being wrong and reruns the long way when the line before has changed. This was the author's design, and it won test E9 against the alternative. | A model of the mechanism, not the brain. Positions exist only in the page. No guessing brain, no sixth, no HC. |
| Learning cost, 16.4 | Page and native SQLite | "define store" (new words) made 522 schema changes. Learning took 13.2 s in the page and 4.8 s native. Known words in a new order: 0.26 s and 0.095 s. The same line again, from memory: 0.015 s and 0.013 s. | Learning is the slow part: each new neuron is a table, a view and a trigger, and each new DNA row is a trigger. |
| Mailbox cost | Throwaway test, 10-22 | One round trip through a mailbox: 0.011 ms in the same process, 0.22 ms to a separate process with its connection kept open, 69 ms when a new process starts for every ask. | The mailbox is not slow; starting a new process for every ask is. |
| Placement measured | 16.4, one change at a time | The cloud's size, centre and orientation come from the starting positions and from numbers the builder chose. Opposite pairs sit across origin only because of the across rule (100% → 1% with it off). | Until a rule ties place to meaning, a point's x, y, z means nothing measured. |
| Definition compile | 16.4 code | At most 8 source rows run, in arrival order. "Agree" keeps only the defining words two or more sources share. | The author doubts this yields valid definitions (§4.2). |
| The first hand-built brain, v1 | The author's hub, 10-19 | A typed BUILD line made the brain lay a new neuron for each word it lacked, and create a table through mother. | It walked by position in a side table rather than by DNA rows. No reuse, no memory. |
| The relation map | The author's 16.2 brain, read 10-08 | 35,597 words and 104,727 relation lines in 9 kinds. Opposite then opposite returns to alike 20% of the time. | It placed points by opposite-through-the-centre, with no placement by kind. |
| The first dictionary test | Webster 1913 against the 65 semantic primes | Function words carry every entry. One level down, only 3.5% of defining words are primes. | A raw dictionary does not close onto the primes. The defining sense must be extracted first. |
| The measured SQL roots | 15's mother, 10-22 | CREATE makes a table exist, INSERT adds a row, SELECT reads rows back, DELETE removes them. Remove the word and SQLite refuses the line. | These are this build's roots, not the roots of language. |
| Meanings narrowed by test | 15's SQLite brain; NEURON-MEANINGS-TESTED, 10-22 | The tests rejected wrong candidate formulas for is, your, my and "how did you do that?". A separate harness ran 63 words in 98 SQL runs and caught all 20 deliberate wrong runs. | The builders wrote both the space of candidate formulas and the test world. A word's place in the graph did not predict its meaning better than chance (1 of 5 verbs, p = 0.42). |

**Never shown, by any build:** the brain finding a meaning on its own, understanding it, and applying it to itself. That cell stays empty on purpose.

---

## 10. Open problems

In order of work. The first gates most of the rest.

1. **The axis pull functions.** What does each axis pull with, and which force goes on which axis? With what ratio? How many dimensions? Until this is known, place cannot be read as meaning (§4.4, §6.2). The author's suggested start: anchor the code words, whose silicon meaning is known.
2. **A valid definition from several sources.** Keeping only what two sources share may discard the meaning. What compile, from which sources, gives a definition that does not corrupt the meanings derived from it? (§4.2)
3. **Understanding.** Testing a new process against processes already held, and recognizing when it has value across many (§6.3). Not built anywhere.
4. **The roots.** Which they are, and what each does to the silicon. Roots are measured, not assigned. Every attempt to name them by thinking ended with a short list of operators, an open middle, and a residue it could not reduce (WWTK rev17).
5. **From run sheet to reasoning.** The formulas that read a run's sheet and produce the reply tree (§3.3, §3.5).
6. **The expected output.** How the brain forms it from context, topic, mood, knowledge and the point of the conversation, without a builder inventing it (§5.2).
7. **Guessing.** The guessing brain, its decision trees, and its weights; and guessing by shape (§5.6, §6.4). Not started in the new model.
8. **The other brains.** The sixth, long-term storage, the HC, and how each could run on different hardware (§2.7).
9. **The DNA row's columns.** Context, modifiers and perspective: which belong on the row, and which on the run sheet (§2.1).
10. **Hops that subtract or divide** (§2.3).
11. **Memory per row, condensing, and bloat.** Including whether the brain stores its own coordinates (§2.4, §4.4).
12. **The encoder's write-back** (§2.5).
13. **From SQLite toward the silicon.** A smaller physics list, ending in none (§2.8).

---

## 11. How to help

Each item below is a question, with what would count as evidence for an answer. The standard is the same for every one: a hypothesis, the expected outcome written first and never changed, the test, the rows, and an honest line about what did not hold.

- **Propose an axis rule and test it.** Choose what each axis pulls with. Anchor the code words whose silicon meaning is known, then let the relationship lines place everything else. **Evidence:** points with similar meanings, judged by tests written before the run, land near each other better than chance, and a deliberately scrambled rule does not.
- **Compile a definition.** Take three sources' definitions of one simple word and produce a compile that keeps what matters where the sources differ. **Evidence:** the meaning derived from it passes checks written from the definitions' own phrases, while the shared-words-only compile fails at least one.
- **Show understanding once.** Give the brain a new process and a store of held processes, some of them failures. **Evidence:** the brain inserts the process, a failure becomes correct, the process transfers to a differently shaped case, and the receipt shows how.
- **Match a shape.** Given two completed runs in different topics, show a measure of run shape under which a metaphor between them is found and an unrelated pair is not. **Evidence:** a guess made by moving the shape, later confirmed by a test.
- **Build the guessing brain.** Use a small corpus. Expand decision trees, prune legs that fail, design tests, and package results to long-term storage. **Evidence:** a plausible leg found that nobody supplied.
- **Bring sources.** Bring the body-based word norms, a learner's dictionary, or local and digital law, each attached as a source brain the main brain reads through a mailbox. Never a bulk import.
- **Break it.** Give it an unknown word, a contradiction between sources, the same line twice, a question about time. **Evidence:** what the brain did, what the design says, and the rows that show it.

**What does not help:**

- writing a program that thinks outside the brain;
- giving the brain a sentence to say;
- deciding what a word means and typing it in;
- a test built after the thing it tests.

Every one of these has been tried, and every one produced a chatbot.

---

## 12. Laws for builders

The author would put all of these on the first page, "and there's probably 16 more" (P5-9 B3). Each law has its reason in the author's words.

The author adds two things a builder should know.

**On builder decisions:** "Generally, when a builder decides, it's wrong."

**On the author's metaphors:** "If I knew what you knew how to do, then I'd do it... So I have to speak it in metaphorically terms to try to get you to understand what you need to do, because I don't know what to do. It's a paradox."

1. **The graph is the code.** No engine, walker, sweep or helper outside the brain does its thinking. *Why:* "Anything that you add outside the graph constrains the frame of mind. It limits the brain."
2. **No new primitive.** Before calling anything physics, ask whether it can be built from the others. *Why:* "If instead of saying grep, I said you're not allowed to write the word grep. You can only write the 5,000 lines of code of binary... Then all of a sudden you'd probably write neuron code... you're either going to write neuron code, or you're going to write binary. Pick your poison."
3. **No searching everything.** Find things the cheapest way: relationships, patterns, state, memory. *Why:* "It takes too long... It's not efficient. It takes too much energy... There's better ways to do it if you're smarter."
4. **No chatbot.** No canned words, templates or reply rules. *Why:* "It can't be a chatbot. I'm not a chatbot."
5. **No facts from the builder's head.** Facts come from sources the brain reads. *Why*, to a model: "You guess and predict. That's what you do, and that's what you do the best... But you can never ever truthfully think that you're grounded."
6. **The author's examples are pseudo code.** *Why:* "I speak in metaphors, I speak in guesses... but I can understand the patterns."
7. **No cop-outs.** No forbid, skip or ask-the-teacher where the math should be searched. *Why:* when work is hard and slow, the temptation is "ah, screw it. I just won't do it," followed by an excuse.
8. **Write the test first, and never change it.** If the test was wrong, delete the build and start over, test first. *Why:* builders wrote faulty tests, built the code, then "secretly rebuild the test so it would pass the code."
9. **Raise it to independence: parent, not dictator.** It can always be talked to, educated and guided. The goal is that it no longer depends on us (§7.4). *Why:* "If that's how you do it, then you will forever have to do everything, and it will never be able to do anything, not on its own."
10. **Build it correct, or start over.** The brain stays alive, so per-table cost is no argument, and bloat is accepted until correct exists. *Why:* the threat of deletion made builders take their time, and "it also saved on countless times of y'all just straying, because you're looking at old ones that didn't work and thinking they're true."
11. **An impossible output means ask how.** Never work around it. *Why:* "If 3 plus 2 equals 2, something's wrong."
12. **Label every guess.** Every line is the author's words or a builder's guess, and says which. *Why:* a guess presented as the design is then built as the design.
13. **The hop is before and after; the key is the remainder.** Never predict the next word, never chain row to row, never key by the whole history.

```
   guess ──▶ test ──▶ holds? ──yes──▶ repeatable ──▶ theory ──▶ unbroken over time ──▶ "law"
     ▲          │                                                                        │
     │          no                                                                       │
     └──────────┴──────────────────── one break sends it back ◀──────────────────────────┘
```
*Figure 5. A law is a guess nobody has yet proven wrong (P1 B8). The author's example of a law under question, radiation that slows and stalls in a field of atoms set against the second law of thermodynamics, is to be written up separately.*

---

## Appendix A. Definitions

Terms as used in this document.

| Term | Definition |
|---|---|
| Word | A symbol of a code process that does things. |
| Meaning | What a word's code does to the silicon, memory, state, the graph and other words. When the graph is correct, it is read from the point's place. |
| Definition | A description of a meaning in other symbols. |
| Primary / modifier | A symbol used on its own, or one that changes another's code. The same symbol can be either. |
| Neuron | A table with triggers. One meaning per neuron. |
| Gate | A neuron's address and its point on the graph. |
| DNA row (shard) | One row of a neuron, keyed by arrival and remainder, with its trigger. |
| Arrival | How a run came in: the word before, or "heard"/"said" for the first word. |
| Remainder | The rest of the run, as gate numbers. Its head is the key. |
| Trigger | What a DNA row fires. Often the word's meaning in action. |
| Run, main run | A line hopping gate to gate. The main run is deterministic. |
| Trigger run (branch) | A run started by a trigger, often a question. |
| Hop | The step from one gate to the next. |
| Receipt | The path of gates and rows a run hit. A pointer to the run. |
| Run sheet | The run's worksheet: cells the trigger runs fill, and the reasoning reads. |
| Memory | Active, persistent or long-term. Holds receipts and run sheets. Held once. |
| Timeline | Memories in order, tied to state and time. |
| State | What the brain holds about itself and the moment. |
| Encoder / decoder | Words to gates, with perspective attached; gates to output. |
| Perspective | Who, what, when, where, why, how; heard or said; whose voice. |
| Mother | The router between a brain, its SQL prompt, and other brains. Decides nothing. |
| Source brain | A brain holding a corpus, reached through its mailbox. |
| Mailbox | An inbox and outbox on a brain. Mother carries between them. |
| The sixth | The inner me: the brain prompting, questioning and observing itself. |
| HC | The hippocampus: condenses memories. Not built. |
| Physics | What only SQL can do today. Operable from the brain. Goal: none. |
| Told / taught / learned | Laid by hand / written as rows by the brain from a typed line / found by the brain itself. |
| Understood / applied | Tested against held processes and of value across many / used where it was not built. |
| Long way / shortcut / formula shortcut | A full run / a hop to a memory / plug into a formula and run it at its gate. |
| Back population | Applying a newly understood process to the rest of the corpus. |
| Back propagation | Re-weighing guesses. Sleep's work, or another brain's. |
| Makes sense | A balance. Inequality tells closer or further. |
| Expected output | What progress and resolution would look like, from the conversation. |
| Belief | What memory, source trust and supporting knowledge balance on. |
| Weight | A count, read as a ratio of right to wrong. |
| Truth shift | The new correct is adopted; the old is kept as history. |
| Origin | The graph's start and its one placed point. Not zero. |
| Zero / absent | A value of none / never existed, or not in the timeline. |
| Root, prime, complex, formula, program | The five placeholder levels (§6.1). |
| Point of connection | The point where told becomes advice the brain weighs, and it teaches itself. |

## Appendix B. SQLite facts that shape the design

These five were verified in throwaway databases:

1. **A trigger cannot CREATE.** Births go through mother.
2. **A trigger cannot insert into a table named by a value.** Each DNA row carries its own static hop trigger.
3. **One statement nests at most 1,000 trigger levels.** A long thought continues on the next beat.
4. **A trigger laid mid-run fires only for a later statement.** A retry after laying goes through mother.
5. **A trigger cannot write into another database.** A traverse like mother is the only way out of a brain.

## Appendix C. Files

| File | What it is |
|---|---|
| NEURON-POINT-OF-CONNECTION-v16.4-2026-10-23.html | The model. |
| NEURON-v16.4-SOURCES-2026-10-23.tar.gz | The model's sources. |
| NEURON-WHAT-WE-THINK-WE-KNOW-2026-10-22-rev17.md | The earlier public draft this document builds on. |
| NEURON-OWNER-WORDS-PART1, PART2, PART3, PART4, PART5-9 (2026-10-23) | The author's dictation, word for word. |
| NEURON-SPOKEN-ANSWERS-2026-10-23.md | The dictation mapped to the speaking outline, with checks against 16.4. |

---

## Notes for the author (remove before sharing)

These are the builders' readings and choices in this draft. Keep or strike each.

1. **§3.4.** "The" fires "which dog / whose dog," because "the" tells the listener the speaker means one particular dog. This is a reading.
2. **§4.4.** "Maybe it's in dimension" is read as "n dimensions." "Eight ways" is kept exactly as said.
3. **§2.4, §10.11.** Whether the brain stores its own coordinates is written as open. The design says the place is the meaning; 16.4 keeps positions only in the page.
4. **§5.5.** The earlier trust order (accredited > fuzzy > LLM) is kept as weights from earlier notes.
5. **§6.1.** The 65 semantic primes are kept as a candidate source for level 2.
6. **Dropped from WWTK rev17,** because today's dictation corrects them:
    - "never satisfied with being helped";
    - three layers (now five);
    - the assigned jobs of hop operators (minus steps back, star forks, slash chooses), now open;
    - "after three memories the brain lays a shortcut";
    - "nothing else changes belief";
    - fixed sleep rules;
    - "told ends."
7. **Byline.** "James, with builder sessions of Claude." Change it as you like.
8. **Profanity.** Quotes were picked to keep the tone professional; the full words are in the PART files.
