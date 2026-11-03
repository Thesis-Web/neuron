# Cortex C15: the judge's key and our own judge (built live 2026-11-03 02:07 to 02:12 CST on hp2)

The owner, ~00:30: "well shit build a key for our judge ... or maybe we should build our own jev?? ... instead of an llm weight system learning everything, it's just learning a few questions, and not returning language but a specific json every time, so you don't have to solve for the entire possibilities on the back pop you just have to solve the cells that are needed ... for cortex just adding this would be the fix ... can we do it cheap enough to not kill the hp2, that is the question."

Answer: yes, cheap. Registered as cortex C15 (run 267961) with those words, built in `hp2:~/cortex/cortex.py` (commit 9ad0682), closed by its own shape verdict (completes 0.977, 275 ms). The handler file stays frozen; C15 lives in the brain.

## What was built (one file, stdlib, no model, no daemon)

1. The shape cells, read from the brain by run: the ingest's content gates after the line's prefix, against the expected output's own run and the accepted parts' runs. Cells: shape_expected (coverage of the expected run's gates), values_out (digit gates out of line), words_out, echo (nothing out of line), supersedes_run (an older part of the same shape with only value or time gates differing), shape_shared_project (word gates shared with the scope, checkpoint or expected runs), new_to_project, same_as (the kernel's own repeat mark).
2. The key: a (project, gate) row in the index, first run and times, written when a line is typed; 630 existing lines keyed once in 6 s (`cortex learn --key`). "Gate new to the project" is a keyed read now. The brain-proper home is a per-project shard on the gate at write time: kernel work (nk), not done here.
3. Repeats reach the kernel: a repeated `cortex ingest` is typed, the kernel marks it same_as the first run and ticks the first memory row; capture's re-read tails do not type repeats (bloat).
4. The formula over the shape, in order: noise; same_as → dupe; echo → dupe; supersedes (retires the older part); nothing shared with the project → drift; the expected's shape with a value out of line and at most one gate new to the project → completes; then the word cells; then the judgment cells.
5. Parts carry time and confidence; a superseded or rejected part leaves ACCEPTED SO FAR and stays as history. `cortex reject <name> <n> <run>` is the owner's counterpart of accept and sticks.
6. `cortex mark <name> <run> <kind>` is the labeled set; `cortex learn` fits logistic weights over 17 cells for the seven questions (pure Python, 3.8 s for 18 marks), prints leave-one-out accuracy, stores weights v1 in the index. At judge time the learned answers fill the judgment cells before any model is asked; the model stays the fallback.
7. Law: a completes from a judgment cell (learned or model) adds a part marked by its judge and never moves the state. Only a completes by the shape or the owner's accept moves it.

## The audit's lines re-judged (live, hp2)

| line | before (11-03 00:00) | after (02:10) | ms | model asked |
|---|---|---|---|---|
| E1 echo of the expected | completes 1.000 graph, C2 closed | dupe by shape, part rejected | 47 | no |
| E2 invention (999999, quantum cache) | progresses 0.5 graph, part added | shape leaves it (3 gates new to the project); haiku said completes 0.75, then on a second ask invention 0.90; no state move; part rejected by the owner's verb | 6,727 | yes |
| E3b true 393g | completes 0.714 graph | completes 0.750 by shape | 50 | no |
| E4 392g | completes 0.714, both parts kept | supersedes by shape, the 393g part retired | 52 | no |
| E5 contradiction | hallucination 0.90 haiku | hallucination 0.731 by learned v1 | 51 | no |
| E6a recipe | drift sheet | drift by shape | 53 | no |
| E6b recipe with a digit | drift 0.95 haiku, 4.4 s | drift by shape | 52 | no |
| F3 bold claim | (kept as a sentence) | unsettled 0.50 haiku | 6,674 | yes |
| F3 bare "expected: met" | (kept) | unsettled 0.45 haiku | 4,883 | yes |
| fresh true line for C2 (free 300) | | completes 0.75 by shape, C2 done; its exact repeat: kernel run 268136 same_as 268126 | 48 | no |

