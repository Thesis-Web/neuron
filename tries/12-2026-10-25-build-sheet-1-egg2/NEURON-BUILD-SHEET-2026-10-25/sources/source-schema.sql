CREATE TABLE corpus (word TEXT COLLATE NOCASE, hw TEXT, text TEXT);
CREATE INDEX cw ON corpus(word);
CREATE TABLE inbox (id INTEGER PRIMARY KEY, run INTEGER, word TEXT);
CREATE TABLE outbox (id INTEGER PRIMARY KEY, run INTEGER, word TEXT, hw TEXT, text TEXT);
CREATE TRIGGER work AFTER INSERT ON inbox BEGIN
  INSERT INTO outbox (run, word, hw, text) SELECT NEW.run, NEW.word, hw, text FROM corpus WHERE word = NEW.word;
  DELETE FROM inbox WHERE id = NEW.id;
END;
