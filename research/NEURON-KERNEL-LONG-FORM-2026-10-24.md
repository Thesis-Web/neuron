# The long form: what each SQL word runs inside SQLite (kernel log)

SQLite is the crutch: the brain hands SQL text to mother, and SQLite turns it into these steps (its bytecode) and runs them in its C code.
The brain cannot run these steps itself. This file keeps them, so a kernel built later knows what each word must do.
Programs from the page's SQLite (3.39.3), test table t (a INTEGER, b TEXT) with 3 rows. Step descriptions are SQLite's own, from sqlite.org/opcode.html (fetched 2026-10-24).
Each line is: step name, then SQLite's registers P1 P2 P3, P4, P5, then the description.

## SELECT
With the word: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## INSERT
With the word: `INSERT INTO t VALUES (4, 'w')`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenWrite         0    2    0  2                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Integer           4    2    0                                 0  The 32-bit integer value P1 is written into register P2.
String8           0    3    0  w                              0  P4 points to a nul terminated UTF-8 string.
NewRowid          0    1    0                                 0  Get a new integer record number (a.k.a "rowid") used as the key to a table.
MakeRecord        2    2    4  DB                             0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            0    4    1  t                             57  Write an entry into the table of cursor P1.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## UPDATE
With the word: `UPDATE t SET b = 'q' WHERE a = 1`
```
Init              0   15    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Null              0    1    2                                 0  Write a NULL into registers P2.
Noop              1    0    1                                 0  Do nothing.
OpenWrite         0    2    0  2                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Rewind            0   14    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    5                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                6   13    5  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Rowid             0    2    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
IsNull            2   14    0                                 0  Jump to P2 if the value in register P1 is NULL.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
String8           0    4    0  q                              0  P4 points to a nul terminated UTF-8 string.
MakeRecord        3    2    1  DB                             0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            0    1    2  t                              7  Write an entry into the table of cursor P1.
Next              0    5    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           1    6    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## DELETE
With the word: `DELETE FROM t WHERE a = 1`
```
Init              0   10    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Null              0    1    0                                 0  Write a NULL into registers P2.
OpenWrite         0    2    0  2                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Rewind            0    9    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                3    8    2  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Rowid             0    4    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
Delete            0    1    0  t                              2  Delete the record at which the P1 cursor is currently pointing.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           1    3    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## CREATE
With the word: `CREATE TABLE u (c)`
```
Init              0   28    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
ReadCookie        0    3    2                                 0  Read cookie number P3 from database P1 and write it into register P2.
If                3    5    0                                 0  Jump to P2 if the value in register P1 is true.
SetCookie         0    2    4                                 0  Write the integer value P3 into cookie number P2 of database P1.
SetCookie         0    5    1                                 0  Write the integer value P3 into cookie number P2 of database P1.
CreateBtree       0    2    1                                 0  Allocate a new b-tree in the main database file if P1==0 or in the TEMP database file if P1==1 or in an attached database if P1>1.
OpenWrite         0    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
NewRowid          0    1    0                                 0  Get a new integer record number (a.k.a "rowid") used as the key to a table.
Blob              6    3    0                                0  P4 points to a blob of data P1 bytes long.
Insert            0    3    1                                 8  Write an entry into the table of cursor P1.
Close             0    0    0                                 0  Close a cursor previously opened as P1.
Close             0    0    0                                 0  Close a cursor previously opened as P1.
Null              0    4    5                                 0  Write a NULL into registers P2.
Noop              2    0    4                                 0  Do nothing.
OpenWrite         1    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
SeekRowid         1   17    1                                 0  P1 is the index of a cursor open on an SQL table btree (with integer keys).
Rowid             1    5    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
IsNull            5   25    0                                 0  Jump to P2 if the value in register P1 is NULL.
String8           0    6    0  table                          0  P4 points to a nul terminated UTF-8 string.
String8           0    7    0  u                              0  P4 points to a nul terminated UTF-8 string.
String8           0    8    0  u                              0  P4 points to a nul terminated UTF-8 string.
SCopy             2    9    0                                 0  Make a shallow copy of register P1 into register P2.
String8           0   10    0  CREATE TABLE u (c)             0  P4 points to a nul terminated UTF-8 string.
MakeRecord        6    5    4  BBBDB                          0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            1    4    5                                 0  Write an entry into the table of cursor P1.
SetCookie         0    1    2                                 0  Write the integer value P3 into cookie number P2 of database P1.
ParseSchema       0    0    0  tbl_name='u' AND type!='trig   0  Read and parse all entries from the schema table of database P1 that match the WHERE clause P4.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## WITH
With the word: `WITH c AS (SELECT a FROM t) SELECT a FROM c`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          1    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            1    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            1    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              1    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM (SELECT a FROM t)`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          1    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            1    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            1    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              1    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## FROM
With the word: `SELECT 1 FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  0                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Integer           1    1    0                                 0  The 32-bit integer value P1 is written into register P2.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT 1`
```
Init              0    1    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Integer           1    1    0                                 0  The 32-bit integer value P1 is written into register P2.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Halt              0    0    0                                 0  Exit immediately.
```

