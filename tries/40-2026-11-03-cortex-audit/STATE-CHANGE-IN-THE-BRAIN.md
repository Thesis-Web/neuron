# State change in the brain: what the Cortex brain on hp2 already holds (read 2026-11-03 00:20 CST)

The owner, 2026-11-03 ~00:10 (his words): "state cannot change unless the dna shard of that neuron is changed? ... if the state changed, it means a relationship pull changed, a dna shard trigger changed, or the memory row changed and became a new row ... this data is just words in a graph with meta data attaching it to the neuron project ... when the data hits the gate and the dna row is written for that run, presto that run dna shard on that gate becomes part of the neuron project ... if it's a common sentence that has been stored before we write a full new memory just timestamp index the counter, and now add the project name, and maybe category, component, topic, concept ... runs that already exist don't have to be built again they just need the timestamp and meta data for that ingest ... if the run exists already for the project, presto we should know that it's a dupe ... when you have a run of neurons that looks almost the same for a project but one or two neurons are out of line, presto ---> judge these two shapes look similar this is prior state, this is new ingest, do they correlate? is one drift invention, hallucination? should I change state, leave it the same or the two have no correlation and keep both ... the shape of the graph is so important it will make drift, invention, hallucination stick out like a thumb."

Every row below is a keyed read of the Cortex brain (nk copy on hp2, 127.0.0.1:7007). Nothing was changed except one typed line (the dupe test).

## 1. What one ingest leaves in the brain

Run 266417, `cortex ingest audit : the command df -h / was run and its printed line shows avail 393g for the root filesystem`:
- `run`: id 266417, arrival 1, hops 27, ended, complete, same_as 0, again 0, kept 1.
- `seq`: 47 gates in order. The shape. Digits are single gates: 393g is the gates 3, 9, 3, g. The project is in the shape: gates cortex, ingest, audit at positions 1, 3, 5.
- `hit`: one row per step: gate, before, next, had 1 (the dna row existed), shard 16, ord. The hop trail.
- `run_receipt`: one row per step (receipts ARE kept for typed lines: 418,780 receipts over 28,103 runs).
- `run_memory`: ONE row, keyed at the END gate of the run (29087 filesystem): input = the whole gate string, again 0, last_at, last_run. "The end of that run writes the memory": confirmed.
- `dna` on the gates it crossed (audit, avail, filesystem, quantum, cache): still ONE row each, the educated row (before 156, trigger 68 ':', spawn 13367, times 0). The ingest wrote no new dna shard and ticked none. The project is not on the gate; it is only in the run's shape and in the front door's Python index `cx`.

## 2. The dupe, by the kernel itself

The front door ticks repeats in its index and never types them (handler decision 15:08: "the kernel's own repeat rule needs kept receipts, which a typed line's are not"). That premise is false now: receipts are kept. Typed at the main prompt a second time, the kernel answered by itself:
- new run 267054: `same_as 266417`, no memory row of its own;
- the first run's memory row ticked: `again 1, last_run 267054, last_at 267054`.
That is the owner's "timestamp index the counter". It is in the brain, keyed by run, and the Cortex does not use it.

## 3. The shapes, by the kernel's seq, against the expected output's own run

| ingest | shared gates with the expected run | out of line | digit gates out of line |
|---|---|---|---|
| E1 echo (C2's expected sentence typed as an ingest) | 20 of 20 content gates; differs only in the prefix (expected 2 vs ingest) | 0 | 0 |
| E3b true 393g (against C1's expected) | 18 | 7: 3 9 g root filesystem shows ingest | 2 |
| E4 true 392g, run again at 23:59 | 18 | 11: 2 3 5 9 g at again root filesystem shows ingest | 4 |
| E3b vs E4 (prior state vs new ingest) | 25 | second only: at 2 again 5 | 2 |
| E5 contradiction, no observation | 7 (the prefix and stop gates) | 11: space machine this of root full left no has filesystem ingest | 0 |
| E6a recipe | 7 (the prefix and stop gates) | 12 | 0 |
| E2 invention vs C2's expected | 11 | 5: confirmed quantum cache it 9 | 1 (the repeated 9) |

Read in the owner's terms, from seq alone, keyed by run, deterministic:
- Same shape as the expected's own run with nothing out of line = the expected sentence itself, not an observation (the echo). The current judge called it completes 1.000.
- The expected's shape plus digit gates out of line = a value was observed.
- Two project runs of the same shape differing only in digit gates (and a time) = the same thing with a new value: change of state, supersede. The current judge called it completes again and kept both.
- Out-of-line gates that no run of this project has crossed before = the thumb that sticks out (quantum, cache, confirmed). The current judge never looked: it settled by word coverage first.
- Only the prefix and stop gates shared = no correlation: drift. The sheet gets this one right by word sets.

## 4. What is missing, in the kernel's own terms (for the owner; not built)

- The judge's cells should be the brain's rows, not Python word sets: the ingest run's seq against the prior-state runs' seqs (the part runs the index already holds), shared / out of line / digit gates / gates new to the project. All keyed by run.
- "Has this gate crossed a run of this project before" is not a keyed read today, because an ingest writes no per-project dna shard on its gates (dna stays one educated row per gate). The owner's design puts the project and its metadata on the shard at the gate when the run writes it; that is kernel work (nk, the hp builder's and the owner's), not the front door's.
- Repeats should reach the kernel: same_as and the memory row's again/last_run are the dupe, with the project in the shape; the Python index tick duplicates the brain and hides repeats from it.
- Asking the brain about a state change in prose: no verb exists. Tonight it is keyed reads of run, seq, hit, run_memory. The `memory` door command is a size report, not a question.
