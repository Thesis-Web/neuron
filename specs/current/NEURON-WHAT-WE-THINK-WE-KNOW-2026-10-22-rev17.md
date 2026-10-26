# Neuron: What We Think We Know

Oct 22, 2026 · @James

## What Neuron is, in one page

Neuron is a computer that builds itself and talks to itself, made of database nodes we call neurons, and meant to reason, understand and learn on its own. It is not a chatbot and not a language model. It is a graph that runs language as code.

It has three parts. **Code**: it performs the actions that the meanings of words stand for. **Math**: problem solving, which gives it reasoning. **Language**: a graph of the root meanings under every human language, so any language can be laid on it without the brain changing.

The idea underneath all of it is one claim: a human word is shorthand code. Its meaning is the action it causes. A definition only describes that action. We lost the roots over the history of language, because shorthand was described with more shorthand, and that is why meanings are hard to find and definitions are easy.

It learns slowly. Once it understands something, it runs almost like a deterministic function. On the surface that looks like a chatbot. Underneath, many runs in parallel turn determinism into cognition using very little energy, by asking itself questions about its own state, history and memories, and by checking sources.

It starts from a small hand-laid base, the physics, because a thing cannot learn until it can learn. After that nobody writes code for it. It writes its own, by running. Today the physics sits on SQLite, which we treat as a crutch: the closer the kernel gets to the silicon, the less fluff between the brain and the machine, and the faster and cheaper it runs.

Why build it: the systems we tried before could not take in information fast enough and judge whether it was true or contradictory. Neuron's goal is to become smarter and more efficient on its own, never satisfied with being helped, asking for help only when it cannot do the thing itself.

## The claim about words

A word is a symbol for the code behind it. The letters, and how they are arranged, mean nothing; if they did, the world would have one language. What the symbol stands for is what it makes happen, and that is its meaning.

Take grep. The word is the symbol. Its definition is a description: take a pattern and a place to look; read the place one line at a time; compare each line with the pattern; say out the lines that balance; end when the place runs out. That describes grep. It is not grep. grep's meaning is the five thousand lines of C that the machine actually runs. Add a modifier, a flag, and the code behaves differently. Language works the same way: the words around a word change what its code does.

So a definition and a meaning are two different things. A definition describes a meaning using other symbols. A meaning is what the code does. Every dictionary ever written holds definitions, which is why dictionaries have never produced a machine that understands.

In Neuron, what the code does has several targets at once, in some ratio that differs by word and by context:

- **The silicon.** The physical actions the machine performs: read, write, compare, find, split, join, add, subtract, move, the clock, hear, say, call out. The simplest words, which we call roots, are nearly pure silicon. In the current build those are SQL words: CREATE, INSERT, SELECT.
- **The graph.** New gates, new DNA rows, new relationships, a point that moves.
- **Memory, state and time.** What is remembered, what the brain holds about itself and the moment, the timeline.
- **Questions.** Most words make the brain ask itself something: have I seen this, is it like that, what is it the opposite of, who is this about. The questions are where reasoning starts.
- **Other words.** A word's code is built from other words' code, down through levels until it reaches the silicon. A complicated word, meaning, learning, love, may stand on sheets of code five or six levels deep.

That last point is the whole method. A word's meaning is only right if the meanings behind it are right, all the way back to the roots. Nothing can be picked and declared. Every meaning has to be derived upward from the roots, or it is a guess wearing a label.

## Roots, primes, words: the three layers

Meanings are built in layers, and the order matters.