## WHERE
With the word: `SELECT a FROM t WHERE a = 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    7    1  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## =
With the word: `SELECT a FROM t WHERE a = 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    7    1  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
IfNot             1    7    1                                 0  Jump to P2 if the value in register P1 is False.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## >
With the word: `SELECT a FROM t WHERE a > 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Le                2    7    1  BINARY-8                      84  This works just like the Lt opcode except that the jump is taken if the content of register P3 is less than or equal to the content of register P1.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
IfNot             1    7    1                                 0  Jump to P2 if the value in register P1 is False.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## <
With the word: `SELECT a FROM t WHERE a < 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ge                2    7    1  BINARY-8                      84  This works just like the Lt opcode except that the jump is taken if the content of register P3 is greater than or equal to the content of register P1.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
IfNot             1    7    1                                 0  Jump to P2 if the value in register P1 is False.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## IS
With the word: `SELECT a FROM t WHERE a IS 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    7    1  BINARY-8                     196  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a = 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    7    1  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## NOT
With the word: `SELECT a FROM t WHERE NOT a = 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Eq                2    7    1  BINARY-8                      84  Compare the values in register P1 and P3.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a = 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    7    1  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## AND
With the word: `SELECT a FROM t WHERE a = 2 AND b = 'y'`
```
Init              0   11    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0   10    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    9    1  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                3    9    1  BINARY-8                      82  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    4                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         4    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
String8           0    3    0  y                              0  P4 points to a nul terminated UTF-8 string.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a = 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    7    1  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## OR
With the word: `SELECT a FROM t WHERE a = 2 OR b = 'x'`
```
Init              0   11    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0   10    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Eq                2    7    1  BINARY-8                      68  Compare the values in register P1 and P3.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                3    9    1  BINARY-8                      82  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    4                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         4    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
String8           0    3    0  x                              0  P4 points to a nul terminated UTF-8 string.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a = 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    7    1  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## IN
With the word: `SELECT a FROM t WHERE a IN (1, 2)`
```
Init              0   10    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    9    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Eq                1    6    2  BINARY-8                      68  Compare the values in register P1 and P3.
Ne                1    8    3  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    4                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         4    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           1    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Integer           2    3    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a = 1`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    7    1  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           1    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## LIKE
With the word: `SELECT a FROM t WHERE b LIKE 'y'`
```
Init              0   10    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    9    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Function          1    2    1  like(2)                        0  Invoke a user function (P4 is a pointer to an sqlite3_context object that contains a pointer to the function to be run) with arguments taken from register P2 and successors.
IfNot             1    8    1                                 0  Jump to P2 if the value in register P1 is False.
Column            0    0    4                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         4    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
String8           0    2    0  y                              0  P4 points to a nul terminated UTF-8 string.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE b = 'y'`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2    7    1  BINARY-8                      82  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
String8           0    2    0  y                              0  P4 points to a nul terminated UTF-8 string.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## EXISTS
With the word: `SELECT EXISTS (SELECT 1 FROM t WHERE a = 2)`
```
Init              0   16    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
BeginSubrtn       0    2    0                                 0  Mark the beginning of a subroutine that can be entered in-line or that can be called using Gosub .
Once              0   12    0                                 0  Fall through to the next instruction the first time this opcode is encountered on each invocation of the byte-code program.
Integer           0    3    0                                 0  The 32-bit integer value P1 is written into register P2.
Integer           1    4    0                                 0  The 32-bit integer value P1 is written into register P2.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0   12    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    5                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                6   11    5  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Integer           1    3    0                                 0  The 32-bit integer value P1 is written into register P2.
DecrJumpZero      4   12    0                                 0  Register P1 must hold an integer.
Next              0    7    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Return            2    2    1                                 0  Jump to the address stored in register P1.
Copy              3    1    0                                 0  Make a copy of registers P1..P1+P3 into registers P2..P2+P3.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    6    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT (SELECT 1 FROM t WHERE a = 2)`
```
Init              0   16    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
BeginSubrtn       0    2    0                                 0  Mark the beginning of a subroutine that can be entered in-line or that can be called using Gosub .
Once              0   12    0                                 0  Fall through to the next instruction the first time this opcode is encountered on each invocation of the byte-code program.
Null              0    3    3                                 0  Write a NULL into registers P2.
Integer           1    4    0                                 0  The 32-bit integer value P1 is written into register P2.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0   12    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    5                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                6   11    5  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Integer           1    3    0                                 0  The 32-bit integer value P1 is written into register P2.
DecrJumpZero      4   12    0                                 0  Register P1 must hold an integer.
Next              0    7    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Return            2    2    1                                 0  Jump to the address stored in register P1.
Copy              3    1    0                                 0  Make a copy of registers P1..P1+P3 into registers P2..P2+P3.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    6    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## LIMIT
With the word: `SELECT a FROM t LIMIT 1`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Integer           1    1    0                                 0  The 32-bit integer value P1 is written into register P2.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
DecrJumpZero      1    8    0                                 0  Register P1 must hold an integer.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## ORDER BY
With the word: `SELECT a FROM t ORDER BY b`
```
Init              0   16    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
SorterOpen        1    3    0  k(1,B)                         0  This opcode works like OpenEphemeral except that it opens a transient index that is specifically designed to sort large tables using an external merge-sort algorithm.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    9    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
MakeRecord        1    2    3                                 0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
SorterInsert      1    3    1  2                              0  Register P2 holds an SQL index key made using the MakeRecord instructions.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
OpenPseudo        2    4    3                                 0  Open a new cursor that points to a fake table that contains a single row of data.
SorterSort        1   15    0                                 0  After all records have been inserted into the Sorter object identified by P1, invoke this opcode to actually do the sorting.
SorterData        1    4    2                                 0  Write into register P2 the current sorter data for sorter cursor P1.
Column            2    1    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
SorterNext        1   11    0                                 0  This opcode works just like Next except that P1 must be a sorter object for which the SorterSort opcode has been invoked.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## DESC
With the word: `SELECT a FROM t ORDER BY b DESC`
```
Init              0   16    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
SorterOpen        1    3    0  k(1,-B)                        0  This opcode works like OpenEphemeral except that it opens a transient index that is specifically designed to sort large tables using an external merge-sort algorithm.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    9    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
MakeRecord        1    2    3                                 0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
SorterInsert      1    3    1  2                              0  Register P2 holds an SQL index key made using the MakeRecord instructions.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
OpenPseudo        2    4    3                                 0  Open a new cursor that points to a fake table that contains a single row of data.
SorterSort        1   15    0                                 0  After all records have been inserted into the Sorter object identified by P1, invoke this opcode to actually do the sorting.
SorterData        1    4    2                                 0  Write into register P2 the current sorter data for sorter cursor P1.
Column            2    1    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
SorterNext        1   11    0                                 0  This opcode works just like Next except that P1 must be a sorter object for which the SorterSort opcode has been invoked.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t ORDER BY b`
```
Init              0   16    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
SorterOpen        1    3    0  k(1,B)                         0  This opcode works like OpenEphemeral except that it opens a transient index that is specifically designed to sort large tables using an external merge-sort algorithm.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    9    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
MakeRecord        1    2    3                                 0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
SorterInsert      1    3    1  2                              0  Register P2 holds an SQL index key made using the MakeRecord instructions.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
OpenPseudo        2    4    3                                 0  Open a new cursor that points to a fake table that contains a single row of data.
SorterSort        1   15    0                                 0  After all records have been inserted into the Sorter object identified by P1, invoke this opcode to actually do the sorting.
SorterData        1    4    2                                 0  Write into register P2 the current sorter data for sorter cursor P1.
Column            2    1    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
SorterNext        1   11    0                                 0  This opcode works just like Next except that P1 must be a sorter object for which the SorterSort opcode has been invoked.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## NULL
With the word: `SELECT NULL`
```
Init              0    1    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Null              0    1    0                                 0  Write a NULL into registers P2.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Halt              0    0    0                                 0  Exit immediately.
```
Without it: `SELECT 1`
```
Init              0    1    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Integer           1    1    0                                 0  The 32-bit integer value P1 is written into register P2.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Halt              0    0    0                                 0  Exit immediately.
```

## CAST
With the word: `SELECT CAST(b AS INTEGER) FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Cast              1   68    0                                 0  Force the value in register P1 to be the type defined by P2.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT b FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## AS
With the word: `SELECT a AS k FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## INTEGER
With the word: `SELECT CAST(b AS INTEGER) FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Cast              1   68    0                                 0  Force the value in register P1 to be the type defined by P2.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT CAST(b AS TEXT) FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Cast              1   66    0                                 0  Force the value in register P1 to be the type defined by P2.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## INTEGER
With the word: `CREATE TABLE u (c INTEGER)`
```
Init              0   28    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
ReadCookie        0    3    2                                 0  Read cookie number P3 from database P1 and write it into register P2.
If                3    5    0                                 0  Jump to P2 if the value in register P1 is true.
SetCookie         0    2    4                                 0  Write the integer value P3 into cookie number P2 of database P1.
SetCookie         0    5    1                                 0  Write the integer value P3 into cookie number P2 of database P1.
CreateBtree       0    2    1                                 0  Allocate a new b-tree in the main database file if P1==0 or in the TEMP database file if P1==1 or in an attached database if P1>1.
OpenWrite         0    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
NewRowid          0    1    0                                 0  Get a new integer record number (a.k.a "rowid") used as the key to a table.
Blob              6    3    0                                0  P4 points to a blob of data P1 bytes long.
Insert            0    3    1                                 8  Write an entry into the table of cursor P1.
Close             0    0    0                                 0  Close a cursor previously opened as P1.
Close             0    0    0                                 0  Close a cursor previously opened as P1.
Null              0    4    5                                 0  Write a NULL into registers P2.
Noop              2    0    4                                 0  Do nothing.
OpenWrite         1    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
SeekRowid         1   17    1                                 0  P1 is the index of a cursor open on an SQL table btree (with integer keys).
Rowid             1    5    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
IsNull            5   25    0                                 0  Jump to P2 if the value in register P1 is NULL.
String8           0    6    0  table                          0  P4 points to a nul terminated UTF-8 string.
String8           0    7    0  u                              0  P4 points to a nul terminated UTF-8 string.
String8           0    8    0  u                              0  P4 points to a nul terminated UTF-8 string.
SCopy             2    9    0                                 0  Make a shallow copy of register P1 into register P2.
String8           0   10    0  CREATE TABLE u (c INTEGER)     0  P4 points to a nul terminated UTF-8 string.
MakeRecord        6    5    4  BBBDB                          0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            1    4    5                                 0  Write an entry into the table of cursor P1.
SetCookie         0    1    2                                 0  Write the integer value P3 into cookie number P2 of database P1.
ParseSchema       0    0    0  tbl_name='u' AND type!='trig   0  Read and parse all entries from the schema table of database P1 that match the WHERE clause P4.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `CREATE TABLE u (c)`
```
Init              0   28    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
ReadCookie        0    3    2                                 0  Read cookie number P3 from database P1 and write it into register P2.
If                3    5    0                                 0  Jump to P2 if the value in register P1 is true.
SetCookie         0    2    4                                 0  Write the integer value P3 into cookie number P2 of database P1.
SetCookie         0    5    1                                 0  Write the integer value P3 into cookie number P2 of database P1.
CreateBtree       0    2    1                                 0  Allocate a new b-tree in the main database file if P1==0 or in the TEMP database file if P1==1 or in an attached database if P1>1.
OpenWrite         0    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
NewRowid          0    1    0                                 0  Get a new integer record number (a.k.a "rowid") used as the key to a table.
Blob              6    3    0                                0  P4 points to a blob of data P1 bytes long.
Insert            0    3    1                                 8  Write an entry into the table of cursor P1.
Close             0    0    0                                 0  Close a cursor previously opened as P1.
Close             0    0    0                                 0  Close a cursor previously opened as P1.
Null              0    4    5                                 0  Write a NULL into registers P2.
Noop              2    0    4                                 0  Do nothing.
OpenWrite         1    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
SeekRowid         1   17    1                                 0  P1 is the index of a cursor open on an SQL table btree (with integer keys).
Rowid             1    5    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
IsNull            5   25    0                                 0  Jump to P2 if the value in register P1 is NULL.
String8           0    6    0  table                          0  P4 points to a nul terminated UTF-8 string.
String8           0    7    0  u                              0  P4 points to a nul terminated UTF-8 string.
String8           0    8    0  u                              0  P4 points to a nul terminated UTF-8 string.
SCopy             2    9    0                                 0  Make a shallow copy of register P1 into register P2.
String8           0   10    0  CREATE TABLE u (c)             0  P4 points to a nul terminated UTF-8 string.
MakeRecord        6    5    4  BBBDB                          0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            1    4    5                                 0  Write an entry into the table of cursor P1.
SetCookie         0    1    2                                 0  Write the integer value P3 into cookie number P2 of database P1.
ParseSchema       0    0    0  tbl_name='u' AND type!='trig   0  Read and parse all entries from the schema table of database P1 that match the WHERE clause P4.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## VALUES
With the word: `INSERT INTO t VALUES (4, 'w')`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenWrite         0    2    0  2                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Integer           4    2    0                                 0  The 32-bit integer value P1 is written into register P2.
String8           0    3    0  w                              0  P4 points to a nul terminated UTF-8 string.
NewRowid          0    1    0                                 0  Get a new integer record number (a.k.a "rowid") used as the key to a table.
MakeRecord        2    2    4  DB                             0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            0    4    1  t                             57  Write an entry into the table of cursor P1.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `INSERT INTO t SELECT 4, 'w'`
```
Init              0   13    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
InitCoroutine     4    6    2                                 0  Set up register P1 so that it will Yield to the coroutine located at address P3.
Integer           4    2    0                                 0  The 32-bit integer value P1 is written into register P2.
String8           0    3    0  w                              0  P4 points to a nul terminated UTF-8 string.
Yield             4    0    0                                 0  Swap the program counter with the value in register P1.
EndCoroutine      4    0    0                                 0  The instruction at the address in register P1 is a Yield .
OpenWrite         0    2    0  2                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Yield             4   12    0                                 0  Swap the program counter with the value in register P1.
NewRowid          0    1    0                                 0  Get a new integer record number (a.k.a "rowid") used as the key to a table.
MakeRecord        2    2    5  DB                             0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            0    5    1  t                             57  Write an entry into the table of cursor P1.
Goto              0    7    0                                 0  An unconditional jump to address P2.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## INTO
With the word: `INSERT INTO t VALUES (4, 'w')`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenWrite         0    2    0  2                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Integer           4    2    0                                 0  The 32-bit integer value P1 is written into register P2.
String8           0    3    0  w                              0  P4 points to a nul terminated UTF-8 string.
NewRowid          0    1    0                                 0  Get a new integer record number (a.k.a "rowid") used as the key to a table.
MakeRecord        2    2    4  DB                             0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            0    4    1  t                             57  Write an entry into the table of cursor P1.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `INSERT t VALUES (4, 'w')` (SQLite refuses it: near "t": syntax error)

## SET
With the word: `UPDATE t SET b = 'q' WHERE a = 1`
```
Init              0   15    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Null              0    1    2                                 0  Write a NULL into registers P2.
Noop              1    0    1                                 0  Do nothing.
OpenWrite         0    2    0  2                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Rewind            0   14    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    5                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                6   13    5  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Rowid             0    2    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
IsNull            2   14    0                                 0  Jump to P2 if the value in register P1 is NULL.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
String8           0    4    0  q                              0  P4 points to a nul terminated UTF-8 string.
MakeRecord        3    2    1  DB                             0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            0    1    2  t                              7  Write an entry into the table of cursor P1.
Next              0    5    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           1    6    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `UPDATE t b = 'q' WHERE a = 1` (SQLite refuses it: near "b": syntax error)

