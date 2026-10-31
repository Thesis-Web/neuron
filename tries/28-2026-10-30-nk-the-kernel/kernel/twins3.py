#!/usr/bin/env python3
# twins3.py: are the two brains the same physics? their triggers compared; and why P shows no define run for words it spawned early
import json, urllib.request, time, hashlib
def q(port, sql, timeout=900):
    req = urllib.request.Request(f'http://127.0.0.1:{port}/api/q', data=json.dumps({'sql': sql}).encode(), headers={'content-type': 'application/json'})
    d = json.load(urllib.request.urlopen(req, timeout=timeout)); return d.get('rows', d)
T = {}
for name, port in (('live', 8056), ('P', 8057)):
    rows = q(port, "SELECT name, sql FROM sqlite_master WHERE type = 'trigger' ORDER BY name"); T[name] = {r[0]: hashlib.sha1(r[1].encode()).hexdigest()[:10] for r in rows}
    srows = q(port, "SELECT name, sql FROM sixth.sqlite_master WHERE type = 'trigger' ORDER BY name"); T[name + '6'] = {r[0]: hashlib.sha1(r[1].encode()).hexdigest()[:10] for r in srows}
print("main triggers:", "identical" if T['live'] == T['P'] else "DIFFER: " + str([k for k in set(T['live']) | set(T['P']) if T['live'].get(k) != T['P'].get(k)]))
print("sixth triggers:", "identical" if T['live6'] == T['P6'] else "DIFFER: " + str([k for k in set(T['live6']) | set(T['P6']) if T['live6'].get(k) != T['P6'].get(k)]))
for name, port in (('live', 8056), ('P', 8057)):
    t = time.time()
    d = q(port, "SELECT (SELECT gate FROM label WHERE symbol = 'define'), (SELECT count(*) FROM third), (SELECT count(*) FROM run WHERE arrival = 5 AND kind = 0), (SELECT count(*) FROM run r WHERE r.arrival = 5 AND r.kind = 0 AND EXISTS (SELECT 1 FROM run_sheet s WHERE s.run = r.id AND s.cell = 23)), (SELECT count(*) FROM run r WHERE r.arrival = 5 AND r.kind = 0 AND EXISTS (SELECT 1 FROM run_sheet s WHERE s.run = r.id AND s.cell = 24 AND s.state = 1)), (SELECT count(*) FROM run r WHERE r.arrival = 5 AND r.kind = 0 AND NOT EXISTS (SELECT 1 FROM run_memory m WHERE m.run = r.id))")[0]
    print(f"{name} ({time.time() - t:.0f} s): define gate {d[0]}; lines from the sixth {d[1]}; runs from the sixth {d[2]}; with a what cell {d[3]}; with def filled {d[4]}; without an end yet {d[5]}")
    last = q(port, "SELECT t.run, (SELECT group_concat(symbol, '') FROM (SELECT l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = t.run ORDER BY s.pos)), (SELECT value FROM run_sheet WHERE run = t.run AND cell = 23), (SELECT state FROM run_sheet WHERE run = t.run AND cell = 24) FROM third t ORDER BY t.id DESC LIMIT 4")
    print("   the newest lines from the sixth:", [(r[0], (r[1] or '')[:28], r[2], r[3]) for r in last])
    hop = q(port, "SELECT count(*), min(id), max(id) FROM hop"); print("   mailbox rows:", hop[0])
