| # | prompt | line | run | runs | hits | born | refused | s | what the brain put in its out mailbox |
|---|---|---|---|---|---|---|---|---|---|
| | | *WIKT-LINES-2026-10-29.txt: the ten lines that wire Wiktionary (wikt.db, the lean file laid by build_wikt.py --lean, beside the live brain's* | | | | | | | |
| | | *other sources at w/19/sources; the full file is D:\Neuron-sources\built\wikt-full.db) into the live v6 brain as a ninth source, in this order,* | | | | | | | |
| | | *at the page's prompt (a line that begins with "6> " goes to the sixth's prompt). Each is the v6 line it comes from (LINES-v6.txt 8, 10, 15, 17* | | | | | | | |
| | | *and their binds) with the one change the ninth source needs: its inbox in the ask, and its gate counted wherever the brain counts source* | | | | | | | |
| | | *returns ("arrival BETWEEN 7 AND 14", the eight hand-laid source gates; the ninth is born by line 1, so its gate is read from the label table).* | | | | | | | |
| | | *Two things the first trial on a copy found (2026-10-29 20:35): this SQLite attaches at most ten databases and the brain already has ten (the* | | | | | | | |
| | | *sixth, the eight sources, the guesser), so the Merriam-Webster dictionary slice mw (304 lines for 150 words, all of which Wiktionary holds)* | | | | | | | |
| | | *is detached in line 2 to make room and left out of the ask; its file stays, one ATTACH line brings it back. And "me" is a hole word the brain* | | | | | | | |
| | | *fills with the run number, so the source brain's table is written ME in line 3 (SQLite reads names without case; the encoder does not).* | | | | | | | |
| | | *{run:k} is the run number that line k of THIS file started: read it under What came out as the line's "me" cell (main run N · me: N) and* | | | | | | | |
| | | *type the number in its place. The gate numbers written here were read from the live brain on 2026-10-29 evening: define 153, why 231 (main),* | | | | | | | |
| | | *seen 82 (sixth); ":" is 68, heard 1, the sixth 5, main 6.* | | | | | | | |
| | | *After a restart of the door the attachment of line 2 is gone (an ATTACH lives on the connection): type line 2 again, or change SOURCES in* | | | | | | | |
| | | *brain/bottom6.py (mw out, wikt in), a change to a file that is yours to make by name.* | | | | | | | |
| | | *To undo the wiring: change call : define from {run:5} to 124 (the v6 define run), and the same shape for why (from {run:9} to its old call),* | | | | | | | |
| | | *and at 6> a BUILD UPDATE of sixth."82" back to its old call; DETACH wikt ; ATTACH the mw file AS mw.* | | | | | | | |
| | | *1. wikt is born: its two tables, through the create neuron tool.* | | | | | | | |
| 1 | main | `create neuron : wikt` | 10126 | 11 | 1068 | 1 | 0 | 1.42 | main run 10126 · me: 10126<br>main run 10126 · newgate: 3241<br>main run 10126 · what: 3241<br>main run 10126 · say: run 10133 from mother: ok<br>main run 10126 · know: 2/7<br>main run 10126 · remember: 0<br>main run 10126 · shape: 0<br>sixth run 986 · me: 986 |
| | | *2. mw gives up its slot; the source file is attached to the brain's connection as wikt (ATTACH through mother was tested 10-29 morning).* | | | | | | | |
| 2 | main | `BUILD DETACH mw ; ATTACH '/tmp/claude-1000/-home-exnulla-neu` | 10137 | 29 | 1735 | 12 | 0 | 2.78 |  |
| | | *3. The source brain learns its own gate from the encoder (every source brain carries its gate in its me table; its carry trigger writes it on every return).* | | | | | | | |
| 3 | main | `BUILD UPDATE wikt.ME SET gate = ( SELECT gate FROM label WHE` | 10166 | 6 | 551 | 0 | 0 | 1.85 | main run 10166 · me: 10166<br>main run 10166 · reply: run 10171 from mother: ok<br>main run 10166 · know: 4/39<br>main run 10166 · remember: 0<br>main run 10166 · shape: 0<br>sixth run 989 · me: 989 |
| | | *4. The ask, laid again without mw and with a ninth inbox (LINES-v6 line 8). Typed at the top it answers an error about above: the long way. Its run number is {run:4}.* | | | | | | | |
| 4 | main | `BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state ` | 10172 | 6 | 1032 | 0 | 0 | 1.48 | main run 10172 · me: 10172<br>main run 10172 · reply: run 10177 from mother: error: no such column: above<br>main run 10172 · know: 59/510<br>main run 10172 · remember: 0<br>main run 10172 · shape: 0<br>sixth run 992 · me: 992 |
| | | *5. The define run, laid again (LINES-v6 line 10): span 1 calls the new ask ({run:4}); span 3 counts wikt's returns with the eight sources'. Its run number is {run:5}.* | | | | | | | |
| 5 | main | `BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state ` | 10178 | 8 | 1757 | 0 | 0 | 1.77 | main run 10178 · me: 10178<br>main run 10178 · reply: run 10185 from mother: error: no such column: above<br>main run 10178 · know: 70/1211<br>main run 10178 · remember: 0<br>main run 10178 · shape: 0<br>sixth run 995 · me: 995 |
| | | *6. Bind define's shard (arrived from heard, next ":") to the new define run.* | | | | | | | |
| 6 | main | `BUILD UPDATE "153" SET call = 10178 WHERE before = 1 AND tri` | 10186 | 6 | 554 | 0 | 0 | 1.10 | main run 10186 · me: 10186<br>main run 10186 · reply: run 10191 from mother: ok<br>main run 10186 · know: 5/42<br>main run 10186 · remember: 0<br>main run 10186 · shape: 0<br>sixth run 998 · me: 998 |
| | | *7. The sixth's observing line, laid again (LINES-v6 line 15): its count of source returns includes wikt's. Its run number is {run:7} (in the sixth).* | | | | | | | |
| 7 | sixth | `6> BUILD INSERT INTO sixth.asked ( run , cell , returns ) SE` | 1001 | 12 | 904 | 0 | 0 | 1.17 | sixth run 1001 · me: 1001<br>sixth run 1001 · newgate: 114<br>sixth run 1001 · reply: run 1012 from mother: ok |
| | | *8. Bind the sixth's seen shard (arrived from main, next ":") to it.* | | | | | | | |
| 8 | sixth | `6> BUILD UPDATE sixth."82" SET call = 1001 WHERE before = 6 ` | 1013 | 2 | 45 | 0 | 0 | 0.07 | sixth run 1013 · me: 1013<br>sixth run 1013 · reply: run 1014 from mother: ok |
| | | *9. The why line, laid again (LINES-v6 line 17): the guessing brain's corpus and the returns count include wikt's. Its run number is {run:9}.* | | | | | | | |
| 9 | main | `BUILD INSERT OR IGNORE INTO guess.corpus ( line , word ) SEL` | 10192 | 6 | 1375 | 0 | 0 | 2.23 | main run 10192 · me: 10192<br>main run 10192 · reply: run 10197 from mother: error: no such column: above<br>main run 10192 · know: 51/853<br>main run 10192 · remember: 0<br>main run 10192 · shape: 0<br>sixth run 1015 · me: 1015 |
| | | *10. Bind why's shard (arrived from the sixth, next ":") to it.* | | | | | | | |
| 10 | main | `BUILD UPDATE "231" SET call = 10192 WHERE before = 5 AND tri` | 10198 | 6 | 554 | 0 | 0 | 1.13 | main run 10198 · me: 10198<br>main run 10198 · reply: run 10203 from mother: ok<br>main run 10198 · know: 5/42<br>main run 10198 · remember: 0<br>main run 10198 · shape: 0<br>sixth run 1018 · me: 1018 |
| | | *Then: define : who. Under Run, wikt's returns come as rows of its own ([word: who] [part of speech: pron] ...; pron 1: ...).* | | | | | | | |
| | | *--- after the wiring, on the copy only: two defines to see wikt's returns arrive and be counted* | | | | | | | |
| 11 | main | `define : who` | 10204 | 1076 | 62410 | 511 | 0 | 53.03 | main run 10204 · me: 10204<br>main run 10204 · what: 121<br>main run 10204 · def: run 10212 from wn: noun 1: a United Nations agency to coordinate international health acti<br>main run 10204 · know: 2/5<br>main run 10204 · remember: run 723 from heard: define : who<br>main run 10204 · shape: 124<br>main run 10204 · known: me what know source count about no who other like of a to and an as or the which by on all<br>main run 10204 · unknown: said mother say state s m h hit word k l A known AS United Nations agency coordinate inter |
| 12 | main | `define : ask` | 11280 | 1292 | 73666 | 558 | 0 | 77.82 | main run 11280 · me: 11280<br>main run 11280 · what: 199<br>main run 11280 · def: run 11288 from wn: verb 1: make a request or demand for something to somebody; "She asked <br>main run 11280 · know: 2/5<br>main run 11280 · remember: run 4539 from heard: define : ask<br>main run 11280 · shape: 10178<br>main run 11280 · known: me what know before call source count about no who like of a to and an as or the ask which<br>main run 11280 · unknown: said times id ok state s m pos h such inbox word k A y g AS help syn Health later also use |
