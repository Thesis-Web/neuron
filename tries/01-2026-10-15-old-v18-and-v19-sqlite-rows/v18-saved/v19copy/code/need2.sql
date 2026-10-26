-- two values are needed: the newest value held is the first; wait for the next one
INSERT INTO wait (op, a, ear)
  SELECT :ME:, (SELECT h.neuron FROM held h WHERE h.ear = s.ear AND h.used IS NULL ORDER BY h.id DESC LIMIT 1), s.ear
  FROM step s WHERE s.id = :S: AND s.a IS NULL AND s.b IS NULL AND s.ear IS NOT NULL;
UPDATE held SET used = :S:
  WHERE id = (SELECT h.id FROM held h JOIN step s ON h.ear = s.ear
              WHERE s.id = :S: AND s.a IS NULL AND s.b IS NULL AND h.used IS NULL
              ORDER BY h.id DESC LIMIT 1);
