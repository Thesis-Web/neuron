PRAGMA recursive_triggers = ON;

CREATE TABLE event (id INTEGER PRIMARY KEY, kind TEXT, gate TEXT, run INTEGER, rowgate TEXT, text TEXT, roots TEXT, a TEXT, b TEXT);

CREATE TABLE encoder (gate INTEGER PRIMARY KEY, word TEXT UNIQUE COLLATE NOCASE, role TEXT, born INTEGER, sourced INTEGER DEFAULT 0);

CREATE TABLE input (id INTEGER PRIMARY KEY, line TEXT, direction TEXT DEFAULT 'heard', parent INTEGER, kind TEXT DEFAULT 'line', subject TEXT, word TEXT, fgate INTEGER, fshard INTEGER, rest TEXT, before TEXT);

CREATE TABLE run (id INTEGER PRIMARY KEY, input INTEGER, line TEXT, gates TEXT DEFAULT '', direction TEXT, expected TEXT, parent INTEGER, root INTEGER, kind TEXT, subject TEXT, word TEXT, fgate INTEGER, fshard INTEGER, output TEXT, mark TEXT, memid INTEGER, reopen INTEGER DEFAULT 0, recalled INTEGER DEFAULT 0, failed INTEGER DEFAULT 0, build INTEGER DEFAULT 0, t0 INTEGER, t1 INTEGER);

CREATE TABLE encode (id INTEGER PRIMARY KEY, run INTEGER, text TEXT);

CREATE TABLE decide (id INTEGER PRIMARY KEY, run INTEGER);

CREATE TABLE lay (id INTEGER PRIMARY KEY, gate INTEGER, arrival INTEGER, remainder INTEGER, run INTEGER, rest TEXT, trig INTEGER, shard INTEGER);

CREATE TABLE born (id INTEGER PRIMARY KEY, word TEXT COLLATE NOCASE, run INTEGER, why TEXT);

CREATE TABLE source (id INTEGER PRIMARY KEY, word TEXT COLLATE NOCASE, run INTEGER);

CREATE TABLE agree (id INTEGER PRIMARY KEY, word TEXT COLLATE NOCASE, run INTEGER);

CREATE TABLE "end" (id INTEGER PRIMARY KEY, run INTEGER);

CREATE TABLE sense (id INTEGER PRIMARY KEY, run INTEGER, stmt INTEGER, src TEXT, word TEXT, kept INTEGER, aside INTEGER, total INTEGER, asked TEXT, needed TEXT, wrong TEXT, setaside TEXT, ok INTEGER);

CREATE TABLE memory (id INTEGER PRIMARY KEY, list TEXT, line TEXT, direction TEXT, receipt TEXT, output TEXT, answer TEXT, mark TEXT, times INTEGER DEFAULT 1, first INTEGER, last INTEGER, run INTEGER, ended INTEGER DEFAULT 0, prevgates TEXT);

CREATE TABLE memwrong (id INTEGER PRIMARY KEY, memid INTEGER, run INTEGER, first INTEGER, prevgates TEXT, given TEXT, expected TEXT);

CREATE TABLE timeline (id INTEGER PRIMARY KEY, t INTEGER, mem INTEGER, run INTEGER);

CREATE TABLE say (id INTEGER PRIMARY KEY, run INTEGER, text TEXT);

CREATE TABLE "BUILD" (id INTEGER PRIMARY KEY, run INTEGER, text TEXT);

CREATE TABLE formula (id INTEGER PRIMARY KEY, word TEXT COLLATE NOCASE, run INTEGER, origin TEXT DEFAULT 'told', t INTEGER, ended INTEGER DEFAULT 0);

CREATE TABLE var (id INTEGER PRIMARY KEY, run INTEGER, name TEXT, value TEXT, src TEXT, t INTEGER, sense INTEGER);

CREATE TABLE state (id INTEGER PRIMARY KEY, key TEXT, value TEXT, t INTEGER);

CREATE TABLE receipt (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER);

CREATE TABLE fire (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER, trig INTEGER, rest TEXT, subject TEXT, word TEXT);

CREATE TABLE stmt (id INTEGER PRIMARY KEY, run INTEGER, text TEXT);

CREATE TABLE secondary (id INTEGER PRIMARY KEY, run INTEGER, stmt INTEGER, src TEXT, word TEXT, hw TEXT, value TEXT, words TEXT, cols TEXT, n INTEGER, err TEXT, changes INTEGER, waiting INTEGER DEFAULT 0, last INTEGER DEFAULT 0);

CREATE TABLE output (id INTEGER PRIMARY KEY, run INTEGER, text TEXT);

CREATE TABLE envelope (id INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, run INTEGER, rest TEXT);

CREATE TABLE gap (id INTEGER PRIMARY KEY, run INTEGER, need TEXT, fill TEXT, who TEXT, word TEXT COLLATE NOCASE, kind TEXT);

CREATE TABLE relation (id INTEGER PRIMARY KEY, a TEXT COLLATE NOCASE, rel TEXT, b TEXT COLLATE NOCASE, trust REAL DEFAULT 0.6);

CREATE TABLE definition (id INTEGER PRIMARY KEY, word TEXT COLLATE NOCASE, src TEXT, hw TEXT, text TEXT, words TEXT);

CREATE TABLE defword (id INTEGER PRIMARY KEY, def INTEGER, word TEXT COLLATE NOCASE, src TEXT, w TEXT COLLATE NOCASE, rest TEXT);

CREATE TABLE need (w TEXT PRIMARY KEY COLLATE NOCASE, n INTEGER);

CREATE TABLE proc (word TEXT PRIMARY KEY COLLATE NOCASE, status TEXT, uses INTEGER DEFAULT 0, right INTEGER DEFAULT 0, wrong INTEGER DEFAULT 0);

CREATE TABLE procrun (id INTEGER PRIMARY KEY, word TEXT COLLATE NOCASE, receipt TEXT);

CREATE TABLE place (id INTEGER PRIMARY KEY, word TEXT COLLATE NOCASE, x REAL, y REAL, z REAL, t INTEGER, ended INTEGER DEFAULT 0);

INSERT INTO encoder (gate, word, role, born) VALUES (1, 'input', 'physics', 0);

CREATE TABLE g1 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_1 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g1;

