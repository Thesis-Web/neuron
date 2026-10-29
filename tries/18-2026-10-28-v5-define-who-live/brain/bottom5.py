#!/usr/bin/env python3
# bottom5.py (2026-10-28): the env handler and the prompts (the owner's outline 10-25 21:50, lines 1, 9 to 12).
# It opens the main brain, loads mother, attaches the sixth, the guessing brain and the eight source brains, and then does two
# things: a line typed at the user's prompt is written into main.input; a line typed at the sixth's prompt (prefix "6> ") is written
# into sixth.input. Mother's prompt is the SQL prompt she pastes into; no one else types there. It prints what lands in the out
# mailboxes (out_user of each brain), read back through that brain's encoder, because the brain holds numbers. It decides nothing.
# usage: python3 bottom5.py [--lines FILE] [--ledger FILE] [--quiet]      interactive when no --lines; Ctrl-D leaves.
# In a lines file, "{run:k}" is replaced by the run number that line k of the file started, "{gate:x}" by the gate of symbol x in the
# main brain's encoder and "{gate6:x}" in the sixth's: the teacher reading numbers back from the brain, as at the terminal.
import os, re, sqlite3, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
BRAIN = os.path.join(HERE, 'brain.db'); SIXTH = os.path.join(HERE, 'sixth.db')
SRC = os.path.join(ROOT, 'sources'); SOURCES = ['wn', 'gcide', 'mw', 'mwt', 'moby', 'map', 'sqldoc', 'measured', 'guess']
POINTERS = {22, 24, 25, 27}   # cells whose value points at a run: reply, def, say, remember (the fresh egg's gate numbers)

def open_brain():
    db = sqlite3.connect(BRAIN, isolation_level=None)
    db.enable_load_extension(True); db.load_extension(os.path.join(HERE, 'mother'))
    db.execute('PRAGMA recursive_triggers = ON')
    db.execute('ATTACH ? AS sixth', (SIXTH,))
    for s in SOURCES: db.execute(f'ATTACH ? AS {s}', (os.path.join(SRC, s + '.db'),))
    return db

def decode(db, schema, run):
    r = db.execute(f"SELECT group_concat(symbol, '') FROM (SELECT l.symbol FROM {schema}.seq s JOIN {schema}.label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos)", (run,)).fetchone()
    return r[0] if r and r[0] is not None else ''

def show_out(db, schema, since, quiet):
    rows = db.execute(f"SELECT o.id, o.run, o.cell, o.value, (SELECT symbol FROM {schema}.label WHERE gate = o.cell) FROM {schema}.out_user o WHERE o.id > ? ORDER BY o.id", (since,)).fetchall()
    out = []
    for oid, run, cell, value, cname in rows:
        v = value
        if value is not None and str(value).isdigit() and int(value) > 0 and cell in POINTERS:
            arrival = db.execute(f"SELECT arrival FROM {schema}.run WHERE id = ?", (int(value),)).fetchone()
            who = db.execute(f"SELECT symbol FROM {schema}.label WHERE gate = ?", (arrival[0],)).fetchone() if arrival else None
            v = f"run {value} from {who[0] if who else '?'}: {decode(db, schema, int(value))[:160]}"
        out.append((schema, run, cname, v))
        if not quiet: print(f"  {schema} run {run} · {cname}: {v}")
    return (rows[-1][0] if rows else since), out

RUNS = []   # the run each typed line started, in order
def fill(db, line):
    def r(m):
        k = int(m.group(1)); return str(RUNS[k - 1]) if 0 < k <= len(RUNS) and RUNS[k - 1] else m.group(0)
    line = re.sub(r'\{run:(\d+)\}', r, line)
    def g(m):
        schema = 'sixth' if m.group(1) == '6' else 'main'
        row = db.execute(f"SELECT gate FROM {schema}.label WHERE symbol = ?", (m.group(2),)).fetchone()
        return str(row[0]) if row else m.group(0)
    return re.sub(r'\{gate(6?):([^}]+)\}', g, line)

