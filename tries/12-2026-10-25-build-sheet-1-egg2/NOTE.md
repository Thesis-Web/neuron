# 12. Build sheet 1, the egg (2026-10-25 evening, 18:32)

**Status: superseded by build sheet 2 (`../13`) the same night, after the owner's rebuttal.**

**What he asked for** (10-25): "an instruction manual on how to build it, such that I can just copy and paste in what I need... that gets me to a build state where I can prompt engineer the teaching of the brain... for me to build not you".

**What was delivered.** `NEURON-BUILD-SHEET-2026-10-25.md` (the instructions, with every file pasted in full) and the folder: `mother.c` (about 60 lines: runs the text, answers ok / rows / error, carries source outboxes into secondary input, writes a refusal into the run's output, queues a DROP that SQLite refuses mid-run into `later`), the SQLite headers, `mother-hub-x86_64.so`, `egg.sql` (264 gates, 7 physics neurons, 81 word neurons, the ear, encoder, shard counter, receipt, sheet, secondary, output, later), `BORN-RUN.txt` (541 tokens), `bottom.py`, `look.sql`, `sources/` (seven source brains as SQLite files from the 470-word slices), `gen_egg2.py`. v1's shape rebuilt from his 10-19 and 10-20 words: ear → encoder → hop from heard → gate view with one INSTEAD OF trigger → hop view → mother. Tested on the hub (SQLite 3.37.2) and on hp (3.46.1). Measured: hop 1.2 to 1.7 ms flat; born run 0.3 to 0.4 s; define dog prints WordNet.

**The owner's rebuttal, 10-26 00:41.** The sheet was "incomplete, out of order, or built wrong"; `later` is a decision in mother ("why is the later queue needed"); `build_go` is code outside the brain's reach ("explain"); the bootstrap stopped where prompt engineering starts and he needs the prompts that create definition, memory and timeline; "core min... not plus bloat, invention, drift"; everything must be in the sheet; "you have fought me on all the things a database cannot do... many of which you can do.... how do you kill a db .exit".

**Mistakes recorded** (checklist #73 to #80): defending the build against an audit point by point instead of testing each point; a work-around inside mother; a sweep where the design says populated-driven; a loop from making replies runs; a NULL cell write clobbering a cell a sub-run needed; a SQL form one SQLite version takes and another refuses; a claim from numbers that said otherwise.

**`hp-run/`.** What differed on hp after the sheet ran there: `brain.db` (the brain as it stood on hp), `mother.so` (built on hp), `look.sql` (an edited copy), `sources/wn.db` (built on hp's SQLite). Everything else in `hp:~/neuron-egg-test` was byte-identical to the folder here.
