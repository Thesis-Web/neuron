# The agreement test, 2026-10-30: the kernel against the v6 brain (tries/19), the same sixty lines

Run as: python3 -I test/agree.py <v6 brain.db> <kernel export brain.db> <v6 ledger> <kernel ledger> <LINES-v6.txt> <LINES-nk.txt> main|sixth
The kernel's export is what its 'export <dir>' request writes: every region as plain rows. Read the header of agree.py for what is compared and how the by-design differences are treated.

## main

```
main lines: 55; with the same text in both: 31; receipts identical on 30 of them; sheets identical on 28; subtrees identical on 45; out identical on 28 (of all main lines)

line 3 (changed text; v6 run 1, kernel run 1): BUILD CREATE TABLE "newgate" ( shard INTEGER PRIMARY KEY , before INTE
   - sheet: only v6 [('me', 1, '<heard: BUILD CREATE TABLE "newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger INTEGER , call I>')] only kernel [('me', 1, '<heard: BUILD INSERT INTO neuron ( gate ) VALUES ( newgate ) ; BUILD>')]
   - subtree: v6 1 runs, kernel 1; differing [((3, 'mother', 'reply', 'error: no such column: newgate'), 0, 1), ((3, 'mother', 'reply', 'ok'), 1, 0)]
   - out: v6 [('me', '<heard: BUILD CREATE TABLE "newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger INTEGER , call I>')] kernel [('me', '<heard: BUILD INSERT INTO neuron ( gate ) VALUES ( newgate ) ; BUILD>')]

line 4 (changed text; v6 run 3, kernel run 3): BUILD UPDATE "16" SET call = {run:3} WHERE before IS NULL AND trigger 
   - sheet: only v6 [('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>')] only kernel [('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')]

line 5 (same text; v6 run 7, kernel run 7): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - subtree: v6 81 runs, kernel 75; differing [((3, 'mother', 'reply', 'ok'), 39, 36), ('born run', 39, 36)]

line 6 (changed text; v6 run 89, kernel run 83): BUILD UPDATE "1" SET call = {run:5} WHERE before IS NULL AND trigger I
   - sheet: only v6 [('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>')] only kernel [('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')]

line 8 (same text; v6 run 98, kernel run 92): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - subtree: v6 15 runs, kernel 13; differing [('born run', 5, 4), ((3, 'mother', 'reply', 'ok'), 8, 7)]

line 12 (changed text; v6 run 187, kernel run 179): BUILD UPDATE "{gate:define}" SET call = {run:10} WHERE before = 1 AND 
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 13 (same text; v6 run 193, kernel run 185): define : who
   - subtree: v6 162 runs, kernel 160; differing [((3, 'mother', 'reply', 'error: neuron # already exists'), 0, 1), ('born run', 74, 73), ((3, 'mother', 'reply', 'error: table "#" already exists'), 1, 0), ((3, 'mother', 'reply', 'ok'), 80, 79)]

line 19 (changed text; v6 run 384, kernel run 374): BUILD UPDATE "{gate:why}" SET call = {run:17} WHERE before = 5 AND tri
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 25 (changed text; v6 run 439, kernel run 429): BUILD UPDATE "{gate:correct}" SET call = {run:21} WHERE before = 1 AND
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 26 (changed text; v6 run 445, kernel run 435): BUILD UPDATE "{gate:incorrect}" SET call = {run:22} WHERE before = 1 A
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 28 (changed text; v6 run 458, kernel run 448): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - sheet: only v6 [('know', 1, '0/261')] only kernel [('know', 1, '0/267')]
   - subtree: v6 7 runs, kernel 7; differing [((3, 'mother', 'reply', 'error: no such column: what'), 0, 1), ((3, 'mother', 'reply', 'error: no such table: what'), 1, 0)]
   - out: v6 [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/261'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/267'), ('remember', '0'), ('shape', '0')]

line 29 (same text; v6 run 466, kernel run 456): print dna : who
   - sheet: only v6 [('newgate', 1, 'dna')] only kernel [('newgate', 1, 'print')]
   - subtree: v6 8 runs, kernel 6; differing [((3, 'mother', 'reply', 'ok'), 5, 4), ('born run', 2, 1)]
   - out: v6 [('me', '<heard: print dna : who>'), ('newgate', 'dna'), ('know', '2/7'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: print dna : who>'), ('newgate', 'print'), ('know', '2/7'), ('remember', '0'), ('shape', '0')]

line 30 (changed text; v6 run 475, kernel run 463): BUILD UPDATE "{gate:print}" SET call = {run:28} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 33 (changed text; v6 run 498, kernel run 486): BUILD UPDATE "{gate:print}" SET call = {run:31} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/47'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/47'), ('remember', '0'), ('shape', '0')]

line 34 (changed text; v6 run 504, kernel run 492): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - sheet: only v6 [('know', 1, '0/362')] only kernel [('know', 1, '0/368')]
   - subtree: v6 9 runs, kernel 9; differing [((3, 'mother', 'reply', 'error: no such column: what'), 0, 1), ((3, 'mother', 'reply', 'error: no such table: what.node'), 1, 0)]
   - out: v6 [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('newgate', 'n'), ('reply', '<mother: error: no such column: above>'), ('know', '0/362'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('newgate', 'n'), ('reply', '<mother: error: no such column: above>'), ('know', '0/368'), ('remember', '0'), ('shape', '0')]

line 36 (changed text; v6 run 519, kernel run 507): BUILD UPDATE "{gate:print}" SET call = {run:34} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/40'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/46'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/40'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/46'), ('remember', '0'), ('shape', '0')]

line 39 (changed text; v6 run 540, kernel run 528): BUILD UPDATE "{gate:print}" SET call = {run:37} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/47'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/47'), ('remember', '0'), ('shape', '0')]

line 41 (same text; v6 run 554, kernel run 542): print table : rel
   - receipts differ at (3, (3, 'table'), (2, 'born'))
   - sheet: only v6 [] only kernel [('newgate', 1, 'table')]
   - subtree: v6 4 runs, kernel 6; differing [((3, 'mother', 'reply', 'ok'), 3, 4), ('born run', 0, 1)]
   - out: v6 [('me', '<heard: print table : rel>'), ('know', '1/7'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: print table : rel>'), ('newgate', 'table'), ('know', '1/7'), ('remember', '0'), ('shape', '0')]

line 42 (changed text; v6 run 559, kernel run 549): BUILD UPDATE "{gate:print}" SET call = {run:40} WHERE before = 1 AND t
   - sheet: only v6 [('know', 1, '0/41'), ('me', 1, '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('know', 1, '0/47'), ('me', 1, '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE "#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/41'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD UPDATE dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>'), ('know', '0/47'), ('remember', '0'), ('shape', '0')]

line 43 (changed text; v6 run 565, kernel run 555): BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) 
   - sheet: only v6 [('know', 1, '0/439'), ('newgate', 1, 'type')] only kernel [('know', 1, '0/423')]
   - subtree: v6 15 runs, kernel 7; differing [('born run', 4, 0), ((3, 'mother', 'reply', 'error: no such column: what'), 0, 1), ((3, 'mother', 'reply', 'ok'), 8, 3)]
   - out: v6 [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('newgate', 'type'), ('reply', '<mother: error: no such column: above>'), ('know', '0/439'), ('remember', '0'), ('shape', '0')] kernel [('me', '<heard: BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , # , # , ( SELE>'), ('reply', '<mother: error: no such column: above>'), ('know', '0/423'), ('remember', '0'), ('shape', '0')]

line 44 (same text; v6 run 581, kernel run 563): create neuron : who
   - sheet: only v6 [('newgate', 1, 'neuron')] only kernel [('newgate', 1, 'create')]
   - subtree: v6 8 runs, kernel 6; differing [((3, 'mother', 'reply', 'ok'), 5, 4), ('born run', 2, 1)]
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

shards (born-line words, the space and the digits left out; call and spawn as the text of the run they point at, run numbers masked): v6 675, kernel 656; same 614; only v6 61; only kernel 42
   only v6     ("'", '(', 'what', None, None, 1)
   only v6     ("'", ',', 'what', None, None, 1)
   only v6     ("'", 'node', ')', None, None, 1)
   only v6     ("'", 'what', ',', None, None, 1)
   only v6     (':', 'column', 'what', None, None, 4)
   only v6     (':', 'error', 'no', None, None, 38)
   only v6     (':', 'error', 'table', None, None, 1)
   only v6     (':', 'table', 'what', None, None, 2)
   only v6     ('=', 'gate', 'what', None, None, 34)
   only v6     ('=', 'name', 'CAST', None, None, 1)
   only v6     ('AS', 'what', 'TEXT', None, None, 1)
   only v6     ('BUILD', ';', None, None, None, 281)
   only kernel (':', 'column', 'what', None, None, 7)
   only kernel (':', 'error', 'neuron', None, None, 1)
   only kernel (':', 'error', 'no', None, None, 39)
   only kernel ('=', 'gate', 'what', None, None, 41)
   only kernel ('AND', 'what', 'born', None, None, 1)
   only kernel ('AND', 'what', 'call', None, None, 1)
   only kernel ('AND', 'what', 'spawn', None, None, 1)
   only kernel ('AND', 'what', 'trigger', None, None, 1)
   only kernel ('BUILD', ';', None, None, None, 271)
   only kernel ('BUILD', 'heard', 'CREATE', None, None, 1)
   only kernel ('BUILD', 'heard', 'INSERT', None, None, 16)
   only kernel ('BUILD', 'said', 'INSERT', None, None, 234)
memories (born runs left out): v6 59 distinct, kernel 57; only v6 16, only kernel 14
   only v6     ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only v6     ('BUILD   CREATE   TABLE   " newgate "   (   shard   INTEGER   PRIMARY  ', '1', 'BUILD')
   only v6     ('BUILD   CREATE   TABLE   " newgate "   (   shard   INTEGER   PRIMARY  ', '2', 'BUILD')
   only v6     ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only v6     ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only v6     ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   OR   REPLACE   INTO   run_sheet   (   run   ,   cell ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   INTO   neuron   (   gate   )   VALUES   (   newgate  ', '1', 'BUILD')
   only kernel ('BUILD   INSERT   INTO   neuron   (   gate   )   VALUES   (   newgate  ', '2', 'BUILD')
rel: v6 0, kernel 0; identical: True; only v6 [] only kernel []
definition nodes: v6 2 neurons with rows (5 rows), kernel 2 (5 rows); identical: True

runs in all: v6 722, kernel 702; symbols: v6 265, kernel 261; only v6 ['TEXT', 'name', 'sqlite_master', 'type']; only kernel []
```

