-- the long way: one place down, as many times as the second value counts; the run ends when nothing remains.
-- A place with no neuron gets one.
DELETE FROM walk WHERE step = :S:;
WITH RECURSIVE w(n, p, r) AS (
  SELECT 0, CAST(na.gate AS INTEGER), CAST(nb.gate AS INTEGER)
    FROM step s JOIN neuron na ON na.id = s.a JOIN neuron nb ON nb.id = s.b
    WHERE s.id = :S: AND s.c IS NULL AND na.gate IS NOT NULL AND nb.gate IS NOT NULL AND CAST(nb.gate AS INTEGER) >= 0
  UNION ALL
  SELECT n + 1, p - 1, r - 1 FROM w WHERE r > 0
)
INSERT INTO walk (step, n, place) SELECT :S:, n, p FROM w;
INSERT OR IGNORE INTO neuron (gate, born)
  SELECT CAST(place AS TEXT), (SELECT max(id) FROM TIMELINE) FROM walk WHERE step = :S: ORDER BY n;
UPDATE step SET c = (SELECT n.id FROM walk w JOIN neuron n ON n.gate = CAST(w.place AS TEXT)
                     WHERE w.step = :S: ORDER BY w.n DESC LIMIT 1)
  WHERE id = :S: AND c IS NULL;
