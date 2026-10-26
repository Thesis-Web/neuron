-- egg.sql: the hand-laid part of the brain. Laid once. Everything else is typed at the prompt.
-- Made from the owner's words of 2026-10-19/20 (see the build sheet).
PRAGMA recursive_triggers = ON;

-- the ear, the encoder, the one shard counter, the receipt, the sheet
CREATE TABLE input (id INTEGER PRIMARY KEY, parent INTEGER, arrival INTEGER, gates TEXT, text TEXT);
CREATE TABLE encoder (gate INTEGER PRIMARY KEY, word TEXT NOT NULL UNIQUE);
CREATE TABLE shards (n INTEGER NOT NULL);
INSERT INTO shards VALUES (0);
CREATE TABLE receipt (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER);
CREATE INDEX receipt_run ON receipt (run, gate);
CREATE TABLE sheet (id INTEGER PRIMARY KEY, run INTEGER, name INTEGER, value);
CREATE INDEX sheet_name ON sheet (name, run);

-- physics neurons: heard and said (where a line arrives from), hop, born, fire, end, build. Each is also a word
INSERT INTO encoder (gate, word) VALUES (1, 'heard');
INSERT INTO encoder (gate, word) VALUES (2, 'heard.dna');
INSERT INTO encoder (gate, word) VALUES (3, 'heard.definition');
INSERT INTO encoder (gate, word) VALUES (4, 'heard.memory');
CREATE TABLE "2" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "1" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "2" ;
CREATE TRIGGER "1" INSTEAD OF INSERT ON "1" BEGIN SELECT mother ( 'INSERT INTO "2" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "2" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "2" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 1 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "3" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "4" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "2" (shard, trigger) SELECT n + 1, 3 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (5, 'said');
INSERT INTO encoder (gate, word) VALUES (6, 'said.dna');
INSERT INTO encoder (gate, word) VALUES (7, 'said.definition');
INSERT INTO encoder (gate, word) VALUES (8, 'said.memory');
CREATE TABLE "6" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "5" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "6" ;
CREATE TRIGGER "5" INSTEAD OF INSERT ON "5" BEGIN SELECT mother ( 'INSERT INTO "6" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "6" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "6" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 5 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "7" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "8" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "6" (shard, trigger) SELECT n + 1, 7 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (9, 'hop');
INSERT INTO encoder (gate, word) VALUES (10, 'hop.dna');
INSERT INTO encoder (gate, word) VALUES (11, 'hop.definition');
INSERT INTO encoder (gate, word) VALUES (12, 'hop.memory');
CREATE TABLE "10" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "9" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "10" ;
CREATE TRIGGER "9" INSTEAD OF INSERT ON "9" BEGIN SELECT mother ( 'INSERT INTO "10" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "10" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "10" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 9 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "11" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "12" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "10" (shard, trigger) SELECT n + 1, 11 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (13, 'born');
INSERT INTO encoder (gate, word) VALUES (14, 'born.dna');
INSERT INTO encoder (gate, word) VALUES (15, 'born.definition');
INSERT INTO encoder (gate, word) VALUES (16, 'born.memory');
CREATE TABLE "14" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "13" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "14" ;
CREATE TRIGGER "13" INSTEAD OF INSERT ON "13" BEGIN SELECT mother ( 'INSERT INTO "14" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "14" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "14" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 13 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "15" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "16" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "14" (shard, trigger) SELECT n + 1, 15 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (17, 'fire');
INSERT INTO encoder (gate, word) VALUES (18, 'fire.dna');
INSERT INTO encoder (gate, word) VALUES (19, 'fire.definition');
INSERT INTO encoder (gate, word) VALUES (20, 'fire.memory');
CREATE TABLE "18" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "17" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "18" ;
CREATE TRIGGER "17" INSTEAD OF INSERT ON "17" BEGIN SELECT mother ( 'INSERT INTO "18" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "18" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "18" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 17 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "19" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "20" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "18" (shard, trigger) SELECT n + 1, 19 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (21, 'end');
INSERT INTO encoder (gate, word) VALUES (22, 'end.dna');
INSERT INTO encoder (gate, word) VALUES (23, 'end.definition');
INSERT INTO encoder (gate, word) VALUES (24, 'end.memory');
CREATE TABLE "22" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "21" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "22" ;
CREATE TRIGGER "21" INSTEAD OF INSERT ON "21" BEGIN SELECT mother ( 'INSERT INTO "22" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "22" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "22" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 21 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "23" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "24" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "22" (shard, trigger) SELECT n + 1, 23 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (25, 'build');
INSERT INTO encoder (gate, word) VALUES (26, 'build.dna');
INSERT INTO encoder (gate, word) VALUES (27, 'build.definition');
INSERT INTO encoder (gate, word) VALUES (28, 'build.memory');
CREATE TABLE "26" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "25" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "26" ;
CREATE TRIGGER "25" INSTEAD OF INSERT ON "25" BEGIN SELECT mother ( 'INSERT INTO "26" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "26" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "26" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 25 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "27" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "28" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "26" (shard, trigger) SELECT n + 1, 27 FROM shards; UPDATE shards SET n = n + 1;

-- the gates of the physics: views with no table under them, so a hand-off holds no cursor open while the next hop runs
CREATE VIEW hop AS SELECT NULL AS run, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest;
CREATE VIEW born AS SELECT NULL AS run, NULL AS gate;
CREATE VIEW fire AS SELECT NULL AS run, NULL AS target, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest, NULL AS shard;
CREATE VIEW build AS SELECT NULL AS run;

-- BUILD, var, the digits 0 to 9 (draft §3.9), and every token of the born run
INSERT INTO encoder (gate, word) VALUES (29, 'BUILD');
INSERT INTO encoder (gate, word) VALUES (30, 'BUILD.dna');
INSERT INTO encoder (gate, word) VALUES (31, 'BUILD.definition');
INSERT INTO encoder (gate, word) VALUES (32, 'BUILD.memory');
CREATE TABLE "30" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "29" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "30" ;
CREATE TRIGGER "29" INSTEAD OF INSERT ON "29" BEGIN SELECT mother ( 'INSERT INTO "30" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "30" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "30" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 29 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "31" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "32" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "30" (shard, trigger) SELECT n + 1, 31 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (33, 'var');
INSERT INTO encoder (gate, word) VALUES (34, 'var.dna');
INSERT INTO encoder (gate, word) VALUES (35, 'var.definition');
INSERT INTO encoder (gate, word) VALUES (36, 'var.memory');
CREATE TABLE "34" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "33" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "34" ;
CREATE TRIGGER "33" INSTEAD OF INSERT ON "33" BEGIN SELECT mother ( 'INSERT INTO "34" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "34" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "34" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 33 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "35" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "36" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "34" (shard, trigger) SELECT n + 1, 35 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (37, '0');
INSERT INTO encoder (gate, word) VALUES (38, '0.dna');
INSERT INTO encoder (gate, word) VALUES (39, '0.definition');
INSERT INTO encoder (gate, word) VALUES (40, '0.memory');
CREATE TABLE "38" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "37" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "38" ;
CREATE TRIGGER "37" INSTEAD OF INSERT ON "37" BEGIN SELECT mother ( 'INSERT INTO "38" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "38" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "38" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 37 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "39" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "40" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "38" (shard, trigger) SELECT n + 1, 39 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (41, '1');
INSERT INTO encoder (gate, word) VALUES (42, '1.dna');
INSERT INTO encoder (gate, word) VALUES (43, '1.definition');
INSERT INTO encoder (gate, word) VALUES (44, '1.memory');
CREATE TABLE "42" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "41" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "42" ;
CREATE TRIGGER "41" INSTEAD OF INSERT ON "41" BEGIN SELECT mother ( 'INSERT INTO "42" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "42" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "42" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 41 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "43" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "44" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "42" (shard, trigger) SELECT n + 1, 43 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (45, '2');
INSERT INTO encoder (gate, word) VALUES (46, '2.dna');
INSERT INTO encoder (gate, word) VALUES (47, '2.definition');
INSERT INTO encoder (gate, word) VALUES (48, '2.memory');
CREATE TABLE "46" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "45" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "46" ;
CREATE TRIGGER "45" INSTEAD OF INSERT ON "45" BEGIN SELECT mother ( 'INSERT INTO "46" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "46" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "46" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 45 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "47" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "48" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "46" (shard, trigger) SELECT n + 1, 47 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (49, '3');
INSERT INTO encoder (gate, word) VALUES (50, '3.dna');
INSERT INTO encoder (gate, word) VALUES (51, '3.definition');
INSERT INTO encoder (gate, word) VALUES (52, '3.memory');
CREATE TABLE "50" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "49" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "50" ;
CREATE TRIGGER "49" INSTEAD OF INSERT ON "49" BEGIN SELECT mother ( 'INSERT INTO "50" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "50" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "50" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 49 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "51" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "52" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "50" (shard, trigger) SELECT n + 1, 51 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (53, '4');
INSERT INTO encoder (gate, word) VALUES (54, '4.dna');
INSERT INTO encoder (gate, word) VALUES (55, '4.definition');
INSERT INTO encoder (gate, word) VALUES (56, '4.memory');
CREATE TABLE "54" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "53" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "54" ;
CREATE TRIGGER "53" INSTEAD OF INSERT ON "53" BEGIN SELECT mother ( 'INSERT INTO "54" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "54" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "54" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 53 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "55" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "56" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "54" (shard, trigger) SELECT n + 1, 55 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (57, '5');
INSERT INTO encoder (gate, word) VALUES (58, '5.dna');
INSERT INTO encoder (gate, word) VALUES (59, '5.definition');
INSERT INTO encoder (gate, word) VALUES (60, '5.memory');
CREATE TABLE "58" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "57" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "58" ;
CREATE TRIGGER "57" INSTEAD OF INSERT ON "57" BEGIN SELECT mother ( 'INSERT INTO "58" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "58" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "58" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 57 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "59" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "60" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "58" (shard, trigger) SELECT n + 1, 59 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (61, '6');
INSERT INTO encoder (gate, word) VALUES (62, '6.dna');
INSERT INTO encoder (gate, word) VALUES (63, '6.definition');
INSERT INTO encoder (gate, word) VALUES (64, '6.memory');
CREATE TABLE "62" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "61" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "62" ;
CREATE TRIGGER "61" INSTEAD OF INSERT ON "61" BEGIN SELECT mother ( 'INSERT INTO "62" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "62" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "62" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 61 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "63" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "64" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "62" (shard, trigger) SELECT n + 1, 63 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (65, '7');
INSERT INTO encoder (gate, word) VALUES (66, '7.dna');
INSERT INTO encoder (gate, word) VALUES (67, '7.definition');
INSERT INTO encoder (gate, word) VALUES (68, '7.memory');
CREATE TABLE "66" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "65" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "66" ;
CREATE TRIGGER "65" INSTEAD OF INSERT ON "65" BEGIN SELECT mother ( 'INSERT INTO "66" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "66" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "66" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 65 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "67" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "68" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "66" (shard, trigger) SELECT n + 1, 67 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (69, '8');
INSERT INTO encoder (gate, word) VALUES (70, '8.dna');
INSERT INTO encoder (gate, word) VALUES (71, '8.definition');
INSERT INTO encoder (gate, word) VALUES (72, '8.memory');
CREATE TABLE "70" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "69" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "70" ;
CREATE TRIGGER "69" INSTEAD OF INSERT ON "69" BEGIN SELECT mother ( 'INSERT INTO "70" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "70" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "70" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 69 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "71" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "72" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "70" (shard, trigger) SELECT n + 1, 71 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (73, '9');
INSERT INTO encoder (gate, word) VALUES (74, '9.dna');
INSERT INTO encoder (gate, word) VALUES (75, '9.definition');
INSERT INTO encoder (gate, word) VALUES (76, '9.memory');
CREATE TABLE "74" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "73" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "74" ;
CREATE TRIGGER "73" INSTEAD OF INSERT ON "73" BEGIN SELECT mother ( 'INSERT INTO "74" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "74" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "74" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 73 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "75" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "76" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "74" (shard, trigger) SELECT n + 1, 75 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (77, ' ');
INSERT INTO encoder (gate, word) VALUES (78, ' .dna');
INSERT INTO encoder (gate, word) VALUES (79, ' .definition');
INSERT INTO encoder (gate, word) VALUES (80, ' .memory');
CREATE TABLE "78" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "77" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "78" ;
CREATE TRIGGER "77" INSTEAD OF INSERT ON "77" BEGIN SELECT mother ( 'INSERT INTO "78" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "78" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "78" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 77 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "79" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "80" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "78" (shard, trigger) SELECT n + 1, 79 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (81, 'CREATE');
INSERT INTO encoder (gate, word) VALUES (82, 'CREATE.dna');
INSERT INTO encoder (gate, word) VALUES (83, 'CREATE.definition');
INSERT INTO encoder (gate, word) VALUES (84, 'CREATE.memory');
CREATE TABLE "82" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "81" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "82" ;
CREATE TRIGGER "81" INSTEAD OF INSERT ON "81" BEGIN SELECT mother ( 'INSERT INTO "82" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "82" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "82" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 81 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "83" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "84" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "82" (shard, trigger) SELECT n + 1, 83 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (85, 'TABLE');
INSERT INTO encoder (gate, word) VALUES (86, 'TABLE.dna');
INSERT INTO encoder (gate, word) VALUES (87, 'TABLE.definition');
INSERT INTO encoder (gate, word) VALUES (88, 'TABLE.memory');
CREATE TABLE "86" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "85" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "86" ;
CREATE TRIGGER "85" INSTEAD OF INSERT ON "85" BEGIN SELECT mother ( 'INSERT INTO "86" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "86" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "86" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 85 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "87" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "88" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "86" (shard, trigger) SELECT n + 1, 87 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (89, '"');
INSERT INTO encoder (gate, word) VALUES (90, '".dna');
INSERT INTO encoder (gate, word) VALUES (91, '".definition');
INSERT INTO encoder (gate, word) VALUES (92, '".memory');
CREATE TABLE "90" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "89" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "90" ;
CREATE TRIGGER "89" INSTEAD OF INSERT ON "89" BEGIN SELECT mother ( 'INSERT INTO "90" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "90" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "90" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 89 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "91" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "92" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "90" (shard, trigger) SELECT n + 1, 91 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (93, 'dna');
INSERT INTO encoder (gate, word) VALUES (94, 'dna.dna');
INSERT INTO encoder (gate, word) VALUES (95, 'dna.definition');
INSERT INTO encoder (gate, word) VALUES (96, 'dna.memory');
CREATE TABLE "94" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "93" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "94" ;
CREATE TRIGGER "93" INSTEAD OF INSERT ON "93" BEGIN SELECT mother ( 'INSERT INTO "94" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "94" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "94" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 93 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "95" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "96" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "94" (shard, trigger) SELECT n + 1, 95 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (97, '(');
INSERT INTO encoder (gate, word) VALUES (98, '(.dna');
INSERT INTO encoder (gate, word) VALUES (99, '(.definition');
INSERT INTO encoder (gate, word) VALUES (100, '(.memory');
CREATE TABLE "98" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "97" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "98" ;
CREATE TRIGGER "97" INSTEAD OF INSERT ON "97" BEGIN SELECT mother ( 'INSERT INTO "98" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "98" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "98" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 97 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "99" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "100" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "98" (shard, trigger) SELECT n + 1, 99 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (101, 'shard');
INSERT INTO encoder (gate, word) VALUES (102, 'shard.dna');
INSERT INTO encoder (gate, word) VALUES (103, 'shard.definition');
INSERT INTO encoder (gate, word) VALUES (104, 'shard.memory');
CREATE TABLE "102" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "101" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "102" ;
CREATE TRIGGER "101" INSTEAD OF INSERT ON "101" BEGIN SELECT mother ( 'INSERT INTO "102" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "102" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "102" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 101 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "103" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "104" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "102" (shard, trigger) SELECT n + 1, 103 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (105, 'INTEGER');
INSERT INTO encoder (gate, word) VALUES (106, 'INTEGER.dna');
INSERT INTO encoder (gate, word) VALUES (107, 'INTEGER.definition');
INSERT INTO encoder (gate, word) VALUES (108, 'INTEGER.memory');
CREATE TABLE "106" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "105" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "106" ;
CREATE TRIGGER "105" INSTEAD OF INSERT ON "105" BEGIN SELECT mother ( 'INSERT INTO "106" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "106" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "106" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 105 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "107" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "108" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "106" (shard, trigger) SELECT n + 1, 107 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (109, 'PRIMARY');
INSERT INTO encoder (gate, word) VALUES (110, 'PRIMARY.dna');
INSERT INTO encoder (gate, word) VALUES (111, 'PRIMARY.definition');
INSERT INTO encoder (gate, word) VALUES (112, 'PRIMARY.memory');
CREATE TABLE "110" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "109" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "110" ;
CREATE TRIGGER "109" INSTEAD OF INSERT ON "109" BEGIN SELECT mother ( 'INSERT INTO "110" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "110" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "110" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 109 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "111" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "112" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "110" (shard, trigger) SELECT n + 1, 111 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (113, 'KEY');
INSERT INTO encoder (gate, word) VALUES (114, 'KEY.dna');
INSERT INTO encoder (gate, word) VALUES (115, 'KEY.definition');
INSERT INTO encoder (gate, word) VALUES (116, 'KEY.memory');
CREATE TABLE "114" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "113" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "114" ;
CREATE TRIGGER "113" INSTEAD OF INSERT ON "113" BEGIN SELECT mother ( 'INSERT INTO "114" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "114" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "114" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 113 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "115" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "116" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "114" (shard, trigger) SELECT n + 1, 115 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (117, ',');
INSERT INTO encoder (gate, word) VALUES (118, ',.dna');
INSERT INTO encoder (gate, word) VALUES (119, ',.definition');
INSERT INTO encoder (gate, word) VALUES (120, ',.memory');
CREATE TABLE "118" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "117" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "118" ;
CREATE TRIGGER "117" INSTEAD OF INSERT ON "117" BEGIN SELECT mother ( 'INSERT INTO "118" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "118" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "118" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 117 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "119" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "120" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "118" (shard, trigger) SELECT n + 1, 119 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (121, 'arrival');
INSERT INTO encoder (gate, word) VALUES (122, 'arrival.dna');
INSERT INTO encoder (gate, word) VALUES (123, 'arrival.definition');
INSERT INTO encoder (gate, word) VALUES (124, 'arrival.memory');
CREATE TABLE "122" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "121" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "122" ;
CREATE TRIGGER "121" INSTEAD OF INSERT ON "121" BEGIN SELECT mother ( 'INSERT INTO "122" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "122" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "122" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 121 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "123" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "124" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "122" (shard, trigger) SELECT n + 1, 123 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (125, 'remainder');
INSERT INTO encoder (gate, word) VALUES (126, 'remainder.dna');
INSERT INTO encoder (gate, word) VALUES (127, 'remainder.definition');
INSERT INTO encoder (gate, word) VALUES (128, 'remainder.memory');
CREATE TABLE "126" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "125" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "126" ;
CREATE TRIGGER "125" INSTEAD OF INSERT ON "125" BEGIN SELECT mother ( 'INSERT INTO "126" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "126" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "126" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 125 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "127" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "128" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "126" (shard, trigger) SELECT n + 1, 127 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (129, 'trigger');
INSERT INTO encoder (gate, word) VALUES (130, 'trigger.dna');
INSERT INTO encoder (gate, word) VALUES (131, 'trigger.definition');
INSERT INTO encoder (gate, word) VALUES (132, 'trigger.memory');
CREATE TABLE "130" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "129" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "130" ;
CREATE TRIGGER "129" INSTEAD OF INSERT ON "129" BEGIN SELECT mother ( 'INSERT INTO "130" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "130" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "130" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 129 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "131" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "132" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "130" (shard, trigger) SELECT n + 1, 131 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (133, ')');
INSERT INTO encoder (gate, word) VALUES (134, ').dna');
INSERT INTO encoder (gate, word) VALUES (135, ').definition');
INSERT INTO encoder (gate, word) VALUES (136, ').memory');
CREATE TABLE "134" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "133" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "134" ;
CREATE TRIGGER "133" INSTEAD OF INSERT ON "133" BEGIN SELECT mother ( 'INSERT INTO "134" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "134" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "134" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 133 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "135" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "136" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "134" (shard, trigger) SELECT n + 1, 135 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (137, ';');
INSERT INTO encoder (gate, word) VALUES (138, ';.dna');
INSERT INTO encoder (gate, word) VALUES (139, ';.definition');
INSERT INTO encoder (gate, word) VALUES (140, ';.memory');
CREATE TABLE "138" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "137" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "138" ;
CREATE TRIGGER "137" INSTEAD OF INSERT ON "137" BEGIN SELECT mother ( 'INSERT INTO "138" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "138" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "138" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 137 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "139" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "140" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "138" (shard, trigger) SELECT n + 1, 139 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (141, 'VIEW');
INSERT INTO encoder (gate, word) VALUES (142, 'VIEW.dna');
INSERT INTO encoder (gate, word) VALUES (143, 'VIEW.definition');
INSERT INTO encoder (gate, word) VALUES (144, 'VIEW.memory');
CREATE TABLE "142" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "141" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "142" ;
CREATE TRIGGER "141" INSTEAD OF INSERT ON "141" BEGIN SELECT mother ( 'INSERT INTO "142" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "142" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "142" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 141 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "143" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "144" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "142" (shard, trigger) SELECT n + 1, 143 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (145, 'gate');
INSERT INTO encoder (gate, word) VALUES (146, 'gate.dna');
INSERT INTO encoder (gate, word) VALUES (147, 'gate.definition');
INSERT INTO encoder (gate, word) VALUES (148, 'gate.memory');
CREATE TABLE "146" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "145" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "146" ;
CREATE TRIGGER "145" INSTEAD OF INSERT ON "145" BEGIN SELECT mother ( 'INSERT INTO "146" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "146" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "146" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 145 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "147" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "148" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "146" (shard, trigger) SELECT n + 1, 147 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (149, 'AS');
INSERT INTO encoder (gate, word) VALUES (150, 'AS.dna');
INSERT INTO encoder (gate, word) VALUES (151, 'AS.definition');
INSERT INTO encoder (gate, word) VALUES (152, 'AS.memory');
CREATE TABLE "150" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "149" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "150" ;
CREATE TRIGGER "149" INSTEAD OF INSERT ON "149" BEGIN SELECT mother ( 'INSERT INTO "150" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "150" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "150" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 149 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "151" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "152" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "150" (shard, trigger) SELECT n + 1, 151 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (153, 'SELECT');
INSERT INTO encoder (gate, word) VALUES (154, 'SELECT.dna');
INSERT INTO encoder (gate, word) VALUES (155, 'SELECT.definition');
INSERT INTO encoder (gate, word) VALUES (156, 'SELECT.memory');
CREATE TABLE "154" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "153" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "154" ;
CREATE TRIGGER "153" INSTEAD OF INSERT ON "153" BEGIN SELECT mother ( 'INSERT INTO "154" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "154" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "154" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 153 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "155" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "156" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "154" (shard, trigger) SELECT n + 1, 155 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (157, 'NULL');
INSERT INTO encoder (gate, word) VALUES (158, 'NULL.dna');
INSERT INTO encoder (gate, word) VALUES (159, 'NULL.definition');
INSERT INTO encoder (gate, word) VALUES (160, 'NULL.memory');
CREATE TABLE "158" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "157" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "158" ;
CREATE TRIGGER "157" INSTEAD OF INSERT ON "157" BEGIN SELECT mother ( 'INSERT INTO "158" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "158" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "158" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 157 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "159" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "160" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "158" (shard, trigger) SELECT n + 1, 159 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (161, 'run');
INSERT INTO encoder (gate, word) VALUES (162, 'run.dna');
INSERT INTO encoder (gate, word) VALUES (163, 'run.definition');
INSERT INTO encoder (gate, word) VALUES (164, 'run.memory');
CREATE TABLE "162" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "161" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "162" ;
CREATE TRIGGER "161" INSTEAD OF INSERT ON "161" BEGIN SELECT mother ( 'INSERT INTO "162" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "162" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "162" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 161 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "163" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "164" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "162" (shard, trigger) SELECT n + 1, 163 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (165, 'rest');
INSERT INTO encoder (gate, word) VALUES (166, 'rest.dna');
INSERT INTO encoder (gate, word) VALUES (167, 'rest.definition');
INSERT INTO encoder (gate, word) VALUES (168, 'rest.memory');
CREATE TABLE "166" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "165" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "166" ;
CREATE TRIGGER "165" INSTEAD OF INSERT ON "165" BEGIN SELECT mother ( 'INSERT INTO "166" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "166" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "166" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 165 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "167" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "168" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "166" (shard, trigger) SELECT n + 1, 167 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (169, 'FROM');
INSERT INTO encoder (gate, word) VALUES (170, 'FROM.dna');
INSERT INTO encoder (gate, word) VALUES (171, 'FROM.definition');
INSERT INTO encoder (gate, word) VALUES (172, 'FROM.memory');
CREATE TABLE "170" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "169" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "170" ;
CREATE TRIGGER "169" INSTEAD OF INSERT ON "169" BEGIN SELECT mother ( 'INSERT INTO "170" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "170" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "170" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 169 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "171" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "172" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "170" (shard, trigger) SELECT n + 1, 171 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (173, 'TRIGGER');
INSERT INTO encoder (gate, word) VALUES (174, 'TRIGGER.dna');
INSERT INTO encoder (gate, word) VALUES (175, 'TRIGGER.definition');
INSERT INTO encoder (gate, word) VALUES (176, 'TRIGGER.memory');
CREATE TABLE "174" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "173" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "174" ;
CREATE TRIGGER "173" INSTEAD OF INSERT ON "173" BEGIN SELECT mother ( 'INSERT INTO "174" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "174" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "174" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 173 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "175" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "176" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "174" (shard, trigger) SELECT n + 1, 175 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (177, 'INSTEAD');
INSERT INTO encoder (gate, word) VALUES (178, 'INSTEAD.dna');
INSERT INTO encoder (gate, word) VALUES (179, 'INSTEAD.definition');
INSERT INTO encoder (gate, word) VALUES (180, 'INSTEAD.memory');
CREATE TABLE "178" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "177" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "178" ;
CREATE TRIGGER "177" INSTEAD OF INSERT ON "177" BEGIN SELECT mother ( 'INSERT INTO "178" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "178" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "178" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 177 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "179" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "180" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "178" (shard, trigger) SELECT n + 1, 179 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (181, 'OF');
INSERT INTO encoder (gate, word) VALUES (182, 'OF.dna');
INSERT INTO encoder (gate, word) VALUES (183, 'OF.definition');
INSERT INTO encoder (gate, word) VALUES (184, 'OF.memory');
CREATE TABLE "182" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "181" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "182" ;
CREATE TRIGGER "181" INSTEAD OF INSERT ON "181" BEGIN SELECT mother ( 'INSERT INTO "182" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "182" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "182" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 181 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "183" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "184" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "182" (shard, trigger) SELECT n + 1, 183 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (185, 'INSERT');
INSERT INTO encoder (gate, word) VALUES (186, 'INSERT.dna');
INSERT INTO encoder (gate, word) VALUES (187, 'INSERT.definition');
INSERT INTO encoder (gate, word) VALUES (188, 'INSERT.memory');
CREATE TABLE "186" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "185" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "186" ;
CREATE TRIGGER "185" INSTEAD OF INSERT ON "185" BEGIN SELECT mother ( 'INSERT INTO "186" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "186" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "186" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 185 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "187" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "188" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "186" (shard, trigger) SELECT n + 1, 187 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (189, 'ON');
INSERT INTO encoder (gate, word) VALUES (190, 'ON.dna');
INSERT INTO encoder (gate, word) VALUES (191, 'ON.definition');
INSERT INTO encoder (gate, word) VALUES (192, 'ON.memory');
CREATE TABLE "190" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "189" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "190" ;
CREATE TRIGGER "189" INSTEAD OF INSERT ON "189" BEGIN SELECT mother ( 'INSERT INTO "190" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "190" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "190" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 189 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "191" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "192" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "190" (shard, trigger) SELECT n + 1, 191 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (193, 'BEGIN');
INSERT INTO encoder (gate, word) VALUES (194, 'BEGIN.dna');
INSERT INTO encoder (gate, word) VALUES (195, 'BEGIN.definition');
INSERT INTO encoder (gate, word) VALUES (196, 'BEGIN.memory');
CREATE TABLE "194" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "193" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "194" ;
CREATE TRIGGER "193" INSTEAD OF INSERT ON "193" BEGIN SELECT mother ( 'INSERT INTO "194" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "194" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "194" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 193 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "195" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "196" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "194" (shard, trigger) SELECT n + 1, 195 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (197, 'mother');
INSERT INTO encoder (gate, word) VALUES (198, 'mother.dna');
INSERT INTO encoder (gate, word) VALUES (199, 'mother.definition');
INSERT INTO encoder (gate, word) VALUES (200, 'mother.memory');
CREATE TABLE "198" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "197" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "198" ;
CREATE TRIGGER "197" INSTEAD OF INSERT ON "197" BEGIN SELECT mother ( 'INSERT INTO "198" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "198" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "198" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 197 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "199" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "200" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "198" (shard, trigger) SELECT n + 1, 199 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (201, '''');
INSERT INTO encoder (gate, word) VALUES (202, '''.dna');
INSERT INTO encoder (gate, word) VALUES (203, '''.definition');
INSERT INTO encoder (gate, word) VALUES (204, '''.memory');
CREATE TABLE "202" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "201" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "202" ;
CREATE TRIGGER "201" INSTEAD OF INSERT ON "201" BEGIN SELECT mother ( 'INSERT INTO "202" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "202" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "202" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 201 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "203" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "204" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "202" (shard, trigger) SELECT n + 1, 203 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (205, 'INTO');
INSERT INTO encoder (gate, word) VALUES (206, 'INTO.dna');
INSERT INTO encoder (gate, word) VALUES (207, 'INTO.definition');
INSERT INTO encoder (gate, word) VALUES (208, 'INTO.memory');
CREATE TABLE "206" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "205" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "206" ;
CREATE TRIGGER "205" INSTEAD OF INSERT ON "205" BEGIN SELECT mother ( 'INSERT INTO "206" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "206" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "206" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 205 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "207" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "208" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "206" (shard, trigger) SELECT n + 1, 207 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (209, 'n');
INSERT INTO encoder (gate, word) VALUES (210, 'n.dna');
INSERT INTO encoder (gate, word) VALUES (211, 'n.definition');
INSERT INTO encoder (gate, word) VALUES (212, 'n.memory');
CREATE TABLE "210" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "209" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "210" ;
CREATE TRIGGER "209" INSTEAD OF INSERT ON "209" BEGIN SELECT mother ( 'INSERT INTO "210" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "210" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "210" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 209 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "211" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "212" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "210" (shard, trigger) SELECT n + 1, 211 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (213, '+');
INSERT INTO encoder (gate, word) VALUES (214, '+.dna');
INSERT INTO encoder (gate, word) VALUES (215, '+.definition');
INSERT INTO encoder (gate, word) VALUES (216, '+.memory');
CREATE TABLE "214" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "213" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "214" ;
CREATE TRIGGER "213" INSTEAD OF INSERT ON "213" BEGIN SELECT mother ( 'INSERT INTO "214" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "214" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "214" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 213 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "215" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "216" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "214" (shard, trigger) SELECT n + 1, 215 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (217, '|');
INSERT INTO encoder (gate, word) VALUES (218, '|.dna');
INSERT INTO encoder (gate, word) VALUES (219, '|.definition');
INSERT INTO encoder (gate, word) VALUES (220, '|.memory');
CREATE TABLE "218" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "217" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "218" ;
CREATE TRIGGER "217" INSTEAD OF INSERT ON "217" BEGIN SELECT mother ( 'INSERT INTO "218" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "218" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "218" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 217 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "219" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "220" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "218" (shard, trigger) SELECT n + 1, 219 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (221, 'coalesce');
INSERT INTO encoder (gate, word) VALUES (222, 'coalesce.dna');
INSERT INTO encoder (gate, word) VALUES (223, 'coalesce.definition');
INSERT INTO encoder (gate, word) VALUES (224, 'coalesce.memory');
CREATE TABLE "222" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "221" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "222" ;
CREATE TRIGGER "221" INSTEAD OF INSERT ON "221" BEGIN SELECT mother ( 'INSERT INTO "222" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "222" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "222" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 221 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "223" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "224" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "222" (shard, trigger) SELECT n + 1, 223 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (225, 'NEW');
INSERT INTO encoder (gate, word) VALUES (226, 'NEW.dna');
INSERT INTO encoder (gate, word) VALUES (227, 'NEW.definition');
INSERT INTO encoder (gate, word) VALUES (228, 'NEW.memory');
CREATE TABLE "226" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "225" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "226" ;
CREATE TRIGGER "225" INSTEAD OF INSERT ON "225" BEGIN SELECT mother ( 'INSERT INTO "226" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "226" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "226" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 225 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "227" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "228" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "226" (shard, trigger) SELECT n + 1, 227 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (229, '.');
INSERT INTO encoder (gate, word) VALUES (230, '..dna');
INSERT INTO encoder (gate, word) VALUES (231, '..definition');
INSERT INTO encoder (gate, word) VALUES (232, '..memory');
CREATE TABLE "230" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "229" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "230" ;
CREATE TRIGGER "229" INSTEAD OF INSERT ON "229" BEGIN SELECT mother ( 'INSERT INTO "230" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "230" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "230" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 229 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "231" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "232" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "230" (shard, trigger) SELECT n + 1, 231 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (233, 'shards');
INSERT INTO encoder (gate, word) VALUES (234, 'shards.dna');
INSERT INTO encoder (gate, word) VALUES (235, 'shards.definition');
INSERT INTO encoder (gate, word) VALUES (236, 'shards.memory');
CREATE TABLE "234" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "233" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "234" ;
CREATE TRIGGER "233" INSTEAD OF INSERT ON "233" BEGIN SELECT mother ( 'INSERT INTO "234" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "234" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "234" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 233 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "235" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "236" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "234" (shard, trigger) SELECT n + 1, 235 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (237, 'WHERE');
INSERT INTO encoder (gate, word) VALUES (238, 'WHERE.dna');
INSERT INTO encoder (gate, word) VALUES (239, 'WHERE.definition');
INSERT INTO encoder (gate, word) VALUES (240, 'WHERE.memory');
CREATE TABLE "238" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "237" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "238" ;
CREATE TRIGGER "237" INSTEAD OF INSERT ON "237" BEGIN SELECT mother ( 'INSERT INTO "238" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "238" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "238" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 237 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "239" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "240" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "238" (shard, trigger) SELECT n + 1, 239 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (241, 'NOT');
INSERT INTO encoder (gate, word) VALUES (242, 'NOT.dna');
INSERT INTO encoder (gate, word) VALUES (243, 'NOT.definition');
INSERT INTO encoder (gate, word) VALUES (244, 'NOT.memory');
CREATE TABLE "242" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "241" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "242" ;
CREATE TRIGGER "241" INSTEAD OF INSERT ON "241" BEGIN SELECT mother ( 'INSERT INTO "242" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "242" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "242" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 241 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "243" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "244" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "242" (shard, trigger) SELECT n + 1, 243 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (245, 'EXISTS');
INSERT INTO encoder (gate, word) VALUES (246, 'EXISTS.dna');
INSERT INTO encoder (gate, word) VALUES (247, 'EXISTS.definition');
INSERT INTO encoder (gate, word) VALUES (248, 'EXISTS.memory');
CREATE TABLE "246" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "245" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "246" ;
CREATE TRIGGER "245" INSTEAD OF INSERT ON "245" BEGIN SELECT mother ( 'INSERT INTO "246" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "246" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "246" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 245 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "247" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "248" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "246" (shard, trigger) SELECT n + 1, 247 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (249, 'IS');
INSERT INTO encoder (gate, word) VALUES (250, 'IS.dna');
INSERT INTO encoder (gate, word) VALUES (251, 'IS.definition');
INSERT INTO encoder (gate, word) VALUES (252, 'IS.memory');
CREATE TABLE "250" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "249" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "250" ;
CREATE TRIGGER "249" INSTEAD OF INSERT ON "249" BEGIN SELECT mother ( 'INSERT INTO "250" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "250" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "250" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 249 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "251" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "252" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "250" (shard, trigger) SELECT n + 1, 251 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (253, 'AND');
INSERT INTO encoder (gate, word) VALUES (254, 'AND.dna');
INSERT INTO encoder (gate, word) VALUES (255, 'AND.definition');
INSERT INTO encoder (gate, word) VALUES (256, 'AND.memory');
CREATE TABLE "254" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "253" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "254" ;
CREATE TRIGGER "253" INSTEAD OF INSERT ON "253" BEGIN SELECT mother ( 'INSERT INTO "254" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "254" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "254" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 253 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "255" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "256" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "254" (shard, trigger) SELECT n + 1, 255 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (257, 'UPDATE');
INSERT INTO encoder (gate, word) VALUES (258, 'UPDATE.dna');
INSERT INTO encoder (gate, word) VALUES (259, 'UPDATE.definition');
INSERT INTO encoder (gate, word) VALUES (260, 'UPDATE.memory');
CREATE TABLE "258" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "257" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "258" ;
CREATE TRIGGER "257" INSTEAD OF INSERT ON "257" BEGIN SELECT mother ( 'INSERT INTO "258" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "258" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "258" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 257 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "259" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "260" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "258" (shard, trigger) SELECT n + 1, 259 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (261, 'SET');
INSERT INTO encoder (gate, word) VALUES (262, 'SET.dna');
INSERT INTO encoder (gate, word) VALUES (263, 'SET.definition');
INSERT INTO encoder (gate, word) VALUES (264, 'SET.memory');
CREATE TABLE "262" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "261" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "262" ;
CREATE TRIGGER "261" INSTEAD OF INSERT ON "261" BEGIN SELECT mother ( 'INSERT INTO "262" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "262" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "262" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 261 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "263" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "264" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "262" (shard, trigger) SELECT n + 1, 263 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (265, '=');
INSERT INTO encoder (gate, word) VALUES (266, '=.dna');
INSERT INTO encoder (gate, word) VALUES (267, '=.definition');
INSERT INTO encoder (gate, word) VALUES (268, '=.memory');
CREATE TABLE "266" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "265" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "266" ;
CREATE TRIGGER "265" INSTEAD OF INSERT ON "265" BEGIN SELECT mother ( 'INSERT INTO "266" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "266" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "266" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 265 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "267" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "268" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "266" (shard, trigger) SELECT n + 1, 267 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (269, 'VALUES');
INSERT INTO encoder (gate, word) VALUES (270, 'VALUES.dna');
INSERT INTO encoder (gate, word) VALUES (271, 'VALUES.definition');
INSERT INTO encoder (gate, word) VALUES (272, 'VALUES.memory');
CREATE TABLE "270" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "269" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "270" ;
CREATE TRIGGER "269" INSTEAD OF INSERT ON "269" BEGIN SELECT mother ( 'INSERT INTO "270" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "270" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "270" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 269 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "271" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "272" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "270" (shard, trigger) SELECT n + 1, 271 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (273, 'END');
INSERT INTO encoder (gate, word) VALUES (274, 'END.dna');
INSERT INTO encoder (gate, word) VALUES (275, 'END.definition');
INSERT INTO encoder (gate, word) VALUES (276, 'END.memory');
CREATE TABLE "274" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "273" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "274" ;
CREATE TRIGGER "273" INSTEAD OF INSERT ON "273" BEGIN SELECT mother ( 'INSERT INTO "274" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "274" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "274" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 273 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "275" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "276" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "274" (shard, trigger) SELECT n + 1, 275 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (277, 'def');
INSERT INTO encoder (gate, word) VALUES (278, 'def.dna');
INSERT INTO encoder (gate, word) VALUES (279, 'def.definition');
INSERT INTO encoder (gate, word) VALUES (280, 'def.memory');
CREATE TABLE "278" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "277" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "278" ;
CREATE TRIGGER "277" INSTEAD OF INSERT ON "277" BEGIN SELECT mother ( 'INSERT INTO "278" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "278" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "278" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 277 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "279" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "280" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "278" (shard, trigger) SELECT n + 1, 279 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (281, 'id');
INSERT INTO encoder (gate, word) VALUES (282, 'id.dna');
INSERT INTO encoder (gate, word) VALUES (283, 'id.definition');
INSERT INTO encoder (gate, word) VALUES (284, 'id.memory');
CREATE TABLE "282" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "281" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "282" ;
CREATE TRIGGER "281" INSTEAD OF INSERT ON "281" BEGIN SELECT mother ( 'INSERT INTO "282" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "282" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "282" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 281 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "283" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "284" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "282" (shard, trigger) SELECT n + 1, 283 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (285, 'mem');
INSERT INTO encoder (gate, word) VALUES (286, 'mem.dna');
INSERT INTO encoder (gate, word) VALUES (287, 'mem.definition');
INSERT INTO encoder (gate, word) VALUES (288, 'mem.memory');
CREATE TABLE "286" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;
CREATE VIEW "285" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "286" ;
CREATE TRIGGER "285" INSTEAD OF INSERT ON "285" BEGIN SELECT mother ( 'INSERT INTO "286" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM "286" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM "286" WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 285 , NEW.arrival , NEW.remainder , NEW.rest ) ; END ;
CREATE TABLE "287" ( id INTEGER PRIMARY KEY , run INTEGER ) ;
CREATE TABLE "288" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;
INSERT INTO "286" (shard, trigger) SELECT n + 1, 287 FROM shards; UPDATE shards SET n = n + 1;


-- the hop: writes the receipt; fires what the row's trigger column names; closes a BUILD pair; at the end of a run that arrived from heard or a source (not from said, not from build) fires end; births a missing gate; lands on the next gate
CREATE TRIGGER hop_go INSTEAD OF INSERT ON hop BEGIN
  SELECT mother('INSERT INTO receipt (run, gate, shard) SELECT ' || NEW.run || ', ' || NEW.gate || ', shard FROM "' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.dna') || '" WHERE arrival IS ' || coalesce(NEW.arrival, 'NULL') || ' AND remainder IS ' || coalesce(NEW.remainder, 'NULL'));
  SELECT mother('INSERT INTO fire (run, target, gate, arrival, remainder, rest, shard) SELECT ' || NEW.run || ', trigger, ' || NEW.gate || ', ' || coalesce(NEW.arrival, 'NULL') || ', ' || coalesce(NEW.remainder, 'NULL') || ', ' || coalesce(quote(NEW.rest), 'NULL') || ', shard FROM "' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.dna') || '" WHERE arrival IS ' || coalesce(NEW.arrival, 'NULL') || ' AND remainder IS ' || coalesce(NEW.remainder, 'NULL') || ' AND trigger IS NOT NULL');
  SELECT mother('INSERT INTO build (run) VALUES (' || NEW.run || ')') WHERE NEW.gate = 29 AND (SELECT count(*) FROM receipt WHERE run = NEW.run AND gate = 29) % 2 = 0;
  SELECT mother('INSERT INTO fire (run, target, gate, arrival, remainder, rest, shard) SELECT ' || NEW.run || ', 21, ' || NEW.gate || ', ' || coalesce(NEW.arrival, 'NULL') || ', NULL, NULL, shard FROM "' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.dna') || '" WHERE arrival IS ' || coalesce(NEW.arrival, 'NULL') || ' AND remainder IS NULL') WHERE NEW.remainder IS NULL AND (SELECT arrival FROM input WHERE id = NEW.run) NOT IN (5, 25);
  SELECT mother('INSERT INTO born (run, gate) SELECT ' || NEW.run || ', ' || NEW.remainder || ' WHERE NOT EXISTS (SELECT 1 FROM sqlite_master WHERE type = ''view'' AND name = ''' || NEW.remainder || ''')') WHERE NEW.remainder IS NOT NULL;
  SELECT mother('INSERT INTO "' || NEW.remainder || '" (run, arrival, remainder, rest) VALUES (' || NEW.run || ', ' || NEW.gate || ', ' || coalesce(nullif(substr(NEW.rest || ' ', 1, instr(NEW.rest || ' ', ' ') - 1), ''), 'NULL') || ', ' || coalesce(quote(nullif(trim(substr(NEW.rest || ' ', instr(NEW.rest || ' ', ' ') + 1)), '')), 'NULL') || ')') WHERE NEW.remainder IS NOT NULL;
END;

-- build: the second BUILD of a pair landed. The words between the two BUILDs are read back with the var cells filled (this run's cells first, then its parents') and handed to mother; her answer comes back into the brain as a run
CREATE TRIGGER build_go INSTEAD OF INSERT ON build BEGIN
  SELECT mother('INSERT INTO input (text, parent, arrival) VALUES (' || quote(mother(t)) || ', ' || NEW.run || ', 25)') FROM (SELECT (
    WITH RECURSIVE up(id) AS (SELECT NEW.run UNION ALL SELECT i.parent FROM input i JOIN up ON i.id = up.id WHERE i.parent IS NOT NULL)
    SELECT group_concat(w, '') FROM (
      SELECT CASE WHEN p2 = 'var' AND p1 = ' ' THEN coalesce((SELECT value FROM sheet s WHERE s.name = g AND s.run IN (SELECT id FROM up) ORDER BY (s.run = NEW.run) DESC, s.id DESC LIMIT 1), 'var ' || word)
                  WHEN word = 'var' AND n1 = ' ' THEN '' WHEN p1 = 'var' AND word = ' ' THEN '' ELSE word END AS w
      FROM (SELECT e.word, e.gate AS g, lag(e.word, 1) OVER (ORDER BY r.id) AS p1, lag(e.word, 2) OVER (ORDER BY r.id) AS p2, lead(e.word, 1) OVER (ORDER BY r.id) AS n1, r.id
            FROM receipt r JOIN encoder e ON e.gate = r.gate
            WHERE r.run = NEW.run AND r.gate <> 29
              AND r.id > (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = 29 AND id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = 29))
              AND r.id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = 29)) ORDER BY id)) AS t);
END;

-- born: a gate with no neuron. It gives the new neuron's three tables their gate numbers in the encoder, writes the four numbers as cells, then fires born's own run if one is bound
CREATE TRIGGER born_go INSTEAD OF INSERT ON born BEGIN
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.dna' FROM encoder WHERE gate = NEW.gate;
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.definition' FROM encoder WHERE gate = NEW.gate;
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.memory' FROM encoder WHERE gate = NEW.gate;
  INSERT INTO sheet (run, name, value) VALUES
    (NEW.run, 145, NEW.gate),
    (NEW.run, 93, (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.dna')),
    (NEW.run, 277, (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.definition')),
    (NEW.run, 285, (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.memory'));
  SELECT mother('INSERT INTO fire (run, target, gate) SELECT ' || NEW.run || ', 13, ' || NEW.gate || ' WHERE EXISTS (SELECT 1 FROM "16" WHERE shard IS NULL)');
END;

-- fire: a DNA row's trigger column named a neuron (or the run ended: target end). The run, the row's gate, arrival, remainder, rest and shard are written as cells (a value that is NULL writes no cell); the neuron's formula, the newest run bound in its memory node (shard NULL), is typed again as a sub-run of this run, arriving from said
CREATE TRIGGER fire_go INSTEAD OF INSERT ON fire BEGIN
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 161, NEW.run WHERE NEW.run IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 145, NEW.gate WHERE NEW.gate IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 121, NEW.arrival WHERE NEW.arrival IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 125, NEW.remainder WHERE NEW.remainder IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 165, NEW.rest WHERE NEW.rest IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 101, NEW.shard WHERE NEW.shard IS NOT NULL;
  SELECT mother('INSERT INTO input (gates, parent, arrival) SELECT (SELECT group_concat(gate, '' '') FROM (SELECT gate FROM receipt WHERE run = (SELECT run FROM "' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.target) || '.memory') || '" WHERE shard IS NULL ORDER BY id DESC LIMIT 1) ORDER BY id)), ' || NEW.run || ', 5 WHERE EXISTS (SELECT 1 FROM "' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.target) || '.memory') || '" WHERE shard IS NULL)')
    WHERE EXISTS (SELECT 1 FROM encoder WHERE gate = (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.target) || '.memory'));
END;

-- the ear: a line with text is encoded to gates (a word is a run of letters and _; every digit and every other character, space included, is its own neuron), new words get a gate, the text is let go; a line that comes as gates (a replay) keeps them. Then the run hops from where it arrived (heard, said, a source, build) to its first gate
CREATE TRIGGER ear AFTER INSERT ON input BEGIN
  INSERT OR IGNORE INTO encoder (word)
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c))
    SELECT group_concat(ch, '') FROM t WHERE NEW.text IS NOT NULL GROUP BY tok;
  UPDATE input SET gates = (
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c)),
    w AS (SELECT tok, group_concat(ch, '') AS word FROM t GROUP BY tok)
    SELECT group_concat(gate, ' ') FROM (SELECT e.gate FROM w JOIN encoder e ON e.word = w.word ORDER BY w.tok)), text = NULL, arrival = coalesce(NEW.arrival, 1) WHERE id = NEW.id AND NEW.text IS NOT NULL;
  UPDATE input SET arrival = coalesce(NEW.arrival, 1) WHERE id = NEW.id AND NEW.text IS NULL;
  INSERT INTO hop (run, gate, arrival, remainder, rest)
    SELECT NEW.id, arrival, NULL, CAST(substr(gates || ' ', 1, instr(gates || ' ', ' ') - 1) AS INTEGER), nullif(trim(substr(gates || ' ', instr(gates || ' ', ' ') + 1)), '') FROM input WHERE id = NEW.id AND gates IS NOT NULL AND gates <> '';
END;
