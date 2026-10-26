-- the physics: laid by the skull at EVERY open, in RAM. Working rows (ear, need, step, said) never go into the file.
CREATE TEMP TABLE ear (id INTEGER PRIMARY KEY, line TEXT NOT NULL, heard TEXT NOT NULL DEFAULT '');
CREATE TEMP TABLE need (id INTEGER PRIMARY KEY, word TEXT NOT NULL);
CREATE TEMP TABLE step (id INTEGER PRIMARY KEY, run INTEGER, neuron INTEGER NOT NULL, remainder TEXT NOT NULL);
CREATE TEMP TABLE said (run INTEGER PRIMARY KEY, receipt INTEGER, line TEXT, result TEXT);

-- listen: take the first word off the line (the space is the hop). A line that starts with a formula word goes to the formula instead. A known word becomes its number;
-- an unknown word is a need and listening stops; a last word of /build starts the run at /build with everything heard.
CREATE TEMP TRIGGER listen AFTER INSERT ON ear WHEN NEW.line <> '' AND NOT (NEW.heard = '' AND EXISTS (SELECT 1 FROM formula f JOIN code c ON c.id = f.neuron WHERE c.word = substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1))) BEGIN
  INSERT INTO ear (line, heard)
    SELECT ltrim(substr(NEW.line, instr(NEW.line || ' ', ' ') + 1)), ltrim(NEW.heard || ' ' || c.id)
    FROM code c WHERE c.word = substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1) AND c.word <> '/build';
  INSERT INTO need (word)
    SELECT substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1)
    WHERE NOT EXISTS (SELECT 1 FROM code WHERE word = substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1));
  INSERT INTO step (neuron, remainder)
    SELECT c.id, NEW.heard FROM code c WHERE c.word = '/build' AND NEW.line = '/build' AND NEW.heard <> '';
END;

-- hop: the key is the head of the remainder. A shard from here by that key: walk it again (times + 1). No shard: lay it.
-- Land on its next gate with the rest of the remainder.
CREATE TEMP TRIGGER hop AFTER INSERT ON step WHEN NEW.remainder <> '' BEGIN
  UPDATE dna SET times = times + 1
    WHERE neuron = NEW.neuron AND key = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER);
  INSERT INTO dna (neuron, key, dest)
    SELECT NEW.neuron, c.id, c.id FROM code c
    WHERE c.id = CAST(substr(NEW.remainder, 1, instr(NEW.remainder || ' ', ' ') - 1) AS INTEGER)
      AND NOT EXISTS (SELECT 1 FROM dna WHERE neuron = NEW.neuron AND key = c.id);
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
           (SELECT group_concat(w, ' ') FROM (SELECT c.word AS w FROM step s JOIN code c ON c.id = s.neuron WHERE s.run = NEW.run ORDER BY s.id));
  UPDATE said SET result = mother(line)
    WHERE run = NEW.run AND (SELECT neuron FROM step WHERE id = NEW.run) = (SELECT id FROM code WHERE word = '/build');
  UPDATE memory SET ended_at = CURRENT_TIMESTAMP
    WHERE ended_at IS NULL AND receipt = (SELECT receipt FROM said WHERE run = NEW.run) AND result IS NOT (SELECT result FROM said WHERE run = NEW.run);
  UPDATE memory SET times = times + 1, last_at = CURRENT_TIMESTAMP
    WHERE ended_at IS NULL AND receipt = (SELECT receipt FROM said WHERE run = NEW.run) AND result IS (SELECT result FROM said WHERE run = NEW.run);
  INSERT INTO memory (receipt, neuron, result)
    SELECT s.receipt, NEW.neuron, s.result FROM said s WHERE s.run = NEW.run
      AND NOT EXISTS (SELECT 1 FROM memory WHERE ended_at IS NULL AND receipt = s.receipt AND result IS s.result);
  SELECT mother(printf('INSERT INTO TIMELINE (receipt, words) VALUES (%d, %Q)', s.receipt,
                (SELECT word FROM code WHERE id = (SELECT neuron FROM step WHERE id = NEW.run)) || coalesce(' ' || substr(s.result, 1, instr(s.result || ':', ':') - 1), '')))
    FROM said s WHERE s.run = NEW.run;
  DELETE FROM said WHERE run = NEW.run;
  DELETE FROM step WHERE run = NEW.run OR id = NEW.run;
  DELETE FROM ear;
END;

-- a formula run: from a formula word, by a key (the next word), the rest of the line up to /build is the remainder: the values.
CREATE TEMP TABLE frun (id INTEGER PRIMARY KEY, formula INTEGER NOT NULL, word INTEGER NOT NULL, vals TEXT NOT NULL, moment INTEGER, line TEXT, result TEXT, receipt INTEGER);

-- hear a formula line: first word = a formula word; its next word picks the formula when one is keyed by it.
CREATE TEMP TRIGGER hear_formula AFTER INSERT ON ear
WHEN NEW.heard = '' AND NEW.line LIKE '% /build'
 AND EXISTS (SELECT 1 FROM formula f JOIN code c ON c.id = f.neuron WHERE c.word = substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1))
