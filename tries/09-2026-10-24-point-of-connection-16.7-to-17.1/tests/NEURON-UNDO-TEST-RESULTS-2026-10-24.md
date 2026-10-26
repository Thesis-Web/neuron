# Undo test results (2026-10-24)
Predictions frozen at 19:30 before the run: NEURON-UNDO-TEST-EXPECT-2026-10-24.md (sha256 2c75f85c0375...). Every prediction held.
One test line was wrong in my first run (it cut a different text than it compared with); fixed and rerun. Numbers below come from undo.json.

SQLite 3.37.2. Start: t (a INTEGER, b TEXT) with rows (1,'x'), (2,'y'), (3,'z'). Exact = same schema, rows and rowids. Content = same rows, rowids ignored.

| A then B | Back to the start? |
|---|---|
| INSERT then DELETE that row | exactly |
| DELETE then INSERT it back | content only (the row has a new rowid) |
| CREATE then DROP | exactly |
| DROP t then CREATE t | no |
| UPDATE then UPDATE with the old value | exactly |
| copy (INSERT ... SELECT) then DELETE the copy | exactly |
| read (SELECT) then write (INSERT what was read) | no (A changed nothing) |
| write (INSERT) then read (SELECT) | no |
| DELETE then CREATE (delete / spawn) | no |
| +2 then -2 | exactly |
| -2 then +2 | exactly |
| *2 then /2 | exactly |
| /2 then *2 | no: [0, 2, 2] from [1, 2, 3] |
| join (\|\| 'k') then cut back (substr) | exactly |
| cut 'hello' into two pieces then join them | exactly |
| cut 'store' into two pieces then join them | exactly |
| cut 'a b c' into two pieces then join them | exactly |
| NOT twice | the same program as no NOT |
| = and <> | complements: together all rows, overlap none |
