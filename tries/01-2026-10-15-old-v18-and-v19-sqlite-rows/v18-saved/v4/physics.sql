-- the physics: laid by the skull at EVERY open, in RAM. Working rows (ear, need, step, said) never go into the file.
CREATE TEMP TABLE ear (id INTEGER PRIMARY KEY, line TEXT NOT NULL, heard TEXT NOT NULL DEFAULT '');
CREATE TEMP TABLE need (id INTEGER PRIMARY KEY, word TEXT NOT NULL);
CREATE TEMP TABLE step (id INTEGER PRIMARY KEY, run INTEGER, neuron INTEGER NOT NULL, remainder TEXT NOT NULL);
CREATE TEMP TABLE said (run INTEGER PRIMARY KEY, receipt INTEGER, line TEXT, result TEXT);

-- listen: take the first word off the line (the space is the hop). A known word becomes its number;
-- an unknown word is a need and listening stops; a last word of /build starts the run at /build with everything heard.
CREATE TEMP TRIGGER listen AFTER INSERT ON ear WHEN NEW.line <> '' BEGIN
  INSERT INTO ear (line, heard)
    SELECT ltrim(substr(NEW.line, instr(NEW.line || ' ', ' ') + 1)), ltrim(NEW.heard || ' ' || c.neuron)
    FROM code c WHERE c.word = substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1) AND c.word <> '/build';
  INSERT INTO need (word)
    SELECT substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1)
    WHERE NOT EXISTS (SELECT 1 FROM code WHERE word = substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1));
  INSERT INTO step (neuron, remainder)
    SELECT c.neuron, NEW.heard FROM code c WHERE c.word = '/build' AND NEW.line = '/build' AND NEW.heard <> '';
END;

-- hop: the key is the head of the remainder. A shard from here by that key: walk it again (times + 1). No shard: lay it.
-- Land on its next gate with the rest of the remainder.
CREATE TEMP TRIGGER hop AFTER INSERT ON step WHEN NEW.remainder <> '' BEGIN
  UPDATE dna SET times = times + 1
    WHERE neuron = NEW.neuron AND key = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER);
  INSERT INTO dna (neuron, key, dest)
    SELECT NEW.neuron, c.neuron, c.neuron FROM code c
    WHERE c.neuron = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER)
      AND NOT EXISTS (SELECT 1 FROM dna WHERE neuron = NEW.neuron AND key = c.neuron);
  INSERT INTO step (run, neuron, remainder)
    SELECT coalesce(NEW.run, NEW.id), d.dest, ltrim(substr(NEW.remainder, instr(NEW.remainder || ' ', ' ') + 1))
    FROM dna d WHERE d.neuron = NEW.neuron AND d.key = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER);
END;

-- end: nothing remains. The receipt is written once (the run's numbers); the line is put together once from the run's words;
-- a run that began at /build hands it to the mother. The memory (the only time stamp) counts up on the same truth, a changed
-- answer ends the old one. The timeline gets one row: the receipt number and two key words. Then the working rows are let go.
CREATE TEMP TRIGGER end_of_run AFTER INSERT ON step WHEN NEW.remainder = '' BEGIN
  INSERT OR IGNORE INTO receipt (path) SELECT remainder FROM step WHERE id = NEW.run;
  INSERT INTO said (run, receipt, line)
    SELECT NEW.run, (SELECT r.id FROM receipt r JOIN step s ON s.id = NEW.run WHERE r.path = s.remainder),
           (SELECT group_concat(w, ' ') FROM (SELECT c.word AS w FROM step s JOIN code c ON c.neuron = s.neuron WHERE s.run = NEW.run ORDER BY s.id));
  UPDATE said SET result = mother(line)
    WHERE run = NEW.run AND (SELECT neuron FROM step WHERE id = NEW.run) = (SELECT neuron FROM code WHERE word = '/build');
  UPDATE memory SET ended_at = CURRENT_TIMESTAMP
    WHERE ended_at IS NULL AND receipt = (SELECT receipt FROM said WHERE run = NEW.run) AND result IS NOT (SELECT result FROM said WHERE run = NEW.run);
  UPDATE memory SET times = times + 1, last_at = CURRENT_TIMESTAMP
    WHERE ended_at IS NULL AND receipt = (SELECT receipt FROM said WHERE run = NEW.run) AND result IS (SELECT result FROM said WHERE run = NEW.run);
  INSERT INTO memory (receipt, neuron, result)
    SELECT s.receipt, NEW.neuron, s.result FROM said s WHERE s.run = NEW.run
      AND NOT EXISTS (SELECT 1 FROM memory WHERE ended_at IS NULL AND receipt = s.receipt AND result IS s.result);
  SELECT mother(printf('INSERT INTO TIMELINE (receipt, words) VALUES (%d, %Q)', s.receipt,
                (SELECT word FROM code WHERE neuron = (SELECT neuron FROM step WHERE id = NEW.run)) || ' ' || substr(s.result, 1, instr(s.result || ':', ':') - 1)))
    FROM said s WHERE s.run = NEW.run;
  DELETE FROM said WHERE run = NEW.run;
  DELETE FROM step WHERE run = NEW.run OR id = NEW.run;
  DELETE FROM ear;
END;
