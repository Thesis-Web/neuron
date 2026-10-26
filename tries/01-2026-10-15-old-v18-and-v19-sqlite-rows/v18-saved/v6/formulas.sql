-- the formula nodes, told once: from a word, by a key, a head (the long run) and a row with its holes (var, now)
CREATE TEMP TABLE fw (neuron TEXT, key TEXT, head TEXT, row TEXT);
INSERT INTO fw VALUES ('new', 'word',   'INSERT INTO code ( word ) VALUES',            '( var )'),
                      ('new', 'neuron', 'INSERT INTO neuron ( gate , born ) VALUES',   '( var , now )'),
                      ('now', NULL,     'SELECT max ( id ) + 1 FROM TIMELINE',         NULL);
CREATE TEMP TABLE tok AS SELECT fw.rowid AS f, 'head' AS part, j.key AS n, j.value AS w FROM fw, json_each('["' || replace(fw.head, ' ', '","') || '"]') j
  UNION ALL SELECT fw.rowid, 'row', j.key, j.value FROM fw, json_each('["' || replace(fw.row, ' ', '","') || '"]') j WHERE fw.row IS NOT NULL;
INSERT INTO formula (neuron, KEY, head, row)
  SELECT (SELECT id FROM code WHERE word = fw.neuron), (SELECT id FROM code WHERE word = fw.key),
         (SELECT group_concat(id, ' ') FROM (SELECT c.id FROM tok t JOIN code c ON c.word = t.w WHERE t.f = fw.rowid AND t.part = 'head' ORDER BY t.n)),
         (SELECT group_concat(id, ' ') FROM (SELECT c.id FROM tok t JOIN code c ON c.word = t.w WHERE t.f = fw.rowid AND t.part = 'row' ORDER BY t.n))
  FROM fw ORDER BY fw.rowid;
DROP TABLE tok; DROP TABLE fw;
