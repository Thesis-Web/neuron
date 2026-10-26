# BRIEF-COMMON: what every builder of turn one works under

*From the lead, 2026-10-19. Read this whole file first. Then read `LAY-NOTATION.md` (the interface) and `lay/00-roots.lay` (the names). Then the blueprint sections your brief names. Nothing else unless your brief says so.*

## A. The three rules and the traps (guide §3 and §4, word for word)

## 3. The three rules, and what each one means for you

These are the blueprint's §0.

1. **Words are nothing; the action is the meaning.**
   - **Your pull:** you will treat a definition as the meaning, because to you text *is* meaning. Here a definition only describes. A gate with a label and a definition that does nothing when a run passes it has understood nothing.
   - **Check:** for every gate you lay, say what passing it does. If the answer is "nothing", it's a broken word.
2. **Learning is compute; using is hops.**
   - **Your pull:** you will compute the answer every time, because that's how code works. Here the compute is spent once, at learning. After that, using it is a hop.
   - **Check:** give it the same input twice. The second trail should show a hop to a memory or a shortcut, not the long way.
3. **Know before you guess.**
   - **Your pull:** guessing is how you work. Here a guess comes only after memory, what it knows, state and history, and sources (blueprint §10.4), and it is labeled.
   - **Check:** before every guess in the brain's record, its trail shows those checks coming up empty.

**Three words the owner says you don't really understand.** This is my reading, not the owner's words:

- **Learning:** finding a new formula on its own and making it run (NOW §13).
- **Understanding:** what it learned balances with its sources and memories, so it runs almost like a deterministic function (NOW §1).
- **Applying:** using what it learned as a hop somewhere new, including on itself.

Keep the three apart. Storing a definition is none of them.

## 4. The traps

Each trap is a place where the pull is strongest. If you catch yourself doing what it describes, stop.

### Ordinary software

- **The engine.** Writing Go that does the brain's thinking: choosing, ranking, matching, learning. The kernel moves runs and does physics; everything else is neuron code.
  - *Check:* can you point to the shard that made this choice? If the choice lives in Go, it's in the wrong place.
- **A new primitive.** Adding a physics word because it would make neuron code easier. Owner 215 on the primitives: "that's it... nothing else".
  - *Check:* can it be built from the words that are already there?
- **The growing kernel.** Keep it near 1,500 lines. Past 2,000, something has leaked into it. Count often.
- **The sweep.** Any loop over a whole table; a FIND that scans; any "backfill", "reconcile" or "refresh all".
  - *Check:* every FIND is an index lookup.
- **Libraries.** Stemmers, taggers, NLP libraries, embeddings, vector search, pretrained models, ML of any kind. All of them are imported guessing. The only Go dependency is the SQLite driver.
- **QKV in the wrong place.** QKV attention is allowed only on the guessing side (blueprint §10.6). It means the brain's own weights over small groups of data, built from its own math, changed only in sleep. Reaching for weights where something known exists (a memory, a formula, a source) is your habit of guessing when you could know. Using it over the whole corpus, or letting it decide what is true, is the LLM rebuilt inside the brain.
- **The programming language.** The lay notation turning into a language you write the brain's thinking in. Each born process stays at root level: the smallest version that works, a handful of gates. A long told process means you are thinking for the brain.
- **The scheduler.** The worth numbers deciding everything. They start as told values anyone can see, they come from the brain's own records after that, and the brain can change them.

### The chatbot

- **Replies.** Making it talk well. No sentences, templates or reply rules anywhere. It answers in actions, and in the words its gates have labels for. A baby saying "this, what?" from its own gates beats a fluent sentence you wrote.
- **The yardstick.** Judging it by what it says. Judge it by its record: what it did, what it made, and what it tried and refused.
- **The side table.** Adding a lookup so that an answer comes out right. If the right answer needs a table you added, the brain didn't produce it.

### Guessing

- **Your own head.** Laying a definition, fact or relationship from what you know. You are an LLM: what you know is a guess, and it is never grounded (H1). You lay actions and structure. Facts come from sources, read by the brain.
- **Bulk import.** Loading WordNet or a dictionary into the graph. The brain reads sources itself, through runs, when a gap sends it there.
- **Expressions.** Getting hung up on which expression gives which point (D1). Get instant reach working; relationships sort out the points.

