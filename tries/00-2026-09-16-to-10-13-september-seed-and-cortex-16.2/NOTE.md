# 00. The September line and Cortex 16.2 (2026-09-16 to 10-13)

**Status: dead. Nothing carries over.** NOW (10-18): "Nothing from Cortex carries over."

**What it was.** The versions audit (10-25), reconstructed from 4,663 tool-call captures because the code itself is gone: `cortex.db` with shared tables `gate`, `dna` (all neurons, typed by `kind`), `form`; 0 triggers ever written. Python wrote every row (`learn.py place()`, `add_gate`); traversal was a Python walker (`physics.py walk()`, LIMIT 20000), then the L0 interpreter (`l0.py`, 17 primitives, STEP_LIMIT 5,000,000). All lesson bodies LLM-typed. Brain-authored programs: 0 of 10,013 (the owner's record, 10-05).

**The owner's words.** 10-06: "it encoded input, decided unheard/conclude, scheduled thinking and executed everything. The neuron code was never in control." 10-16: "16.2 had almost not physics." 10-07: "the end of the line is that we roll back to 10-3-26 and trash the garbage". 10-05: "don't just turn it off,, delete it.. it was built wrong, and outside the brain.. get rid of it, so it doesn't get turned back on later."

**Audit.** Fails all four tests (versions audit, row 1). The independent 16.2 audit of 10-01 is pasted in `../../prose/2026-10-17-by-topic/NEURON_OWNER_WORDS_BY_TOPIC.md`, Appendix A, paste A15.

**What is in this folder.** Recovered pieces, downloaded to the hub on 10-21 while the versions audit was being prepared. My reading of what each is, from its contents (the dates and table names), marked as inference:

| File | What it is |
|---|---|
| `brain.db` (42 MB, downloaded 10-21 01:32) | A SQLite brain with tables `term`, `event`, `object`, `revision`, `current`, `protection`, `configuration`, `run`; configuration keys `entry:input`, `sealed`, `world`; 42,446 terms starting nil, true, false. Inference: the September seed/L0 line (the hub's bash history has `~/neuron-v3/runs/20260924_...`), not 16.2's `cortex.db`. |
| `seed-map.json`, `connected-07-summary.json`, `connected-07-recursive-acquisition.json`, `connected-07-recursive-program.json` | The seed programs (`nil?`, `not`, `type?`... from `seed/00-structure.ng`, origin TOLD) and a run summary with actors seed and owner. Same line as the brain above. |
| `cortex_plan.html`, `cortex_slice01_erd.html` (10-21 15:44) | A page titled "Cortex Plan" and an entity-relationship drawing of a Cortex slice. Rendered 10-21 from the Cortex-era data. |
| `Neuron Relation Map.zip` (10-21 15:48) | `index.html` + `data.json` (2.4 MB): the owner's relation map read from his 16.2 brain on 10-08 (reference draft §9: 35,597 words, 104,727 relation lines in 9 kinds; merged to one point per spelling for Six Pulls: 27,606 words). This map is what the 16.5 to 16.9 placement experiments were scored on. |
| `package-neuron-v16_2.sh`, `neuron-v16.2-review-20261013T114157Z-GtrCeC/` | The 10-13 capture script and what it left: `READ-ME.txt`, `DIRECTORY-SIZES.txt` (`/home/exnulla/neuron-v16.2` was 4.2 GB), `DISK-SPACE.txt`, and `FAILED.txt`: "INCOMPLETE: packaging exited with status 1. Do not treat these parts as a finished capture." The capture failed, which is why the code is gone. |
| `DISK_ALERT_20261014_2330.md` | An observer note from 10-14: C: at 14 GB free, "STOP making brain copies; delete yours (rule 703c)". |

The V12 builder's sheet and `plan.json` of 09-26, which drove this line, are in `../../specs/superseded/2026-09-26-v12-builders-sheet/`.

**Dropped as duplicates when archived:** `brain (1).db` (byte-identical to `brain.db`), `package-neuron-v16_2 (1).sh` (byte-identical).
