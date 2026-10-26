#!/usr/bin/env python3
# gen_egg2.py: writes egg.sql, the hand-laid part of the brain, from the owner's words of 2026-10-19/20.
# The egg is: the ear (input), the encoder, one shard counter, the receipt, the sheet, the secondary input,
# the output, the later queue; the physics neurons heard, said, hop, born, fire, end, build; and one neuron for
# every token of the born run, so the brain can lay its own tables ("WE WILL HAND LAY ALL THOSE SAME WORDS AS NODES").
# Every write that happens while a deeper hop is still running goes to mother as its own statement: SQLite keeps an
# INSERT's cursor open until its statement ends, and a chain 2,000 hops deep would otherwise hold thousands open.
import re, sys

def tokens(s):
    return re.findall(r'[A-Za-z_]+|[^A-Za-z_]', s)

def gate_trigger(dna, gate, trig):
    # the one trigger of a neuron, on its gate: hit the DNA row if it exists, write it if not, hand the run to hop
    return (f'CREATE TRIGGER {trig} INSTEAD OF INSERT ON "{gate}" BEGIN '
            f"SELECT mother ( 'INSERT INTO {dna} ( shard , arrival , remainder ) SELECT n + 1 , ' || coalesce ( NEW.arrival , 'NULL' ) || ' , ' || coalesce ( NEW.remainder , 'NULL' ) "
            f"|| ' FROM shards WHERE NOT EXISTS ( SELECT 1 FROM {dna} WHERE arrival IS ' || coalesce ( NEW.arrival , 'NULL' ) || ' AND remainder IS ' || coalesce ( NEW.remainder , 'NULL' ) || ' )' ) ; "
            f"SELECT mother ( 'UPDATE shards SET n = n + 1 WHERE EXISTS ( SELECT 1 FROM {dna} WHERE shard = n + 1 )' ) ; "
            f'INSERT INTO hop ( run , gate , arrival , remainder , rest ) VALUES ( NEW.run , {gate} , NEW.arrival , NEW.remainder , NEW.rest ) ; END')

# The born run, exactly as the owner will type it at the prompt (one line). "var x" reads cell x.
BORN = ('BUILD CREATE TABLE var dna ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ; '
        'CREATE VIEW "var gate" AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM var dna ; '
        + gate_trigger('var dna', 'var gate', 'var trig') + ' ; '
        'CREATE TABLE var def ( id INTEGER PRIMARY KEY , run INTEGER , secondary INTEGER ) ; '
        'CREATE TABLE var mem ( id INTEGER PRIMARY KEY , run INTEGER ) ; '
        'INSERT INTO var dna ( shard , trigger ) SELECT n + 1 , var defgate FROM shards ; UPDATE shards SET n = n + 1 ; BUILD')

# the SQL words the owner named on 10-19 23:03 and 23:27, digits and the letters of table names, plus every token of the born run
EXTRA = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'g', 't', 'd', 'm', 'DROP', 'ALTER', 'DELETE', 'VALUES', 'INTO', 'TEXT', 'ON', 'AFTER', 'WHEN', 'IS', 'AND', 'OR', 'NOT', 'NULL', 'end', 'new', 'next']
PHYSICS = ['heard', 'said', 'hop', 'born', 'fire', 'end', 'build']
word_neurons = []
for w in ['BUILD', 'var'] + EXTRA + tokens(BORN):
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

def std_neuron(word, g):
    # a neuron: DNA table g<N>, gate view "<N>" (the entry), gate trigger t<N>, definition node, memory node, first shard -> definition node
    dg = enc(word + '.definition'); mg = enc(word + '.memory')
    E(f'CREATE TABLE g{g} (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER);')
    E(f'CREATE VIEW "{g}" AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g{g};')
    E(gate_trigger(f'g{g}', g, f't{g}') + ';')
    E(f'CREATE TABLE g{dg} (id INTEGER PRIMARY KEY, run INTEGER, secondary INTEGER);')
    E(f'CREATE TABLE g{mg} (id INTEGER PRIMARY KEY, run INTEGER);')
    E(f'INSERT INTO g{g} (shard, trigger) SELECT n + 1, {dg} FROM shards; UPDATE shards SET n = n + 1;')
    E('')

