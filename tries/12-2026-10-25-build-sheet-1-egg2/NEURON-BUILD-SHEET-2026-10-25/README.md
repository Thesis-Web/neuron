# NEURON build folder, 2026-10-25

The hand-laid part of the brain and the prompt. The instructions are in `NEURON-BUILD-SHEET-2026-10-25.md` (one folder up).

| File | What it is |
|---|---|
| mother.c | mother: runs the text she is handed at the SQL prompt, answers ok / rows / error; carries source outboxes into secondary input; writes a refusal into the run's output; queues a DROP SQLite refuses mid-run into `later`. ~60 lines of C. Build: `gcc -shared -fPIC -O2 -o mother.so mother.c -I.` |
| sqlite3ext.h, sqlite3.h | SQLite's own headers, so mother.c compiles anywhere (from the 3.46.1 amalgamation). |
| mother-hub-x86_64.so | mother already built on the hub (WSL, x86_64). On the hp build your own. |
| egg.sql | the egg: laid once into an empty brain.db. 264 gates, 7 physics neurons, 81 word neurons (every token of the born run), the ear, the encoder, the shard counter, receipt, sheet, secondary, output, later. |
| BORN-RUN.txt | the born run, the first line you type after a new word fails. One line, 541 tokens. |
| bottom.py | the prompt: writes your line into `input`, prints what the brain said (and what its sub-runs said), runs `later`. Nothing else. |
| look.sql | your eyes: `.read look.sql` at the sqlite3 prompt shows the last run's receipt, cells, new words, new tables, secondary input, counts. |
| sources/ | seven source brains as SQLite files (wn, gcide, mw, mwt, moby, map, sqldoc), each: corpus(word, hw, text), inbox, outbox, and its own `work` trigger. The corpora are the 470-word slices captured for 17.x; the full WordNet and GCIDE live on the hp (see the sheet). |
| gen_egg2.py | the script that wrote egg.sql, so you can see every rule it holds. You do not need to run it. |
