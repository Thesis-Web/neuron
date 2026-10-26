.load ./mother
PRAGMA recursive_triggers = ON;
CREATE TABLE shards (n INTEGER NOT NULL); INSERT INTO shards VALUES (0);
CREATE TABLE hoplog (id INTEGER PRIMARY KEY, gate INTEGER, arrival INTEGER, remainder INTEGER, shard INTEGER);
CREATE TABLE "265" (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE TRIGGER "265" BEFORE INSERT ON "265" BEGIN
  SELECT mother('INSERT INTO "265" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce(NEW.arrival,'NULL') || ' , ' || coalesce(NEW.remainder,'NULL') || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "265" WHERE arrival IS ' || coalesce(NEW.arrival,'NULL') || ' AND remainder IS ' || coalesce(NEW.remainder,'NULL') || ' )');
  SELECT mother('UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "265" WHERE shard = n + 1 )');
  SELECT mother('INSERT INTO hoplog ( gate , arrival , remainder , shard ) SELECT 265 , ' || coalesce(NEW.arrival,'NULL') || ' , ' || coalesce(NEW.remainder,'NULL') || ' , shard FROM "265" WHERE arrival IS ' || coalesce(NEW.arrival,'NULL') || ' AND remainder IS ' || coalesce(NEW.remainder,'NULL'));
  SELECT RAISE(IGNORE);
END;
INSERT INTO "265" (arrival, remainder) VALUES (1, 118);
INSERT INTO "265" (arrival, remainder) VALUES (1, 118);
INSERT INTO "265" (arrival, remainder) VALUES (7, NULL);
SELECT 'rows in 265:', count(*) FROM "265"; SELECT * FROM "265";
SELECT 'hoplog:'; SELECT * FROM hoplog;
SELECT 'counter:', n FROM shards;
