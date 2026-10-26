#!/usr/bin/env python3
# gen_egg3.py: writes egg.sql, the hand-laid part of the brain, from the owner's words of 2026-10-19/20 and the
# reference draft. Hand-laid: the ear (input), the encoder, the shard counter, the receipt, the sheet; the physics
# neurons heard, said, hop, born, fire, end, build; and one neuron for every token of the born run, so the brain can
# type its own CREATE ("WE WILL HAND LAY ALL THOSE SAME WORDS AS NODES SO THE BRAINS CAN LAY IT'S OWN TABLES").
# Every table a neuron owns is named by a gate number; the encoder is the only table that holds a word.
# Every write that happens while a deeper hop is still running goes to mother as its own statement (SQLite keeps an
# INSERT's cursor open until its statement ends).
import re, sys

def tokens(s):
    return re.findall(r'[A-Za-z_]+|[^A-Za-z_]', s)

def gate_trigger(dna, gate):
    # the one trigger of a neuron, on its gate view: hit the DNA row (arrival, remainder) if it exists, write it if
    # not (shard = the next number of the one sequence), then hand the run to hop. Same text for every neuron.
    return (f'CREATE TRIGGER "{gate}" INSTEAD OF INSERT ON "{gate}" BEGIN '
            f"SELECT mother ( 'INSERT INTO \"{dna}\" ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) "
            f"|| ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM \"{dna}\" WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; "
            f"SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM \"{dna}\" WHERE shard = n + 1 )' ) ; "
            f'INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , {gate} , NEW.arrival , NEW.remainder , NEW.rest ) ; END')

# The born run, exactly as the owner types it (one line). "var x" reads cell x. The cells gate, dna, def, mem are the
# four gate numbers born wrote: the missing gate, its DNA table, its definition node, its memory node.
BORN = ('BUILD CREATE TABLE "var dna" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ; '
        'CREATE VIEW "var gate" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "var dna" ; '
        + gate_trigger('var dna', 'var gate') + ' ; '
        'CREATE TABLE "var def" ( id INTEGER PRIMARY KEY , run INTEGER ) ; '
        'CREATE TABLE "var mem" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ; '
        'INSERT INTO "var dna" ( shard , trigger ) SELECT n + 1 , var def FROM shards ; UPDATE shards SET n = n + 1 ; BUILD')

PHYSICS = ['heard', 'said', 'hop', 'born', 'fire', 'end', 'build']
word_neurons = []
for w in ['BUILD', 'var'] + list('0123456789') + tokens(BORN):
    if w not in word_neurons and w not in PHYSICS:
        word_neurons.append(w)

out = []
E = out.append
def sq(s): return "'" + s.replace("'", "''") + "'"
gate = {}
n = 0
def enc(word):
    global n
    n += 1; gate[word] = n
    E(f"INSERT INTO encoder (gate, word) VALUES ({n}, {sq(word)});")
    return n

def neuron(word):
    # a neuron: gate view "<N>" (the entry), DNA table "<N+1>", definition node "<N+2>", memory node "<N+3>", the one
    # gate trigger, and the first shard pointing at the definition node. Only the encoder knows which number is which.
    # The text is spaced exactly as the born run types it, so a hand-laid neuron and a born one read the same.
    g = enc(word); d = enc(word + '.dna'); df = enc(word + '.definition'); m = enc(word + '.memory')
    E(f'CREATE TABLE "{d}" ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ;')
    E(f'CREATE VIEW "{g}" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM "{d}" ;')
    E(gate_trigger(d, g) + ' ;')
    E(f'CREATE TABLE "{df}" ( id INTEGER PRIMARY KEY , run INTEGER ) ;')
    E(f'CREATE TABLE "{m}" ( id INTEGER PRIMARY KEY , run INTEGER , shard INTEGER ) ;')
    E(f'INSERT INTO "{d}" (shard, trigger) SELECT n + 1, {df} FROM shards; UPDATE shards SET n = n + 1;')
    E('')
    return g

