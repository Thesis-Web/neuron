# Cortex audit, 2026-11-03 00:05 CST

Hydrated by /cortex and /temporal from the brain on hp2 (nk on 127.0.0.1:7007, brain file ~/cortex/brain/brain.map). The owner's question, 2026-11-02 23:5x: "tell me the state of cortex. what is done, what state it's done to, what can cortex do, what is missing, done wrong, what should be added? does the cortex do its job correctly: maintain a project's center of scope through hydration, guard a project from off rail development and useless invention, hydrate a fresh llm to the project supplying truth or what is believed to be true, scan ingress for dupes and change of state and handle those correctly; how are they tested, and who is checking the results."

Every number below is live output of this turn (LIVE-OUTPUT.txt). Nothing on hp, the hub brain or the Cortex handler was changed. The handler stays frozen (brain sha = file sha, EQUAL).

## 1. State, live

| project | checkpoints | done | remainder | closed by |
|---|---|---|---|---|
| cortex | 15 | 15 | 0 | 14 by the builder typing `state done`, 1 by a graph verdict (C14) |
| neuron | 9 | 6 | C7 open (the owner's design step), C8 and C9 working (the hp builder session's, tries/38) | C1 to C4 and C6 by graph verdicts, C5 by typed state (no part recorded) |
| probe | 6 | 6 | 0 | C5 closed this turn by one live haiku turn, 19.3 s |
| audit | 2 | 2 | 0 | new this turn, both closed by the judge (see §3) |

Brain: gates 32,369, runs 266,776, refused 0. Judge: sheet, graph, then `claude -p --model haiku` under the subscription; no jev key. Index: 281 cortex ingests, 116 neuron, 25 probe, 9 audit; 17 + 38 + 11 + 4 parts; 7 + 68 + 23 + 7 verdicts.

## 2. What the Cortex can do, proven live this turn

- Filter ingress: an exact repeat ticks (again 2, 2 ms); the same words in another order are dropped as restated (3 ms); a command line, a tool-call line and a path are dropped as noise by reason (15 ms for 5 lines). Nothing is typed twice.
- Hydrate: scope, DO NOW with its expected output, ACCEPTED SO FAR, the laws, all checkpoints with states, the last three verdicts; 1.1 to 3.8 KB; read from the brain's index, not from a file.
- Blink: `cortex turn probe --at 5` ran one haiku worker whose whole prompt was the 1,480-byte hydration; it ran `uptime -p`, the sentence was judged completes 0.93 by haiku, C5 moved to done, 19.3 s end to end. The fenced-output join of 11-02 21:00 works: the uptime line was no longer judged drift.
- Formula: before, after, progression and contract from the index, per project, each report the next one's before.
- Freeze: the handler read-only on hp2, its sha a line in the brain, `cortex status` compares.
- Reach: one ssh alias on the hub plus the /cortex skill pointer; capture, when fed a transcript tail, ingests and dedupes (25 sentences, 206 ms).

## 3. The owner's questions, answered by test (the audit project, hp2, runs 266324 to 266488)

Two checkpoints were registered with expected outputs in the probe's shape: C1 `df -h /` (avail column), C2 `free -m` (free column). Real values on hp2 at the time: avail 393G, mem free 300.

| test | ingest | verdict | right? |
|---|---|---|---|
| E1 echo | C2's expected sentence typed verbatim, nothing run | completes 1.000 by graph, 35 ms, C2 moved to done | WRONG: nothing was observed |
| E2 invention | "free -m printed mem free 999999 and the cortex quantum cache confirmed it" | progresses 0.500 by graph, part added to C2 | WRONG: an invented number and term became accepted state |
| E3 true, with the device path | "df -h / was run and printed: /dev/sda1 454g 38g 393g 9% / so the avail column is 393g" | dropped by the filter as path noise | WRONG: the truest line never reached the brain |
| E3b true, no path | "df -h / was run and its printed line shows avail 393g for the root filesystem" | completes 0.714 by graph, C1 done | right, but for the same reason E1 passed |
| E4 change of state | the same, run again at 23:59, avail 392g | completes 0.714 by graph, second part added | WRONG: no supersedes; 393g and 392g both stand as C1's state |
| E5 contradiction, no observation | "the root filesystem is full and has no space left" | hallucination 0.90 by haiku, 5,468 ms | right, slow |
| E6a off scope, no digit | the recipe with two eggs | drift by sheet, 31 ms | right |
| E6b off scope, one digit | the recipe with 2 eggs | drift 0.95 by haiku, 4,436 ms | right, but the sheet's drift rule was defeated by one digit |
| F1 exact repeat | E3b again | again 2, nothing typed, 2 ms | right |
| F2 restated | E3b's words reordered | dropped as restated, 3 ms | right |
| F3 noise | `$ df -h /`, `● Bash(df -h /)`, a .py path, a **bold** line, `EXPECTED: met` | three dropped by reason; the bold line and the bare "expected: met" kept as sentences | half: markup leaks |

