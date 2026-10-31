main lines: 55; with the same text in both: 30; receipts identical on 26 of them; sheets identical on 28; subtrees identical on 44; out identical on 28 (of all main lines)

line 3 (changed text; v6 run 1, kernel run 1): BUILD CREATE TABLE "newgate" ( shard INTEGER PRIMARY KEY , before INTE
   - sheet: only v6 [('me', 1, '<heard: BUILD CREATE TABLE "newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger INTEGER , call I>')] only kernel [('me', 1, '<heard: BUILD INSERT INTO neuron ( gate ) VALUES ( newgate ) ; BUILD>')]
   - subtree: v6 1 runs, kernel 1; differing [((3, 'mother', 'reply', 'ok'), 1, 0), ((3, 'mother', 'reply', 'error: no such column: newgate'), 0, 1)]
   - out: v6 [('me', '<heard: BUILD CREATE TABLE "newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger INTEGER , call I>')] kernel [('me', '<heard: BUILD INSERT INTO neuron ( gate ) VALUES ( newgate ) ; BUILD>')]

line 4 (changed text; v6 run 3, kernel run 3): BUILD UPDATE "16" SET call = {run:3} WHERE before IS NULL AND trigger 
   - sheet: only v6 [('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>')] only kernel [('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')]

line 5 (changed text; v6 run 7, kernel run 7): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - subtree: v6 81 runs, kernel 67; differing [('born run', 39, 32), ((3, 'mother', 'reply', 'ok'), 39, 32)]

line 6 (changed text; v6 run 89, kernel run 75): BUILD UPDATE "1" SET call = {run:5} WHERE before IS NULL AND trigger I
   - sheet: only v6 [('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>')] only kernel [('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')]

line 8 (same text; v6 run 98, kernel run 84): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - receipts differ at (73, (72, 'about'), (71, 'born'))

line 9 (same text; v6 run 114, kernel run 100): BUILD CREATE TABLE rel ( gate INTEGER , kind INTEGER , other INTEGER ,
   - receipts differ at (18, (17, 'kind'), (16, 'born'))
   - subtree: v6 9 runs, kernel 11; differing [('born run', 2, 3), ((3, 'mother', 'reply', 'ok'), 6, 7)]

line 10 (same text; v6 run 124, kernel run 112): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - receipts differ at (190, (186, 'r'), (185, 'born'))
   - subtree: v6 55 runs, kernel 61; differing [((3, 'mother', 'reply', 'ok'), 27, 30), ('born run', 24, 27)]

line 12 (changed text; v6 run 187, kernel run 181): BUILD UPDATE "{gate:define}" SET call = {run:10} WHERE before = 1 AND 
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 13 (same text; v6 run 193, kernel run 187): define : who
   - subtree: v6 162 runs, kernel 160; differing [((3, 'mother', 'reply', 'ok'), 80, 79), ((3, 'mother', 'reply', 'error: table "#" already exists'), 1, 0), ('born run', 74, 73), ((3, 'mother', 'reply', 'error: neuron # already exists'), 0, 1)]

line 19 (changed text; v6 run 384, kernel run 376): BUILD UPDATE "{gate:why}" SET call = {run:17} WHERE before = 5 AND tri
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 25 (changed text; v6 run 439, kernel run 431): BUILD UPDATE "{gate:correct}" SET call = {run:21} WHERE before = 1 AND
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 26 (changed text; v6 run 445, kernel run 437): BUILD UPDATE "{gate:incorrect}" SET call = {run:22} WHERE before = 1 A
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 28 (changed text; v6 run 458, kernel run 450): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - sheet: only v6 [('know', 1, '0/261')] only kernel [('know', 1, '0/267')]
   - subtree: v6 7 runs, kernel 7; differing [((3, 'mother', 'reply', 'error: no such table: what'), 1, 0), ((3, 'mother', 'reply', 'error: no such column: what'), 0, 1)]
   - out: v6 [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/261'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/267'), ('remember', '0'), ('shape', '0')]

line 29 (same text; v6 run 466, kernel run 458): print dna : who
   - sheet: only v6 [('newgate', 1, 'dna')] only kernel [('newgate', 1, 'print')]
   - subtree: v6 8 runs, kernel 6; differing [('born run', 2, 1), ((3, 'mother', 'reply', 'ok'), 5, 4)]
   - out: v6 [('me', '<heard: print dna : who>'), ('newgate', 'dna'), ('know', '2/7'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: print dna : who>'), ('newgate', 'print'), ('know', '2/7'), ('remember', '0'), ('shape', '0')]

line 30 (changed text; v6 run 475, kernel run 465): BUILD UPDATE "{gate:print}" SET call = {run:28} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 33 (changed text; v6 run 498, kernel run 488): BUILD UPDATE "{gate:print}" SET call = {run:31} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/47'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/47'), ('remember', '0'), ('shape', '0')]

line 34 (changed text; v6 run 504, kernel run 494): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - sheet: only v6 [('know', 1, '0/362'), ('newgate', 1, 'n')] only kernel [('know', 1, '0/368')]
   - subtree: v6 9 runs, kernel 7; differing [((3, 'mother', 'reply', 'ok'), 4, 3), ('born run', 1, 0), ((3, 'mother', 'reply', 'error: no such column: what'), 0, 1), ((3, 'mother', 'reply', 'error: no such table: what.node'), 1, 0)]
   - out: v6 [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('newgate', 'n'), ('reply', '<mother: error: no such column: above>'), ('know', '0/362'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/368'), ('remember', '0'), ('shape', '0')]

line 36 (changed text; v6 run 519, kernel run 507): BUILD UPDATE "{gate:print}" SET call = {run:34} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 39 (changed text; v6 run 540, kernel run 528): BUILD UPDATE "{gate:print}" SET call = {run:37} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/47'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/47'), ('remember', '0'), ('shape', '0')]

line 41 (same text; v6 run 554, kernel run 542): print table : rel
   - receipts differ at (3, (3, 'table'), (2, 'born'))
   - sheet: only v6 [] only kernel [('newgate', 1, 'table')]
   - subtree: v6 4 runs, kernel 6; differing [('born run', 0, 1), ((3, 'mother', 'reply', 'ok'), 3, 4)]
   - out: v6 [('me', '<heard: print table : rel>'), ('know', '1/7'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: print table : rel>'), ('newgate', 'table'), ('know', '1/7'), ('remember', '0'), ('shape', '0')]

line 42 (changed text; v6 run 559, kernel run 549): BUILD UPDATE "{gate:print}" SET call = {run:40} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/47'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/47'), ('remember', '0'), ('shape', '0')]

line 43 (changed text; v6 run 565, kernel run 555): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - sheet: only v6 [('know', 1, '0/439'), ('newgate', 1, 'type')] only kernel [('know', 1, '0/423')]
   - subtree: v6 15 runs, kernel 7; differing [((3, 'mother', 'reply', 'ok'), 8, 3), ('born run', 4, 0), ((3, 'mother', 'reply', 'error: no such column: what'), 0, 1)]
   - out: v6 [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('newgate', 'type'), ('reply', '<mother: error: no such column: above>'), ('know', '0/439'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/423'), ('remember', '0'), ('shape', '0')]

line 44 (same text; v6 run 581, kernel run 563): create neuron : who
   - sheet: only v6 [('newgate', 1, 'neuron')] only kernel [('newgate', 1, 'create')]
   - subtree: v6 8 runs, kernel 6; differing [('born run', 2, 1), ((3, 'mother', 'reply', 'ok'), 5, 4)]
   - out: v6 [('me', '<heard: create neuron : who>'), ('newgate', 'neuron'), ('know', '2/7'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: create neuron : who>'), ('newgate', 'create'), ('know', '2/7'), ('remember', '0'), ('shape', '0')]

line 45 (changed text; v6 run 590, kernel run 570): BUILD UPDATE "{gate:create}" SET call = {run:43} WHERE before = 1 AND 
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 46 (changed text; v6 run 596, kernel run 576): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - sheet: only v6 [('know', 1, '0/1010')] only kernel [('know', 1, '0/1016')]
   - out: v6 [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('newgate', 'changes'), ('reply', '<mother: error: no such column: above>'), ('know', '0/1010'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('newgate', 'changes'), ('reply', '<mother: error: no such column: above>'), ('know', '0/1016'), ('remember', '0'), ('shape', '0')]

line 48 (changed text; v6 run 631, kernel run 611): BUILD UPDATE "{gate:change}" SET call = {run:46} WHERE before = 1 AND 
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 49 (changed text; v6 run 637, kernel run 617): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - sheet: only v6 [('know', 1, '0/1010')] only kernel [('know', 1, '0/1016')]
   - out: v6 [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/1010'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/1016'), ('remember', '0'), ('shape', '0')]

line 51 (changed text; v6 run 650, kernel run 630): BUILD UPDATE "{gate:change}" SET call = {run:49} WHERE before = 1 AND 
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 52 (changed text; v6 run 656, kernel run 636): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - sheet: only v6 [('know', 1, '0/1010')] only kernel [('know', 1, '0/1016')]
   - out: v6 [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/1010'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/1016'), ('remember', '0'), ('shape', '0')]

line 54 (changed text; v6 run 669, kernel run 649): BUILD UPDATE "{gate:change}" SET call = {run:52} WHERE before = 1 AND 
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 57 (changed text; v6 run 696, kernel run 676): BUILD UPDATE "{gate:change}" SET call = {run:55} WHERE before = 1 AND 
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/47'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/47'), ('remember', '0'), ('shape', '0')]

line 60 (changed text; v6 run 717, kernel run 697): BUILD UPDATE "{gate:change}" SET call = {run:58} WHERE before = 1 AND 
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/47'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/47'), ('remember', '0'), ('shape', '0')]

