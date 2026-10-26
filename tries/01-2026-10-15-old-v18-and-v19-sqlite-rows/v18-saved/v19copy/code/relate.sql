-- relate (a, b = two operations that undo each other): lay the relation both ways,
-- then back-populate: every shard either one already laid gets its partner from the other. Nothing is retaught.
INSERT INTO dna (neuron, op, rem, dest, born)
  SELECT s.a, #INV#, NULL, s.b, (SELECT max(id) FROM TIMELINE) FROM step s
  WHERE s.id = :S: AND s.a IS NOT NULL AND s.b IS NOT NULL
    AND NOT EXISTS (SELECT 1 FROM dna x WHERE x.neuron = s.a AND x.op = #INV# AND x.dest = s.b);
INSERT INTO dna (neuron, op, rem, dest, born)
  SELECT s.b, #INV#, NULL, s.a, (SELECT max(id) FROM TIMELINE) FROM step s
  WHERE s.id = :S: AND s.a IS NOT NULL AND s.b IS NOT NULL
    AND NOT EXISTS (SELECT 1 FROM dna x WHERE x.neuron = s.b AND x.op = #INV# AND x.dest = s.a);
INSERT INTO dna (neuron, op, rem, dest, born)
  SELECT d.dest, CASE d.op WHEN s.a THEN s.b ELSE s.a END, d.rem, d.neuron, (SELECT max(id) FROM TIMELINE)
  FROM dna d JOIN step s ON s.id = :S: AND d.op IN (s.a, s.b) AND d.rem IS NOT NULL
  WHERE NOT EXISTS (SELECT 1 FROM dna x WHERE x.neuron = d.dest AND x.rem = d.rem
                    AND x.op = CASE d.op WHEN s.a THEN s.b ELSE s.a END);
