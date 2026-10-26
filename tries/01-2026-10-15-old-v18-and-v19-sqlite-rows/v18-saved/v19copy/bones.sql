-- Neuron v19: the bones. Laid by hand, once.
-- Tables and the triggers are the only things the brain cannot make for itself.
-- Everything else (neurons, shards, memories, moments) is a row the brain makes by hitting neurons.

-- time
CREATE TABLE TIMELINE (id INTEGER PRIMARY KEY, at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);

-- every neuron. gate = its place (a number's place is the number; empty until placed).
-- does = what it does, as code. A neuron that does nothing is a value.
CREATE TABLE neuron (id INTEGER PRIMARY KEY, gate TEXT UNIQUE, born INTEGER, does TEXT);

-- the encoder: a word is only a pointer to a neuron. Words live here and nowhere else.
CREATE TABLE word (text TEXT PRIMARY KEY, neuron INTEGER NOT NULL);

-- DNA shards: from a neuron, by an operation and a remainder, to a destination.
CREATE TABLE dna (id INTEGER PRIMARY KEY, neuron INTEGER NOT NULL, op INTEGER NOT NULL, rem INTEGER,
                  dest INTEGER NOT NULL, born INTEGER, times INTEGER NOT NULL DEFAULT 1, last INTEGER);
CREATE INDEX dna_hop ON dna (neuron, op, rem);

-- a step: a run lands on a neuron (with up to two values a, b; c is what it produced)
CREATE TABLE step (id INTEGER PRIMARY KEY, neuron INTEGER NOT NULL, a INTEGER, b INTEGER, c INTEGER,
                   shard INTEGER, ear INTEGER, at INTEGER);

-- what was typed, and each token of it
CREATE TABLE ear (id INTEGER PRIMARY KEY, text TEXT NOT NULL);
CREATE TABLE heard (id INTEGER PRIMARY KEY, ear INTEGER NOT NULL, token TEXT NOT NULL);

-- short-term: values held while a sentence runs, and operations waiting for a value
CREATE TABLE held (id INTEGER PRIMARY KEY, neuron INTEGER, ear INTEGER, used INTEGER);
CREATE TABLE wait (id INTEGER PRIMARY KEY, op INTEGER NOT NULL, a INTEGER, ear INTEGER, filled INTEGER);
CREATE TABLE walk (step INTEGER NOT NULL, n INTEGER NOT NULL, place INTEGER NOT NULL);

-- memory: the same truth again is the same row with one more time; a changed truth ends the old row
CREATE TABLE memory (id INTEGER PRIMARY KEY, neuron INTEGER NOT NULL, op INTEGER NOT NULL, a INTEGER NOT NULL,
                     b INTEGER NOT NULL, times INTEGER NOT NULL DEFAULT 1, first_at INTEGER NOT NULL,
                     last_at INTEGER NOT NULL, ended_at INTEGER);
-- each time a memory happened: which meaning ran, which shard was used, how many hops
CREATE TABLE occurrence (id INTEGER PRIMARY KEY, memory INTEGER NOT NULL, step INTEGER NOT NULL, at INTEGER NOT NULL,
                         meaning INTEGER, shard INTEGER, hops INTEGER NOT NULL);
-- the receipt of a long run: every place it stood on
CREATE TABLE path (occurrence INTEGER NOT NULL, n INTEGER NOT NULL, neuron INTEGER NOT NULL);

-- every version of what a neuron does. The long form is kept when a formula takes its place.
CREATE TABLE meaning (id INTEGER PRIMARY KEY, neuron INTEGER NOT NULL, does TEXT NOT NULL, form INTEGER,
                      balanced INTEGER, from_at INTEGER, until_at INTEGER);
-- shapes of two places that study may try (A and B are the two places)
CREATE TABLE form (neuron INTEGER PRIMARY KEY, expr TEXT NOT NULL);
-- the code pattern a found formula is written into
CREATE TABLE pattern (id INTEGER PRIMARY KEY, code TEXT NOT NULL);
-- study's work: how many memories each form balanced
CREATE TABLE fit (step INTEGER NOT NULL, form INTEGER NOT NULL, ok INTEGER, total INTEGER);

-- what the brain produced for the mouth: a balance, a need, a value
CREATE TABLE balance (id INTEGER PRIMARY KEY, ear INTEGER, a INTEGER, b INTEGER, ok INTEGER, at INTEGER);
CREATE TABLE need (id INTEGER PRIMARY KEY, ear INTEGER, token TEXT, neuron INTEGER, at INTEGER);
CREATE TABLE out (id INTEGER PRIMARY KEY, ear INTEGER, neuron INTEGER, at INTEGER);

-- how the mouth renders a neuron: a number by its place, anything else by the word that points to it
CREATE VIEW nm AS
  SELECT n.id, CASE WHEN n.gate IS NOT NULL THEN n.gate
                    ELSE coalesce((SELECT w.text FROM word w WHERE w.neuron = n.id ORDER BY w.rowid LIMIT 1), '#' || n.id) END AS text
  FROM neuron n;

-- PHYSICS 1, excite: a step lands. A new moment; the neuron does what it does.
-- A neuron that does nothing is a value, so it is held.
CREATE TRIGGER excite AFTER INSERT ON step BEGIN
  INSERT INTO TIMELINE (at) VALUES (CURRENT_TIMESTAMP);
  UPDATE step SET at = (SELECT max(id) FROM TIMELINE) WHERE id = NEW.id;
  SELECT eval(replace(replace(does, ':S:', NEW.id), ':ME:', NEW.neuron)) FROM neuron WHERE id = NEW.neuron AND does IS NOT NULL;
  INSERT INTO held (neuron, ear) SELECT id, NEW.ear FROM neuron WHERE id = NEW.neuron AND does IS NULL AND NEW.ear IS NOT NULL;
END;

-- PHYSICS 2, arrive: a value is held while an operation waits for one. The waiting neuron fires with both.
CREATE TRIGGER arrive AFTER INSERT ON held
WHEN EXISTS (SELECT 1 FROM wait WHERE ear = NEW.ear AND filled IS NULL)
BEGIN
  UPDATE held SET used = NEW.id WHERE id = NEW.id;
  UPDATE wait SET filled = NEW.id WHERE id = (SELECT max(id) FROM wait WHERE ear = NEW.ear AND filled IS NULL);
  INSERT INTO step (neuron, a, b, ear) SELECT op, a, NEW.neuron, ear FROM wait WHERE filled = NEW.id;
END;

-- PHYSICS 3, point: a heard token is a pointer. A word goes to its neuron; a number goes to its place
-- (if nothing lives there yet, neuron 1, the one that makes neurons, is hit with that place); anything else is a need.
CREATE TRIGGER point AFTER INSERT ON heard BEGIN
  INSERT INTO step (neuron, ear) SELECT neuron, NEW.ear FROM word WHERE text = NEW.token;
  INSERT INTO step (neuron, ear)
    SELECT n.id, NEW.ear FROM neuron n
    WHERE NOT EXISTS (SELECT 1 FROM word WHERE text = NEW.token)
      AND ((NEW.token GLOB '[0-9]*' AND NEW.token NOT GLOB '*[^0-9]*')
           OR (NEW.token GLOB '-[0-9]*' AND substr(NEW.token, 2) NOT GLOB '*[^0-9]*'))
      AND n.gate = CAST(CAST(NEW.token AS INTEGER) AS TEXT);
  INSERT INTO step (neuron, a, ear)
    SELECT 1, CAST(NEW.token AS INTEGER), NEW.ear
    WHERE NOT EXISTS (SELECT 1 FROM word WHERE text = NEW.token)
      AND ((NEW.token GLOB '[0-9]*' AND NEW.token NOT GLOB '*[^0-9]*')
           OR (NEW.token GLOB '-[0-9]*' AND substr(NEW.token, 2) NOT GLOB '*[^0-9]*'))
      AND NOT EXISTS (SELECT 1 FROM neuron WHERE gate = CAST(CAST(NEW.token AS INTEGER) AS TEXT));
  INSERT INTO need (ear, token, at)
    SELECT NEW.ear, NEW.token, (SELECT max(id) FROM TIMELINE)
    WHERE NOT EXISTS (SELECT 1 FROM word WHERE text = NEW.token)
      AND NOT ((NEW.token GLOB '[0-9]*' AND NEW.token NOT GLOB '*[^0-9]*')
               OR (NEW.token GLOB '-[0-9]*' AND substr(NEW.token, 2) NOT GLOB '*[^0-9]*'));
END;

-- the only neuron laid by hand: neuron 1, the one that makes neurons
INSERT INTO neuron (id, does) VALUES (1, CAST(readfile('code/new.sql') AS TEXT));
INSERT INTO meaning (neuron, does) SELECT 1, does FROM neuron WHERE id = 1;

-- the first run: time begins, and zero is born at place 0
INSERT INTO step (neuron, a) VALUES (1, 0);