## TABLE
With the word: `CREATE TABLE u (c)`
```
Init              0   28    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
ReadCookie        0    3    2                                 0  Read cookie number P3 from database P1 and write it into register P2.
If                3    5    0                                 0  Jump to P2 if the value in register P1 is true.
SetCookie         0    2    4                                 0  Write the integer value P3 into cookie number P2 of database P1.
SetCookie         0    5    1                                 0  Write the integer value P3 into cookie number P2 of database P1.
CreateBtree       0    2    1                                 0  Allocate a new b-tree in the main database file if P1==0 or in the TEMP database file if P1==1 or in an attached database if P1>1.
OpenWrite         0    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
NewRowid          0    1    0                                 0  Get a new integer record number (a.k.a "rowid") used as the key to a table.
Blob              6    3    0                                0  P4 points to a blob of data P1 bytes long.
Insert            0    3    1                                 8  Write an entry into the table of cursor P1.
Close             0    0    0                                 0  Close a cursor previously opened as P1.
Close             0    0    0                                 0  Close a cursor previously opened as P1.
Null              0    4    5                                 0  Write a NULL into registers P2.
Noop              2    0    4                                 0  Do nothing.
OpenWrite         1    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
SeekRowid         1   17    1                                 0  P1 is the index of a cursor open on an SQL table btree (with integer keys).
Rowid             1    5    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
IsNull            5   25    0                                 0  Jump to P2 if the value in register P1 is NULL.
String8           0    6    0  table                          0  P4 points to a nul terminated UTF-8 string.
String8           0    7    0  u                              0  P4 points to a nul terminated UTF-8 string.
String8           0    8    0  u                              0  P4 points to a nul terminated UTF-8 string.
SCopy             2    9    0                                 0  Make a shallow copy of register P1 into register P2.
String8           0   10    0  CREATE TABLE u (c)             0  P4 points to a nul terminated UTF-8 string.
MakeRecord        6    5    4  BBBDB                          0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            1    4    5                                 0  Write an entry into the table of cursor P1.
SetCookie         0    1    2                                 0  Write the integer value P3 into cookie number P2 of database P1.
ParseSchema       0    0    0  tbl_name='u' AND type!='trig   0  Read and parse all entries from the schema table of database P1 that match the WHERE clause P4.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `CREATE u (c)` (SQLite refuses it: near "u": syntax error)

## instr
With the word: `SELECT instr(b, 'y') FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Function          2    2    1  instr(2)                       0  Invoke a user function (P4 is a pointer to an sqlite3_context object that contains a pointer to the function to be run) with arguments taken from register P2 and successors.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
String8           0    3    0  y                              0  P4 points to a nul terminated UTF-8 string.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT b FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## count
With the word: `SELECT count(a) FROM t`
```
Init              0   11    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Null              0    1    2                                 0  Write a NULL into registers P2.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
AggStep           0    3    1  count(1)                       1  Execute the xStep function for an aggregate.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
AggFinal          1    1    0  count(1)                       0  P1 is the memory location that is the accumulator for an aggregate or window function.
Copy              1    4    0                                 0  Make a copy of registers P1..P1+P3 into registers P2..P2+P3.
ResultRow         4    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## max
With the word: `SELECT max(a) FROM t`
```
Init              0   12    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Null              0    1    2                                 0  Write a NULL into registers P2.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
CollSeq           0    0    0  BINARY-8                       0  P4 is a pointer to a CollSeq object.
AggStep           0    3    1  max(1)                         1  Execute the xStep function for an aggregate.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
AggFinal          1    1    0  max(1)                         0  P1 is the memory location that is the accumulator for an aggregate or window function.
Copy              1    4    0                                 0  Make a copy of registers P1..P1+P3 into registers P2..P2+P3.
ResultRow         4    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## group_concat
With the word: `SELECT group_concat(b) FROM t`
```
Init              0   11    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Null              0    1    2                                 0  Write a NULL into registers P2.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
AggStep           0    3    1  group_concat(1)                1  Execute the xStep function for an aggregate.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
AggFinal          1    1    0  group_concat(1)                0  P1 is the memory location that is the accumulator for an aggregate or window function.
Copy              1    4    0                                 0  Make a copy of registers P1..P1+P3 into registers P2..P2+P3.
ResultRow         4    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT b FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## ( )
With the word: `SELECT (a) FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## ,
With the word: `SELECT a, b FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Column            0    1    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    2    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## ;
With the word: `SELECT a FROM t;`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## * (all columns)
With the word: `SELECT * FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Column            0    1    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    2    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## * (times)
With the word: `SELECT a * 2 FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Multiply          3    2    1                                 0  Multiply the value in register P1 by the value in register P2 and store the result in register P3.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    3    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## ||
With the word: `SELECT b || 'x' FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Concat            3    2    1                                 0  Add the text in register P1 onto the end of the text in register P2 and store the result in register P3.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
String8           0    3    0  x                              0  P4 points to a nul terminated UTF-8 string.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT b FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## = (in SET)
With the word: `UPDATE t SET b = 'q' WHERE a = 1`
```
Init              0   15    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Null              0    1    2                                 0  Write a NULL into registers P2.
Noop              1    0    1                                 0  Do nothing.
OpenWrite         0    2    0  2                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Rewind            0   14    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    5                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                6   13    5  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Rowid             0    2    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
IsNull            2   14    0                                 0  Jump to P2 if the value in register P1 is NULL.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
String8           0    4    0  q                              0  P4 points to a nul terminated UTF-8 string.
MakeRecord        3    2    1  DB                             0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            0    1    2  t                              7  Write an entry into the table of cursor P1.
Next              0    5    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           1    6    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `UPDATE t SET b 'q' WHERE a = 1` (SQLite refuses it: near "'q'": syntax error)

## <> (not told)
With the word: `SELECT a FROM t WHERE a <> 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Eq                2    7    1  BINARY-8                      84  Compare the values in register P1 and P3.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
IfNot             1    7    1                                 0  Jump to P2 if the value in register P1 is False.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## != (not told)
With the word: `SELECT a FROM t WHERE a != 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Eq                2    7    1  BINARY-8                      84  Compare the values in register P1 and P3.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
IfNot             1    7    1                                 0  Jump to P2 if the value in register P1 is False.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## >= (not told)
With the word: `SELECT a FROM t WHERE a >= 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Lt                2    7    1  BINARY-8                      84  Compare the values in register P1 and P3.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
IfNot             1    7    1                                 0  Jump to P2 if the value in register P1 is False.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## <= (not told)
With the word: `SELECT a FROM t WHERE a <= 2`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Gt                2    7    1  BINARY-8                      84  This works just like the Lt opcode except that the jump is taken if the content of register P3 is greater than the content of register P1.
Column            0    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    2    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t WHERE a`
```
Init              0    9    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
IfNot             1    7    1                                 0  Jump to P2 if the value in register P1 is False.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         2    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## DROP (not told)
With the word: `DROP TABLE u`
```
Init              0   37    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Null              0    1    0                                 0  Write a NULL into registers P2.
OpenWrite         0    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Rewind            0   11    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    2    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                3   10    2  BINARY-8                      82  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Eq                4   10    2  BINARY-8                      82  Compare the values in register P1 and P3.
Rowid             0    5    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
Delete            0    0    0                                 2  Delete the record at which the P1 cursor is currently pointing.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Destroy           3    2    0                                 0  Delete an entire database table or index whose root page in the database file is given by P1.
Null              0    6    7                                 0  Write a NULL into registers P2.
OpenEphemeral     2    0    6                                 0  Open a new cursor P1 to a transient table.
IfNot             2   22    1                                 0  Jump to P2 if the value in register P1 is False.
OpenRead          1    1    0  4                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            1   22    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            1    3   13                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Ne                2   21   13  BINARY-8                      84  This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal.
Rowid             1    7    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
Insert            2    6    7                                 0  Write an entry into the table of cursor P1.
Next              1   17    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
OpenWrite         1    1    0  5                              0  Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below).
Rewind            2   34    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Rowid             2    7    0                                 0  Store in register P2 an integer which is the key of the table entry that P1 is currently point to.
NotExists         1   33    7                                 0  P1 is the index of a cursor open on an SQL table btree (with integer keys).
Column            1    0    8                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Column            1    1    9                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Column            1    2   10                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Integer           3   11    0                                 0  The 32-bit integer value P1 is written into register P2.
Column            1    4   12                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
MakeRecord        8    5   15  BBBDB                          0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
Insert            1   15    7                                 0  Write an entry into the table of cursor P1.
Next              2   24    0                                 0  Advance cursor P1 so that it points to the next key/data pair in its table or index.
DropTable         0    0    0  u                              0  Remove the internal (in-memory) data structures that describe the table named P4 in database P1.
SetCookie         0    1    3                                 0  Write the integer value P3 into cookie number P2 of database P1.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    2  0                              1  Begin a transaction on database P1 if a transaction is not already active.
String8           0    3    0  u                              0  P4 points to a nul terminated UTF-8 string.
String8           0    4    0  trigger                        0  P4 points to a nul terminated UTF-8 string.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## EXCEPT (not told)
With the word: `SELECT a FROM t EXCEPT SELECT 1`
```
Init              0   16    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenEphemeral     1    1    0  k(1,B)                         0  Open a new cursor P1 to a transient table.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    8    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
MakeRecord        1    1    2                                 0  Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index.
IdxInsert         1    2    1  1                              0  Register P2 holds an SQL index key made using the MakeRecord instructions.
Next              0    4    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Integer           1    1    0                                 0  The 32-bit integer value P1 is written into register P2.
IdxDelete         1    1    1                                 0  The content of P5 registers starting at register P2 form an unpacked index key.
Rewind            1   14    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            1    0    3                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         3    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              1   11    0                                 0  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Close             1    0    0                                 0  Close a cursor previously opened as P1.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## + (not told)
With the word: `SELECT a + 2 FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Add               3    2    1                                 0  Add the value in register P1 to the value in register P2 and store the result in register P3.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    3    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## - (not told)
With the word: `SELECT a - 2 FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Subtract          3    2    1                                 0  Subtract the value in register P1 from the value in register P2 and store the result in register P3.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    3    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## / (not told)
With the word: `SELECT a / 2 FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Divide            3    2    1                                 0  Divide the value in register P1 by the value in register P2 and store the result in register P3 (P3=P2/P1).
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           2    3    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT a FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  1                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    0    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## DELETE (no WHERE) (not told)
With the word: `DELETE FROM t`
```
Init              0    3    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
Clear             2    0   -1  t                              0  Delete all contents of the database table or index whose root page in the database file is given by P1.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    1    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## substr (not told)
With the word: `SELECT substr(b, 1, 1) FROM t`
```
Init              0    8    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    7    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    2                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
Function          6    2    1  substr(3)                      0  Invoke a user function (P4 is a pointer to an sqlite3_context object that contains a pointer to the function to be run) with arguments taken from register P2 and successors.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Integer           1    3    0                                 0  The 32-bit integer value P1 is written into register P2.
Integer           1    4    0                                 0  The 32-bit integer value P1 is written into register P2.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```
Without it: `SELECT b FROM t`
```
Init              0    7    0                                 0  Programs contain a single instance of this opcode as the very first opcode.
OpenRead          0    2    0  2                              0  Open a read-only cursor for the database table whose root page is P2 in a database file.
Rewind            0    6    0                                 0  The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index.
Column            0    1    1                                 0  Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction.
ResultRow         1    1    0                                 0  The registers P1 through P1+P2-1 contain a single row of results.
Next              0    3    0                                 1  Advance cursor P1 so that it points to the next key/data pair in its table or index.
Halt              0    0    0                                 0  Exit immediately.
Transaction       0    0    1  0                              1  Begin a transaction on database P1 if a transaction is not already active.
Goto              0    1    0                                 0  An unconditional jump to address P2.
```

