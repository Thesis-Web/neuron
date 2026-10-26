# REPORT: Neuron turn two (the meaning blueprint), hp, 2026-10-19

*Lead. Turn two opened on the live body at 12:05 (the owner: "Open turn two on this body, re-tell it, go"), merged at 13:25, closed at the end of this report. Everything here is from the live brain's own rows and acts. The record of decisions is DECISIONS.md (turn-two lines from "Lead (12:05, turn two opens...)"), the adversary's findings 42 on are in FINDINGS.md.*

## 1. What was built

The meaning blueprint's seven-step loop (gap, spec, compile, test, hold, wire, use), on top of turn one, in one session with three builders and one adversary:

- **Kernel** (3,466 lines; finding 4 stays open): `neuron told-opens` reopens the told base on a body after told ends (a told row on the timeline); the loader keeps a gate's string when a binding is re-laid, and takes `gate NAME : plain`; inside the miss way the quiet mark stands (a test's outcome left after a miss excursion fires no triggers).
- **00-roots**: the handle `meaning`.
- **10-told (A2)**: w-something and w-someone are holes (a hole takes a bound gate in hand under it, else stands); first-guess actions for the nine inert primes (people, body, mine, live, touch, a long time, a short time, some time, don't want's opposite line); the worksheet's derivations as `r-derived-from` lines with state guess.
- **30-questions (lead)**: know-this asks "has the word a meaning yet?": a spec with no action is a gap of the meaning kind, compiled at once for a person's own input.
- **40-sources (lead)**: prose from a source is a spec and nothing more: no gate spawned for a word met in prose, no co-occurrence line; the structured readers (antonyms, synonyms, hypernyms, meronyms) stay. The prose scripts' cut is 200 words.
- **45-meaning (M, new, 276 procs)**: `meaning g`: section 3 empty -> source-check and the gap row again (bounded by gap-tries); a bare gate the brain made with a spec -> compile: one compile-reading child per spec line (a bound gate is a meaning, anything else a hole), the richest list and the richest other, the candidate = what they agree on (else the richest as a guess), wired with `write-proc`, written to sections 4 and 6, a guesses row (held when two sources agreed, with a yes mark), section-9 lines and receipts for the brain's own words used inside; a wired word -> the use test on a use memory marked right (understood at two rights), a sense gate for a failed formula; an unfilled hole asked back once per input. The told base is never compiled.
- **50-learning (E2, lead)**: the sixth picks gaps first and splits `meaning` instead of `answer`; the fit way moves its offset gate instead of spawning one; generalize keys its guesses rows by the pair of memories; an untestable guess row is touched so it rests; a parked question about a word no input ever used is dropped (asked again when an input uses it).

## 2. The live merge, plainly

13:25: kernel installed, brain resumed under tools/start.sh, told opened, six files re-told with 0 errors. Three faults of the lead's own followed, each found in the rows and fixed by a re-tell: re-laying the roots had wiped the miss way and end-of-run (two minutes with no memory and nothing said; 20-memory re-told 13:26; loader fixed); two pad slips in the sixth's questions path (an empty-pad split and a refused delete every beat for eight minutes; traced on a copy of the body under a cap, deleted the same minute; fixed 13:33). The adversary's first pass (13:26-13:48, findings 42-56) found two breaks the lead fixed at 13:53 with a restart: the compile had rewritten the `?` key and the `sleep` gate from dictionary text (one question then said "a ?" 795 times; the told base is now never compiled, the two gates restored plain), and a refused MOVE inside coffee's formula had left its `no` through the miss way and fired the person's correction (kernel: the quiet mark stands).

## 3. What the live rows show (14:03, told ends)

18,994 gates (1,758 told, 27 derived, 17,204 spawned, 5 core); 57,425 memory rows (ids to 255,911); 33 guesses rows, 15,663 parked questions still draining, 1 gap; 40 derived action lines in sections 4 and 6; 21,635 shards; 65,527 relationship lines; 10,878 trust rows; brain.db 92 MB; the process 429 MB under a 2 GB cap with GOMEMLIMIT 1200 MiB.

