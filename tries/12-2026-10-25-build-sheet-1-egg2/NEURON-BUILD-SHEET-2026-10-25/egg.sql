-- egg.sql: the hand-laid part of the brain. Laid once. Everything else is typed at the prompt.
-- Made from the owner's words of 2026-10-19/20 (see NEURON-BUILD-SHEET-2026-10-25.md).
PRAGMA recursive_triggers = ON;

-- the ear, the encoder, the shard counter, the receipt, the sheet, the secondary input, the output, the later queue
CREATE TABLE input (id INTEGER PRIMARY KEY, text TEXT NOT NULL, parent INTEGER, gates TEXT, answer TEXT);
CREATE TABLE encoder (gate INTEGER PRIMARY KEY, word TEXT NOT NULL UNIQUE);
CREATE TABLE shards (n INTEGER NOT NULL);
INSERT INTO shards VALUES (0);
CREATE TABLE receipt (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER);
CREATE INDEX receipt_run ON receipt (run, gate);
CREATE TABLE sheet (id INTEGER PRIMARY KEY, run INTEGER, name TEXT, value);
CREATE INDEX sheet_name ON sheet (name, run);
CREATE TABLE secondary (id INTEGER PRIMARY KEY, run INTEGER, source TEXT, word TEXT, hw TEXT, text TEXT);
CREATE TABLE output (id INTEGER PRIMARY KEY, run INTEGER, text TEXT);
CREATE INDEX output_run ON output (run);
CREATE TABLE later (id INTEGER PRIMARY KEY, text TEXT);

