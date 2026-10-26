# Undo test: which pairs undo each other in the silicon. Predictions frozen before the run (builder's, not the owner's)
2026-10-24. Rule under test: two operations belong on opposite ends of ONE line only if doing A then B puts the database
(or the value) back exactly where it started. Pairs that cannot undo each other get separate lines.
Start: t (a INTEGER, b TEXT) rows (1,'x'),(2,'y'),(3,'z'). "Exact" = same schema, same rows, same rowids. "Content" = same rows ignoring rowids.

Predictions:
- INSERT then DELETE that row: exact. DELETE then INSERT it back: content only (the row comes back with a new rowid).
- CREATE then DROP: exact. DROP t then CREATE t: NOT undone (the rows are lost).
- UPDATE then UPDATE with the old value: exact (update is undone by itself).
- +2 then -2, -2 then +2: exact. *2 then /2: exact. /2 then *2: NOT (integer division loses 1 and 3).
- join (||) then cut (substr) at the join: exact. cut into two pieces then join them: exact.
- NOT twice: the same program as none. = and <> : complements (together all rows, apart no row), not undo.
- read (SELECT) then anything: there is nothing to undo; read changes nothing. No partner.
- The owner's guessed pairs that I expect NOT to undo: read/write, hear/say (both only add rows), find/move, delete/spawn.