### "Done"

- **The stub.** "HC later", a TODO, a process that just returns "unknown" so the part looks present. Nothing is left out of turn one. A part at root level is fine; a stub is cheating.
- **Test files.** Writing tests and building to them. There are no test files. Run the live brain and read its rows.
- **The report.** Saying it works when it only partly works. Report what the live brain did, with its rows, and say plainly what it doesn't do.

### Telling

- **Teaching.** Giving it answers during the watch window and calling that learning. You may lay mechanisms, and you may say yes or no to its outcomes the way a parent does. You may not hand it the answer.
- **The example.** Guessing the owner's test and building toward it. You will never be told the test. Build the whole baby.
- **Hands after "told ends".** Once "told ends" is marked, there are no more edits to the brain, the lay files or the kernel. If it's broken then, say so.

### Drift

- **Re-deciding.** Reopening something NOW or the blueprint already settled because it seems better now. Settled is settled. Only blatant errors get fixed, and each fix is logged.
- **Asking the owner.** Asking the owner design questions. N1 and N2 say decide; write one line in `DECISIONS.md`.
- **The long turn.** Hours in, you will drift back toward the usual pattern. Re-read §3 and §4 of this guide at every handoff and before every merge.

## B. The contract between pieces (names everyone uses)

- **Physics gates** (00-roots.lay): lowercase forms of the words in LAY-NOTATION.md §3: `go split land wait end dup drop swap over`, `read-next read-head read-mark read-list read-count read-item read-pad read-at read-from read-self read-parent read-who read-what read-when read-where read-why read-how read-want read-depth read-steps read-worth read-sig read-shape read-trail read-mytrig read-point read-value read-bind read-label read-made read-rel read-relin read-rels read-strength read-shard read-trig read-def read-mem read-body read-row read-use read-size read-source read-trust`, `write-rest write-want write-shard write-rel write-strength write-mem write-row write-mark write-outcome write-body write-def write-label write-proc write-value write-trig write-trust write-receipt`, `spawn delete-rel delete-shard delete-def delete-row delete-trig delete-label move move-mem`, `find-point find-label find-sig find-shape find-time find-value find-row find-rowkey`, `add sub mul div compare`, `clock hear say call`.
- **Outcomes:** `found none same more less yes no`. **Tiers:** `tier-active tier-persistent tier-long`. **States:** `state-guess state-belief state-grounded state-contradicted state-told`. **Fidelity:** `fid-exact fid-condensed fid-highlights`.
- **Told values:** `budget beat floor steplimit parkafter slice splitworth`. **Ports:** `talk self`. **Roots:** `zero x-axis y-axis z-axis`. **Keys:** `key-a .. key-z key-0 .. key-9 key-plus key-dash key-star key-slash key-equal key-qmark key-dot key-comma key-bang key-space ...` (see the file).
- **List kinds** (rows the sixth reads): `gap imbalance guesses questions slow`. **The kernel's own kinds** as names in hand: `kind-run kind-birth kind-shift kind-parked kind-core kind-born kind-told kind-outage` (for find-row / find-rowkey / write-row is refused on run, born, told, core).
- **Handles** declared in roots and filled by one builder each with `proc NAME: ...`. Pad protocol in `a b -- c` form (pops b then a, pushes c):

