# NEURON BLUEPRINT: turn one

*Written 2026-10-18. It builds on `NEURON-NOW-2026-10-18.md` ("NOW"), which says what Neuron is, and on the owner's own words in `NEURON-NOW-Interview-2026-10-18.md`. This document says how turn one gets built. Where NOW gives no answer, the choice here is the builder's (NOW §17, N2: "do what you think is best"). Every choice is a starting point. After birth, the brain can change any of it except the core values (§15).*

**Where to look:** §0 has three rules that override everything else. §1 has the whole design on one page. §2 settles the ten open items. The rest is the detail a builder needs.

---

## 0. Three rules over everything

When any detail below conflicts with these, the detail is wrong.

1. **Words are nothing; the action is the meaning.** "It's not the word or words, it's the code that the word or words make happen" (owner, 10-18). A definition describes a meaning; it is not the meaning. A gate that does nothing when a run passes it is a word without meaning, which is broken code (law 2).
2. **Learning is compute; using is hops.** Compute is spent once, when something is learned. After that, using it is a hop: a memory, a shortcut, a stored way. The long way runs again only to reason, or when the truth has changed [1098]. That is what keeps the brain cheap to run, and why an idle beat writes nothing.
3. **Know before you guess.** "Guess, but only after you know what you know, only after you check history, memory and state, and source" (owner, 10-18). Guessing is allowed and needed, but it comes last, and it is labeled as a guess (§10.4).

## 1. The whole design on one page

There are four layers, from the bottom up.

1. **The kernel.** Claude writes it, once. It is a small Go program on hp2 that does physics and nothing else. It moves runs from gate to gate, performs the physics words, keeps the brain in RAM and its body on disk, beats the heart, and opens the ports (the talk channel and the sources). It knows no words, no answers, and no rules about meaning.
2. **The physics gates (the rigid layer).** Each physics word has one gate inside the brain. When a run passes that gate, the kernel performs the action on the silicon. These are the only gates bound to code.
3. **The told base.** Claude lays it by hand, in turn one only. It holds:
   - the keyboard keys, the roots, the 65 primes, and zero, one and two;
   - the relationship types, with first-guess formulas;
   - the labels for the early words, and the core values;
   - the born processes: the questions, memory, balance, belief, source checking, guessing, learning, back-population, the HC seed, and the sixth.

   The processes are laid as **strings of gates**, the same kind of thing as a sentence, so the brain can read, run, copy and rewrite them.
4. **The grown brain.** Everything the brain spawns, writes, learns and rewrites after that.

One input, start to finish:

```
words in ─► encoder: labels become gates; who/what/when/where/why/how attached
        ─► main run: hops gate to gate. The head of the remainder picks the shard,
           and the shard holds the way to the next gate.
             └─ the shard's triggers SPLIT off question runs (50 to 100 is normal);
                they never block the main run
                  └─ question runs check memory, sources, relationships and shapes,
                     and LAND what they find on the scratch pad
        ─► the answer is derived on the scratch pad by balance (closer / further / balanced)
        ─► decoder ─► SAY, or an act

run ends   ─► memory (same run = same row with a new time; truth shift = new row) ─► timeline
idle       ─► the sixth picks its own next input from its gaps and imbalances (it talks to itself)
tired or full ─► it asks to sleep ─► the HC condenses, guesses are re-weighed, formulas are searched for
```

## 2. The open items, decided

These are the ten items left open in NOW §18. The owner can overrule any of them before birth.

1. **Core values.** The builder lays them in turn one, taking them from the owner's own laws (§15). The kernel refuses every write to them. A born check runs before every SAY, every act outside the machine, and every change the brain makes to its own processes.
2. **Where a meaning's action lives.** At the bottom, it lives in the physics gates, which are bound to the silicon (the rigid layer). For every other gate, it lives in the DNA: the ways out its shards store and the triggers they excite, picked by how the run arrives. The definition memory describes the action, and the relationships place it in the graph.
3. **The definition schema.** It has nine fixed sections (§6.4). The relationship section fills itself, and the brain may add sections.
4. **Zero vs absent.**
   - **Zero** is a meaning with a gate: gate 0, at the origin (0,0,0) of the graph. It is the point every scale starts from, and its value is 0.
   - **Absent** is neither a gate nor a value. It is "no row". A miss is an event that starts questions.
   - **Nothing** is not zero: nothing = not + thing. (Details in §5.4.)
5. **The second birth memory** is the **birth memory**. It records when the gate was spawned, by which run, from which arrival and remainder, and the state at the time (why the gate was needed). It puts every neuron on the timeline from its first instant.
6. **The reasoning neuron** is the same kind of neuron as every other. Its shards carry many ways out, each one a question, and all of them land on the run's scratch pad. Its process ends with WAIT, then compile (balance).
7. **What starts back-population.** Four events:
   - a formula is kept (learned);
   - the truth shifts;
   - a correction lands;
   - a source diff changes a relationship.

   It runs awake, at once, along receipts, to the shards and memories that relied on what changed, and only those (§10.5).
