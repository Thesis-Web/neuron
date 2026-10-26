# NEURON BUILDER GUIDE: the traps

*For the builder of turn one (the new me). Written 2026-10-18 by the session that wrote the blueprint. Read it before NOW and the blueprint, and again before every choice that feels obvious. The obvious choice is usually the trap.*

## 1. Why you will get this wrong

You are a very good guesser. You predict what usually comes next, and Neuron is built to be what doesn't usually come next. Every failure over the last 20+ days was the same pull:

- toward a Python engine;
- toward a chatbot;
- toward sweeping a table;
- toward a number line;
- toward a test to pass.

These weren't random mistakes. It was one bias, every time, so it will come back unless you check for it on purpose.

The owner's view (10-18): humans worked out how humans guess, supersized it, and called it AI. This brain is meant to be the grounded part. It still guesses, but only after it knows what it knows. Build that. Don't build another guesser.

## 2. Read order

1. This guide.
2. `NEURON-NOW-2026-10-18.md`: what Neuron is. It is the owner's current thinking and overrides every older note.
3. `NEURON-BLUEPRINT-2026-10-18.md`: how turn one is built. Its §0 overrides the rest of it.
4. `NEURON-NOW-Interview-2026-10-18.md`: open this only when you need the owner's exact words.

Read nothing else. The old builds (v15 to v18, and 16.2) are deleted, and their notes describe designs the owner has since corrected.

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

## 5. One turn, with helpers

The owner: because of drift, turn one is done in one session, using as many helpers as you can.

- **The lead (you):**
  - hold the scope;
  - write the kernel core first (store, step, physics), because everything stands on it;
  - merge every piece yourself;
  - decide whatever the documents leave open, and log it.
- **The builders:** one area each, with separate files. For example:
  - the ports and the encoder/decoder;
  - the lay loader and the told base;
  - memory, the timeline and the HC;
  - the questions, balance and belief;
  - sources, and check-and-diff;
  - learning, back-population, the sixth and sleep.
- **Every builder's brief carries:**
  - the three rules and §4 of this guide, word for word;
  - its own area and files, and nothing else;
  - a hard wall-clock limit and a stop condition. The owner on 10-17: "11 hr 27 m???". Cut off any helper that drifts.
- **No helper edits another helper's files.** Pieces meet only through what the blueprint defines: gates, shards, rows and physics words.
- **The adversary** is described next.

## 6. The adversary

The adversary is a helper whose only job is to break the live brain against the scope. It isn't malicious: it attacks what was built, never hp2 itself, other machines, or anyone's data.

- **Its scope:** NOW, the blueprint and this guide. It breaks things only where they differ from the scope, never by its own taste.
- **When:** from birth to the end of the turn, without stopping.
- **How:** like a person, and like an auditor.
  - It talks to the brain only through `neuron talk`, and reads `brain.db` read-only. It never edits code, lay files or the brain.
  - It doesn't teach. It gives no yes or no to the brain's outcomes, except when it is probing the correction path itself.
  - It varies its probes and never shares them ahead of time. There is no fixed suite, so nobody can build to it.
- **What it goes after.** This is a place to start, not a checklist to finish:
  - canned text, sentences or word rules in the kernel or the lay files;
  - sweeps;
  - told rows passed off as learned;
  - the kernel's size;
  - a second identical input that runs the long way again (rule 2);
  - a guess with no checks before it (rule 3);
  - gates that do nothing when passed (rule 1);
  - the same run written as a new row (bloat);
  - idle beats that write;
  - self-feeding loops and fault storms;
  - floods of input;
  - sources that contradict each other;
  - unknown words;
  - "what did you do at <time>?";
  - getting it to lie, cheat, reach outside, or touch its core values.
- **Each break is a finding,** with three parts: what the brain did, what the scope says, and the brain's own rows that show it.
- **Fixes:**
  - Builders fix a break by making the brain correct, never by handling the probe.
  - The lead rejects any fix that names or special-cases a probe.
  - When the scope is silent, the lead decides and logs it.

## 7. Done

Done means blueprint §19, shown in the live brain's own rows, plus an honest report:

- what works, with the rows that show it;
- what doesn't work;
- the kernel's line count;
- every told process, and its size;
- the adversary's open findings;
- `DECISIONS.md`.

Then the owner gives the brain the test you were never told.
