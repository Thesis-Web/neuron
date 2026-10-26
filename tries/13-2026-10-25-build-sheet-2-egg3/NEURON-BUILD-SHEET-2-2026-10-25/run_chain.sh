#!/bin/bash
# run_chain.sh: lays a fresh egg and types the sheet's lines in order, logging each line and what came back.
cd "$(dirname "$0")"
SRC="sources/wn.db sources/gcide.db sources/mw.db sources/mwt.db sources/moby.db sources/map.db sources/sqldoc.db"
rm -f brain.db
sqlite3 brain.db ".load ./mother" ".read egg.sql"
q() { sqlite3 brain.db "$1"; }
say() { echo; echo "### $1"; }
typeit() { echo "> $1"; printf '%s\n' "$1" | python3 bottom.py brain.db $SRC 2>/dev/null | grep -v '^> *$' | sed 's/^> //'; }
say "egg laid"; q "SELECT type, count(*) FROM sqlite_master GROUP BY type; SELECT count(*) FROM encoder; SELECT n FROM shards;"
say "S1 dog (nothing bound yet)"; typeit "dog"; q "SELECT run, (SELECT word FROM encoder WHERE gate = name) AS cell, value FROM sheet; SELECT count(*) AS receipts FROM receipt;"
say "S2 the born run, typed once"; typeit "$(cat BORN-RUN.txt)"; q "SELECT max(id) AS born_run_id FROM input WHERE parent IS NULL;"
say "S3 bind the born run to born's memory node (16)"; typeit 'BUILD INSERT INTO "16" ( run ) VALUES ( 2 ) ; BUILD'
say "S4 dog"; typeit "dog"; DG=$(q "SELECT gate FROM encoder WHERE word='dog'"); q "SELECT gate, word FROM encoder WHERE word LIKE 'dog%'; SELECT type, name FROM sqlite_master WHERE name IN ('$DG','$((DG+1))','$((DG+2))','$((DG+3))'); SELECT shard, arrival, remainder, trigger FROM \"$((DG+1))\";"
say "S5 cat"; typeit "cat"
say "S6 BUILD CREATE TABLE things ( a ) ; BUILD"; typeit 'BUILD CREATE TABLE things ( a ) ; BUILD'; q "SELECT name FROM sqlite_master WHERE name = 'things';"
say "S7 the timeline table, through BUILD"; typeit 'BUILD CREATE TABLE timeline ( id INTEGER PRIMARY KEY , run INTEGER , clock DEFAULT CURRENT_TIMESTAMP ) ; BUILD'
END_RUN="BUILD INSERT INTO sheet ( run , name , value ) SELECT var run , ( SELECT gate FROM encoder WHERE word = 'mem' ) , gate FROM encoder WHERE word = ( SELECT word FROM encoder WHERE gate = var gate ) || '.memory' ; BUILD BUILD INSERT INTO \"var mem\" ( run , shard ) VALUES ( var run , var shard ) ; BUILD BUILD INSERT INTO timeline ( run ) VALUES ( var run ) ; BUILD"
say "S8 the end run (memory + timeline), typed once"; typeit "$END_RUN"; ER=$(q "SELECT max(id) FROM input WHERE parent IS NULL"); echo "end run id = $ER"
say "S9 bind the end run to end's memory node (24)"; typeit "BUILD INSERT INTO \"24\" ( run ) VALUES ( $ER ) ; BUILD"
say "S10 cat (now a memory and a timeline row are written when the line ends)"; typeit "cat"; CG=$(q "SELECT gate FROM encoder WHERE word='cat'"); q "SELECT 'cat.memory rows (id|run|shard):'; SELECT * FROM \"$((CG+3))\"; SELECT 'timeline:'; SELECT * FROM timeline; SELECT 'cat dna:'; SELECT * FROM \"$((CG+1))\";"
say "S11 define dog (define is born; nothing else)"; typeit "define dog"; DF=$(q "SELECT gate FROM encoder WHERE word='define'"); echo "define gate = $DF, define.dna = $((DF+1)), define.memory = $((DF+3))"
DEFINE_RUN="BUILD INSERT INTO born ( run , gate ) SELECT var run , CAST ( var rest AS INTEGER ) WHERE NOT EXISTS ( SELECT 1 FROM sqlite_master WHERE type = 'view' AND name = CAST ( var rest AS INTEGER ) ) ; BUILD BUILD INSERT INTO sheet ( run , name , value ) SELECT var run , ( SELECT gate FROM encoder WHERE word = 'def' ) , gate FROM encoder WHERE word = ( SELECT word FROM encoder WHERE gate = CAST ( var rest AS INTEGER ) ) || '.definition' ; BUILD BUILD INSERT INTO wn . inbox ( run , word ) SELECT var run , word FROM encoder WHERE gate = CAST ( var rest AS INTEGER ) ; BUILD BUILD INSERT INTO \"var def\" ( run ) SELECT id FROM input WHERE parent = var run AND arrival = ( SELECT gate FROM encoder WHERE word = 'wn' ) ; BUILD"
say "S12 the define run, typed once"; typeit "$DEFINE_RUN"; DR=$(q "SELECT max(id) FROM input WHERE parent IS NULL"); echo "define run id = $DR"
say "S13 bind the define run to define's memory node"; typeit "BUILD INSERT INTO \"$((DF+3))\" ( run ) VALUES ( $DR ) ; BUILD"
say "S14 write the dna: define's row (heard, space) fires define"; typeit "BUILD UPDATE \"$((DF+1))\" SET trigger = $DF WHERE arrival = 1 AND remainder = 77 ; BUILD"; q "SELECT * FROM \"$((DF+1))\";"
say "S15 define dog"; typeit "define dog"; q "SELECT 'dog.definition rows (id|run):'; SELECT * FROM \"$((DG+2))\";"
say "S16 define bird (a word the brain has no neuron for yet)"; typeit "define bird"; BG=$(q "SELECT gate FROM encoder WHERE word='bird'"); q "SELECT 'bird objects:'; SELECT type, name FROM sqlite_master WHERE name IN ('$BG','$((BG+1))','$((BG+2))','$((BG+3))'); SELECT 'bird.definition rows:'; SELECT * FROM \"$((BG+2))\";"
say "S16b define bird again (everything in memory now: no births, no asking twice?)"; typeit "define bird"; q "SELECT 'bird.definition rows:'; SELECT * FROM \"$((BG+2))\";"
say "S17 BUILD DROP TABLE things ; BUILD"; typeit 'BUILD DROP TABLE things ; BUILD'; q "SELECT 'things still there:', count(*) FROM sqlite_master WHERE name='things';"
say "S18 shards: one sequence?"; q "SELECT n FROM shards;"; python3 - <<'PY'
import sqlite3
db = sqlite3.connect('brain.db')
dna = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND sql LIKE '%( shard INTEGER PRIMARY KEY%'")]
shards = []
for t in dna: shards += [r[0] for r in db.execute(f'SELECT shard FROM "{t}"')]
n = db.execute('SELECT n FROM shards').fetchone()[0]
print('dna tables:', len(dna), 'rows:', len(shards), 'counter:', n, 'distinct:', len(set(shards)), 'min:', min(shards), 'max:', max(shards), 'one sequence, no gaps, no duplicates:', sorted(shards) == list(range(1, n + 1)))
PY
say "S19 timeline and memory counts"; q "SELECT count(*) AS timeline_rows FROM timeline; SELECT count(*) AS runs FROM input; SELECT count(*) AS receipts FROM receipt;"
