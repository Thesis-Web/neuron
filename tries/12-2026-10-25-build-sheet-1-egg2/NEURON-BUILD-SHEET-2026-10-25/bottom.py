#!/usr/bin/env python3
# bottom.py: the prompt. Each line you type is written into brain.db (table input) and what the brain
# answered is printed, for the line and for every sub-run it started. Then anything the brain asked to
# run after the line (table later: a DROP SQLite refused inside the run) is run. Nothing else.
# usage: python3 bottom.py brain.db [source.db ...]      Ctrl-D leaves. The brain stays in the file.
import os, sqlite3, sys, time
here = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(sys.argv[1], isolation_level=None)
db.enable_load_extension(True)
db.load_extension(os.path.join(here, 'mother'))
db.execute('PRAGMA recursive_triggers = ON')
for src in sys.argv[2:]:
    db.execute('ATTACH ? AS ' + os.path.splitext(os.path.basename(src))[0], (src,))
while True:
    try:
        line = input('> ')
    except EOFError:
        break
    if not line.strip():
        continue
    t = time.time()
    try:
        run = db.execute('INSERT INTO input (text) VALUES (?)', (line,)).lastrowid
    except sqlite3.Error as e:
        print('refused:', e)
        continue
    for rid, parent, text, answer in db.execute(
            'SELECT id, parent, text, answer FROM input WHERE id >= ? ORDER BY id', (run,)):
        tag = f'run {rid}' + (f' (sub-run of {parent})' if parent else '')
        if rid != run:
            print(f'  {tag}: {text[:60]}{"..." if len(text) > 60 else ""}')
        if answer is not None:
            print(f'  {tag} said: {answer}')
    later = [t for (t,) in db.execute('SELECT text FROM later ORDER BY id').fetchall()]
    db.execute('DELETE FROM later')
    for text in later:
        print('  later:', text[:60], '->', db.execute('SELECT mother(?)', (text,)).fetchone()[0])
    print(f'  [{time.time() - t:.2f} s]')
