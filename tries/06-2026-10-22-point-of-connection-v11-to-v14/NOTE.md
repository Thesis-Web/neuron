# 06. Point Of Connection v11 to v14 (2026-10-22)

**Status: superseded by v15 (`../07`).**

**v11 (other session), v12, v13: drawings.** Versions audit, row 6: no SQLite; "mother" is a counter (v11) or a regex toy SQL engine over arrays (v13, v12). "The headers claim 'sixteen physics tables with their triggers'; none exist. Every `ensureGate` prints 'mother makes its table, its trigger, a blank definition node' and makes neither." v13 shipped broken (a shadowed variable threw on first render); the owner found it "completely broken, cannot input the text"; from this came the rule to smoke-test every page under a fake DOM and a real headless browser before publishing.

**v14: the first real SQLite** (row 7). Six physics tables (state, memory, relation, definition, timeline, formula) + 2 triggers + 7 attached source stand-ins. Neurons, DNA rows and hops are still JS objects (`addGate`, `landOn`); a JS loop hops. `mother(S, text)` = `S.sql.exec(text)` plus outbox pickup, but her return path checks, keeps or sets aside rows and updates trust in JS. Formula statements sliced to `;` in JS, holes quoted in JS. Scores: no, half, half, no. The owner, 10-22, asked to fix it: the physics played in JS while called triggers.

**The owner's rules from this day.** "do not just over write the model I have also. create a new one, such that I can compare and diff the two on my own." (Every later version is a new file beside the old.) And, after a build drifted into training a model on the GPU: "triple check my words... some what you are doing might be off scope."

**Tests.** `tests/NEURON-v14-CHECKS-AND-EXPERIMENTS-2026-10-22.md`: the sixteen physics as SQLite triggers with 44 checks and controls (that became v15), the envelope speed fix, E5 (place in the graph → formula: 1 of 5 verbs, p = 0.42, not better than chance), E6 (the owner's shape "what is your name?": 18 small forms narrowed by tests), E8 ("how did you do that?" answered from the brain's own rows; the memory hop returns a stale answer on repeat), E7 (guessing brain on GPU: designed, not trained, scope flagged). The measured router and AS facts of the same day are in `../../llm/memory-snapshots-2026-10-26/hub-neuron-v1/project_neuron_router_and_as_facts_20261022.md`: a trigger cannot write into another attached database, so mother is the only way out of a brain; round trips 0.011 ms in-process, 0.22 ms to a resident process, 69 ms per spawned process.

**Research from the same day:** `../../research/NEURON-MEANING-DISCOVERY-2026-10-22.md`, `NEURON-MEANINGS-TESTED-2026-10-22.md`, `NEURON-ROOT-TEST-WEBSTER-2026-10-22.md`.

**Files.** The four pages. **Dropped as duplicate:** `NEURON-POINT-OF-CONNECTION-2026-10-21.html`, byte-identical to the v13 page.