1. **Roots.** The bottom. Actions the silicon really performs, and a small number of root meanings that the next layer seems to be made from. The roots are not known yet. Every published attempt to name them by thinking ended with a short list of operators, an open middle layer, and a residue it could not reduce. Our position is that roots are measured, not assigned: the words everything else leans on, found by counting in real sources and by testing what combining them does.
2. **Primes.** The 65 meanings found in every human language, a list that linguists have held stable for years: I, you, someone, something, this, the same, other, one, two, some, all, good, bad, big, small, think, know, want, feel, see, hear, say, do, happen, move, be, there is, live, die, when, now, before, after, where, here, above, below, far, near, not, maybe, can, because, if, very, more, like, and the rest. Each prime is a formula of roots. Some are plainly combinations: nothing is none plus thing.
3. **Words.** Everything else is a formula of primes and other words. Some are short. Some are enormous. Some have several formulas that are each right in a different context, the way one shell command behaves differently depending on where it sits in a pipeline.

Two more things sit across the layers.

**Operators.** Words that change another word's code rather than adding their own. Minus flips it. Plus gives more. Slash takes a part. Star joins. Tense, number and affixes are small fixed steps: walked stays beside walk. Relation words, like, opposite, kind, same, different, are operators too. The same operator can do different jobs depending on the row it is hit on; which job is the row's to carry, and the brain has to find it by test.

**Modifiers.** The other words in the sentence. Who is, who are, who did and who was each fire a different row inside the one neuron for who, and each row points at a different formula: a different place to look, a different thing to read, a different thing to say.

What we have on paper is a worksheet of guesses: die as minus live, before as minus now, below as minus above. We mark them guesses. Two of the eight have held up under test so far; three failed; three were the wrong kind of thing. That is the expected outcome of a worksheet, and it is why nothing on it is laid into the brain as truth.

## The graph: gates, DNA, triggers, runs

The brain is a database of individual neurons, not one big table. Each neuron is its own table. Its name is its gate, the address a run enters by. Its rows are its DNA. Each DNA row holds how a run arrived (the gate before), the remainder (the gate after), a trigger column, and a count of how many times it has been hit. There is nothing else in a neuron.

A run is a typed line encoded into gate numbers. It lands on the first gate. That landing fires the table's trigger, and the trigger does three things: it looks for the DNA row that matches how the run arrived and what comes next; if the row exists it counts it and the row's own hop trigger lands the run in the next gate; if the row does not exist, the row is laid, with its hop trigger, and the run goes on. Nothing outside the database runs during this. There is no program walking the steps. The input string runs, and running it is what fires the triggers.

The trigger column on a row is where thinking starts. A row can point at another neuron, and when the row is hit, a second run begins there and runs beside the first. The main run keeps going. Those branch runs are the questions: is this like that, have I seen this, who is this about. One input can start fifty of them. Every one of them is made of the same thing as the main run: rows in neuron tables.

The hop between two gates is a plus by default, continue. A hop can carry another operator. A minus steps the run back a gate so the next word is hit from an earlier arrival, a different row. A star forks a test run beside the main one and compares the two. A slash is a choice between paths. What each operator does on a given row is not assigned by hand; the brain binds it by trial, keeping the job that balances an expected output.

A neuron is born when a remainder has no gate. The brain writes the SQL that makes it, word by word, and hands it to one small function, mother, that runs SQL text. mother is the only thing loaded beside SQLite, and she does no work other than the traverse. The brain cannot change her, so she does only what the brain cannot do for itself: leave its database and come back. She carries the brain's output to the SQL prompt, or to the mailbox of another database, and when that mailbox is populated she carries the reply back in as an input of the run that asked, never as a new run. Not on a timer: populated. The brain decides what goes where and which cell the answer fills; mother only routes. The sources, dictionaries, thesauri, the code's own documentation, the relation map, are databases outside the brain, brain-like in structure, each with a mailbox, and each able to do its own work on its own data, including reaching out to the world to populate itself. Everything else is rows and triggers.

Four facts about SQLite, verified, shape all of this. A trigger cannot create a table, so births go through mother. A trigger cannot insert into a table named by a value, so each DNA row carries its own static hop trigger, laid once. One statement nests at most one thousand trigger levels, so a long thought continues on the next beat. A trigger laid in the middle of a run fires only for a statement started after it, so a retry after laying goes through mother too.

