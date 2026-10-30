-- lean-hop.sql (2026-10-30): the hop laid again with every effect kept and the redundancy gone. What changes: the landing carries its key
-- (kb, kn: the nearest symbols that are not the space, before and after) so land_go does not look it up eight times; one paste through
-- mother finds the shard, bumps its times and brings back shard, call and spawn in one answer (UPDATE ... RETURNING); the shard is laid
-- and the counter bumped only when that paste found nothing; the hit row is written from the answer without a second lookup. The receipt,
-- the ended, the next landing, the birth path (newgate, born, via), the calls and spawns, the build spans and the span to mother are the
-- same statements as before. A landing written by the old hit_go (kb NULL) still works: the key is looked up as before.
ALTER TABLE land ADD COLUMN kb INTEGER;
ALTER TABLE land ADD COLUMN kn INTEGER;
ALTER TABLE hit ADD COLUMN kb INTEGER;
ALTER TABLE hit ADD COLUMN kn INTEGER;
CREATE TABLE IF NOT EXISTS step (k INTEGER PRIMARY KEY CHECK (k = 1), v TEXT);
ALTER TABLE hop ADD COLUMN p7;
ALTER TABLE hop ADD COLUMN p8;
DROP TRIGGER land_go;
CREATE TRIGGER land_go AFTER INSERT ON land BEGIN
  INSERT OR REPLACE INTO step (k, v) VALUES (1, mother('UPDATE ' || 'main."' || NEW.gate || '"' || ' SET times = times + 1 WHERE before IS ? AND trigger IS ? RETURNING shard, call, spawn',
    (CASE WHEN NEW.pos = 0 OR NEW.via = 1 OR NEW.gate = 3 THEN NULL ELSE coalesce(NEW.kb, (SELECT gate FROM seq WHERE run = NEW.run AND pos < NEW.pos AND gate <> 3 ORDER BY pos DESC LIMIT 1), (SELECT arrival FROM run WHERE id = NEW.run)) END),
    (CASE WHEN NEW.pos = 0 OR NEW.via = 1 OR NEW.gate = 3 THEN NULL WHEN NEW.kn IS NULL THEN (SELECT gate FROM seq WHERE run = NEW.run AND pos > NEW.pos AND gate <> 3 ORDER BY pos LIMIT 1) WHEN NEW.kn = 0 THEN NULL ELSE NEW.kn END)));
  INSERT OR REPLACE INTO step (k, v) SELECT 1, mother('INSERT INTO ' || 'main."' || NEW.gate || '"' || ' (shard, before, trigger, times) SELECT n + 1, ?, ?, 1 FROM main.shards RETURNING shard, call, spawn',
    (CASE WHEN NEW.pos = 0 OR NEW.via = 1 OR NEW.gate = 3 THEN NULL ELSE coalesce(NEW.kb, (SELECT gate FROM seq WHERE run = NEW.run AND pos < NEW.pos AND gate <> 3 ORDER BY pos DESC LIMIT 1), (SELECT arrival FROM run WHERE id = NEW.run)) END),
    (CASE WHEN NEW.pos = 0 OR NEW.via = 1 OR NEW.gate = 3 THEN NULL WHEN NEW.kn IS NULL THEN (SELECT gate FROM seq WHERE run = NEW.run AND pos > NEW.pos AND gate <> 3 ORDER BY pos LIMIT 1) WHEN NEW.kn = 0 THEN NULL ELSE NEW.kn END))
    WHERE (SELECT v FROM step WHERE k = 1) = 'ok';
  UPDATE shards SET n = n + 1 WHERE (SELECT v FROM step WHERE k = 1) <> 'ok' AND CAST(substr((SELECT v FROM step WHERE k = 1), 1, instr((SELECT v FROM step WHERE k = 1), ' | ') - 1) AS INTEGER) = n + 1;
  INSERT INTO hit (run, pos, gate, before, next, via, had, shard, call, spawn, kb, kn)
    SELECT NEW.run, NEW.pos, NEW.gate, NEW.before, NEW.next, NEW.via,
      (CASE WHEN NEW.next IS NULL THEN 0 WHEN EXISTS (SELECT 1 FROM pragma_table_info(CAST(NEW.next AS TEXT), 'main')) THEN 1 ELSE 0 END),
      CAST(substr(v, 1, instr(v, ' | ') - 1) AS INTEGER),
      nullif(substr(v, instr(v, ' | ') + 3, instr(substr(v, instr(v, ' | ') + 3), ' | ') - 1), ''),
      nullif(substr(substr(v, instr(v, ' | ') + 3), instr(substr(v, instr(v, ' | ') + 3), ' | ') + 3), ''),
      (CASE WHEN NEW.pos = 0 OR NEW.via = 1 OR NEW.gate = 3 THEN NULL ELSE coalesce(NEW.kb, (SELECT gate FROM seq WHERE run = NEW.run AND pos < NEW.pos AND gate <> 3 ORDER BY pos DESC LIMIT 1), (SELECT arrival FROM run WHERE id = NEW.run)) END),
      (CASE WHEN NEW.pos = 0 OR NEW.via = 1 OR NEW.gate = 3 THEN NULL WHEN NEW.kn IS NULL THEN coalesce((SELECT gate FROM seq WHERE run = NEW.run AND pos > NEW.pos AND gate <> 3 ORDER BY pos LIMIT 1), 0) WHEN NEW.kn = 0 THEN NULL ELSE NEW.kn END)
    FROM step WHERE k = 1 AND v <> 'ok' AND v NOT LIKE 'error:%';
