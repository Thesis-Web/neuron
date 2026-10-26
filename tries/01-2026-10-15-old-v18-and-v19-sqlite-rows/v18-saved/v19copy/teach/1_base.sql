-- Teaching, part 1. What the teacher lays once.
-- Each neuron is born the brain's way (a step on neuron 1, the one that makes neurons);
-- the teacher then writes what it does (its long form) and points words at it.

-- the inverse relation: does nothing; a shard between two operations that undo each other uses it as its key
INSERT INTO step (neuron) VALUES (1);
INSERT INTO word VALUES ('inverse', (SELECT max(id) FROM neuron));

-- stop: '.', '?' and the end of a line point here
INSERT INTO step (neuron) VALUES (1);
UPDATE neuron SET does = CAST(readfile('code/stop.sql') AS TEXT) WHERE id = (SELECT max(id) FROM neuron);
INSERT INTO word VALUES ('.', (SELECT max(id) FROM neuron)), ('?', (SELECT max(id) FROM neuron));

-- study: looks for the formula behind an operation's long runs
INSERT INTO step (neuron) VALUES (1);
UPDATE neuron SET does = CAST(readfile('code/study.sql') AS TEXT) WHERE id = (SELECT max(id) FROM neuron);
INSERT INTO word VALUES ('study', (SELECT max(id) FROM neuron));

-- relate: two operations undo each other
INSERT INTO step (neuron) VALUES (1);
UPDATE neuron SET does = replace(CAST(readfile('code/relate.sql') AS TEXT), '#INV#', (SELECT neuron FROM word WHERE text = 'inverse'))
  WHERE id = (SELECT max(id) FROM neuron);
INSERT INTO word VALUES ('relate', (SELECT max(id) FROM neuron));

-- the forms study may try: shapes of two places A and B. The teacher gives the shapes;
-- study, not the teacher, decides which one (if any) an operation is, by balancing its own memories.
INSERT INTO step (neuron) VALUES (1); INSERT INTO form VALUES ((SELECT max(id) FROM neuron), 'A+B');
INSERT INTO step (neuron) VALUES (1); INSERT INTO form VALUES ((SELECT max(id) FROM neuron), 'A-B');
INSERT INTO step (neuron) VALUES (1); INSERT INTO form VALUES ((SELECT max(id) FROM neuron), 'B-A');
INSERT INTO step (neuron) VALUES (1); INSERT INTO form VALUES ((SELECT max(id) FROM neuron), 'A*B');
INSERT INTO step (neuron) VALUES (1); INSERT INTO form VALUES ((SELECT max(id) FROM neuron), 'A*A');
INSERT INTO step (neuron) VALUES (1); INSERT INTO form VALUES ((SELECT max(id) FROM neuron), 'B*B');
INSERT INTO step (neuron) VALUES (1); INSERT INTO form VALUES ((SELECT max(id) FROM neuron), 'A');
INSERT INTO step (neuron) VALUES (1); INSERT INTO form VALUES ((SELECT max(id) FROM neuron), 'B');

-- the pattern a found formula is written into
INSERT INTO pattern VALUES (1,
     CAST(readfile('code/need2.sql') AS TEXT)
  || CAST(readfile('code/formula.sql') AS TEXT)
  || CAST(readfile('code/remember.sql') AS TEXT)
  || CAST(readfile('code/receipt_formula.sql') AS TEXT)
  || CAST(readfile('code/hold.sql') AS TEXT));

-- plus: its long form, taught once (one place up, as many times as the second value counts)
INSERT INTO step (neuron) VALUES (1);
UPDATE neuron SET does = replace(replace(
     CAST(readfile('code/need2.sql') AS TEXT)
  || CAST(readfile('code/shortcut.sql') AS TEXT)
  || CAST(readfile('code/walk_up.sql') AS TEXT)
  || CAST(readfile('code/remember.sql') AS TEXT)
  || CAST(readfile('code/receipt_long.sql') AS TEXT)
  || CAST(readfile('code/lay.sql') AS TEXT)
  || CAST(readfile('code/hold.sql') AS TEXT)
  || CAST(readfile('code/study_hit.sql') AS TEXT),
  '#INV#', (SELECT neuron FROM word WHERE text = 'inverse')),
  '#STUDY#', (SELECT neuron FROM word WHERE text = 'study'))
  WHERE id = (SELECT max(id) FROM neuron);
INSERT INTO word VALUES ('+', (SELECT max(id) FROM neuron));

-- equals: do two sides land on the same neuron
INSERT INTO step (neuron) VALUES (1);
UPDATE neuron SET does = CAST(readfile('code/need2.sql') AS TEXT) || CAST(readfile('code/equals.sql') AS TEXT)
  WHERE id = (SELECT max(id) FROM neuron);
INSERT INTO word VALUES ('=', (SELECT max(id) FROM neuron));

-- every taught meaning is kept as the first version of what that neuron does
INSERT INTO meaning (neuron, does, from_at)
  SELECT id, does, (SELECT max(id) FROM TIMELINE) FROM neuron
  WHERE does IS NOT NULL AND id NOT IN (SELECT neuron FROM meaning);
