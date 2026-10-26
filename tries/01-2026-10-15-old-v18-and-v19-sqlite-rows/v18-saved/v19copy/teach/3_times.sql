-- Teaching, part 3. Times: its long form (rounds of steps up from zero), taught once.
INSERT INTO step (neuron) VALUES (1);
UPDATE neuron SET does = replace(replace(
     CAST(readfile('code/need2.sql') AS TEXT)
  || CAST(readfile('code/shortcut.sql') AS TEXT)
  || CAST(readfile('code/walk_times.sql') AS TEXT)
  || CAST(readfile('code/remember.sql') AS TEXT)
  || CAST(readfile('code/receipt_long.sql') AS TEXT)
  || CAST(readfile('code/lay.sql') AS TEXT)
  || CAST(readfile('code/hold.sql') AS TEXT)
  || CAST(readfile('code/study_hit.sql') AS TEXT),
  '#INV#', (SELECT neuron FROM word WHERE text = 'inverse')),
  '#STUDY#', (SELECT neuron FROM word WHERE text = 'study'))
  WHERE id = (SELECT max(id) FROM neuron);
INSERT INTO word VALUES ('x', (SELECT max(id) FROM neuron)), ('*', (SELECT max(id) FROM neuron));
INSERT INTO meaning (neuron, does, from_at)
  SELECT id, does, (SELECT max(id) FROM TIMELINE) FROM neuron
  WHERE does IS NOT NULL AND id NOT IN (SELECT neuron FROM meaning);
