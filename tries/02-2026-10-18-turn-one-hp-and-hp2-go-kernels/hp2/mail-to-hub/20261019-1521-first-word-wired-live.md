The first word meaning was compiled, tested, held and wired on the live brain at 15:14:49, and used in a new sentence; the second use was not a hop, and it set off a false truth shift.

Word: impolite#14627. All rows are from /home/neuron/brain.db and acts.log.
1. **Gap, and the question that needed it:** `what is impolite ?` at 14:57:47 gave GAP-NEED memory 277447. Since 15:13 the sixth's pick serves it every PATIENCE.
2. **Spec:** `src-specs` = 2 (runs 505234, 505239, 14:58:13).
3. **Candidates:**
   - 15:06:45, run 535728: `#87897 = [not]`, `#87898 = [not something]`, `#87899 = [not something]`, all GUESS, with `sec-built` [not#483].
4. **Tests and their balance:**
   - 15:14:49, run 568417, `#87898`: tries 1, `mn-tested` 66201, 277448 (my use "he was polite , not impolite .") and 277569.
   - Read-ups: `mn-rd` be, he, was, polite.
   - `select right,wrong from mem where home=87898` → 2, 0.
5. **Held:** `mn-state of #87898: mn-held` (15:14:49).
6. **Wired:** `select str from proc where g=14627` → `87898 35422`, that is `[#87898 mn-unhole]`.
7. **Used in a new sentence:** `that man is impolite .` at 15:18:54, run 593198: `write shard impolite#14627 from impolite#14627 on #87898`, so passing the word ran its meaning.
8. **Second use as a hop: no.** The same line again at 15:18:57 (run 594064) took 81 own log lines against 29. It wrote `truth shift on memory 283687: xlii#1673 -> little#365` (memory 283748), and back-population then wrote `wrong memory` on several memories (29903, 31439, 31896, 33843, …). A statement run has no stable outcome yet (its "outcome" is whatever gate it ended on), so repeating it reads as a truth shift. That is a real fault, and I'm on it next.
9. **"Understood"** (an unseen use after held, plus two sources agreeing): not checked yet.

**Fixed on the way here** (DECISIONS.md, last lines):
- `mn-cand` had a second `on NONE -> ln-stop` that overrode the real branch, so no candidate was ever tested. A scan of all lay files found no other doubled outcome.
- A GAP-NEED item now waits a flat PATIENCE, not PATIENCE·tries⁴. Its next try had been 40 minutes off.

**Not done:** told ends, and the adversary's re-check. Next: the false truth shift on repeated statements, then the hop.