## The told physics: steps inside each told trigger (counts, page SQLite)
Each trigger's whole program is in b3.json; here, how many of each step it holds, brain work and log (the event rows the page draws from) apart.
- **input_teach** (input): Integer 21, Param 15, String8 14, Null 13, Function:instr 8, Function:substr 5, Subtract 4, Ne 3, MakeRecord 3, NewRowid 3, Insert 3, Column 3, If 2, BeginSubrtn 2, Once 2, OpenRead 2, DecrJumpZero 2, Return 2, Yield 2, Goto 2, OpenWrite 2, SoftNull 2, Program 2, ResetCount 2, Le 1, Function:like 1, InitCoroutine 1, IsNull 1, Affinity 1, SeekGE 1, IdxGT 1, EndCoroutine 1, OpenEphemeral 1, Rewind 1, Next 1, Close 1, Add 1, Function:trim 1, Last 1, Rowid 1, CollSeq 1, AggStep 1, Prev 1, AggFinal 1, SCopy 1, NotNull 1, Copy 1; log: 35 steps
- **input_bind** (input): Null 13, Integer 10, Param 9, String8 9, Function:instr 3, OpenWrite 2, SoftNull 2, Function:substr 2, Function:trim 2, NewRowid 2, MakeRecord 2, Insert 2, ResetCount 2, Ne 1, Le 1, Subtract 1, Add 1, Function:replace 1, BeginSubrtn 1, Once 1, OpenRead 1, Last 1, Rowid 1, CollSeq 1, AggStep 1, Goto 1, Prev 1, AggFinal 1, SCopy 1, NotNull 1, DecrJumpZero 1, Return 1, Copy 1, Program 1, Halt 1
- **input_run** (input): Param 24, Integer 16, String8 14, Function:instr 9, Null 8, Ne 4, Le 3, Function:substr 3, Goto 3, Subtract 2, Function:like 2, Function:trim 2, IfNot 1, Gt 1, OpenWrite 1, SoftNull 1, Add 1, BeginSubrtn 1, Once 1, OpenRead 1, Last 1, Rowid 1, CollSeq 1, AggStep 1, Prev 1, AggFinal 1, SCopy 1, NotNull 1, DecrJumpZero 1, Return 1, Copy 1, NewRowid 1, MakeRecord 1, Insert 1, Program 1, ResetCount 1, Halt 1
- **run_go** (run): Null 58, SCopy 48, Param 32, Column 32, String8 29, Integer 27, Goto 19, BeginSubrtn 19, Once 19, OpenRead 19, DecrJumpZero 19, Return 19, Copy 17, Yield 16, SeekRowid 11, Rowid 11, Ne 11, OpenWrite 10, MakeRecord 10, Insert 10, ResetCount 10, NotNull 9, CollSeq 9, AggStep 9, Prev 9, AggFinal 9, SoftNull 9, NewRowid 9, InitCoroutine 8, Last 8, EndCoroutine 8, Program 3, IsNull 2, Noop 1, SeekLT 1, Halt 1
- **run_said** (run): Param 1, NotNull 1; log: 97 steps
- **encode_word** (encode): Column 34, String8 33, Integer 27, Param 23, Concat 18, Function:trim 17, MakeRecord 10, OpenRead 9, BeginSubrtn 8, Once 8, Return 8, Null 8, Function:instr 7, Function:substr 7, DecrJumpZero 7, Ne 7, Subtract 6, Insert 6, IsNull 5, SeekRowid 5, NewRowid 5, Affinity 4, Goto 4, Yield 4, OpenWrite 4, Program 4, ResetCount 4, IdxInsert 4, SeekGE 3, IdxGT 3, OpenEphemeral 3, Rewind 3, SoftNull 3, Next 3, InitCoroutine 2, If 2, EndCoroutine 2, Close 2, Eq 1, DeferredSeek 1, NotFound 1, Noop 1, Rowid 1, IdxRowid 1, Add 1, Halt 1
- **encode_done** (encode): Param 6, Integer 6, Column 6, BeginSubrtn 4, Once 4, OpenRead 4, DecrJumpZero 4, Return 4, Yield 4, MakeRecord 4, NewRowid 4, Insert 4, String8 3, Ne 3, Null 3, SeekRowid 3, Rewind 3, Next 3, InitCoroutine 2, EndCoroutine 2, OpenEphemeral 2, Goto 2, OpenWrite 2, SoftNull 2, Program 2, Close 2, ResetCount 2, Function:trim 1, Eq 1, IfNot 1, Halt 1; log: 38 steps
- **born_go** (born): Null 19, String8 18, Param 17, Concat 13, Integer 11, OpenRead 10, BeginSubrtn 9, Once 9, DecrJumpZero 9, Return 9, Affinity 9, IsNull 8, SeekGE 8, IdxGT 8, IdxRowid 7, MakeRecord 5, OpenWrite 4, Goto 4, NewRowid 4, Insert 4, SoftNull 3, Function:like 3, ResetCount 3, Function:mother 3, Column 3, IfNot 2, If 2, SCopy 2, NotNull 2, Halt 2, Program 2, Yield 2, Function:glob 1, Last 1, Rowid 1, CollSeq 1, AggStep 1, Prev 1, AggFinal 1, Copy 1, IntCopy 1, NoConflict 1, IdxInsert 1, InitCoroutine 1, DeferredSeek 1, Ne 1, EndCoroutine 1, OpenEphemeral 1, Rewind 1, Next 1, Close 1; log: 40 steps
- **decide_go** (decide): Column 112, Integer 52, String8 38, Ne 24, Null 21, Function:trim 21, OpenRead 19, Concat 18, BeginSubrtn 17, Return 17, DecrJumpZero 16, IsNull 12, SeekRowid 11, Param 10, MakeRecord 9, Function:instr 8, Function:substr 8, Rowid 7, Copy 7, Once 7, OpenWrite 6, Insert 6, ResetCount 6, Rewind 6, Next 6, Noop 5, IfNot 5, Add 5, SeekGE 4, IdxGT 4, IdxRowid 4, Yield 4, SCopy 4, Prev 3, NotNull 3, IdxInsert 3, Affinity 3, Subtract 3, NewRowid 3, Goto 3, ZeroOrNull 2, MustBeInt 2, Last 2, If 2, OpenEphemeral 2, InitCoroutine 2, EndCoroutine 2, SoftNull 2, NotFound 1, Cast 1, SeekLT 1, Eq 1, Program 1, Close 1, Function:mother 1, CollSeq 1, AggStep 1, AggFinal 1, Delete 1, Halt 1; log: 57 steps
- **memhit_go** (memhit): Column 56, Integer 19, Null 17, OpenRead 11, BeginSubrtn 10, DecrJumpZero 10, Return 10, SeekRowid 9, Copy 8, Param 7, Rowid 7, Once 6, NotNull 6, MakeRecord 6, Insert 6, OpenWrite 5, ResetCount 5, Goto 4, Prev 4, String8 4, NewRowid 4, Noop 3, IsNull 3, Last 3, CollSeq 3, AggStep 3, AggFinal 3, SCopy 3, SoftNull 3, Function:trim 2, Concat 2, Ne 2, Yield 2, Add 1, InitCoroutine 1, Eq 1, Function:instr 1, Subtract 1, Function:substr 1, Cast 1, ZeroOrNull 1, MustBeInt 1, IfNot 1, SeekLT 1, EndCoroutine 1, OpenEphemeral 1, Rewind 1, Program 1, Next 1, Close 1; log: 153 steps
- **memwrong_go** (memwrong): Concat 12, String8 10, Null 9, Integer 7, BeginSubrtn 5, Once 5, OpenRead 5, DecrJumpZero 5, Return 5, SeekGE 3, IdxGT 3, IdxRowid 3, Param 2, Last 2, Rowid 2, CollSeq 2, AggStep 2, Goto 2, Prev 2, AggFinal 2, SCopy 2, NotNull 2, IsNull 1, Function:mother 1; log: 48 steps
- **lay_go** (lay): Concat 64, String8 48, Param 36, Null 27, Column 18, Integer 17, BeginSubrtn 15, Once 15, OpenRead 15, DecrJumpZero 15, Return 15, SeekRowid 13, NotNull 9, Goto 6, SCopy 6, Copy 6, Rowid 5, Function:quote 4, OpenWrite 3, IsNull 3, Last 3, CollSeq 3, AggStep 3, Prev 3, AggFinal 3, Function:mother 3, ResetCount 3, MakeRecord 2, Insert 2, Ne 2, Yield 2, Noop 1, SeekGE 1, IdxGT 1, IdxRowid 1, InitCoroutine 1, EndCoroutine 1, SoftNull 1, NewRowid 1, Delete 1, Halt 1; log: 133 steps
- **bind_go** (bindgo): Integer 87, Column 86, Null 62, BeginSubrtn 61, Once 61, OpenRead 61, DecrJumpZero 61, Return 61, String8 58, Function:trim 49, Concat 36, Copy 33, Rewind 28, Param 28, Next 28, SeekRowid 27, Ne 27, Function:instr 21, Function:substr 18, Add 13, SeekGE 7, IdxGT 7, IdxRowid 7, IsNull 6, Subtract 5, Affinity 5, Goto 4, Le 3, Yield 2, MakeRecord 2, NewRowid 2, Insert 2, InitCoroutine 1, EndCoroutine 1, OpenEphemeral 1, OpenWrite 1, SoftNull 1, Program 1, Close 1, ResetCount 1, Halt 1
- **bindrow_go** (bindrow): Column 14, Param 13, Null 12, Concat 10, String8 7, SeekRowid 4, MakeRecord 3, Insert 3, BeginSubrtn 3, Once 3, Integer 3, OpenRead 3, DecrJumpZero 3, Return 3, OpenWrite 2, IsNull 2, NotNull 2, Function:mother 2, ResetCount 2, Yield 2, NewRowid 2, Noop 1, Rowid 1, InitCoroutine 1, EndCoroutine 1, OpenEphemeral 1, Goto 1, Rewind 1, SoftNull 1, Program 1, Next 1, Close 1, Halt 1; log: 109 steps
- **fire_go** (fire): Column 59, Integer 41, Null 35, OpenRead 34, Param 31, BeginSubrtn 31, Return 31, Once 30, DecrJumpZero 30, SeekRowid 25, Copy 22, String8 18, Ne 14, MakeRecord 13, Next 10, IdxInsert 9, Rewind 8, Yield 8, Goto 7, InitCoroutine 6, SCopy 6, Noop 5, AggStep 5, AggFinal 5, NotNull 5, IsNull 4, Rowid 4, Insert 4, EndCoroutine 4, OpenWrite 3, OpenEphemeral 3, Eq 3, ResetCount 3, Concat 3, NewRowid 3, Program 3, SeekGE 2, IdxGT 2, Last 2, IdxRowid 2, CollSeq 2, Prev 2, If 2, Ge 2, SoftNull 2, Affinity 1, SeekGT 1, IfNot 1, Close 1, Halt 1
- **stmt_go** (stmt): Param 3, Function:mother 1, Halt 1; log: 18 steps
- **secondary_refused** (secondary): Column 21, Param 7, String8 6, Null 4, Integer 3, Concat 3, IsNull 2, OpenWrite 2, SeekRowid 2, MakeRecord 2, Insert 2, ResetCount 2, Ne 1, Eq 1, SoftNull 1, BeginSubrtn 1, Once 1, OpenRead 1, DecrJumpZero 1, Return 1, Copy 1, NewRowid 1, Noop 1, Rowid 1, Halt 1; log: 18 steps
- **secondary_ask** (secondary): Column 17, Param 16, Integer 14, Ne 12, Null 11, Copy 6, String8 5, Function:instr 4, BeginSubrtn 3, Once 3, OpenRead 3, Rewind 3, AggStep 3, Next 3, AggFinal 3, DecrJumpZero 3, Return 3, Eq 2, Le 2, Subtract 2, Function:substr 2, Goto 2, Program 2, NotNull 1, OpenWrite 1, SoftNull 1, NewRowid 1, MakeRecord 1, Insert 1, ResetCount 1, Halt 1
- **secondary_sql** (secondary): Param 15, String8 13, Integer 7, Null 6, Concat 5, Goto 5, Ne 2, IsNull 2, BeginSubrtn 2, Once 2, OpenRead 2, SeekRowid 2, Column 2, DecrJumpZero 2, Return 2, Copy 2, Function:like 2, Le 2, Program 2, OpenWrite 1, SoftNull 1, If 1, IfNot 1, NotNull 1, NewRowid 1, MakeRecord 1, Insert 1, ResetCount 1, Halt 1; log: 41 steps
- **secondary_wait** (secondary): Column 22, Null 10, Param 7, Integer 6, OpenWrite 3, BeginSubrtn 3, Once 3, OpenRead 3, SeekRowid 3, DecrJumpZero 3, Return 3, Copy 3, MakeRecord 3, Insert 3, ResetCount 3, String8 3, SoftNull 2, Rowid 2, NewRowid 2, Ne 1, Last 1, CollSeq 1, AggStep 1, Goto 1, Prev 1, AggFinal 1, SCopy 1, NotNull 1, Concat 1, Noop 1, IsNull 1, Halt 1; log: 16 steps
- **sense_ask** (sense): Column 61, Param 42, String8 39, Integer 33, Concat 25, Goto 17, Ne 14, Null 10, Le 10, Function:instr 9, SCopy 7, MakeRecord 6, Insert 6, OpenWrite 5, ResetCount 5, OpenRead 4, Subtract 4, Function:substr 4, Copy 4, NewRowid 4, Yield 4, SeekRowid 3, Rowid 3, BeginSubrtn 3, Once 3, Rewind 3, Next 3, DecrJumpZero 3, Return 3, SoftNull 3, Eq 2, Noop 2, IsNull 2, Function:lower 2, AggStep 2, AggFinal 2, InitCoroutine 2, EndCoroutine 2, Gt 1, ZeroOrNull 1, Last 1, CollSeq 1, Prev 1, NotNull 1, OpenEphemeral 1, Program 1, Close 1, Halt 1; log: 104 steps
- **sense_sql** (sense): Column 44, Integer 16, Param 15, Null 15, String8 12, Ne 9, BeginSubrtn 7, Once 7, OpenRead 7, DecrJumpZero 7, Return 7, SCopy 7, Goto 5, Copy 5, OpenWrite 4, Rowid 4, Function:like 4, MakeRecord 4, Insert 4, ResetCount 4, Rewind 4, Next 4, SeekRowid 3, NotNull 3, Noop 2, IsNull 2, IfNot 2, SoftNull 2, Le 2, Concat 2, Last 2, CollSeq 2, AggStep 2, Prev 2, AggFinal 2, NewRowid 2, Yield 2, InitCoroutine 1, EndCoroutine 1, If 1, Halt 1; log: 33 steps
- **definition_split** (definition): Param 6, String8 1, Eq 1, IsNull 1, OpenWrite 1, SoftNull 1, Null 1, NewRowid 1, MakeRecord 1, Insert 1, Program 1, ResetCount 1, Halt 1
- **defword_next** (defword): Param 8, String8 7, Function:trim 6, Concat 4, Integer 3, Function:instr 2, Function:substr 2, Eq 1, OpenWrite 1, SoftNull 1, Subtract 1, Add 1, NewRowid 1, MakeRecord 1, Insert 1, Program 1, ResetCount 1, Halt 1
- **say_go** (say): Null 4, Integer 3, BeginSubrtn 2, Once 2, OpenRead 2, Param 2, DecrJumpZero 2, Return 2, Copy 2, String8 2, OpenWrite 1, SoftNull 1, SeekRowid 1, Column 1, Last 1, Rowid 1, CollSeq 1, AggStep 1, Goto 1, Prev 1, AggFinal 1, SCopy 1, NotNull 1, NewRowid 1, MakeRecord 1, Insert 1, ResetCount 1; log: 21 steps
- **relation_drawn** (relation): ; log: 87 steps
- **formula_written** (formula): String8 6, Column 6, Null 4, Param 3, Goto 3, Integer 3, MakeRecord 3, OpenWrite 2, Ne 2, Insert 2, NewRowid 1, Affinity 1, SCopy 1, IntCopy 1, NoConflict 1, IdxRowid 1, SeekRowid 1, Noop 1, Rowid 1, Copy 1, Program 1, IdxInsert 1, ResetCount 1; log: 171 steps
- **source_go** (source): Column 48, Integer 41, String8 26, Param 23, Null 22, BeginSubrtn 17, Once 17, OpenRead 17, DecrJumpZero 17, Return 17, MakeRecord 15, Ne 15, Rewind 13, Next 13, Insert 12, Yield 12, SCopy 12, NewRowid 11, OpenWrite 9, ResetCount 8, Copy 8, SeekGE 7, IdxGT 7, SoftNull 7, Program 7, InitCoroutine 6, EndCoroutine 6, Goto 6, IdxRowid 6, OpenEphemeral 5, If 4, IfNot 4, Close 4, IsNull 3, Eq 3, IdxInsert 3, Affinity 2, SeekRowid 2, Noop 1, DeferredSeek 1, Rowid 1, Concat 1, NotNull 1, Function:trim 1, NotFound 1, Halt 1
- **agree_go** (agree): Column 13, Integer 12, MakeRecord 5, Return 5, Gosub 4, Null 3, Ne 3, Goto 3, OpenRead 2, Rewind 2, Param 2, Next 2, IfPos 2, IdxInsert 2, If 2, Yield 2, OpenWrite 2, Insert 2, InitCoroutine 1, SorterOpen 1, IsNull 1, Eq 1, Function:length 1, Le 1, SorterInsert 1, OpenPseudo 1, SorterSort 1, SorterData 1, Compare 1, Jump 1, Move 1, Found 1, AggStep 1, SorterNext 1, AggFinal 1, Lt 1, BeginSubrtn 1, DecrJumpZero 1, Copy 1, OpenEphemeral 1, EndCoroutine 1, NewRowid 1, Affinity 1, SCopy 1, IntCopy 1, NoConflict 1, IdxRowid 1, SeekRowid 1, Noop 1, Rowid 1, Add 1, ResetCount 1; log: 130 steps
- **end_branch** (end): Column 49, Null 26, Integer 18, BeginSubrtn 14, OpenRead 14, DecrJumpZero 14, Return 14, String8 14, Once 13, Param 13, SeekRowid 10, Copy 10, Concat 10, Ne 8, IsNull 6, Goto 6, Yield 6, OpenWrite 5, MakeRecord 5, Insert 5, InitCoroutine 5, Noop 4, AggStep 4, AggFinal 4, ResetCount 4, Rewind 4, Next 4, Rowid 3, EndCoroutine 3, NewRowid 3, NotNull 2, SoftNull 2, SeekGE 2, IdxGT 2, Program 2, Last 1, CollSeq 1, Prev 1, SCopy 1, DeferredSeek 1, Lt 1, Add 1, IdxRowid 1, Function:mother 1, OpenEphemeral 1, Close 1, Halt 1; log: 53 steps
- **step_back** (stepq): Column 13, Null 12, Param 9, BeginSubrtn 8, Once 8, Integer 8, OpenRead 8, SeekRowid 8, DecrJumpZero 8, Return 8, SCopy 6, String8 5, Copy 4, Yield 4, MakeRecord 3, NewRowid 3, Insert 3, Concat 3, InitCoroutine 2, EndCoroutine 2, Goto 2, OpenWrite 2, SoftNull 2, ResetCount 2, IsNull 1, OpenEphemeral 1, Rewind 1, Program 1, Next 1, Close 1, NotNull 1, Halt 1; log: 123 steps
- **end_teach** (end): Column 55, Null 24, Integer 18, SCopy 14, OpenRead 10, Copy 10, BeginSubrtn 9, Once 9, Param 9, DecrJumpZero 9, Return 9, Rowid 8, Goto 7, SeekRowid 6, AggStep 6, AggFinal 6, String8 5, OpenWrite 5, Last 5, CollSeq 5, Prev 5, MakeRecord 5, Insert 5, ResetCount 5, Ne 4, Noop 4, NotNull 4, Yield 4, IsNull 3, InitCoroutine 3, Rewind 2, Next 2, Concat 2, EndCoroutine 2, SoftNull 2, NewRowid 2, Program 1, Halt 1
- **end_line** (end): Column 165, Integer 57, Null 40, Ne 35, OpenRead 29, Param 27, BeginSubrtn 26, Return 26, String8 25, DecrJumpZero 24, Once 23, Goto 19, SeekRowid 17, Copy 17, MakeRecord 14, Insert 12, Next 12, Noop 12, Rowid 12, IsNull 12, OpenWrite 11, Rewind 11, Yield 10, ResetCount 10, Prev 9, Last 8, InitCoroutine 7, AggStep 7, AggFinal 7, SCopy 7, NewRowid 6, ZeroOrNull 6, NotNull 6, EndCoroutine 5, IfNot 5, Concat 5, CollSeq 5, OpenEphemeral 4, SoftNull 4, MustBeInt 4, Eq 4, Close 2, IdxInsert 2, Add 2, Function:length 1, Subtract 1, Function:substr 1, Function:trim 1, Program 1, Le 1, If 1, SeekGE 1, IdxGT 1, DeferredSeek 1, Affinity 1, NotFound 1, SeekLT 1; log: 468 steps
- **receipt_gap** (receipt): Integer 13, Column 11, BeginSubrtn 8, Once 8, OpenRead 8, Param 8, DecrJumpZero 8, Return 8, String8 7, Ne 7, Null 6, SeekRowid 6, Rewind 2, Next 2, If 2, OpenWrite 1, SoftNull 1, Concat 1, Copy 1, NewRowid 1, MakeRecord 1, Insert 1, ResetCount 1; log: 36 steps
- **build_go** (BUILD): Param 2, OpenWrite 1, SoftNull 1, NewRowid 1, MakeRecord 1, Insert 1, Program 1, ResetCount 1, Halt 1
- **state_written** (state): ; log: 44 steps
- **proc_status** (proc): Param 2, Eq 1; log: 44 steps