E('-- egg.sql: the hand-laid part of the brain. Laid once. Everything else is typed at the prompt.')
E("-- Made from the owner's words of 2026-10-19/20 (see NEURON-BUILD-SHEET-2026-10-25.md).")
E('PRAGMA recursive_triggers = ON;')
E('')
E('-- the ear, the encoder, the shard counter, the receipt, the sheet, the secondary input, the output, the later queue')
E('CREATE TABLE input (id INTEGER PRIMARY KEY, text TEXT NOT NULL, parent INTEGER, gates TEXT, answer TEXT);')
E('CREATE TABLE encoder (gate INTEGER PRIMARY KEY, word TEXT NOT NULL UNIQUE);')
E('CREATE TABLE shards (n INTEGER NOT NULL);')
E('INSERT INTO shards VALUES (0);')
E('CREATE TABLE receipt (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER);')
E('CREATE INDEX receipt_run ON receipt (run, gate);')
E('CREATE TABLE sheet (id INTEGER PRIMARY KEY, run INTEGER, name TEXT, value);')
E('CREATE INDEX sheet_name ON sheet (name, run);')
E('CREATE TABLE secondary (id INTEGER PRIMARY KEY, run INTEGER, source TEXT, word TEXT, hw TEXT, text TEXT);')
E('CREATE TABLE output (id INTEGER PRIMARY KEY, run INTEGER, text TEXT);')
E('CREATE INDEX output_run ON output (run);')
E('CREATE TABLE later (id INTEGER PRIMARY KEY, text TEXT);')
E('')
E('-- physics neurons: heard and said (where a line arrives from), hop, born, fire, end, build. Each is also a word, so a typed line may name it')
H = enc('heard'); std_neuron('heard', H)
S_ = enc('said'); std_neuron('said', S_)
HOP = enc('hop'); std_neuron('hop', HOP)
BORN_G = enc('born'); std_neuron('born', BORN_G)
FIRE = enc('fire'); std_neuron('fire', FIRE)
END = enc('end'); std_neuron('end', END)
BLD = enc('build'); std_neuron('build', BLD)
E('-- the gates of the physics: views with no table under them, so a hand-off holds no cursor open while the next hop runs')
E('CREATE VIEW hop AS SELECT NULL AS run, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest;')
E('CREATE VIEW born AS SELECT NULL AS run, NULL AS gate;')
E('CREATE VIEW fire AS SELECT NULL AS run, NULL AS target, NULL AS gate, NULL AS arrival, NULL AS remainder, NULL AS rest;')
E('CREATE VIEW build AS SELECT NULL AS run;')
E('')
E('-- BUILD, var, and every word of the born run')
for w in word_neurons:
    std_neuron(w, enc(w))
K = gate['BUILD']; V = gate['var']; BM = gate['born.memory']; SP = gate[' ']
E('')

