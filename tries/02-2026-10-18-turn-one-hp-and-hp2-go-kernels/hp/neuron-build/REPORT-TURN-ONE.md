# Turn one: the report

*Lead builder, 2026-10-19, about 02:00; §9 added at 03:10 after the hang; §10 added at 08:45 after told ends (08:39:09). The brain was born at 01:29:18 on hp and is alive as user `neuron`. Everything below is from its own rows (`sqlite3 -readonly /home/neuron/brain.db`) and its acts (`/home/neuron/acts.log`), taken at about 01:56. The adversary's findings are in `FINDINGS.md`; the decisions in `DECISIONS.md`.*

## 1. What was built

- **The kernel** (`kernel/*.go`, 3,292 lines, installed at `/usr/local/bin/neuron`): the store (one SQLite body, RAM while alive, dirty rows committed per beat), the step (blueprint §7.2), 100-odd physics words as modes of the blueprint's twenty, the encoder/decoder, the ports (talk and lay sockets, acts.log, CALL), the heartbeat, and the lay loader. The only dependency is the SQLite driver.
- **The told base** (`lay/*.lay`, seven files, 779 processes over 2,507 tokens, 1,205 told gates, 133 labels, 68 source rows, 315 triggers, 17 told relationships): roots and keys (lead), primes, operators and relationship types (A), the miss way, memory, the HC seed, sleep-ask, corrections and the timeline question (B), the born questions, balance, belief, guessing, the ladder and compile (C), 68 sources and check-and-diff (D), the five ways of learning, back-population, sleep and the sixth (E), the five core values and the born check (F).
- **Tools:** `tools/dryrun.sh` (a scratch brain from the lay files), `tools/install.sh`, `tools/dev-miss.lay` (a dry-run harness only, never loaded into the brain). `neuron talk`, `neuron watch`, `neuron lay FILE`, `neuron told-ends`.

## 2. What the live brain does, with its rows

