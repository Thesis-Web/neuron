#!/usr/bin/env python3
# bottom7.py (2026-10-29, v7): the env handler and the prompts (the owner's outline 10-25 21:50, lines 1, 9 to 12). From bottom6.py; what v7
# changes is where the hop mailbox is read. In v5 and v6 mother herself, after the text she was handed, drained every brain's hop table
# inside the typed line's statement (the pump), so a whole line was one statement, one transaction and one door job, and nothing could
# touch the brain until it ended. The owner, 10-29 night: mother is a router; take the output, route, paste, hit enter; the sixth is its
# own brain. So: each brain has a router loop of its own on its own connection that takes the newest row of that brain's hop mailbox,
# pastes it as a statement of its own, and keeps the refusal in that brain's refused table; between two hops the brain is free, so the
# page reads and the owner types while a run is going. Both brain files are in WAL mode (one line typed once stays), which is what makes
# a reader never wait and a hop's own commit cost 24 us instead of 5 ms (measured 10-29). The order is newest first: every formula taught
# so far relies on a call or a birth finishing before the landing after it (hit_go writes the rows in that order; the stack is the brain's).
# The router decides nothing: it takes the row the brain wrote last, pastes it, and keeps SQLite's refusal. The sixth has no sources of
# its own (the owner: the same core trained to fix, find and observe; it calls the brain for source drops if it needs them).
# usage: python3 bottom7.py [--lines FILE] [--ledger FILE] [--quiet]      interactive when no --lines; Ctrl-D leaves.
import os, re, sqlite3, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
BRAIN = os.path.join(HERE, 'brain.db'); SIXTH = os.path.join(HERE, 'sixth.db')
SRC = os.path.join(ROOT, 'sources')
SOURCES = ['wn', 'gcide', 'mwt', 'moby', 'map', 'sqldoc', 'measured', 'guess', 'wikt']   # as the live brain's connection had them on 10-29 night (mw detached for the slot)
POINTERS = {22, 24, 25, 27}   # cells whose value points at a run: reply, def, say, remember (the fresh egg's gate numbers)
LISTS = {'known', 'unknown'}   # cells whose value is a list of gates

def connect(sources=True):
    db = sqlite3.connect(BRAIN, isolation_level=None, timeout=60, check_same_thread=False, cached_statements=4096)
    db.enable_load_extension(True); db.load_extension(os.path.join(HERE, 'mother'))
    db.execute('PRAGMA recursive_triggers = ON'); db.execute('PRAGMA busy_timeout = 60000')
    db.execute('PRAGMA journal_mode = WAL'); db.execute('PRAGMA synchronous = NORMAL')
    db.execute('ATTACH ? AS sixth', (SIXTH,)); db.execute('PRAGMA sixth.journal_mode = WAL')
    if sources:
        for s in SOURCES:
            db.execute(f'ATTACH ? AS {s}', (os.path.join(SRC, s + '.db'),))
            try: db.execute(f'PRAGMA {s}.journal_mode = WAL')
            except sqlite3.Error: pass
    return db

