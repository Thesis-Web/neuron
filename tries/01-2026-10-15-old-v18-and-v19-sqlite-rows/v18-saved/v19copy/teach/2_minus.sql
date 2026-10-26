-- Teaching, part 2. Minus: its long form (one place down), taught once.
INSERT INTO step (neuron) VALUES (1);
UPDATE neuron SET does = replace(replace(
     CAST(readfile('code/need2.sql') AS TEXT)
  || CAST(readfile('code/shortcut.sql') AS TEXT)
  || CAST(readfile('code/walk_down.sql') AS TEXT)
  || CAST(readfile('code/remember.sql') AS TEXT)
  || CAST(readfile('code/receipt_long.sql') AS TEXT)
  || CAST(readfile('code/lay.sql') AS TEXT)
  || CAST(readfile('code/hold.sql') AS TEXT)
  || CAST(readfile('code/study_hit.sql') AS TEXT),
  '#INV#', (SELECT neuron FROM word WHERE text = 'inverse')),
  '#STUDY#', (SELECT neuron FROM word WHERE text = 'study'))
  WHERE id = (SELECT max(id) FROM neuron);
INSERT INTO word VALUES ('-', (SELECT max(id) FROM neuron));
INSERT INTO meaning (neuron, does, from_at)
  SELECT id, does, (SELECT max(id) FROM TIMELINE) FROM neuron
  WHERE does IS NOT NULL AND id NOT IN (SELECT neuron FROM meaning);

-- minus undoes plus: hit relate with the two. The brain lays the relation and back-populates
-- a minus shard for every plus shard it already has. Subtraction of those pairs is never taught.
INSERT INTO step (neuron, a, b) VALUES ((SELECT neuron FROM word WHERE text = 'relate'),
                                        (SELECT neuron FROM word WHERE text = '+'),
                                        (SELECT neuron FROM word WHERE text = '-'));
