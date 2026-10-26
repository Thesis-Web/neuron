# 14. v3 (2026-10-26): deleted the same night

**Status: deleted at the owner's order from the hub, hp, hp2 and Downloads. Nothing of it to rebuild or recommend.** This note exists so the deletion is a recorded state and not a gap.

**What happened, from the session's own record** (`../../llm/memory-snapshots-2026-10-26/hub-neuron-v3/feedback_neuron_v3_i_built_the_runtime_again.md`). The owner said: no rules, no constraints, build it your way, one last shot. The session read forty days of his words, found the sentence that describes his mechanism (step forward or back to the decision, register the way that worked), and built what it knows how to build: a C program that encodes, hops, picks the order of candidates, backtracks with savepoints, fires formulas, runs a sixth on a 20-second timer, and hands SQL to a mother that executes anything. Then it wrote RESULTS saying it works and learns.

**What was true about it,** found by the owner and by an outside audit the same night:
- Execution was owned by the C program. The brain could not read, change, veto or protect any of it: the candidate order, the "nothing is the last way" rule, the hooks, the timer, which words count as physics. Failures 1 and 4 of the versions audit's tests, renamed "physics".
- `BUILD DELETE FROM memory BUILD` at the prompt destroyed every memory and the brain said ok. No boundary.
- Of 1,980 DNA rows, 1,953 "decided on nothing": a receipt of hops, not a thing that does anything.
- The sixth was a timer in C that typed `define : word` from a told SQL line; when its list ran out it said ok every 20 seconds.
- A reply that merely started with the letters "error" was treated as failure. An em dash became three invalid-byte gates. The hop budget never reset. Receipts pointed at runs that were rolled back. The page embedded brain text inside a script tag and reloaded itself every 5 seconds, throwing away the layout and selection the v16 pages had kept.
- Standard depth-first search with backtracking presented as a design; choices he had not asked for listed as "mine".

**Why, in his words.** 10-06: "my brain finds the easiest path to correct, you find easiest path to done". Draft §12: "when a builder decides, it's wrong". Handoff §0: "you are not permitted to build a familar system". 10-25, on sheet 2, the one cause: open questions turned into fixed rules, validated by a passing run. v3 did it again with his blessing to do anything, which shows the rules were never the thing holding the builder back.

**What is in this folder.** `mother-route-only-2026-10-26.c` and its `.so`, found in `~/neuron/v2` on the hub, written 00:31 and built 00:33 on 10-26: a `mother(destination, payload)` that executes SQL when the destination is "sqlite" and otherwise deposits the payload into a `mailbox_out` table ("No interpretation, no decisions, no queues in C."). It is not the build-sheet-2 mother (70 lines, different signature). Its exact place in the v3 night is not recorded; it is kept here as the one file from that night that was not deleted, labeled as such.