E('-- egg.sql: the hand-laid part of the brain. Laid once. Everything else is typed at the prompt.')
E("-- Made from the owner's words of 2026-10-19/20 (see the build sheet).")
E('PRAGMA recursive_triggers = ON;')
E('')
E('-- the ear, the encoder, the one shard counter, the receipt, the sheet')
E('CREATE TABLE input (id INTEGER PRIMARY KEY, parent INTEGER, arrival INTEGER, gates TEXT, text TEXT);')
E('CREATE TABLE encoder (gate INTEGER PRIMARY KEY, word TEXT NOT NULL UNIQUE);')
E('CREATE TABLE shards (n INTEGER NOT NULL);')
E('INSERT INTO shards VALUES (0);')
E('CREATE TABLE receipt (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER);')
E('CREATE INDEX receipt_run ON receipt (run, gate);')
E('CREATE TABLE sheet (id INTEGER PRIMARY KEY, run INTEGER, name INTEGER, value);')
E('CREATE INDEX sheet_name ON sheet (name, run);')
E('')
E('-- physics neurons: heard and said (where a line arrives from), hop, born, fire, end, build. Each is also a word')
H = neuron('heard'); S_ = neuron('said'); HOP = neuron('hop'); BORN_G = neuron('born'); FIRE = neuron('fire'); END = neuron('end'); BLD = neuron('build')
E('-- the gates of the physics: views with no table under them, so a hand-off holds no cursor open while the next hop runs')
E('CREATE VIEW hop AS SELECT NULL AS run, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest;')
E('CREATE VIEW born AS SELECT NULL AS run, NULL AS gate;')
E('CREATE VIEW fire AS SELECT NULL AS run, NULL AS target, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest, NULL AS shard;')
E('CREATE VIEW build AS SELECT NULL AS run;')
E('')
E('-- BUILD, var, the digits 0 to 9 (draft §3.9), and every token of the born run')
for w in word_neurons:
    neuron(w)
K = gate['BUILD']; SP = gate[' ']
BM = gate['born.memory']; EM = gate['end.memory']
C = {w: gate[w] for w in ['run', 'gate', 'dna', 'def', 'mem', 'arrival', 'remainder', 'rest', 'shard']}   # cell names are these words' gates
E('')