END;
DROP TRIGGER hit_go;
CREATE TRIGGER hit_go AFTER INSERT ON hit BEGIN
  INSERT INTO run_receipt (run, pos, gate, shard) VALUES (NEW.run, NEW.pos, NEW.gate, NEW.shard);
  INSERT INTO hop (text, p1, p2, p3) SELECT 'INSERT INTO main.ended (run, gate, shard) VALUES (?, ?, ?)', NEW.run, NEW.gate, NEW.shard WHERE NEW.next IS NULL AND NEW.via = 0;
  INSERT INTO hop (text, p1, p2, p3, p4, p5, p6, p7) SELECT 'INSERT INTO main.land (run, pos, gate, before, next, via, kb, kn) VALUES (?, ?, ?, ?, ?, 0, ?, ?)', NEW.run, NEW.pos + 1, NEW.next, (CASE WHEN NEW.via = 1 THEN NEW.before ELSE NEW.gate END), (SELECT gate FROM seq WHERE run = NEW.run AND pos = NEW.pos + 2), (CASE WHEN NEW.via = 1 THEN NEW.kb WHEN NEW.gate = 3 THEN NEW.kb ELSE NEW.gate END), (CASE WHEN NEW.next = 3 THEN coalesce(NEW.kn, 0) ELSE coalesce((SELECT gate FROM seq WHERE run = NEW.run AND pos > NEW.pos + 1 AND gate <> 3 ORDER BY pos LIMIT 1), 0) END) WHERE NEW.next IS NOT NULL AND (NEW.via = 1 OR NEW.had = 1);
  INSERT OR REPLACE INTO run_sheet (run, cell, state, value) SELECT NEW.run, 21, 1, NEW.next WHERE NEW.next IS NOT NULL AND NEW.via = 0 AND NEW.had = 0;
  INSERT INTO hop (text, p1, p2, p3, p4, p5, p6) SELECT 'INSERT INTO main.land (run, pos, gate, before, next, via) VALUES (?, ?, ?, ?, ?, ?)', NEW.run, NEW.pos, 16, NEW.gate, NEW.next, 1 WHERE NEW.next IS NOT NULL AND NEW.via = 0 AND NEW.had = 0;
  INSERT INTO hop (text, p1, p2, p3) SELECT 'INSERT INTO main.replay (parent, source, kind) VALUES (?, ?, ?)', NEW.run, NEW.spawn, 2 WHERE NEW.spawn IS NOT NULL;
  INSERT INTO hop (text, p1, p2, p3) SELECT 'INSERT INTO main.replay (parent, source, kind) VALUES (?, ?, ?)', NEW.run, NEW.call, 1 WHERE NEW.call IS NOT NULL;
  INSERT INTO build_span (run, pos) SELECT NEW.run, NEW.pos WHERE NEW.gate = 29 AND NEW.via = 0 AND NOT EXISTS (SELECT 1 FROM build_span WHERE run = NEW.run);
  DELETE FROM build_span WHERE run = NEW.run AND NEW.gate = 29 AND NEW.via = 0 AND NEW.pos > pos AND EXISTS (SELECT 1 FROM build_span WHERE run = NEW.run AND pos < NEW.pos);
  INSERT INTO out_mother (run, cell, gate, at, text) SELECT NEW.run, 22, 29, (SELECT at FROM run WHERE id = NEW.run), (SELECT group_concat(piece, '') FROM (SELECT coalesce((SELECT value FROM run_sheet WHERE run = NEW.run AND cell = s.gate AND state = 1), (SELECT value FROM run_sheet WHERE run = (SELECT parent FROM run WHERE id = NEW.run) AND cell = s.gate AND state = 1), (SELECT value FROM run_sheet WHERE run = (SELECT parent FROM run WHERE id = (SELECT parent FROM run WHERE id = NEW.run)) AND cell = s.gate AND state = 1), l.symbol) AS piece FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = NEW.run AND s.pos > b.pos AND s.pos < NEW.pos ORDER BY s.pos)) FROM (SELECT pos FROM (SELECT max(r.pos) AS pos FROM run_receipt r WHERE r.run = NEW.run AND r.gate = 29 AND r.pos < NEW.pos)) b WHERE NEW.gate = 29 AND NEW.via = 0 AND b.pos IS NOT NULL AND NOT EXISTS (SELECT 1 FROM build_span WHERE run = NEW.run);
END;
