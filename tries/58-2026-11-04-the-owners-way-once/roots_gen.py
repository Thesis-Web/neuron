# tries/58 roots_gen.py: the told block as lines, from the owner's roots table (ROOTS-GIVEN-AGAIN.md). Writes ROOTS-nk.txt.
# Shape of a root line: span 1 calls the inspection run `after` (the words after the root, read from the line onto this run's sheet:
# what = the first word after the use noun, and of/to/with/from/as = the word after each preposition); span 2 is the root's one physical
# act, written with those words bare (the kernel decodes a cell's name in a span to its value). A root's result lands on the line's sheet
# under the root's own gate. The use is the noun after the root (cell, word, value, point, run, dna, shard, link, key, line), the shard's trigger.
NOUNS = ['cell', 'word', 'value', 'point', 'run', 'dna', 'shard', 'link', 'key', 'line', 'node']
PREPS = ['of', 'to', 'at', 'by']   # none of them an SQL word: FROM, AS, WITH were merged into from, as, with by the cascade, and a cell's name decodes everywhere in a span
def word_after(X):   # the text of the word that follows the space at position X on the line (digits concatenate, a word is one symbol)
    return ("( SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = LINE AND s.pos > %s "
            "AND s.pos < coalesce ( ( SELECT min ( pos ) FROM seq WHERE run = LINE AND gate = 3 AND pos > %s ) , 999999999 ) ORDER BY s.pos ) )" % (X, X))
def resolved(W):     # the word it names the line's own cell 23, the result of the root before (the output of one root is the input of the next)
    return "CASE WHEN %s = 'it' THEN ( SELECT value FROM run_sheet WHERE run = LINE AND cell = 23 ) ELSE %s END" % (W, W)
LINE = "( SELECT from_run FROM run WHERE id = above )"
ORD = "( SELECT from_ord FROM run WHERE id = above )"
P = "( SELECT pos FROM run_receipt WHERE run = LINE ORDER BY id LIMIT 1 OFFSET ORD )"
SP1 = "( SELECT min ( pos ) FROM seq WHERE run = LINE AND gate = 3 AND pos > P )"
SP2 = "( SELECT min ( pos ) FROM seq WHERE run = LINE AND gate = 3 AND pos > SP1 )"
G1 = "( SELECT gate FROM seq WHERE run = LINE AND pos = SP1 + 1 )"
nouns_in = "( " + " , ".join("{gate:%s}" % n for n in NOUNS) + " )"
stmts = ["INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , CASE WHEN G1 IN NOUNS THEN %s ELSE %s END" % (resolved(word_after("SP2")), resolved(word_after("SP1")))]
for p in PREPS:
    SPp = "( SELECT min ( pos ) FROM seq WHERE run = LINE AND gate = 3 AND pos > ( SELECT min ( pos ) FROM seq WHERE run = LINE AND gate = {gate:%s} AND pos > P ) )" % p
    stmts.append("INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , {gate:%s} , 1 , %s WHERE %s IS NOT NULL" % (p, resolved(word_after(SPp)), SPp))