BATCH = 64   # hops pasted in one transaction before the commit that lets the typist and the page in; mine (a buffer, not a choice of order)
import queue
class Router(threading.Thread):
    """the one router: on one connection it takes the newest row of main's hop mailbox, then the sixth's, pastes each as a statement, keeps the
    refusal in that brain's refused table, commits every BATCH, and between batches runs what the door handed it (a typed line's insert, a
    read). One connection on purpose (v7.1, 2026-10-30 00:40): every birth is a schema change, and a second connection must reload the whole
    schema (16,000 tables) after each one, so under a cascade of births a second connection's statements failed and its writes starved; the
    first v7 lost the sixth's router that way. The sixth keeps its own file and its own mailbox; its hops are pasted in their turn."""
    def __init__(self, env):
        super().__init__(daemon=True, name='router')
        self.env = env; self.db = connect()
        self.wake = threading.Event(); self.idle = threading.Event(); self.idle.set()
        self.jobs = queue.Queue()
        self.hops = {'main': 0, 'sixth': 0}; self.refused = {'main': 0, 'sixth': 0}; self.commits = 0
    def batch(self, s):
        db = self.db
        take = f'DELETE FROM {s}.hop WHERE id = (SELECT max(id) FROM {s}.hop) RETURNING id, text, p1, p2, p3, p4, p5, p6'
        db.execute('BEGIN IMMEDIATE'); n = 0
        while n < BATCH:
            row = db.execute(take).fetchone()
            if row is None: break
            text = row[1] or ''; params = tuple(row[2:2 + text.count('?')])
            try:
                if params or ';' not in text: db.execute(text, params)
                else: db.execute('COMMIT'); db.executescript(text); db.execute('BEGIN IMMEDIATE')
            except sqlite3.Error as e:
                self.refused[s] += 1; db.execute(f'INSERT INTO {s}.refused (text, error) VALUES (?, ?)', (text, str(e)))
            n += 1
        db.execute('COMMIT'); self.commits += 1; self.hops[s] += n
        return n
    def run(self):
        while True:
            self.idle.clear()
            did = self.batch('main') + self.batch('sixth')
            while not self.jobs.empty():
                fn, out = self.jobs.get()
                try: out['result'] = fn(self.db)
                except Exception as e: out['error'] = e
                out['done'].set()
            self.env.changed.set()
            if did == 0 and self.jobs.empty():
                self.idle.set(); self.wake.wait(); self.wake.clear(); self.idle.clear()

class Env:
    def __init__(self):
        self.changed = threading.Event()
        threading.stack_size(1 << 30)
        self.router = Router(self)
        threading.stack_size(0)
        self.router.start()
        self.main = self.router; self.sixth = self.router      # v7.1: one router serves both mailboxes
    def wake_all(self): self.router.wake.set()
    def submit(self, fn, timeout=None):
        """hand the router a statement to run between batches, on its connection; wait for the answer"""
        out = {'done': threading.Event(), 'result': None, 'error': None}
        self.router.jobs.put((fn, out)); self.router.wake.set()
        out['done'].wait(timeout)
        if out['error']: raise out['error']
        return out['result']
    def q(self, sql, params=()):
        return self.submit(lambda db: db.execute(sql, params).fetchall())
    def pending(self): return self.q('SELECT (SELECT count(*) FROM main.hop) + (SELECT count(*) FROM sixth.hop)')[0][0]
    def until_ended(self, schema, rid, timeout=None):
        """wait until the typed line's own run has ended (its memory row is written); what the sixth fills later shows on the page's next read"""
        t0 = time.time()
        while True:
            self.changed.clear()
            ended, pend = self.submit(lambda db: (db.execute(f"SELECT 1 FROM {schema}.run_memory WHERE run = ?", (rid,)).fetchone() is not None,
                                                  db.execute('SELECT (SELECT count(*) FROM main.hop) + (SELECT count(*) FROM sixth.hop)').fetchone()[0]))
            if ended or pend == 0: return True
            self.changed.wait(0.2)
            if timeout and time.time() - t0 > timeout: return False
    def drain(self, timeout=None):
        t0 = time.time()
        while True:
            self.changed.clear()
            if self.pending() == 0 and self.router.jobs.empty(): return True
            self.changed.wait(0.2)
            if timeout and time.time() - t0 > timeout: return False

class Via:
    """a db-like handle for the typist and the door: every execute runs on the router's connection between batches; fetchone/fetchall as usual"""
    class Cur:
        def __init__(self, rows, lastrowid, description): self.rows, self.lastrowid, self.description = rows, lastrowid, description
        def fetchone(self): return self.rows[0] if self.rows else None
        def fetchall(self): return self.rows
    def __init__(self, env): self.env = env
    def execute(self, sql, params=()):
        def run(db):
            c = db.execute(sql, params); rows = c.fetchall() if c.description else []
            return rows, c.lastrowid, c.description
        rows, lastrowid, description = self.env.submit(run)
        return Via.Cur(rows, lastrowid, description)
