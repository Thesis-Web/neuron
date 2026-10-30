#!/usr/bin/env python3
# profile_define.py (2026-10-29): opens a COPY of the brain exactly as bottom6 does, traces every statement SQLite runs on the connection
# (statements inside mother and inside triggers included), types one line, and prints where the time went: per statement shape, total
# seconds and count. The gap from one statement's start to the next is charged to the first. Measurement only; it changes no row of the live brain.
import os, re, sys, sqlite3, time, threading, collections
HERE = sys.argv[1]; LINE = sys.argv[2]
ROOT = os.path.dirname(HERE); SRC = os.path.join(ROOT, 'sources')
SOURCES = ['wn', 'gcide', 'mwt', 'moby', 'map', 'sqldoc', 'measured', 'guess', 'wikt']
db = sqlite3.connect(os.path.join(HERE, 'brain.db'), isolation_level=None)
db.enable_load_extension(True); db.load_extension(os.path.join(HERE, 'mother'))
db.execute('PRAGMA recursive_triggers = ON')
db.execute('ATTACH ? AS sixth', (os.path.join(HERE, 'sixth.db'),))
for s in SOURCES: db.execute(f'ATTACH ? AS {s}', (os.path.join(SRC, s + '.db'),))
events = []
def tr(sql): events.append((time.perf_counter(), sql))
db.set_trace_callback(tr)
t0 = time.perf_counter()
db.execute("INSERT INTO main.input (text) VALUES (?)", (LINE,))
t1 = time.perf_counter()
db.set_trace_callback(None)
def shape(sql):
    s = re.sub(r'\s+', ' ', sql.strip())
    s = re.sub(r"'[^']*'", "'…'", s); s = re.sub(r'\b\d+\b', 'N', s)
    return s[:150]
tot = collections.Counter(); cnt = collections.Counter(); mx = collections.defaultdict(float)
for i, (t, sql) in enumerate(events):
    d = (events[i + 1][0] if i + 1 < len(events) else t1) - t
    k = shape(sql); tot[k] += d; cnt[k] += 1; mx[k] = max(mx[k], d)
print(f'line: {LINE}\ntotal {t1 - t0:.1f} s, {len(events)} statement starts\n')
print('--- top 30 statement shapes by total seconds (total, count, longest single)')
for k, v in tot.most_common(30): print(f'{v:8.2f} s  x{cnt[k]:6d}  max {mx[k]:6.2f}  {k}')
print('\n--- top 12 by count')
for k, c in cnt.most_common(12): print(f'x{c:7d}  {tot[k]:7.2f} s  {k}')