## Brains of brains: mother, mailboxes, and the check

The main brain is cognition: reasoning, problem solving, state, history, time, scope. Other brains sit beside it. Source brains hold a corpus each, a dictionary, a thesaurus, the code's own documentation, and their reasoning is about understanding the ask and answering it from what they hold. Further brains test, guess, form hypotheses, dream and observe. One of them, the sixth, watches the main brain's runs, sparks questions, holds the morals, ethics and checksums that keep it honest, and drives growth: more efficient processes, new formulas, old things done better.

Every brain has a mailbox. When a run needs something from outside, its output leaves through a port, mother carries it into the other brain's inbox, that brain's own trigger does its work at once, and when its outbox is populated mother picks it up, empties it, and carries it back in as a sub-input of the run that asked. Nothing runs on a timer. The brain decides what goes where and which cell the answer fills; mother only routes. A brain cannot do this traverse itself: SQLite will not let a trigger write into another database.

What comes back is checked before it is used, with three questions. Is this the data I asked for? Dictionaries answer with neighbours: asked for "as", Webster 1913 sends "So" first, and Merriam-Webster sends arsenic and an abbreviation. Is it the data I needed? It must fill the cell the run opened, and when the run ends, a wrong output marks every return it used as suspect. Did I ask wrong? An empty reply opens that question, and the run steps back to the neuron that fired and takes another row if it has one. A source that never answers leaves the cell waiting, and the run knows it is waiting.

Two cautions about the sixth, from the rules this project already keeps. It should reach the main brain only through mother and mailboxes, so every change it makes is a row the brain can see and walk back. And whatever SQL it writes into the main brain is told, not learned: the line between correcting a brain and doing its thinking for it is exactly where earlier builds went wrong.

## Memory, receipts, the timeline, state

When a run has no remainder left it ends, and ending writes a memory. The memory holds the receipt: the exact path the run took, every gate and every DNA row it hit, in order. A receipt is small, a pointer, so a memory is held once and pointed at from wherever it is needed. The same run again is the same row with a new time stamp and a count, never a second copy. The brain needs to know done a lot and correct, not the exact number.

Before a memory is written, the proposed output goes through a balance check we call makes sense. It is set against the previous output for the same receipt, and against an expected output when a person gave one. Balanced, it ships. Not balanced, the run steps back to the decision that picked this path and takes a different row, and the failed try stays in memory marked wrong. That is how the brain finds where it went off, and why the long way is never thrown away: a shortcut whose receipt cannot be walked back is a shortcut that cannot be corrected.

A truth shift is a memory whose answer changed. The old row is ended, not erased, and the new row records what was held true and what is true now.

The timeline is a row per run that ends: time, receipt, memory. It is what lets the brain say I did this on Wednesday, this last week, this seven months ago. State is a small table of rows the brain holds about itself and the moment: now, the last line, and what it has been told it is.

Two more things about memory that matter to the design. Heard is not said. A typed line's first row arrives from heard. The brain's own words fed back to its ear arrive from said, a different row in the same neuron, and I and you swap when a formula looks in state. And fresh memories are exact, while old ones are meant to condense to highlights that can rebuild the run. That condensing, the hippocampus, is not built yet. It does not have to exist on day one, but the brain must be able to build it itself.

## Told, taught, learned, automated: the point of connection

A human baby is born able to breathe, swallow, cry and keep warm, and almost nothing else. Everything else is done for it until it can do it on its own, and then nobody does it for it ever again. The brain's development is a degressive formula: hand-laid at first, then self-done, one function at a time. The point of connection is when nothing is left on the hand-laid list that the brain cannot do for itself.

Four words carry that arc, and they are not the same word.

