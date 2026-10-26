# v18 (2026-10-25): the hand-laid core, from the owner's words only (EXPECT-v18.md).
# Hand-laid: the encoder (label), the neurons that make the table (every token of the neuron-building run, each with its DNA
# table, its gate and the gate's one trigger), the hop neuron, the trigger column, BUILD front and end.
# Everything else is laid by runs typed at the prompt.
import json, sys

W = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

def tokens(s):
    """a run of letters, digits or _ is one token; every other character (space, punctuation) is a token of its own"""
    out, i = [], 0
    while i < len(s):
        if s[i] in W:
            j = i
            while j < len(s) and s[j] in W: j += 1
            out.append(s[i:j]); i = j
        else:
            out.append(s[i]); i += 1
    return out

def lit(s):
    return "'" + s.replace("'", "''") + "'"

def HEAD(x):
    return (f"(CASE WHEN length({x}) > length(ltrim({x}, '{W}')) THEN substr({x}, 1, length({x}) - length(ltrim({x}, '{W}'))) "
            f"ELSE substr({x}, 1, 1) END)")
def TAIL(x):
    return f"substr({x}, length({HEAD(x)}) + 1)"
def G(w):
    return f"(SELECT gate FROM label WHERE word = {w})"

# a neuron's gate: a run lands on it; if the shard keyed by how the run arrived and its remainder exists the run hits it,
# if not the shard is written with the next shard number ("if chard exists hits the chard, if not writes it"); the shard goes
# to the hop neuron with its trigger column ("a column in the dna chard table just pointed to that trigger neuron"); then the
# run lands on its remainder gate. Each step is its own statement handed to mother, so no table is held open while the run
# goes on. Holes: {DNA} the DNA table, {ENTRY} the gate, {GATET} this trigger, {GATE} the gate number.
GATE_TEMPLATE = ("CREATE TRIGGER {GATET} INSTEAD OF INSERT ON {ENTRY} BEGIN "
    "SELECT motherp('INSERT INTO {DNA} (shard, arrival, remainder) SELECT n + 1, ?, ? FROM shards WHERE NOT EXISTS (SELECT 1 FROM {DNA} WHERE arrival IS ? AND remainder IS ?)', NEW.arrival, NEW.remainder, NEW.arrival, NEW.remainder); "
    "SELECT motherp('UPDATE shards SET n = n + 1 WHERE EXISTS (SELECT 1 FROM {DNA} WHERE shard = n + 1)'); "
    "SELECT motherp('INSERT INTO hop (run, gate, shard, remainder, rest, trig) SELECT ?, {GATE}, shard, ?, ?, trigger FROM {DNA} WHERE arrival IS ? AND remainder IS ?', NEW.run, NEW.remainder, NEW.rest, NEW.arrival, NEW.remainder); "
    "SELECT motherp('INSERT INTO land_' || NEW.remainder || ' (arrival, remainder, run, rest) VALUES (?, ?, ?, ?)', {GATE}, (SELECT gate FROM label WHERE word = " + HEAD('NEW.rest') + "), NEW.run, " + TAIL('NEW.rest') + ") WHERE NEW.remainder IS NOT NULL; END")
def gate_trigger(k):
    return GATE_TEMPLATE.format(DNA=f'g{k}', ENTRY=f'land_{k}', GATET=f'gate_{k}', GATE=str(k))
def gate_trigger_holes():
    return GATE_TEMPLATE.format(DNA='var dna', ENTRY='var entry', GATET='var gatet', GATE='var gate')

