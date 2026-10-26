-- the shortcut: a shard an earlier run laid for this same hop
UPDATE step SET shard = (SELECT d.id FROM dna d WHERE d.neuron = step.a AND d.op = :ME: AND d.rem = step.b
                         ORDER BY d.times DESC, d.id LIMIT 1)
  WHERE id = :S: AND a IS NOT NULL AND b IS NOT NULL;
UPDATE step SET c = (SELECT d.dest FROM dna d WHERE d.id = step.shard) WHERE id = :S: AND shard IS NOT NULL;
UPDATE dna SET times = times + 1, last = (SELECT max(id) FROM TIMELINE)
  WHERE id = (SELECT shard FROM step WHERE id = :S:);