- **Told.** Hand-laid, once, as SQL. The physics: fourteen physical actions, sixteen tables with their triggers (input, encoder, decide, lay, born, source, agree, end, sense, memory, timeline, say, BUILD, formula, var, state), and the one function mother, who only traverses. These cannot be born, because a trigger cannot create a table. They are laid as one block, with nothing firing, and the brain can rewrite how it thinks on top of them. Exactly this, and not one thing more.
- **Taught.** A line typed to the brain that it writes as rows itself: a word's formula, a DNA row with its trigger column filled, a task with an expected output. The person types; the brain lays.
- **Learned.** The brain finds a formula on its own and makes it run. New neurons, new rows and moving points are not learning; they happen by themselves. After three memories of the same receipt, the brain lays a shortcut.
- **Automated.** From then on the thing is a hop. Use is cheap; learning was the compute.

Two more words sit between learned and automated and matter as much. **Understood** means what was learned balances with its sources and its memories, and worked on a use it had not seen. **Applied** means it ran somewhere it was not built for: in a new sentence, inside another meaning, or in the brain's own processes.

The trap in all of this is the start. Early on, much must be told, and told things are memorized, not learned. The whole discipline is that the told base has to lead directly to the brain asking itself who, what, when, where, why and how, checking its timeline and its memories, and from there deriving, deducing and applying on its own. A told base that does not lead there is a program with a vocabulary.

## The method: hypotheses that expect to be wrong

Everything in this document is a hypothesis. Nothing here is treated as truth, including the owner's own words, which are the shape of the idea and not its formulas.

The method is the one a person uses to find out, not the one a machine uses to confirm. Form a guess. Test it fully expecting it to be wrong. Look for the small part that held, label that part progress, and test again. Over time the parts that keep holding form a pattern, and the pattern becomes a belief: not a truth, the most correct thing to the current state of knowledge, open to being shown wrong at any moment and adjusted. A belief that cannot be shown wrong is not held here.

That is the opposite of building a test after the output and proving the output right. Expected outputs come first, written from the words of the spec, and only then is the thing built and run against them. A test that cannot fail is not a test.

The same rule reaches the tools. A large language model is a very good guesser. It predicts what usually comes next, and Neuron is built to be what does not usually come next, so every default an LLM reaches for is a trap: a program outside the brain, a template, a side table, a first sense, a sweep, a stub that looks like the part. The rule for the LLM in this work is therefore narrow: it may write the first physics, run tests, measure, and report what the data showed and what it did not. It may never assign a word a meaning, never lay a fact or relationship from its own head, never treat a worksheet guess as a root, and never call a thing done that only partly works.

The larger bet behind the method is this. Today the question everyone asks of language models is how to stop them from drifting, inventing and hallucinating. If Neuron is built correctly, the question flips: how do we get a model to drift, invent and hallucinate in the specific ways a grounded brain finds useful. The brain holds the known, the sources, the memories and the balance. The model supplies the guesses. Each does what it is good at, the corpus the brain needs is a fraction of a model's, and the energy falls with it.

## What has been built and measured so far

As of 2026-10-22. Each line below is a thing that exists and was checked, with its limit stated.