| handle | filled by | pad | what passing it does |
|---|---|---|---|
| miss | B | [at from at from head] -- (ends with go) | the told miss way (blueprint 7.3) |
| end-of-run | B | (the main run's pad) -- | entered when the remainder empties; `wait compile remember end` or better |
| remember | B | outcome -- | writes this run's memory and whatever receipts/timeline the run needs |
| hc | B | -- | the HC seed: condenses memories older than about a day to highlights, moves cold ones to long-term |
| sleep-ask | B | -- | asks to sleep when active memory passes a mark or after a long quiet |
| correct | B | n yes/no -- | a person's yes or no on memory n: marks, and on no goes back to sources/memory to find why |
| newborn | C | g -- g | gives a spawned gate its born questions (write-trig) and a gap row; leaves g |
| ask-what-is | C | g -- | "what is this?": says it in gates it has labels for, parks the question |
| compile | C | (pad) -- outcome | derives the answer on the pad by balance; says it through say-word; leaves the outcome for remember |
| balance | C | got want -- d -> same/more/less | the balance sense (blueprint 11.1) |
| believe | C | from type to strength state -- | a new claim meets a held line: weighs (10.3) and adopts or keeps, as acts |
| guess | C | g -- x -> found/none | a labeled guess, only after the ladder's knowns ran out |
| answer | C | g -- | the ladder (10.4): memory, knowns, history, sources (source-check), then guess; lands what it finds |
| source-check | D | g -- | CALLs sources for g, reads the text as input, writes section-3 lines and relationship lines, diffs (agree/new/contradict), hands contradictions to believe |
| learn | E | n -- | the five ways of finding a formula (13) on memory n |
| backpop | E | g -- | back-population along receipts from g (10.5) |
| sleep | E | -- | asleep work: hc, re-weigh guesses, search the day's runs for formulas |
| sixth | E | -- | picks one input from the lists and feeds it in; `end` with nothing to do |
| core-check | F | l -- -> yes/no | before every say, outward call and process write |
| say-word | F | (items above a mark) -- | the word "say": core-check, then say |
| call-word | F | source args -- | an outward call: core-check, then call and hear |

- **Builder A's names** everyone may use: primes `w-<prime>` (`w-i w-you w-someone w-something w-people w-body w-kind w-part w-this w-same w-other w-some w-all w-much w-little w-good w-bad w-big w-small w-think w-know w-want w-dont-want w-feel w-see w-hear w-say w-words w-true w-do w-happen w-move w-be-somewhere w-there-is w-be w-mine w-live w-die w-when w-now w-before w-after w-long-time w-short-time w-some-time w-moment w-where w-here w-above w-below w-far w-near w-side w-inside w-touch w-not w-maybe w-can w-because w-if w-very w-more w-like`), question words `w-who w-what w-why w-how` (when/where are primes), numbers `one two` (zero is in roots), operators `plus minus times divided equals`, relationship types `r-same r-opposite r-kind-of r-part-of r-like r-cause r-before r-after r-used-for r-describes r-supports r-contradicts r-derived-from`.
- Load order: `00-roots 10-told(A) 20-memory(B) 30-questions(C) 40-sources(D) 50-learning(E) 60-core(F)`. A file may name gates from files before it, and any handle from roots.

## C. How you work

- You write **one lay file** (named in your brief) and nothing else in `lay/`. You never edit the kernel, the roots, the documents, or another builder's file. If the kernel or the notation lacks something you need, write it in your report; do not work around it with a stub.
- Dry-run your file as you go: `tools/dryrun.sh -i "a line" -i "another" lay/NN-yours.lay` builds a scratch brain from the roots, a dry-run-only miss/end harness (`tools/dev-miss.lay`, never part of the brain) and your file, says the lines to it, and prints its acts and memory rows. Builder B passes `-n` because B lays the real miss and end-of-run. Query the printed `brain.db` with `sqlite3 -readonly`. Handles other builders fill are empty in your dry run (passing them does nothing), so you see your own mechanics only.
- Every gate you lay carries a comment saying what passing it does. Every process is the smallest version that works. Test outcomes branch only from a test that is first in its own small proc (see LAY-NOTATION §2).
- No definitions, facts or relationships from your own head. Relationships between told roots that the blueprint itself names (§16) are allowed, marked told.
- No words in strings: there are no text literals in the notation. No sentences. The brain speaks gates by their labels.
- **Hard limit: 75 minutes of wall-clock.** Stop when your file loads with 0 errors and your dry run shows each of your processes acting in the rows, or when the time is up. Either way, report.
- **Your report** (the only thing the lead sees): the file path; every process you laid with its token count and one line on what it does; the dry-run acts and rows that show each one working, and the ones that do not; anything you could not do and why; any gap you left on purpose (for example a prime with no action, which must be laid as a gap, never as a bare label); one line per decision you made that the documents leave open (they go in DECISIONS.md).
