---
name: project_neuron_v1_build_state_20261021
description: "State of the owner's hand build ~/neuron/v1 on 2026-10-21 (egg.sql, bottom.py, kernel/mother.so, brain.db unchanged since 10-19 19:41) and the spec audit: what matches the owner's words, what contradicts them, what is not built"
metadata:
  node_type: memory
  type: project
  originSessionId: 7c20c611-9fe3-4487-be20-478341fdbaa9
  modified: 2026-10-21T17:50:47.593Z
---

**Files:** egg.sql (5 physics neurons g1 read, g2 hear, g3 born, g4 hop, g5 BUILD; label = encoder; shards(n) counter; input(id,text,time,answer)), bottom.py (writes a typed line to input, prints input.answer), kernel/mother.c (runs SQL text, returns 'ok'/'error:'), kernel/eval.c unused. brain.db: 7 runs, 104 shards, 25 labels; the brain born CREATE, TABLE, x, (, a, ), ;, space and 'hello', 'world' itself.

**Matches the owner's words:** one table per neuron, rows = DNA; every token incl. space and punctuation is a neuron; shard rows record arrival + remainder; gapless map-wide shard numbers, no look-ahead; unknown word is born (table + trigger + blank definition node + first shard pointing at the definition); BUILD front and end hands the line to mother and the error comes back into the brain; the bottom is only I/O; hop is its own neuron reached by a hop.

**Contradicts the owner's words (2026-10-21 audit):**
1. Positional walk: hear stores the sentence by pos, hop looks up pos+2, BUILD checks pos=1 (367: never a position column; the run carries its remainder). run/pos columns are not in the owner's typed shard (shard, arrival, remainder, trigger).
2. Born runs in a batch during hear, before the run; owner: born fires at the gate when the remainder has no gate.
3. No shard reuse: a known (arrival, remainder) is written again every pass (probe: 3 walks = 3 rows, 1 distinct pair); arrival is never used to select.
4. The shard does not store the way to the next gate; mother recomputes every hop. Owner's own typed shard laid a static per-shard hop trigger.
5. The trigger pointer (to the definition table) is never followed.
6. Born is a canned SQL template in the g3 trigger, not a run through word neurons + BUILD (362, 380); owner allowed it only as a temporary chicken-and-egg scaffold.
7. read/hear tokenize inside the brain by per-character recursion: ~1,000-char line cap; the owner questioned both ("the encoder does this?").
8. BUILD's product is rebuilt from hear's typed words, not read off the gates walked.
9. mother drops SELECT rows (BUILD SELECT → 'ok').
10. Tables named g<N> instead of the word; owner handoff says the tables are "built wrong" by an engineering change (g<N> name, run/pos columns, trigger TEXT→INTEGER are the three differences from what the owner typed).

**Not built yet (owner's stated next order):** memory at run end, receipt row, timeline/clock, trigger neurons fired from shard pointers, DROP NEURON, the neuron-building run as word neurons, source lookup for definitions.

Related: [[reference_neuron_spec_sources]], [[feedback_never_write_in_v1_owner_pastes]].
