# cascade_demo.py: on the v7 copy at 8057: bind the self-feeding observing line, type define : word, then watch the brain define its own
# unknowns for a few minutes while reading and typing through the door; then put the collect-only observing line back.
import json, time, urllib.request, sys
U = 'http://127.0.0.1:8057'
def get(p):
    t = time.perf_counter(); r = json.load(urllib.request.urlopen(U + p, timeout=300)); return r, time.perf_counter() - t
def post(p, d): return json.load(urllib.request.urlopen(urllib.request.Request(U + p, data=json.dumps(d).encode(), headers={'Content-Type': 'application/json'}), timeout=300))
def typed(line, prompt='main'):
    j = post('/api/type', {'line': line, 'prompt': prompt}); t = time.perf_counter()
    while not j['done']: time.sleep(0.5); j, _ = get('/api/job?id=%d' % j['id'])
    return j['result'], time.perf_counter() - t
def q(sql): return post('/api/q', {'sql': sql})['rows']
def say(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
lines = [l for l in open(sys.argv[1], encoding='utf-8').read().split('\n') if l.strip() and not l.startswith('#')]
r, dt = typed(lines[0], 'sixth'); say(f"feed line typed: sixth run {r['run']}, {r['seconds']:.1f} s, refused {r['refused']}")
bind = lines[1].replace('{run:1}', str(r['run'])); r2, dt = typed(bind, 'sixth'); say(f"bind typed: {r2['out'][-1][3] if r2['out'] else ''}")
before = q("SELECT count(*) FROM run WHERE kind = 0 AND arrival = 5 AND id IN (SELECT run FROM seq WHERE pos = 1 AND gate = 153)")[0][0]
r, dt = typed('define : word'); say(f"define : word returned at its own end: {r['seconds']:.1f} s, {r['runs']} runs, {r['hits']} hits, {r['born']} born, refused {r['refused']}")
say('  def:', [str(v)[:90] for (s, run, c, v) in r['out'] if c == 'def'])
t0 = time.time(); typed_mid = False
while time.time() - t0 < 330:
    time.sleep(30)
    info, _ = get('/api/info'); rt = info['routers']
    n = q("SELECT count(*) FROM run WHERE kind = 0 AND arrival = 5 AND id IN (SELECT run FROM seq WHERE pos = 1 AND gate = 153)")[0][0] - before
    done = q("SELECT count(*) FROM run_memory WHERE run IN (SELECT id FROM run WHERE kind = 0 AND arrival = 5 AND id IN (SELECT run FROM seq WHERE pos = 1 AND gate = 153))")[0][0]
    sent = q("SELECT count(*) FROM sixth.spawned WHERE sent = 1")[0][0]; pend = q("SELECT count(*) FROM sixth.spawned WHERE sent = 0")[0][0]
    newest = q("SELECT group_concat(l.symbol, ' ') FROM (SELECT s.gate FROM run_sheet s JOIN seq qq ON qq.run = s.run AND qq.pos = 1 AND qq.gate = 153 JOIN run r ON r.id = s.run WHERE s.cell = 23 AND r.arrival = 5 AND EXISTS (SELECT 1 FROM run_memory m WHERE m.run = s.run) ORDER BY s.run DESC LIMIT 8) x JOIN label l ON l.gate = x.gate")[0][0]
    say(f"main hops {rt['main']['hops']}, sixth hops {rt['sixth']['hops']}; define lines from the sixth: {n} started, {done} ended so far; spawned sent {sent}, pending {pend}; newest ended: {newest}")
    if not typed_mid and time.time() - t0 > 60:
        g, dtg = get('/api/graph?schema=main'); say(f"  graph read during the cascade: {dtg:.1f} s, {len(g['dna'])} rows")
        rr, dtt = typed('print dna : who'); say(f"  typed print dna : who during the cascade: returned in {dtt:.1f} s, say = {[str(v)[:60] for (s, run, c, v) in rr['out'] if c == 'say']}")
        typed_mid = True
r3, _ = typed('6> BUILD UPDATE sixth."82" SET call = 1077 WHERE before = 6 AND trigger = 68 ; BUILD', 'sixth'); say('seen bound back to the collect-only observing run 1077:', [str(v)[:40] for (s, run, c, v) in r3['out'] if c == 'reply'])
say('the define lines already started keep running on the copy until the door is stopped')
