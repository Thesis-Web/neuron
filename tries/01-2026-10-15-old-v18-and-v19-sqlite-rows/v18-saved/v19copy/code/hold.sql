-- the answer is held for whatever comes next; a run that could not finish says what it needs
INSERT INTO held (neuron, ear) SELECT c, ear FROM step WHERE id = :S: AND c IS NOT NULL AND ear IS NOT NULL;
INSERT INTO need (ear, neuron, at)
  SELECT ear, :ME:, (SELECT max(id) FROM TIMELINE) FROM step
  WHERE id = :S: AND ear IS NOT NULL AND c IS NULL AND NOT (a IS NULL AND b IS NULL);
