# v18 results (2026-10-25), against EXPECT-v18.md (frozen 10:13 UTC, sha256 2263a5006f3f, not changed)
Native SQLite (Python 3.10, SQLite 3.37.2) on the hub. A fresh brain: the hand-laid core, then the four teaching lines typed at the prompt, then the lines.

## T1 Hand-laid, and nothing else: holds
644 statements: 189 tables, 87 gates (views), 100 triggers, 4 indexes.
87 hand-laid neurons: heard, said, start, origin, and every token of the neuron-building run (born) and its teaching line. Each has its gate (label), its DNA table, its gate (entry) with its one trigger, its definition node, and its first shard pointing at that node.
13 working triggers, the whole of the hand-laid work: input_teach, input_bind, input_run (a line in), run_go (a run lands on its first gate), born_go (the born run fires; a word a line brought is looked up), fire_go (a trigger column runs its neuron's formula), hop_go (the hop neuron: receipt, BUILD front and end, fire, end, birth of the next word), bind_go (a DNA row's trigger column), build_go (the receipt between two BUILD gates, holes filled, to mother), secondary_go (a source's reply comes back as a run), end_teach, end_return, end_line.
Every rule of mine listed in the test is gone (checked in the block's text: LIMIT 8, agree, the SQL-verb rule, expected, decide and the memory hop, gaps, proc, step-back, derive, visit counters). One flag in my check came up true: "'?'" matched the neuron for the question mark, which the gate's text uses; it is not the echo.

## T2 Birth is a run: holds
After "born = ..." was taught, every word was born by the born run: its BUILD output (the run's receipt, holes filled from its data sheet) made the label rows, the DNA table, the gate, the gate's trigger, the definition node, and the first shard pointing at the definition node. dog: gate 293, first shard 904 -> its definition node (294, dog.definition).

## T3 Shards: holds
4665 shards over the whole brain, one sequence 1..4665, no gaps, no repeats.

## T4: holds. "BUILD SELECT 1 + 1 BUILD" said 2.

## T5 define : dog (dog not a neuron yet): holds
dog was born by the define run; all 32 source lines came back as runs (WordNet 8, Webster 1913 9, Moby 15); dog's definition node holds 32 rows, best first; the print is row 1, Webster 1913 sense 1. It took 0.4 s: about 700 new words in those 32 lines, each born by the 1,272-hop born run.
Printed: (Zool.) A quadruped of the genus {Canis}, esp. the domestic dog ({Canis familiaris}). Note: The dog is distinguished above all others of the inferior animals for intelligence, docility, and attachment to man. There are numerous carefully bred varieties, as the {akita}, {beagle}, {bloodhound}, {bulldog}, {coachdog}, {collie}, {Danish dog}, {foxhound}, {greyhound}, {mastiff}, {pointer}, {poodle}, {St. Bernard}, {setter}, {spaniel}, {spitz}, {terrier}, {German shepherd}, {pit bull}, {Chihuahua}, etc. There are also many mixed breeds, and partially domesticated varieties, as well as wild dogs, like the dingo and dhole. (See these names in the Vocabulary.) [1913 Webster +PJC]

The top six rows (source, score by my measure, start of text):
- gcide 5.482: (Zool.) A quadruped of the genus {Canis}, esp. the domestic dog ({Canis familiaris}). Note: The dog is disting
- gcide 4.441: {A dog in the manger}, an ugly-natured person who prevents others from enjoying what would be an advantage to 
- wn 3.911: a member of the genus Canis (probably descended from the common wolf) that has been domesticated by man since 
- wn 2.438: a hinged catch that fits into a notch of a ratchet to move a wheel forward or prevent it from moving backward
- gcide 2.37: (Mech.) (a) A grappling iron, with a claw or claws, for fastening into wood or other heavy articles, for the p
- gcide 1.898: a {hot dog}. [slang] [PJC] Note: Dog is used adjectively or in composition, commonly in the sense of relating 

## T6 define : dog again: holds. The same print in 0.4 s, no asks to any source.

## T7 define : cat: holds as written (the cat-animal sense from a dictionary); my script's string check said false
Printed (Merriam-Webster, its second line): any of a family (Felidae) of carnivorous usually solitary and nocturnal mammals (such as the domestic cat, lion, tiger, leopard, jaguar, cougar, wildcat, lynx, and cheetah)
My script only listed the first line of each dictionary as acceptable; that list was narrower than the written test. Took 155.3 s, 12 lines back.
define : store (recorded only): a mercantile establishment for the retail sale of goods or services; "he bought it at a shop on Cape Cod" [syn: {shop}, {store}] 2: a supply of something available for future use; "he brought back a large store of Cuban
(the stand-in WordNet row holds senses 1 and 2 run together, so both print). Took 149.5 s, all 17 lines back.

## T8: does not hold
canis and Canis had been born inside dog's returns (empty definition nodes). define : canis asked every source; no source holds canis, nothing came back, the definition node stayed empty, nothing printed, and the define run's last BUILD block failed ("near AND: syntax error"): it has no step for an empty definition node. What the brain should do when every source comes back empty is yours to say.

## What I changed during the build, and why (measured, not guessed)
1. The first version gave every shard its own SQL trigger carrying the whole hop: one birth took 10 s and memory reached 5.8 GB. Your words of 10-19 say "hop should be it's own neuron", "a column in the dna chard table just pointed to that trigger neuron", "if chard exists hits the chard, if not writes it", and your typed hop hands the next landing to mother. Now each neuron has one gate trigger: it hits the shard or writes it (the next shard number), hands it to the hop neuron, and mother lands the run on its remainder gate. A shard is a row, no SQL trigger of its own.
2. A table read at one hop and written by a deeper hop keeps its cursor open, so every deeper write grows with depth (measured on a bare chain: 0.025 ms per hop plain, 0.29 ms at 800 deep with one such table). Each step of the gate is now its own statement through mother. Result: about 0.3 ms per hop, flat with depth; a birth 0.4 to 0.6 s; memory under 100 MB for the test brain.
3. shard is INTEGER PRIMARY KEY, as in your typed table of 10-19 22:54.
4. The host's statement cache had kept every compiled landing (memory climbing): it holds 1,024 statements now.

## Open, yours to decide
- What the brain does when no source holds a word (T8).
- Words born inside a return are not looked up until a line asks for them (otherwise one word would pull in the whole dictionary). My policy, labelled.
- My "best" measure: dictionary lines first, then agreement with the other sources weighted by rarity. It ranks Webster's "A dog in the manger" second, above WordNet's sense 1.
- Spaces are neurons, as you said on 10-19; a word's own DNA rows then mostly read (space, space), and the word before and after shows up in the space neuron's rows.
- Not built yet, by your order in the handoff: the runs for the timeline and memory nodes at the end of a run, write the dna, read, write, move, copy; decide; the other brains.
