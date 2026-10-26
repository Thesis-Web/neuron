# v18 test, written before any v18 code (2026-10-25). Not to be changed after the run.

## Your words this is built from
- Handoff §0: "you are only allowed to hand lay the neurons that make the table for the run, and make it possible to hop and trigger... the rest will be laid by the neuron, via runs that you prompt in." "The only code you can write is the bottom which only accepts an output from the neurons and inputs that output to the sqlite prompt." "the bottom is permitted to have a sql output that inputs an error, or a response from sql back to the neuron graph."
- 10-19 21:52: "THE NEURONS WILL HAVE TO HAVE THE RUNS FOR CREATE TABLE (IF REMAINDER GATE DOESN'T EXIST)... CREATE ---> TABLE ---> (INSERT (remainder)) -> INTERGER --> etc... it will land at build which is the last step of the create new table run.... build will then send that run reciept to the py and py will forward it to sql... all the puncation must be correct"
- 10-19 23:03 / 23:08: "( , integer , primary, key, ... ; ... all neurons of their own"; "every punctuation, special char, all of it has to have it's own neuron"; "if create table (var a) .. then it would create a table of what ever is sitting at the newest memory at var a"
- 10-19 23:40: "every new neuron first dna chard is the definition... a new gate, new dna table and new defintion node is born all at the same time,,, one action 5 triggers at least... write row in the dna, and find source and write row in defintion"
- 10-19 23:27: "a column in the dna chard table just pointed to that trigger neuron"; 10-20 00:34-00:39: "shard numbers are sequential"; no look-ahead; no invention without reason.
- 10-20 01:22: "goes to gate create, space remainder, to gate space, table remainder if space doesn't have that chard .. writes it, and triggers born, if "table" doesn't exist.. if it does exist goes to table, if chard exists hits the chard, if not writes it."
- 10-25: "define is a run through the neurons like every thing else... it has a run data sheet like every other run... define : dog = tell me the dictionary definition of dog, compare your sources and give me the best definition.... if dog exists... it's the first memory of that neuron... look up definition memory print.... if the neuron doesn't exist create it and then print the definition memory, that better be there."

## T1 Hand-laid, and nothing else
The bottom (mother: runs the text the neurons send at the SQL prompt; a source reply or SQL's answer or error comes back into the graph), the encoder (label: word to gate), the neurons that make the table (every token of the neuron-building run), the hop (a shard's own hop trigger, the write of a missing shard), the trigger column (a hit shard whose trigger column points at a neuron runs that neuron's formula), BUILD front and end (the run's receipt between them goes to mother; the reply goes into the run's data sheet).
Deleted, all mine: run at most 8 source lines; agree; nothing fires after an SQL verb; the teacher's expected answer overwrites; the exact-line memory hop (decide) and memory/timeline at a run's end (not yet laid by runs); the "?" echo; every canned sentence; gaps; taught/learned/automated counts; step-back; derive/deduce at birth; a word with its own formula fires on every pass; visit counters on DNA rows; the depth cap; the 14 action gates, the 40 SQL word gates and the physics names as hand-laid gates.

## T2 Birth is a run
After "born = <the neuron-building run>" is taught at the prompt, a new word's gate, its DNA table, its gate (entry), its miss trigger, its definition node and its first shard (trigger column -> the definition node) all come from that run's BUILD output (its receipt, holes filled from its data sheet), not from a template in a trigger.

## T3 Shards: one sequence over the whole brain, no gaps, no repeats.

## T4 Spaces and punctuation are neurons; "BUILD SELECT 1 + 1 BUILD" typed at the prompt says 2.

## T5 define : dog, dog not a neuron yet
dog is born by the define run; every source line comes back as a run (wn 8 + gcide 9 + moby 15 = 32 return runs); dog's definition node holds 32 rows, best first; the print is row 1; row 1 is the domestic-dog sense from a dictionary (WordNet sense 1 or Webster 1913 sense 1).
## T6 define : dog again: the same print, no new asks to any source.
## T7 define : cat: the cat-animal sense from a dictionary. define : store: recorded only (I have no rule from you for which store sense is best).
## T8 A word born inside a return (canis): empty definition node until asked; define : canis asks the sources then prints.

## The measure for "best" (mine, labelled; yours to change)
For each returned line: for every other source, the most it shares with any one of that source's lines, each shared gate weighted 1 / (how many of this word's returned lines hold it); summed over the other sources. Dictionary lines (wn, gcide, mw) first, then by that score.