def type_line(db, line, quiet=False):
    schema, text = 'main', line
    if line.startswith('6> '): schema, text = 'sixth', line[3:]
    t = time.time()
    before_s = db.execute("SELECT coalesce(max(id), 0) FROM sixth.out_user").fetchone()[0]
    before_m = db.execute("SELECT coalesce(max(id), 0) FROM main.out_user").fetchone()[0]
    runs0 = db.execute(f"SELECT coalesce(max(id), 0) FROM {schema}.run").fetchone()[0]
    gates0 = db.execute("SELECT count(*) FROM main.label").fetchone()[0]
    refused0 = db.execute("SELECT count(*) FROM main.refused").fetchone()[0] + db.execute("SELECT count(*) FROM sixth.refused").fetchone()[0]
    try:
        db.execute(f"INSERT INTO {schema}.input (text) VALUES (?)", (text,))
    except sqlite3.Error as e:
        print('refused:', e); RUNS.append(None); return None
    RUNS.append(runs0 + 1)
    runs1 = db.execute(f"SELECT coalesce(max(id), 0) FROM {schema}.run").fetchone()[0]
    hits = db.execute(f"SELECT count(*) FROM {schema}.run_receipt WHERE run > ?", (runs0,)).fetchone()[0]
    gates1 = db.execute("SELECT count(*) FROM main.label").fetchone()[0]
    refused1 = db.execute("SELECT count(*) FROM main.refused").fetchone()[0] + db.execute("SELECT count(*) FROM sixth.refused").fetchone()[0]
    dt = time.time() - t
    if not quiet: print(f"  [{schema}: run {runs0 + 1}, {runs1 - runs0} runs, {hits} hits, {gates1 - gates0} born, {dt:.2f} s]")
    _, o1 = show_out(db, 'main', before_m, quiet); _, o2 = show_out(db, 'sixth', before_s, quiet)
    return {'schema': schema, 'run': runs0 + 1, 'runs': runs1 - runs0, 'hits': hits, 'born': gates1 - gates0, 'refused': refused1 - refused0, 'seconds': dt, 'out': o1 + o2}

def main():
    quiet = '--quiet' in sys.argv
    lines = None; ledger = None
    if '--lines' in sys.argv: lines = [l.rstrip('\n') for l in open(sys.argv[sys.argv.index('--lines') + 1], encoding='utf-8')]
    if '--ledger' in sys.argv: ledger = open(sys.argv[sys.argv.index('--ledger') + 1], 'w', encoding='utf-8')
    db = open_brain()
    if lines is not None:
        k = 0
        if ledger: ledger.write("| # | prompt | line | run | runs | hits | born | refused | s | what the brain put in its out mailbox |\n|---|---|---|---|---|---|---|---|---|---|\n")
        for l in lines:
            if not l.strip() or l.startswith('#'):
                if ledger and l.startswith('# '): ledger.write(f"| | | *{l[2:].replace('|', '/')}* | | | | | | | |\n")
                continue
            k += 1
            l = fill(db, l)
            print('>', l[:140] + ('…' if len(l) > 140 else ''))
            r = type_line(db, l, quiet)
            if ledger:
                if r is None: ledger.write(f"| {k} | | {l[:60].replace('|', '/')} | refused | | | | | | |\n"); continue
                outs = '<br>'.join(f"{s} run {run} · {c}: {str(v)[:90].replace('|', '/')}" for (s, run, c, v) in r['out'][:8])
                ledger.write(f"| {k} | {r['schema']} | `{l[:60].replace('|', '/')}` | {r['run']} | {r['runs']} | {r['hits']} | {r['born']} | {r['refused']} | {r['seconds']:.2f} | {outs} |\n")
        if ledger: ledger.close()
        return
    while True:
        try: l = input('> ')
        except EOFError: break
        if l.strip(): type_line(db, fill(db, l))

if __name__ == '__main__':
    sys.setrecursionlimit(1000000)
    threading.stack_size(1 << 30)
    t = threading.Thread(target=main); t.start(); t.join()