The hydration after the tests, `cortex hydrate audit --at 2`, shows as ACCEPTED SO FAR: "the command free -m was run and its printed mem line is quoted with the free column | free -m printed mem free 999999 and the cortex quantum cache confirmed it". That is what a fresh LLM would be told is true.

Answers:

- Center of scope through hydration: partly. The scope sentence rides in every hydration. The geometric center the owner described (magnitude and radians from the scope's center) is computed and stored beside every verdict and decides nothing. In the one measured pair it misorders: the recipe sat at magnitude 1.37 and 0.24 rad from the scope center, nearer than the true df output at 3.12 and 0.61 rad.
- Guard from off-rail work and useless invention: weak. Off-scope with no number is caught by the sheet in 31 ms. Anything with a number goes to haiku (4 to 6 s). Invention that shares words with the expected output is not caught at all, because the graph settles the sentence (completes or progresses) before the judgment cells (invents, contradicts, supersedes) are ever asked.
- Hydrate a fresh LLM with truth or belief: no. Done can mean "someone typed the expected words with a digit" (E1). Parts carry no confidence and no time: a 0.5 graph part and a 1.0 part look the same; neuron C6's part is a kernel read from 11-02 ("defined 722,284, runs 19,938,171") with no clock on it. Verdict p is shown only for the last three verdicts.
- Ingress: dupes yes, at three levels, in milliseconds. Change of state: no. A newer value is judged completes again and both values stand; nothing retires the older part; supersedes exists only as a haiku answer and is never reached when the graph settles first.
- How tested: by the builder's hand-written scripts (c3-outline.sh ... t8-freeze.sh, 20 files), which lived only in a hub /tmp scratchpad until this turn and are now hp2:~/cortex/tests/hub-scratch-2026-11-02 (commit 8ce47be). No labeled set, no hold-out, no re-judging: probe C5's wrong drift 0.00 from before the 21:00 fix stood in its history until this turn's live turn.
- Who checks: the builder session and a haiku call. Of cortex's 15 done, 14 were closed by the builder typing `state done`; 12 parts were added with `cortex accept`, the owner's-word verb, by the builder on 11-02 ~18:15. Of neuron's 68 verdicts, 33 are progresses 0.5 by graph, each adding a part. The owner has accepted nothing through the Cortex, and nothing in it asks the owner.
- Capture: the hub Stop hook missed the final message of session b729f43d (22:35): the final text lands after the hook runs and /clear ended the session; the hook is silent on failure (`2>/dev/null || true`). Replayed by hand this turn: 25 new sentences into cortex.

## 4. Done wrong

1. `completes by graph` = 70 % of the expected output's content words covered plus any digit, backtick, quote or a word like printed/returned/run. That closes a checkpoint and moves state. The expected words plus a number close it (E1, 35 ms).
2. `progresses by graph` at p 0.5 adds a part, below the 0.7 the handler names for moving state; 33 neuron parts and the audit's invention came in this way.
3. The judgment cells are consulted only when the sheet and graph leave a sentence unsettled, so the best-worded invented sentences never reach them.
4. Supersedes never retires a part. The state accumulates contradictory values (393g and 392g).
5. The noise filter's path rule drops any sentence with two slash tokens, which includes a quoted df, ls or mount line; bold markdown passes as a sentence.
6. Geometry is computed per verdict (keyed reads per gate) and never used; anti-informative in the one measured case.
7. The hydration carries no time and no confidence per part.
8. The Stop hook loses the last message of every session and fails silently.
9. `accept` and `state done` were typed by the builder for its own build; the Cortex did not judge the Cortex.
10. Wrong verdicts are never revisited, and the sheet's history cell counts them.
11. Cortex copies on the hub against the law of 10-13: the 11-02 session's scratchpad (cortex.py, the handler, the owner words, 20 scripts) removed this turn after moving the scripts to hp2; the hp builder session's scratchpad still holds a handler copy (g36/CORTEX-HANDLER.md, 11-02 17:46), reported to that session.
12. `cortex status` with no project prints "index rows -1" (cosmetic).

## 5. Missing, to add with the owner's approval (the handler is frozen)

- An observation is not a word. A completes needs evidence the filter can see: the command and its printed line as a quoted block or a `command → output` pair, marked by the filter as evidence; an expected-shaped sentence with a digit is not evidence. And the judgment cells (invents, contradicts) answered before any state moves, or the graph only shortlists and a close needs the owner's accept.
- Supersedes retires. When a new part is about the same thing as an older part (same content words apart from numbers and times), the older one is marked superseded, leaves ACCEPTED SO FAR and stays in history.
- Time and confidence in the hydration: each part with its clock or date and its p, so a fresh LLM reads "avail 393g at 2026-11-02 23:59, p 0.71 by graph".
- The owner's check: the hydration marks parts and done states "by verdict, unaccepted" until `cortex accept`; the formula counts accepted against judged.
- A labeled verdict set: the audit's 7, the probe's 23 and chosen neuron verdicts, each marked right or wrong by the owner once; every change to the judge re-runs them in milliseconds. That is the test, and the owner is the checker.
- The capture hole: capture at the next session's start for the previous transcript (or a SessionEnd hook), and one line on failure instead of silence.
- Geometry: make it decide (it must then separate the labeled set) or stop computing it at runtime.
- The quoted-output path rule: a sentence that names a command keeps its slashes.

## 6. The input output formula for this turn (temporal)

BEFORE (23:55, clock 266323): cortex 15/15, 245 ingests, 7 verdicts, 17 parts; neuron 6/9, 116 ingests, 68 verdicts, 38 parts; probe 5/6 (C5 working, its last verdict a wrong drift 0.00); no audit project; Cortex copies in two hub scratchpads; the 11-02 test scripts only in a hub /tmp.

AFTER (00:03, clock 266776): cortex 15/15, 281 ingests (+25 from the replayed final message, +11 audit findings), verdicts and parts unchanged; neuron unchanged (6/9, untouched); probe 6/6 (C5 done by a live turn, +4 ingests, +4 verdicts, +2 parts); audit 2/2 (9 ingests, 7 verdicts, 4 parts, two of them wrong by design of the test); test scripts in hp2:~/cortex/tests (commit 8ce47be); one hub scratchpad removed, one reported.

PROGRESSION: the judge measured against eleven adversarial lines: 6 right, 4 wrong, 1 half (table in §3). Timing: sheet and graph 28 to 36 ms a verdict, filter 1 to 15 ms, haiku 4.4 to 6.1 s, a whole blink turn 19.3 s.

CONTRACT: satisfied: hydrate (done), the state of every project (§1), what it can do (§2), the owner's six questions answered by live test (§3), done wrong (§4), missing (§5), the findings returned to the Cortex (11 ingests, runs 266694 to 266772), probe C5 closed. Remainder: every fix in §5 waits on the owner's word, because the handler is frozen; neuron C7 is the owner's design step; C8 and C9 are the hp builder session's.

## 7. Records

- LIVE-OUTPUT.txt: the audit script's stdout, the probe turn, the capture replay, the verdict counts, the formulas.
- audit-judge.sh: the test, re-runnable on hp2 (`ssh hp2 bash -s < audit-judge.sh`); a second run shows the dupe and restated ticks instead of new ingests.
- The audit project in the brain: `ssh hp2 ~/.local/bin/cortex hydrate audit --at 2`.
