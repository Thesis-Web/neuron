-- the receipt of this run: which meaning ran, whether a shard was used, how many hops, and every place it stood on
INSERT INTO occurrence (memory, step, at, meaning, shard, hops)
  SELECT m.id, s.id, (SELECT max(id) FROM TIMELINE),
         (SELECT id FROM meaning WHERE neuron = :ME: AND until_at IS NULL), s.shard,
         CASE WHEN s.shard IS NOT NULL THEN 1 ELSE (SELECT count(*) - 1 FROM walk WHERE step = s.id) END
  FROM step s JOIN memory m ON m.ended_at IS NULL AND m.op = :ME: AND m.a = s.a AND m.b = s.b AND m.neuron = s.c
  WHERE s.id = :S:;
INSERT INTO path (occurrence, n, neuron)
  SELECT o.id, w.n, nn.id FROM occurrence o JOIN walk w ON w.step = o.step JOIN neuron nn ON nn.gate = CAST(w.place AS TEXT)
  WHERE o.step = :S:;
DELETE FROM walk WHERE step = :S:;
