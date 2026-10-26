-- stop: the run ends here. What is held is said; anything still waiting says what it needs.
INSERT INTO out (ear, neuron, at)
  SELECT s.ear, (SELECT h.neuron FROM held h WHERE h.ear = s.ear AND h.used IS NULL ORDER BY h.id DESC LIMIT 1),
         (SELECT max(id) FROM TIMELINE)
  FROM step s WHERE s.id = :S: AND s.ear IS NOT NULL;
INSERT INTO need (ear, neuron, at)
  SELECT w.ear, w.op, (SELECT max(id) FROM TIMELINE) FROM wait w JOIN step s ON s.ear = w.ear
  WHERE s.id = :S: AND w.filled IS NULL;
UPDATE wait SET filled = 0 WHERE filled IS NULL AND ear = (SELECT ear FROM step WHERE id = :S:);
