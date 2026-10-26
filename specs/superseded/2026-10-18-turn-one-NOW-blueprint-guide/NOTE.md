# Superseded: the turn-one spec set (2026-10-18 and 10-19)

Five documents, written by the Claude session of 10-18 from the owner interview (the interview itself is his words: `../../../prose/2026-10-18-NOW-interview/`).

| File | What it was |
|---|---|
| `NEURON-NOW-2026-10-18.md` | What Neuron is, as of 10-18: the baby that can become Isaac Newton; day-one abilities; the hypotheses, with OPEN items the builder decides. |
| `NEURON-BLUEPRINT-2026-10-18.md` | How turn one is built: §0 three rules (words are nothing, the action is the meaning; learning is compute, using is hops; know before you guess); a Go kernel with 20 physics words, "the only code Claude writes", target 1,500 lines; the graph, shards, runs, triggers, memory tiers, sources, the sixth, sleep, core values. |
| `NEURON-BUILDER-GUIDE-2026-10-18.md` | The traps (§3, §4), one turn with helpers (§5), the adversary (§6), done (§7). |
| `NEURON-MEANING-BLUEPRINT-2026-10-19.md` | Added during the builds: roots, primes, words as formulas; the seven-step gap/spec/compile/test/hold/wire/use loop; "Everything here is a guess". |
| `NEURON-UPDATE-2026-10-19.md` | The MW keys, the source list, the `/home/james` mode, QKV on the guessing side only, the research file. |

**What it drove.** The two Go-kernel builds on hp (Fable) and hp2 (Opus), 10-18 night to 10-19 afternoon: `../../../tries/02-...`.

**Why it is not current.** Both builds failed all four tests of the versions audit. The design put the physics in Go where the brain could not read or change it, and the lay notation became a program the builders wrote the brain's thinking in (hp audit M12, hp2 audit M16). The owner, 10-19, on hp: "go code sitting in the neurons that the brain cannot use, or understand is not the same as having the physics access to the brain"; on hp2: "the brain has to understand and be able to use it's physics to improve or build itself"; 10-19 23:40: "the easy way is to do it outside, but outside can never be adjusted... my way the brain can change it how ever it want's to change it just by changing the run". The handoff of 10-20 (§0): "The only code you can write is the bottom which only accepts an output from the neurons and inputs that output to the sqlite prompt.. no other outside code is permitted." The reference draft of 10-23 replaced NOW; its §2.8: the physics list is "kept as small as possible... The end goal is no physics list."

**What still stands.** The three rules of Blueprint §0 and the traps of Guide §3 and §4 are not contradicted by anything later; they are folded into `../../../LLM-HANDLER.md`. The adversary method (§6: breaks only where the build differs from the scope; findings with rows) is what the 10-25 audits did. The source list of 10-19 is kept in `../../../research/`.

**What was wrong in the guide itself, found later.** It told the builder to "decide whatever the documents leave open, and log it" (§5). The 10-25 audit of build sheet 2 named exactly that as the one cause under every failure: open questions turned into fixed rules, validated by a passing run. The owner (draft §12): "when a builder decides, it's wrong."
