-- look.sql: your eyes on the brain after a line. At the sqlite3 prompt: .read look.sql
-- Nothing here changes the brain; these are reads of its tables.
.mode column
.headers on
SELECT 'LAST RUN' AS section;
SELECT id, parent, substr(text, 1, 70) AS text, answer FROM input WHERE id >= (SELECT max(id) FROM input WHERE parent IS NULL) ORDER BY id;
SELECT 'RECEIPT of the last typed line: gate:shard in order' AS section;
SELECT group_concat(e.word || '(' || r.gate || ':' || coalesce(r.shard, '-') || ')', ' ') AS path
  FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = (SELECT max(id) FROM input WHERE parent IS NULL) ORDER BY r.id;
SELECT 'SHEET (cells) of the last typed line and its sub-runs' AS section;
SELECT run, name, value FROM sheet WHERE run >= (SELECT max(id) FROM input WHERE parent IS NULL) ORDER BY id;
SELECT 'NEW WORDS (encoder rows born since the last typed line)' AS section;
SELECT gate, word FROM encoder WHERE gate > (SELECT coalesce(max(gate), 0) FROM encoder e WHERE EXISTS (SELECT 1 FROM receipt r WHERE r.gate = e.gate AND r.run < (SELECT max(id) FROM input WHERE parent IS NULL))) ORDER BY gate;
SELECT 'NEW TABLES, GATES, TRIGGERS (the last 12 made)' AS section;
SELECT type, name, substr(sql, 1, 90) AS sql FROM sqlite_master WHERE rowid > (SELECT max(rowid) - 12 FROM sqlite_master) ORDER BY rowid;
SELECT 'SECONDARY INPUT (what the sources sent back, last 10)' AS section;
SELECT id, run, source, word, substr(text, 1, 80) AS text FROM secondary ORDER BY id DESC LIMIT 10;
SELECT 'COUNTS' AS section;
SELECT (SELECT n FROM shards) AS shards, (SELECT count(*) FROM receipt) AS receipts, (SELECT count(*) FROM encoder) AS words, (SELECT count(*) FROM sqlite_master WHERE type = 'table') AS tables, (SELECT count(*) FROM later) AS waiting_for_the_run_to_end;
