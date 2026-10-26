-- the balance: do the two sides land on the same neuron? The left side stays held.
INSERT INTO balance (ear, a, b, ok, at)
  SELECT ear, a, b, a = b, (SELECT max(id) FROM TIMELINE) FROM step WHERE id = :S: AND a IS NOT NULL AND b IS NOT NULL;
INSERT INTO held (neuron, ear)
  SELECT a, ear FROM step WHERE id = :S: AND a IS NOT NULL AND b IS NOT NULL AND ear IS NOT NULL;
INSERT INTO need (ear, neuron, at)
  SELECT ear, :ME:, (SELECT max(id) FROM TIMELINE) FROM step
  WHERE id = :S: AND ear IS NOT NULL AND ((a IS NULL) <> (b IS NULL));