BEGIN
  INSERT INTO frun (formula, word, vals)
    SELECT f.id, f.neuron,
           CASE WHEN f.KEY IS NULL THEN trim(substr(r1, 1, length(r1) - 6))
                ELSE trim(substr(substr(r1, instr(r1 || ' ', ' ') + 1), 1, length(substr(r1, instr(r1 || ' ', ' ') + 1)) - 6)) END
    FROM (SELECT ltrim(substr(NEW.line, instr(NEW.line || ' ', ' ') + 1)) AS r1, substr(NEW.line, 1, instr(NEW.line || ' ', ' ') - 1) AS t1) x
    JOIN code c ON c.word = x.t1 JOIN formula f ON f.neuron = c.id
    WHERE f.KEY = (SELECT id FROM code WHERE word = substr(x.r1, 1, instr(x.r1 || ' ', ' ') - 1))
       OR (f.KEY IS NULL AND NOT EXISTS (SELECT 1 FROM formula g WHERE g.neuron = c.id
                                          AND g.KEY = (SELECT id FROM code WHERE word = substr(x.r1, 1, instr(x.r1 || ' ', ' ') - 1))))
    LIMIT 1;
  DELETE FROM ear;
END;

-- the formula run. The long way once: the first time, its words are walked one by one (shards, a receipt, a memory).
-- Then the shortcut: the head, and one row per value with var = the value and now = this run's moment, handed to the mother.
-- A formula with no row (now) answers the moment itself. The receipt, the memory and the timeline as for any run.
CREATE TEMP TRIGGER formula_run AFTER INSERT ON frun BEGIN
  INSERT INTO step (neuron, remainder)
    SELECT CAST(substr(p, 1, instr(p || ' ', ' ') - 1) AS INTEGER), ltrim(substr(p, instr(p || ' ', ' ') + 1))
    FROM (SELECT f.head || coalesce(' ' || f.row, '') AS p FROM formula f WHERE f.id = NEW.formula) x
    WHERE NOT EXISTS (SELECT 1 FROM receipt WHERE path = ltrim(substr(x.p, instr(x.p || ' ', ' ') + 1)));
  UPDATE frun SET moment = (SELECT coalesce(max(id), 0) + 1 FROM TIMELINE) WHERE id = NEW.id;
  UPDATE frun SET line =
      (SELECT group_concat(w, ' ') FROM (SELECT c.word AS w FROM formula f, json_each('[' || replace(f.head, ' ', ',') || ']') j JOIN code c ON c.id = j.value
                                         WHERE f.id = NEW.formula ORDER BY j.key))
      || ' ' ||
      (SELECT group_concat(x, ' , ') FROM (
         SELECT trim(replace(replace(' ' || rw.w || ' ', ' var ', ' ' || quote(v.value) || ' '), ' now ', ' ' || fr.moment || ' ')) AS x
         FROM frun fr,
              (SELECT group_concat(w, ' ') AS w FROM (SELECT c.word AS w FROM formula f, json_each('[' || replace(f.row, ' ', ',') || ']') j JOIN code c ON c.id = j.value
                                                      WHERE f.id = NEW.formula ORDER BY j.key)) rw,
              json_each('["' || replace(replace(fr.vals, '"', ''), ' ', '","') || '"]') v
         WHERE fr.id = NEW.id AND fr.vals <> '' ORDER BY v.key))
      || ' ;'
    WHERE id = NEW.id AND (SELECT row FROM formula WHERE id = NEW.formula) IS NOT NULL;
  UPDATE frun SET result = mother(line) WHERE id = NEW.id AND line IS NOT NULL;
  UPDATE frun SET result = CASE WHEN line IS NULL AND (SELECT row FROM formula WHERE id = NEW.formula) IS NOT NULL THEN 'error: no values' ELSE coalesce(result, 'now ' || moment) END WHERE id = NEW.id;
  INSERT OR IGNORE INTO receipt (path)
    SELECT trim(fr.word || coalesce(' ' || f.KEY, '') || ' ' || (SELECT id FROM code WHERE word = '/build') || ' : ' || fr.vals)
    FROM frun fr JOIN formula f ON f.id = fr.formula WHERE fr.id = NEW.id;
  UPDATE frun SET receipt = (SELECT r.id FROM receipt r, formula f WHERE f.id = NEW.formula
                             AND r.path = trim(frun.word || coalesce(' ' || f.KEY, '') || ' ' || (SELECT id FROM code WHERE word = '/build') || ' : ' || frun.vals))
    WHERE id = NEW.id;
  UPDATE memory SET ended_at = CURRENT_TIMESTAMP
    WHERE ended_at IS NULL AND receipt = (SELECT receipt FROM frun WHERE id = NEW.id) AND result IS NOT (SELECT result FROM frun WHERE id = NEW.id);
  UPDATE memory SET times = times + 1, last_at = CURRENT_TIMESTAMP
    WHERE ended_at IS NULL AND receipt = (SELECT receipt FROM frun WHERE id = NEW.id) AND result IS (SELECT result FROM frun WHERE id = NEW.id);
  INSERT INTO memory (receipt, neuron, result)
    SELECT fr.receipt, (SELECT id FROM code WHERE word = '/build'), fr.result FROM frun fr WHERE fr.id = NEW.id
      AND NOT EXISTS (SELECT 1 FROM memory WHERE ended_at IS NULL AND receipt = fr.receipt AND result IS fr.result);
  INSERT INTO TIMELINE (receipt, words)
    SELECT fr.receipt, (SELECT word FROM code WHERE id = fr.word) || ' ' || substr(fr.result, 1, instr(fr.result || ':', ':') - 1)
    FROM frun fr WHERE fr.id = NEW.id;
  DELETE FROM frun WHERE id = NEW.id;
END;
