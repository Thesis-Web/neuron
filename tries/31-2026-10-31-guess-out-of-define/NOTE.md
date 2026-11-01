# tries/31 (2026-10-31 night): the guesser out of define, and a fault of mine found on the way

The owner, 2026-10-31 night: "what does the guesser have any fucking thing to do with source compare????? define is from source if you add the guesser into that you are adding the fucking guessing of basically a fucking llm..... that is not what guessing is for... fucking stop inventing your pieces... redesing the guessing part of the brain to be used only for my fucking design".

What the design says about guessing, what I built against it, and what is left open is in `GUESS-IN-THE-OWNERS-WORDS.md`. The open items are the owner's, and nothing was built for them.

## What was measured first, on the big kernel, reading only

Pastes took 59.8 s of a 60 s window and hops 0.29 s. One paste, `INSERT INTO guess.inbox`, took 42.4 s of it: 103 calls at 412 ms each (292 ms over the brain's life, so it grows). The corpus feed took 4.5 s. The corpus was 53.9 million rows, 2.9 GB on disk. The guesser had laid 11,978 guesses; one was ever answered by a person. The newest: `Minderbinder` gives `chins`, `NewScientist` gives `Sumit`, `Iulianus` gives `Bosoms`.

## What changed

`guess_out.py` reads the formula bound to each shard from the brain, cuts the one span that touches the guessing brain, types what is left at the prompt, and rebinds the shard: define (before 1 and before 5, trigger `:`) and why (before 5). No kernel code, no rows deleted. The guessing brain stays attached and its rows stay, draft 5.6: "never lost". To undo: bind the shards back to the old runs.

An unknown now stays an unknown. Nothing fills the cell.

## The test (`test_guess_distinct.py`, written before the change)

Two small kernels on the slice sources, each in its own folder and port; `hp-g31.sh`. Control: old lines. Changed: `guess_out.py`. Same lines into both, the full chain on, run to the end.

| Check | Control (guesser in) | Changed (guesser out) |
|---|---|---|
| G1 corpus rows added | 19,170 | 0 |
| G2 guesses added | 2,900 to 2,902 | 0 |
| Paste time | 268.7 s, 278.4 s | 131.4 s, 131.9 s |
| Runs, two tries | 53,594 and 53,580 | 44,489 and 44,489 |
| Hops, two tries | 14,206,107 and 14,197,299 | 12,693,653 and 12,693,653 |

G3, the source work: 2,067 source returns the same in both, 1,618 relationship rows the same in both.

**G3 as finally written still prints FAIL.** Its third part compares the set of symbols each define read, and 3 to 5 entries differ, every one a define that read nothing (`Nations`, `Originally`, `Situated`). They are not source work, and the names change from try to try on the control itself. I report it as it printed. I did not widen the test again to make it pass.

G1 and G2 fail on the old lines, as they must. G3's own negative control: a third kernel with one source emptied fails it, 676 returns and 674 relationship rows short.

The changed kernel gave the same run and hop counts both tries. The control did not. Taking the guesser out made the chain repeatable.

The test was changed twice before anything was applied live, and both changes are in its header: "stays empty" could not be true after the recipe's own lines, and comparing mother's replies and the known/unknown split compared the order of the chain, not the sources. The runs that showed each are `g31-run1-asan.txt` and the early hp-g31 output.

The recipe also has a race I did not cause tonight but must name: the bind of define's (the sixth, :) shard can run before that shard exists, so on a small kernel it may hold no call. In one run it held on one kernel and not the other, which gave 100 returns against 2,082 and looked like a huge effect of the guesser. It was not. `bind5.py` puts both in the big kernel's state.

## The fault found on the way: mine, in the cut

The small kernel died with status 139. A debug copy under AddressSanitizer: heap-use-after-free at `land` (nk.c:161), freed by `try_compact`. When a run repeats an earlier one it borrows that run's symbols at its start (`dedupe_check`), but the earlier run's `again` count was raised only at the repeat's end (`ended`). Compaction leaves a run with `again > 0` alone, so in between it could free symbols a run was still landing on. It can crash, or it can read garbage as the next symbol and key a landing wrongly with no error. I cannot say whether that has already happened on the big brain.

The fix: raise `again` when the repeat starts. One count moved, no new field. Checked: AddressSanitizer 0 reports on both small kernels through the full chain (44,000 to 53,000 runs). With every line drained, old binary against itself 21 of 22 tables identical, old against fixed 21 of 22; the one table that differs is `run`, in both pairs, which holds the clock.

`again` is raised even if the repeat never reaches its end. That can only over-count by one on a stalled run.

## Applied to the big kernel on hp, the night of 2026-10-31 to 11-01

Snapshot `out/snap-20261031-233036`: 1,340 s, 18 GB, 6,281,612 runs, read back and counted before the kernel was stopped. The kernel stopped, nk.c changed, built, loaded from that snapshot in about 18 minutes, then `guess_out.py` on the loaded brain. define's two shards went from run 1098 to 6281759, why's from 1218 to 6281809; neither new run mentions the guessing brain. The chain carried on.

| Measured on the big kernel | Before | After |
|---|---|---|
| Defines a minute | 190 to 292 | 799 (740, 861, 795 in three 77 s windows) |
| Guesses added | 14,417 in all | 0 |
| Refused | 1 | 1 |
| Memory a define | about 46 KB | about 18 KB, over only 4 minutes |

I had estimated about 1,350 a minute from the rest of one profile window. It came in at 799. That estimate was too high.

At 00:26: 140,687 points defined, 539,267 waiting. The costliest paste now is the define's known and unknown test, 25 ms a define. Then the sixth's collection, 7 ms, and the ask.

## A second fault of mine, seen in the first measurement after the load

The rate after the load was 110 a minute. The sixth's paste had gone from 5.6 ms to 222 ms. A load brings back tables, not indexes laid at the prompt, so the two indexes of TEACH-8 were gone. Laid again (mother: ok), 799 a minute. This was in the record: it is why the index line was the last line of the journal after the 18:18 resume. I did not read it as a rule then. `resume` now lays them.

## What `run-on-hp.sh resume` does now

Lays the two indexes, runs `guess_out.py` (it reads the brain and does nothing on a brain already cut), and waits 2,400 s for a load instead of 900. The 900 s limit passed before the 18 minute load ended, and the door did not come up until I started it.

`typed-lines.txt` in `snap-20261031-233036` was changed by hand from 131 to 137, so a resume does not replay the six lines typed after the load. Those lines carry filled run numbers, and replaying them over a different history would bind define to the wrong run, the trap of 10-30. The same two effects come from the resume itself, read from the brain.

## Not done

- **The hub is not changed.** Its why line still feeds and asks the guesser, and its sixth still sends nothing (tries/30: the focus lines were never typed). Typing the focus lines as they stand would start it. The hub's why has to be cut first.
- **A `fresh` brain gets the guesser back.** LINES-nk and TEACH-LINES still carry it. On a fresh brain `guess_out.py` has to follow TEACH-8.
- **The 14,417 guesses and the 55 million corpus rows are kept.** Nothing was deleted. The cells a guess filled are still filled, as returns from gate 15.
- **Whether the use-after-free already keyed a landing wrongly on the big brain is not known.** There is no check for it.
- **The guessing brain is not redesigned.** The design's fixed parts are in `GUESS-IN-THE-OWNERS-WORDS.md`; its four open items are the owner's. Until then it is attached and unused.
