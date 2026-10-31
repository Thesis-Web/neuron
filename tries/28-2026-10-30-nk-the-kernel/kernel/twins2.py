#!/usr/bin/env python3
# twins2.py: the same word defined by both brains, side by side: when, from which source the definition came, how many of its symbols were known then
import json, urllib.request, time
def q(port, sql, timeout=900):
    req = urllib.request.Request(f'http://127.0.0.1:{port}/api/q', data=json.dumps({'sql': sql}).encode(), headers={'content-type': 'application/json'})
    d = json.load(urllib.request.urlopen(req, timeout=timeout)); return d.get('rows', d)
WORDS = ['comparable', 'mother', 'memory', 'chemistry', 'bread', 'Greek']
for name, port in (('live 8056', 8056), ('copy P 8057', 8057)):
    t = time.time()
    rows = q(port, "SELECT l.symbol, p.id, (SELECT min(s.run) FROM run_sheet s JOIN seq z ON z.run = s.run AND z.pos = 1 AND z.gate = (SELECT gate FROM label WHERE symbol = 'define') WHERE s.cell = 23 AND s.value = l.gate) FROM sixth.spawned p JOIN label l ON l.gate = p.gate WHERE l.symbol IN (" + ",".join("'%s'" % w for w in WORDS) + ")")
    print(f"\n{name} ({time.time() - t:.0f} s): word, its place in the sixth's order, its define run")
    for (w, place, run) in rows:
        if not run: print(f"  {w}: spawned at {place}, not defined yet"); continue
        d = q(port, f"SELECT (SELECT value FROM run_sheet WHERE run = {run} AND cell = 24), (SELECT value FROM run_sheet WHERE run = {run} AND cell = (SELECT gate FROM label WHERE symbol = 'known')), (SELECT value FROM run_sheet WHERE run = {run} AND cell = (SELECT gate FROM label WHERE symbol = 'unknown')), (SELECT at FROM run WHERE id = {run})")[0]
        src = q(port, f"SELECT (SELECT symbol FROM label WHERE gate = arrival), (SELECT group_concat(symbol, '') FROM (SELECT l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = {int(d[0])} ORDER BY s.pos)) FROM run WHERE id = {int(d[0])}")[0] if d[0] and str(d[0]).isdigit() else (None, None)
        print(f"  {w}: spawned at {place}, define run {run} at clock {d[3]}: def from {src[0]}: {str(src[1])[:70]!r}; known {len((d[1] or '').split())}, unknown {len((d[2] or '').split())}")
