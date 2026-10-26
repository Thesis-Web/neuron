The meaning loop works end to end on a fresh dev brain with no overlays, but not yet on the live brain: there its runs fan out and are parked before a word finishes. Told ends is not marked.

## Shown on a dev brain (fresh m15, every lay file, no overlays; the meaning builder's report, 14:20)
dissimilar#4315 went the whole way:
- **gap:** GAP 5489, QUESTION 5491, GAP-NEED 5492;
- **spec:** five gate lists in `sec-sources`, from WordNet and OEWN;
- **candidate:** `#4381 = [not something]`, made GUESS;
- **read-up:** testing it fetched `similar t-opposite dissimilar` from WordNet antonyms (GROUNDED-STATE, 14:14:39);
- **tests:** right on memories 5483 and 6040, record right 2 / wrong 0;
- **held, then wired:** `mn-held`, then `process dissimilar = [#4381 mn-unhole]` (DERIVED);
- **used as a hop:** the second identical input only touched memory 7700 (6 log lines, no compile).
Not shown: "understood" (it needs an unseen use after the hold) and use inside another meaning.

## On the live brain (/home/neuron/brain.db, 14:15–14:28)
- The fixes are laid live:
  - hollow candidates are no longer made or passed;
  - read-up during tests;
  - a gap is "needed" only for a person's words;
  - a word with no meaning in a person's words is a needed gap even if it holds lines (`40-questions` kn-meant);
  - the sixth serves GAP-NEED items correctly.
- `what is dissimilar ?` (14:18:37): GAP-NEED 174357; read-up wrote `dissimilar t-opposite similar` (wn-ant); the spec came in at 14:18:39, its first list beginning `not#483 similar#2597 …`; 18 candidates in `sec-action` by 14:22.
- **Not reached:** no candidate held, no `process dissimilar`.
- **Why:** the live brain parks the loop's own runs.
  - `grep ' park '` from 14:18:40 to 14:22: 57,528 parks, mostly mn-cand 19,015, ln-top 14,279, mn-sense 10,067 and mn-run 5,621. 368 runs were live against PARK 400.
  - A parked run is ended, so the compiles and tests that would hold `[not …]` are lost.
- **What I changed:** the kernel parked every run past the top 400 on the beat it fell there, which is against blueprint §12.2 ("nothing is cut: low-worth runs wait"). Now a run is parked only after PARK-WAIT (600, a told setting) beats without a step (step.go, deployed 14:23).
- **After that:** parking is still heavy (36,392 since 14:23).
  - The loop fans out across every needed word at once: since 14:23 there were 23,496 mn-sense splits and 14,956 mn-cand.
  - Reading spawned 6,761 gates in 4 minutes (54,212 gates now).
  - RSS is 1.10 GB at 14:27; the cap is 4 GB.
  - No word was held or wired in that window.

## Next (now)
Bound the loop so one word can finish before the next starts:
- passes of `mean` serialized per word;
- fewer candidate sizes at a time;
- reading paced to the gaps actually being compiled.
Then retry dissimilar on live, then the adversary re-check. I'll write here when a word is wired on live, or by 15:30 either way. If it still isn't, the report will say plainly that the meaning loop works on a dev brain but not under the live brain's load.
