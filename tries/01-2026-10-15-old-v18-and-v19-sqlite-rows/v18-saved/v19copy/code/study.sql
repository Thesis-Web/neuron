-- study (a = the operation to study): which form balances every memory of it?
-- Each form is tried on each memory: the form's answer against the remembered answer.
DELETE FROM fit WHERE step = :S:;
INSERT INTO fit (step, form, ok, total)
  SELECT :S:, f.neuron,
         sum(CAST(eval('SELECT ' || replace(replace(f.expr, 'A', '(' || na.gate || ')'), 'B', '(' || nb.gate || ')')) AS INTEGER)
             = CAST(nc.gate AS INTEGER)),
         count(*)
  FROM step s
  JOIN memory m ON m.op = s.a AND m.ended_at IS NULL
  JOIN neuron na ON na.id = m.a JOIN neuron nb ON nb.id = m.b JOIN neuron nc ON nc.id = m.neuron
  CROSS JOIN form f
  WHERE s.id = :S: AND na.gate IS NOT NULL AND nb.gate IS NOT NULL AND nc.gate IS NOT NULL
  GROUP BY f.neuron;
-- adopt only when one form, and only one, balances all of at least three different memories.
-- The long form is not deleted: its meaning row is ended and stays.
UPDATE meaning SET until_at = (SELECT max(id) FROM TIMELINE)
  WHERE until_at IS NULL AND form IS NULL AND neuron = (SELECT a FROM step WHERE id = :S:)
    AND (SELECT count(*) FROM fit WHERE step = :S: AND ok = total AND total >= 3) = 1;
INSERT INTO meaning (neuron, does, form, balanced, from_at)
  SELECT s.a, replace(p.code, '#EXPR#', f.expr), f.neuron, ft.total, (SELECT max(id) FROM TIMELINE)
  FROM step s JOIN fit ft ON ft.step = s.id AND ft.ok = ft.total AND ft.total >= 3
  JOIN form f ON f.neuron = ft.form JOIN pattern p ON p.id = 1
  WHERE s.id = :S:
    AND (SELECT count(*) FROM fit WHERE step = :S: AND ok = total AND total >= 3) = 1
    AND NOT EXISTS (SELECT 1 FROM meaning x WHERE x.neuron = s.a AND x.until_at IS NULL);
UPDATE neuron SET does = (SELECT x.does FROM meaning x WHERE x.neuron = neuron.id AND x.until_at IS NULL)
  WHERE id = (SELECT a FROM step WHERE id = :S:)
    AND EXISTS (SELECT 1 FROM meaning x WHERE x.neuron = neuron.id AND x.until_at IS NULL AND x.form IS NOT NULL);
