# The guessing part of the brain, in the owner's words (2026-10-31)

Written at the owner's word of 2026-10-31 night: "what does the guesser have any fucking thing to do with source compare????? define is from source if you add the guesser into that you are adding the fucking guessing of basically a fucking llm..... that is not what guessing is for... fucking stop inventing your pieces... redesing the guessing part of the brain to be used only for my fucking design".

Nothing below is new. Every line of the first table is the owner's or the reference draft's, with its place. The second table is what I built against it. The third is what the words leave open: those are the owner's, and nothing has been built for them.

## What the design says

| | The design | Where |
|---|---|---|
| 1 | "define is from source" | owner, 2026-10-31 night |
| 2 | "The lookup order is memory, then state, then sources, then a guess." | reference draft 5.6 (P5-9 B1) |
| 3 | "A real unknown is followed by the brain's own guess, never a bare 'teach me.'" | draft 5.6 |
| 4 | "Keep guessing distinct from known execution. Shape similarity and historical frequency can support a candidate, not verify it." | build chain 83 |
| 5 | "a guessing or hypothesis brain with a very small corpus, which packages finished results to long-term storage instead of keeping them alive" | draft 2.7 |
| 6 | "your qkv is over the entire corpus, but here it's only over targeted runs inside a corpus" | owner, 2026-10-07 |
| 7 | "guesses are fine but they have to be announced... whith data.. I don't know the correct answer I have a guess that I believe is 93% probably the correct answer would you like to test the hypothosis? (guess)... we do not hidden guess" | owner, 2026-09-30; draft 5.6 |
| 8 | "I think it stops at the first unknown... but if that unknow has relationships, then it becomes a guess after that, and it can continue stepping forward based on relationships ... those must remained labeled guess" | owner, 2026-10-05 |
| 9 | "it should derive a formula to look at those other words via relationship, definitions, and it should be able to compare relationships amongst the other words and use the the graph and relationships know" | owner, 2026-09-30 |
| 10 | Run a decision tree, down each leg as far as possible, asking at every step "does this make sense, does it progress toward the outcome?"; drop a leg that fails; go back to the decision and take another leg; design a test before using it; each correct result makes the process more likely to become a belief or a truth | draft 5.6 (P5-9 B1) |
| 11 | "Shape makes guesses." Lay a piece of a process whose before and after are unknown into a completed process that looks similar | draft 6.4 |
| 12 | "A guess is always a guess, a guess can turn into a belief, but can never be knowledge until confirmed by grounded truth, but that confirmation or lack there of builds confidense or not in the processes that determined that answer" | owner, 2026-10-08 |
| 13 | Back propagation "belongs to sleep, or to another brain"; "the hippocampus doesn't run all the time, only in a sleep cycle... this is later also where we believe optimize (or qkv) for presise 'guessing' is done... on targeted runs or topics" | draft 5.7; owner, 2026-10-06 |
| 14 | "my guessing system is basically you and its something I use on the daily but it's not the core of my brain function" | owner, 2026-10-22 |
| 15 | "[Open] Guessing has not been started in the new model." | draft 5.6 |

## What I built against it (mine, tries/18, tries/28)

| The design | What I built | Broke it how |
|---|---|---|
| 1, 4: define is from source; guessing distinct from known execution | Span 4 of the define run fed every source return into the guesser's corpus, on every define | The guesser sat inside define |
| 5, 6: very small corpus, targeted runs | 53.9 million corpus rows, every word of every return, 2.9 GB | A whole-corpus search, the thing the design exists to avoid; law 3 |
| 7: announced, tested, no hidden guess | `why` asked it by itself for an open cell and laid the answer into the cell. 11,978 guesses on the big brain, one ever answered by a person | Hidden guesses, made in a chain nobody was reading |
| 8, 9, 11: from relationships and shape | Which word sits on the most lines with it. `Minderbinder` gives `chins`, `NewScientist` gives `Sumit` | Word counting: the small LLM the design says the brain does not need to be |
| 10: a decision tree, legs, a test first | One answer, one query | None of it there |
| 13: sleep, or its own brain | Ran inside the waking chain on every open cell | |

My own 10-28 note said it plainly and I built on it anyway: "the simplest guesser, not the hand-built llm the owner described".

## Left open: the owner's, nothing built

1. **What starts a guess.** The words say a real unknown after memory, state and sources. They do not say whether it starts only from a line at the prompt, or whether the sixth may start one.
2. **What the very small corpus is.** The words say small and targeted. They do not say what goes in it.
3. **What a leg walks on, and what "does this make sense, does it progress" is as a check.** Items 8 and 9 point at relationship rows. The rows hold only `like` and `opposite` today.
4. **The weights.** Draft 5.6: "through backpropagation... I don't know enough about it."

Until those are the owner's, the guessing brain stays attached and unused, its rows kept (draft 5.6: "never lost"), and an unknown stays an announced unknown.