| What | Where | What it showed | Limit |
| --- | --- | --- | --- |
| A hand-built brain, v1: one SQLite table per neuron, a Python shell that only writes a typed line and prints the answer, one C function (mother) that runs SQL text | the owner's hub, Oct 19 | A typed BUILD line made the brain lay new neurons for every word it did not have, and create a table through mother | The walk was by position in a side table, not by DNA rows; no reuse; no memory. Audited and listed for correction |
| Four SQLite facts, verified in a throwaway database | this session, Oct 21 | A trigger cannot CREATE; a trigger cannot insert into a table named by a value; one statement nests 1,000 trigger levels; a trigger laid mid-run fires only for a later statement | These fix where mother is needed and nowhere else |
| The relation map | the owner's 16.2 brain, read Oct 8 | 35,597 words, 104,727 relation lines in 9 kinds, 16,398 words placed by expressions over 5,992 roots; opposite then opposite returns to alike 20% of the time; alike then kind lands on kind 36% | Placement by opposite-through-the-center and no placement by kind; the map's own errors show (small placed from great; kind the gentle sense) |
| A simulator of the brain as rows and triggers | Point Of Connection pages: 13.1, 14 and 15, each kept unchanged beside the next, so they can be compared | Starts with only the hand-laid base; typed lines run one landing per tick; shows every row laid, every gap, every physical action. In 14: mother runs real SQLite in the browser; a word's formula is a row in the brain's formula table and holds the SQL itself; what a run sends out leaves through a port to mother and comes back through another as a sub-input; every return is checked; a failed ask steps back to another row; a word's meaning is measured by running a line with and without it, counting lines answered from memory | In 14 the sixteen physics tables played their triggers in JavaScript. In 15 they are real SQLite tables and triggers: 377 statements, 44 checks, each with a control that must fail when the thing it credits is removed. It is a model of the mechanism, not the brain. 48 checks pass in 14, each written before the build from the owner's words, 8 of them controls that remove what a check credits |
| Seven source brains, each its own database with a mailbox | fetched Oct 22 for 163 words, plus English "as" with each entry's own headword, plus the SQLite docs | WordNet 3.0, Webster 1913, Moby, Merriam-Webster Collegiate and Thesaurus, the owner's relation map, and the SQLite docs for the SQL words. The brain asks only the ones its source formula names. Asked for "as", the sources sent back other words too: So, As (arsenic, an ace, a Roman weight), AS, as-, "as far as". The check sets those aside | Stand-ins: a page cannot call sources itself. The real source brains would live on the owner's machines and fetch for themselves |
| The first dictionary test | Webster 1913, the 65 primes | Function words carry every entry (the, a, to, or, and, of, in, as, is, not); the load-bearing primes by the dictionary's own use are not, be, this, one, all, other, you, some, place, more, like, part, time, thing, same, do, now, good, there, if, can; one level down only 3.5% of defining words are primes | A raw dictionary does not close onto the primes; its entries are examples and etymology; the defining sense must be extracted first |
| The measured roots | the simulator's mother, Oct 22 | CREATE makes a table exist; INSERT adds a row; SELECT reads rows and says them back; DELETE removes rows; remove the word and mother refuses the line | These are the SQL roots of this build, measured, not the roots of language |
| Meanings narrowed by tests | the real SQLite brain of page 15, Oct 22 | Every assignment of 18 small formulas, built only from what a run holds, was tried against sentences in the owner's shape ("what is your name ?"); the tests threw out the wrong ones. is: write what follows under the key built before it, only if one was built. your, my: set the key's owner, the other one or the speaker; this is decided only once the brain holds its own name before anything is said. "How did you do that ?": the brain answers from its own record of the statements it ran | The space of formulas is the builder's; which word carries "how" is not decided; a repeated context question is answered from stale memory; a word's place in the graph did not predict its meaning better than chance (1 of 5 verbs, p = 0.42) |
| A separate harness by another session | NEURON-MEANINGS-TESTED, Oct 22 | 63 words, 98 SQL runs on an invented world, 78 passing their written checks, 20 deliberate wrong runs all caught | The runs and the world were the builder's hand; a run is right only if the meanings behind it are right to the roots. Its method stands; its meanings do not |

Three experiments from the night of 2026-10-22 shape what comes next. AS in SQL is not a syntax mark: in CAST, in CREATE TABLE ... AS SELECT and in WITH, removing it makes SQLite refuse the line; in a column alias SQLite does not need it, and the reader does. A brain's trigger cannot write into another database (SQLite: "qualified table names are not allowed on INSERT, UPDATE, and DELETE statements within triggers"), so a traverse like mother is the only way out of a brain. And a round trip through a mailbox costs 0.011 ms in the same process, 0.22 ms to a separate process with its connection kept open, and 69 ms when a new process is started per ask: the mailbox is not slow; starting something per ask is.