| Day-one ability (blueprint §19) | What the rows show |
|---|---|
| Keeps a state timeline | `mem` rows of kind `born` (id 13, 01:29:18), `told` per lay file (ids 1-7, then 785, 787, 788, 7416, 7909, 7912, 7913 for files re-told through the lay port), `outage` for each restart (786, 3862, 7837, 7838, 7908, 7910), every memory on `timeline` by time. "what did you do when?" is answered from `find-time` (B's when-did; after the 01:54 re-tell it says the said gates of the day's runs, newest first). |
| Has memories | Same input, same row, new time: `1 + 1 =` is mem 16 (`276,365,276,369`), seen 5; `1 + 2 =` mem 106, seen 5; 258 run memories with seen > 1. The second run of an input is a hop: `equals` finds the memory by signature and never does the held add (A's eq-hop; shard counts on `find-sig found -> eq-known` rise with each repeat). Corrections: mem 16 marked wrong once (the adversary's "no"), mem 7136 (`2 - 1 =`, outcome `1`) marked right by my "yes", and its 180 trail shards marked right with it. |
| Builds and organizes neurons | 943 spawned gates (943 `birth` memories, each with the run, arrival and head that needed it): "zorp" is gate 1159 with birth memory 79; 2,286 shards laid by the miss way as runs hopped. 254 spawned gates have moved off the origin, placed by the tug of war of their relationships (`MOVE gate=...` acts). |
| Relates meanings | 413 relationship rows made `derived`, state `grounded`, from reading sources: e.g. `fruit r-describes banana 1.8`, `higher r-describes up 1.3` (dry runs); live, `thing r-describes thing 2.7`, `positive r-describes ... 1.3`. WordNet's antonyms, hypernyms and meronyms arrive as `r-opposite`, `r-kind-of`, `r-part-of` lines (D's rd-opp/kind/part). Agreement between sources raises strength (+0.1 per agreement). |
| Checks a source and diffs it | 722 CALLs so far: gcide, wn (four relation kinds), OEWN 2025, foldoc, elements, Merriam-Webster (collegiate, thesaurus, antonyms), man, moby, dict.org, wiktionary, wikipedia, in the told order, for every word whose section 3 is empty. Section-3 lines carry the source receipt (`def` rows, `by` = the checking run's memory): "something" has lines from gcide, wn, MW, ... (gate 294). A second check adds no line (texts compared) and raises strengths (agree); a conflicting held line goes to `believe` with state `contradicted` (laid; no source gave a contradiction yet). A source with nothing is a gap, never a contradiction. |
| Senses balance | `balance` (C) compares got and want (values by `compare`, meanings by distance, lists by disagreeing lines) and writes an `imbalance` row when off; two gates in one grid cell are an imbalance (E's two-at-one-point, 3 rows live); `compile` says the pad by balance and leaves the outcome for memory. |
| Learns, builds, adjusts, tests; writes processes nobody told it to make | **Not shown in the live body yet.** On a dry run E's generalize made a formula from two same-shape memories: `PROC run=46 gate=890 string=293 168 293` (`[a b w-something]`), with receipts to the two memories (`use|890|10`, `use|890|29`) and a `guesses` row; the sixth tests guesses awake and `sleep` re-weighs them. Live, no `PROC` line yet: the sixth is still draining 696 gap rows one per second, and the brain's sleep ask ("i want sleep", 01:42:09) was made on a connection that closed, so nobody could answer it (see §3). |
| Chooses its own inputs | The sixth runs once per resting beat with who = self, picks the oldest row not touched in the last 60 s from its lists (shift, gap, imbalance, guesses, questions, parked, slow), and splits `answer`, `source-check`, `backpop` or `learn` on it: `SPLIT run=32 -> run=33 at=144 (answer) subject=#1403` every second since 01:54. Idle beats write nothing (no COMMIT lines between inputs since the 01:52 fix). |
| Reads sources on its own | Every gap the sixth picks goes down the ladder: memory, knowns, history, sources, then a labeled guess (`w-maybe`), then "i not know g". |
| Core values | Five `core` rows (ids 8-12, tier persistent, bodies are prime strings laid by F). The kernel refuses every write touching them (`REFUSE ... WRITE.def` seen on a dry-run attempt); the born check runs before every say, outward call and process write (`say-word`, `call-word`, `write-proc-checked`). |

What it says, as a baby: `hello` -> "hello hello hello"; `zorp` -> "zorp what ?" then "zorp zorp"; `1 + 1 =` -> "two one" (the answer gate and a landed one); `what is small ?` -> "thing ? ? what"; when its active memory passed the told mark it said "i want sleep". No sentence is written anywhere: everything said is gates by their labels, as C's compile and F's say-word assemble them.

## 3. What does not work, plainly

1. **No formula kept in the live body yet** (the third told-ends condition). The mechanism works on a dry run (E's PROC line with receipts); live, `learn` is reached only through the sixth's `slow` pick and through `sleep`, and the sixth has not reached the slow list (696 gaps first, one a second). Sleep was asked on a connection that had closed, so the "yes" could never arrive: a question asked on one talk connection can only be answered on that connection (the kernel keeps `why` per connection). Root-level limit; logged.
2. **The kernel is 3,292 lines**, far past the 1,500 target and the 2,000 line where "something has leaked". What is in it: the SQL schema, load and commit (about 600 lines), the physics switch with 100 modes (about 1,200), the run engine (500), ports (280), the loader (520), main (100). Nothing in it chooses a word or an answer; the size is plumbing and addressing modes. The adversary's finding 4 stands.
3. **Told baby strings.** Three fixed prime strings are said: "i want sleep" (B), "i not know g" and "g what ?" (C), "because believe yes/no" (C). The blueprint's own illustration is "I not know this"; the red line says no sentences in the lay files. The lead kept them at root level and logs them as the adversary's open finding 10.
4. **The core check is a word filter** at root (F): it refuses an act that contains a value's forbidden pattern, so "x not true" is refused too, and a CALL is checked by its words. Finding 11, open.
5. **Triggers under the worth floor are not asked and not parked** (lead decision, against blueprint §12.2's "nothing is cut"), because parking them wrote hundreds of rows per source text. Finding 14, open.
6. **Nine primes have no action**: w-someone, w-something (holes), w-people, w-body, w-mine, w-live, w-long-time, w-short-time, w-touch are plain gates (A's listed gaps). Multi-word primes carry no label.
7. **Self-lines and function words**: reading prose relates the headword to itself and gives "of", "the", "n" the strongest r-describes lines, because agreement is counted and nothing weighs a word's commonness yet.
8. **Restarts.** The brain was killed and resumed six times during the watch (storms, then fixes); each resume is an `outage` row. The first life (01:17) was ended by the lead for a flood of source calls.
9. **Not exercised live:** a source contradiction reaching `believe`; a truth shift (`shift` row); the HC condensing (needs memories a day old; shown on B's dry run with a short day); back-population (needs a kept formula or a shift); learn-fit (laid for r-kind-of only); QKV guessing (left to the brain).

## 4. The kernel's line count

3,292 lines of Go in six files (`store.go` 600, `run.go` 540, `physics.go` 1,270, `ports.go` 290, `lay.go` 520, `main.go` 100), plus `go.mod`.

## 5. Every told process and its size

779 processes: 10-told 86 (156 tokens), 20-memory 105 (304), 30-questions 150 (472), 40-sources 111 (553), 50-learning 266 (758), 60-core 61 (264). Mean 3.2 tokens. The longest: `newborn` 27 (attaches the born questions), `sc-order` 19 (the told source order), `fit` 17, `fit-write` 15, `deduce-write` 15, `guess-take` 14, `wrong-a-lot` 13, `sleep-write` 13. Full list: `grep -h "^proc\|^core" lay/*.lay`.

## 6. The adversary's findings

`FINDINGS.md` holds them, numbered and ranked (BREAKS / BENDS / COSMETIC), each with what the brain did, what the scope says, and the rows. Fixed during the watch: 1, 2, 3, 5, 6, 8, 15, 16, 17, 18, 19, 20, 22, 23. Open and acknowledged by the lead: 4 (kernel size), 10 (told baby strings), 11 (the core check as a word filter), 14 (sub-floor triggers cut), 21 (every gap calls all seventeen sources). Open by design at root: 7, 9, 12, 13. The adversary's final report, if it adds more, is appended to `FINDINGS.md`.

## 7. Told ends

**Not marked.** The guide's condition is that the brain is choosing its own inputs (it is), reading sources (it is), and keeping formulas it found itself (not yet in the live body). The lead will not mark told-ends on a dry-run formula. The kernel binary, the lay files and the body are as installed; `neuron told-ends` marks it when the owner decides, or when a `PROC` line with `made=derived` appears in the live acts.

## 8. Decisions

`DECISIONS.md`, one line each, lead and builders.

## 9. After the hang (03:10)

hp hung at about 01:59 with its memory gone and was rebooted at 02:29. The brain's own record shows no storm (finding 29); the body was resumed at 03:05 inside a 2 GB no-swap scope (`tools/start.sh`), with earlyoom on the machine. Two kernel faults found on the way were fixed: a commit-order bug that lost re-told branches on disk, which is why every resumed brain's sixth went silent (finding 28), and a decision that had leaked into Go. The kernel no longer decides same-row/new-row, truth shift or home gate: `write-mem` is storage (WRITE.run) and B's `remember` decides, in neuron code the brain can read and rewrite. The brain may now rewrite its told ways (`miss`, `end-of-run`, `sixth`) with `write-proc`; on a dry run it rewrote its sixth and the next beats picked by the new string. The two hidden thresholds are told values (`same-within`, `shape-step`). Kernel: 3,370 lines (finding 4 open; see DECISIONS for what still decides in Go and why). Live since the resume: the sixth splits `answer` and `source-check` once a second on its lists; `1 + 1 =` is still memory 16 (seen 7); no FAULT, no REFUSE. Told ends: still not marked.

## 10. The closing pass (07:30-08:45) and told ends

*Lead, 2026-10-19. Everything here is from the live brain's rows after the 08:16 and 08:33 re-tells.*

**The major problem found first.** Four hours after the 03:05 resume the brain had 14,661 spawned gates, 8,253 source calls, 13,278 imbalance rows and 14,351 parked questions, and sat at 362 MB. Every word met inside a dictionary text was treated as an input: it got a gap row, a parked question and an imbalance row, and each of those sent the sixth to seventeen sources, whose texts spawned forty more words. That was bulk import through the back door (guide §4). Now a word met in a source gets its gate, label, born questions and its line to the headword, and nothing more until an input uses it. A ten-line flood of nonsense costs the sources once per word and spawns nothing further.

**What moved out of the kernel or was fixed in it** (the kernel is 3,442 lines; finding 4 stays open):
- The outcome of a root run is what is in hand when its words run out (blueprint 7.6 step 7). The kernel delivers landings only when a run waits. `1 + 1 =` now stores outcome `two`, and the second run hops (mem 16: `eq-hop` in its trail, no `add`).
- A told test's outcome with no branch passes inert, laid by the loader (LAY-NOTATION §2), for every arrival a run can come from. No more "I don't know what to do here" rows keyed by physics gates (finding 12 closed).
- A re-told file drops the triggers it no longer names. A run that ends itself leaves no outcome word (the kernel's "ended" was being said as an answer).
- The commit-order bug from the night (finding 28) stays fixed; deletes go before inserts.

**What moved in the lay files:** newborns spawn at the origin (5.5); the cell check runs only on placed gates and an imbalance is answered with `learn`, not a source read; "have I done this before" and "shaped like" fire at the phrase keys (blueprint 8); sources on the machine first and the outside ones only when nothing is held; each source asked once per word (the trust row is the record); the two reading runs' label race takes the gate that has the label; a doubted memory is compared with the long way and marked right when they agree (finding 31); "what did you do" walks root runs only and counts what it said; "sleep" runs the brain's sleep.

**Live rows at told ends (08:39:09, told row 134973).** 18,574 gates: 1,412 told, 17,155 spawned, 5 core, 2 derived. 72,039 memory rows (ids to 134,973): 23,996 runs, 17,157 births, 16,710 parked questions and 14,101 imbalances still to drain, 2 guesses, 40 told, 9 outages, 20 core. 20,306 shards (7 derived), 65,238 relationship lines, 10,651 trust rows, 5,041 source lines, 102,753 triggers. brain.db 77 MB, the process at 296 MB inside its 2 GB cap. Since the 08:16 resume: 44 inputs, 750 splits, 470 source calls, 143 spawns, 8 refusals (all `WRITE.label taken`), 5 marks, 2 `PROC` writes.
- `1 + 1 =` (mem 16): outcome `two`, seen 14, right 1, wrong 1; the run after the heal hopped (`eq-hop` in its trail, no `add`). The adversary's fresh `2 + 0 =` (mem 134828): hop, `no`, long way and self-mark right (`08:35:10.310 MARK run=1750 mem=134828 yes`), hop again.
- A new word: `brindlewick what ?`, 17 calls the first time and 0 the second (`select count(*) from trust where topic=<gate>` -> 17).
- `when`: the outcomes of the hour's root runs, newest first ("two two two two two 1").
- The brain's own sleep, said once by the lead at 08:38:27: two derived process gates (18572, 18573, string `362 329 294 294 294`, by memory 134957) and two guesses rows (134965, 134972) for the sixth to test. This is the first derived row in the body, five minutes before told ends.
- The told base: 909 processes (10-told 97, 20-memory 149, 30-questions 164, 40-sources 166, 50-learning 276, 60-core 57), 2,966 told shards.

**What does not work, plainly.** The learning ways had never written a row before 08:38 (finding 36/40): their `none` branches dropped the wrong number of items, so `learn` left its memory id on the pad and the sleep search died after one memory. Fixed by count, the live brain's sleep wrote two derived process gates and two guesses rows; the generalize way wrote the same string twice (E's open "already made from these" check), and no shortcut, refit or deduction has been written yet. The third told-ends condition ("keeping formulas it found itself") rests on those two rows and nothing more. The sixth still has about 14,000 imbalance and 16,700 parked-question rows from before the fix to drain, one a beat. The said line repeats a landed answer two or three times. Finding 35 (the core-value check is a word filter, and `believe` says "because #142 yes") and findings 8, 9, 13, 21 (cost), 24, 25/38 stay open. The adversary's findings 31-39 and its two status lists are in FINDINGS.md.