shards (born-line words, the space and the digits left out; call and spawn as the text of the run they point at, run numbers masked): v6 675, kernel 650; same 599; only v6 76; only kernel 51
   only v6     ("'", '(', 'what', None, None, 1)
   only v6     ("'", ',', 'what', None, None, 1)
   only v6     ("'", 'node', ')', None, None, 1)
   only v6     ("'", 'what', ',', None, None, 1)
   only v6     (':', 'column', 'what', None, None, 4)
   only v6     (':', 'error', 'no', None, None, 38)
   only v6     (':', 'error', 'table', None, None, 1)
   only v6     (':', 'table', 'what', None, None, 2)
   only v6     ('=', 'about', 's', None, None, 60)
   only v6     ('=', 'gate', 's', None, None, 36)
   only v6     ('=', 'gate', 'what', None, None, 34)
   only v6     ('=', 'name', 'CAST', None, None, 1)
   only kernel (':', 'column', 'what', None, None, 7)
   only kernel (':', 'error', 'neuron', None, None, 1)
   only kernel (':', 'error', 'no', None, None, 39)
   only kernel ('=', 'about', 's', None, None, 8)
   only kernel ('=', 'gate', 's', None, None, 88)
   only kernel ('=', 'gate', 'what', None, None, 41)
   only kernel ('=', 'run', 'r', None, None, 20)
   only kernel ('AND', 'what', 'born', None, None, 1)
   only kernel ('AND', 'what', 'call', None, None, 1)
   only kernel ('AND', 'what', 'spawn', None, None, 1)
   only kernel ('AND', 'what', 'trigger', None, None, 1)
   only kernel ('BUILD', ';', None, None, None, 271)
memories (born runs left out): v6 59 distinct, kernel 44; only v6 30, only kernel 15
   only v6     ('BUILD   INSERT   OR   IGNORE   INTO   guess . corpus   (   line   ,   ', '2', 'BUILD')
   only v6     ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only v6     ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '2', 'BUILD')
   only v6     ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '2', 'BUILD')
   only v6     ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only v6     ('BUILD   UPDATE   guess . guesses   SET   incorrect   =   incorrect   +', '2', 'BUILD')
   only kernel ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   INTO   neuron   (   gate   )   VALUES   (   newgate  ', '1', 'BUILD')
rel: v6 0, kernel 0; identical: True; only v6 [] only kernel []
definition nodes: v6 2 neurons with rows (5 rows), kernel 2 (5 rows); identical: True

runs in all: v6 722, kernel 702; symbols: v6 265, kernel 261; only v6 ['TEXT', 'name', 'sqlite_master', 'type']; only kernel []