CREATE TRIGGER miss_1 INSTEAD OF INSERT ON land_1 WHEN NOT EXISTS (SELECT 1 FROM g1 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (1, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (2, 'encoder', 'physics', 0);

CREATE TABLE g2 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_2 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g2;

CREATE TRIGGER miss_2 INSTEAD OF INSERT ON land_2 WHEN NOT EXISTS (SELECT 1 FROM g2 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (2, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (3, 'decide', 'physics', 0);

CREATE TABLE g3 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_3 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g3;

CREATE TRIGGER miss_3 INSTEAD OF INSERT ON land_3 WHEN NOT EXISTS (SELECT 1 FROM g3 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (3, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (4, 'lay', 'physics', 0);

CREATE TABLE g4 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_4 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g4;

CREATE TRIGGER miss_4 INSTEAD OF INSERT ON land_4 WHEN NOT EXISTS (SELECT 1 FROM g4 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (4, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (5, 'born', 'physics', 0);

CREATE TABLE g5 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_5 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g5;

CREATE TRIGGER miss_5 INSTEAD OF INSERT ON land_5 WHEN NOT EXISTS (SELECT 1 FROM g5 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (5, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (6, 'source', 'physics', 0);

CREATE TABLE g6 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_6 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g6;

CREATE TRIGGER miss_6 INSTEAD OF INSERT ON land_6 WHEN NOT EXISTS (SELECT 1 FROM g6 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (6, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (7, 'agree', 'physics', 0);

CREATE TABLE g7 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_7 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g7;

CREATE TRIGGER miss_7 INSTEAD OF INSERT ON land_7 WHEN NOT EXISTS (SELECT 1 FROM g7 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (7, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (8, 'end', 'physics', 0);

CREATE TABLE g8 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_8 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g8;

CREATE TRIGGER miss_8 INSTEAD OF INSERT ON land_8 WHEN NOT EXISTS (SELECT 1 FROM g8 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (8, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (9, 'sense', 'physics', 0);

CREATE TABLE g9 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_9 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g9;

CREATE TRIGGER miss_9 INSTEAD OF INSERT ON land_9 WHEN NOT EXISTS (SELECT 1 FROM g9 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (9, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (10, 'memory', 'physics', 0);

CREATE TABLE g10 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_10 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g10;

CREATE TRIGGER miss_10 INSTEAD OF INSERT ON land_10 WHEN NOT EXISTS (SELECT 1 FROM g10 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (10, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (11, 'timeline', 'physics', 0);

CREATE TABLE g11 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_11 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g11;

CREATE TRIGGER miss_11 INSTEAD OF INSERT ON land_11 WHEN NOT EXISTS (SELECT 1 FROM g11 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (11, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (12, 'say', 'physics', 0);

CREATE TABLE g12 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_12 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g12;

CREATE TRIGGER miss_12 INSTEAD OF INSERT ON land_12 WHEN NOT EXISTS (SELECT 1 FROM g12 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (12, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (13, 'BUILD', 'physics', 0);

CREATE TABLE g13 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_13 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g13;

CREATE TRIGGER miss_13 INSTEAD OF INSERT ON land_13 WHEN NOT EXISTS (SELECT 1 FROM g13 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (13, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (14, 'formula', 'physics', 0);

CREATE TABLE g14 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_14 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g14;

CREATE TRIGGER miss_14 INSTEAD OF INSERT ON land_14 WHEN NOT EXISTS (SELECT 1 FROM g14 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (14, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (15, 'var', 'physics', 0);

CREATE TABLE g15 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_15 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g15;

CREATE TRIGGER miss_15 INSTEAD OF INSERT ON land_15 WHEN NOT EXISTS (SELECT 1 FROM g15 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (15, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (16, 'state', 'physics', 0);

CREATE TABLE g16 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_16 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g16;

CREATE TRIGGER miss_16 INSTEAD OF INSERT ON land_16 WHEN NOT EXISTS (SELECT 1 FROM g16 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (16, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (17, 'READ', 'root', 0);

CREATE TABLE g17 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_17 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g17;

CREATE TRIGGER miss_17 INSTEAD OF INSERT ON land_17 WHEN NOT EXISTS (SELECT 1 FROM g17 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (17, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (18, 'WRITE', 'root', 0);

CREATE TABLE g18 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_18 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g18;

CREATE TRIGGER miss_18 INSTEAD OF INSERT ON land_18 WHEN NOT EXISTS (SELECT 1 FROM g18 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (18, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (19, 'COMPARE', 'root', 0);

CREATE TABLE g19 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_19 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g19;

CREATE TRIGGER miss_19 INSTEAD OF INSERT ON land_19 WHEN NOT EXISTS (SELECT 1 FROM g19 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (19, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (20, 'ADD', 'root', 0);

CREATE TABLE g20 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_20 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g20;

CREATE TRIGGER miss_20 INSTEAD OF INSERT ON land_20 WHEN NOT EXISTS (SELECT 1 FROM g20 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (20, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (21, 'SUBTRACT', 'root', 0);

CREATE TABLE g21 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_21 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g21;

CREATE TRIGGER miss_21 INSTEAD OF INSERT ON land_21 WHEN NOT EXISTS (SELECT 1 FROM g21 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (21, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (22, 'MOVE', 'root', 0);

CREATE TABLE g22 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_22 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g22;

CREATE TRIGGER miss_22 INSTEAD OF INSERT ON land_22 WHEN NOT EXISTS (SELECT 1 FROM g22 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (22, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (23, 'FIND', 'root', 0);

CREATE TABLE g23 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_23 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g23;

CREATE TRIGGER miss_23 INSTEAD OF INSERT ON land_23 WHEN NOT EXISTS (SELECT 1 FROM g23 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (23, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (24, 'SPLIT', 'root', 0);

CREATE TABLE g24 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_24 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g24;

CREATE TRIGGER miss_24 INSTEAD OF INSERT ON land_24 WHEN NOT EXISTS (SELECT 1 FROM g24 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (24, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (25, 'JOIN', 'root', 0);

CREATE TABLE g25 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_25 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g25;

CREATE TRIGGER miss_25 INSTEAD OF INSERT ON land_25 WHEN NOT EXISTS (SELECT 1 FROM g25 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (25, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (26, 'CLOCK', 'root', 0);

CREATE TABLE g26 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_26 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g26;

CREATE TRIGGER miss_26 INSTEAD OF INSERT ON land_26 WHEN NOT EXISTS (SELECT 1 FROM g26 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (26, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (27, 'HEAR', 'root', 0);

CREATE TABLE g27 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_27 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g27;

CREATE TRIGGER miss_27 INSTEAD OF INSERT ON land_27 WHEN NOT EXISTS (SELECT 1 FROM g27 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (27, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (28, 'CALL', 'root', 0);

CREATE TABLE g28 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_28 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g28;

CREATE TRIGGER miss_28 INSTEAD OF INSERT ON land_28 WHEN NOT EXISTS (SELECT 1 FROM g28 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (28, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (29, 'SPAWN', 'root', 0);

CREATE TABLE g29 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_29 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g29;

CREATE TRIGGER miss_29 INSTEAD OF INSERT ON land_29 WHEN NOT EXISTS (SELECT 1 FROM g29 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (29, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (30, 'SELECT', 'sqlroot', 0);

CREATE TABLE g30 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_30 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g30;

CREATE TRIGGER miss_30 INSTEAD OF INSERT ON land_30 WHEN NOT EXISTS (SELECT 1 FROM g30 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (30, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (31, 'FROM', 'sqlroot', 0);

CREATE TABLE g31 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_31 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g31;

CREATE TRIGGER miss_31 INSTEAD OF INSERT ON land_31 WHEN NOT EXISTS (SELECT 1 FROM g31 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (31, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (32, 'WHERE', 'sqlroot', 0);

CREATE TABLE g32 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_32 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g32;

CREATE TRIGGER miss_32 INSTEAD OF INSERT ON land_32 WHEN NOT EXISTS (SELECT 1 FROM g32 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (32, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (33, 'INSERT', 'sqlroot', 0);

CREATE TABLE g33 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_33 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g33;

CREATE TRIGGER miss_33 INSTEAD OF INSERT ON land_33 WHEN NOT EXISTS (SELECT 1 FROM g33 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (33, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (34, 'INTO', 'sqlroot', 0);

CREATE TABLE g34 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_34 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g34;

CREATE TRIGGER miss_34 INSTEAD OF INSERT ON land_34 WHEN NOT EXISTS (SELECT 1 FROM g34 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (34, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (35, 'VALUES', 'sqlroot', 0);

CREATE TABLE g35 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_35 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g35;

CREATE TRIGGER miss_35 INSTEAD OF INSERT ON land_35 WHEN NOT EXISTS (SELECT 1 FROM g35 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (35, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (36, 'UPDATE', 'sqlroot', 0);

CREATE TABLE g36 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_36 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g36;

CREATE TRIGGER miss_36 INSTEAD OF INSERT ON land_36 WHEN NOT EXISTS (SELECT 1 FROM g36 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (36, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (37, 'SET', 'sqlroot', 0);

CREATE TABLE g37 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_37 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g37;

CREATE TRIGGER miss_37 INSTEAD OF INSERT ON land_37 WHEN NOT EXISTS (SELECT 1 FROM g37 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (37, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (38, 'DELETE', 'sqlroot', 0);

CREATE TABLE g38 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_38 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g38;

CREATE TRIGGER miss_38 INSTEAD OF INSERT ON land_38 WHEN NOT EXISTS (SELECT 1 FROM g38 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (38, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (39, 'CREATE', 'sqlroot', 0);

CREATE TABLE g39 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_39 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g39;

CREATE TRIGGER miss_39 INSTEAD OF INSERT ON land_39 WHEN NOT EXISTS (SELECT 1 FROM g39 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (39, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (40, 'TABLE', 'sqlroot', 0);

CREATE TABLE g40 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_40 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g40;

CREATE TRIGGER miss_40 INSTEAD OF INSERT ON land_40 WHEN NOT EXISTS (SELECT 1 FROM g40 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (40, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (41, 'AS', 'sqlroot', 0);

CREATE TABLE g41 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_41 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g41;

CREATE TRIGGER miss_41 INSTEAD OF INSERT ON land_41 WHEN NOT EXISTS (SELECT 1 FROM g41 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (41, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (42, 'AND', 'sqlroot', 0);

CREATE TABLE g42 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_42 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g42;

CREATE TRIGGER miss_42 INSTEAD OF INSERT ON land_42 WHEN NOT EXISTS (SELECT 1 FROM g42 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (42, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (43, 'OR', 'sqlroot', 0);

CREATE TABLE g43 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_43 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g43;

CREATE TRIGGER miss_43 INSTEAD OF INSERT ON land_43 WHEN NOT EXISTS (SELECT 1 FROM g43 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (43, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (44, 'NOT', 'sqlroot', 0);

CREATE TABLE g44 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_44 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g44;

CREATE TRIGGER miss_44 INSTEAD OF INSERT ON land_44 WHEN NOT EXISTS (SELECT 1 FROM g44 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (44, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (45, 'IN', 'sqlroot', 0);

CREATE TABLE g45 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_45 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g45;

CREATE TRIGGER miss_45 INSTEAD OF INSERT ON land_45 WHEN NOT EXISTS (SELECT 1 FROM g45 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (45, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (46, 'LIKE', 'sqlroot', 0);

CREATE TABLE g46 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_46 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g46;

CREATE TRIGGER miss_46 INSTEAD OF INSERT ON land_46 WHEN NOT EXISTS (SELECT 1 FROM g46 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (46, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (47, 'EXISTS', 'sqlroot', 0);

CREATE TABLE g47 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_47 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g47;

CREATE TRIGGER miss_47 INSTEAD OF INSERT ON land_47 WHEN NOT EXISTS (SELECT 1 FROM g47 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (47, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (48, 'LIMIT', 'sqlroot', 0);

CREATE TABLE g48 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_48 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g48;

CREATE TRIGGER miss_48 INSTEAD OF INSERT ON land_48 WHEN NOT EXISTS (SELECT 1 FROM g48 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (48, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (49, 'ORDER', 'sqlroot', 0);

CREATE TABLE g49 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_49 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g49;

CREATE TRIGGER miss_49 INSTEAD OF INSERT ON land_49 WHEN NOT EXISTS (SELECT 1 FROM g49 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (49, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (50, 'BY', 'sqlroot', 0);

CREATE TABLE g50 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_50 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g50;

CREATE TRIGGER miss_50 INSTEAD OF INSERT ON land_50 WHEN NOT EXISTS (SELECT 1 FROM g50 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (50, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (51, 'NULL', 'sqlroot', 0);

CREATE TABLE g51 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_51 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g51;

CREATE TRIGGER miss_51 INSTEAD OF INSERT ON land_51 WHEN NOT EXISTS (SELECT 1 FROM g51 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (51, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (52, 'CAST', 'sqlroot', 0);

CREATE TABLE g52 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_52 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g52;

CREATE TRIGGER miss_52 INSTEAD OF INSERT ON land_52 WHEN NOT EXISTS (SELECT 1 FROM g52 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (52, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (53, 'INTEGER', 'sqlroot', 0);

CREATE TABLE g53 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_53 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g53;

CREATE TRIGGER miss_53 INSTEAD OF INSERT ON land_53 WHEN NOT EXISTS (SELECT 1 FROM g53 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (53, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (54, 'WITH', 'sqlroot', 0);

CREATE TABLE g54 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_54 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g54;

CREATE TRIGGER miss_54 INSTEAD OF INSERT ON land_54 WHEN NOT EXISTS (SELECT 1 FROM g54 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (54, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (55, 'instr', 'sqlroot', 0);

CREATE TABLE g55 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_55 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g55;

CREATE TRIGGER miss_55 INSTEAD OF INSERT ON land_55 WHEN NOT EXISTS (SELECT 1 FROM g55 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (55, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (56, 'count', 'sqlroot', 0);

CREATE TABLE g56 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_56 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g56;

CREATE TRIGGER miss_56 INSTEAD OF INSERT ON land_56 WHEN NOT EXISTS (SELECT 1 FROM g56 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (56, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (57, 'max', 'sqlroot', 0);

CREATE TABLE g57 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_57 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g57;

CREATE TRIGGER miss_57 INSTEAD OF INSERT ON land_57 WHEN NOT EXISTS (SELECT 1 FROM g57 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (57, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (58, 'group_concat', 'sqlroot', 0);

CREATE TABLE g58 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_58 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g58;

CREATE TRIGGER miss_58 INSTEAD OF INSERT ON land_58 WHEN NOT EXISTS (SELECT 1 FROM g58 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (58, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (59, 'IS', 'sqlroot', 0);

CREATE TABLE g59 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_59 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g59;

CREATE TRIGGER miss_59 INSTEAD OF INSERT ON land_59 WHEN NOT EXISTS (SELECT 1 FROM g59 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (59, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (60, 'DESC', 'sqlroot', 0);

CREATE TABLE g60 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_60 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g60;

CREATE TRIGGER miss_60 INSTEAD OF INSERT ON land_60 WHEN NOT EXISTS (SELECT 1 FROM g60 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (60, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (61, '=', 'sqlroot', 0);

CREATE TABLE g61 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_61 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g61;

CREATE TRIGGER miss_61 INSTEAD OF INSERT ON land_61 WHEN NOT EXISTS (SELECT 1 FROM g61 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (61, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (62, '(', 'sqlroot', 0);

CREATE TABLE g62 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_62 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g62;

CREATE TRIGGER miss_62 INSTEAD OF INSERT ON land_62 WHEN NOT EXISTS (SELECT 1 FROM g62 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (62, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (63, ')', 'sqlroot', 0);

CREATE TABLE g63 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_63 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g63;

CREATE TRIGGER miss_63 INSTEAD OF INSERT ON land_63 WHEN NOT EXISTS (SELECT 1 FROM g63 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (63, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (64, ',', 'sqlroot', 0);

CREATE TABLE g64 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_64 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g64;

CREATE TRIGGER miss_64 INSTEAD OF INSERT ON land_64 WHEN NOT EXISTS (SELECT 1 FROM g64 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (64, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (65, ';', 'sqlroot', 0);

CREATE TABLE g65 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_65 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g65;

CREATE TRIGGER miss_65 INSTEAD OF INSERT ON land_65 WHEN NOT EXISTS (SELECT 1 FROM g65 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (65, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (66, '*', 'sqlroot', 0);

CREATE TABLE g66 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_66 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g66;

CREATE TRIGGER miss_66 INSTEAD OF INSERT ON land_66 WHEN NOT EXISTS (SELECT 1 FROM g66 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (66, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (67, '>', 'sqlroot', 0);

CREATE TABLE g67 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_67 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g67;

CREATE TRIGGER miss_67 INSTEAD OF INSERT ON land_67 WHEN NOT EXISTS (SELECT 1 FROM g67 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (67, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (68, '<', 'sqlroot', 0);

CREATE TABLE g68 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_68 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g68;

CREATE TRIGGER miss_68 INSTEAD OF INSERT ON land_68 WHEN NOT EXISTS (SELECT 1 FROM g68 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (68, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (69, '||', 'sqlroot', 0);

CREATE TABLE g69 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_69 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g69;

CREATE TRIGGER miss_69 INSTEAD OF INSERT ON land_69 WHEN NOT EXISTS (SELECT 1 FROM g69 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (69, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (70, 'heard', 'arrival', 0);

CREATE TABLE g70 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_70 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g70;

CREATE TRIGGER miss_70 INSTEAD OF INSERT ON land_70 WHEN NOT EXISTS (SELECT 1 FROM g70 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (70, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (71, 'said', 'arrival', 0);

CREATE TABLE g71 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_71 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g71;

CREATE TRIGGER miss_71 INSTEAD OF INSERT ON land_71 WHEN NOT EXISTS (SELECT 1 FROM g71 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (71, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (72, 'start', 'arrival', 0);

CREATE TABLE g72 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_72 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g72;

CREATE TRIGGER miss_72 INSTEAD OF INSERT ON land_72 WHEN NOT EXISTS (SELECT 1 FROM g72 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (72, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (73, 'origin', 'word', 0);

CREATE TABLE g73 (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER);

CREATE VIEW land_73 AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g73;

CREATE TRIGGER miss_73 INSTEAD OF INSERT ON land_73 WHEN NOT EXISTS (SELECT 1 FROM g73 WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (73, NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END;

INSERT INTO encoder (gate, word, role, born) VALUES (74, 'output to sources', 'port', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (75, 'secondary input', 'port', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (76, 'OUTPUT', 'port', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (77, 'mother', 'port', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (78, 'SQL prompt', 'port', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (79, 'wn', 'sat', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (80, 'gcide', 'sat', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (81, 'mw', 'sat', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (82, 'mwt', 'sat', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (83, 'moby', 'sat', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (84, 'map', 'sat', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (85, 'sqldoc', 'sat', 0);

INSERT INTO encoder (gate, word, role, born) VALUES (86, 'measured', 'sat', 0);

CREATE TRIGGER input_teach AFTER INSERT ON input WHEN NEW.kind = 'line' AND instr(NEW.line, ' = ') > 1 AND instr(NEW.line, '=>') = 0 AND instr(substr(NEW.line, 1, instr(NEW.line, ' = ') - 1), ' ') = 0 AND NEW.line NOT LIKE 'BUILD %' BEGIN
      INSERT INTO born (word, run, why) SELECT substr(NEW.line, 1, instr(NEW.line, ' = ') - 1), NULL, 'a word given a formula'
        WHERE NOT EXISTS (SELECT 1 FROM encoder WHERE word = substr(NEW.line, 1, instr(NEW.line, ' = ') - 1));
      INSERT INTO run (input, line, kind, word, t0, direction) VALUES (NEW.id, trim(substr(NEW.line, instr(NEW.line, ' = ') + 3)), 'teach', substr(NEW.line, 1, instr(NEW.line, ' = ') - 1), (SELECT coalesce(max(id), 0) FROM event), 'start');
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('input', 'input', (SELECT max(id) FROM run), 'input', 'primary input: "' || NEW.line || '": a told line. Its words run through the neurons from start; when the run ends, the formula row points at that run.', 'HEAR WRITE', NULL, NULL);
    END;

CREATE TRIGGER input_bind AFTER INSERT ON input WHEN NEW.kind = 'line' AND instr(NEW.line, ' -> ') > 0 BEGIN
      INSERT INTO bindq (words, f, input) VALUES (trim(substr(NEW.line, 1, instr(NEW.line, ' -> ') - 1)), trim(substr(NEW.line, instr(NEW.line, ' -> ') + 4)), NEW.id);
      INSERT INTO run (input, line, kind, t0, direction) VALUES (NEW.id, replace(NEW.line, ' -> ', ' '), 'bind', (SELECT coalesce(max(id), 0) FROM event), 'heard');
    END;

CREATE TRIGGER input_run AFTER INSERT ON input WHEN NOT (NEW.kind = 'line' AND instr(NEW.line, ' = ') > 1 AND instr(NEW.line, '=>') = 0 AND instr(substr(NEW.line, 1, instr(NEW.line, ' = ') - 1), ' ') = 0 AND NEW.line NOT LIKE 'BUILD %') AND NOT (NEW.kind = 'line' AND instr(NEW.line, ' -> ') > 0) BEGIN
      INSERT INTO run (input, line, expected, direction, parent, kind, subject, word, fgate, fshard, t0, build)
        VALUES (NEW.id, trim(CASE WHEN instr(NEW.line, ' => ') > 0 THEN substr(NEW.line, 1, instr(NEW.line, ' => ') - 1) ELSE NEW.line END),
                CASE WHEN instr(NEW.line, ' => ') > 0 THEN trim(substr(NEW.line, instr(NEW.line, ' => ') + 4)) END,
                NEW.direction, NEW.parent, NEW.kind, NEW.subject, NEW.word, NEW.fgate, NEW.fshard, (SELECT coalesce(max(id), 0) FROM event), (NEW.line LIKE 'BUILD % BUILD'));
    END;

CREATE TABLE bindq (id INTEGER PRIMARY KEY, words TEXT, f TEXT, input INTEGER);

CREATE TRIGGER run_go AFTER INSERT ON run BEGIN
      UPDATE run SET root = CASE WHEN NEW.kind = 'defrow' THEN NEW.id ELSE coalesce((SELECT root FROM run WHERE id = NEW.parent), NEW.id) END WHERE id = NEW.id;
      INSERT INTO var (run, name, value, src, t) SELECT NEW.id, ':head', (SELECT word FROM encoder WHERE gate = NEW.fgate), 'the run', (SELECT coalesce(max(id), 0) FROM event) WHERE NEW.kind = 'formula';
      INSERT INTO var (run, name, value, src, t) SELECT NEW.id, ':after', (SELECT rest FROM input WHERE id = NEW.input), 'the run', (SELECT coalesce(max(id), 0) FROM event) WHERE NEW.kind = 'formula';
      INSERT INTO var (run, name, value, src, t) SELECT NEW.id, ':before', (SELECT before FROM input WHERE id = NEW.input), 'the run', (SELECT coalesce(max(id), 0) FROM event) WHERE NEW.kind = 'formula';
      INSERT INTO var (run, name, value, src, t) SELECT NEW.id, ':subject', NEW.subject, 'the run', (SELECT coalesce(max(id), 0) FROM event) WHERE NEW.kind = 'formula' AND NEW.subject IS NOT NULL;
      INSERT INTO var (run, name, value, src, t) SELECT NEW.id, ':line', (SELECT line FROM run WHERE id = (SELECT root FROM run WHERE id = NEW.id)), 'the run', (SELECT coalesce(max(id), 0) FROM event) WHERE NEW.kind = 'formula';
      INSERT INTO var (run, name, value, src, t) SELECT NEW.id, ':run', (SELECT root FROM run WHERE id = NEW.id), 'the run', (SELECT coalesce(max(id), 0) FROM event) WHERE NEW.kind = 'formula';
      INSERT INTO var (run, name, value, src, t) SELECT NEW.id, ':prev', (SELECT max(id) FROM run WHERE kind = 'line' AND id < (SELECT root FROM run WHERE id = NEW.id)), 'the run', (SELECT coalesce(max(id), 0) FROM event) WHERE NEW.kind = 'formula';
      INSERT INTO var (run, name, value, src, t) SELECT NEW.id, ':speaker', CASE (SELECT direction FROM run WHERE id = (SELECT root FROM run WHERE id = NEW.id)) WHEN 'said' THEN 'self' ELSE 'user' END, 'the run', (SELECT coalesce(max(id), 0) FROM event) WHERE NEW.kind = 'formula';
      INSERT INTO encode (run, text) VALUES (NEW.id, NEW.line);
    END;

CREATE TRIGGER run_said AFTER UPDATE OF root ON run WHEN OLD.root IS NULL BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('input', CASE WHEN NEW.kind = 'formula' THEN NEW.word ELSE 'input' END, NEW.id, CASE WHEN NEW.kind IN ('line', 'teach', 'bind') THEN 'input' ELSE NULL END, CASE NEW.kind WHEN 'line' THEN (CASE NEW.direction WHEN 'said' THEN 'said back: "' || NEW.line || '": the brain''s own words fed to its ear; the first row arrives from said' ELSE 'primary input: "' || NEW.line || '"' || coalesce(' with expected output "' || NEW.expected || '"', '') || '. The first row arrives from heard.' END) WHEN 'formula' THEN NEW.word || ' fires: its formula runs as a branch of run ' || NEW.parent || ': ' || NEW.line WHEN 'defrow' THEN 'a definition row of ' || NEW.subject || ' runs like any line, with ' || NEW.subject || ' as its subject: ' || NEW.line WHEN 'teach' THEN 'the words of a told line get their gates' ELSE NEW.line END, 'HEAR WRITE', NULL, NULL);
    END;

CREATE TRIGGER encode_word AFTER INSERT ON encode WHEN trim(NEW.text) <> '' BEGIN
      INSERT INTO born (word, run, why) SELECT substr(trim(NEW.text) || ' ', 1, instr(trim(NEW.text) || ' ', ' ') - 1), NEW.run, CASE (SELECT kind FROM run WHERE id = NEW.run) WHEN 'line' THEN NULL WHEN 'defrow' THEN 'named in a definition row of ' || (SELECT subject FROM run WHERE id = NEW.run) || '; not looked up until a line needs it' ELSE 'a word in a formula' END
        WHERE NOT EXISTS (SELECT 1 FROM encoder WHERE word = substr(trim(NEW.text) || ' ', 1, instr(trim(NEW.text) || ' ', ' ') - 1));
      INSERT INTO source (word, run) SELECT substr(trim(NEW.text) || ' ', 1, instr(trim(NEW.text) || ' ', ' ') - 1), NEW.run FROM encoder e WHERE e.word = substr(trim(NEW.text) || ' ', 1, instr(trim(NEW.text) || ' ', ' ') - 1) AND e.role IN ('word', 'sqlroot', 'root', 'physics') AND e.sourced = 0 AND (SELECT kind FROM run WHERE id = NEW.run) = 'line' AND NOT EXISTS (SELECT 1 FROM formula WHERE word = substr(trim(NEW.text) || ' ', 1, instr(trim(NEW.text) || ' ', ' ') - 1) AND ended = 0) AND (SELECT build FROM run WHERE id = NEW.run) = 0;
      UPDATE run SET gates = trim(gates || ' ' || (SELECT gate FROM encoder WHERE word = substr(trim(NEW.text) || ' ', 1, instr(trim(NEW.text) || ' ', ' ') - 1))) WHERE id = NEW.run;
      INSERT INTO encode (run, text) VALUES (NEW.run, trim(substr(trim(NEW.text) || ' ', instr(trim(NEW.text) || ' ', ' ') + 1)));
    END;

CREATE TRIGGER encode_done AFTER INSERT ON encode WHEN trim(NEW.text) = '' BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('encode', 'encoder', NEW.run, 'encoder', 'encoder: ' || (SELECT line FROM run WHERE id = NEW.run) || ' = gates ' || (SELECT gates FROM run WHERE id = NEW.run), 'READ FIND', NULL, NULL);
      INSERT INTO decide (run) SELECT NEW.run WHERE (SELECT kind FROM run WHERE id = NEW.run) <> 'bind';
      INSERT INTO bindgo (run) SELECT NEW.run WHERE (SELECT kind FROM run WHERE id = NEW.run) = 'bind' AND EXISTS (SELECT 1 FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run));
    END;

CREATE TRIGGER born_go AFTER INSERT ON born BEGIN
      INSERT INTO encoder (word, role, born) VALUES (NEW.word, CASE WHEN NEW.word LIKE ':%' THEN 'var' WHEN NEW.word GLOB '[0-9]*' OR NEW.word LIKE '''%' OR NEW.word LIKE '%''' THEN 'literal' ELSE 'word' END, (SELECT coalesce(max(id), 0) FROM event));
      SELECT mother('CREATE TABLE g' || (SELECT gate FROM encoder WHERE word = NEW.word) || ' (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER, op TEXT, times INTEGER DEFAULT 0, first INTEGER, last INTEGER)', NULL, NULL);
      SELECT mother('CREATE VIEW land_' || (SELECT gate FROM encoder WHERE word = NEW.word) || ' AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g' || (SELECT gate FROM encoder WHERE word = NEW.word), NULL, NULL);
      SELECT mother('CREATE TRIGGER miss_' || (SELECT gate FROM encoder WHERE word = NEW.word) || ' INSTEAD OF INSERT ON land_' || (SELECT gate FROM encoder WHERE word = NEW.word) || ' WHEN NOT EXISTS (SELECT 1 FROM g' || (SELECT gate FROM encoder WHERE word = NEW.word) || ' WHERE arrival = NEW.arrival AND remainder IS NEW.remainder) BEGIN INSERT INTO lay (gate, arrival, remainder, run, rest) VALUES (' || (SELECT gate FROM encoder WHERE word = NEW.word) || ', NEW.arrival, NEW.remainder, NEW.run, NEW.rest); END', NULL, NULL);
      INSERT INTO definition (word, src) VALUES (NEW.word, 'node');
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('born', NEW.word, NEW.run, 'mother', 'born ' || NEW.word || ' (gate ' || (SELECT gate FROM encoder WHERE word = NEW.word) || '): mother makes its table, its gate and its trigger, and a blank definition node' || coalesce('. ' || NEW.why, ''), 'SPAWN WRITE CALL', NULL, NULL);
      INSERT INTO source (word, run) SELECT NEW.word, NEW.run WHERE NEW.why IS NULL AND (SELECT role FROM encoder WHERE word = NEW.word) = 'word';
    END;

CREATE TRIGGER decide_go AFTER INSERT ON decide BEGIN
      UPDATE run SET memid = (SELECT m.id FROM memory m WHERE m.list = run.gates AND m.direction = run.direction AND m.ended = 0 ORDER BY m.id DESC LIMIT 1) WHERE id = NEW.run AND kind = 'line' AND build = 0;
      UPDATE run SET reopen = 1 WHERE id = NEW.run AND memid IS NOT NULL AND (SELECT answer FROM memory WHERE id = run.memid) IS NULL AND (SELECT EXISTS (SELECT 1 FROM gap g WHERE g.run = (SELECT run FROM memory WHERE id = r.memid) AND ((g.kind = 'word' AND EXISTS (SELECT 1 FROM formula f WHERE f.word = g.word AND f.ended = 0)) OR (g.kind = 'source' AND EXISTS (SELECT 1 FROM formula f WHERE f.word = 'source' AND f.ended = 0)) OR (g.kind = 'defrows' AND EXISTS (SELECT 1 FROM formula f WHERE f.word IN ('like', 'opposite', 'kind') AND f.ended = 0)))) FROM run r WHERE r.id = NEW.run);
      UPDATE run SET reopen = 1 WHERE id = NEW.run AND memid IS NOT NULL AND reopen = 0 AND EXISTS (SELECT 1 FROM g3 WHERE arrival = CAST(substr(trim(run.gates) || ' ', 1, instr(trim(run.gates) || ' ', ' ') - 1) AS INTEGER) AND trigger = (SELECT gate FROM encoder WHERE word = ':prev')) AND coalesce((SELECT prevgates FROM memory WHERE id = run.memid), '') <> coalesce((SELECT gates FROM run WHERE kind = 'line' AND id < NEW.run ORDER BY id DESC LIMIT 1), '');
      INSERT INTO memhit (run) SELECT NEW.run FROM run WHERE id = NEW.run AND memid IS NOT NULL AND reopen = 0;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) SELECT 'decide', 'decide', NEW.run, 'decide', CASE WHEN (SELECT reopen FROM run WHERE id = NEW.run) = 1 THEN 'decide: this line is in memory, but that memory was written with gaps and something it lacked now exists. It runs again the long way.' ELSE 'decide: not in memory. The line runs from its first word; each landing fires its row.' END, 'FIND COMPARE', NULL, NULL WHERE EXISTS (SELECT 1 FROM run WHERE id = NEW.run AND (memid IS NULL OR reopen = 1));
      INSERT INTO envelope (arrival, remainder, run, rest) SELECT (SELECT gate FROM encoder WHERE word = r.direction), (SELECT gate FROM encoder WHERE word = substr(trim(trim(substr(trim(r.line) || ' ', instr(trim(r.line) || ' ', ' ') + 1))) || ' ', 1, instr(trim(trim(substr(trim(r.line) || ' ', instr(trim(r.line) || ' ', ' ') + 1))) || ' ', ' ') - 1)), r.id, trim(substr(trim(trim(substr(trim(r.line) || ' ', instr(trim(r.line) || ' ', ' ') + 1))) || ' ', instr(trim(trim(substr(trim(r.line) || ' ', instr(trim(r.line) || ' ', ' ') + 1))) || ' ', ' ') + 1)) FROM run r WHERE r.id = NEW.run AND (r.memid IS NULL OR r.reopen = 1);
      SELECT mother('INSERT INTO land_' || (SELECT gate FROM encoder WHERE word = substr(trim(r.line) || ' ', 1, instr(trim(r.line) || ' ', ' ') - 1)) || ' (arrival, remainder, run, rest) SELECT arrival, remainder, run, rest FROM envelope WHERE id = (SELECT max(id) FROM envelope)', NULL, NULL) FROM run r WHERE r.id = NEW.run AND (r.memid IS NULL OR r.reopen = 1);
      DELETE FROM envelope WHERE id = (SELECT max(id) FROM envelope) AND run = NEW.run;
    END;

CREATE TABLE memhit (id INTEGER PRIMARY KEY, run INTEGER);

CREATE TRIGGER memhit_go AFTER INSERT ON memhit BEGIN
      UPDATE memory SET times = times + 1, last = (SELECT coalesce(max(id), 0) FROM event) WHERE id = (SELECT memid FROM run WHERE id = NEW.run);
      INSERT INTO memwrong (memid, run, first, prevgates, given, expected) SELECT r.memid, r.id, CAST(substr(trim(r.gates) || ' ', 1, instr(trim(r.gates) || ' ', ' ') - 1) AS INTEGER), (SELECT gates FROM run WHERE kind = 'line' AND id < r.id ORDER BY id DESC LIMIT 1), (SELECT coalesce(answer, output) FROM memory WHERE id = r.memid), r.expected FROM run r WHERE r.id = NEW.run AND r.expected IS NOT NULL AND r.expected IS NOT (SELECT coalesce(answer, output) FROM memory WHERE id = r.memid);
      UPDATE run SET recalled = 1, output = (SELECT coalesce(answer, output) FROM memory WHERE id = run.memid), t1 = (SELECT coalesce(max(id), 0) FROM event) WHERE id = NEW.run;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('memhit', 'memory', NEW.run, 'memory', 'decide: this line is in memory (receipt ' || (SELECT receipt FROM memory WHERE id = (SELECT memid FROM run WHERE id = NEW.run)) || '). Do I know this? Yes: one hop to it, times ' || (SELECT times FROM memory WHERE id = (SELECT memid FROM run WHERE id = NEW.run)) || '. No rows fire, no lay, no mother.', 'FIND COMPARE WRITE', (SELECT line FROM run WHERE id = NEW.run), (SELECT memid FROM run WHERE id = NEW.run));
      INSERT INTO timeline (t, mem, run) VALUES ((SELECT coalesce(max(id), 0) FROM event), (SELECT memid FROM run WHERE id = NEW.run), NEW.run);
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('timeline', 'timeline', NEW.run, 'timeline', 'timeline: row ' || (SELECT max(id) FROM timeline) || ' (memory ' || (SELECT memid FROM run WHERE id = NEW.run) || ')', 'CLOCK WRITE', NULL, NULL);
      INSERT INTO output (run, text) VALUES (NEW.run, (SELECT output FROM run WHERE id = NEW.run));
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('say', 'say', NEW.run, 'OUTPUT', 'say: ' || coalesce((SELECT output FROM run WHERE id = NEW.run), ''), 'READ SAY', NULL, NULL);
    END;

CREATE TRIGGER memwrong_go AFTER INSERT ON memwrong WHEN (SELECT gate FROM encoder WHERE word = ':prev') IS NOT NULL BEGIN
      SELECT mother('INSERT INTO g3 (arrival, remainder, trigger, times, first, last) SELECT ' || NEW.first || ', NULL, ' || (SELECT gate FROM encoder WHERE word = ':prev') || ', 0, ' || (SELECT coalesce(max(id), 0) FROM event) || ', ' || (SELECT coalesce(max(id), 0) FROM event) ||
        ' WHERE NOT EXISTS (SELECT 1 FROM g3 WHERE arrival = ' || NEW.first || ' AND trigger = ' || (SELECT gate FROM encoder WHERE word = ':prev') || ')', NULL, NULL);
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('learned', 'decide', NEW.run, 'decide', 'decide was wrong: memory ' || NEW.memid || ' answered ' || quote(substr(NEW.given, 1, 60)) || ' where ' || quote(substr(NEW.expected, 1, 60)) || ' was right. Kept as history, not overwritten. The line before differed from the one before that memory, so decide''s row for a line arriving from ' || (SELECT word FROM encoder WHERE gate = NEW.first) || ' now points at :prev: the line before matters', 'COMPARE WRITE', NULL, NULL);
    END;

CREATE TRIGGER lay_go AFTER INSERT ON lay BEGIN
      UPDATE lay SET shard = mother('INSERT INTO g' || NEW.gate || ' (arrival, remainder, trigger, times, first, last) VALUES (' || NEW.arrival || ', ' || coalesce(NEW.remainder, 'NULL') || ', ' || coalesce(NEW.trig, 'NULL') || ', 0, ' || (SELECT coalesce(max(id), 0) FROM event) || ', ' || (SELECT coalesce(max(id), 0) FROM event) || ')', NULL, NULL) WHERE id = NEW.id;
      SELECT mother('CREATE TRIGGER hop_' || NEW.gate || '_' || (SELECT shard FROM lay WHERE id = NEW.id) || ' INSTEAD OF INSERT ON land_' || NEW.gate || ' WHEN NEW.arrival = ' || NEW.arrival || ' AND NEW.remainder IS ' || coalesce(NEW.remainder, 'NULL') || ' BEGIN ' || 'UPDATE g' || NEW.gate || ' SET times = times + 1, last = (SELECT coalesce(max(id), 0) FROM event) WHERE shard = ' || (SELECT shard FROM lay WHERE id = NEW.id) || '; ' || 'INSERT INTO receipt (run, gate, shard) VALUES (NEW.run, ' || NEW.gate || ', ' || (SELECT shard FROM lay WHERE id = NEW.id) || '); ' || 'INSERT INTO event (kind, gate, run, rowgate, text, roots) VALUES (''hit'', ' || quote((SELECT word FROM encoder WHERE gate = NEW.gate)) || ', NEW.run, ' || quote((SELECT word FROM encoder WHERE gate = NEW.gate)) || ', ' || quote((SELECT word FROM encoder WHERE gate = NEW.gate) || ': row (' || coalesce((SELECT word FROM encoder WHERE gate = NEW.arrival), '?') || ', ' || coalesce((SELECT word FROM encoder WHERE gate = NEW.remainder), 'end') || ') hit; its own hop trigger carries the run on') || ', ''COMPARE WRITE''); ' || CASE WHEN NEW.gate = (SELECT gate FROM encoder WHERE word = ';') THEN 'INSERT INTO stmt (run, text) SELECT NEW.run, (SELECT group_concat(w, '' '') FROM (SELECT CASE WHEN e.role = ''var'' THEN quote(coalesce((SELECT value FROM var WHERE run = NEW.run AND name = e.word ORDER BY id DESC LIMIT 1), (SELECT value FROM var WHERE run = (SELECT parent FROM run WHERE id = NEW.run) AND name = e.word ORDER BY id DESC LIMIT 1), (SELECT value FROM var WHERE run = (SELECT root FROM run WHERE id = NEW.run) AND name = e.word ORDER BY id DESC LIMIT 1))) ELSE e.word END AS w FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run AND r.id >= (SELECT min(r2.id) FROM receipt r2 JOIN encoder e2 ON e2.gate = r2.gate WHERE r2.run = NEW.run AND e2.word IN (''SELECT'',''INSERT'',''UPDATE'',''DELETE'',''CREATE'',''WITH'') AND r2.id > coalesce((SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = 65 AND id < (SELECT max(id) FROM receipt WHERE run = NEW.run)), 0)) ORDER BY r.id)) WHERE (SELECT kind FROM run WHERE id = NEW.run) = ''formula''; ' ELSE '' END || 'INSERT INTO fire (run, gate, shard, trig, rest) VALUES (NEW.run, ' || NEW.gate || ', ' || (SELECT shard FROM lay WHERE id = NEW.id) || ', (SELECT trigger FROM g' || NEW.gate || ' WHERE shard = ' || (SELECT shard FROM lay WHERE id = NEW.id) || '), trim(' || quote(coalesce((SELECT word FROM encoder WHERE gate = NEW.remainder), '')) || ' || '' '' || coalesce(NEW.rest, ''''))); ' || CASE WHEN NEW.remainder IS NULL THEN 'INSERT INTO "end" (run) VALUES (NEW.run); ' ELSE 'INSERT INTO land_' || NEW.remainder || ' (arrival, remainder, run, rest) VALUES (' || NEW.gate || ', (SELECT gate FROM encoder WHERE word = substr(trim(NEW.rest) || '' '', 1, instr(trim(NEW.rest) || '' '', '' '') - 1)), NEW.run, trim(substr(trim(NEW.rest) || '' '', instr(trim(NEW.rest) || '' '', '' '') + 1))); ' END || 'END', NULL, NULL);
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('lay', (SELECT word FROM encoder WHERE gate = NEW.gate), NEW.run, (SELECT word FROM encoder WHERE gate = NEW.gate), (SELECT word FROM encoder WHERE gate = NEW.gate) || ': no row for (' || coalesce((SELECT word FROM encoder WHERE gate = NEW.arrival), '?') || ', ' || coalesce((SELECT word FROM encoder WHERE gate = NEW.remainder), 'end') || '). lay writes row s' || (SELECT shard FROM lay WHERE id = NEW.id) || ' and mother lays its own hop trigger' || CASE WHEN NEW.trig IS NOT NULL THEN ', trigger column ' || (SELECT word FROM encoder WHERE gate = NEW.trig) ELSE '' END || CASE WHEN NEW.run IS NOT NULL THEN '; the landing is retried through mother' ELSE '' END, 'WRITE SPAWN CALL', (SELECT word FROM encoder WHERE gate = NEW.remainder), (SELECT shard FROM lay WHERE id = NEW.id));
      INSERT INTO envelope (arrival, remainder, run, rest) SELECT NEW.arrival, NEW.remainder, NEW.run, NEW.rest WHERE NEW.run IS NOT NULL;
      SELECT mother('INSERT INTO land_' || NEW.gate || ' (arrival, remainder, run, rest) SELECT arrival, remainder, run, rest FROM envelope WHERE id = (SELECT max(id) FROM envelope)', NULL, NULL) WHERE NEW.run IS NOT NULL;
      DELETE FROM envelope WHERE id = (SELECT max(id) FROM envelope) AND run = NEW.run;
    END;

CREATE TABLE bindgo (id INTEGER PRIMARY KEY, run INTEGER);

CREATE TRIGGER bind_go AFTER INSERT ON bindgo BEGIN
      INSERT INTO bindrow (gate, arrival, remainder, trig, run) SELECT
        CASE WHEN (instr(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1)), ' ') > 0) THEN (SELECT gate FROM encoder WHERE word = substr(trim(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1))) || ' ', 1, instr(trim(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1))) || ' ', ' ') - 1)) ELSE (SELECT gate FROM encoder WHERE word = substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', 1, instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') - 1)) END,
        CASE WHEN (instr(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1)), ' ') > 0) THEN (SELECT gate FROM encoder WHERE word = substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', 1, instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') - 1)) ELSE (SELECT gate FROM encoder WHERE word = 'heard') END,
        CASE WHEN (instr(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1)), ' ') > 0) THEN (SELECT gate FROM encoder WHERE word = substr(trim(trim(substr(trim(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1))) || ' ', instr(trim(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1))) || ' ', ' ') + 1))) || ' ', 1, instr(trim(trim(substr(trim(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1))) || ' ', instr(trim(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1))) || ' ', ' ') + 1))) || ' ', ' ') - 1)) ELSE (SELECT gate FROM encoder WHERE word = substr(trim(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1))) || ' ', 1, instr(trim(trim(substr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', instr(trim((SELECT words FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))) || ' ', ' ') + 1))) || ' ', ' ') - 1)) END,
        (SELECT gate FROM encoder WHERE word = (SELECT f FROM bindq WHERE input = (SELECT input FROM run WHERE id = NEW.run))), NEW.run;
    END;

CREATE TABLE bindrow (id INTEGER PRIMARY KEY, gate INTEGER, arrival INTEGER, remainder INTEGER, trig INTEGER, run INTEGER, found INTEGER);

CREATE TRIGGER bindrow_go AFTER INSERT ON bindrow BEGIN
      UPDATE bindrow SET found = mother('SELECT shard FROM g' || NEW.gate || ' WHERE arrival = ' || NEW.arrival || ' AND remainder IS ' || coalesce(NEW.remainder, 'NULL'), NULL, NULL) WHERE id = NEW.id;
      SELECT mother('UPDATE g' || NEW.gate || ' SET trigger = ' || NEW.trig || ' WHERE shard = ' || (SELECT found FROM bindrow WHERE id = NEW.id), NULL, NULL) WHERE (SELECT found FROM bindrow WHERE id = NEW.id) IS NOT NULL;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) SELECT 'lay', (SELECT word FROM encoder WHERE gate = NEW.gate), NEW.run, (SELECT word FROM encoder WHERE gate = NEW.gate), (SELECT word FROM encoder WHERE gate = NEW.gate) || ': its row (' || (SELECT word FROM encoder WHERE gate = NEW.arrival) || ', ' || coalesce((SELECT word FROM encoder WHERE gate = NEW.remainder), 'end') || ') already exists; its trigger column is set to ' || (SELECT word FROM encoder WHERE gate = NEW.trig), 'WRITE', NULL, NULL WHERE (SELECT found FROM bindrow WHERE id = NEW.id) IS NOT NULL;
      INSERT INTO lay (gate, arrival, remainder, run, rest, trig) SELECT NEW.gate, NEW.arrival, NEW.remainder, NULL, NULL, NEW.trig WHERE (SELECT found FROM bindrow WHERE id = NEW.id) IS NULL;
    END;

CREATE TRIGGER fire_go AFTER INSERT ON fire BEGIN
      UPDATE fire SET word = coalesce((SELECT word FROM encoder WHERE gate = NEW.trig), CASE WHEN EXISTS (SELECT 1 FROM formula WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) AND ended = 0) THEN (SELECT word FROM encoder WHERE gate = NEW.gate) END)
        WHERE id = NEW.id AND NOT (EXISTS (SELECT 1 FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run AND e.word IN ('SELECT','INSERT','UPDATE','DELETE','CREATE','WITH') AND r.id > coalesce((SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = (SELECT gate FROM encoder WHERE word = ';')), 0))) AND (SELECT kind FROM run WHERE id = NEW.run) <> 'teach'
          AND coalesce((SELECT word FROM encoder WHERE gate = NEW.trig), (SELECT word FROM encoder WHERE gate = NEW.gate)) IS NOT (SELECT word FROM run WHERE id = NEW.run)
          AND coalesce((SELECT word FROM encoder WHERE gate = NEW.trig), (SELECT word FROM encoder WHERE gate = NEW.gate)) IS NOT (SELECT word FROM run WHERE id = (SELECT parent FROM run WHERE id = NEW.run))
          AND (SELECT count(*) FROM run a WHERE a.id IN (NEW.run, (SELECT parent FROM run WHERE id = NEW.run), (SELECT parent FROM run WHERE id = (SELECT parent FROM run WHERE id = NEW.run))) AND a.kind = 'formula') < 3;
      INSERT INTO gap (run, need, fill, who, word, kind) SELECT (SELECT root FROM run WHERE id = NEW.run), 'a formula for ' || (SELECT word FROM encoder WHERE gate = NEW.trig), 'the row points at it; teach "' || (SELECT word FROM encoder WHERE gate = NEW.trig) || ' = ..."', 'us, once', (SELECT word FROM encoder WHERE gate = NEW.trig), 'word'
        WHERE NEW.trig IS NOT NULL AND NOT EXISTS (SELECT 1 FROM formula WHERE word = (SELECT word FROM encoder WHERE gate = NEW.trig) AND ended = 0);
      INSERT INTO input (line, direction, parent, kind, word, fgate, fshard, subject, rest, before)
        SELECT (SELECT group_concat(w, ' ') FROM (SELECT e.word AS w FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = f.run ORDER BY r.id)), 'start', NEW.run, 'formula', f.word, NEW.gate, NEW.shard, coalesce(NEW.subject, (SELECT subject FROM run WHERE id = NEW.run)), NEW.rest,
          (SELECT group_concat(w, ' ') FROM (SELECT e.word AS w FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run AND r.id < (SELECT max(id) FROM receipt WHERE run = NEW.run) ORDER BY r.id))
        FROM formula f WHERE f.word = (SELECT word FROM fire WHERE id = NEW.id) AND f.ended = 0;
    END;

CREATE TRIGGER stmt_go AFTER INSERT ON stmt BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('out', 'output to sources', NEW.run, 'output to sources', 'output to sources: the gates the run passed decode to "' || NEW.text || '". Mother picks it up.', 'READ SAY', NULL, NULL);
      SELECT mother(NEW.text, NEW.run, NEW.id);
    END;

CREATE TRIGGER secondary_refused AFTER INSERT ON secondary WHEN NEW.last = 1 AND NEW.src <> 'sql' AND NEW.err IS NOT NULL BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('refused', NEW.src, NEW.run, NEW.src, NEW.src || ': the ask never reached its inbox. The SQL prompt refused it: ' || NEW.err, 'COMPARE', NULL, NULL);
      INSERT INTO gap (run, need, fill, who, word, kind) VALUES ((SELECT root FROM run WHERE id = NEW.run), 'an ask ' || NEW.src || ' could take', 'the statement was refused: ' || NEW.err, 'the brain by another row; else us', NULL, 'refused');
      UPDATE run SET failed = 1 WHERE id = NEW.run;
    END;

CREATE TRIGGER secondary_ask AFTER INSERT ON secondary WHEN NEW.last = 1 AND NEW.src <> 'sql' AND NEW.waiting = 0 AND NEW.err IS NULL BEGIN
      INSERT INTO sense (run, stmt, src, word, kept, aside, total) VALUES (NEW.run, NEW.stmt, NEW.src, NEW.word,
        (SELECT count(*) FROM secondary s WHERE s.stmt = NEW.stmt AND s.src = NEW.src AND s.last = 0 AND (CASE WHEN instr(s.hw, ':') > 0 THEN substr(s.hw, 1, instr(s.hw, ':') - 1) ELSE s.hw END) = NEW.word), (SELECT count(*) FROM secondary s WHERE s.stmt = NEW.stmt AND s.src = NEW.src AND s.last = 0 AND (CASE WHEN instr(s.hw, ':') > 0 THEN substr(s.hw, 1, instr(s.hw, ':') - 1) ELSE s.hw END) <> NEW.word), (SELECT count(*) FROM secondary s WHERE s.stmt = NEW.stmt AND s.src = NEW.src AND s.last = 0));
    END;

CREATE TRIGGER secondary_sql AFTER INSERT ON secondary WHEN NEW.last = 1 AND NEW.src = 'sql' BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('secondary', 'secondary input', NEW.run, 'secondary input', 'secondary input: ' || CASE WHEN NEW.err IS NOT NULL THEN 'the SQL prompt refused it: ' || NEW.err WHEN NEW.n > 0 THEN '"' || NEW.value || '"' ELSE coalesce(NEW.changes, 0) || ' change(s), no rows' END || ' comes back as a sub-input of run ' || NEW.run || ', not a new run', 'HEAR WRITE', NULL, NULL);
      INSERT INTO sense (run, stmt, src, word, kept, aside, total, asked, needed, wrong, ok) VALUES (NEW.run, NEW.stmt, 'sql', NULL, NEW.n, 0, NEW.n,
        CASE WHEN NEW.err IS NOT NULL THEN 'no: refused: ' || NEW.err ELSE 'yes: the reply answers the statement that was sent' END,
        CASE WHEN NEW.err IS NOT NULL THEN 'no: nothing came back' WHEN (SELECT text FROM stmt WHERE id = NEW.stmt) LIKE 'SELECT%' OR (SELECT text FROM stmt WHERE id = NEW.stmt) LIKE 'WITH%' THEN (CASE WHEN NEW.n > 0 THEN 'yes: ' || NEW.n || ' row(s) fill the cell' ELSE 'no: no row came back; the brain does not hold this' END) ELSE (CASE WHEN coalesce(NEW.changes, 0) > 0 THEN 'yes: ' || NEW.changes || ' change(s) made' ELSE 'no: the statement changed nothing' END) END,
        NULL, NULL);
    END;

CREATE TRIGGER secondary_wait AFTER INSERT ON secondary WHEN NEW.waiting = 1 BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('waiting', NEW.src, NEW.run, NEW.src, NEW.src || ': the ask sits in its inbox. Its outbox has not said it is populated, so mother has nothing to pick up. The cell waits; no timer fills it.', '', NULL, NULL);
      INSERT INTO var (run, name, value, src, t) VALUES (NEW.run, (SELECT text FROM stmt WHERE id = NEW.stmt), NULL, NULL, (SELECT coalesce(max(id), 0) FROM event));
      INSERT INTO gap (run, need, fill, who, word, kind) VALUES ((SELECT root FROM run WHERE id = NEW.run), 'a reply from ' || NEW.src, 'the ask was delivered and nothing has populated the outbox; waiting is the answer until it does', NEW.src, NULL, 'wait');
      UPDATE run SET failed = 1 WHERE id = NEW.run;
    END;

CREATE TRIGGER sense_ask AFTER INSERT ON sense WHEN NEW.src <> 'sql' BEGIN
      UPDATE sense SET
        asked = CASE WHEN NEW.total = 0 THEN 'no: nothing came back to compare with the ask' WHEN NEW.aside = 0 THEN 'yes: every row is about ' || NEW.word || ', the word asked' WHEN NEW.kept > 0 THEN 'partly: ' || NEW.kept || ' row(s) about ' || NEW.word || ', ' || NEW.aside || ' about other words, set aside' ELSE 'no: every row is about another word' END,
        needed = CASE WHEN NEW.kept > 0 THEN 'yes: ' || NEW.kept || ' row(s) fill the definition of ' || NEW.word || '; whether they are what the run needs is asked again when the run ends' ELSE 'no: ' || CASE WHEN NEW.total = 0 THEN NEW.src || ' sent back nothing for ' || NEW.word ELSE 'nothing that was asked for came back' END END,
        wrong = CASE WHEN NEW.kept > 0 AND NEW.aside = 0 THEN 'no: the ask got what it asked for' WHEN NEW.kept > 0 THEN 'partly: the ask was answered, and also for other words; the brain keeps only its own word' ELSE 'maybe I asked wrong: the data may not be there, the place may be wrong, or the word asked in the wrong form' END,
        setaside = (SELECT group_concat(s.hw || ' (' || CASE WHEN lower((CASE WHEN instr(s.hw, ':') > 0 THEN substr(s.hw, 1, instr(s.hw, ':') - 1) ELSE s.hw END)) = lower(NEW.word) THEN 'same letters, different case' WHEN instr((CASE WHEN instr(s.hw, ':') > 0 THEN substr(s.hw, 1, instr(s.hw, ':') - 1) ELSE s.hw END), NEW.word) > 0 THEN 'a longer form that holds ' || NEW.word ELSE 'a different word' END || ')', '; ') FROM secondary s WHERE s.stmt = NEW.stmt AND s.src = NEW.src AND s.last = 0 AND (CASE WHEN instr(s.hw, ':') > 0 THEN substr(s.hw, 1, instr(s.hw, ':') - 1) ELSE s.hw END) <> NEW.word),
        ok = (NEW.kept > 0) WHERE id = NEW.id;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('secondary', 'secondary input', NEW.run, 'secondary input', 'secondary input: ' || NEW.total || ' row(s) from ' || NEW.src || ' for "' || NEW.word || '" come back as a sub-input of run ' || NEW.run || ', not a new run', 'HEAR WRITE', NULL, NULL);
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('check', 'sense', NEW.run, 'sense', 'check the return from ' || NEW.src || ' for ' || NEW.word || '. Asked for? ' || (SELECT asked FROM sense WHERE id = NEW.id) || '. Needed? ' || (SELECT needed FROM sense WHERE id = NEW.id) || '. Asked wrong? ' || (SELECT wrong FROM sense WHERE id = NEW.id) || coalesce('. Set aside: ' || (SELECT setaside FROM sense WHERE id = NEW.id), ''), 'COMPARE FIND', NULL, NULL);
      INSERT INTO var (run, name, value, src, t, sense) VALUES (NEW.run, NEW.src || ': ' || NEW.word, CASE WHEN NEW.kept > 0 THEN NEW.kept || ' row(s)' END, NEW.src, (SELECT coalesce(max(id), 0) FROM event), NEW.id);
      INSERT INTO definition (word, src, hw, text, words) SELECT s.word, s.src, s.hw, s.value, s.words FROM secondary s WHERE s.stmt = NEW.stmt AND s.src = NEW.src AND s.last = 0 AND (CASE WHEN instr(s.hw, ':') > 0 THEN substr(s.hw, 1, instr(s.hw, ':') - 1) ELSE s.hw END) = NEW.word;
      INSERT INTO gap (run, need, fill, who, word, kind) SELECT (SELECT root FROM run WHERE id = NEW.run), 'an answer from ' || NEW.src || ' for ' || NEW.word, 'did I ask wrong? The data may not be there, the place may be wrong, or the word in the wrong form', 'the brain by another row; else us', NEW.word, 'ask' WHERE NEW.kept = 0;
      UPDATE run SET failed = 1 WHERE id = NEW.run AND NEW.kept = 0;
    END;

CREATE TRIGGER sense_sql AFTER INSERT ON sense WHEN NEW.src = 'sql' BEGIN
      UPDATE sense SET ok = (NEW.needed LIKE 'yes%'), wrong = CASE WHEN NEW.needed LIKE 'yes%' THEN 'no: the ask got what it asked for' ELSE 'maybe I asked wrong: the data may not be there, it may be held somewhere else, or the question went to the wrong table' END WHERE id = NEW.id;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('check', 'sense', NEW.run, 'sense', 'check the return. Asked for? ' || NEW.asked || '. Needed? ' || NEW.needed || '. Asked wrong? ' || (SELECT wrong FROM sense WHERE id = NEW.id), 'COMPARE FIND', NULL, NULL);
      INSERT INTO var (run, name, value, src, t, sense) VALUES (NEW.run, (SELECT text FROM stmt WHERE id = NEW.stmt), CASE WHEN NEW.needed LIKE 'yes%' THEN coalesce((SELECT value FROM secondary WHERE stmt = NEW.stmt AND last = 1 AND n > 0), 'ok, ' || (SELECT changes FROM secondary WHERE stmt = NEW.stmt AND last = 1) || ' change(s)') END, 'mother', (SELECT coalesce(max(id), 0) FROM event), NEW.id);
      INSERT INTO var (run, name, value, src, t) SELECT NEW.run, ':found', (SELECT value FROM secondary WHERE stmt = NEW.stmt AND last = 1), 'mother', (SELECT coalesce(max(id), 0) FROM event) WHERE (SELECT n FROM secondary WHERE stmt = NEW.stmt AND last = 1) > 0;
      UPDATE run SET failed = 1 WHERE id = NEW.run AND NEW.needed NOT LIKE 'yes%';
    END;

CREATE TRIGGER definition_split AFTER INSERT ON definition WHEN NEW.src <> 'node' AND NEW.words IS NOT NULL BEGIN
      INSERT INTO defword (def, word, src, w, rest) VALUES (NEW.id, NEW.word, NEW.src, NULL, NEW.words);
    END;

CREATE TRIGGER defword_next AFTER INSERT ON defword WHEN trim(NEW.rest) <> '' BEGIN
      INSERT INTO defword (def, word, src, w, rest) VALUES (NEW.def, NEW.word, NEW.src, substr(trim(NEW.rest) || ' ', 1, instr(trim(NEW.rest) || ' ', ' ') - 1), trim(substr(trim(NEW.rest) || ' ', instr(trim(NEW.rest) || ' ', ' ') + 1)));
    END;

CREATE TRIGGER say_go AFTER INSERT ON say BEGIN
      INSERT INTO var (run, name, value, src, t) VALUES ((SELECT root FROM run WHERE id = NEW.run), 'output', NEW.text, 'say', (SELECT coalesce(max(id), 0) FROM event));
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('op', 'say', NEW.run, 'OUTPUT', 'say: "' || coalesce(NEW.text, '') || '" goes to output to use', 'SAY', NULL, NULL);
    END;

CREATE TRIGGER relation_drawn AFTER INSERT ON relation BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('rel', NEW.a, (SELECT max(id) FROM run), NULL, 'relation row ' || NEW.a || ' ' || NEW.rel || ' ' || NEW.b || ' (trust ' || NEW.trust || '): the relation table''s own trigger draws the line and the points pull', 'WRITE', NULL, NULL);
      UPDATE event SET a = NEW.b, b = NEW.rel || '|' || NEW.trust WHERE id = (SELECT max(id) FROM event);
    END;

CREATE TRIGGER formula_written AFTER INSERT ON formula BEGIN
      INSERT INTO proc (word, status) VALUES (NEW.word, CASE WHEN NEW.origin = 'told' THEN 'taught' ELSE 'derived' END)
        ON CONFLICT(word) DO UPDATE SET status = CASE WHEN NEW.origin = 'told' THEN 'taught' ELSE 'derived' END;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('taught', NEW.word, (SELECT max(id) FROM run), 'formula', CASE WHEN NEW.origin = 'told' THEN NEW.word || ' = ' || coalesce((SELECT group_concat(w, ' ') FROM (SELECT e.word AS w FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run ORDER BY r.id)), '') || ' (read back from the run that taught it). What it is made of is that run; what it does is measured when it runs.' || CASE WHEN (SELECT count(*) FROM formula WHERE word = NEW.word) > 1 THEN ' A truth shift: the old row is ended, not erased.' ELSE '' END ELSE NEW.word || ' now has a formula the brain found itself, marked ' || NEW.origin || ', a guess until tested: ' || coalesce((SELECT group_concat(w, ' ') FROM (SELECT e.word AS w FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run ORDER BY r.id)), '') END, 'WRITE', NULL, NULL);
      UPDATE event SET kind = 'derived' WHERE id = (SELECT max(id) FROM event) AND NEW.origin <> 'told';
    END;

CREATE TRIGGER source_go AFTER INSERT ON source BEGIN
      UPDATE encoder SET sourced = 1 WHERE word = NEW.word;
      INSERT INTO gap (run, need, fill, who, word, kind) SELECT (SELECT root FROM run WHERE id = NEW.run), 'where to look for a definition of ' || NEW.word, 'no formula says where to look: teach source', 'us, once; then the brain', NEW.word, 'source' WHERE NOT EXISTS (SELECT 1 FROM formula WHERE word = 'source' AND ended = 0);
      INSERT INTO fire (run, gate, shard, trig, rest, subject) SELECT NEW.run, (SELECT gate FROM encoder WHERE word = 'source'), NULL, (SELECT gate FROM encoder WHERE word = 'source'), NEW.word, NEW.word WHERE EXISTS (SELECT 1 FROM formula WHERE word = 'source' AND ended = 0);
      INSERT INTO agree (word, run) VALUES (NEW.word, NEW.run);
      INSERT INTO input (line, direction, parent, kind, subject) SELECT d.words, NEW.word, NEW.run, 'defrow', NEW.word FROM definition d WHERE d.word = NEW.word AND d.src <> 'node' AND trim(coalesce(d.words, '')) <> '' LIMIT 8;
      INSERT INTO gap (run, need, fill, who, word, kind) SELECT (SELECT root FROM run WHERE id = NEW.run), 'formulas for the words in the definition rows (like, opposite, kind)', 'teach them; then the rows write relations', 'us, once', NULL, 'defrows'
        WHERE EXISTS (SELECT 1 FROM definition WHERE word = NEW.word AND src <> 'node') AND NOT EXISTS (SELECT 1 FROM formula WHERE word IN ('like', 'opposite', 'kind') AND ended = 0);
      INSERT INTO fire (run, gate, shard, trig, rest, subject) SELECT NEW.run, (SELECT gate FROM encoder WHERE word = 'born'), NULL, (SELECT gate FROM encoder WHERE word = 'derive'), NEW.word, NEW.word WHERE EXISTS (SELECT 1 FROM formula WHERE word = 'derive' AND ended = 0) AND NOT EXISTS (SELECT 1 FROM formula WHERE word = NEW.word AND ended = 0);
      INSERT INTO fire (run, gate, shard, trig, rest, subject) SELECT NEW.run, (SELECT gate FROM encoder WHERE word = 'born'), NULL, (SELECT gate FROM encoder WHERE word = 'deduce'), NEW.word, NEW.word WHERE EXISTS (SELECT 1 FROM formula WHERE word = 'deduce' AND ended = 0) AND NOT EXISTS (SELECT 1 FROM formula WHERE word = NEW.word AND ended = 0);
    END;

CREATE TRIGGER agree_go AFTER INSERT ON agree BEGIN
      INSERT INTO need (w, n) SELECT w, 1 FROM defword WHERE word = NEW.word AND w IS NOT NULL AND w <> NEW.word AND length(w) > 1 GROUP BY w HAVING count(DISTINCT src) >= 2 AND NOT EXISTS (SELECT 1 FROM formula WHERE word = w AND ended = 0)
        ON CONFLICT(w) DO UPDATE SET n = n + 1;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) SELECT 'agree', NEW.word, NEW.run, 'agree', 'agree: defining words two or more sources share for ' || NEW.word || ': ' || coalesce((SELECT group_concat(w, ', ') FROM (SELECT w FROM defword WHERE word = NEW.word AND w IS NOT NULL AND w <> NEW.word AND length(w) > 1 GROUP BY w HAVING count(DISTINCT src) >= 2 LIMIT 14)), 'none'), 'READ COMPARE WRITE', NULL, NULL WHERE EXISTS (SELECT 1 FROM definition WHERE word = NEW.word AND src <> 'node');
    END;

CREATE TRIGGER end_branch AFTER INSERT ON "end" WHEN (SELECT kind FROM run WHERE id = NEW.run) = 'formula' BEGIN
      UPDATE run SET t1 = (SELECT coalesce(max(id), 0) FROM event) WHERE id = NEW.run;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('substitute', (SELECT word FROM run WHERE id = NEW.run), NEW.run, NULL, 'substitution: the cells plug into ' || (SELECT word FROM run WHERE id = NEW.run) || '''s formula and it ran. ' || CASE WHEN (SELECT failed FROM run WHERE id = NEW.run) = 1 THEN 'An ask came back without what it needed.' ELSE 'Every ask came back with what it asked for.' END, 'READ WRITE', NULL, NULL);
      INSERT INTO procrun (word, receipt) VALUES ((SELECT word FROM run WHERE id = NEW.run), (SELECT group_concat(x, ' ') FROM (SELECT r.gate || ':s' || r.shard AS x FROM receipt r WHERE r.run = NEW.run ORDER BY r.id)));
      UPDATE proc SET uses = uses + 1, status = CASE WHEN status = 'taught' AND (SELECT count(*) FROM procrun p WHERE p.word = proc.word AND p.receipt = (SELECT group_concat(x, ' ') FROM (SELECT r.gate || ':s' || r.shard AS x FROM receipt r WHERE r.run = NEW.run ORDER BY r.id))) >= 3 THEN 'learned' WHEN status = 'learned' THEN 'automated' ELSE status END WHERE word = (SELECT word FROM run WHERE id = NEW.run);
      INSERT INTO stepq (run, alt) SELECT NEW.run, mother('SELECT trigger FROM g' || (SELECT fgate FROM run WHERE id = NEW.run) || ' WHERE trigger IS NOT NULL AND trigger <> ' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM run WHERE id = NEW.run)) || ' AND shard IS NOT ' || coalesce((SELECT fshard FROM run WHERE id = NEW.run), 'NULL') || ' LIMIT 1', NULL, NULL) WHERE (SELECT failed FROM run WHERE id = NEW.run) = 1 AND (SELECT fgate FROM run WHERE id = NEW.run) IS NOT NULL AND (SELECT fshard FROM run WHERE id = NEW.run) IS NOT NULL;
    END;

CREATE TABLE stepq (id INTEGER PRIMARY KEY, run INTEGER, alt INTEGER);

CREATE TRIGGER step_back AFTER INSERT ON stepq BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) SELECT 'stepback', (SELECT word FROM encoder WHERE gate = (SELECT fgate FROM run WHERE id = NEW.run)), (SELECT parent FROM run WHERE id = NEW.run), (SELECT word FROM encoder WHERE gate = (SELECT fgate FROM run WHERE id = NEW.run)), 'step back: ' || (SELECT word FROM run WHERE id = NEW.run) || ' asked and the check failed. The run steps back to ' || (SELECT word FROM encoder WHERE gate = (SELECT fgate FROM run WHERE id = NEW.run)) || ' and takes its other row, whose trigger is ' || (SELECT word FROM encoder WHERE gate = NEW.alt), 'FIND COMPARE MOVE', NULL, NULL WHERE NEW.alt IS NOT NULL;
      INSERT INTO fire (run, gate, shard, trig, rest) SELECT (SELECT parent FROM run WHERE id = NEW.run), (SELECT fgate FROM run WHERE id = NEW.run), NULL, NEW.alt, (SELECT rest FROM input WHERE id = (SELECT input FROM run WHERE id = NEW.run)) WHERE NEW.alt IS NOT NULL;
      INSERT INTO gap (run, need, fill, who, word, kind) SELECT (SELECT root FROM run WHERE id = NEW.run), 'another way to ask what ' || (SELECT word FROM run WHERE id = NEW.run) || ' asked', (SELECT word FROM encoder WHERE gate = (SELECT fgate FROM run WHERE id = NEW.run)) || ' has no other row with a trigger', 'us, or the brain once it learns one', NULL, 'stepback' WHERE NEW.alt IS NULL;
    END;

CREATE TRIGGER end_teach AFTER INSERT ON "end" WHEN (SELECT kind FROM run WHERE id = NEW.run) = 'teach' BEGIN
      UPDATE run SET t1 = (SELECT coalesce(max(id), 0) FROM event) WHERE id = NEW.run;
      UPDATE formula SET ended = 1 WHERE word = (SELECT word FROM run WHERE id = NEW.run) AND ended = 0;
      INSERT INTO memory (list, line, direction, receipt, output, answer, mark, first, last, run) SELECT gates, line, direction, (SELECT group_concat(x, ' ') FROM (SELECT r.gate || ':s' || r.shard AS x FROM receipt r WHERE r.run = NEW.run ORDER BY r.id)), NULL, NULL, 'told', (SELECT coalesce(max(id), 0) FROM event), (SELECT coalesce(max(id), 0) FROM event), NEW.run FROM run WHERE id = NEW.run;
      UPDATE run SET memid = (SELECT max(id) FROM memory) WHERE id = NEW.run;
      INSERT INTO formula (word, run, origin, t) VALUES ((SELECT word FROM run WHERE id = NEW.run), NEW.run, 'told', (SELECT coalesce(max(id), 0) FROM event));
    END;

CREATE TRIGGER end_line AFTER INSERT ON "end" WHEN (SELECT kind FROM run WHERE id = NEW.run) = 'line' BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('end', 'end', NEW.run, 'end', 'end: receipt ' || coalesce((SELECT group_concat(x, ' ') FROM (SELECT r.gate || ':s' || r.shard AS x FROM receipt r WHERE r.run = NEW.run ORDER BY r.id)), '') || '. ' || (SELECT count(*) FROM run WHERE parent = NEW.run) || ' branch run(s) wrote against this run.', 'READ JOIN WRITE', NULL, NULL);
      INSERT INTO "BUILD" (run, text) SELECT NEW.run, trim(substr(line, 7, length(line) - 12)) FROM run WHERE id = NEW.run AND build = 1;
      UPDATE run SET output = CASE WHEN build = 1 THEN coalesce((SELECT CASE WHEN s.err IS NOT NULL THEN 'error: ' || s.err WHEN s.n > 0 THEN s.value ELSE 'ok' END FROM secondary s WHERE s.run = NEW.run AND s.last = 1 ORDER BY s.id DESC LIMIT 1), 'ok') ELSE coalesce((SELECT value FROM var WHERE run = NEW.run AND name = 'output' ORDER BY id DESC LIMIT 1), (SELECT group_concat(x, ' ') FROM (SELECT e.word || CASE WHEN e.role IN ('word', 'literal') AND NOT EXISTS (SELECT 1 FROM formula WHERE word = e.word AND ended = 0) AND e.word <> '?' THEN '?' ELSE '' END AS x FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run ORDER BY r.id))) END WHERE id = NEW.run;
      UPDATE run SET mark = CASE WHEN expected IS NOT NULL THEN (CASE WHEN output = expected THEN 'right' ELSE 'wrong' END)
        WHEN EXISTS (SELECT 1 FROM memory WHERE list = run.gates AND direction = run.direction) THEN (CASE WHEN (SELECT output FROM memory WHERE list = run.gates AND direction = run.direction ORDER BY id DESC LIMIT 1) = output THEN 'balanced' ELSE 'shift' END) ELSE 'unchecked' END WHERE id = NEW.run;
      UPDATE proc SET right = right + ((SELECT mark FROM run WHERE id = NEW.run) = 'right'), wrong = wrong + ((SELECT mark FROM run WHERE id = NEW.run) = 'wrong') WHERE (SELECT expected FROM run WHERE id = NEW.run) IS NOT NULL AND word IN (SELECT word FROM run WHERE root = NEW.run AND kind = 'formula');
      UPDATE var SET src = src || '; the run came out wrong, so this may not have been what was needed' WHERE sense IS NOT NULL AND run IN (SELECT id FROM run WHERE root = NEW.run) AND (SELECT mark FROM run WHERE id = NEW.run) = 'wrong';
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('sense', 'sense', NEW.run, 'sense', 'makes sense: proposed "' || (SELECT output FROM run WHERE id = NEW.run) || '". ' || CASE WHEN (SELECT expected FROM run WHERE id = NEW.run) IS NOT NULL THEN 'expected "' || (SELECT expected FROM run WHERE id = NEW.run) || '": ' ELSE '' END || (SELECT mark FROM run WHERE id = NEW.run) || CASE WHEN (SELECT mark FROM run WHERE id = NEW.run) = 'wrong' THEN '. The failed try stays in memory as wrong; the expected output is kept with it, so next time the hop answers it.' ELSE '' END, 'COMPARE FIND', NULL, NULL);
      UPDATE memory SET ended = 1 WHERE list = (SELECT gates FROM run WHERE id = NEW.run) AND direction = (SELECT direction FROM run WHERE id = NEW.run) AND ended = 0 AND (SELECT build FROM run WHERE id = NEW.run) = 0;
      INSERT INTO memory (list, line, direction, receipt, output, answer, mark, first, last, run, prevgates) SELECT gates, line, direction, (SELECT group_concat(x, ' ') FROM (SELECT r.gate || ':s' || r.shard AS x FROM receipt r WHERE r.run = NEW.run ORDER BY r.id)), CASE WHEN mark = 'wrong' THEN expected ELSE output END, expected, mark, (SELECT coalesce(max(id), 0) FROM event), (SELECT coalesce(max(id), 0) FROM event), NEW.run, (SELECT gates FROM run WHERE kind = 'line' AND id < NEW.run ORDER BY id DESC LIMIT 1) FROM run WHERE id = NEW.run AND build = 0;
      UPDATE run SET memid = (SELECT max(id) FROM memory), t1 = (SELECT coalesce(max(id), 0) FROM event) WHERE id = NEW.run AND build = 0;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) SELECT 'memory', 'memory', NEW.run, 'memory', 'memory: new row ' || (SELECT max(id) FROM memory) || ' (' || (SELECT mark FROM run WHERE id = NEW.run) || ')', 'FIND COMPARE WRITE', (SELECT line FROM run WHERE id = NEW.run), (SELECT max(id) FROM memory) WHERE (SELECT build FROM run WHERE id = NEW.run) = 0;
      INSERT INTO timeline (t, mem, run) SELECT (SELECT coalesce(max(id), 0) FROM event), (SELECT memid FROM run WHERE id = NEW.run), NEW.run WHERE (SELECT build FROM run WHERE id = NEW.run) = 0;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) SELECT 'timeline', 'timeline', NEW.run, 'timeline', 'timeline: row ' || (SELECT max(id) FROM timeline) || ' (memory ' || (SELECT memid FROM run WHERE id = NEW.run) || ')', 'CLOCK WRITE', (SELECT memid FROM run WHERE id = NEW.run), NULL WHERE (SELECT build FROM run WHERE id = NEW.run) = 0;
      INSERT INTO output (run, text) VALUES (NEW.run, (SELECT output FROM run WHERE id = NEW.run));
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('say', 'say', NEW.run, 'OUTPUT', 'say: ' || coalesce((SELECT output FROM run WHERE id = NEW.run), '') || CASE WHEN (SELECT mark FROM run WHERE id = NEW.run) = 'wrong' THEN ' (corrected to "' || (SELECT expected FROM run WHERE id = NEW.run) || '" for next time)' ELSE '' END, 'READ SAY', NULL, NULL);
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) SELECT 'gaps', 'gaps', NEW.run, NULL, 'this run needed ' || (SELECT count(*) FROM gap WHERE run = NEW.run) || ' thing(s) it did not have', '', NULL, NULL WHERE EXISTS (SELECT 1 FROM gap WHERE run = NEW.run);
    END;

CREATE TRIGGER receipt_gap AFTER INSERT ON receipt WHEN (SELECT kind FROM run WHERE id = NEW.run) = 'line' AND (SELECT role FROM encoder WHERE gate = NEW.gate) = 'word'
        AND NOT EXISTS (SELECT 1 FROM formula WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) AND ended = 0) AND NOT EXISTS (SELECT 1 FROM gap WHERE run = NEW.run AND word = (SELECT word FROM encoder WHERE gate = NEW.gate) AND kind = 'word') BEGIN
      INSERT INTO gap (run, need, fill, who, word, kind) VALUES (NEW.run, 'a meaning for ' || (SELECT word FROM encoder WHERE gate = NEW.gate), 'it does nothing when a run passes it. A formula: typed, or found by the brain through derive', 'the brain through derive; else us', (SELECT word FROM encoder WHERE gate = NEW.gate), 'word');
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('gap', (SELECT word FROM encoder WHERE gate = NEW.gate), NEW.run, NULL, (SELECT word FROM encoder WHERE gate = NEW.gate) || ': the run passes it and nothing happens. No formula. A broken word.', '', NULL, NULL);
    END;

CREATE TRIGGER build_go AFTER INSERT ON "BUILD" BEGIN
      INSERT INTO stmt (run, text) VALUES (NEW.run, NEW.text);
    END;

CREATE TRIGGER state_written AFTER INSERT ON state BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('state', 'state', (SELECT max(id) FROM run), 'state', 'state: ' || coalesce(NEW.key, 'NULL') || ' = ' || coalesce(quote(NEW.value), 'NULL') || '. A formula wrote it; the brain holds it now.', 'WRITE', NEW.key, NULL);
    END;

CREATE TRIGGER place_written AFTER INSERT ON place BEGIN
      UPDATE place SET ended = 1 WHERE word = NEW.word AND id < NEW.id AND ended = 0;
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('place', NEW.word, (SELECT max(id) FROM run), 'place', 'place: ' || NEW.word || ' at ' || NEW.x || ', ' || NEW.y || ', ' || NEW.z || '. An older place of this word, if any, is kept as history.', '', NEW.word, NEW.x || ',' || NEW.y || ',' || NEW.z);
    END;

CREATE TRIGGER proc_status AFTER UPDATE OF status ON proc WHEN NEW.status <> OLD.status BEGIN
      INSERT INTO event (kind, gate, run, rowgate, text, roots, a, b) VALUES ('learned', NEW.word, (SELECT max(id) FROM run), 'formula', NEW.word || CASE NEW.status WHEN 'learned' THEN ' has three memories of the same receipt: learned.' WHEN 'automated' THEN ' ran again after learned: automated.' ELSE ' is ' || NEW.status END, 'COMPARE WRITE', NEW.status, NULL);
    END;

INSERT INTO input (line, direction) VALUES ('source = INSERT INTO wn.inbox ( word ) VALUES ( :subject ) ; INSERT INTO gcide.inbox ( word ) VALUES ( :subject ) ; INSERT INTO mw.inbox ( word ) VALUES ( :subject ) ; INSERT INTO mwt.inbox ( word ) VALUES ( :subject ) ; INSERT INTO moby.inbox ( word ) VALUES ( :subject ) ; INSERT INTO map.inbox ( word ) VALUES ( :subject ) ; INSERT INTO sqldoc.inbox ( word ) VALUES ( :subject ) ; INSERT INTO measured.inbox ( word ) VALUES ( :subject ) ;', 'heard');
