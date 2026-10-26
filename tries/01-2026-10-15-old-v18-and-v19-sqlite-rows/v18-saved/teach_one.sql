PRAGMA recursive_triggers = ON;
CREATE TABLE step (id INTEGER PRIMARY KEY, neuron INTEGER NOT NULL, remainder INTEGER, moment INTEGER NOT NULL);
CREATE TRIGGER excite AFTER INSERT ON step WHEN NEW.remainder IS NOT NULL BEGIN
  INSERT INTO TIMELINE (at) VALUES (CURRENT_TIMESTAMP);
  INSERT OR IGNORE INTO neuron (gate, born)
    SELECT CAST(CAST(n.gate AS INTEGER) + NEW.remainder AS TEXT), (SELECT max(id) FROM TIMELINE)
    FROM neuron n WHERE n.id = NEW.neuron
      AND NOT EXISTS (SELECT 1 FROM dna WHERE neuron = NEW.neuron AND key = NEW.remainder);
  INSERT INTO dna (neuron, key, dest, born)
    SELECT NEW.neuron, NEW.remainder, b.id, (SELECT max(id) FROM TIMELINE)
    FROM neuron n JOIN neuron b ON b.gate = CAST(CAST(n.gate AS INTEGER) + NEW.remainder AS TEXT)
    WHERE n.id = NEW.neuron AND NOT EXISTS (SELECT 1 FROM dna WHERE neuron = NEW.neuron AND key = NEW.remainder);
  INSERT INTO step (neuron, remainder, moment)
    SELECT dest, NULL, (SELECT max(id) FROM TIMELINE) FROM dna WHERE neuron = NEW.neuron AND key = NEW.remainder LIMIT 1;
END;
