#!/usr/bin/env python3
# serve8_patch.py (2026-11-03, tries/43): the kernel's door tells the page. The door passes every typed line; when the line's answer returns
# (the kernel pumped the run until it ended or nothing was pending), the door reads the moves since the clock it last told and the run count,
# and puts them on every open page stream. No timer: the kernel is asked only when the door itself passed a line. GET /api/stream holds one
# response per tab open (server-sent events); POST /api/hold names the gates a tab holds, so its stream carries moves of those gates only.
# The kernel binary is untouched. usage: python3 serve8_patch.py <serve8.py>
import sys
path = sys.argv[1]; t = open(path, encoding='utf-8').read()

old = "import time, sys, os, json, socket, re, time, http.server, urllib.parse\n"
assert t.count(old) == 1, 'imports'
t = t.replace(old, old + "import queue, threading\n")

old = "RUNS = []\n"
assert t.count(old) == 1, 'RUNS'
t = t.replace(old, old + '''SUBS = []; HOLD = {}; TOLD = {'clock': 0, 'runs': 0}; TELL_LOCK = threading.Lock()   # tries/43: the open page streams, what each tab holds, what was told last
def tell(why):
    """tries/43 (2026-11-03; the owner: "a timer and a sweep... both which just won't work in a system like this"): the door tells the page.
    After a line the door passed, the moves since the clock last told (the timeline's move receipts, from the kernel's moved verb) and the
    run count go to every open page stream; the page reads the runs that ended by their ids and glides the points moved. The kernel is asked
    here only because the door itself just passed a line; never on a clock. The kernel's own pending work ending a run after the line
    returned, and a line typed on the kernel's socket without this door, are not told: that is the kernel's own tell, on the owner's word."""
    if not SUBS: return
    with TELL_LOCK:
        try: m = ask('moved ' + str(TOLD['clock'])); st = ask('stats')
        except Exception: return
        runs = (st.get('main') or {}).get('runs') or 0
        ev = {'moves': [[r[0], r[1], r[2], r[3], r[4], 0] for r in (m.get('moved') or [])], 'passes': m.get('passes') or 0, 'runs': runs, 'runs_before': TOLD['runs'], 'clock': m.get('clock'), 'why': why}
        TOLD['clock'] = m.get('clock') or TOLD['clock']; TOLD['runs'] = runs
    for s in list(SUBS):
        try: s.put_nowait(ev)
        except queue.Full:
            try: SUBS.remove(s)
            except ValueError: pass
''')

old = "            if u.path == '/api/moved': return self.send(200, ask('moved ' + str(int(qs.get('since', ['0'])[0]))))"
assert t.count(old) == 1, '/api/moved'
t = t.replace(old, old + "\n            if u.path == '/api/stream': return self.stream(qs)   # tries/43: the door tells the page")

old = "    def do_POST(self):\n        u = urllib.parse.urlparse(self.path)\n        try: d = self.body()\n        except Exception as e: return self.send(400, {'error': 'bad json: ' + str(e)})\n        try:\n"
assert t.count(old) == 1, 'do_POST head'
t = t.replace(old, '''    def stream(self, qs):
        """tries/43: one open response per tab (server-sent events); tell() puts an event here after every line this door passed. No timer:
        this response waits on the queue. A tab that stopped reading is dropped at the next write."""
        tab = (qs.get('tab') or [''])[0]; sq = queue.Queue(maxsize=4096)
        if not SUBS:
            try:
                TOLD['runs'] = (ask('stats').get('main') or {}).get('runs') or 0
                if TOLD['clock'] == 0: TOLD['clock'] = ((q('SELECT n FROM main.clock') or {}).get('rows') or [[0]])[0][0] or 0   # the first stream begins at the clock now
            except Exception: pass
        SUBS.append(sq)
        self.send_response(200); self.send_header('Content-Type', 'text/event-stream; charset=utf-8'); self.send_header('Cache-Control', 'no-store'); self.send_header('Access-Control-Allow-Origin', '*'); self.end_headers()
        try:
            self.wfile.write(('data: ' + json.dumps({'hello': 'the kernel door tells', 'clock': TOLD['clock'], 'runs': TOLD['runs']}) + '\\n\\n').encode()); self.wfile.flush()
            while True:
                ev = sq.get(); hold = HOLD.get(tab) if tab else None
                moves = ev['moves'] if hold is None else [mv for mv in ev['moves'] if mv[0] in hold]
                if not moves and not ev['passes'] and ev['runs'] <= ev['runs_before']: continue
                self.wfile.write(('data: ' + json.dumps(dict(ev, moves=moves)) + '\\n\\n').encode()); self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError): pass
        finally:
            try: SUBS.remove(sq)
            except ValueError: pass
            if tab: HOLD.pop(tab, None)
    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        try: d = self.body()
        except Exception as e: return self.send(400, {'error': 'bad json: ' + str(e)})
        if u.path == '/api/hold':   # tries/43: the gates a tab holds (its zoom); kept at the door, nothing asked of the kernel
            tab = str(d.get('tab') or ''); s = HOLD.setdefault(tab, set())
            if d.get('gates') is not None: s.clear(); s.update(int(g) for g in d['gates'])
            s.update(int(g) for g in (d.get('add') or []))
            return self.send(200, {'tab': tab, 'held': len(s)})
        try:
''')

old = "                JOBS[j['id']] = j; return self.send(200, j)\n"
assert t.count(old) == 1, 'type end'
t = t.replace(old, "                JOBS[j['id']] = j; tell('type'); return self.send(200, j)   # tries/43: the brain changed by this line: the page streams are told now\n")

open(path, 'w', encoding='utf-8').write(t)
print('patched', path, ': /api/stream, /api/hold, tell() after every typed line')