def steady(db, sql, params=()): return db.execute(sql, params)

def decode(db, schema, run):
    r = steady(db, f"SELECT group_concat(symbol, '') FROM (SELECT l.symbol FROM {schema}.seq s JOIN {schema}.label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos)", (run,)).fetchone()
    return r[0] if r and r[0] is not None else ''

def show_out(db, schema, since, quiet):
    rows = steady(db, f"SELECT o.id, o.run, o.cell, o.value, (SELECT symbol FROM {schema}.label WHERE gate = o.cell) FROM {schema}.out_user o WHERE o.id > ? ORDER BY o.id", (since,)).fetchall()
    out = []
    for oid, run, cell, value, cname in rows:
        v = value
        if value is not None and str(value).isdigit() and int(value) > 0 and cell in POINTERS:
            arrival = db.execute(f"SELECT arrival FROM {schema}.run WHERE id = ?", (int(value),)).fetchone()
            who = db.execute(f"SELECT symbol FROM {schema}.label WHERE gate = ?", (arrival[0],)).fetchone() if arrival else None
            v = f"run {value} from {who[0] if who else '?'}: {decode(db, schema, int(value))[:160]}"
        elif cname in LISTS and value is not None and all(x.isdigit() for x in str(value).split()):
            v = ' '.join((db.execute(f"SELECT symbol FROM {schema}.label WHERE gate = ?", (int(x),)).fetchone() or ['?'])[0] for x in str(value).split()) or '(none)'
        out.append((schema, run, cname, v))
        if not quiet: print(f"  {schema} run {run} · {cname}: {v}")
    return (rows[-1][0] if rows else since), out

RUNS = []   # the run each typed line started, in order
def match_runs(db, lines):
    RUNS.clear(); seen = {}; typed = {}
    for schema in ('main', 'sixth'):
        rows = db.execute(f"SELECT run FROM {schema}.input WHERE run IS NOT NULL ORDER BY id").fetchall()
        typed[schema] = [(r[0], decode(db, schema, r[0])) for r in rows]
    for l in lines:
        if not l.strip() or l.startswith('#'): continue
        l = fill(db, l); schema, text = ('sixth', l[3:]) if l.startswith('6> ') else ('main', l)
        n = seen.get((schema, text), 0); seen[(schema, text)] = n + 1
        hits = [run for (run, t) in typed[schema] if t == text]
        RUNS.append(hits[n] if n < len(hits) else None)
    return RUNS
def fill(db, line):
    def r(m):
        k = int(m.group(1)); return str(RUNS[k - 1]) if 0 < k <= len(RUNS) and RUNS[k - 1] else m.group(0)
    line = re.sub(r'\{run:(\d+)\}', r, line)
    def g(m):
        schema = 'sixth' if m.group(1) == '6' else 'main'
        row = db.execute(f"SELECT gate FROM {schema}.label WHERE symbol = ?", (m.group(2),)).fetchone()
        return str(row[0]) if row else m.group(0)
    return re.sub(r'\{gate(6?):([^}]+)\}', g, line)