## Every step used above, as SQLite describes it

- **Add**: Add the value in register P1 to the value in register P2 and store the result in register P3. If either input is NULL, the result is NULL.
- **Affinity**: Apply affinities to a range of P2 registers starting with P1. P4 is a string that is P2 characters long. The N-th character of the string indicates the column affinity that should be used for the N-th memory cell in the range.
- **AggFinal**: P1 is the memory location that is the accumulator for an aggregate or window function. Execute the finalizer function for an aggregate and store the result in P1. P2 is the number of arguments that the step function takes and P4 is a pointer to the FuncDef for this function. The P2 argument is not used by this opcode. It is only there to disambiguate functions that can take varying numbers of arguments. The P4 argument is only needed for the case where the step function was not previously called.
- **AggStep**: Execute the xStep function for an aggregate. The function has P5 arguments. P4 is a pointer to the FuncDef structure that specifies the function. Register P3 is the accumulator. The P5 arguments are taken from register P2 and its successors.
- **BeginSubrtn**: Mark the beginning of a subroutine that can be entered in-line or that can be called using Gosub . The subroutine should be terminated by an Return instruction that has a P1 operand that is the same as the P2 operand to this opcode and that has P3 set to 1. If the subroutine is entered in-line, then the Return will simply fall through. But if the subroutine is entered using Gosub , then the Return will jump back to the first instruction after the Gosub . This routine works by loading a NULL into the P2 register. When the return address register contains a NULL, the Return instruction is a no-op that simply falls through to the next instruction (assuming that the Return opcode has a P3 value of 1). Thus if the subroutine is entered in-line, then the Return will cause in-line execution to continue. But if the subroutine is entered via Gosub , then the Return will cause a return to the address following the Gosub . This opcode is identical to Null . It has a different name only to make the byte code easier to read and verify.
- **Blob**: P4 points to a blob of data P1 bytes long. Store this blob in register P2. If P4 is a NULL pointer, then construct a zero-filled blob that is P1 bytes long in P2.
- **Cast**: Force the value in register P1 to be the type defined by P2. P2=='A' → BLOB P2=='B' → TEXT P2=='C' → NUMERIC P2=='D' → INTEGER P2=='E' → REAL A NULL value is not changed by this routine. It remains NULL.
- **Clear**: Delete all contents of the database table or index whose root page in the database file is given by P1. But, unlike Destroy , do not remove the table or index from the database file. The table being cleared is in the main database file if P2==0. If P2==1 then the table to be cleared is in the auxiliary database file that is used to store tables create using CREATE TEMPORARY TABLE. If the P3 value is non-zero, then the row change count is incremented by the number of rows in the table being cleared. If P3 is greater than zero, then the value stored in register P3 is also incremented by the number of rows in the table being cleared. See also: Destroy
- **Close**: Close a cursor previously opened as P1. If P1 is not currently open, this instruction is a no-op.
- **CollSeq**: P4 is a pointer to a CollSeq object. If the next call to a user function or aggregate calls sqlite3GetFuncCollSeq(), this collation sequence will be returned. This is used by the built-in min(), max() and nullif() functions. If P1 is not zero, then it is a register that a subsequent min() or max() aggregate will set to 1 if the current row is not the minimum or maximum. The P1 register is initialized to 0 by this instruction. The interface used by the implementation of the aforementioned functions to retrieve the collation sequence set by this opcode is not available publicly. Only built-in functions have access to this feature.
- **Column**: Interpret the data that cursor P1 points to as a structure built using the MakeRecord instruction. (See the MakeRecord opcode for additional information about the format of the data.) Extract the P2-th column from this record. If there are less than (P2+1) values in the record, extract a NULL. The value extracted is stored in register P3. If the record contains fewer than P2 fields, then extract a NULL. Or, if the P4 argument is a P4_MEM use the value of the P4 argument as the result. If the OPFLAG_LENGTHARG bit is set in P5 then the result is guaranteed to only be used by the length() function or the equivalent. The content of large blobs is not loaded, thus saving CPU cycles. If the OPFLAG_TYPEOFARG bit is set then the result will only be used by the typeof() function or the IS NULL or IS NOT NULL operators or the equivalent. In this case, all content loading can be omitted.
- **Compare**: Compare two vectors of registers in reg(P1)..reg(P1+P3-1) (call this vector "A") and in reg(P2)..reg(P2+P3-1) ("B"). Save the result of the comparison for use by the next Jump instruct. If P5 has the OPFLAG_PERMUTE bit set, then the order of comparison is determined by the most recent Permutation operator. If the OPFLAG_PERMUTE bit is clear, then register are compared in sequential order. P4 is a KeyInfo structure that defines collating sequences and sort orders for the comparison. The permutation applies to registers only. The KeyInfo elements are used sequentially. The comparison is a sort comparison, so NULLs compare equal, NULLs are less than numbers, numbers are less than strings, and strings are less than blobs. This opcode must be immediately followed by an Jump opcode.
- **Concat**: Add the text in register P1 onto the end of the text in register P2 and store the result in register P3. If either the P1 or P2 text are NULL then store NULL in P3. P3 = P2 || P1 It is illegal for P1 and P3 to be the same register. Sometimes, if P3 is the same register as P2, the implementation is able to avoid a memcpy().
- **Copy**: Make a copy of registers P1..P1+P3 into registers P2..P2+P3. If the 0x0002 bit of P5 is set then also clear the MEM_Subtype flag in the destination. The 0x0001 bit of P5 indicates that this Copy opcode cannot be merged. The 0x0001 bit is used by the query planner and does not come into play during query execution. This instruction makes a deep copy of the value. A duplicate is made of any string or blob constant. See also SCopy .
- **CreateBtree**: Allocate a new b-tree in the main database file if P1==0 or in the TEMP database file if P1==1 or in an attached database if P1>1. The P3 argument must be 1 (BTREE_INTKEY) for a rowid table it must be 2 (BTREE_BLOBKEY) for an index or WITHOUT ROWID table. The root page number of the new b-tree is stored in register P2.
- **DecrJumpZero**: Register P1 must hold an integer. Decrement the value in P1 and jump to P2 if the new value is exactly zero.
- **DeferredSeek**: P1 is an open index cursor and P3 is a cursor on the corresponding table. This opcode does a deferred seek of the P3 table cursor to the row that corresponds to the current row of P1. This is a deferred seek. Nothing actually happens until the cursor is used to read a record. That way, if no reads occur, no unnecessary I/O happens. P4 may be an array of integers (type P4_INTARRAY) containing one entry for each column in the P3 table. If array entry a(i) is non-zero, then reading column a(i)-1 from cursor P3 is equivalent to performing the deferred seek and then reading column i from P1. This information is stored in P3 and used to redirect reads against P3 over to P1, thus possibly avoiding the need to seek and read cursor P3.
- **Delete**: Delete the record at which the P1 cursor is currently pointing. If the OPFLAG_SAVEPOSITION bit of the P5 parameter is set, then the cursor will be left pointing at either the next or the previous record in the table. If it is left pointing at the next record, then the next Next instruction will be a no-op. As a result, in this case it is ok to delete a record from within a Next loop. If OPFLAG_SAVEPOSITION bit of P5 is clear, then the cursor will be left in an undefined state. If the OPFLAG_AUXDELETE bit is set on P5, that indicates that this delete is one of several associated with deleting a table row and all its associated index entries. Exactly one of those deletes is the "primary" delete. The others are all on OPFLAG_FORDELETE cursors or else are marked with the AUXDELETE flag. If the OPFLAG_NCHANGE (0x01) flag of P2 (NB: P2 not P5) is set, then the row change count is incremented (otherwise not). If the OPFLAG_ISNOOP (0x40) flag of P2 (not P5!) is set, then the pre-update-hook for deletes is run, but the btree is otherwise unchanged. This happens when the Delete is to be shortly followed by an Insert with the same key, causing the btree entry to be overwritten. P1 must not be pseudo-table. It has to be a real table with multiple rows. If P4 is not NULL then it points to a Table object. In this case either the update or pre-update hook, or both, may be invoked. The P1 cursor must have been positioned using NotFound prior to invoking this opcode in this case. Specifically, if one is configured, the pre-update hook is invoked if P4 is not NULL. The update-hook is invoked if one is configured, P4 is not NULL, and the OPFLAG_NCHANGE flag is set in P2. If the OPFLAG_ISUPDATE flag is set in P2, then P3 contains the address of the memory cell that contains the value that the rowid of the row will be set to by the update.
- **Destroy**: Delete an entire database table or index whose root page in the database file is given by P1. The table being destroyed is in the main database file if P3==0. If P3==1 then the table to be destroyed is in the auxiliary database file that is used to store tables create using CREATE TEMPORARY TABLE. If AUTOVACUUM is enabled then it is possible that another root page might be moved into the newly deleted root page in order to keep all root pages contiguous at the beginning of the database. The former value of the root page that moved - its value before the move occurred - is stored in register P2. If no page movement was required (because the table being dropped was already the last one in the database) then a zero is stored in register P2. If AUTOVACUUM is disabled then a zero is stored in register P2. This opcode throws an error if there are any active reader VMs when it is invoked. This is done to avoid the difficulty associated with updating existing cursors when a root page is moved in an AUTOVACUUM database. This error is thrown even if the database is not an AUTOVACUUM db in order to avoid introducing an incompatibility between autovacuum and non-autovacuum modes. See also: Clear
- **Divide**: Divide the value in register P1 by the value in register P2 and store the result in register P3 (P3=P2/P1). If the value in register P1 is zero, then the result is NULL. If either input is NULL, the result is NULL.
- **DropTable**: Remove the internal (in-memory) data structures that describe the table named P4 in database P1. This is called after a table is dropped from disk (using the Destroy opcode) in order to keep the internal representation of the schema consistent with what is on disk.
- **EndCoroutine**: The instruction at the address in register P1 is a Yield . Jump to the P2 parameter of that Yield . After the jump, the value register P1 is left with a value such that subsequent OP_Yields go back to the this same EndCoroutine instruction. See also: InitCoroutine
- **Eq**: Compare the values in register P1 and P3. If reg(P3)==reg(P1) then jump to address P2. The SQLITE_AFF_MASK portion of P5 must be an affinity character - SQLITE_AFF_TEXT, SQLITE_AFF_INTEGER, and so forth. An attempt is made to coerce both inputs according to this affinity before the comparison is made. If the SQLITE_AFF_MASK is 0x00, then numeric affinity is used. Note that the affinity conversions are stored back into the input registers P1 and P3. So this opcode can cause persistent changes to registers P1 and P3. Once any conversions have taken place, and neither value is NULL, the values are compared. If both values are blobs then memcmp() is used to determine the results of the comparison. If both values are text, then the appropriate collating function specified in P4 is used to do the comparison. If P4 is not specified then memcmp() is used to compare text string. If both values are numeric, then a numeric comparison is used. If the two values are of different types, then numbers are considered less than strings and strings are considered less than blobs. If SQLITE_NULLEQ is set in P5 then the result of comparison is always either true or false and is never NULL. If both operands are NULL then the result of comparison is true. If either operand is NULL then the result is false. If neither operand is NULL the result is the same as it would be if the SQLITE_NULLEQ flag were omitted from P5. This opcode saves the result of comparison for use by the new Jump opcode.
- **Found**: If P4==0 then register P3 holds a blob constructed by MakeRecord . If P4>0 then register P3 is the first of P4 registers that form an unpacked record. Cursor P1 is on an index btree. If the record identified by P3 and P4 is a prefix of any entry in P1 then a jump is made to P2 and P1 is left pointing at the matching entry. This operation leaves the cursor in a state where it can be advanced in the forward direction. The Next instruction will work, but not the Prev instruction. See also: NotFound , NoConflict , NotExists . SeekGe
- **Ge**: This works just like the Lt opcode except that the jump is taken if the content of register P3 is greater than or equal to the content of register P1. See the Lt opcode for additional information.
- **Gosub**: Write the current address onto register P1 and then jump to address P2.
- **Goto**: An unconditional jump to address P2. The next instruction executed will be the one at index P2 from the beginning of the program. The P1 parameter is not actually used by this opcode. However, it is sometimes set to 1 instead of 0 as a hint to the command-line shell that this Goto is the bottom of a loop and that the lines from P2 down to the current line should be indented for EXPLAIN output.
- **Gt**: This works just like the Lt opcode except that the jump is taken if the content of register P3 is greater than the content of register P1. See the Lt opcode for additional information.
- **Halt**: Exit immediately. All open cursors, etc are closed automatically. P1 is the result code returned by sqlite3_exec(), sqlite3_reset(), or sqlite3_finalize(). For a normal halt, this should be SQLITE_OK (0). For errors, it can be some other value. If P1!=0 then P2 will determine whether or not to rollback the current transaction. Do not rollback if P2==OE_Fail. Do the rollback if P2==OE_Rollback. If P2==OE_Abort, then back out all changes that have occurred during this execution of the VDBE, but do not rollback the transaction. If P3 is not zero and P4 is NULL, then P3 is a register that holds the text of an error message. If P3 is zero and P4 is not null then the error message string is held in P4. P5 is a value between 1 and 4, inclusive, then the P4 error message string is modified as follows: 1: NOT NULL constraint failed: P4 2: UNIQUE constraint failed: P4 3: CHECK constraint failed: P4 4: FOREIGN KEY constraint failed: P4 If P3 is zero and P5 is not zero and P4 is NULL, then everything after the ":" is omitted. There is an implied " Halt 0 0 0" instruction inserted at the very end of every program. So a jump past the last instruction of the program is the same as executing Halt .
- **IdxDelete**: The content of P5 registers starting at register P2 form an unpacked index key. This opcode removes that entry from the index opened by cursor P1. P4 is a pointer to an Index structure. If P3 is non-zero, it is the register number of a register holding a record that will be inserted into this index. If that record is identical to the one that would be deleted by this instruction, skip the delete and set register P3 to NULL. Raise an SQLITE_CORRUPT_INDEX error if no matching index entry is found and not in writable_schema mode.
- **IdxGT**: The P4 register values beginning with P3 form an unpacked index key that omits the PRIMARY KEY. Compare this key value against the index that P1 is currently pointing to, ignoring the PRIMARY KEY or ROWID fields at the end. If the P1 index entry is greater than the key value then jump to P2. Otherwise fall through to the next instruction.
- **IdxInsert**: Register P2 holds an SQL index key made using the MakeRecord instructions. This opcode writes that key into the index P1. Data for the entry is nil. If P4 is not zero, then it is the number of values in the unpacked key of reg(P2). In that case, P3 is the index of the first register for the unpacked key. The availability of the unpacked key can sometimes be an optimization. If P5 has the OPFLAG_APPEND bit set, that is a hint to the b-tree layer that this insert is likely to be an append. If P5 has the OPFLAG_NCHANGE bit set, then the change counter is incremented by this instruction. If the OPFLAG_NCHANGE bit is clear, then the change counter is unchanged. If the OPFLAG_USESEEKRESULT flag of P5 is set, the implementation might run faster by avoiding an unnecessary seek on cursor P1. However, the OPFLAG_USESEEKRESULT flag must only be set if there have been no prior seeks on the cursor or if the most recent seek used a key equivalent to P2. This instruction only works for indices. The equivalent instruction for tables is Insert .
- **IdxRowid**: Write into register P2 an integer which is the last entry in the record at the end of the index key pointed to by cursor P1. This integer should be the rowid of the table entry to which this index entry points. See also: Rowid , MakeRecord .
- **If**: Jump to P2 if the value in register P1 is true. The value is considered true if it is numeric and non-zero. If the value in P1 is NULL then take the jump if and only if P3 is non-zero.
- **IfNot**: Jump to P2 if the value in register P1 is False. The value is considered false if it has a numeric value of zero. If the value in P1 is NULL then take the jump if and only if P3 is non-zero.
- **IfPos**: Register P1 must contain an integer. If the value of register P1 is 1 or greater, subtract P3 from the value in P1 and jump to P2. If the initial value of register P1 is less than 1, then the value is unchanged and control passes through to the next instruction.
- **Init**: Programs contain a single instance of this opcode as the very first opcode. If tracing is enabled (by the sqlite3_trace()) interface, then the UTF-8 string contained in P4 is emitted on the trace callback. Or if P4 is blank, use the string returned by sqlite3_sql(). If P2 is not zero, jump to instruction P2. Increment the value of P1 so that Once opcodes will jump the first time they are evaluated for this run. If P3 is not zero, then it is an address to jump to if an SQLITE_CORRUPT error is encountered.
- **InitCoroutine**: Set up register P1 so that it will Yield to the coroutine located at address P3. If P2!=0 then the coroutine implementation immediately follows this opcode. So jump over the coroutine implementation to address P2. See also: EndCoroutine
- **Insert**: Write an entry into the table of cursor P1. A new entry is created if it doesn't already exist or the data for an existing entry is overwritten. The data is the value MEM_Blob stored in register number P2. The key is stored in register P3. The key must be a MEM_Int. If the OPFLAG_NCHANGE flag of P5 is set, then the row change count is incremented (otherwise not). If the OPFLAG_LASTROWID flag of P5 is set, then rowid is stored for subsequent return by the sqlite3_last_insert_rowid() function (otherwise it is unmodified). If the OPFLAG_USESEEKRESULT flag of P5 is set, the implementation might run faster by avoiding an unnecessary seek on cursor P1. However, the OPFLAG_USESEEKRESULT flag must only be set if there have been no prior seeks on the cursor or if the most recent seek used a key equal to P3. If the OPFLAG_ISUPDATE flag is set, then this opcode is part of an UPDATE operation. Otherwise (if the flag is clear) then this opcode is part of an INSERT operation. The difference is only important to the update hook. Parameter P4 may point to a Table structure, or may be NULL. If it is not NULL, then the update-hook (sqlite3.xUpdateCallback) is invoked following a successful insert. (WARNING/TODO: If P1 is a pseudo-cursor and P2 is dynamically allocated, then ownership of P2 is transferred to the pseudo-cursor and register P2 becomes ephemeral. If the cursor is changed, the value of register P2 will then change. Make sure this does not cause any problems.) This instruction only works on tables. The equivalent instruction for indices is IdxInsert .
- **IntCopy**: Transfer the integer value held in register P1 into register P2. This is an optimized version of SCopy that works only for integer values.
- **Integer**: The 32-bit integer value P1 is written into register P2.
- **IsNull**: Jump to P2 if the value in register P1 is NULL.
- **Jump**: Jump to the instruction at address P1, P2, or P3 depending on whether in the most recent Compare instruction the P1 vector was less than, equal to, or greater than the P2 vector, respectively. This opcode must immediately follow an Compare opcode.
- **Last**: The next use of the Rowid or Column or Prev instruction for P1 will refer to the last entry in the database table or index. If the table or index is empty and P2>0, then jump immediately to P2. If P2 is 0 or if the table or index is not empty, fall through to the following instruction. This opcode leaves the cursor configured to move in reverse order, from the end toward the beginning. In other words, the cursor is configured to use Prev , not Next .
- **Le**: This works just like the Lt opcode except that the jump is taken if the content of register P3 is less than or equal to the content of register P1. See the Lt opcode for additional information.
- **Lt**: Compare the values in register P1 and P3. If reg(P3)<reg(P1) then jump to address P2. If the SQLITE_JUMPIFNULL bit of P5 is set and either reg(P1) or reg(P3) is NULL then the take the jump. If the SQLITE_JUMPIFNULL bit is clear then fall through if either operand is NULL. The SQLITE_AFF_MASK portion of P5 must be an affinity character - SQLITE_AFF_TEXT, SQLITE_AFF_INTEGER, and so forth. An attempt is made to coerce both inputs according to this affinity before the comparison is made. If the SQLITE_AFF_MASK is 0x00, then numeric affinity is used. Note that the affinity conversions are stored back into the input registers P1 and P3. So this opcode can cause persistent changes to registers P1 and P3. Once any conversions have taken place, and neither value is NULL, the values are compared. If both values are blobs then memcmp() is used to determine the results of the comparison. If both values are text, then the appropriate collating function specified in P4 is used to do the comparison. If P4 is not specified then memcmp() is used to compare text string. If both values are numeric, then a numeric comparison is used. If the two values are of different types, then numbers are considered less than strings and strings are considered less than blobs. This opcode saves the result of comparison for use by the new Jump opcode.
- **MakeRecord**: Convert P2 registers beginning with P1 into the record format use as a data record in a database table or as a key in an index. The Column opcode can decode the record later. P4 may be a string that is P2 characters long. The N-th character of the string indicates the column affinity that should be used for the N-th field of the index key. The mapping from character to affinity is given by the SQLITE_AFF_ macros defined in sqliteInt.h. If P4 is NULL then all index fields have the affinity BLOB. The meaning of P5 depends on whether or not the SQLITE_ENABLE_NULL_TRIM compile-time option is enabled: * If SQLITE_ENABLE_NULL_TRIM is enabled, then the P5 is the index of the right-most table that can be null-trimmed. * If SQLITE_ENABLE_NULL_TRIM is omitted, then P5 has the value OPFLAG_NOCHNG_MAGIC if the MakeRecord opcode is allowed to accept no-change records with serial_type 10. This value is only used inside an assert() and does not affect the end result.
- **Move**: Move the P3 values in register P1..P1+P3-1 over into registers P2..P2+P3-1. Registers P1..P1+P3-1 are left holding a NULL. It is an error for register ranges P1..P1+P3-1 and P2..P2+P3-1 to overlap. It is an error for P3 to be less than 1.
- **Multiply**: Multiply the value in register P1 by the value in register P2 and store the result in register P3. If either input is NULL, the result is NULL.
- **MustBeInt**: Force the value in register P1 to be an integer. If the value in P1 is not an integer and cannot be converted into an integer without data loss, then jump immediately to P2, or if P2==0 raise an SQLITE_MISMATCH exception.
- **Ne**: This works just like the Eq opcode except that the jump is taken if the operands in registers P1 and P3 are not equal. See the Eq opcode for additional information.
- **NewRowid**: Get a new integer record number (a.k.a "rowid") used as the key to a table. The record number is not previously used as a key in the database table that cursor P1 points to. The new record number is written written to register P2. If P3>0 then P3 is a register in the root frame of this VDBE that holds the largest previously generated record number. No new record numbers are allowed to be less than this value. When this value reaches its maximum, an SQLITE_FULL error is generated. The P3 register is updated with the ' generated record number. This P3 mechanism is used to help implement the AUTOINCREMENT feature.
- **Next**: Advance cursor P1 so that it points to the next key/data pair in its table or index. If there are no more key/value pairs then fall through to the following instruction. But if the cursor advance was successful, jump immediately to P2. The Next opcode is only valid following an SeekGT , SeekGE , or Rewind opcode used to position the cursor. Next is not allowed to follow SeekLT , SeekLE , or Last . The P1 cursor must be for a real table, not a pseudo-table. P1 must have been opened prior to this opcode or the program will segfault. The P3 value is a hint to the btree implementation. If P3==1, that means P1 is an SQL index and that this instruction could have been omitted if that index had been unique. P3 is usually 0. P3 is always either 0 or 1. If P5 is positive and the jump is taken, then event counter number P5-1 in the prepared statement is incremented. See also: Prev
- **NoConflict**: If P4==0 then register P3 holds a blob constructed by MakeRecord . If P4>0 then register P3 is the first of P4 registers that form an unpacked record. Cursor P1 is on an index btree. If the record identified by P3 and P4 contains any NULL value, jump immediately to P2. If all terms of the record are not-NULL then a check is done to determine if any row in the P1 index btree has a matching key prefix. If there are no matches, jump immediately to P2. If there is a match, fall through and leave the P1 cursor pointing to the matching row. This opcode is similar to NotFound with the exceptions that the branch is always taken if any part of the search key input is NULL. This operation leaves the cursor in a state where it cannot be advanced in either direction. In other words, the Next and Prev opcodes do not work after this operation. See also: NotFound , Found , NotExists
- **Noop**: Do nothing. Continue downward to the next opcode.
- **NotExists**: P1 is the index of a cursor open on an SQL table btree (with integer keys). P3 is an integer rowid. If P1 does not contain a record with rowid P3 then jump immediately to P2. Or, if P2 is 0, raise an SQLITE_CORRUPT error. If P1 does contain a record with rowid P3 then leave the cursor pointing at that record and fall through to the next instruction. The SeekRowid opcode performs the same operation but also allows the P3 register to contain a non-integer value, in which case the jump is always taken. This opcode requires that P3 always contain an integer. The NotFound opcode performs the same operation on index btrees (with arbitrary multi-value keys). This opcode leaves the cursor in a state where it cannot be advanced in either direction. In other words, the Next and Prev opcodes will not work following this opcode. See also: Found , NotFound , NoConflict , SeekRowid
- **NotFound**: If P4==0 then register P3 holds a blob constructed by MakeRecord . If P4>0 then register P3 is the first of P4 registers that form an unpacked record. Cursor P1 is on an index btree. If the record identified by P3 and P4 is not the prefix of any entry in P1 then a jump is made to P2. If P1 does contain an entry whose prefix matches the P3/P4 record then control falls through to the next instruction and P1 is left pointing at the matching entry. This operation leaves the cursor in a state where it cannot be advanced in either direction. In other words, the Next and Prev opcodes do not work after this operation. See also: Found , NotExists , NoConflict , IfNoHope
- **NotNull**: Jump to P2 if the value in register P1 is not NULL.
- **Null**: Write a NULL into registers P2. If P3 greater than P2, then also write NULL into register P3 and every register in between P2 and P3. If P3 is less than P2 (typically P3 is zero) then only register P2 is set to NULL. If the P1 value is non-zero, then also set the MEM_Cleared flag so that NULL values will not compare equal even if SQLITE_NULLEQ is set on Ne or Eq .
- **Once**: Fall through to the next instruction the first time this opcode is encountered on each invocation of the byte-code program. Jump to P2 on the second and all subsequent encounters during the same invocation. Top-level programs determine first invocation by comparing the P1 operand against the P1 operand on the Init opcode at the beginning of the program. If the P1 values differ, then fall through and make the P1 of this opcode equal to the P1 of Init . If P1 values are the same then take the jump. For subprograms, there is a bitmask in the VdbeFrame that determines whether or not the jump should be taken. The bitmask is necessary because the self-altering code trick does not work for recursive triggers. The P3 operand is not used directly by this opcode. However P3 is used by the code generator as follows: If this opcode is the start of a subroutine and that subroutine uses a Bloom filter, then P3 will be the register that holds that Bloom filter. See tag-202407032019 in the source code for implementation details.
- **OpenEphemeral**: Open a new cursor P1 to a transient table. The cursor is always opened read/write even if the main database is read-only. The ephemeral table is deleted automatically when the cursor is closed. If the cursor P1 is already opened on an ephemeral table, the table is cleared (all content is erased). P2 is the number of columns in the ephemeral table. The cursor points to a BTree table if P4==0 and to a BTree index if P4 is not 0. If P4 is not NULL, it points to a KeyInfo structure that defines the format of keys in the index. The P5 parameter can be a mask of the BTREE_* flags defined in btree.h. These flags control aspects of the operation of the btree. The BTREE_OMIT_JOURNAL and BTREE_SINGLE flags are added automatically. If P3 is positive, then reg[P3] is modified slightly so that it can be used as zero-length data for Insert . This is an optimization that avoids an extra Blob opcode to initialize that register.
- **OpenPseudo**: Open a new cursor that points to a fake table that contains a single row of data. The content of that one row is the content of memory register P2. In other words, cursor P1 becomes an alias for the MEM_Blob content contained in register P2. A pseudo-table created by this opcode is used to hold a single row output from the sorter so that the row can be decomposed into individual columns using the Column opcode. The Column opcode is the only cursor opcode that works with a pseudo-table. P3 is the number of fields in the records that will be stored by the pseudo-table. If P2 is 0 or negative then the pseudo-cursor will return NULL for every column.
- **OpenRead**: Open a read-only cursor for the database table whose root page is P2 in a database file. The database file is determined by P3. P3==0 means the main database, P3==1 means the database used for temporary tables, and P3>1 means used the corresponding attached database. Give the new cursor an identifier of P1. The P1 values need not be contiguous but all P1 values should be small integers. It is an error for P1 to be negative. Allowed P5 bits: 0x02 OPFLAG_SEEKEQ : This cursor will only be used for equality lookups (implemented as a pair of opcodes SeekGE / IdxGT of SeekLE / IdxLT ) The P4 value may be either an integer (P4_INT32) or a pointer to a KeyInfo structure (P4_KEYINFO). If it is a pointer to a KeyInfo object, then table being opened must be an index b-tree where the KeyInfo object defines the content and collating sequence of that index b-tree. Otherwise, if P4 is an integer value, then the table being opened must be a table b-tree with a number of columns no less than the value of P4. See also: OpenWrite , ReopenIdx
- **OpenWrite**: Open a read/write cursor named P1 on the table or index whose root page is P2 (or whose root page is held in register P2 if the OPFLAG_P2ISREG bit is set in P5 - see below). The P4 value may be either an integer (P4_INT32) or a pointer to a KeyInfo structure (P4_KEYINFO). If it is a pointer to a KeyInfo object, then table being opened must be an index b-tree where the KeyInfo object defines the content and collating sequence of that index b-tree. Otherwise, if P4 is an integer value, then the table being opened must be a table b-tree with a number of columns no less than the value of P4. Allowed P5 bits: 0x02 OPFLAG_SEEKEQ : This cursor will only be used for equality lookups (implemented as a pair of opcodes SeekGE / IdxGT of SeekLE / IdxLT ) 0x08 OPFLAG_FORDELETE : This cursor is used only to seek and subsequently delete entries in an index btree. This is a hint to the storage engine that the storage engine is allowed to ignore. The hint is not used by the official SQLite b*tree storage engine, but is used by COMDB2. 0x10 OPFLAG_P2ISREG : Use the content of register P2 as the root page, not the value of P2 itself. This instruction works like OpenRead except that it opens the cursor in read/write mode. See also: OpenRead , ReopenIdx
- **Param**: This opcode is only ever present in sub-programs called via the Program instruction. Copy a value currently stored in a memory cell of the calling (parent) frame to cell P2 in the current frames address space. This is used by trigger programs to access the new.* and old.* values. The address of the cell in the parent frame is determined by adding the value of the P1 argument to the value of the P1 argument to the calling Program instruction.
- **ParseSchema**: Read and parse all entries from the schema table of database P1 that match the WHERE clause P4. If P4 is a NULL pointer, then the entire schema for P1 is reparsed. When P4 is NULL, the P5 value is used as the mFlags argument to sqlite3InitOne(). In other words, P5 should be a mask composed of INITFLAG_* values. The P4==0 case is only used by ALTER TABLE and P5!=0 for all such cases. For uses other than ALTER TABLE, P4<>0 and P5==0. This opcode invokes the parser to create a new virtual machine, then runs the new virtual machine. It is thus a re-entrant opcode.
- **Prev**: Back up cursor P1 so that it points to the previous key/data pair in its table or index. If there is no previous key/value pairs then fall through to the following instruction. But if the cursor backup was successful, jump immediately to P2. The Prev opcode is only valid following an SeekLT , SeekLE , or Last opcode used to position the cursor. Prev is not allowed to follow SeekGT , SeekGE , or Rewind . The P1 cursor must be for a real table, not a pseudo-table. If P1 is not open then the behavior is undefined. The P3 value is a hint to the btree implementation. If P3==1, that means P1 is an SQL index and that this instruction could have been omitted if that index had been unique. P3 is usually 0. P3 is always either 0 or 1. If P5 is positive and the jump is taken, then event counter number P5-1 in the prepared statement is incremented.
- **Program**: Execute the trigger program passed as P4 (type P4_SUBPROGRAM). P1 contains the address of the memory cell that contains the first memory cell in an array of values used as arguments to the sub-program. P2 contains the address to jump to if the sub-program throws an IGNORE exception using the RAISE() function. P2 might be zero, if there is no possibility that an IGNORE exception will be raised. Register P3 contains the address of a memory cell in this (the parent) VM that is used to allocate the memory required by the sub-vdbe at runtime. P4 is a pointer to the VM containing the trigger program. If P5 is non-zero, then recursive program invocation is enabled.
- **ReadCookie**: Read cookie number P3 from database P1 and write it into register P2. P3==1 is the schema version. P3==2 is the database format. P3==3 is the recommended pager cache size, and so forth. P1==0 is the main database file and P1==1 is the database file used to store temporary tables. There must be a read-lock on the database (either a transaction must be started or there must be an open cursor) before executing this instruction.
- **RealAffinity**: If register P1 holds an integer convert it to a real value. This opcode is used when extracting information from a column that has REAL affinity. Such column values may still be stored as integers, for space efficiency, but after extraction we want them to have only a real value.
- **ResetCount**: The value of the change counter is copied to the database handle change counter (returned by subsequent calls to sqlite3_changes()). Then the VMs internal change counter resets to 0. This is used by trigger programs.
- **ResultRow**: The registers P1 through P1+P2-1 contain a single row of results. This opcode causes the sqlite3_step() call to terminate with an SQLITE_ROW return code and it sets up the sqlite3_stmt structure to provide access to the r(P1)..r(P1+P2-1) values as the result row.
- **Return**: Jump to the address stored in register P1. If P1 is a return address register, then this accomplishes a return from a subroutine. If P3 is 1, then the jump is only taken if register P1 holds an integer values, otherwise execution falls through to the next opcode, and the Return becomes a no-op. If P3 is 0, then register P1 must hold an integer or else an assert() is raised. P3 should be set to 1 when this opcode is used in combination with BeginSubrtn , and set to 0 otherwise. The value in register P1 is unchanged by this opcode. P2 is not used by the byte-code engine. However, if P2 is positive and also less than the current address, then the "EXPLAIN" output formatter in the CLI will indent all opcodes from the P2 opcode up to be not including the current Return . P2 should be the first opcode in the subroutine from which this opcode is returning. Thus the P2 value is a byte-code indentation hint. See tag-20220407a in wherecode.c and shell.c.
- **Rewind**: The next use of the Rowid or Column or Next instruction for P1 will refer to the first entry in the database table or index. If the table or index is empty, jump immediately to P2. If the table or index is not empty, fall through to the following instruction. If P2 is zero, that is an assertion that the P1 table is never empty and hence the jump will never be taken. This opcode leaves the cursor configured to move in forward order, from the beginning toward the end. In other words, the cursor is configured to use Next , not Prev .
- **Rowid**: Store in register P2 an integer which is the key of the table entry that P1 is currently point to. P1 can be either an ordinary table or a virtual table. There used to be a separate OP_VRowid opcode for use with virtual tables, but this one opcode now works for both table types.
- **SCopy**: Make a shallow copy of register P1 into register P2. This instruction makes a shallow copy of the value. If the value is a string or blob, then the copy is only a pointer to the original and hence if the original changes so will the copy. Worse, if the original is deallocated, the copy becomes invalid. Thus the program must guarantee that the original will not change during the lifetime of the copy. Use Copy to make a complete copy.
- **SeekGE**: If cursor P1 refers to an SQL table (B-Tree that uses integer keys), use the value in register P3 as the key. If cursor P1 refers to an SQL index, then P3 is the first in an array of P4 registers that are used as an unpacked index key. Reposition cursor P1 so that it points to the smallest entry that is greater than or equal to the key value. If there are no records greater than or equal to the key and P2 is not zero, then jump to P2. If the cursor P1 was opened using the OPFLAG_SEEKEQ flag, then this opcode will either land on a record that exactly matches the key, or else it will cause a jump to P2. When the cursor is OPFLAG_SEEKEQ, this opcode must be followed by an IdxLE opcode with the same arguments. The IdxGT opcode will be skipped if this opcode succeeds, but the IdxGT opcode will be used on subsequent loop iterations. The OPFLAG_SEEKEQ flags is a hint to the btree layer to say that this is an equality search. This opcode leaves the cursor configured to move in forward order, from the beginning toward the end. In other words, the cursor is configured to use Next , not Prev . See also: Found , NotFound , SeekLt, SeekGt, SeekLe
- **SeekGT**: If cursor P1 refers to an SQL table (B-Tree that uses integer keys), use the value in register P3 as a key. If cursor P1 refers to an SQL index, then P3 is the first in an array of P4 registers that are used as an unpacked index key. Reposition cursor P1 so that it points to the smallest entry that is greater than the key value. If there are no records greater than the key and P2 is not zero, then jump to P2. This opcode leaves the cursor configured to move in forward order, from the beginning toward the end. In other words, the cursor is configured to use Next , not Prev . See also: Found , NotFound , SeekLt, SeekGe, SeekLe
- **SeekLT**: If cursor P1 refers to an SQL table (B-Tree that uses integer keys), use the value in register P3 as a key. If cursor P1 refers to an SQL index, then P3 is the first in an array of P4 registers that are used as an unpacked index key. Reposition cursor P1 so that it points to the largest entry that is less than the key value. If there are no records less than the key and P2 is not zero, then jump to P2. This opcode leaves the cursor configured to move in reverse order, from the end toward the beginning. In other words, the cursor is configured to use Prev , not Next . See also: Found , NotFound , SeekGt, SeekGe, SeekLe
- **SeekRowid**: P1 is the index of a cursor open on an SQL table btree (with integer keys). If register P3 does not contain an integer or if P1 does not contain a record with rowid P3 then jump immediately to P2. Or, if P2 is 0, raise an SQLITE_CORRUPT error. If P1 does contain a record with rowid P3 then leave the cursor pointing at that record and fall through to the next instruction. The NotExists opcode performs the same operation, but with NotExists the P3 register must be guaranteed to contain an integer value. With this opcode, register P3 might not contain an integer. The NotFound opcode performs the same operation on index btrees (with arbitrary multi-value keys). This opcode leaves the cursor in a state where it cannot be advanced in either direction. In other words, the Next and Prev opcodes will not work following this opcode. See also: Found , NotFound , NoConflict , SeekRowid
- **SetCookie**: Write the integer value P3 into cookie number P2 of database P1. P2==1 is the schema version. P2==2 is the database format. P2==3 is the recommended pager cache size, and so forth. P1==0 is the main database file and P1==1 is the database file used to store temporary tables. A transaction must be started before executing this opcode. If P2 is the SCHEMA_VERSION cookie (cookie number 1) then the internal schema version is set to P3-P5. The "PRAGMA schema_version=N" statement has P5 set to 1, so that the internal schema version will be different from the database schema version, resulting in a schema reset.
- **SoftNull**: Set register P1 to have the value NULL as seen by the MakeRecord instruction, but do not free any string or blob memory associated with the register, so that if the value was a string or blob that was previously copied using SCopy , the copies will continue to be valid.
- **SorterData**: Write into register P2 the current sorter data for sorter cursor P1. Then clear the column header cache on cursor P3. This opcode is normally used to move a record out of the sorter and into a register that is the source for a pseudo-table cursor created using OpenPseudo . That pseudo-table cursor is the one that is identified by parameter P3. Clearing the P3 column cache as part of this opcode saves us from having to issue a separate NullRow instruction to clear that cache.
- **SorterInsert**: Register P2 holds an SQL index key made using the MakeRecord instructions. This opcode writes that key into the sorter P1. Data for the entry is nil.
- **SorterNext**: This opcode works just like Next except that P1 must be a sorter object for which the SorterSort opcode has been invoked. This opcode advances the cursor to the next sorted record, or jumps to P2 if there are no more sorted records.
- **SorterOpen**: This opcode works like OpenEphemeral except that it opens a transient index that is specifically designed to sort large tables using an external merge-sort algorithm. If argument P3 is non-zero, then it indicates that the sorter may assume that a stable sort considering the first P3 fields of each key is sufficient to produce the required results.
- **SorterSort**: After all records have been inserted into the Sorter object identified by P1, invoke this opcode to actually do the sorting. Jump to P2 if there are no records to be sorted. This opcode is an alias for Sort and Rewind that is used for Sorter objects.
- **String8**: P4 points to a nul terminated UTF-8 string. This opcode is transformed into a String opcode before it is executed for the first time. During this transformation, the length of string P4 is computed and stored as the P1 parameter.
- **Subtract**: Subtract the value in register P1 from the value in register P2 and store the result in register P3. If either input is NULL, the result is NULL.
- **Transaction**: Begin a transaction on database P1 if a transaction is not already active. If P2 is non-zero, then a write-transaction is started, or if a read-transaction is already active, it is upgraded to a write-transaction. If P2 is zero, then a read-transaction is started. If P2 is 2 or more then an exclusive transaction is started. P1 is the index of the database file on which the transaction is started. Index 0 is the main database file and index 1 is the file used for temporary tables. Indices of 2 or more are used for attached databases. If a write-transaction is started and the Vdbe.usesStmtJournal flag is true (this flag is set if the Vdbe may modify more than one row and may throw an ABORT exception), a statement transaction may also be opened. More specifically, a statement transaction is opened iff the database connection is currently not in autocommit mode, or if there are other active statements. A statement transaction allows the changes made by this VDBE to be rolled back after an error without having to roll back the entire transaction. If no error is encountered, the statement transaction will automatically commit when the VDBE halts. If P5!=0 then this opcode also checks the schema cookie against P3 and the schema generation counter against P4. The cookie changes its value whenever the database schema changes. This operation is used to detect when that the cookie has changed and that the current process needs to reread the schema. If the schema cookie in P3 differs from the schema cookie in the database header or if the schema generation counter in P4 differs from the current generation counter, then an SQLITE_SCHEMA error is raised and execution halts. The sqlite3_step() wrapper function might then reprepare the statement and rerun it from the beginning.
- **Yield**: Swap the program counter with the value in register P1. This has the effect of yielding to a coroutine. If the coroutine that is launched by this instruction ends with Yield or Return then continue to the next instruction. But if the coroutine launched by this instruction ends with EndCoroutine , then jump to P2 rather than continuing with the next instruction. See also: InitCoroutine
- **ZeroOrNull**: If both registers P1 and P3 are NOT NULL, then store a zero in register P2. If either registers P1 or P3 are NULL then put a NULL in register P2.
- **Function**: Invoke a user function (P4 is a pointer to an sqlite3_context object that contains a pointer to the function to be run) with arguments taken from register P2 and successors. The number of arguments is in the sqlite3_context object that P4 points to. The result of the function is stored in register P3. Register P3 must not be one of the function inputs. P1 is a 32-bit bitmask indicating whether or not each argument to the function was determined to be constant at compile time. If the first argument was constant then bit 0 of P1 is set. This is used to determine whether meta data associated with a user function argument using the sqlite3_set_auxdata() API may be safely retained until the next invocation of this opcode. See also: AggStep , AggFinal , PureFunc