after = " ; ".join(stmts)
import re as _re
for k, v in [("NOUNS", nouns_in), ("G1", G1), ("SP2", SP2), ("SP1", SP1), ("P", P), ("ORD", ORD), ("LINE", LINE)]: after = _re.sub(r'\b' + k + r'\b', lambda m: v, after)
ROOTS = [  # (root, use noun, the owner's definition, the act, the example line)
 ("read", "cell", "Obtain the value of an addressed point or shard", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT value FROM run_sheet WHERE run = of AND cell = what ) )", "read cell 25 of {R}"),
 ("find", "word", "Locate an address satisfying a condition", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT gate FROM label WHERE symbol = 'what' ) )", "find word scan"),
 ("write", "value", "Change or create stored information", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( of , to , 1 , 'what' ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , 'what' )", "write value seven to 4921 of {R}"),
 ("move", "point", "Change a position or traverse to another point", "UPDATE xyz SET x = ( SELECT x FROM xyz WHERE gate = to ) , y = ( SELECT y FROM xyz WHERE gate = to ) , z = ( SELECT z FROM xyz WHERE gate = to ) WHERE gate = what ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT x || ' ' || y || ' ' || z FROM xyz WHERE gate = what ) )", "move point 2437 to 1330"),
 ("copy", "cell", "Reproduce specified information", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( to , what , 1 , ( SELECT value FROM run_sheet WHERE run = of AND cell = what ) ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT value FROM run_sheet WHERE run = to AND cell = what ) )", "copy cell 25 of {R} to {R2}"),
 ("link", "point", "Establish a relationship between points", "INSERT OR REPLACE INTO rel ( gate , kind , other , run ) VALUES ( what , by , to , above ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT count ( * ) FROM rel WHERE gate = what AND other = to ) )", "link point 2437 to 1330 by 12"),
 ("split", "run", "Separate a structure into components", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT group_concat ( gate , ' ' ) FROM seq WHERE run = what ) )", "split run {R}"),
 ("join", "run", "Combine structures according to a relationship", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol AS symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = what ORDER BY s.pos ) ) )", "join run {R}"),
 ("select", "dna", "Return rows satisfying a query", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT group_concat ( shard || ':' || before || ':' || trigger || ':' || coalesce ( call , 0 ) , ' ' ) FROM dna WHERE gate = what ) )", "select dna 2437"),
 ("insert", "shard", "Add a row to a table", "INSERT INTO dna ( gate , shard , before , trigger , call , spawn , times ) VALUES ( what , NULL , at , to , NULL , NULL , 0 ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT shard FROM dna WHERE gate = what AND before = at AND trigger = to ) )", "insert shard 2437 at 1 to 68"),
 ("update", "shard", "Modify an existing row", "UPDATE dna SET call = by WHERE gate = what AND before = at AND trigger = to ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT call FROM dna WHERE gate = what AND before = at AND trigger = to ) )", "update shard 2437 at 1 to 68 by {R}"),
 ("delete", "link", "Remove a row", "DELETE FROM rel WHERE gate = what AND other = to AND kind = by ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT count ( * ) FROM rel WHERE gate = what AND other = to ) )", "delete link 2437 to 1330 by 12"),
 ("store", "value", "Persist information for future use", "INSERT OR REPLACE INTO stored ( key , value , at_clock , run ) VALUES ( at , 'what' , ( SELECT n FROM clock ) , above ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT value FROM stored WHERE key = at ) )", "store value seven at 2437"),
 ("recall", "key", "Recover previously stored information", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT value FROM stored WHERE key = what ) )", "recall key 2437"),
 ("stamp", "cell", "Associate an occurrence with a time", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT n FROM clock ) || ' ' || of || ' ' || what )", "stamp cell 25 of {R}"),
 ("append", "cell", "Add an occurrence to chronological history", "INSERT INTO history ( at_clock , run , cell , value ) VALUES ( ( SELECT n FROM clock ) , of , what , ( SELECT value FROM run_sheet WHERE run = of AND cell = what ) ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT count ( * ) FROM history ) )", "append cell 25 of {R}"),
 ("compare", "value", "Determine equality, difference or ordering", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , CASE WHEN 'what' = 'to' THEN 0 WHEN 'what' < 'to' THEN -1 ELSE 1 END )", "compare value seven to nine"),
 ("set", "cell", "Establish a new state", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( of , what , to , ( SELECT value FROM run_sheet WHERE run = of AND cell = what ) ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT state FROM run_sheet WHERE run = of AND cell = what ) )", "set cell 4921 of {R} to 0"),
 ("measure", "run", "Obtain a quantity or difference", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT count ( * ) FROM run_receipt WHERE run = what ) )", "measure run {R}"),
 ("fetch", "word", "Acquire external information", "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , ( SELECT count ( * ) || ' rows: ' || substr ( group_concat ( text , ' | ' ) , 1 , 300 ) FROM at.corpus WHERE word = 'what' ) )", "fetch word scan at wn"),
 ("run", "line", "Perform a specified operation", "INSERT INTO replay ( parent , source , kind ) VALUES ( above , what , 1 )", "run line {R}"),
]
out = ["# ROOTS-nk.txt (tries/58, 2026-11-04): the told block, the owner's way. The owner's roots table and definitions (ROOTS-GIVEN-AGAIN.md); the",
       "# physics of the kernel gives a run me, above, from_run and from_ord; everything else here is read from the brain's own tables.",
       "# 1. two tables the memory and timeline roots write (stored, history), named so no root word stands in a span",
       "BUILD CREATE TABLE IF NOT EXISTS stored ( key INTEGER PRIMARY KEY , value TEXT , at_clock INTEGER , run INTEGER ) ; CREATE TABLE IF NOT EXISTS history ( id INTEGER PRIMARY KEY , at_clock INTEGER , run INTEGER , cell INTEGER , value TEXT ) ; BUILD",
       "# 2. after: the inspection of the line (the owner, 10-28: the inspection run reads the input row, the symbols after this gate): the words after",
       "#    the root onto the root run's sheet: cell 23 = the first word after the use noun; of, to, with, from, as = the word after each preposition.",
       "BUILD " + after + " ; BUILD"]
for i, (w, noun, d, act, ex) in enumerate(ROOTS):
    out.append("# %d. %s (%s): the owner: %s. Use: %s" % (i + 3, w, noun, d, ex))
    out.append("BUILD INSERT INTO replay ( parent , source , kind ) VALUES ( me , {run:2} , 1 ) ; BUILD BUILD " + act + " ; BUILD")
for i, (w, noun, d, act, ex) in enumerate(ROOTS):
    out.append("# bind %s at (heard, %s) and at (and, %s) to its run: two uses" % (w, noun, noun))
    for bf in ("1", "{gate:and}"):
        out.append("BUILD INSERT INTO dna ( gate , shard , before , trigger , call , spawn , times ) VALUES ( {gate:%s} , NULL , %s , {gate:%s} , {run:%d} , NULL , 0 ) ; UPDATE dna SET call = {run:%d} WHERE gate = {gate:%s} AND before = %s AND trigger = {gate:%s} ; BUILD" % (w, bf, noun, i + 3, i + 3, w, bf, noun))
open('ROOTS-nk.txt', 'w').write("\n".join(out) + "\n")
composed = [("find+select", "it", "find word scan and select dna it"), ("measure+compare", "it", "measure run {R} and compare value it to 4"), ("read+write", "it", "read cell 25 of {R} and write value it to 4921 of {R2}")]
import json; json.dump([(w, noun, ex) for w, noun, d, act, ex in ROOTS] + composed, open('roots_examples.json', 'w'))
print(len(out), 'lines;', sum(1 for l in out if l.startswith('BUILD')), 'BUILD lines;', sum(len(l) for l in out if l.startswith('BUILD')), 'bytes')