head = "substr(NEW.rest || ' ', 1, instr(NEW.rest || ' ', ' ') - 1)"
tail = "trim(substr(NEW.rest || ' ', instr(NEW.rest || ' ', ' ') + 1))"
nul = lambda x: f"coalesce({x}, 'NULL')"
dna_of = "(SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.dna')"
mem_of = lambda g: f"(SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = {g}) || '.memory')"
E("-- the hop: writes the receipt; fires what the row's trigger column names; closes a BUILD pair; at the end of a run that arrived from heard or a source (not from said, not from build) fires end; births a missing gate; lands on the next gate")
E(f"""CREATE TRIGGER hop_go INSTEAD OF INSERT ON hop BEGIN
  SELECT mother('INSERT INTO receipt (run, gate, shard) SELECT ' || NEW.run || ', ' || NEW.gate || ', shard FROM "' || {dna_of} || '" WHERE arrival IS ' || {nul('NEW.arrival')} || ' AND remainder IS ' || {nul('NEW.remainder')});
  SELECT mother('INSERT INTO fire (run, target, gate, arrival, remainder, rest, shard) SELECT ' || NEW.run || ', trigger, ' || NEW.gate || ', ' || {nul('NEW.arrival')} || ', ' || {nul('NEW.remainder')} || ', ' || coalesce(quote(NEW.rest), 'NULL') || ', shard FROM "' || {dna_of} || '" WHERE arrival IS ' || {nul('NEW.arrival')} || ' AND remainder IS ' || {nul('NEW.remainder')} || ' AND trigger IS NOT NULL');
  SELECT mother('INSERT INTO build (run) VALUES (' || NEW.run || ')') WHERE NEW.gate = {K} AND (SELECT count(*) FROM receipt WHERE run = NEW.run AND gate = {K}) % 2 = 0;
  SELECT mother('INSERT INTO fire (run, target, gate, arrival, remainder, rest, shard) SELECT ' || NEW.run || ', {END}, ' || NEW.gate || ', ' || {nul('NEW.arrival')} || ', NULL, NULL, shard FROM "' || {dna_of} || '" WHERE arrival IS ' || {nul('NEW.arrival')} || ' AND remainder IS NULL') WHERE NEW.remainder IS NULL AND (SELECT arrival FROM input WHERE id = NEW.run) NOT IN ({S_}, {BLD});
  SELECT mother('INSERT INTO born (run, gate) SELECT ' || NEW.run || ', ' || NEW.remainder || ' WHERE NOT EXISTS (SELECT 1 FROM sqlite_master WHERE type = ''view'' AND name = ''' || NEW.remainder || ''')') WHERE NEW.remainder IS NOT NULL;
  SELECT mother('INSERT INTO "' || NEW.remainder || '" (run, arrival, remainder, rest) VALUES (' || NEW.run || ', ' || NEW.gate || ', ' || coalesce(nullif({head}, ''), 'NULL') || ', ' || coalesce(quote(nullif({tail}, '')), 'NULL') || ')') WHERE NEW.remainder IS NOT NULL;
END;""")
E('')
E("-- build: the second BUILD of a pair landed. The words between the two BUILDs are read back with the var cells filled (this run's cells first, then its parents') and handed to mother; her answer comes back into the brain as a run")
E(f"""CREATE TRIGGER build_go INSTEAD OF INSERT ON build BEGIN
  SELECT mother('INSERT INTO input (text, parent, arrival) VALUES (' || quote(mother(t)) || ', ' || NEW.run || ', {BLD})') FROM (SELECT (
    WITH RECURSIVE up(id) AS (SELECT NEW.run UNION ALL SELECT i.parent FROM input i JOIN up ON i.id = up.id WHERE i.parent IS NOT NULL)
    SELECT group_concat(w, '') FROM (
      SELECT CASE WHEN p2 = 'var' AND p1 = ' ' THEN coalesce((SELECT value FROM sheet s WHERE s.name = g AND s.run IN (SELECT id FROM up) ORDER BY (s.run = NEW.run) DESC, s.id DESC LIMIT 1), 'var ' || word)
                  WHEN word = 'var' AND n1 = ' ' THEN '' WHEN p1 = 'var' AND word = ' ' THEN '' ELSE word END AS w
      FROM (SELECT e.word, e.gate AS g, lag(e.word, 1) OVER (ORDER BY r.id) AS p1, lag(e.word, 2) OVER (ORDER BY r.id) AS p2, lead(e.word, 1) OVER (ORDER BY r.id) AS n1, r.id
            FROM receipt r JOIN encoder e ON e.gate = r.gate
            WHERE r.run = NEW.run AND r.gate <> {K}
              AND r.id > (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {K} AND id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {K}))
              AND r.id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {K})) ORDER BY id)) AS t);
END;""")
E('')
E("-- born: a gate with no neuron. It gives the new neuron's three tables their gate numbers in the encoder, writes the four numbers as cells, then fires born's own run if one is bound")
E(f"""CREATE TRIGGER born_go INSTEAD OF INSERT ON born BEGIN
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.dna' FROM encoder WHERE gate = NEW.gate;
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.definition' FROM encoder WHERE gate = NEW.gate;
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.memory' FROM encoder WHERE gate = NEW.gate;
  INSERT INTO sheet (run, name, value) VALUES
    (NEW.run, {C['gate']}, NEW.gate),
    (NEW.run, {C['dna']}, (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.dna')),
    (NEW.run, {C['def']}, (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.definition')),
    (NEW.run, {C['mem']}, (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.memory'));
  SELECT mother('INSERT INTO fire (run, target, gate) SELECT ' || NEW.run || ', {BORN_G}, ' || NEW.gate || ' WHERE EXISTS (SELECT 1 FROM "{BM}" WHERE shard IS NULL)');
END;""")
E('')
E("-- fire: a DNA row's trigger column named a neuron (or the run ended: target end). The run, the row's gate, arrival, remainder, rest and shard are written as cells (a value that is NULL writes no cell); the neuron's formula, the newest run bound in its memory node (shard NULL), is typed again as a sub-run of this run, arriving from said")
E(f"""CREATE TRIGGER fire_go INSTEAD OF INSERT ON fire BEGIN
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['run']}, NEW.run WHERE NEW.run IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['gate']}, NEW.gate WHERE NEW.gate IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['arrival']}, NEW.arrival WHERE NEW.arrival IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['remainder']}, NEW.remainder WHERE NEW.remainder IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['rest']}, NEW.rest WHERE NEW.rest IS NOT NULL;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, {C['shard']}, NEW.shard WHERE NEW.shard IS NOT NULL;
  SELECT mother('INSERT INTO input (gates, parent, arrival) SELECT (SELECT group_concat(gate, '' '') FROM (SELECT gate FROM receipt WHERE run = (SELECT run FROM "' || {mem_of('NEW.target')} || '" WHERE shard IS NULL ORDER BY id DESC LIMIT 1) ORDER BY id)), ' || NEW.run || ', {S_} WHERE EXISTS (SELECT 1 FROM "' || {mem_of('NEW.target')} || '" WHERE shard IS NULL)')
    WHERE EXISTS (SELECT 1 FROM encoder WHERE gate = {mem_of('NEW.target')});
END;""")
E('')
E("-- the ear: a line with text is encoded to gates (a word is a run of letters and _; every digit and every other character, space included, is its own neuron), new words get a gate, the text is let go; a line that comes as gates (a replay) keeps them. Then the run hops from where it arrived (heard, said, a source, build) to its first gate")
E(f"""CREATE TRIGGER ear AFTER INSERT ON input BEGIN
  INSERT OR IGNORE INTO encoder (word)
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c))
    SELECT group_concat(ch, '') FROM t WHERE NEW.text IS NOT NULL GROUP BY tok;
  UPDATE input SET gates = (
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c)),
    w AS (SELECT tok, group_concat(ch, '') AS word FROM t GROUP BY tok)
    SELECT group_concat(gate, ' ') FROM (SELECT e.gate FROM w JOIN encoder e ON e.word = w.word ORDER BY w.tok)), text = NULL, arrival = coalesce(NEW.arrival, {H}) WHERE id = NEW.id AND NEW.text IS NOT NULL;
  UPDATE input SET arrival = coalesce(NEW.arrival, {H}) WHERE id = NEW.id AND NEW.text IS NULL;
  INSERT INTO hop (run, gate, arrival, remainder, rest)
    SELECT NEW.id, arrival, NULL, CAST(substr(gates || ' ', 1, instr(gates || ' ', ' ') - 1) AS INTEGER), nullif(trim(substr(gates || ' ', instr(gates || ' ', ' ') + 1)), '') FROM input WHERE id = NEW.id AND gates IS NOT NULL AND gates <> '';
END;""")
open(sys.argv[1] if len(sys.argv) > 1 else 'egg.sql', 'w').write('\n'.join(out) + '\n')
open('BORN-RUN.txt', 'w').write(BORN + '\n')
print('egg:', len(out), 'lines;', n, 'gates;', 7 + len(word_neurons), 'neurons;', len(tokens(BORN)), 'tokens in the born run; heard', H, 'said', S_, 'hop', HOP, 'born', BORN_G, 'fire', FIRE, 'end', END, 'build', BLD, 'BUILD', K, 'var', gate['var'], 'space', SP, 'born.memory', BM, 'end.memory', EM, 'cells', C)