## sixth

```
sixth lines: 5; with the same text in both: 2; receipts identical on 2 of them; sheets identical on 2; subtrees identical on 1; out identical on 2 (of all main lines)

line 1 (changed text; v6 run 1, kernel run 1): 6> BUILD CREATE TABLE sixth."newgate" ( shard INTEGER PRIMARY KEY , be
   - sheet: only v6 [('me', 1, '<heard: BUILD CREATE TABLE sixth."newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger INTEGER , >')] only kernel [('me', 1, '<heard: BUILD INSERT INTO sixth.neuron ( gate ) VALUES ( newgate ) ; BUILD>')]
   - subtree: v6 1 runs, kernel 1; differing [((3, 'mother', 'reply', 'error: no such column: newgate'), 0, 1), ((3, 'mother', 'reply', 'ok'), 1, 0)]
   - out: v6 [('me', '<heard: BUILD CREATE TABLE sixth."newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger INTEGER , >')] kernel [('me', '<heard: BUILD INSERT INTO sixth.neuron ( gate ) VALUES ( newgate ) ; BUILD>')]

line 2 (changed text; v6 run 3, kernel run 3): 6> BUILD UPDATE sixth."16" SET call = {run:1} WHERE before IS NULL AND
   - sheet: only v6 [('me', 1, '<heard: BUILD UPDATE sixth."#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>')] only kernel [('me', 1, '<heard: BUILD UPDATE sixth.dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>')]
   - subtree: v6 3 runs, kernel 3; differing [((1, 'said', None, 'BUILD CREATE TABLE sixth."newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger '), 1, 0), ('born run', 0, 1)]
   - out: v6 [('me', '<heard: BUILD UPDATE sixth."#" SET call = # WHERE before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')] kernel [('me', '<heard: BUILD UPDATE sixth.dna SET call = # WHERE gate = # AND before IS NULL AND trigger IS NULL ; BUILD>'), ('reply', '<mother: ok>')]

line 14 (same text; v6 run 20, kernel run 20): 6> BUILD CREATE TABLE sixth.asked ( id INTEGER PRIMARY KEY , run INTEG
   - subtree: v6 11 runs, kernel 11; differing [((1, 'said', None, 'BUILD CREATE TABLE sixth."newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger '), 5, 0), ('born run', 0, 5)]

line 15 (same text; v6 run 32, kernel run 32): 6> BUILD INSERT INTO sixth.asked ( run , cell , returns ) SELECT s.run
   - subtree: v6 45 runs, kernel 41; differing [((1, 'said', None, 'BUILD CREATE TABLE sixth."newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger '), 22, 0), ('born run', 0, 20), ((3, 'mother', 'reply', 'ok'), 23, 21)]

line 16 (changed text; v6 run 78, kernel run 74): 6> BUILD UPDATE sixth."{gate6:seen}" SET call = {run:15} WHERE before 
   - sheet: only v6 [('me', 1, '<heard: BUILD UPDATE sixth."#" SET call = # WHERE before = # AND trigger = # ; BUILD>')] only kernel [('me', 1, '<heard: BUILD UPDATE sixth.dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>')]
   - out: v6 [('me', '<heard: BUILD UPDATE sixth."#" SET call = # WHERE before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>')] kernel [('me', '<heard: BUILD UPDATE sixth.dna SET call = # WHERE gate = # AND before = # AND trigger = # ; BUILD>'), ('reply', '<mother: ok>')]

shards (born-line words, the space and the digits left out; call and spawn as the text of the run they point at, run numbers masked): v6 107, kernel 106; same 97; only v6 10; only kernel 9
   only v6     ('BUILD', ';', None, None, None, 80)
   only v6     ('BUILD', 'heard', 'CREATE', None, None, 2)
   only v6     ('BUILD', 'heard', 'INSERT', None, None, 1)
   only v6     ('BUILD', 'said', 'CREATE', None, None, 29)
   only v6     ('BUILD', 'said', 'INSERT', None, None, 46)
   only v6     ('SET', '"', 'call', None, None, 2)
   only v6     ('born', None, None, 'BUILD CREATE TABLE sixth."newgate" ( shard INTEGER PRIMARY K', None, 30)
   only v6     ('mother', None, None, None, None, 80)
   only v6     ('ok', 'mother', None, None, None, 79)
   only v6     ('said', None, None, None, None, 75)
   only kernel ('BUILD', ';', None, None, None, 78)
   only kernel ('BUILD', 'heard', 'CREATE', None, None, 1)
   only kernel ('BUILD', 'heard', 'INSERT', None, None, 2)
   only kernel ('BUILD', 'said', 'INSERT', None, None, 73)
   only kernel ('SET', 'dna', 'call', None, None, 2)
   only kernel ('born', None, None, 'BUILD INSERT INTO sixth.neuron ( gate ) VALUES ( newgate ) ;', None, 28)
   only kernel ('mother', None, None, None, None, 78)
   only kernel ('ok', 'mother', None, None, None, 77)
   only kernel ('said', None, None, None, None, 73)
memories (born runs left out): v6 24 distinct, kernel 24; only v6 7, only kernel 7
   only v6     ('BUILD   CREATE   TABLE   sixth . " newgate "   (   shard   INTEGER   P', '1', 'BUILD')
   only v6     ('BUILD   CREATE   TABLE   sixth . " newgate "   (   shard   INTEGER   P', '2', 'BUILD')
   only v6     ('BUILD   UPDATE   sixth . " # # "   SET   call   =   #   WHERE   before', '1', 'BUILD')
   only v6     ('BUILD   UPDATE   sixth . " # # "   SET   call   =   # #   WHERE   befo', '1', 'BUILD')
   only v6     ('seen   :   # #', '6', '1')
   only v6     ('seen   :   # #', '6', '8')
   only kernel ('BUILD   INSERT   INTO   sixth . neuron   (   gate   )   VALUES   (   n', '1', 'BUILD')
   only kernel ('BUILD   INSERT   INTO   sixth . neuron   (   gate   )   VALUES   (   n', '2', 'BUILD')
   only kernel ('BUILD   UPDATE   sixth . dna   SET   call   =   #   WHERE   gate   =  ', '1', 'BUILD')
   only kernel ('BUILD   UPDATE   sixth . dna   SET   call   =   # #   WHERE   gate   =', '1', 'BUILD')
   only kernel ('seen   :   # #', '6', '2')
   only kernel ('seen   :   # #', '6', '3')
rel: v6 0, kernel 0; identical: True; only v6 [] only kernel []
definition nodes: v6 0 neurons with rows (0 rows), kernel 0 (0 rows); identical: True

runs in all: v6 217, kernel 213; symbols: v6 109, kernel 117; only v6 []; only kernel ['VALUES', 'column', 'dna', 'error', 'gate', 'neuron', 'no', 'such']
```
