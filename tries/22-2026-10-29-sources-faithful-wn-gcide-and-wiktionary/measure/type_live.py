#!/usr/bin/env python3
# type_live.py (2026-10-29): types the lines of a lines file into the live brain through the 8056 door, one at a time, the way the page does
# (POST /api/type), waiting for each to finish; {run:k} is filled with the run number line k of the file started, read back from the door.
# A typist only: it decides nothing and stops at the first line the door reports an error for. Not part of the brain; kept in the scratchpad.
# usage: python3 -I type_live.py <lines file> <type lines from k1> <to k2> [runs of the lines before k1, comma separated]
import sys, json, re, time, urllib.request
URL = 'http://127.0.0.1:8056'
lines = [l.rstrip('\n') for l in open(sys.argv[1], encoding='utf-8')]
k1, k2 = int(sys.argv[2]), int(sys.argv[3])
RUNS = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else []
assert len(RUNS) == k1 - 1, 'give the run number of every line before k1'
def fill(l):
    return re.sub(r'\{run:(\d+)\}', lambda m: str(RUNS[int(m.group(1)) - 1]), l)
def post(path, d):
    r = urllib.request.urlopen(urllib.request.Request(URL + path, data=json.dumps(d).encode(), headers={'Content-Type': 'application/json'}), timeout=30)
    return json.load(r)
def job(i):
    return json.load(urllib.request.urlopen(URL + '/api/job?id=%d' % i, timeout=30))
k = 0
for l in lines:
    if not l.strip() or l.startswith('#'): continue
    k += 1
    if k < k1: continue
    if k > k2: break
    l = fill(l)
    prompt = 'sixth' if l.startswith('6> ') else 'main'
    j = post('/api/type', {'line': l, 'prompt': prompt})
    while not j['done']:
        time.sleep(0.5); j = job(j['id'])
    r = j['result']
    if j.get('error') or r is None:
        print(f'{k}. STOPPED: door error {j.get("error")!r} for line: {l[:100]}'); sys.exit(1)
    RUNS.append(r['run'])
    outs = '; '.join(f"{c}: {str(v)[:90]}" for (s, run, c, v) in r['out'] if c in ('say', 'reply', 'what', 'newgate', 'def', 'known', 'unknown'))
    print(f"{k}. {prompt} run {r['run']}: {r['runs']} runs, {r['hits']} hits, {r['born']} born, {r['refused']} refused, {r['seconds']:.2f} s | {l[:60]}{'…' if len(l) > 60 else ''}\n     {outs}")
    if r['refused']: print('     STOPPED: SQLite refused something in this line'); sys.exit(1)
print('runs:', RUNS)
