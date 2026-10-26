#!/usr/bin/env python3
# bottom.py: each line typed is written into brain.db (table input); what the brain answers is printed. Ctrl-D leaves.
import os, sqlite3
here = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(here, 'brain.db'), isolation_level=None)
db.enable_load_extension(True)
db.load_extension(os.path.join(here, 'kernel', 'mother'))
db.execute('PRAGMA recursive_triggers = ON')
while True:
    try:
        line = input('> ')
    except EOFError:
        break
    try:
        run = db.execute('INSERT INTO input(text) VALUES(?)', (line,)).lastrowid
    except sqlite3.Error as e:
        print('refused:', e)
        continue
    answer = db.execute('SELECT answer FROM input WHERE id = ?', (run,)).fetchone()[0]
    if answer is not None:
        print(answer)
