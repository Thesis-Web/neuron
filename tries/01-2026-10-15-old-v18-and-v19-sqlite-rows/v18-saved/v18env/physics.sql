-- the neuron the brain hands its finished line to the mother through
INSERT INTO code (word) VALUES ('/build');

-- a step: a run lands on a neuron, carrying its remainder (the rest of the run, as numbers) and what it has said so far
CREATE TABLE step (id INTEGER PRIMARY KEY, run INTEGER, neuron INTEGER NOT NULL, remainder TEXT NOT NULL, said TEXT NOT NULL DEFAULT '', result TEXT, at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);

-- dna: from a neuron, by a key (the head of the remainder), to the next gate; times = how often it was walked
CREATE TABLE dna (id INTEGER PRIMARY KEY, neuron INTEGER NOT NULL, key INTEGER NOT NULL, dest INTEGER NOT NULL, times INTEGER NOT NULL DEFAULT 1, at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE INDEX dna_hop ON dna (neuron, key);

-- memory: what a run said and what the mother answered, attached to the neuron the run ended on
CREATE TABLE memory (id INTEGER PRIMARY KEY, run INTEGER NOT NULL, neuron INTEGER NOT NULL, said TEXT NOT NULL, result TEXT,
                     times INTEGER NOT NULL DEFAULT 1, first_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                     last_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, ended_at TEXT);

-- the ear: a typed line, the numbers heard so far, and the words it has no neuron for
CREATE TABLE ear (id INTEGER PRIMARY KEY, line TEXT NOT NULL, heard TEXT NOT NULL DEFAULT '', first INTEGER, at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE need (id INTEGER PRIMARY KEY, ear INTEGER NOT NULL, word TEXT NOT NULL, at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);

-- PHYSICS 1, listen: take the first word off the line (the space is the hop). A known word becomes its number;
-- an unknown word is a need and listening stops; a last word of /build starts the run at /build with everything heard.
CREATE TRIGGER listen AFTER INSERT ON ear WHEN NEW.line <> '' BEGIN
  INSERT INTO ear (line, heard, first)
    SELECT ltrim(substr(NEW.line, instr(NEW.line || ' ', ' ') + 1)), ltrim(NEW.heard || ' ' || c.id), coalesce(NEW.first, NEW.id)
    FROM code c WHERE c.word = substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1) AND c.word <> '/build';
  INSERT INTO need (ear, word)
    SELECT coalesce(NEW.first, NEW.id), substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1)
    WHERE NOT EXISTS (SELECT 1 FROM code WHERE word = substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1));
  INSERT INTO step (neuron, remainder)
    SELECT c.id, NEW.heard FROM code c
    WHERE c.word = '/build' AND NEW.line = '/build' AND NEW.heard <> '';
END;

-- PHYSICS 2, hop: the key is the head of the remainder. A shard from here by that key: walk it again (times + 1).
-- No shard: lay it. Land on its next gate with the rest of the remainder; that neuron adds its word.
CREATE TRIGGER hop AFTER INSERT ON step WHEN NEW.remainder <> '' BEGIN
  UPDATE dna SET times = times + 1, at = CURRENT_TIMESTAMP
    WHERE neuron = NEW.neuron AND key = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER);
  INSERT INTO dna (neuron, key, dest)
    SELECT NEW.neuron, c.id, c.id FROM code c
    WHERE c.id = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER)
      AND NOT EXISTS (SELECT 1 FROM dna WHERE neuron = NEW.neuron AND key = c.id);
  INSERT INTO step (run, neuron, remainder, said)
    SELECT coalesce(NEW.run, NEW.id), d.dest, ltrim(substr(NEW.remainder, instr(NEW.remainder || ' ', ' ') + 1)),
           ltrim(NEW.said || ' ' || c.word)
    FROM dna d JOIN code c ON c.id = d.dest
    WHERE d.neuron = NEW.neuron AND d.key = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER);
END;

-- PHYSICS 3, end: nothing remains, so the run ends here. A run that began at /build hands what it said to the mother
-- and keeps her answer. Then the memory: the same truth again counts up; a changed answer ends the old memory.
CREATE TRIGGER end_of_run AFTER INSERT ON step WHEN NEW.remainder = '' BEGIN
  UPDATE step SET result = mother(NEW.said)
    WHERE id = NEW.id AND (SELECT s.neuron FROM step s WHERE s.id = NEW.run) = (SELECT id FROM code WHERE word = '/build');
  UPDATE memory SET ended_at = CURRENT_TIMESTAMP
    WHERE ended_at IS NULL AND said = NEW.said AND result IS NOT (SELECT result FROM step WHERE id = NEW.id);
  UPDATE memory SET times = times + 1, last_at = CURRENT_TIMESTAMP
    WHERE ended_at IS NULL AND said = NEW.said AND result IS (SELECT result FROM step WHERE id = NEW.id);
  INSERT INTO memory (run, neuron, said, result)
    SELECT NEW.run, NEW.neuron, NEW.said, s.result FROM step s WHERE s.id = NEW.id
      AND NOT EXISTS (SELECT 1 FROM memory WHERE ended_at IS NULL AND said = NEW.said AND result IS s.result);
END;