head = "substr(NEW.rest || ' ', 1, instr(NEW.rest || ' ', ' ') - 1)"
tail = "trim(substr(NEW.rest || ' ', instr(NEW.rest || ' ', ' ') + 1))"
nul = lambda x: f"coalesce({x}, 'NULL')"
E('-- the hop: writes the receipt, fires the row\'s trigger column, closes a BUILD pair, ends the run, births a missing gate, lands on the next gate')
E(f"""CREATE TRIGGER hop_go INSTEAD OF INSERT ON hop BEGIN
  SELECT mother('INSERT INTO receipt (run, gate, shard) SELECT ' || NEW.run || ', ' || NEW.gate || ', shard FROM g' || NEW.gate || ' WHERE arrival IS ' || {nul('NEW.arrival')} || ' AND remainder IS ' || {nul('NEW.remainder')});
  SELECT mother('INSERT INTO fire (run, target, gate, arrival, remainder, rest) SELECT ' || NEW.run || ', trigger, ' || NEW.gate || ', ' || {nul('NEW.arrival')} || ', ' || {nul('NEW.remainder')} || ', ' || coalesce(quote(NEW.rest), 'NULL') || ' FROM g' || NEW.gate || ' WHERE arrival IS ' || {nul('NEW.arrival')} || ' AND remainder IS ' || {nul('NEW.remainder')} || ' AND trigger IS NOT NULL AND EXISTS (SELECT 1 FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = trigger) || ''.memory'')');
  SELECT mother('INSERT INTO build (run) VALUES (' || NEW.run || ')') WHERE NEW.gate = {K} AND (SELECT count(*) FROM receipt WHERE run = NEW.run AND gate = {K}) % 2 = 0;
  INSERT INTO "{END}" (run, arrival, remainder, rest) SELECT NEW.run, NEW.gate, NULL, NULL WHERE NEW.remainder IS NULL AND NEW.gate <> {END};
  SELECT mother('INSERT INTO born (run, gate) SELECT ' || NEW.run || ', ' || NEW.remainder || ' WHERE NOT EXISTS (SELECT 1 FROM sqlite_master WHERE type = ''view'' AND name = ''' || NEW.remainder || ''')') WHERE NEW.remainder IS NOT NULL;
  SELECT mother('INSERT INTO "' || NEW.remainder || '" (run, arrival, remainder, rest) VALUES (' || NEW.run || ', ' || NEW.gate || ', ' || coalesce(nullif({head}, ''), 'NULL') || ', ' || coalesce(quote(nullif({tail}, '')), 'NULL') || ')', NEW.run) WHERE NEW.remainder IS NOT NULL;
  UPDATE input SET answer = (SELECT group_concat(text, char(10)) FROM output WHERE run = NEW.run) WHERE id = NEW.run AND EXISTS (SELECT 1 FROM output WHERE run = NEW.run);
END;""")
E('')
E('-- build: the second BUILD of a pair landed. The words between the two BUILDs are read back (var cells filled) and handed to mother; her answer is the run\'s output')
E(f"""CREATE TRIGGER build_go INSTEAD OF INSERT ON build BEGIN
  SELECT mother('INSERT INTO output (run, text) VALUES (' || NEW.run || ', ' || quote(mother(t)) || ')') FROM (SELECT (SELECT group_concat(w, '') FROM (
      SELECT CASE WHEN p2 = 'var' AND p1 = ' ' THEN coalesce((SELECT value FROM sheet s WHERE s.name = word AND s.run = NEW.run ORDER BY s.id DESC LIMIT 1), (SELECT value FROM sheet s WHERE s.name = word ORDER BY s.id DESC LIMIT 1), 'var ' || word)
                  WHEN word = 'var' AND n1 = ' ' THEN '' WHEN p1 = 'var' AND word = ' ' THEN '' ELSE word END AS w
      FROM (SELECT e.word, lag(e.word, 1) OVER (ORDER BY r.id) AS p1, lag(e.word, 2) OVER (ORDER BY r.id) AS p2, lead(e.word, 1) OVER (ORDER BY r.id) AS n1, r.id
            FROM receipt r JOIN encoder e ON e.gate = r.gate
            WHERE r.run = NEW.run AND r.gate <> {K}
              AND r.id > (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {K} AND id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {K}))
              AND r.id < (SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {K})) ORDER BY id)) AS t);
END;""")
E('')
E('-- born: a gate with no neuron. It writes the cells the born run reads, then fires born\'s own memory run if one exists')
E(f"""CREATE TRIGGER born_go INSTEAD OF INSERT ON born BEGIN
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.definition' FROM encoder WHERE gate = NEW.gate;
  INSERT OR IGNORE INTO encoder (word) SELECT word || '.memory' FROM encoder WHERE gate = NEW.gate;
  INSERT INTO sheet (run, name, value) VALUES
    (NEW.run, 'gate', NEW.gate), (NEW.run, 'dna', 'g' || NEW.gate), (NEW.run, 'trig', 't' || NEW.gate),
    (NEW.run, 'defgate', (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.definition')),
    (NEW.run, 'def', 'g' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.definition')),
    (NEW.run, 'mem', 'g' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.gate) || '.memory'));
  SELECT mother('INSERT INTO fire (run, target, gate) SELECT ' || NEW.run || ', {BORN_G}, ' || NEW.gate || ' WHERE EXISTS (SELECT 1 FROM g{BM})');
END;""")
E('')
E('-- fire: a DNA row\'s trigger column named a neuron. The cells at/before/after say which row fired; the newest run in that neuron\'s memory node is typed again as a sub-run of this run')
E(f"""CREATE TRIGGER fire_go INSTEAD OF INSERT ON fire BEGIN
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'at', word FROM encoder WHERE gate = NEW.gate;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'before', word FROM encoder WHERE gate = NEW.arrival;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'after', word FROM encoder WHERE gate = NEW.remainder;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'next', word FROM encoder WHERE gate = CASE WHEN NEW.remainder IS NOT {SP} THEN NEW.remainder ELSE CAST(substr(NEW.rest || ' ', 1, instr(NEW.rest || ' ', ' ') - 1) AS INTEGER) END;
  INSERT INTO sheet (run, name, value) SELECT NEW.run, 'prev', e.word FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = NEW.run AND r.gate NOT IN ({SP}, NEW.gate, {H}) ORDER BY r.id DESC LIMIT 1;
  SELECT mother('INSERT INTO input (text, parent) SELECT (SELECT group_concat(w, '''') FROM (SELECT e.word AS w FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.shard IS NOT NULL AND r.gate NOT IN ({H}, {S_}, {END}) AND r.run = (SELECT run FROM g'
    || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.target) || '.memory')
    || ' ORDER BY id DESC LIMIT 1) ORDER BY r.id)), ' || NEW.run || ' WHERE EXISTS (SELECT 1 FROM g' || (SELECT gate FROM encoder WHERE word = (SELECT word FROM encoder WHERE gate = NEW.target) || '.memory') || ')', NEW.run);
END;""")
E('')
E('-- the ear: a typed line is encoded to gates (a word is a run of letters and _; every digit and every other character, space included, is its own neuron); new words get a gate; the run starts by hopping from heard to the first word')
E(f"""CREATE TRIGGER ear AFTER INSERT ON input BEGIN
  INSERT OR IGNORE INTO encoder (word)
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c))
    SELECT group_concat(ch, '') FROM t GROUP BY tok;
  UPDATE input SET gates = (
    WITH RECURSIVE c(i, ch) AS (SELECT 1, substr(NEW.text, 1, 1) UNION ALL SELECT i + 1, substr(NEW.text, i + 1, 1) FROM c WHERE i < length(NEW.text)),
    t AS (SELECT i, ch, sum(start) OVER (ORDER BY i) AS tok FROM (SELECT i, ch, CASE WHEN ch GLOB '[A-Za-z_]' AND coalesce(lag(ch) OVER (ORDER BY i), ' ') GLOB '[A-Za-z_]' THEN 0 ELSE 1 END AS start FROM c)),
    w AS (SELECT tok, group_concat(ch, '') AS word FROM t GROUP BY tok)
    SELECT group_concat(gate, ' ') FROM (SELECT e.gate FROM w JOIN encoder e ON e.word = w.word ORDER BY w.tok)) WHERE id = NEW.id;
  INSERT INTO sheet (run, name, value) VALUES (NEW.id, 'run', NEW.id);
  INSERT INTO receipt (run, gate, shard) VALUES (NEW.id, {H}, NULL);
  INSERT INTO hop (run, gate, arrival, remainder, rest)
    SELECT NEW.id, {H}, NULL, CAST(substr(gates || ' ', 1, instr(gates || ' ', ' ') - 1) AS INTEGER), nullif(trim(substr(gates || ' ', instr(gates || ' ', ' ') + 1)), '') FROM input WHERE id = NEW.id;
END;""")
open(sys.argv[1] if len(sys.argv) > 1 else 'egg.sql', 'w').write('\n'.join(out) + '\n')
open('BORN-RUN.txt', 'w').write(BORN + '\n')
print('egg:', len(out), 'lines;', n, 'gates;', len(word_neurons), 'word neurons;', len(tokens(BORN)), 'tokens in the born run; heard', H, 'hop', HOP, 'born', BORN_G, 'fire', FIRE, 'end', END, 'build', BLD, 'BUILD', K, 'var', V, 'born.memory', BM)
