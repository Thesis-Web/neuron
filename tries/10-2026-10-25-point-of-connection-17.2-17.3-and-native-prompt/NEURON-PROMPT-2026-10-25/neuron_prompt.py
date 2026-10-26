# A prompt for the brain on native SQLite (full stack depth). The same bottom as the page: it writes a typed line into input and
# reads output; mother is host15.py's. It decides nothing. The brain is kept in a .db file, so it stays alive between sessions.
# usage: python3 -I neuron_prompt.py <dir holding host15.py> <told.json> <sat.json> <brain.db> [sheet.json]
#   a line runs; ":sheet" types the whole teaching sheet, ":save" writes the brain to its .db file, ":q" saves and quits.
import json, os, sqlite3, sys, time
sys.path.insert(0, sys.argv[1]); from host15 import Brain
told, sat, dbfile = sys.argv[2], json.load(open(sys.argv[3])), sys.argv[4]
sheet = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else []
b = Brain(told, sat=sat)
if os.path.exists(dbfile):
    src = sqlite3.connect(dbfile); src.backup(b.con, name='main'); src.close()   # the brain as it was saved (sources are reattached by the host)
    print('brain loaded from', dbfile)
def save():
    dst = sqlite3.connect(dbfile); b.con.backup(dst, name='main'); dst.close(); print('brain saved to', dbfile)
def run(line):
    t = time.time()
    try: out = b.type(line)
    except Exception as e: print('  the brain refused the line:', e); return
    print(f'  [{time.time() - t:.1f} s] {out}')
while True:
    try: line = input('neuron> ').strip()
    except EOFError: break
    if not line: continue
    if line == ':q': break
    if line == ':save': save(); continue
    if line == ':sheet':
        for lab, l in sheet: print('neuron>', l[:100] + ('...' if len(l) > 100 else '')); run(l)
        continue
    run(line)
save()