def build(sheet_born_line):
    out = ["PRAGMA recursive_triggers = ON"]
    T = out.append
    T("CREATE TABLE shards (n INTEGER)"); T("INSERT INTO shards VALUES (0)")
    T("CREATE TABLE label (gate INTEGER PRIMARY KEY, word TEXT UNIQUE)")
    T("CREATE TABLE input (id INTEGER PRIMARY KEY, line TEXT, direction TEXT DEFAULT 'heard', parent INTEGER, kind TEXT DEFAULT 'line', word TEXT, subject INTEGER, rest TEXT)")
    T("CREATE TABLE run (id INTEGER PRIMARY KEY, input INTEGER, line TEXT, direction TEXT, parent INTEGER, root INTEGER, kind TEXT, word TEXT, subject INTEGER)")
    T("CREATE INDEX run_root ON run (root)"); T("CREATE INDEX run_parent ON run (parent)")
    T("CREATE TABLE receipt (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER)")
    T("CREATE INDEX receipt_run ON receipt (run, gate)")
    # the run data sheet: a run's cells
    T("CREATE TABLE sheet (id INTEGER PRIMARY KEY, run INTEGER, name TEXT, value TEXT)")
    T("CREATE INDEX sheet_run ON sheet (run, name)")
    T("CREATE TABLE hop (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER, remainder INTEGER, rest TEXT, trig INTEGER)")
    T("CREATE TABLE born (id INTEGER PRIMARY KEY, word TEXT, run INTEGER, source INTEGER DEFAULT 0)")
    T("CREATE TABLE fire (id INTEGER PRIMARY KEY, run INTEGER, gate INTEGER, shard INTEGER, trig INTEGER, rest TEXT, subject INTEGER)")
    T("CREATE TABLE formula (id INTEGER PRIMARY KEY, gate INTEGER, run INTEGER, ended INTEGER DEFAULT 0)")
    T("CREATE TABLE build (id INTEGER PRIMARY KEY, run INTEGER, rid INTEGER)")
    T("CREATE TABLE secondary (id INTEGER PRIMARY KEY, run INTEGER, src TEXT, value TEXT)")
    T('CREATE TABLE "end" (id INTEGER PRIMARY KEY, run INTEGER)')
    T("CREATE TABLE output (id INTEGER PRIMARY KEY, run INTEGER, text TEXT)")
    T("CREATE TABLE bindq (id INTEGER PRIMARY KEY, line TEXT, g INTEGER, a INTEGER, r INTEGER, t INTEGER)")

    # ---- the hand-laid neurons: the arrivals, origin, and every token of the neuron-building run and its teaching line.
    # Each: its gate (label), its DNA table, its gate (entry) and the gate's trigger, its definition node, and its first shard pointing at that node.
    words = ['heard', 'said', 'start', 'origin']
    for t in tokens(sheet_born_line):
        if t not in words: words.append(t)
    gate = {}
    k = 0; shard = 0
    for w in words:
        k += 1; gate[w] = k; dk = k + 1
        T(f"INSERT INTO label (gate, word) VALUES ({k}, {lit(w)})")
        T(f"INSERT INTO label (gate, word) VALUES ({dk}, {lit(w + '.definition')})")
        T(f"CREATE TABLE g{k} (shard INTEGER PRIMARY KEY, arrival INTEGER, remainder INTEGER, trigger INTEGER)")
        T(f"CREATE VIEW land_{k} AS SELECT arrival, remainder, NULL AS run, NULL AS rest FROM g{k}")
        T(gate_trigger(k))
        T(f"CREATE TABLE g{dk} (id INTEGER PRIMARY KEY, source INTEGER, run INTEGER, score REAL)")
        shard += 1
        T(f"INSERT INTO g{k} (shard, trigger) VALUES ({shard}, {dk})")
        k = dk
    T(f"UPDATE shards SET n = {shard}")
    BUILDG = gate['BUILD']

    # ---- input: a teaching line (word = run), a binding line (phrase -> word), or a run
    h = HEAD('NEW.line')
    TEACH = (f"NEW.kind = 'line' AND length({h}) > 0 AND length(ltrim({h}, '{W}')) = 0 AND substr(NEW.line, length({h}) + 1, 3) = ' = '")
    BIND = "NEW.kind = 'line' AND instr(NEW.line, ' -> ') > 0"
    T(f"""CREATE TRIGGER input_teach AFTER INSERT ON input WHEN {TEACH} BEGIN
      INSERT INTO born (word, run, source) SELECT {h}, NULL, 0 WHERE NOT EXISTS (SELECT 1 FROM label WHERE word = {h});
      INSERT INTO run (input, line, direction, kind, word) VALUES (NEW.id, substr(NEW.line, length({h}) + 4), 'start', 'teach', {h});
    END""")
    T(f"""CREATE TRIGGER input_bind AFTER INSERT ON input WHEN {BIND} BEGIN
      INSERT INTO bindq (line) VALUES (NEW.line);
    END""")
    T(f"""CREATE TRIGGER input_run AFTER INSERT ON input WHEN NOT ({TEACH}) AND NOT ({BIND}) BEGIN
      INSERT INTO run (input, line, direction, parent, kind, word, subject) VALUES (NEW.id, NEW.line, NEW.direction, NEW.parent, NEW.kind, NEW.word, NEW.subject);
    END""")

    # ---- a run: its root; a formula run's first cells; then it lands on its first gate (a token with no gate is born first)
    L = "coalesce(NEW.line, '')"
    T(f"""CREATE TRIGGER run_go AFTER INSERT ON run BEGIN
      UPDATE run SET root = CASE WHEN NEW.parent IS NULL THEN NEW.id ELSE coalesce((SELECT root FROM run WHERE id = NEW.parent), NEW.parent) END WHERE id = NEW.id;
      INSERT INTO sheet (run, name, value) SELECT NEW.id, 'run', NEW.id WHERE NEW.kind = 'formula';
      INSERT INTO sheet (run, name, value) SELECT NEW.id, 'after', (SELECT rest FROM input WHERE id = NEW.input) WHERE NEW.kind = 'formula';
      INSERT INTO sheet (run, name, value) SELECT NEW.id, 'subject', NEW.subject WHERE NEW.kind = 'formula';
      INSERT INTO born (word, run, source) SELECT {HEAD(L)}, NEW.id, NEW.kind = 'line' WHERE {L} <> '' AND NOT EXISTS (SELECT 1 FROM label WHERE word = {HEAD(L)});
      INSERT INTO born (word, run, source) SELECT {HEAD(TAIL(L))}, NEW.id, NEW.kind = 'line' WHERE {TAIL(L)} <> '' AND NOT EXISTS (SELECT 1 FROM label WHERE word = {HEAD(TAIL(L))});
      SELECT motherp('INSERT INTO land_' || {G(HEAD(L))} || ' (arrival, remainder, run, rest) VALUES (?, ?, ?, ?)', {G('NEW.direction')}, {G(HEAD(TAIL(L)))}, NEW.id, {TAIL(TAIL(L))}) WHERE {L} <> '';
    END""")

    # ---- born: the neuron-building run fires (the neuron 'born' holds it once taught); a word a typed line brought, or one asked
    # for by a run, is then looked up: the source run fires
    T(f"""CREATE TRIGGER born_go AFTER INSERT ON born BEGIN
      INSERT INTO fire (run, trig, subject) VALUES (NEW.run, {gate['born']}, NEW.id);
      INSERT INTO fire (run, trig, subject) SELECT NEW.run, {G("'source'")}, {G('NEW.word')} WHERE NEW.source = 1 AND EXISTS (SELECT 1 FROM label WHERE word = NEW.word);
    END""")

    # ---- the trigger column: the neuron it points at runs its formula as a branch of this run (its tokens are the run that taught it)
    T("""CREATE TRIGGER fire_go AFTER INSERT ON fire BEGIN
      INSERT INTO input (line, direction, parent, kind, word, subject, rest)
        SELECT (SELECT group_concat(w, '') FROM (SELECT l.word AS w FROM receipt x JOIN label l ON l.gate = x.gate WHERE x.run = f.run ORDER BY x.id)),
               'start', NEW.run, 'formula', (SELECT word FROM label WHERE gate = NEW.trig), NEW.subject, NEW.rest
        FROM formula f WHERE f.gate = NEW.trig AND f.ended = 0;
    END""")

    # ---- the hop neuron: the receipt; BUILD front and end; the shard's trigger column fires; the last node ends the run; the head of
    # the remainder is born if it has no gate (then the gate lands the run on its remainder gate through mother, the owner's typed hop, 10-19)
    T(f"""CREATE TRIGGER hop_go AFTER INSERT ON hop BEGIN
      INSERT INTO receipt (run, gate, shard) VALUES (NEW.run, NEW.gate, NEW.shard);
      INSERT INTO build (run, rid) SELECT NEW.run, (SELECT max(id) FROM receipt WHERE run = NEW.run) WHERE NEW.gate = {BUILDG} AND (SELECT kind FROM run WHERE id = NEW.run) <> 'teach'
        AND (SELECT count(*) FROM receipt WHERE run = NEW.run AND gate = {BUILDG}) % 2 = 0;
      INSERT INTO fire (run, gate, shard, trig, rest) SELECT NEW.run, NEW.gate, NEW.shard, NEW.trig, coalesce((SELECT word FROM label WHERE gate = NEW.remainder), '') || coalesce(NEW.rest, '') WHERE NEW.trig IS NOT NULL;
      INSERT INTO "end" (run) SELECT NEW.run WHERE NEW.remainder IS NULL;
      INSERT INTO born (word, run, source) SELECT {HEAD('NEW.rest')}, NEW.run, (SELECT kind FROM run WHERE id = NEW.run) = 'line'
        WHERE NEW.remainder IS NOT NULL AND NEW.rest <> '' AND NOT EXISTS (SELECT 1 FROM label WHERE word = {HEAD('NEW.rest')});
      DELETE FROM hop WHERE id = NEW.id;
    END""")

    # ---- binding a DNA row's trigger column: "<the start of a line> -> <word>": the row the line's first token hits (arriving from heard,
    # its remainder the token after) points at the word's neuron; the row is written if it is not there
    P = "trim(substr(NEW.line, 1, instr(NEW.line, ' -> ') - 1))"
    F = "trim(substr(NEW.line, instr(NEW.line, ' -> ') + 4))"
    T(f"""CREATE TRIGGER bind_go AFTER INSERT ON bindq BEGIN
      UPDATE bindq SET g = {G(HEAD(P))}, a = {G("'heard'")}, r = CASE WHEN {TAIL(P)} = '' THEN NULL ELSE {G(HEAD(TAIL(P)))} END, t = {G(F)} WHERE id = NEW.id;
      SELECT motherp('INSERT INTO g' || g || ' (shard, arrival, remainder) SELECT n + 1, ?, ? FROM shards WHERE NOT EXISTS (SELECT 1 FROM g' || g || ' WHERE arrival IS ? AND remainder IS ?)', a, r, a, r) FROM bindq WHERE id = NEW.id AND g IS NOT NULL AND t IS NOT NULL;
      SELECT motherp('UPDATE shards SET n = n + 1 WHERE EXISTS (SELECT 1 FROM g' || g || ' WHERE shard = n + 1)') FROM bindq WHERE id = NEW.id AND g IS NOT NULL AND t IS NOT NULL;
      SELECT motherp('UPDATE g' || g || ' SET trigger = ? WHERE arrival IS ? AND remainder IS ?', t, a, r) FROM bindq WHERE id = NEW.id AND g IS NOT NULL AND t IS NOT NULL;
    END""")

    # ---- BUILD front and end: the receipt between the two BUILD gates, holes ("var name") filled from the run's data sheet
    # (this run's newest cell of that name, else its parent's, else its root's), goes to mother; her reply is the run's cell BUILD
    def HOLE(run, name):
        return (f"coalesce((SELECT value FROM sheet WHERE run = {run} AND name = {name} ORDER BY id DESC LIMIT 1), "
                f"(SELECT value FROM sheet WHERE run = (SELECT parent FROM run WHERE id = {run}) AND name = {name} ORDER BY id DESC LIMIT 1), "
                f"(SELECT value FROM sheet WHERE run = (SELECT root FROM run WHERE id = {run}) AND name = {name} ORDER BY id DESC LIMIT 1))")
    A = f"coalesce((SELECT max(id) FROM receipt WHERE run = NEW.run AND gate = {BUILDG} AND id < NEW.rid), 0)"
    decode = (f"(SELECT trim(group_concat(p, '')) FROM (SELECT id, CASE WHEN w = 'var' AND n1 = ' ' THEN '' WHEN w = ' ' AND w1 = 'var' THEN '' "
              f"WHEN w1 = ' ' AND w2 = 'var' THEN coalesce({HOLE('NEW.run', 'w')}, '') ELSE w END AS p "
              f"FROM (SELECT x.id AS id, l.word AS w, lag(l.word, 1) OVER o AS w1, lag(l.word, 2) OVER o AS w2, lead(l.word, 1) OVER o AS n1 "
              f"FROM receipt x JOIN label l ON l.gate = x.gate WHERE x.run = NEW.run AND x.id > {A} AND x.id < NEW.rid WINDOW o AS (ORDER BY x.id)) ORDER BY id))")
    T(f"""CREATE TRIGGER build_go AFTER INSERT ON build BEGIN
      INSERT INTO sheet (run, name, value) VALUES (NEW.run, 'BUILD', mother({decode}, NEW.run));
    END""")

    # ---- a source's reply comes back as a run through the neurons, headed by where it came from
    T("""CREATE TRIGGER secondary_go AFTER INSERT ON secondary BEGIN
      INSERT INTO input (line, direction, parent, kind, word, subject)
        VALUES ('return from ' || coalesce((SELECT line FROM run WHERE id = (SELECT root FROM run WHERE id = NEW.run)), '') || ' from source ' || NEW.src || ' /build ' || coalesce(NEW.value, ''),
                'heard', NEW.run, 'defrow', NEW.src, (SELECT subject FROM run WHERE id = NEW.run));
    END""")

    # ---- the last node of a run
    T("""CREATE TRIGGER end_teach AFTER INSERT ON "end" WHEN (SELECT kind FROM run WHERE id = NEW.run) = 'teach' BEGIN
      UPDATE formula SET ended = 1 WHERE gate = (SELECT gate FROM label WHERE word = (SELECT word FROM run WHERE id = NEW.run)) AND ended = 0;
      INSERT INTO formula (gate, run) VALUES ((SELECT gate FROM label WHERE word = (SELECT word FROM run WHERE id = NEW.run)), NEW.run);
    END""")
    T("""CREATE TRIGGER end_return AFTER INSERT ON "end" WHEN (SELECT kind FROM run WHERE id = NEW.run) = 'defrow' BEGIN
      INSERT INTO sheet (run, name, value) SELECT parent, word, NEW.run FROM run WHERE id = NEW.run;
    END""")
    T("""CREATE TRIGGER end_line AFTER INSERT ON "end" WHEN (SELECT kind FROM run WHERE id = NEW.run) = 'line' BEGIN
      INSERT INTO output (run, text) VALUES (NEW.run, coalesce(
        (SELECT value FROM sheet WHERE name = 'say' AND run IN (SELECT id FROM run WHERE root = NEW.run) ORDER BY id DESC LIMIT 1),
        (SELECT value FROM sheet WHERE run = NEW.run AND name = 'BUILD' ORDER BY id DESC LIMIT 1)));
    END""")
    return out, words, gate

if __name__ == '__main__':
    sheet = json.load(open(sys.argv[2]))
    born_line = [l for k, l in sheet if k == 'teach born'][0]
    stmts, words, gate = build(born_line)
    json.dump({'statements': stmts, 'sats': ['wn', 'gcide', 'mw', 'mwt', 'moby', 'map', 'sqldoc', 'measured'], 'handlaid': words}, open(sys.argv[1], 'w'))
    print(len(stmts), 'statements;', len(words), 'hand-laid neurons:', ' '.join(repr(w) for w in words))
