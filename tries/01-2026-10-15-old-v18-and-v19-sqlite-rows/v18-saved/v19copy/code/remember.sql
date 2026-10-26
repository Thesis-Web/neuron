-- memory: the same truth again is the same row, one more time; a changed truth ends the old row and starts a new one
UPDATE memory SET ended_at = (SELECT max(id) FROM TIMELINE)
  WHERE ended_at IS NULL AND op = :ME:
    AND a = (SELECT a FROM step WHERE id = :S:) AND b = (SELECT b FROM step WHERE id = :S:)
    AND neuron <> (SELECT c FROM step WHERE id = :S: AND c IS NOT NULL);
UPDATE memory SET times = times + 1, last_at = (SELECT max(id) FROM TIMELINE)
  WHERE ended_at IS NULL AND op = :ME:
    AND a = (SELECT a FROM step WHERE id = :S:) AND b = (SELECT b FROM step WHERE id = :S:)
    AND neuron = (SELECT c FROM step WHERE id = :S:);
INSERT INTO memory (neuron, op, a, b, first_at, last_at)
  SELECT s.c, :ME:, s.a, s.b, (SELECT max(id) FROM TIMELINE), (SELECT max(id) FROM TIMELINE)
  FROM step s WHERE s.id = :S: AND s.c IS NOT NULL
    AND NOT EXISTS (SELECT 1 FROM memory m WHERE m.ended_at IS NULL AND m.op = :ME:
                    AND m.a = s.a AND m.b = s.b AND m.neuron = s.c);