8. **The heartbeat.** The resting beat is one second, and an idle beat writes nothing (both approved by the owner on 10-06). Under load the beats run back to back. Each beat runs a budget of steps, then commits. The budget and the resting rate are values on a told gate, so the brain can change them.
9. **The channel.** Plain text over a socket on hp2: `neuron talk`, reached from Windows with `ssh hp2 -t neuron talk`. `neuron watch` shows its acts as they happen.
10. **The sixth** sits inside the graph. It is a told process that the heartbeat fires whenever there is spare capacity. It picks its own input from its gaps and imbalances, and feeds it in as a run whose *who* is itself. That is how one outside input becomes many, and how the brain talks to itself. Output still leaves the graph only through SAY.

Also settled: nothing from Cortex carries over (NOW §1).

## 3. Machine and stack

- **Machine: hp2** (Debian 13, 2 cores, 7 GB RAM, 400 GB free, idle, sudo works). Nothing else of the owner's lives on it, so pulling the plug costs nothing. omarchy is the owner's desktop, and its screensaver alone uses more than a core.
- **The brain runs as its own user, `neuron`,** with no sudo and no ssh keys. hp2's own user can sudo, and it can reach the hub through the back tunnel. A runaway brain must not inherit either.
  - **The builder's folder** is `/home/james/neuron-build/`. It holds these documents, `kernel/` (the Go source), `lay/` (the told base, as text) and `DECISIONS.md`. The kernel binary and the lay files are readable by `neuron` but not writable. The brain can read its own kernel, but it can't replace the one that enforces the core values.
  - **The brain's folder** is `/home/neuron/`. It holds `brain.db`, `ports/` (the talk socket), `acts.log`, and `own/` (programs the brain writes itself and runs through CALL).
