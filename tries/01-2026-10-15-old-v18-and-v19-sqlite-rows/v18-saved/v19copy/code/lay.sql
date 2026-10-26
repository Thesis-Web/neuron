-- after the long way: lay the shortcut, then back-populate the shard of the operation that undoes this one
INSERT INTO dna (neuron, op, rem, dest, born)
  SELECT a, :ME:, b, c, (SELECT max(id) FROM TIMELINE) FROM step WHERE id = :S: AND shard IS NULL AND c IS NOT NULL;
INSERT INTO dna (neuron, op, rem, dest, born)
  SELECT s.c, i.dest, s.b, s.a, (SELECT max(id) FROM TIMELINE)
  FROM step s JOIN dna i ON i.neuron = :ME: AND i.op = #INV# AND i.rem IS NULL
  WHERE s.id = :S: AND s.shard IS NULL AND s.c IS NOT NULL
    AND NOT EXISTS (SELECT 1 FROM dna x WHERE x.neuron = s.c AND x.op = i.dest AND x.rem = s.b);
