-- the bones: laid by hand ONCE. The brain's first run needs them, so it cannot write them itself.

-- the word neurons: the only neurons with words. Each word is one neuron; its number is its gate.
CREATE TABLE code (id INTEGER PRIMARY KEY, word TEXT NOT NULL UNIQUE);
INSERT INTO code (word) VALUES ('CREATE'), ('TABLE'), ('('), (')'), (','), (';'), ('INTEGER'), ('PRIMARY'), ('KEY'), ('TEXT'), ('NOT'), ('NULL'), ('DEFAULT'), ('CURRENT_TIMESTAMP'), ('UNIQUE'), ('TIMELINE'), ('neuron'), ('id'), ('at'), ('gate'), ('born'), ('receipt'), ('words'), ('/build');

-- dna: from a neuron, by a key (the head of the remainder), to the next gate; times = how often it was walked
CREATE TABLE dna (id INTEGER PRIMARY KEY, neuron INTEGER NOT NULL, key INTEGER NOT NULL, dest INTEGER NOT NULL, times INTEGER NOT NULL DEFAULT 1);
CREATE INDEX dna_hop ON dna (neuron, key);

-- a receipt: a run's path as numbers, written ONCE. The same run again points to the same receipt.
CREATE TABLE receipt (id INTEGER PRIMARY KEY, path TEXT NOT NULL UNIQUE);

-- a memory: a receipt and the mother's answer, on the neuron the run ended on. The only place with time.
CREATE TABLE memory (id INTEGER PRIMARY KEY, receipt INTEGER NOT NULL, neuron INTEGER NOT NULL, result TEXT, times INTEGER NOT NULL DEFAULT 1,
                     first_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, last_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, ended_at TEXT);