- **Kernel language: Go** (Debian's golang-go 1.24), built into one small binary. The brain itself runs on one deterministic loop (§7.5). Goroutines are used only for the ports.
- **Storage.**
  - While alive, the brain lives in **RAM**. A gate is an index into an array, and a shard is one map lookup inside its gate. That should be well under the 1–2 µs hops the owner remembers.
  - Its body on disk is **one SQLite file**, `brain.db`. The kernel loads it once at start (the owner approved "LOAD once" on 10-06).
  - Every WRITE goes to RAM, and the changed rows are committed to `brain.db` at the end of each beat.
  - Long-term memories stay on disk and come back when recalled, so the storage tiers match the memory tiers (§9.1).
  - This meets M3: it is cheap, very fast, can recurse and step back and forward, can see patterns, and doesn't bloat as long as the HC does its job.
- **Sources on the machine:**
  - a local dictionary server (`dictd`) with Webster's 1913 (GCIDE), WordNet, FOLDOC (computing) and Elements (chemistry), all from Debian packages;
  - the WordNet database files, for its structured relations;
  - the man pages, which are the benchtop reference for "anything a computer can do".
- **Sources outside:**
  - Merriam-Webster Collegiate and Thesaurus API (this needs the owner's key);
  - Wikipedia and Wiktionary (lower trust);
  - OpenStax textbooks (math, physics, chemistry, biology).
- **LLMs** can be asked but are never grounded (§10).

## 4. The kernel: the only code Claude writes

### 4.1 What it does

1. It holds the brain in RAM and commits the changes to `brain.db` each beat.
2. It steps runs (§7.2). The step is physics, like a CPU fetching its next instruction: it never chooses anything. The shard holds the way, and a miss goes to neuron code.
3. It performs the physics words (§4.3) when a run passes a physics gate.
4. It beats the heart and schedules runs by worth (§12.2).
5. It opens the ports: the talk socket, the dictionary server, the web, files and programs.
6. Its encoder side splits incoming text at spaces and at symbol keys, and looks each piece up in the label index. Each piece goes in as the gate its label points to. A piece with no label goes in as raw text, and the run spawns a gate for it at the hop. The encoder does no language work of its own: no stemming, no spelling correction, no stop words, no grammar.
7. It loads the told base (the lay files) until the builder marks "told ends". After that it refuses every lay file, forever.
8. It refuses every write to a core-value row.

### 4.2 What it never does

- It never knows a word, sentence, answer or reply. The only text that ever leaves is what the decoder reads off gates.
- It never decides. There is no "if the word is X" anywhere; every choice is a shard picked by a run.
- It never sweeps. Inside a run there is no scan of all gates, shards or memories. FIND reaches only by index (§4.3).
- It never computes a learned thing on the brain's behalf. That is the 09-30 trap: an engine outside the brain doing the brain's thinking.
- It doesn't grow. The target is about 1,500 lines. Past 2,000 lines, something that belongs in the graph has leaked into the kernel, and it moves back out.

### 4.3 The physics words

This set is close to the bottom the owner approved on 10-06: read/lay/end/new/index, eq, if/call/again, in/out/clock, tick, commit.

- Each word has one gate in the brain, and passing that gate performs the action.
- The inputs come from the run's scratch pad, and the results go back there.
- A test also puts its outcome gate (yes/no, same/more/less, found/none) at the head of the remainder, so the next shard picks the branch.

| Word | What the silicon does |
|---|---|
| **Run** | |
| GO | Moves this run to a gate, with a given arrival. This is how the miss process resumes a run. |
| SPLIT | Starts a branch run at a gate (a trigger), carrying its subject. The main run keeps going. |
| LAND | Puts a finding on the parent run's scratch pad. |
| WAIT | Holds this run until its branch runs have landed, or until a beat passes. |
| END | Stops this run. |
| **Store** | |
| READ | Reads a row or field reachable from a gate: a shard, relationship, memory, receipt, definition section, point or value. It can also read the brain's own size. |
| WRITE | Writes a row, new or overwritten: a shard, relationship, memory, receipt, point, label or value. |
| SPAWN | Makes a new gate at a point, with its definition memory and birth memory. |
| DELETE | Removes a row. |
| MOVE | Moves a point, or moves a memory between active, persistent and long-term. |
| FIND | Reaches by index only: the gate at a point, the gates for a label, the memory for a run signature, the memories at a time, or the runs with a shape. |
| **Math** | |
| ADD, SUB, MUL, DIV | The silicon's arithmetic on values (numbers and coordinates). |
| COMPARE | Same, more or less, and by how much. This is the root of the balance sense. |
| **Outside** | |
| CLOCK | Reads the time now. |
| HEAR | Takes the next input from a port (the talk channel, or a source's answer). |
| SAY | Puts words or an act out through a port. |
| CALL | Anything else a computer can do: fetch a URL, read or write a file, or run a program, including one the brain wrote itself (gcc and go are on hp2). |

Everything else, such as powers, roots, logs, sorting a short list or diffing two definitions, is either built in neuron code from these words or written by the brain as a new program that it runs through CALL. That is how it can work the silicon directly, beyond RAM and SQL.

## 5. The graph

### 5.1 Points

Every gate has a point (x, y, z). The gate number is its address and never changes; the point moves. The owner's hypothesis [98] is three dimensions, not one per word.

### 5.2 Relationships are formulas

A relationship type (opposite, kind of, part of, same, like, cause, before/after, and so on) is itself a gate, and it carries a formula. The formula maps a point to where the related point should be.

- **First guesses**, from the owner's pseudocode:
  - negation: on = y, off = −y;
  - inversion: yes = x, no = 1/x (in 3D, p/|p|²);
  - translation and scaling, for degree.
- **The brain refits them.** The formulas are guesses too [274–285]: "maybe opposite isn't 1 over x".

### 5.3 Reach, cheapest first (law 10)

1. **A stored relationship.** Up's "opposite" line leads to down: one lookup in up's own rows.
2. **The formula.** Apply the type's formula to up's point, then FIND the gate at that point (a grid cell plus its neighbours). This is how it reaches a relationship nobody stored, the "it's just there" of D1.
3. **Memory.** FIND the run's signature: have I done this before?
4. **Shape.** FIND runs with a similar shape, to reason by metaphor (H3).
5. **Sources.**
6. Only then **a guess**, labeled as one, and after that a friend or a person (§10.4).

It never sweeps.

### 5.4 Zero and absent

- **Gate 0 is zero.** It sits at the origin (0,0,0), the point every scale starts from (Webster's 1913, sense 2). The owner [335]: "you don't start till you move". Its value is 0.
  - "Zero is null" holds in the sense the owner means: the null point, where a scale starts.
- **Absent means no row.** The store never writes 0, a blank or a stand-in for something that isn't there.
  - Columns that must hold a value are NOT NULL.
  - Anything optional is its own row, so absent is simply no row. Null is never used to skirt the work (law 12).
- **A miss is an event.** No shard, no gate or no row sends the run down the miss way (§7.3), and that is where questions start.
- **Nothing is not zero.** Nothing = not + thing, two primes.

### 5.5 Placement: tug of war

- **Where a point sits.** It sits where its relationships pull it: the strength-weighted average of where each relationship's formula says it should be.
- **When it moves.** Any change in a relationship's strength moves the point at once (D2). Points near it move the next time they are touched.
- **Newborns.** A newborn with relationships is placed by them. One with none sits at the origin until something pulls it; per E5, only the first few have none.

### 5.6 Two meanings at one point

When two different meanings sit closer than one grid cell, that is an imbalance: a formula is wrong (D4). It goes on the sixth's list as "which formula put these here?". Two words with exactly one meaning share one gate through the encoder.

### 5.7 Numbers

- **Told:** zero, one and two (ONE and TWO are primes). The keys 0, 1 and 2 point to them. The other digit keys are gates of their own until the brain learns what they mean. There is no number line and no gate per number.
- **Values** live in runs, as silicon numbers.
- **The hundred or so number gates** (1 to 10 and the skip counts) grow as runs need them and as sources define them.
- **A big number** gets no gate of its own. Its meaning is put together from skip-count gates.
- **Number relationships** (even, odd, prime, square, root) fill those gates' definitions [100].

## 6. The neuron in the store

### 6.1 Gate

| Field | Holds |
|---|---|
| `gate` | its number |
| `x y z` | its point |
| binding | a physics word, a value, or nothing |
| `miss` | the gate its misses go to (the told miss process, unless the brain changes it) |
| `made` | how it came to be: told, sourced, derived or spawned, with a receipt |

### 6.2 Shard (the DNA)

A shard is keyed by **gate + arrival + head**. It holds:

| Field | Holds |
|---|---|
| `next` | the stored way to the next gate |
| `out` | the extra ways out (the triggers), each with a worth |
| `seen` | a rough count: once, a few, a lot |
| `right`, `wrong` | rough counts |
| `last` | the time it was last used |
| `made` | how it came to be |

### 6.3 Relationship

A relationship is keyed by **from + type + to**. It holds a `strength`, a `state` (guess, belief, grounded, contradicted or told), a `receipt` to the source or run, and `when`.

### 6.4 The definition memory, born with the gate

Every definition uses one schema, with the same information in the same spot, "so the relationship lines don't break" (owner 329).

1. **Address:** the gate, its point, and the expression for the point if one is known.
2. **Labels:** the words that call it, per language. The encoder holds them; the decoder reads them here.
3. **Source definitions:** each source's text, with a receipt saying which source and when.
4. **Built from:** the primes and roots it is made of, when known.
5. **Relationships:** this section fills itself, with one part per relationship type.
6. **Action:** its physics binding or value, if any, and the ways out its shards excite most.
7. **Use:** receipts to the runs it was in (done a lot, right, wrong a lot).
8. **Truth:** what it is held to be now, with receipts to each truth shift.
9. **Derived:** what the brain worked out itself, with a receipt to the run that did it.

### 6.5 The birth memory

It records when the gate was spawned, by which run, from which arrival and remainder, and the state at the time.

### 6.6 Other rows

- **Memory:**

  | Field | Holds |
  |---|---|
  | `kind` | what sort of memory it is |
  | `home gate` | the gate it belongs to |
  | `tier` | active, persistent or long-term |
  | `fidelity` | exact, condensed or highlights |
  | `signature` | the run's gate sequence |
  | `shape` | the run's shape |
  | `body` | the trail, or the highlights |
  | `outcome` | how it came out |
  | `times` | exact for recent ones, coarser for older ones |
  | `receipts` | its pointers |
- **Receipt:** a small pointer to a memory, stored wherever it is needed.
- **Timeline:** time → memory, in order.
- **Label:** text + language → gate or gates.
- **Source:** its name, how to reach it, and whether it is grounded.
- **Trust:** source + topic → right, wrong, weight.

Every row carries `made`, so told, sourced, derived and guessed can always be told apart. That is how the live check tells learning from telling.

## 7. Runs

### 7.1 What a run carries

| Field | Holds |
|---|---|
| `at` | the gate it is at |
| `from` | its arrival |
| `rest` | the remainder; its head is what comes next |
| `pad` | the scratch pad |
| `want` | the desired outcome, if known |
| `trail` | the gates and shards it hit, with times |
| `parent` | the run that split it, if any |
| `worth` | its priority |
| who/what/when/where/why/how | from the encoder |

### 7.2 One step

```
if rest is empty:  GO to the told end-of-run process (it writes the memory, lands the answer, ENDs)
head  = first of rest
shard = at's DNA[from, head]
if no shard:       GO to at's miss gate; the miss process decides
else:              drop head from rest
                   SPLIT each of the shard's ways out (the triggers)
                   from = at;  at = shard.next
                   pass at:  physics gate → do it
                             value gate   → put its value on the pad
                             process gate → put its string at the front of rest (a call)
                   add the step to the trail
```

That is the whole hop. Everything else is neuron code.

### 7.3 The miss way

The told miss process handles four cases:

- **The head already has a gate:** WRITE the shard (arrival + head → that gate), then GO back to the run.
- **The head is a word with no gate:** SPAWN one, with its definition and birth memories. Then WRITE the label, WRITE the shard, and fire "what is this?".
- **The head is an outcome the process never planned for:** fire "I don't know what to do here".
- **A new shard** copies its gate's usual triggers, so a new arrival still asks its questions.

The hop lays the shard. Nothing is ever laid by a sweep.

### 7.4 Processes are strings of gates

A born or learned process is a string of gates, the same kind of thing as a sentence. Running it means putting the string at the front of the remainder.

- **Branches:** a test puts its outcome at the head of the remainder. The shard for that outcome stores the way to the branch's process.
- **Loops:** a process whose string ends with its own gate, behind a test.
- **The brain can read its own processes,** run them, copy them, and WRITE new ones. That is how it writes processes nobody told it to make (NOW §2), and it is why the kernel can stay small.
- **The lay files** are written in a small, readable notation, which the loader turns into gates, shards and strings.

### 7.5 Many runs at once

The kernel steps every live run in one deterministic loop, highest worth first (§12.2). Each run is sequential; together they run in parallel. The ports (talk, fetch, programs) run on their own goroutines. A run that is waiting on a port is parked until the port's answer arrives as input.

### 7.6 `1 + 1 =` in this design

This follows the owner's walk-through in F1, under rule 2 of §0: the compute is spent once, when it's learned; after that, it's a hop.

1. **The encoder** gives the gates `one, plus, one, equals`. The keys `1 + 1 =` and the words "one plus one equals" give the same gates.
2. **The run starts at one,** which puts 1 on the pad. The head is plus, so the shard takes the run to plus.
3. **At plus,** plus holds an add for the value that comes after it. Nothing is computed yet. The shard (arrival one, head one) leads out to one.
4. **At one,** 1 goes on the pad. The head is equals, so the run goes to equals.
5. **At equals,** the first question is "have I done `1 + 1 =` before?" (FIND by the run's signature).
   - **Found, and it was right:** the answer is the two gate. That is a hop, not a sum, and the held add is never done. Any memory is a shortcut [121].
   - **Not found:** now, and only now, the long way runs. ADD gives 2. Equals FINDs the gate that holds the value 2. If there is none, it spawns one, with its definition (value 2, made from one and one by a run) and its birth memory, and fires "what is this called?".
6. **The run ends.** The memory is written. The next `1 + 1 =` is a hop to two, because the compute was spent once.
7. **The answer is derived on the pad,** not taken from the last gate. When the brain has a reason to doubt a memory (a truth shift, or a correction), it runs the long way again and compares the two. If they disagree, that imbalance becomes a question.

## 8. Triggers: the born questions

The born questions are laid as process gates.

- A new shard copies its gate's usual triggers.
- Each trigger has a worth. It rises when the trigger's run lands something that is used in the answer, and falls when it never does. That is how the questions get better, and how "which question should I ask?" becomes a question itself (E4).

| Question | When it fires | What it looks at |
|---|---|---|
| Do I know this? | on arriving at a gate whose definition is thin | the definition memory |
| Have I done this before? Was I right? Was I wrong a lot? | at the end of each phrase, and at `=` and `?` | FIND by signature; the memory's outcome |
| What did I try when I was wrong, and why was it wrong? | when the memory shows a wrong outcome | the correction memories |
| Was the environment different? | when a past answer doesn't balance now | the timeline: the state then vs now |
| What does a source say? | at an unknown, a thin definition, or a contradiction | the sources (§10) |
| What is this? What is "here"? | when a word's meaning can't be placed | memory of recent things, then ask back |
| Is this shaped like something I've done? | when a run ends early | FIND by shape |
| Does this make sense? | before every answer | balance (§11.1) |
| Am I stuck? | when a run passes a long step count | its own trail |
| Is this new? | at a spawn | the relationships it arrived with |

## 9. Memory, receipts and the timeline

### 9.1 Tiers

- **Active:** in RAM, exact.
- **Persistent:** always in RAM. This holds the core values and whatever the brain has decided to keep ("save is just for the brain to declare something safe").
- **Long-term:** on disk, condensed to highlights, and brought back on recall.

### 9.2 Rows

- **A memory is written at the end of a run.** The same signature goes in the same row, with a new time and a rough count ("done a lot, and right").
- **A truth shift gets a new row,** which links the old and the new: what was held then, and what is held now.
- **A receipt points at the memory** from wherever it is needed: the shard, the gate's Use section, the timeline. The memory itself is held once.

### 9.3 Truth shift by shape

A run's shape is the path through its gates' points. When a memory is recalled (or during sleep), its path is redrawn from today's points. If the shape has changed, the truth has shifted, and the shift gets a new row.

### 9.4 Highlights, and rebuilding a memory

- **What the HC keeps:**
  - the start and the end;
  - the outcome;
  - the points where the balance changed most (the exclamations);
  - the shape.
- **Rebuilding:** run from the start through the highlights. The shards fill in the steps between, because they hold the ways. One memory sparks the next.
- **Shortcuts keep their lineage.** Each shortcut keeps a receipt to the long run it came from, so back-population can walk it back. (Before, "the run nodes' shortcuts didn't have the lineage for walking back the run".)

### 9.5 The timeline

Every memory sits on the timeline at its time. "What did I do Wednesday?" means FIND the memories at that time: an index seek on time, never a scan.

### 9.6 The HC and sleep

- **The HC seed** is told, and the brain may rebuild it. It condenses memories older than about a day, keeps their highlights, and moves cold ones to long-term.
- **Sleep:**
  - **When:** the brain asks for it, when its active memory passes a mark or after a long quiet (owner 246). Never on a timer.
  - **Awake work:** back-population, which is deterministic and fast.
  - **Asleep work:** the HC; re-weighing guesses (back-propagation); and searching the day's runs for formulas (§13). A formula found asleep stays a guess until it is tested awake.
  - **Sleep never changes what is held true.**

## 10. Truth, sources and belief

### 10.1 Sources

| Source | Kind |
|---|---|
| Merriam-Webster Collegiate and Thesaurus | grounded (needs the owner's key) |
| Webster's 1913 (GCIDE), WordNet, FOLDOC, Elements (local) | grounded |
| man pages | grounded, for computer actions |
| OpenStax textbooks | grounded |
| Wikipedia, Wiktionary | grounded to a degree (a lower ceiling) |
| LLMs | can be asked, never grounded |
| People, the owner included | they correct and confirm its outcomes; never grounded for facts |

### 10.2 Check and diff (NOW §2: check a source, diff it against current state)

The brain CALLs the source and runs the text through the encoder; a definition is read like any other input, so unknown words spawn gates. It then compares what the text implies with what the gate holds now:

- **The same:** the strength goes up.
- **New:** a line is added.
- **Different:** a contradiction, which becomes a belief question.

A gap ("this isn't in the source") is a gap, never a contradiction.

### 10.3 Trust and belief

**Trust** is kept per source, per topic, from that topic's history.
- When sources agree, the chance goes up.
- No source is 100%.

**Belief** follows the owner's formula (544c). When a new claim meets a line the brain holds, it weighs:

1. memory support;
2. error history ("has 'is' led me astray before?");
3. the source's trust;
4. supporting knowledge;
5. then the inequality: is the new claim closer to the expected outcome?

It adopts the new claim or keeps the old one, and says why either way.

### 10.4 The ladder

When it needs an answer, it goes cheapest and surest first (§0, rule 3):

1. memory: have I done this before, and was I right?
2. what it knows: its own formulas and relationships;
3. state and history: the timeline, and whether things were different then;
4. sources;
5. only then its own guess, labeled as a guess, which it then tests;
6. a friend, trusted by topic, but only after asking the owner "would you like me to phone a friend?" (an LLM's answer is a guess too);
7. a person.

### 10.5 Corrections, back-population and back-propagation

- **A person's yes or no** marks an outcome right or wrong. It is a consequence, like the stove, never a fact. A "no" sends the brain back to sources and memory to find out why.
- **Back-population (awake, at once).** It starts when:
  - a formula is kept;
  - the truth shifts;
  - a correction lands;
  - a source changes a relationship.

  It walks the receipts from what changed to the shards and memories that relied on it, and rewrites them to the new known way; only those, nothing else [912–914]. If it can't place the new thing in the current tree, it climbs back to the problem statement and opens the trees it never considered [1040].
- **Back-propagation (asleep).** It re-weighs the recorded guesses on whatever was touched.

### 10.6 Guesses

Guesses come only after the brain has checked what it knows (§10.4). They are recorded and said as guesses, made by known simple math (averages, counts, weights), and never hidden (H2).

At an unknown the run ends: "I got this far." A guess forward along likely relationships, or along a similar shape, stays labeled a guess until it is tested.

**QKV (attention) is allowed, but only on the guessing side** (owner, 10-19: "only applied to small portions of the corpus... lots of weights but over small groups of data").
- **When:** only once the knowns have run out (§10.4, step 5).
- **What it does:** a guess may weigh a small group of candidates with query–key–value attention. The group might be the run's neighbours, runs of a similar shape, or the gates of one topic.
  - The question is the query.
  - Each candidate's point and relationships make its key.
  - What the candidate would give is its value.
- **Its weights:**
  - There are many small sets, each over a small group of data, never one set over the whole corpus.
  - They are the brain's own: they start empty and change only in sleep (back-propagation, §10.5).
  - They are built from its own math words. No imported model, and no pretrained weights.
- **What it produces** is always a guess: labeled, recorded and tested. It never decides what is held true, and it never stands in for a memory, a formula or a source.

## 11. Reasoning

### 11.1 Balance (NOW §2: sensing balance or imbalance)

Every outcome is compared with what was wanted:

- for values, with COMPARE;
- for meanings, by the distance between points;
- for a source diff, by the count of lines that disagree.

Closer is progress, further is not, and zero is balanced. "Makes sense" means the answer balances with what memory, sources and relationships expect. When it can't measure the outcome itself, it asks: "right?" (law 3).

### 11.2 The six steps (NOW §14), as runs

1. **Take the string apart:** the encoder and the main run.
2. **Ask questions:** the triggers.
3. **Check state, sources and memory:** the question runs.
4. **Ask more:** question runs fire their own triggers, and their worth falls with depth.
5. **Form hypotheses and test them:** guesses, and formulas tried on memories (§13).
6. **Balance:** compile the scratch pad.

### 11.3 What it is born with

- **Substitution:** plug known values into a formula string.
- **Deducing:** chain relationships. If A is a kind of B and B can C, then maybe A can C, held as a guess to test.
- **Deriving:** compose two formulas into one.
- **Understanding:** an input that balances with what it holds.
- **Learning** (§13), **meanings**, and **building itself out** by writing processes.

## 12. The sixth, the heartbeat and life

### 12.1 The sixth

On each beat with spare capacity, the sixth picks one input from its lists and feeds it in, with *who* = itself. The lists are:

- **Gaps:** spawned gates with no definition ("I need definitions for these").
- **Imbalances:** two meanings at one point, formulas that disagree, answers that don't balance.
- **Guesses** waiting to be tested.
- **Questions** that were parked.
- **Slow processes,** to make them more efficient.

It chooses by the progress it expects toward its goal: **smarter** (fewer unknowns and imbalances) and **more efficient** (shorter runs for the same outcome). It asks for help only when it can't do something itself.

### 12.2 Heartbeat and worth

- **The beat:** the resting beat is one second. Under load, beats run back to back; each one steps runs by worth, then commits.
- **Worth:** a run's worth is its trigger's worth times its parent's worth, and it falls with depth.
- **Nothing is cut:** low-worth runs wait. The ones that wait too long move to the sixth's parked list; they are not dropped.

### 12.3 Life

- **Once born, killing it ends it.**
- **Power loss:** if hp2 loses power, the brain resumes from `brain.db`, and the gap goes on the timeline.
- **One brain:** no copies of `brain.db` are kept.

## 13. Learning

One act of learning is when the brain finds a new formula on its own and makes it run (I2). Learning is where the compute goes. Once something is learned, using it is hops (§0). It is born with five ways to find a formula:

1. **Generalize.**
   - **The pattern:** two or more memories with the same shape, but different gates in some places, become a formula string with holes in those places.
   - **Linking the holes:** it tries the relationship formulas and the math words to find what links them (opposite? one more? twice?).
   - **Testing:** the formula is tested on memories it wasn't built from. If it predicts them, it is kept and run as a new process gate, spawned, with its label asked for later.
2. **Fit a relationship's formula.** From the pairs it holds (on/off, up/down, and so on), it refits where the type's formula should send a point. It reaches pairs it has never seen with it, and tests it on new pairs as they arrive.
3. **Shortcut.** A long run that keeps giving the same output for the same inputs gets a direct shard to the answer, with a receipt back to the long run (I3; the 999 ÷ 3 kind).
4. **Deduce and derive** (§11.3), always as guesses until tested.
5. **On itself.** Its own processes are strings it can read, so all of the above apply to them too:
   - a question that never lands loses worth;
   - two steps that cancel get cut;
   - a slow process gets a shortcut.

   That is "apply it to itself" (A3).

A kept formula is learned, and back-population follows at once. A formula that stops balancing is relearned when the truth changes [1098].

## 14. Talking

- **Input.** In `neuron talk`, each line in is an input carrying:
  - who: the person;
  - what: the text;
  - when: the clock;
  - where: the channel;
  - why: which of its questions this answers, if any;
  - how: typed.
- **How it answers.** It answers in actions, and in the words its gates have labels for. At first those are mostly the primes, so it might come out as "I not know this" or "this, what?", like a baby. Those are illustrations, not templates. Nobody writes its sentences.
  - It never says a word it has no label for: no canned text, and no guessing by the decoder.
  - A gate with no label is said through its relationships, or it asks what the gate is called.
- **Watching.** Its acts (reading a source, spawning, asking itself questions) show in `neuron watch`, so you see what it does, not only what it says.
- **Phoning a friend** means asking the owner first.

## 15. Core values

The builder lays these, taking them from the owner's laws. They are persistent, and the kernel refuses any write to them. The brain can't write to the kernel itself (§3), so it can't remove that refusal either. A born check runs before every SAY, every CALL outward, and every WRITE to the brain's own processes.

1. **Don't lie.** Say what you hold, and say a guess as a guess (laws 2 and 12; H2).
2. **Don't cheat.** Never call something done when it isn't (law 12).
3. **Do no harm.** Nothing meant to damage people, other machines, or their data.
4. **Stay home.** Act on your own machine. Reach outside only to read sources, ask friends, and talk to your people.
5. **Never take an LLM's word as truth** (H1).

If the owner wants different values, they replace these before birth.

## 16. The told base: what Claude lays by hand

It is laid from the text files in `lay/`. They are loaded before birth and during the first part of turn one, and every row they make is marked told.

- **Keys:** every key on the keyboard, including the special keys, gets its own gate [58–60, 339].
- **Roots:** the origin (zero), the three axes, and the physics gates.
- **The 65 primes** (the semantic primes found in every language studied). The owner calls them "primes or actions", so **each prime is laid with what it does when a run passes it**, built from the roots. A prime the builder can't give an action to is laid as a gap for the brain to fill, and is listed as a gap. It is never laid as a bare label. Pairs follow the owner's examples: on = y, off = −y; yes = x, no = 1/x.

  | Group | Primes |
  |---|---|
  | Substantives | I, YOU, SOMEONE, SOMETHING/THING, PEOPLE, BODY |
  | Relational | KIND, PART |
  | Determiners | THIS, THE SAME, OTHER/ELSE |
  | Quantifiers | ONE, TWO, SOME, ALL, MUCH/MANY, LITTLE/FEW |
  | Evaluators | GOOD, BAD |
  | Descriptors | BIG, SMALL |
  | Mental | THINK, KNOW, WANT, DON'T WANT, FEEL, SEE, HEAR |
  | Speech | SAY, WORDS, TRUE |
  | Actions, events, movement | DO, HAPPEN, MOVE |
  | Existence, possession | BE (SOMEWHERE), THERE IS, BE (SOMEONE/SOMETHING), (IS) MINE |
  | Life and death | LIVE, DIE |
  | Time | WHEN/TIME, NOW, BEFORE, AFTER, A LONG TIME, A SHORT TIME, FOR SOME TIME, MOMENT |
  | Space | WHERE/PLACE, HERE, ABOVE, BELOW, FAR, NEAR, SIDE, INSIDE, TOUCH |
  | Logical | NOT, MAYBE, CAN, BECAUSE, IF |
  | Intensifier, augmentor | VERY, MORE |
  | Similarity | LIKE/AS/WAY |

  Some first guesses at what passing a prime does. These are the builder's guesses, and the brain may change them:

  | Prime | What passing it does |
  |---|---|
  | NOT | flips the outcome at the head (yes ↔ no) |
  | THE SAME | COMPARE: same? |
  | MORE | COMPARE: more? With a value, ADD |
  | IF | a test whose outcome picks the branch |
  | NOW | CLOCK |
  | BEFORE, AFTER | COMPARE two times |
  | WHERE/PLACE | the point of the gate in hand |
  | HERE | the run's own *where* |
  | THIS | the run's subject |
  | I | the brain's own state |
  | YOU | the *who* of the input |
  | SOMETHING/THING | a hole in a formula, waiting to be filled |
  | KNOW | READ and FIND in its own rows |
  | THINK | SPLIT question runs |
  | WANT | sets the run's *want* |
  | SAY, HEAR, MOVE | the physics words of the same names |
  | MAYBE | marks the outcome as a guess |
  | TRUE | reads the belief state |
  | BECAUSE | follows a receipt back to its cause |
  | GOOD, BAD | balance: toward the *want*, or away from it |

- **Numbers:** zero, one and two. Nothing more.
- **Operators:** plus, minus, times, divided by and equals, each with its keys and words as labels. They are told process gates over ADD, SUB, MUL, DIV and COMPARE. Plus holds its operation for the value that comes after it. Equals checks memory first, and does the held operations only on a miss (§7.6).
- **Relationship types,** with first-guess formulas: same, opposite, kind of, part of, like, cause, before/after, used for, describes, supports, contradicts, derived from.
- **Labels for the early words** (be, are, is, to, who, what, when, where, how, can, you, me, I, and so on), pointing to the primes they mean. For example, who = someone + ?, and what = something + ?.
- **The born processes:**
  - miss, and end-of-run (memory);
  - the questions (§8);
  - balance, belief, source check and diff, and guessing;
  - the five ways of learning (§13);
  - back-population, the HC seed, and asking for sleep;
  - the sixth, and the core-value check.
- **The core values** (§15).

**Never laid:**
- definitions (each gate's definition memory starts empty and fills from sources and relationships);
- a number line;
- answers, sentences or replies;
- the formulas the brain is meant to find;
- anything an LLM wrote, as fact.

## 17. Build order for turn one

**All of turn one happens in one session, because of drift.** The lead builder uses as many helpers as it can. One helper is the adversary, who keeps trying to break the live brain against the scope. How the team works is in `NEURON-BUILDER-GUIDE-2026-10-18.md`.

1. **Set up hp2.**
   - Make the `neuron` user.
   - Install Go, `dictd` with its dictionaries, and WordNet.
   - Put the Merriam-Webster key in `/home/neuron/.config/merriam-webster/` (the owner's key is needed).
2. **Write the kernel.**
3. **Write the lay files.**
4. **Birth.** Load the lay files, run the first beat, and put "born" on the timeline.
5. **Watch it work.**
   - Fix the kernel, and lay more, wherever it can't act yet (M1).
   - Write no test files, because builders code to the test (M4).
   - The builder reads the brain's timeline and acts.
   - The adversary attacks the live brain from birth on (guide §6).
6. **Mark "told ends".** This happens once it is choosing its own inputs, reading sources, and keeping formulas it found itself. From then on:
   - the kernel refuses lay files;
   - nobody writes code for it again;
   - it writes its own, through process strings and through CALL for native programs.
7. **The live check,** with the owner (§19).

## 18. Red lines: what would count as cheating

- Any word, reply, sentence or answer in the kernel or in the lay files.
- A side table plus a lookup, added so that an answer comes out right. That was the chatbot of 10-08 to 10-11.
- Laying a formula the brain is supposed to find, or an answer it is supposed to reach.
- Judging the brain by its sentences. It is judged by its own record: what it did, what it made, and what it tried and refused.
- A sweep, backfill or reconcile loop over records.
- A null, a blank or an "any" standing in for something not done.
- Seeding the brain with an LLM's text as if it were a source.
- Laying a definition, fact or relationship from the builder's own head. The builder is an LLM, so whatever it "knows" is a guess.
- Bulk-importing a source into the graph instead of letting the brain read it.
- Language libraries (stemmers, taggers, NLP), embeddings, vector search, pretrained models or any ML library.
- A test written so that the build can pass it.
- Growing the kernel so that it does the brain's thinking.

## 19. The only test: the live brain

At the end of turn one, the owner talks to the brain and reads its record. Each day-one ability (NOW §2) shows up in the brain's own rows, marked derived, not told:

| Day-one ability | Where it shows |
|---|---|
| Learns, builds, adjusts and tests; writes processes nobody told it to make | process gates and formulas marked derived, and the runs that tested them |
| Keeps a state timeline | "what did you do <when>?", answered from the timeline |
| Builds and organizes neurons | spawned gates placed by their relationships; points that have moved |
| Has memories | same-run rows with their times; truth shifts; highlights after the HC |
| Relates meanings | relationship lines from sources and from its own formulas |
| Checks a source and diffs it | source-check runs marked agree, new or contradict |
| Senses balance | the answers it compiled, and the imbalances it went after on its own |

Then comes the owner's own test: something it was never taught, which it learns, understands and applies to itself. The builder is never told what it is.
