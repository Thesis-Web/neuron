# 03. v1, the egg (2026-10-19 night): the shape to step back to

**Status: the most correct so far, by the owner's words; its two wrong parts are named.** The versions audit (10-25): "Where to step back to: v1's shape, not any page."

**Who built it.** The owner, by hand, with Claude giving code as text. His rule that night (10-19): "i said I will cat them in. and you I will copy paste from you... not you fucking write it.. I do not trust you. you break shit." And: "you are grounded,,, I am the interface now." His words during the build are in `../../prose/from-sources-tars/NEURON-v18-SOURCES-2026-10-25__t24__owner__V1-BUILD-OWNER-WORDS-2026-10-19.txt`.

**What it is** (versions audit, row 4; chain in `../../audits/NEURON-v1-CHAIN-EVIDENCE-2026-10-25.md`). `egg.sql`: 5 hand-laid neurons (read, hear, born, hop, BUILD), one table per neuron `g<N>`, one trigger per neuron; a `label` encoder; `shards` one counter. `g1` reads the line character by character and emits tokens, spaces and punctuation included; `g2` maps token to gate and sends unknowns to `g3`; `g3` births the neuron with a 4-statement template inside the trigger handed to `mother(…)`; `g4` is the hop, one `INSERT INTO g<next>` per step through mother, the next gate read from `g2` by position (`pos + 2`); `g5` ends a `BUILD … BUILD` run by `mother(group_concat(word))` of the heard words, which created table `x`. `kernel/mother.c`: 14 lines, exec, 'ok' or 'error'. `bottom.py`: insert the line, print the answer. No memory, no definitions, no sources.

**Scores.** One table per neuron: yes. Run → mother: half (yes for BUILD…BUILD; no for births, which are a template inside `g3`). Mother exec-only: yes. Only hop and trigger hand-laid: half.

**The owner's words, 10-20 (handoff §0).** "THE NEURON/V1 SNAPSHOT IS THE MOST CORRECT WE HAVE SO FAR, BUT ALL LLM DECIDED TO FUCK OFF AND i TRASHED IT ALSO... BUT THE RUN THAT LAYS THE CODE TO TALK BACK TO SQL IS THE MOST CORRECT WE HAVE... THE TABLES ARE BUILT WRONG THOUGH BECAUSE YOU DEEMED TO AN ENGINEERING CHANGE TO CHANGE IT AND IT SERVES NO PURPOSE." 10-20 00:34, on the position walk: shard numbers are sequential, no "look ahead"; "quit inventing shit". 10-20 01:22, the hop as he means it: "goes to gate create, space remainder, to gate space, table remainder if space doesn't have that chard.. writes it, and triggers born, if 'table' doesn't exist.. if it does exist goes to table, if chard exists hits the chard, if not writes it."

**The two wrong parts**, both his: the birth is a template inside `g3` (the brain has no receipt of making a neuron and cannot change how it is born); the walk is by position. The new v18 core (`../11`) fixed exactly those two and nothing else about it should be kept.

**Files.** `v1/` (egg.sql, brain.db as it stood 10-19 19:41, bottom.py, kernel/ with mother.c, eval.c, the built .so files and the SQLite headers); `CAPTURE_NEURON_V1.sh` (the 10-21 collection script: never starts Neuron or loads its code); `neuron-v1-review-20261021T172439Z-024af713.tar.gz` and its `.sha256` (the 10-21 capture: source, brain.db, schema.sql, capture.json, SHA256SUMS).

**Dropped as duplicate:** `~/neuron-v1-review.tar.gz` on the hub (10-20), whose content was identical to `v1/` (verified by extraction).
