-- the bones: laid by hand ONCE. The brain's first run needs them, so it cannot write them itself.

-- every neuron, one numbering. A word neuron has no place (it does not live in the graph); a graph neuron has a place.
CREATE TABLE neuron (id INTEGER PRIMARY KEY, gate TEXT UNIQUE, born INTEGER);

-- the encoder for code: a word points to its neuron. Words live here and nowhere else.
CREATE TABLE code (word TEXT PRIMARY KEY, neuron INTEGER NOT NULL UNIQUE);

-- the word neurons, born before time (no place, no moment), each with its word
CREATE TEMP TABLE w (word TEXT);
INSERT INTO w VALUES ('CREATE'), ('TABLE'), ('('), (')'), (','), (';'), ('INTEGER'), ('PRIMARY'), ('KEY'), ('TEXT'), ('NOT'), ('NULL'), ('DEFAULT'), ('CURRENT_TIMESTAMP'), ('TIMELINE'), ('id'), ('at'), ('receipt'), ('words'), ('/build'), ('INSERT'), ('INTO'), ('neuron'), ('gate'), ('born'), ('VALUES'), ('0'), ('SELECT'), ('max'), ('+'), ('1'), ('FROM');
INSERT INTO neuron (gate, born) SELECT NULL, NULL FROM w;
INSERT INTO code (word, neuron) SELECT w.word, w.rowid FROM w;
DROP TABLE w;

-- dna: from a neuron, by a key (the head of the remainder), to the next gate; times = how often it was walked
CREATE TABLE dna (id INTEGER PRIMARY KEY, neuron INTEGER NOT NULL, key INTEGER NOT NULL, dest INTEGER NOT NULL, times INTEGER NOT NULL DEFAULT 1);
CREATE INDEX dna_hop ON dna (neuron, key);

-- a receipt: a run's path as numbers, written ONCE. The same run again points to the same receipt.
CREATE TABLE receipt (id INTEGER PRIMARY KEY, path TEXT NOT NULL UNIQUE);

-- a memory: a receipt and the mother's answer, on the neuron the run ended on. The only place with time.
CREATE TABLE memory (id INTEGER PRIMARY KEY, receipt INTEGER NOT NULL, neuron INTEGER NOT NULL, result TEXT, times INTEGER NOT NULL DEFAULT 1,
                     first_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, last_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, ended_at TEXT);