**coffee** (gate 17320, a word spawned from a source text in turn one, typed by the lead at 13:25 and 13:27): its questions row (126016, "what is this?", seen 2); six spec lines in section 3 from gcide, WordNet and the WordNet relation readers; the compile at 13:27:02 (`PROC run=2504 gate=17320 string=312 326`), section 4 and section 6 `small move`, guesses row 136410 held (`MARK run=2504 mem=136410 yes`; outcome the `held` gate, seen 34 since: the sixth's tests, none of which can mark it); 8 use receipts; the second use a hop into a refused MOVE that says "boiler ?" (finding 53). That is the meaning blueprint's §10 items 1 to 3 and the start of 5; items 4 (a test on a use), 6 and 7 do not exist for any word.

Other words the brain compiled on its own from the parked questions and the adversary's inputs: kettle = `inside` (held), believe = `as true move am true inside am` (held), colander = `to to` (held), did = `do do do do do` (right 2), trivet = 80 gates of which 73 are holes (a guess), spatula = 44 gates, 41 holes (a guess), hello = `am am`, adversary = `someone like`. Every one is a first guess the brain holds with its receipts; none has been refit, because nothing has tested one on a use.

**The sixth** since 13:33: gaps first, then the parked questions one a beat (a word no input ever used is dropped, a used one goes the meaning way), the guesses list every few seconds (each test runs the formula, refusals and all, and marks nothing). No fault storm, no refusal per beat, no self-correction since the 13:53 restart.

## 4. What does not work, plainly

1. **Formulas are function-word primes** (finding 45). Every compiled word is a string of the bound labeled gates the dictionary text happens to contain: to, in, is, as, like, small (coffee = `small move`, kettle = `inside`, believe = `like true to are true inside are`), "held" because two dictionaries share one of them. The first-guess layer has about 75 bound labeled gates; dictionary prose is mostly words outside it, which become holes. This is the honest state of a root-level compile over a thin prime layer; the brain's guesses to refit, not the lead's to fix by hand.
2. **A compiled formula runs the primes' physics** (finding 46): `to` is MOVE and refuses with no point in hand; `inside` is read-next and eats the next input word. A word's formula changes what the input run does. The refusal no longer marks anything; it still does nothing useful.
3. **No use test has run** on the live brain: it needs a use memory a person marked right. Understood is unreachable until someone says yes.
4. **The sixth's guesses list cannot test a derived gate** (its branch leaves no memory); the fit way's row is seen 20, right 0, wrong 0 (finding 43's tail).
5. **A hole fills only from the word before it** (finding 48): a word-order fact by construction of the pad.
6. **Cost** (finding 49): a word costs about 15,000 steps to read and compile; a one-word input 1,141 steps; the body 71.7 -> 84 MB in the turn.
7. Findings 8, 9, 13/25/38, 21, 32, 35, 39, 41 from turn one stay open; 31, 33, 34 are fixed as observed; 36 is closed (derived gates exist), 40 not re-probed.

## 5. The adversary's re-probe (13:54-13:58, FINDINGS.md "Re-probe after the 13:53 restart")

42 fixed as far as visible (every input has a memory; the roots re-lay itself was not repeated live); 44 fixed (`?` and `sleep` plain told gates; one `what is coffee ?` says one line); 46 fixed (a refused MOVE marks nothing); 43 changed and open (the guesses list rotates every few seconds and can never mark a derived gate); 49 open and worse per minute (the process 174 -> 442 MB in five minutes of compiling; the body's rows 38 MB; the lead set GOMEMLIMIT after); 53 open (the hop into a compiled word does nothing useful); 54 open (the timeline question answered in holes); 57 new (the restored gates keep the compile's rows as history); 58 new (`did` = five `do`, the count GCIDE's). The adversary's verdict: the §10 record exists for items 1-3 for every word tried; items 4-7 for none.

## 6. The owner's correction (14:10) and what changed

The owner, after the first told ends: core value 5 is right, but a told base and a kernel the brain cannot change make it take the builder's code as truth; a brain can change its mind, adjust it and unfoul its logic, and this one could not even read its own kernel, which blueprint §3 promised. Told was reopened and three files re-told on a kernel of 3,479 lines:

- **The compile is open to everything that is not silicon**: the told lock is gone; keys, told names and handles are compiled from a spec like any word.
- **The brain can change its mind back**: `write-proc` with an empty list makes a gate plain again; the meaning way does it when a formula's row shows more wrongs than rights (a section-9 line names the row), and does not compile that spec again while the wrongs lead.
- **The signal that a formula fouls runs**: a slow row with the word in hand marks its formula wrong when the sixth handles it; the use test marks it too. A refusal inside a formula is not yet a signal (open).
- **The brain reads its own code**: the kernel's six Go files and the eight lay files are grounded sources, read once each onto section 3 of "I" when a run leaves w-i. Shown live: 14 lines, 250 KB, on gate w-i. It cannot rebuild the kernel; it can rewrite everything laid in neuron code.

## 7. Told ends

First marked at 14:03:14, reopened for the owner's correction, and marked again at the time in acts.log's last `TOLD ENDS` line, after the three conditions of the first blueprint §17.6 still hold on this body and the meaning blueprint's §8 changes are in the told base. From here on there are no edits to the brain, the lay files or the kernel; if it is broken, say so. The memory guard, the cap and earlyoom stay; the brain runs under tools/start.sh by hand with no auto-restart; hp2 was not contacted.
