# The host for physics15: the bottom (writes a typed line into input, reads output) and mother (routes text and replies). Nothing else.
import sqlite3, json, re

class Brain:
    def __init__(self, told_path, sat_path=None, sat=None):
        told = json.load(open(told_path))
        self.SATS = told['sats']
        self.con = sqlite3.connect(':memory:', isolation_level=None, cached_statements=4096)
        self.populated = []
        self.con.create_function('mother', 3, self.mother)
        self.con.create_function('satwork', 4, lambda sat, ask, word, n: self.populated.append((sat, ask, word, n)) or 1)
        # SATELLITE: stand-ins for the source brains. Each is its own database: a corpus, an inbox, an outbox, and its own trigger
        # that does its work the moment an ask lands and says when its outbox is populated.
        satdata = sat if sat is not None else (json.load(open(sat_path)) if sat_path else {})
        for s in self.SATS:
            self.con.execute(f"ATTACH ':memory:' AS {s}")
            self.con.executescript(f"""CREATE TABLE {s}.corpus (word TEXT COLLATE NOCASE, hw TEXT, text TEXT, words TEXT); CREATE INDEX {s}.cw ON corpus(word);
                CREATE TABLE {s}.inbox (ask INTEGER PRIMARY KEY, word TEXT); CREATE TABLE {s}.outbox (ask INTEGER, word TEXT, hw TEXT, text TEXT, words TEXT);
                CREATE TRIGGER {s}.work AFTER INSERT ON inbox BEGIN INSERT INTO outbox SELECT NEW.ask, NEW.word, hw, text, words FROM corpus WHERE word = NEW.word;
                  SELECT satwork('{s}', NEW.ask, NEW.word, (SELECT count(*) FROM outbox WHERE ask = NEW.ask)); DELETE FROM inbox WHERE ask = NEW.ask; END;""")
            rows = satdata.get(s, [])
            self.con.executemany(f"INSERT INTO {s}.corpus VALUES (?, ?, ?, ?)", [(r[0], r[1], r[2], r[3] if len(r) > 3 else None) for r in rows])
        # the told block: laid once, as one block
        for st in told['statements']:
            self.con.execute(st)

    # MOTHER: she runs the text she is handed at the SQL prompt. If it is addressed to a source brain's inbox she carries it there,
    # and when that brain says its outbox is populated she picks it up and empties it. What came back she writes into secondary input.
    # She decides nothing and computes nothing about the reply.
    def mother(self, text, run, stmt):
        con = self.con
        addressed = [a.split('.')[0] for a in re.findall(r'\b(\w+)\.inbox\b', text) if a.split('.')[0] in self.SATS]
        if run is not None:
            con.execute("INSERT INTO event (kind, gate, run, rowgate, text, roots) VALUES ('mother', 'mother', ?, 'mother', ?, 'CALL MOVE')",
                        (run, 'mother carries it ' + ('into the inbox of ' + ', '.join(addressed) if addressed else 'to the SQL prompt')))
        self.populated = []
        cols, rows, err, changes = [], [], None, 0
        try:
            cur = con.execute(text)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchall()
            changes = cur.rowcount if cur.rowcount and cur.rowcount > 0 else 0
            lastid = None if cur.description else cur.lastrowid
        except Exception as e:
            err, lastid = str(e), None
        picked = self.populated; self.populated = []
        if run is None:
            # a by-value step of the physics itself (a birth, a lay, a landing): the SQL prompt's own answer goes straight back
            if err: raise sqlite3.OperationalError(err)
            return rows[0][0] if rows and rows[0] else lastid
        if not addressed:
            con.execute("INSERT INTO event (kind, gate, run, rowgate, text, roots) VALUES ('sql', 'SQL prompt', ?, 'SQL prompt', ?, '')", (run, 'the SQL prompt ' + ('refuses it: ' + err if err else 'runs it')))
            con.execute("INSERT INTO event (kind, gate, run, rowgate, text, roots) VALUES ('mother', 'mother', ?, 'mother', 'mother carries the reply back', 'CALL MOVE')", (run,))
            val = ' | '.join(' '.join('' if v is None else str(v) for v in r) for r in rows) if rows else None
            con.execute("INSERT INTO secondary (run, stmt, src, value, cols, n, err, changes, last) VALUES (?, ?, 'sql', ?, ?, ?, ?, ?, 1)",
                        (run, stmt, val, ','.join(cols), len(rows), err, changes))
            return rows[0][0] if rows and rows[0] else None
        for sat in addressed:
            got = [p for p in picked if p[0] == sat]
            if err:
                # the SQL prompt refused the ask: it never reached the inbox. Mother says what came back, the refusal; she does not call it waiting
                con.execute("INSERT INTO secondary (run, stmt, src, err, n, last) VALUES (?, ?, ?, ?, 0, 1)", (run, stmt, sat, err))
                continue
            if not got:
                con.execute("INSERT INTO secondary (run, stmt, src, waiting, last) VALUES (?, ?, ?, 1, 1)", (run, stmt, sat))
                continue
            for (s, ask, word, n) in got:
                con.execute("INSERT INTO event (kind, gate, run, rowgate, text, roots) VALUES ('mailbox', ?, ?, ?, ?, 'FIND READ WRITE')", (s, run, s, s + ': the ask for "' + word + '" lands in its inbox; its own trigger does its work at once'))
                con.execute("INSERT INTO event (kind, gate, run, rowgate, text, roots) VALUES ('populated', ?, ?, NULL, ?, 'WRITE')", (s, run, s + ': its outbox is populated with ' + str(n) + ' row(s), and it says so'))
                out = con.execute(f"SELECT word, hw, text, words FROM {s}.outbox WHERE ask = ?", (ask,)).fetchall()
                con.execute(f"DELETE FROM {s}.outbox WHERE ask = ?", (ask,))
                con.execute("INSERT INTO event (kind, gate, run, rowgate, text, roots) VALUES ('pickup', 'mother', ?, 'mother', ?, 'MOVE CALL')", (run, 'mother picks up ' + str(len(out)) + ' row(s) from ' + s + ' and empties that outbox'))
                for (w, hw, tx, ws) in out:
                    con.execute("INSERT INTO secondary (run, stmt, src, word, hw, value, words, last) VALUES (?, ?, ?, ?, ?, ?, ?, 0)", (run, stmt, s, w, hw, tx, ws))
                con.execute("INSERT INTO secondary (run, stmt, src, word, n, last) VALUES (?, ?, ?, ?, ?, 1)", (run, stmt, s, word, len(out)))
        return None

    # THE BOTTOM: write a typed line into input; read what came out
    def type(self, line, direction='heard'):
        before = self.con.execute("SELECT coalesce(max(id), 0) FROM output").fetchone()[0]
        self.con.execute("INSERT INTO input (line, direction) VALUES (?, ?)", (line, direction))
        r = self.con.execute("SELECT text FROM output WHERE id > ? ORDER BY id DESC LIMIT 1", (before,)).fetchone()
        return r[0] if r else None
    def q(self, sql, params=()):
        return self.con.execute(sql, params).fetchall()
