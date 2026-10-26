#!/usr/bin/env python3
# bottom.py: the prompt. Each line you type is written into brain.db (table input). Then every run that line started
# (the line itself, the runs the brain typed to itself, what the SQL prompt and the sources sent back) is printed,
# read back through the encoder, because the brain holds only gate numbers. Nothing else happens here.
# usage: python3 bottom.py brain.db [source.db ...]      Ctrl-D leaves. The brain stays in the file.
import os, sqlite3, sys, time
here = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(sys.argv[1], isolation_level=None)
db.enable_load_extension(True)
db.load_extension(os.path.join(here, 'mother'))
db.execute('PRAGMA recursive_triggers = ON')
for src in sys.argv[2:]:
    db.execute('ATTACH ? AS ' + os.path.splitext(os.path.basename(src))[0], (src,))
WORDS = ('SELECT id, parent, (SELECT word FROM encoder WHERE gate = i.arrival), '
         "(SELECT group_concat(word, '') FROM (SELECT e.word FROM json_each('[' || replace(i.gates, ' ', ',') || ']') j "
         'JOIN encoder e ON e.gate = j.value ORDER BY j.key)) FROM input i WHERE id >= ? ORDER BY id')
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
    for rid, parent, arrival, words in db.execute(WORDS, (run,)):
        if rid == run:
            continue
        words = words or ''
        print(f'  run {rid} ({arrival}, in run {parent}): {words[:100]}{"..." if len(words) > 100 else ""}')
    print(f'  [{time.time() - t:.2f} s]')