-- physics neurons: heard and said (where a line arrives from), hop, born, fire, end, build. Each is also a word, so a typed line may name it
INSERT INTO encoder (gate, word) VALUES (1, 'heard');
INSERT INTO encoder (gate, word) VALUES (2, 'heard.definition');
INSERT INTO encoder (gate, word) VALUES (3, 'heard.memory');
CREATE TABLE g1 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "1" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g1;
CREATE TRIGGER t1 INSTEAD OF INSERT ON "1" BEGIN SELECT mother ( 'INSERT INTO g1 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g1 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g1 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 1 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g2 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g3 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g1 (shard, trigger) SELECT n + 1, 2 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (4, 'said');
INSERT INTO encoder (gate, word) VALUES (5, 'said.definition');
INSERT INTO encoder (gate, word) VALUES (6, 'said.memory');
CREATE TABLE g4 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "4" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g4;
CREATE TRIGGER t4 INSTEAD OF INSERT ON "4" BEGIN SELECT mother ( 'INSERT INTO g4 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g4 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g4 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 4 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g5 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g6 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g4 (shard, trigger) SELECT n + 1, 5 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (7, 'hop');
INSERT INTO encoder (gate, word) VALUES (8, 'hop.definition');
INSERT INTO encoder (gate, word) VALUES (9, 'hop.memory');
CREATE TABLE g7 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "7" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g7;
CREATE TRIGGER t7 INSTEAD OF INSERT ON "7" BEGIN SELECT mother ( 'INSERT INTO g7 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g7 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g7 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 7 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g8 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g9 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g7 (shard, trigger) SELECT n + 1, 8 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (10, 'born');
INSERT INTO encoder (gate, word) VALUES (11, 'born.definition');
INSERT INTO encoder (gate, word) VALUES (12, 'born.memory');
CREATE TABLE g10 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "10" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g10;
CREATE TRIGGER t10 INSTEAD OF INSERT ON "10" BEGIN SELECT mother ( 'INSERT INTO g10 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g10 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g10 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 10 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g11 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g12 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g10 (shard, trigger) SELECT n + 1, 11 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (13, 'fire');
INSERT INTO encoder (gate, word) VALUES (14, 'fire.definition');
INSERT INTO encoder (gate, word) VALUES (15, 'fire.memory');
CREATE TABLE g13 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "13" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g13;
CREATE TRIGGER t13 INSTEAD OF INSERT ON "13" BEGIN SELECT mother ( 'INSERT INTO g13 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g13 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g13 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 13 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g14 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g15 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g13 (shard, trigger) SELECT n + 1, 14 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (16, 'end');
INSERT INTO encoder (gate, word) VALUES (17, 'end.definition');
INSERT INTO encoder (gate, word) VALUES (18, 'end.memory');
CREATE TABLE g16 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "16" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g16;
CREATE TRIGGER t16 INSTEAD OF INSERT ON "16" BEGIN SELECT mother ( 'INSERT INTO g16 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g16 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g16 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 16 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g17 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g18 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g16 (shard, trigger) SELECT n + 1, 17 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (19, 'build');
INSERT INTO encoder (gate, word) VALUES (20, 'build.definition');
INSERT INTO encoder (gate, word) VALUES (21, 'build.memory');
CREATE TABLE g19 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "19" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g19;
CREATE TRIGGER t19 INSTEAD OF INSERT ON "19" BEGIN SELECT mother ( 'INSERT INTO g19 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g19 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g19 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 19 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g20 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g21 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g19 (shard, trigger) SELECT n + 1, 20 FROM shards; UPDATE shards SET n = n + 1;

-- the gates of the physics: views with no table under them, so a hand-off holds no cursor open while the next hop runs
CREATE VIEW hop AS SELECT NULL AS run, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest;
CREATE VIEW born AS SELECT NULL AS run, NULL AS gate;
CREATE VIEW fire AS SELECT NULL AS run, NULL AS target, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest;
CREATE VIEW build AS SELECT NULL AS run;

-- BUILD, var, and every word of the born run
INSERT INTO encoder (gate, word) VALUES (22, 'BUILD');
INSERT INTO encoder (gate, word) VALUES (23, 'BUILD.definition');
INSERT INTO encoder (gate, word) VALUES (24, 'BUILD.memory');
CREATE TABLE g22 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "22" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g22;
CREATE TRIGGER t22 INSTEAD OF INSERT ON "22" BEGIN SELECT mother ( 'INSERT INTO g22 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g22 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g22 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 22 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g23 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g24 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g22 (shard, trigger) SELECT n + 1, 23 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (25, 'var');
INSERT INTO encoder (gate, word) VALUES (26, 'var.definition');
INSERT INTO encoder (gate, word) VALUES (27, 'var.memory');
CREATE TABLE g25 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "25" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g25;
CREATE TRIGGER t25 INSTEAD OF INSERT ON "25" BEGIN SELECT mother ( 'INSERT INTO g25 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g25 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g25 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 25 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g26 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g27 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g25 (shard, trigger) SELECT n + 1, 26 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (28, '0');
INSERT INTO encoder (gate, word) VALUES (29, '0.definition');
INSERT INTO encoder (gate, word) VALUES (30, '0.memory');
CREATE TABLE g28 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "28" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g28;
CREATE TRIGGER t28 INSTEAD OF INSERT ON "28" BEGIN SELECT mother ( 'INSERT INTO g28 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g28 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g28 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 28 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g29 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g30 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g28 (shard, trigger) SELECT n + 1, 29 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (31, '1');
INSERT INTO encoder (gate, word) VALUES (32, '1.definition');
INSERT INTO encoder (gate, word) VALUES (33, '1.memory');
CREATE TABLE g31 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "31" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g31;
CREATE TRIGGER t31 INSTEAD OF INSERT ON "31" BEGIN SELECT mother ( 'INSERT INTO g31 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g31 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g31 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 31 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g32 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g33 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g31 (shard, trigger) SELECT n + 1, 32 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (34, '2');
INSERT INTO encoder (gate, word) VALUES (35, '2.definition');
INSERT INTO encoder (gate, word) VALUES (36, '2.memory');
CREATE TABLE g34 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "34" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g34;
CREATE TRIGGER t34 INSTEAD OF INSERT ON "34" BEGIN SELECT mother ( 'INSERT INTO g34 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g34 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g34 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 34 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g35 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g36 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g34 (shard, trigger) SELECT n + 1, 35 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (37, '3');
INSERT INTO encoder (gate, word) VALUES (38, '3.definition');
INSERT INTO encoder (gate, word) VALUES (39, '3.memory');
CREATE TABLE g37 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "37" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g37;
CREATE TRIGGER t37 INSTEAD OF INSERT ON "37" BEGIN SELECT mother ( 'INSERT INTO g37 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g37 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g37 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 37 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g38 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g39 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g37 (shard, trigger) SELECT n + 1, 38 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (40, '4');
INSERT INTO encoder (gate, word) VALUES (41, '4.definition');
INSERT INTO encoder (gate, word) VALUES (42, '4.memory');
CREATE TABLE g40 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "40" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g40;
CREATE TRIGGER t40 INSTEAD OF INSERT ON "40" BEGIN SELECT mother ( 'INSERT INTO g40 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g40 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g40 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 40 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g41 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g42 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g40 (shard, trigger) SELECT n + 1, 41 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (43, '5');
INSERT INTO encoder (gate, word) VALUES (44, '5.definition');
INSERT INTO encoder (gate, word) VALUES (45, '5.memory');
CREATE TABLE g43 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "43" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g43;
CREATE TRIGGER t43 INSTEAD OF INSERT ON "43" BEGIN SELECT mother ( 'INSERT INTO g43 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g43 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g43 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 43 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g44 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g45 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g43 (shard, trigger) SELECT n + 1, 44 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (46, '6');
INSERT INTO encoder (gate, word) VALUES (47, '6.definition');
INSERT INTO encoder (gate, word) VALUES (48, '6.memory');
CREATE TABLE g46 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "46" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g46;
CREATE TRIGGER t46 INSTEAD OF INSERT ON "46" BEGIN SELECT mother ( 'INSERT INTO g46 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g46 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g46 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 46 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g47 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g48 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g46 (shard, trigger) SELECT n + 1, 47 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (49, '7');
INSERT INTO encoder (gate, word) VALUES (50, '7.definition');
INSERT INTO encoder (gate, word) VALUES (51, '7.memory');
CREATE TABLE g49 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "49" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g49;
CREATE TRIGGER t49 INSTEAD OF INSERT ON "49" BEGIN SELECT mother ( 'INSERT INTO g49 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g49 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g49 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 49 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g50 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g51 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g49 (shard, trigger) SELECT n + 1, 50 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (52, '8');
INSERT INTO encoder (gate, word) VALUES (53, '8.definition');
INSERT INTO encoder (gate, word) VALUES (54, '8.memory');
CREATE TABLE g52 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "52" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g52;
CREATE TRIGGER t52 INSTEAD OF INSERT ON "52" BEGIN SELECT mother ( 'INSERT INTO g52 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g52 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g52 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 52 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g53 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g54 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g52 (shard, trigger) SELECT n + 1, 53 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (55, '9');
INSERT INTO encoder (gate, word) VALUES (56, '9.definition');
INSERT INTO encoder (gate, word) VALUES (57, '9.memory');
CREATE TABLE g55 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "55" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g55;
CREATE TRIGGER t55 INSTEAD OF INSERT ON "55" BEGIN SELECT mother ( 'INSERT INTO g55 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g55 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g55 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 55 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g56 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g57 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g55 (shard, trigger) SELECT n + 1, 56 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (58, 'g');
INSERT INTO encoder (gate, word) VALUES (59, 'g.definition');
INSERT INTO encoder (gate, word) VALUES (60, 'g.memory');
CREATE TABLE g58 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "58" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g58;
CREATE TRIGGER t58 INSTEAD OF INSERT ON "58" BEGIN SELECT mother ( 'INSERT INTO g58 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g58 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g58 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 58 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g59 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g60 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g58 (shard, trigger) SELECT n + 1, 59 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (61, 't');
INSERT INTO encoder (gate, word) VALUES (62, 't.definition');
INSERT INTO encoder (gate, word) VALUES (63, 't.memory');
CREATE TABLE g61 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "61" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g61;
CREATE TRIGGER t61 INSTEAD OF INSERT ON "61" BEGIN SELECT mother ( 'INSERT INTO g61 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g61 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g61 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 61 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g62 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g63 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g61 (shard, trigger) SELECT n + 1, 62 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (64, 'd');
INSERT INTO encoder (gate, word) VALUES (65, 'd.definition');
INSERT INTO encoder (gate, word) VALUES (66, 'd.memory');
CREATE TABLE g64 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "64" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g64;
CREATE TRIGGER t64 INSTEAD OF INSERT ON "64" BEGIN SELECT mother ( 'INSERT INTO g64 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g64 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g64 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 64 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g65 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g66 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g64 (shard, trigger) SELECT n + 1, 65 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (67, 'm');
INSERT INTO encoder (gate, word) VALUES (68, 'm.definition');
INSERT INTO encoder (gate, word) VALUES (69, 'm.memory');
CREATE TABLE g67 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "67" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g67;
CREATE TRIGGER t67 INSTEAD OF INSERT ON "67" BEGIN SELECT mother ( 'INSERT INTO g67 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g67 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g67 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 67 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g68 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g69 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g67 (shard, trigger) SELECT n + 1, 68 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (70, 'DROP');
INSERT INTO encoder (gate, word) VALUES (71, 'DROP.definition');
INSERT INTO encoder (gate, word) VALUES (72, 'DROP.memory');
CREATE TABLE g70 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "70" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g70;
CREATE TRIGGER t70 INSTEAD OF INSERT ON "70" BEGIN SELECT mother ( 'INSERT INTO g70 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g70 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g70 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 70 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g71 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g72 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g70 (shard, trigger) SELECT n + 1, 71 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (73, 'ALTER');
INSERT INTO encoder (gate, word) VALUES (74, 'ALTER.definition');
INSERT INTO encoder (gate, word) VALUES (75, 'ALTER.memory');
CREATE TABLE g73 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "73" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g73;
CREATE TRIGGER t73 INSTEAD OF INSERT ON "73" BEGIN SELECT mother ( 'INSERT INTO g73 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g73 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g73 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 73 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g74 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g75 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g73 (shard, trigger) SELECT n + 1, 74 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (76, 'DELETE');
INSERT INTO encoder (gate, word) VALUES (77, 'DELETE.definition');
INSERT INTO encoder (gate, word) VALUES (78, 'DELETE.memory');
CREATE TABLE g76 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "76" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g76;
CREATE TRIGGER t76 INSTEAD OF INSERT ON "76" BEGIN SELECT mother ( 'INSERT INTO g76 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g76 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g76 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 76 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g77 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g78 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g76 (shard, trigger) SELECT n + 1, 77 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (79, 'VALUES');
INSERT INTO encoder (gate, word) VALUES (80, 'VALUES.definition');
INSERT INTO encoder (gate, word) VALUES (81, 'VALUES.memory');
CREATE TABLE g79 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "79" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g79;
CREATE TRIGGER t79 INSTEAD OF INSERT ON "79" BEGIN SELECT mother ( 'INSERT INTO g79 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g79 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g79 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 79 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g80 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g81 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g79 (shard, trigger) SELECT n + 1, 80 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (82, 'INTO');
INSERT INTO encoder (gate, word) VALUES (83, 'INTO.definition');
INSERT INTO encoder (gate, word) VALUES (84, 'INTO.memory');
CREATE TABLE g82 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "82" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g82;
CREATE TRIGGER t82 INSTEAD OF INSERT ON "82" BEGIN SELECT mother ( 'INSERT INTO g82 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g82 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g82 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 82 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g83 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g84 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g82 (shard, trigger) SELECT n + 1, 83 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (85, 'TEXT');
INSERT INTO encoder (gate, word) VALUES (86, 'TEXT.definition');
INSERT INTO encoder (gate, word) VALUES (87, 'TEXT.memory');
CREATE TABLE g85 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "85" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g85;
CREATE TRIGGER t85 INSTEAD OF INSERT ON "85" BEGIN SELECT mother ( 'INSERT INTO g85 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g85 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g85 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 85 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g86 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g87 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g85 (shard, trigger) SELECT n + 1, 86 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (88, 'ON');
INSERT INTO encoder (gate, word) VALUES (89, 'ON.definition');
INSERT INTO encoder (gate, word) VALUES (90, 'ON.memory');
CREATE TABLE g88 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "88" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g88;
CREATE TRIGGER t88 INSTEAD OF INSERT ON "88" BEGIN SELECT mother ( 'INSERT INTO g88 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g88 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g88 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 88 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g89 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g90 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g88 (shard, trigger) SELECT n + 1, 89 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (91, 'AFTER');
INSERT INTO encoder (gate, word) VALUES (92, 'AFTER.definition');
INSERT INTO encoder (gate, word) VALUES (93, 'AFTER.memory');
CREATE TABLE g91 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "91" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g91;
CREATE TRIGGER t91 INSTEAD OF INSERT ON "91" BEGIN SELECT mother ( 'INSERT INTO g91 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g91 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g91 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 91 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g92 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g93 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g91 (shard, trigger) SELECT n + 1, 92 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (94, 'WHEN');
INSERT INTO encoder (gate, word) VALUES (95, 'WHEN.definition');
INSERT INTO encoder (gate, word) VALUES (96, 'WHEN.memory');
CREATE TABLE g94 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "94" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g94;
CREATE TRIGGER t94 INSTEAD OF INSERT ON "94" BEGIN SELECT mother ( 'INSERT INTO g94 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g94 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g94 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 94 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g95 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g96 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g94 (shard, trigger) SELECT n + 1, 95 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (97, 'IS');
INSERT INTO encoder (gate, word) VALUES (98, 'IS.definition');
INSERT INTO encoder (gate, word) VALUES (99, 'IS.memory');
CREATE TABLE g97 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "97" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g97;
CREATE TRIGGER t97 INSTEAD OF INSERT ON "97" BEGIN SELECT mother ( 'INSERT INTO g97 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g97 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g97 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 97 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g98 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g99 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g97 (shard, trigger) SELECT n + 1, 98 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (100, 'AND');
INSERT INTO encoder (gate, word) VALUES (101, 'AND.definition');
INSERT INTO encoder (gate, word) VALUES (102, 'AND.memory');
CREATE TABLE g100 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "100" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g100;
CREATE TRIGGER t100 INSTEAD OF INSERT ON "100" BEGIN SELECT mother ( 'INSERT INTO g100 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g100 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g100 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 100 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g101 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g102 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g100 (shard, trigger) SELECT n + 1, 101 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (103, 'OR');
INSERT INTO encoder (gate, word) VALUES (104, 'OR.definition');
INSERT INTO encoder (gate, word) VALUES (105, 'OR.memory');
CREATE TABLE g103 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "103" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g103;
CREATE TRIGGER t103 INSTEAD OF INSERT ON "103" BEGIN SELECT mother ( 'INSERT INTO g103 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g103 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g103 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 103 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g104 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g105 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g103 (shard, trigger) SELECT n + 1, 104 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (106, 'NOT');
INSERT INTO encoder (gate, word) VALUES (107, 'NOT.definition');
INSERT INTO encoder (gate, word) VALUES (108, 'NOT.memory');
CREATE TABLE g106 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "106" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g106;
CREATE TRIGGER t106 INSTEAD OF INSERT ON "106" BEGIN SELECT mother ( 'INSERT INTO g106 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g106 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g106 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 106 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g107 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g108 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g106 (shard, trigger) SELECT n + 1, 107 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (109, 'NULL');
INSERT INTO encoder (gate, word) VALUES (110, 'NULL.definition');
INSERT INTO encoder (gate, word) VALUES (111, 'NULL.memory');
CREATE TABLE g109 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "109" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g109;
CREATE TRIGGER t109 INSTEAD OF INSERT ON "109" BEGIN SELECT mother ( 'INSERT INTO g109 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g109 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g109 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 109 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g110 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g111 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g109 (shard, trigger) SELECT n + 1, 110 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (112, 'new');
INSERT INTO encoder (gate, word) VALUES (113, 'new.definition');
INSERT INTO encoder (gate, word) VALUES (114, 'new.memory');
CREATE TABLE g112 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "112" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g112;
CREATE TRIGGER t112 INSTEAD OF INSERT ON "112" BEGIN SELECT mother ( 'INSERT INTO g112 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g112 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g112 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 112 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g113 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g114 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g112 (shard, trigger) SELECT n + 1, 113 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (115, 'next');
INSERT INTO encoder (gate, word) VALUES (116, 'next.definition');
INSERT INTO encoder (gate, word) VALUES (117, 'next.memory');
CREATE TABLE g115 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "115" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g115;
CREATE TRIGGER t115 INSTEAD OF INSERT ON "115" BEGIN SELECT mother ( 'INSERT INTO g115 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g115 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g115 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 115 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g116 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g117 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g115 (shard, trigger) SELECT n + 1, 116 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (118, ' ');
INSERT INTO encoder (gate, word) VALUES (119, ' .definition');
INSERT INTO encoder (gate, word) VALUES (120, ' .memory');
CREATE TABLE g118 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "118" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g118;
CREATE TRIGGER t118 INSTEAD OF INSERT ON "118" BEGIN SELECT mother ( 'INSERT INTO g118 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g118 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g118 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 118 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g119 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g120 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g118 (shard, trigger) SELECT n + 1, 119 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (121, 'CREATE');
INSERT INTO encoder (gate, word) VALUES (122, 'CREATE.definition');
INSERT INTO encoder (gate, word) VALUES (123, 'CREATE.memory');
CREATE TABLE g121 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "121" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g121;
CREATE TRIGGER t121 INSTEAD OF INSERT ON "121" BEGIN SELECT mother ( 'INSERT INTO g121 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g121 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g121 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 121 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g122 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g123 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g121 (shard, trigger) SELECT n + 1, 122 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (124, 'TABLE');
INSERT INTO encoder (gate, word) VALUES (125, 'TABLE.definition');
INSERT INTO encoder (gate, word) VALUES (126, 'TABLE.memory');
CREATE TABLE g124 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "124" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g124;
CREATE TRIGGER t124 INSTEAD OF INSERT ON "124" BEGIN SELECT mother ( 'INSERT INTO g124 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g124 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g124 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 124 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g125 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g126 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g124 (shard, trigger) SELECT n + 1, 125 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (127, 'dna');
INSERT INTO encoder (gate, word) VALUES (128, 'dna.definition');
INSERT INTO encoder (gate, word) VALUES (129, 'dna.memory');
CREATE TABLE g127 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "127" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g127;
CREATE TRIGGER t127 INSTEAD OF INSERT ON "127" BEGIN SELECT mother ( 'INSERT INTO g127 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g127 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g127 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 127 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g128 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g129 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g127 (shard, trigger) SELECT n + 1, 128 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (130, '(');
INSERT INTO encoder (gate, word) VALUES (131, '(.definition');
INSERT INTO encoder (gate, word) VALUES (132, '(.memory');
CREATE TABLE g130 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "130" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g130;
CREATE TRIGGER t130 INSTEAD OF INSERT ON "130" BEGIN SELECT mother ( 'INSERT INTO g130 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g130 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g130 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 130 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g131 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g132 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g130 (shard, trigger) SELECT n + 1, 131 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (133, 'shard');
INSERT INTO encoder (gate, word) VALUES (134, 'shard.definition');
INSERT INTO encoder (gate, word) VALUES (135, 'shard.memory');
CREATE TABLE g133 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "133" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g133;
CREATE TRIGGER t133 INSTEAD OF INSERT ON "133" BEGIN SELECT mother ( 'INSERT INTO g133 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g133 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g133 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 133 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g134 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g135 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g133 (shard, trigger) SELECT n + 1, 134 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (136, 'INTEGER');
INSERT INTO encoder (gate, word) VALUES (137, 'INTEGER.definition');
INSERT INTO encoder (gate, word) VALUES (138, 'INTEGER.memory');
CREATE TABLE g136 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "136" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g136;
CREATE TRIGGER t136 INSTEAD OF INSERT ON "136" BEGIN SELECT mother ( 'INSERT INTO g136 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g136 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g136 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 136 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g137 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g138 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g136 (shard, trigger) SELECT n + 1, 137 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (139, 'PRIMARY');
INSERT INTO encoder (gate, word) VALUES (140, 'PRIMARY.definition');
INSERT INTO encoder (gate, word) VALUES (141, 'PRIMARY.memory');
CREATE TABLE g139 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "139" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g139;
CREATE TRIGGER t139 INSTEAD OF INSERT ON "139" BEGIN SELECT mother ( 'INSERT INTO g139 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g139 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g139 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 139 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g140 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g141 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g139 (shard, trigger) SELECT n + 1, 140 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (142, 'KEY');
INSERT INTO encoder (gate, word) VALUES (143, 'KEY.definition');
INSERT INTO encoder (gate, word) VALUES (144, 'KEY.memory');
CREATE TABLE g142 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "142" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g142;
CREATE TRIGGER t142 INSTEAD OF INSERT ON "142" BEGIN SELECT mother ( 'INSERT INTO g142 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g142 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g142 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 142 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g143 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g144 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g142 (shard, trigger) SELECT n + 1, 143 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (145, ',');
INSERT INTO encoder (gate, word) VALUES (146, ',.definition');
INSERT INTO encoder (gate, word) VALUES (147, ',.memory');
CREATE TABLE g145 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "145" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g145;
CREATE TRIGGER t145 INSTEAD OF INSERT ON "145" BEGIN SELECT mother ( 'INSERT INTO g145 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g145 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g145 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 145 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g146 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g147 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g145 (shard, trigger) SELECT n + 1, 146 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (148, 'arrival');
INSERT INTO encoder (gate, word) VALUES (149, 'arrival.definition');
INSERT INTO encoder (gate, word) VALUES (150, 'arrival.memory');
CREATE TABLE g148 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "148" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g148;
CREATE TRIGGER t148 INSTEAD OF INSERT ON "148" BEGIN SELECT mother ( 'INSERT INTO g148 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g148 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g148 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 148 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g149 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g150 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g148 (shard, trigger) SELECT n + 1, 149 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (151, 'remainder');
INSERT INTO encoder (gate, word) VALUES (152, 'remainder.definition');
INSERT INTO encoder (gate, word) VALUES (153, 'remainder.memory');
CREATE TABLE g151 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "151" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g151;
CREATE TRIGGER t151 INSTEAD OF INSERT ON "151" BEGIN SELECT mother ( 'INSERT INTO g151 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g151 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g151 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 151 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g152 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g153 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g151 (shard, trigger) SELECT n + 1, 152 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (154, 'trigger');
INSERT INTO encoder (gate, word) VALUES (155, 'trigger.definition');
INSERT INTO encoder (gate, word) VALUES (156, 'trigger.memory');
CREATE TABLE g154 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "154" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g154;
CREATE TRIGGER t154 INSTEAD OF INSERT ON "154" BEGIN SELECT mother ( 'INSERT INTO g154 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g154 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g154 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 154 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g155 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g156 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g154 (shard, trigger) SELECT n + 1, 155 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (157, ')');
INSERT INTO encoder (gate, word) VALUES (158, ').definition');
INSERT INTO encoder (gate, word) VALUES (159, ').memory');
CREATE TABLE g157 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "157" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g157;
CREATE TRIGGER t157 INSTEAD OF INSERT ON "157" BEGIN SELECT mother ( 'INSERT INTO g157 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g157 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g157 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 157 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g158 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g159 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g157 (shard, trigger) SELECT n + 1, 158 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (160, ';');
INSERT INTO encoder (gate, word) VALUES (161, ';.definition');
INSERT INTO encoder (gate, word) VALUES (162, ';.memory');
CREATE TABLE g160 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "160" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g160;
CREATE TRIGGER t160 INSTEAD OF INSERT ON "160" BEGIN SELECT mother ( 'INSERT INTO g160 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g160 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g160 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 160 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g161 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g162 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g160 (shard, trigger) SELECT n + 1, 161 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (163, 'VIEW');
INSERT INTO encoder (gate, word) VALUES (164, 'VIEW.definition');
INSERT INTO encoder (gate, word) VALUES (165, 'VIEW.memory');
CREATE TABLE g163 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "163" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g163;
CREATE TRIGGER t163 INSTEAD OF INSERT ON "163" BEGIN SELECT mother ( 'INSERT INTO g163 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g163 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g163 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 163 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g164 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g165 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g163 (shard, trigger) SELECT n + 1, 164 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (166, '"');
INSERT INTO encoder (gate, word) VALUES (167, '".definition');
INSERT INTO encoder (gate, word) VALUES (168, '".memory');
CREATE TABLE g166 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "166" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g166;
CREATE TRIGGER t166 INSTEAD OF INSERT ON "166" BEGIN SELECT mother ( 'INSERT INTO g166 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g166 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g166 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 166 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g167 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g168 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g166 (shard, trigger) SELECT n + 1, 167 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (169, 'gate');
INSERT INTO encoder (gate, word) VALUES (170, 'gate.definition');
INSERT INTO encoder (gate, word) VALUES (171, 'gate.memory');
CREATE TABLE g169 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "169" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g169;
CREATE TRIGGER t169 INSTEAD OF INSERT ON "169" BEGIN SELECT mother ( 'INSERT INTO g169 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g169 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g169 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 169 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g170 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g171 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g169 (shard, trigger) SELECT n + 1, 170 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (172, 'AS');
INSERT INTO encoder (gate, word) VALUES (173, 'AS.definition');
INSERT INTO encoder (gate, word) VALUES (174, 'AS.memory');
CREATE TABLE g172 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "172" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g172;
CREATE TRIGGER t172 INSTEAD OF INSERT ON "172" BEGIN SELECT mother ( 'INSERT INTO g172 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g172 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g172 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 172 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g173 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g174 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g172 (shard, trigger) SELECT n + 1, 173 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (175, 'SELECT');
INSERT INTO encoder (gate, word) VALUES (176, 'SELECT.definition');
INSERT INTO encoder (gate, word) VALUES (177, 'SELECT.memory');
CREATE TABLE g175 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "175" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g175;
CREATE TRIGGER t175 INSTEAD OF INSERT ON "175" BEGIN SELECT mother ( 'INSERT INTO g175 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g175 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g175 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 175 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g176 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g177 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g175 (shard, trigger) SELECT n + 1, 176 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (178, 'run');
INSERT INTO encoder (gate, word) VALUES (179, 'run.definition');
INSERT INTO encoder (gate, word) VALUES (180, 'run.memory');
CREATE TABLE g178 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "178" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g178;
CREATE TRIGGER t178 INSTEAD OF INSERT ON "178" BEGIN SELECT mother ( 'INSERT INTO g178 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g178 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g178 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 178 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g179 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g180 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g178 (shard, trigger) SELECT n + 1, 179 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (181, 'rest');
INSERT INTO encoder (gate, word) VALUES (182, 'rest.definition');
INSERT INTO encoder (gate, word) VALUES (183, 'rest.memory');
CREATE TABLE g181 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "181" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g181;
CREATE TRIGGER t181 INSTEAD OF INSERT ON "181" BEGIN SELECT mother ( 'INSERT INTO g181 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g181 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g181 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 181 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g182 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g183 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g181 (shard, trigger) SELECT n + 1, 182 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (184, 'FROM');
INSERT INTO encoder (gate, word) VALUES (185, 'FROM.definition');
INSERT INTO encoder (gate, word) VALUES (186, 'FROM.memory');
CREATE TABLE g184 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "184" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g184;
CREATE TRIGGER t184 INSTEAD OF INSERT ON "184" BEGIN SELECT mother ( 'INSERT INTO g184 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g184 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g184 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 184 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g185 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g186 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g184 (shard, trigger) SELECT n + 1, 185 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (187, 'TRIGGER');
INSERT INTO encoder (gate, word) VALUES (188, 'TRIGGER.definition');
INSERT INTO encoder (gate, word) VALUES (189, 'TRIGGER.memory');
CREATE TABLE g187 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "187" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g187;
CREATE TRIGGER t187 INSTEAD OF INSERT ON "187" BEGIN SELECT mother ( 'INSERT INTO g187 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g187 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g187 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 187 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g188 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g189 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g187 (shard, trigger) SELECT n + 1, 188 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (190, 'trig');
INSERT INTO encoder (gate, word) VALUES (191, 'trig.definition');
INSERT INTO encoder (gate, word) VALUES (192, 'trig.memory');
CREATE TABLE g190 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "190" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g190;
CREATE TRIGGER t190 INSTEAD OF INSERT ON "190" BEGIN SELECT mother ( 'INSERT INTO g190 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g190 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g190 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 190 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g191 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g192 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g190 (shard, trigger) SELECT n + 1, 191 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (193, 'INSTEAD');
INSERT INTO encoder (gate, word) VALUES (194, 'INSTEAD.definition');
INSERT INTO encoder (gate, word) VALUES (195, 'INSTEAD.memory');
CREATE TABLE g193 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "193" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g193;
CREATE TRIGGER t193 INSTEAD OF INSERT ON "193" BEGIN SELECT mother ( 'INSERT INTO g193 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g193 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g193 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 193 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g194 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g195 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g193 (shard, trigger) SELECT n + 1, 194 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (196, 'OF');
INSERT INTO encoder (gate, word) VALUES (197, 'OF.definition');
INSERT INTO encoder (gate, word) VALUES (198, 'OF.memory');
CREATE TABLE g196 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "196" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g196;
CREATE TRIGGER t196 INSTEAD OF INSERT ON "196" BEGIN SELECT mother ( 'INSERT INTO g196 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g196 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g196 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 196 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g197 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g198 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g196 (shard, trigger) SELECT n + 1, 197 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (199, 'INSERT');
INSERT INTO encoder (gate, word) VALUES (200, 'INSERT.definition');
INSERT INTO encoder (gate, word) VALUES (201, 'INSERT.memory');
CREATE TABLE g199 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "199" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g199;
CREATE TRIGGER t199 INSTEAD OF INSERT ON "199" BEGIN SELECT mother ( 'INSERT INTO g199 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g199 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g199 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 199 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g200 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g201 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g199 (shard, trigger) SELECT n + 1, 200 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (202, 'BEGIN');
INSERT INTO encoder (gate, word) VALUES (203, 'BEGIN.definition');
INSERT INTO encoder (gate, word) VALUES (204, 'BEGIN.memory');
CREATE TABLE g202 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "202" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g202;
CREATE TRIGGER t202 INSTEAD OF INSERT ON "202" BEGIN SELECT mother ( 'INSERT INTO g202 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g202 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g202 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 202 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g203 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g204 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g202 (shard, trigger) SELECT n + 1, 203 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (205, 'mother');
INSERT INTO encoder (gate, word) VALUES (206, 'mother.definition');
INSERT INTO encoder (gate, word) VALUES (207, 'mother.memory');
CREATE TABLE g205 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "205" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g205;
CREATE TRIGGER t205 INSTEAD OF INSERT ON "205" BEGIN SELECT mother ( 'INSERT INTO g205 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g205 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g205 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 205 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g206 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g207 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g205 (shard, trigger) SELECT n + 1, 206 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (208, '''');
INSERT INTO encoder (gate, word) VALUES (209, '''.definition');
INSERT INTO encoder (gate, word) VALUES (210, '''.memory');
CREATE TABLE g208 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "208" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g208;
CREATE TRIGGER t208 INSTEAD OF INSERT ON "208" BEGIN SELECT mother ( 'INSERT INTO g208 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g208 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g208 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 208 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g209 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g210 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g208 (shard, trigger) SELECT n + 1, 209 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (211, 'n');
INSERT INTO encoder (gate, word) VALUES (212, 'n.definition');
INSERT INTO encoder (gate, word) VALUES (213, 'n.memory');
CREATE TABLE g211 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "211" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g211;
CREATE TRIGGER t211 INSTEAD OF INSERT ON "211" BEGIN SELECT mother ( 'INSERT INTO g211 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g211 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g211 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 211 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g212 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g213 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g211 (shard, trigger) SELECT n + 1, 212 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (214, '+');
INSERT INTO encoder (gate, word) VALUES (215, '+.definition');
INSERT INTO encoder (gate, word) VALUES (216, '+.memory');
CREATE TABLE g214 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "214" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g214;
CREATE TRIGGER t214 INSTEAD OF INSERT ON "214" BEGIN SELECT mother ( 'INSERT INTO g214 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g214 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g214 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 214 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g215 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g216 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g214 (shard, trigger) SELECT n + 1, 215 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (217, '|');
INSERT INTO encoder (gate, word) VALUES (218, '|.definition');
INSERT INTO encoder (gate, word) VALUES (219, '|.memory');
CREATE TABLE g217 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "217" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g217;
CREATE TRIGGER t217 INSTEAD OF INSERT ON "217" BEGIN SELECT mother ( 'INSERT INTO g217 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g217 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g217 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 217 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g218 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g219 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g217 (shard, trigger) SELECT n + 1, 218 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (220, 'coalesce');
INSERT INTO encoder (gate, word) VALUES (221, 'coalesce.definition');
INSERT INTO encoder (gate, word) VALUES (222, 'coalesce.memory');
CREATE TABLE g220 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "220" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g220;
CREATE TRIGGER t220 INSTEAD OF INSERT ON "220" BEGIN SELECT mother ( 'INSERT INTO g220 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g220 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g220 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 220 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g221 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g222 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g220 (shard, trigger) SELECT n + 1, 221 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (223, 'NEW');
INSERT INTO encoder (gate, word) VALUES (224, 'NEW.definition');
INSERT INTO encoder (gate, word) VALUES (225, 'NEW.memory');
CREATE TABLE g223 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "223" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g223;
CREATE TRIGGER t223 INSTEAD OF INSERT ON "223" BEGIN SELECT mother ( 'INSERT INTO g223 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g223 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g223 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 223 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g224 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g225 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g223 (shard, trigger) SELECT n + 1, 224 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (226, '.');
INSERT INTO encoder (gate, word) VALUES (227, '..definition');
INSERT INTO encoder (gate, word) VALUES (228, '..memory');
CREATE TABLE g226 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "226" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g226;
CREATE TRIGGER t226 INSTEAD OF INSERT ON "226" BEGIN SELECT mother ( 'INSERT INTO g226 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g226 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g226 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 226 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g227 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g228 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g226 (shard, trigger) SELECT n + 1, 227 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (229, 'shards');
INSERT INTO encoder (gate, word) VALUES (230, 'shards.definition');
INSERT INTO encoder (gate, word) VALUES (231, 'shards.memory');
CREATE TABLE g229 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "229" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g229;
CREATE TRIGGER t229 INSTEAD OF INSERT ON "229" BEGIN SELECT mother ( 'INSERT INTO g229 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g229 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g229 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 229 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g230 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g231 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g229 (shard, trigger) SELECT n + 1, 230 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (232, 'WHERE');
INSERT INTO encoder (gate, word) VALUES (233, 'WHERE.definition');
INSERT INTO encoder (gate, word) VALUES (234, 'WHERE.memory');
CREATE TABLE g232 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "232" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g232;
CREATE TRIGGER t232 INSTEAD OF INSERT ON "232" BEGIN SELECT mother ( 'INSERT INTO g232 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g232 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g232 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 232 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g233 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g234 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g232 (shard, trigger) SELECT n + 1, 233 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (235, 'EXISTS');
INSERT INTO encoder (gate, word) VALUES (236, 'EXISTS.definition');
INSERT INTO encoder (gate, word) VALUES (237, 'EXISTS.memory');
CREATE TABLE g235 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "235" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g235;
CREATE TRIGGER t235 INSTEAD OF INSERT ON "235" BEGIN SELECT mother ( 'INSERT INTO g235 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g235 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g235 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 235 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g236 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g237 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g235 (shard, trigger) SELECT n + 1, 236 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (238, 'UPDATE');
INSERT INTO encoder (gate, word) VALUES (239, 'UPDATE.definition');
INSERT INTO encoder (gate, word) VALUES (240, 'UPDATE.memory');
CREATE TABLE g238 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "238" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g238;
CREATE TRIGGER t238 INSTEAD OF INSERT ON "238" BEGIN SELECT mother ( 'INSERT INTO g238 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g238 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g238 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 238 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g239 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g240 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g238 (shard, trigger) SELECT n + 1, 239 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (241, 'SET');
INSERT INTO encoder (gate, word) VALUES (242, 'SET.definition');
INSERT INTO encoder (gate, word) VALUES (243, 'SET.memory');
CREATE TABLE g241 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "241" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g241;
CREATE TRIGGER t241 INSTEAD OF INSERT ON "241" BEGIN SELECT mother ( 'INSERT INTO g241 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g241 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g241 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 241 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g242 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g243 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g241 (shard, trigger) SELECT n + 1, 242 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (244, '=');
INSERT INTO encoder (gate, word) VALUES (245, '=.definition');
INSERT INTO encoder (gate, word) VALUES (246, '=.memory');
CREATE TABLE g244 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "244" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g244;
CREATE TRIGGER t244 INSTEAD OF INSERT ON "244" BEGIN SELECT mother ( 'INSERT INTO g244 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g244 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g244 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 244 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g245 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g246 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g244 (shard, trigger) SELECT n + 1, 245 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (247, 'END');
INSERT INTO encoder (gate, word) VALUES (248, 'END.definition');
INSERT INTO encoder (gate, word) VALUES (249, 'END.memory');
CREATE TABLE g247 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "247" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g247;
CREATE TRIGGER t247 INSTEAD OF INSERT ON "247" BEGIN SELECT mother ( 'INSERT INTO g247 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g247 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g247 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 247 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g248 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g249 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g247 (shard, trigger) SELECT n + 1, 248 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (250, 'def');
INSERT INTO encoder (gate, word) VALUES (251, 'def.definition');
INSERT INTO encoder (gate, word) VALUES (252, 'def.memory');
CREATE TABLE g250 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "250" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g250;
CREATE TRIGGER t250 INSTEAD OF INSERT ON "250" BEGIN SELECT mother ( 'INSERT INTO g250 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g250 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g250 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 250 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g251 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g252 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g250 (shard, trigger) SELECT n + 1, 251 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (253, 'id');
INSERT INTO encoder (gate, word) VALUES (254, 'id.definition');
INSERT INTO encoder (gate, word) VALUES (255, 'id.memory');
CREATE TABLE g253 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "253" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g253;
CREATE TRIGGER t253 INSTEAD OF INSERT ON "253" BEGIN SELECT mother ( 'INSERT INTO g253 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g253 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g253 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 253 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g254 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g255 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g253 (shard, trigger) SELECT n + 1, 254 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (256, 'secondary');
INSERT INTO encoder (gate, word) VALUES (257, 'secondary.definition');
INSERT INTO encoder (gate, word) VALUES (258, 'secondary.memory');
CREATE TABLE g256 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "256" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g256;
CREATE TRIGGER t256 INSTEAD OF INSERT ON "256" BEGIN SELECT mother ( 'INSERT INTO g256 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g256 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g256 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 256 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g257 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g258 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g256 (shard, trigger) SELECT n + 1, 257 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (259, 'mem');
INSERT INTO encoder (gate, word) VALUES (260, 'mem.definition');
INSERT INTO encoder (gate, word) VALUES (261, 'mem.memory');
CREATE TABLE g259 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "259" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g259;
CREATE TRIGGER t259 INSTEAD OF INSERT ON "259" BEGIN SELECT mother ( 'INSERT INTO g259 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g259 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g259 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 259 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g260 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g261 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g259 (shard, trigger) SELECT n + 1, 260 FROM shards; UPDATE shards SET n = n + 1;

INSERT INTO encoder (gate, word) VALUES (262, 'defgate');
INSERT INTO encoder (gate, word) VALUES (263, 'defgate.definition');
INSERT INTO encoder (gate, word) VALUES (264, 'defgate.memory');
CREATE TABLE g262 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);
CREATE VIEW "262" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g262;
CREATE TRIGGER t262 INSTEAD OF INSERT ON "262" BEGIN SELECT mother ( 'INSERT INTO g262 ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) || ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM g262 WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM g262 WHERE shard = n + 1 )' ) ; INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , 262 , NEW.arrival , NEW.remainder , NEW.rest ) ; END;
CREATE TABLE g263 (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);
CREATE TABLE g264 (id INTEGER PRIMARY KEY, run INTEGER);
INSERT INTO g262 (shard, trigger) SELECT n + 1, 263 FROM shards; UPDATE shards SET n = n + 1;


-- the hop: writes the receipt, fires the row's trigger column, closes a BUILD pair, ends the run, births a missing gate, lands on the next gate
CREATE TRIGGER hop_go INSTEAD OF INSERT ON hop BEGIN
  SELECT mother('INSERT INTO receipt (run, gate, shard) SELECT ' || NEW.run || ', ' || NEW.gate || ', shard FROM g' || NEW.gate || ' WHERE arrival IS ' || coalesce(NEW.arrival, 'NULL') || ' AND remainder IS ' || coalesce(NEW.remainder, 'NULL'));
  SELECT mother('INSERT INTO fire (run, target, gate, arrival, remainder, rest) SELECT ' || NEW.run || ', trigger, ' || NEW.gate || ', ' || coalesce(NEW.arrival, 'NULL') || ', ' || coalesce(NEW.remainder, 'NULL') || ', ' || coalesce(quote(NEW.rest), 'NULL') || ' FROM g' || NEW.gate || ' WHERE arrival IS ' || coalesce(NEW.arrival, 'NULL') || ' AND remainder IS ' || coalesce(NEW.remainder, 'NULL') || ' AND trigger IS NOT NULL AND EXISTS (SELECT 1 FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = trigger) || ''.memory'')');
  SELECT mother('INSERT INTO build (run) VALUES (' || NEW.run || ')') WHERE NEW.gate = 22 AND (SELECT count(*) FROM receipt WHERE run = NEW.run AND gate = 22) % 2 = 0;
  INSERT INTO "16" (run, arrival, remainder, rest) SELECT NEW.run, NEW.gate, NULL, NULL WHERE NEW.remainder IS NULL AND NEW.gate <> 16;
  SELECT mother('INSERT INTO born (run, gate) SELECT ' || NEW.run || ', ' || NEW.remainder || ' WHERE NOT EXISTS (SELECT 1 FROM sqlite_master WHERE type = ''view'' AND name = ''' || NEW.remainder || ''')') WHERE NEW.remainder IS NOT NULL;
  SELECT mother('INSERT INTO "' || NEW.remainder || '" (run, arrival, remainder, rest) VALUES (' || NEW.run || ', ' || NEW.gate || ', ' || coalesce(nullif(substr(NEW.rest || ' ', 1, instr(NEW.rest || ' ', ' ') - 1), ''), 'NULL') || ', ' || coalesce(quote(nullif(trim(substr(NEW.rest || ' ', instr(NEW.rest || ' ', ' ') + 1)), '')), 'NULL') || ')', NEW.run) WHERE NEW.remainder IS NOT NULL;
  UPDATE input SET answer = (SELECT group_concat(text, char(10)) FROM output WHERE run = NEW.run) WHERE id = NEW.run AND EXISTS (SELECT 1 FROM output WHERE run = NEW.run);
END;

-- build: the second BUILD of a pair landed. The words between the two BUILDs are read back (var cells filled) and handed to mother; her answer is the run's output
CREATE TRIGGER build_go INSTEAD OF INSERT ON build BEGIN
  SELECT mother('INSERT INTO output (run, text) VALUES (' || NEW.run || ', ' || quote(mother(t)) || ')') FROM (SELECT (SELECT group_concat(w, '') FROM (
      SELECT CASE WHEN p2 = 'var' AND p1 = ' ' THEN coalesce((SELECT value FROM sheet s WHERE s.name = word AND s.run = NEW.run ORDER BY s.id DESC LIMIT 1), (SELECT value FROM sheet s WHERE s.name = word ORDER BY s.id DESC LIMIT 1), 'var ' || word)
                  WHEN word = 'var' AND n1 = ' ' THEN '' WHEN p1 = 'var' AND word = ' ' THEN '' ELSE word END AS w
      FROM (SELECT e.word, lag(e.word, 1) OVER (ORDER BY r.id) AS p1, lag(e.word, 2) OVER (ORDER BY r.id) AS p2, lead(e.word, 1) OVER (ORDER BY r.id) AS n1, r.id
            FROM receipt r JOIN encoder e ON e.gate = r.gate
            WHERE r.run = NEW.run AND r.gate <> 22
              AND r.id > (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = 22 AND id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = 22))
              AND r.id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = 22)) ORDER BY id)) AS t);
END;

-- born: a gate with no neuron. It writes the cells the born run reads, then fires born's own memory run if one exists
CREATE TRIGGER born_go INSTEAD OF INSERT ON born BEGIN
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.definition' FROM encoder WHERE gate = NEW.gate;
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.memory' FROM encoder WHERE gate = NEW.gate;
  INSERT INTO sheet (run, name, value) VALUES
    (NEW.run, 'gate', NEW.gate), (NEW.run, 'dna', 'g' || NEW.gate), (NEW.run, 'trig', 't' || NEW.gate),
    (NEW.run, 'defgate', (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.definition')),
    (NEW.run, 'def', 'g' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.definition')),
    (NEW.run, 'mem', 'g' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.memory'));
  SELECT mother('INSERT INTO fire (run, target, gate) SELECT ' || NEW.run || ', 10, ' || NEW.gate || ' WHERE EXISTS (SELECT 1 FROM g12)');
END;

-- fire: a DNA row's trigger column named a neuron. The cells at/before/after say which row fired; the newest run in that neuron's memory node is typed again as a sub-run of this run
CREATE TRIGGER fire_go INSTEAD OF INSERT ON fire BEGIN
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'at', word FROM encoder WHERE gate = NEW.gate;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'before', word FROM encoder WHERE gate = NEW.arrival;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'after', word FROM encoder WHERE gate = NEW.remainder;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'next', word FROM encoder WHERE gate = CASE WHEN NEW.remainder IS NOT 118 THEN NEW.remainder ELSE CAST(substr(NEW.rest || ' ', 1, instr(NEW.rest || ' ', ' ') - 1) AS INTEGER) END;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'prev', e.word FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run AND r.gate NOT IN (118, NEW.gate, 1) ORDER BY r.id DESC LIMIT 1;
  SELECT mother('INSERT INTO input (text, parent) SELECT (SELECT group_concat(w, '''') FROM (SELECT e.word AS w FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.shard IS NOT NULL AND r.gate NOT IN (1, 4, 16) AND r.run = (SELECT run FROM g'
    || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.target) || '.memory')
    || ' ORDER BY id DESC LIMIT 1) ORDER BY r.id)), ' || NEW.run || ' WHERE EXISTS (SELECT 1 FROM g' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.target) || '.memory') || ')', NEW.run);
END;

-- the ear: a typed line is encoded to gates (a word is a run of letters and _; every digit and every other character, space included, is its own neuron); new words get a gate; the run starts by hopping from heard to the first word
CREATE TRIGGER ear AFTER INSERT ON input BEGIN
  INSERT OR IGNORE INTO encoder (word)
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c))
    SELECT group_concat(ch, '') FROM t GROUP BY tok;
  UPDATE input SET gates = (
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c)),
    w AS (SELECT tok, group_concat(ch, '') AS word FROM t GROUP BY tok)
    SELECT group_concat(gate, ' ') FROM (SELECT e.gate FROM w JOIN encoder e ON e.word = w.word ORDER BY w.tok)) WHERE id = NEW.id;
  INSERT INTO sheet (run, name, value) VALUES (NEW.id, 'run', NEW.id);
  INSERT INTO receipt (run, gate, shard) VALUES (NEW.id, 1, NULL);
  INSERT INTO hop (run, gate, arrival, remainder, rest)
    SELECT NEW.id, 1, NULL, CAST(substr(gates || ' ', 1, instr(gates || ' ', ' ') - 1) AS INTEGER), nullif(trim(substr(gates || ' ', instr(gates || ' ', ' ') + 1)), '') FROM input WHERE id = NEW.id;
END;
