# The bottom for v18: writes a typed line into input and reads output; mother runs the text the neurons hand her at the
# SQL prompt and gives back what SQL said (rows, ok, or the error). A source brain is its own database with a corpus,
# an inbox, an outbox and its own trigger; when an ask lands she picks up what its outbox holds and writes each row into
# secondary input. She decides nothing about any of it.
import sqlite3, json, re

class Brain:
    def __init__(self, told_path, sat=None, dbfile=None):
        told = json.load(open(told_path))
        self.SATS = told['sats']
        self.con = sqlite3.connect(':memory:', isolation_level=None, cached_statements=1024)
        self.populated = []
        self.con.create_function('mother', 2, self.mother)
        self.con.create_function('motherp', -1, self.motherp)
        self.con.create_function('satwork', 4, lambda sat, ask, word, n: self.populated.append((sat, ask, word, n)) or 1)
        for s in self.SATS:
            self.con.execute(f"ATTACH ':memory:' AS {s}")
            self.con.executescript(f"""CREATE TABLE {s}.corpus (word TEXT COLLATE NOCASE, hw TEXT, text TEXT, words TEXT); CREATE INDEX {s}.cw ON corpus(word);
                CREATE TABLE {s}.inbox (ask INTEGER PRIMARY KEY, word TEXT); CREATE TABLE {s}.outbox (ask INTEGER, word TEXT, hw TEXT, text TEXT, words TEXT);
                CREATE TRIGGER {s}.work AFTER INSERT ON inbox BEGIN INSERT INTO outbox SELECT NEW.ask, NEW.word, hw, text, words FROM corpus WHERE word = NEW.word;
                  SELECT satwork('{s}', NEW.ask, NEW.word, (SELECT count(*) FROM outbox WHERE ask = NEW.ask)); DELETE FROM inbox WHERE ask = NEW.ask; END;""")
            rows = (sat or {}).get(s, [])
            self.con.executemany(f"INSERT INTO {s}.corpus VALUES (?, ?, ?, ?)", [(r[0], r[1], r[2], r[3] if len(r) > 3 else None) for r in rows])
        if dbfile:
            src = sqlite3.connect(dbfile); src.backup(self.con, name='main'); src.close()
            self.con.execute('PRAGMA recursive_triggers = ON')
        else:
            for st in told['statements']:
                self.con.execute(st)

    @staticmethod
    def split(text):
        out, buf = [], ''
        for piece in text.split(';'):
            buf += piece + ';'
            if sqlite3.complete_statement(buf):
                if buf.strip(' ;\n'): out.append(buf.strip())
                buf = ''
        if buf.strip(' ;\n'): out.append(buf.rstrip(';').strip())
        return out

    # what the neurons put out at BUILD: run it at the SQL prompt, statement by statement, as the sqlite prompt would
    def mother(self, text, run):
        if not text: return 'error: nothing to run'
        reply = 'ok'
        for st in self.split(text):
            self.populated = []
            try:
                cur = self.con.execute(st)
                rows = cur.fetchall() if cur.description else None
            except Exception as e:
                return 'error: ' + str(e)
            picked, self.populated = self.populated, []
            for (s, ask, word, n) in picked:
                out = self.con.execute(f"SELECT text FROM {s}.outbox WHERE ask = ?", (ask,)).fetchall()
                self.con.execute(f"DELETE FROM {s}.outbox WHERE ask = ?", (ask,))
                for (tx,) in out:
                    self.con.execute("INSERT INTO secondary (run, src, value) VALUES (?, ?, ?)", (run, s, tx))
            if rows is not None:
                reply = '\n'.join(' '.join('' if v is None else str(v) for v in r) for r in rows)
        return reply

    # a step of the hop itself (write a shard, lay its hop trigger, land again): SQL's own answer comes straight back
    def motherp(self, text, *values):
        cur = self.con.execute(text, values)
        if cur.description:
            rows = cur.fetchall()
            return rows[0][0] if rows and rows[0] else None
        return cur.lastrowid

    def type(self, line, direction='heard'):
        before = self.con.execute("SELECT coalesce(max(id), 0) FROM output").fetchone()[0]
        self.con.execute("INSERT INTO input (line, direction) VALUES (?, ?)", (line, direction))
        r = self.con.execute("SELECT text FROM output WHERE id > ? ORDER BY id DESC LIMIT 1", (before,)).fetchone()
        return r[0] if r else None
    def q(self, sql, params=()):
        return self.con.execute(sql, params).fetchall()
    def save(self, dbfile):
        dst = sqlite3.connect(dbfile); self.con.backup(dst, name='main'); dst.close()