What has never been shown, in any build, by anyone: the brain finding a meaning on its own, understanding it, and applying it to itself. That line is empty on purpose.

## What is not solved

Stated plainly, because the whole project turns on these and not on what is built.

1. **The roots are not known.** Not the list, and not what each one does to the silicon. Counting shows which words everything leans on; it does not show what they do. Finding that needs tests: combine candidates with the operators inside the brain and read what the rows do.
2. **Nobody knows how to derive a meaning from a definition.** A definition is a description in other symbols. Turning it into a run whose every leaf fires the silicon, and knowing that the run is right, is the open problem. Every attempt so far either assigned the run by hand or pointed at words in the description and called them the meaning. Both are the same mistake.
3. **The brain cannot yet find, read, reason over and ingest what it needs from its sources.** It can find and read. It can count what sources agree on. It cannot yet reason over what it read.
4. **Everything is told or taught.** No build has produced a meaning the brain found, understood and applied. That is the measure of success and it has never been met.
5. **The question words are untested.** Who, what, when, where, why, how, and the being words is, are, was, and helpers like the and a, have never had a meaning hypothesized as a run and tested. They are the words every definition leans on, which makes them first.
6. **Learning, applying, and growing are not built.** The brain must learn on its own, apply a discovery to other objects in the graph, notice when a new process makes an old one more efficient or more correct, and accumulate what it learns to build itself further. All of this hangs on the meanings of the code-word symbols and how they change in context.
7. **The hippocampus and long-term memory do not exist.** Condensing memories to highlights that can rebuild a run is designed and not built.
8. **Parallelism is a sketch.** A branch run is the unit that could go to another core: reasoning here, gathering there, memory lookups elsewhere. The simulator counts how many runs were open at once; nothing runs them side by side.
9. **SQL is a crutch.** It is what is under the brain now. The kernel should close toward the silicon as the brain learns to write it, and nobody knows that path yet.

None of these are reasons to stop. They are the order of work. The first three gate the rest.

## How to help

The project needs people who can hold a question without needing it to come out a particular way. Here are the questions, and what would count as evidence for each.

- **Find the roots by test, not by thought.** Take a candidate set of root actions (the physical ones are known: read, write, compare, find, split, join, add, subtract, move, clock, hear, say, call out, spawn) and a candidate set of root meanings. Combine them with the operators (minus, plus, part, join) and record what each combination does to a small database. Evidence: a combination whose effect, read back from the rows, matches what a prime does in use across many sentences, without anyone having written the match.
- **Say what who does.** Propose, as a run of physical actions over memory and state, what the word who does when a sentence passes it. Then what is, are and was do. Evidence: a set of questions with expected answers, written before the run, that the run gets right and a deliberately wrong run gets wrong.
- **Derive a meaning from a definition.** Take any three-source definition of a simple word and produce a run whose every leaf is a physical action, together with the checks that the run must pass, written from the definition's own phrases. Evidence: the run passes its checks on several different databases, and a run with one line changed fails on the line that names why.
- **Show one act of learning.** Give the brain tasks with expected outputs and no procedure. Evidence: a procedure the brain laid itself, marked derived, that answers a task it had never seen, and the receipt that shows how it got there.
- **Break it.** Give the brain an unknown word, a contradiction between sources, the same line twice, a question about time. Evidence is a finding with three parts: what the brain did, what the design says, and the rows that show it.
- **Build the next source.** Attach a learner's dictionary, or a textbook, as rows the brain reads itself, one word at a time, when a line needs it, and never as a bulk import. Evidence: a word's definition rows arrive only when that word is needed.

What does not help: writing a program that does the thinking outside the brain, giving the brain a sentence to say, deciding what a word means and typing it in, or a test built after the thing it tests. Every one of those has been tried, many times, and every one produced a chatbot.

The standard for any claim is the same: a hypothesis, the expected outcome written first, the test, the rows, and an honest line about what did not hold. If a result cannot be wrong, it is not a result.
