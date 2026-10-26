# NEURON build folder 2, 2026-10-25 evening

The hand-laid part of the brain, the prompt, and the logs of every line typed today. The instructions are in `NEURON-BUILD-SHEET-2-2026-10-25.md` (one folder up), which also pastes every file here in full.

| File | What it is |
|---|---|
| mother.c | mother: runs the text she is handed at the SQL prompt, answers ok / rows / error; when a source's outbox is written she carries it into the brain's input as runs. 70 lines of C. Build: `gcc -shared -fPIC -O2 -o mother.so mother.c -I.` |
| sqlite3ext.h, sqlite3.h | SQLite's own headers (3.46.1 amalgamation), so mother.c compiles anywhere. |
| mother-hub-x86_64.so | mother already built on the hub (WSL, x86_64). On the hp build your own. |
| gen_egg3.py | writes egg.sql and BORN-RUN.txt. `python3 gen_egg3.py` |
| egg.sql | the egg, laid once into an empty brain.db: the ear, the encoder, the shard counter, the receipt, the sheet, 7 physics neurons, BUILD, var, 0-9, the other 53 distinct tokens of the born run. 221 tables, 76 views, 77 triggers. |
| BORN-RUN.txt | the born run, one line, 559 tokens. |
| bottom.py | the prompt: writes your line into `input`, prints every run it started, read back through the encoder. |
| look.sql | your eyes: `.read look.sql` at the sqlite3 prompt. |
| sources/ | seven source brains (wn, gcide, mw, mwt, moby, map, sqldoc), each corpus / inbox / outbox / `work` trigger; 470-word slices. |
| run_chain.sh | lays a fresh egg and types every line of the sheet in order, logging line and answer. |
| timing.sh | the 592 / 1200 / 2400-token lines. |
| CHAIN-LOG.txt, CHAIN-LOG-hp.txt | the chain as it ran on the hub (SQLite 3.37.2) and the hp (3.46.1); identical rows. |
| TIMING-LOG.txt | the timing run on the hub. |