def type_line(env, line, quiet=False):
    db = env.db
    schema, text = 'main', line
    if line.startswith('6> '): schema, text = 'sixth', line[3:]
    t = time.time()
    before_s = db.execute("SELECT coalesce(max(id), 0) FROM sixth.out_user").fetchone()[0]
    before_m = db.execute("SELECT coalesce(max(id), 0) FROM main.out_user").fetchone()[0]
    runs0 = db.execute(f"SELECT coalesce(max(id), 0) FROM {schema}.run").fetchone()[0]
    gates0 = db.execute("SELECT count(*) FROM main.label").fetchone()[0]
    refused0 = db.execute("SELECT count(*) FROM main.refused").fetchone()[0] + db.execute("SELECT count(*) FROM sixth.refused").fetchone()[0]
    try:
        cur = steady(db, f"INSERT INTO {schema}.input (text) VALUES (?)", (text,))
    except sqlite3.Error as e:
        print('refused:', e); RUNS.append(None); return None
    rid = steady(db, f"SELECT run FROM {schema}.input WHERE id = ?", (cur.lastrowid,)).fetchone()[0] or (runs0 + 1)
    env.wake_all(); env.until_ended(schema, rid)
    RUNS.append(rid)
    runs1 = steady(db, f"SELECT count(*) FROM {schema}.run WHERE root = ? OR id = ?", (rid, rid)).fetchone()[0] + runs0
    hits = steady(db, f"SELECT count(*) FROM {schema}.run_receipt WHERE run IN (SELECT id FROM {schema}.run WHERE root = ? OR id = ?)", (rid, rid)).fetchone()[0]
    gates1 = steady(db, "SELECT count(*) FROM main.label").fetchone()[0]
    refused1 = steady(db, "SELECT count(*) FROM main.refused").fetchone()[0] + steady(db, "SELECT count(*) FROM sixth.refused").fetchone()[0]
    dt = time.time() - t
    if not quiet: print(f"  [{schema}: run {runs0 + 1}, {runs1 - runs0} runs, {hits} hits, {gates1 - gates0} born, {dt:.2f} s]")
    _, o1 = show_out(db, 'main', before_m, quiet); _, o2 = show_out(db, 'sixth', before_s, quiet)
    return {'schema': schema, 'run': rid, 'runs': runs1 - runs0, 'hits': hits, 'born': gates1 - gates0, 'refused': refused1 - refused0, 'seconds': dt, 'out': o1 + o2}

def open_brain():
    env = Env(); env.db = Via(env); return env

def main():
    quiet = '--quiet' in sys.argv
    lines = None; ledger = None
    if '--lines' in sys.argv: lines = [l.rstrip('\n') for l in open(sys.argv[sys.argv.index('--lines') + 1], encoding='utf-8')]
    if '--ledger' in sys.argv: ledger = open(sys.argv[sys.argv.index('--ledger') + 1], 'w', encoding='utf-8')
    env = open_brain(); db = env.db
    if lines is not None:
        k = 0
        if ledger: ledger.write("| # | prompt | line | run | runs | hits | born | refused | s | what the brain put in its out mailbox |\n|---|---|---|---|---|---|---|---|---|---|\n")
        for l in lines:
            if not l.strip() or l.startswith('#'):
                if ledger and l.startswith('# '): ledger.write(f"| | | *{l[2:].replace('|', '/')}* | | | | | | | |\n")
                continue
            k += 1
            l = fill(db, l)
            print('>', l[:140] + ('…' if len(l) > 140 else ''), flush=True)
            r = type_line(env, l, quiet)
            if ledger:
                if r is None: ledger.write(f"| {k} | | {l[:60].replace('|', '/')} | refused | | | | | | |\n"); continue
                outs = '<br>'.join(f"{s} run {run} · {c}: {str(v)[:90].replace('|', '/')}" for (s, run, c, v) in r['out'][:8])
                ledger.write(f"| {k} | {r['schema']} | `{l[:60].replace('|', '/')}` | {r['run']} | {r['runs']} | {r['hits']} | {r['born']} | {r['refused']} | {r['seconds']:.2f} | {outs} |\n"); ledger.flush()
        if ledger: ledger.close()
        print(f"routers: main {env.main.hops} hops in {env.main.commits} commits, {env.main.refused} refused; sixth {env.sixth.hops} hops in {env.sixth.commits} commits, {env.sixth.refused} refused")
        return
    while True:
        try: l = input('> ')
        except EOFError: break
        if l.strip(): type_line(env, fill(db, l))

if __name__ == '__main__':
    sys.setrecursionlimit(1000000)
    threading.stack_size(1 << 30)
    t = threading.Thread(target=main); t.start(); t.join()
