-- look.sql: your eyes on the brain after a line. At the sqlite3 prompt: .read look.sql
-- Nothing here changes the brain; these are reads of its tables, with the encoder giving the numbers their words.
.mode column
.headers on
SELECT 'RUNS of the last typed line (the line, the runs it started, what came back)' AS section;
SELECT i.id, i.parent, (SELECT word FROM encoder WHERE gate = i.arrival) AS arrival,
       substr((SELECT group_concat(word, '') FROM (SELECT e.word FROM json_each('[' || replace(i.gates, ' ', ',') || ']') j JOIN encoder e ON e.gate = j.value ORDER BY j.key)), 1, 70) AS words
  FROM input i WHERE i.id >= (SELECT max(id) FROM input WHERE parent IS NULL) ORDER BY i.id;
SELECT 'RECEIPT of the last typed line: word(gate:shard) in order' AS section;
SELECT group_concat(e.word || '(' || r.gate || ':' || r.shard || ')', ' ') AS path
  FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = (SELECT max(id) FROM input WHERE parent IS NULL) ORDER BY r.id;
SELECT 'SHEET (cells) of the last typed line and its runs' AS section;
SELECT s.run, (SELECT word FROM encoder WHERE gate = s.name) AS cell, s.value FROM sheet s WHERE s.run >= (SELECT max(id) FROM input WHERE parent IS NULL) ORDER BY s.id;
SELECT 'NEW WORDS (gates above the egg''s 252, newest first)' AS section;
SELECT gate, word FROM encoder WHERE gate > 252 ORDER BY gate DESC LIMIT 12;
SELECT 'NEW TABLES, GATES, TRIGGERS (the last 12 made)' AS section;
SELECT type, name, substr(sql, 1, 80) AS sql FROM sqlite_master WHERE rowid > (SELECT max(rowid) - 12 FROM sqlite_master) ORDER BY rowid;
SELECT 'COUNTS' AS section;
SELECT (SELECT n FROM shards) AS shards, (SELECT count(*) FROM receipt) AS receipts, (SELECT count(*) FROM encoder) AS encoder_rows, (SELECT count(*) FROM sqlite_master WHERE type = 'table') AS tables, (SELECT count(*) FROM input) AS runs;
