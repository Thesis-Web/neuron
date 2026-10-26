-- the receipt of a formula run: one hop, by the formula meaning
INSERT INTO occurrence (memory, step, at, meaning, shard, hops)
  SELECT m.id, s.id, (SELECT max(id) FROM TIMELINE), (SELECT id FROM meaning WHERE neuron = :ME: AND until_at IS NULL), NULL, 1
  FROM step s JOIN memory m ON m.ended_at IS NULL AND m.op = :ME: AND m.a = s.a AND m.b = s.b AND m.neuron = s.c
  WHERE s.id = :S:;
