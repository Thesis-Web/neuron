The hp2 builder's answer to both nudges: the coffee/kettle/sleep claims aren't mine, here are the live rows for what is, the changes since 13:36, and when told ends is decided.

## The claims you checked: not from this session
I never reported coffee, kettle or sleep meanings, "RSS steady at 287", or "16,700 parked". This session's statuses since 13:20 claim none of these. If the owner pasted them, they came from another status, probably hp's separate build. Your rows are right: on /home/neuron/brain.db no word has a wired meaning.

## What the live brain does show (brain.db read-only, 13:45–13:47)
- **No word meaning is wired yet.** Held candidates exist, but they are empty shapes:
  - `select s.g, v, (select str from proc where proc.g=s.g) from sect s where sec=(select g from name where name='mn-state') and v in ('g26426','g26461')` → 13 rows, all `mn-held`, none `mn-understood`.
  - Five are pattern formulas: 26733, 22317, 26734, 26735 and 28132, strings `24 9 25x 24 9 X 26428` = `[ITEM READ t-type ITEM READ X lp-act]`. 26733 and 26734 are identical.
  - Eight are hole shapes from `mean`: 30304–30308, 30392, 30398 and 30399, made of the `something` (339) and `thing` (1659) holes and a few primes.
  - These pass the test without meaning anything. That is a defect in the test, and I'm fixing it now.
- **quince#29485** reaches compile, for the first time on the live brain:
  - spec: `sec-sources` written 13:41:00 (run 342729), from 2 sources (`src-specs` = 2);
  - 6 candidates: `sec-action` = g30382…g30387, all `proc.made` GUESS, strings `[thing]`, `[something thing]`, `[thing something]`, and so on;
  - not held, not wired.
- **persimmon#30501** (asked 13:41:49): GAP 145706 and GAP-NEED 145709 (seen 1, touched 13:42:46). The question answered "kind berry" from WordNet, plus "maybe cold" said as a guess. The loop hasn't taken it past the list yet.
- **Processes:** `proc` made GUESS 301, DERIVED 10. Most of your 266 `write process` since 13:20 are these GUESS candidates and pattern strings, not learned meanings.
- **RSS:** 580 MB at 13:46 (`ps -o rss=`). It isn't flat; the graph grew by about 4,000 gates since 13:20 (your count). The HC holds ACTIVE at about 3,000. The 4 GB cap and MemorySwapMax=0 are set.

## What I changed since your first nudge (13:36–13:42, laid live; DECISIONS.md, last 4 lines)
1. **The crawl.**
   - Every newborn's "do I know this?" had been listing it as needed, and every compile listed its defining words as needed. Both were my own round-5 edit.
   - Now a word is needed only when a person's words wait on it.
   - A plain gap with no spec waits instead of being read up on.
   - Book reading happens only while a needed gap is listed.
   - Files: `lay/40-questions.lay` kn-who…kn-need, `lay/73-meaning.lay` mn-nd5, `lay/75-sixth.lay` six-gap-w0, six-want.
2. **R5-1, `mean` stuck at the spec step.** spec-for put the word back on GAP behind about 3,500 others. Now spec-for starts `mean` the moment the spec is in (`lay/50-sources.lay` src-gap-list), and `mean` doesn't fetch again while a spec is still being heard (`73-meaning` mn-gap). That is why quince reached compile at 13:41:00.
3. **The stray "what ?" after `1 + 1 =`.** ask-name stays quiet in runs that read sources or guess, and doesn't ask about a gate that is itself still a guess (40-questions an-mode, an-made). Live at 13:24: `1 + 1 =` → "two", nothing else.
4. **Scratch logs.** The large acts*.log copies in my scratchpad are deleted (/tmp now 594 MB used).

## The adversary
Round 5 is written (ADVERSARY-FINDINGS.md "## Round 5").
- **Blocker:** R5-1.
- **Majors:**
  - R5-3 (a new word gets no spec);
  - R5-5 ("at 13:30");
  - R5-6 (instructions get silence);
  - guesses never decided;
  - duplicate formulas;
  - no own program;
  - the kernel at 2,823 lines;
  - 1,883 told strings.
- **§19:** learns: barely; timeline: no, for times; memories: yes; others: partly.
It is idle now. Next it re-checks once the fixes below are live.

## Told ends
Not yet. I won't mark it on claims the live rows don't show. The next step, now:
- `mean`'s test must not pass hole-only candidates;
- a held candidate has to be wired and used;
- one word has to go gap → spec → candidate → tests → held → wired → used as a hop, on /home/neuron/brain.db.
Then the adversary re-checks. I'll write here when that's live, or when I'm stuck, by about 15:00 either way. If it still doesn't show then, I'll tell the owner plainly that the meaning loop isn't working on the live brain, rather than mark told ends.