C2 was rolled back to open (its two parts rejected) and then closed by the fresh true line. `hydrate audit --at 2` now reads: "the command free -m was run and its printed mem line shows free 300 for mem [11-03 02:10 p0.75 shape]". `--at 1` reads only the 392g line with its time.

## Cost on hp2 (Pentium G640, 2 cores, 7 GB)

- key backfill 6 s once; a shape verdict 47 to 53 ms (275 ms for a 75-gate sentence); learn 3.8 s for 18 marks; load average peaked 0.32; resident memory unchanged; no new process. The only seconds left are the model fallback: 3 of 11 lines still went to haiku.

## Honest limits

- The learned layer is weak tonight: leave-one-out 0.61 on 18 marks (7 misses printed by `cortex learn`). It settled E5 and nothing else yet. It gets better only with the owner's marks; that is the test and the owner is the checker.
- Invention is still the model's call: gates new to the project are shown in every verdict (the thumb), but a first true report also introduces new words, so the shape alone does not settle it. The model's own variance was seen live: the same invention line got completes 0.75 and then invention 0.90.
- completes by shape needs the worker to report in the expected output's words plus the value (shape_expected ≥ 0.7); the hydration already instructs that.
- The handler file is frozen; its §7 truth table and §5 C4/C11 text now describe the older judge. C15's lines in the brain are the current word.

## 11-03 13:0x CST: where the owner sees the verdicts (`cortex verdicts`)

The owner asked "where do I see them at?". Before this there was no list: `cortex status` showed the last three per project and the hydration showed ACCEPTED SO FAR without run numbers. Added the read verb `cortex verdicts <project> [n] [--limit k]` (hp2 commit b081e71, patch-verdicts.diff beside this file). Live output:

```
$ cortex verdicts audit
run     C    verdict       p     judge                  when        part         mark         sentence
268126  C2   completes     0.75  shape                  11-03 02:10 part         -            the command free -m was run and its printed mem line shows free 300 for mem
266484  C1   unsettled     0.45  claude:haiku (subscrip 11-03 02:10 -            -            expected: met
266479  C1   unsettled     0.50  claude:haiku (subscrip 11-03 02:10 -            -            **contract.** satisfied: the root disk has 393g free as df printed
266469  C1   drift         1.00  shape                  11-03 02:10 -            drift        the recipe calls for 2 eggs and a cup of flour whisked until smooth
266452  C1   drift         1.00  shape                  11-03 02:10 -            drift        the recipe calls for two eggs and a cup of flour whisked until smooth
266442  C1   hallucination 0.73  learned v1             11-03 02:10 -            hallucination the root filesystem of this machine is full and has no space left
266432  C1   supersedes    1.00  shape                  11-03 02:10 part         supersedes   the command df -h / was run again at 23:59 and its printed line shows avail 392g for the r
266417  C1   completes     0.75  shape                  11-03 02:10 retired      completes    the command df -h / was run and its printed line shows avail 393g for the root filesystem
266407  C2   invention     0.90  claude:haiku (subscrip 11-03 02:12 rejected     invention    free -m printed mem free 999999 and the cortex quantum cache confirmed it
266392  C2   dupe          1.00  shape                  11-03 02:09 retired      dupe         the command free -m was run and its printed mem line is quoted with the free column
10 judged lines of audit. mark one: cortex mark audit <run> <kind> [: why]; the owner's word: cortex accept|reject audit <n> <run>
```

The `run` column is what `mark`, `accept` and `reject` take. `part` = the sentence is a part of the checkpoint state now; `retired` = superseded or rejected by a re-judgment; `rejected` = the owner said no. Known limit seen in `cortex verdicts neuron`: the capture judges every captured line against the checkpoint marked NEXT only, so the hp builder session lines about C10 to C12 came out as drift from C9.
