-- the formula: the place of the answer, worked out from the two places in one step
INSERT OR IGNORE INTO neuron (gate, born)
  SELECT CAST(CAST(eval('SELECT ' || replace(replace('#EXPR#', 'A', '(' || na.gate || ')'), 'B', '(' || nb.gate || ')')) AS INTEGER) AS TEXT),
         (SELECT max(id) FROM TIMELINE)
  FROM step s JOIN neuron na ON na.id = s.a JOIN neuron nb ON nb.id = s.b
  WHERE s.id = :S: AND na.gate IS NOT NULL AND nb.gate IS NOT NULL;
UPDATE step SET c = (
    SELECT n.id FROM neuron n, neuron na, neuron nb
    WHERE na.id = step.a AND nb.id = step.b AND na.gate IS NOT NULL AND nb.gate IS NOT NULL
      AND n.gate = CAST(CAST(eval('SELECT ' || replace(replace('#EXPR#', 'A', '(' || na.gate || ')'), 'B', '(' || nb.gate || ')')) AS INTEGER) AS TEXT))
  WHERE id = :S: AND a IS NOT NULL AND b IS NOT NULL;
