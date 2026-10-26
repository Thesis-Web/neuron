---
name: project_neuron_build_sheet_egg_20261025
description: "The owner's build sheet and egg (2026-10-25 evening) - v1's shape rebuilt from his 10-19/20 words; egg.sql + mother.c + bottom.py in Downloads/NEURON-BUILD-SHEET-2026-10-25; tested on hub and hp; born run typed once, births automatic, define dog prints WordNet; hop flat 1.3-1.7 ms; what he will hit next"
metadata:
  node_type: memory
  type: project
  originSessionId: 95237a7f-7d7c-47a3-a249-06f9202b6633
  modified: 2026-10-25T23:37:03.114Z
---

Owner 10-25: "an instruction manual on how to build it, such that I can just copy and paste in what I need... that gets me to a build state where I can prompt engineer the teaching of the brain... for me to build not you".
Delivered: Downloads/NEURON-BUILD-SHEET-2026-10-25.md + folder NEURON-BUILD-SHEET-2026-10-25/ (mother.c ~60 lines + sqlite headers, egg.sql 264 gates / 272 tables / 92 views / 93 triggers, BORN-RUN.txt 541 tokens, bottom.py prompt, look.sql eyes, sources/*.db from sat172 slices, gen_egg2.py). Scratch copy: scratchpad/egg/. hp test folder: hp:~/neuron-egg-test (works on SQLite 3.46.1).
Design (his words, v1 shape): ear -> encoder (words; digits/space/punct each a token) -> hop from heard -> gate view "<N>" with one INSTEAD OF trigger t<N> (hit or write DNA row via mother statements) -> hop view (receipt, fire, build, end, born, land via mother(text, run)) -> mother exec-only C (ok/rows/error, carries outboxes to secondary, writes refusal to output, queues locked DROP in later). Born run = typed line with cells (var dna/gate/trig/def/mem/defgate written by born); bind = BUILD INSERT INTO g12 (run) VALUES (2); fire = replay the newest run in a neuron's memory node as a sub-run with cells at/before/after/next/prev. define taught in 3 typed lines (run, bind to define.memory, UPDATE row trigger WHERE arrival = 1).
Measured: hop 1.2-1.7 ms flat (600/1200/2400 tokens 0.7/1.7/3.7 s hub; 4.1 s hp); born run 0.3-0.4 s; shards one sequence verified.
Open for him (listed in sheet §12): new DNA rows have NULL trigger; cells newest-of-run else newest; memory/timeline runs not typed yet (hook = end neuron's memory node); definition node not written by define; text in input/sheet/secondary/output; spaces double hops; DROP waits in later.
**How to apply:** any further build starts from this folder and his typed lines; never reintroduce rule tables; every write inside a nesting frame goes through mother (SQLite INSERT cursors stay open to statement end). Related: [[project_neuron_versions_audit_20261025]], [[project_neuron_173_forensic_audit_20261025]], [[feedback_known_failures_checklist]].
