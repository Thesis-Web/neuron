# compare_pick2.py (tries/51): the same counts as compare_pick.py, read once per point, then two orderings printed side by side: the raw counts
# (agreement, meanings, relationships: the longest rows win) and the shares (each count divided by the row's words, so a row is judged by how much
# of what it says the other sources also say and the graph already holds). Rows under 4 words are left out of the shares (a bare head or mark).
import json, sys, time, urllib.request
host = sys.argv[1]; words = sys.argv[2:]
def q(sql, params=()):
    r = urllib.request.Request(host + '/api/q', data=json.dumps({'sql': ' '.join(sql.split('\n')), 'params': list(params)}).encode(), headers={'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=300))
def text(rid):
    t = json.load(urllib.request.urlopen(host + '/api/run?schema=main&id=%d' % rid, timeout=60))['run'].get('text') or ''
    i = t.find('[definition:'); return (t[i + 13:i + 80] if i >= 0 else t[:70]).replace('\n', ' ')
names = {7: 'wn', 8: 'gcide', 10: 'mwt', 11: 'moby', 12: 'map', 13: 'sqldoc', 14: 'measured', 15: 'guess', 443: 'wikt'}
SQL = """WITH w AS MATERIALIZED ( SELECT DISTINCT n.id AS row , n.source AS src , n.run AS run , s.gate AS g FROM node n JOIN seq s ON s.run = n.run JOIN label l ON l.gate = s.gate WHERE n.gate = ? AND l.symbol GLOB '[A-Za-z]*' )
SELECT w.row , w.src , w.run , count ( * ) AS words , sum ( EXISTS ( SELECT 1 FROM w o WHERE o.g = w.g AND o.src <> w.src ) ) AS agree , sum ( EXISTS ( SELECT 1 FROM node d WHERE d.gate = w.g ) ) AS meanings , sum ( EXISTS ( SELECT 1 FROM rel r WHERE r.gate = w.g ) ) AS rels FROM w GROUP BY w.row , w.src , w.run"""
dict_src = (8, 443)
for wd in words:
    g = q('SELECT gate FROM label WHERE symbol = ?', [wd])['rows']
    if not g: print(wd, 'no gate'); continue
    t0 = time.perf_counter(); r = q(SQL, [g[0][0]]); ms = (time.perf_counter() - t0) * 1000
    rows = r.get('rows') or []
    if r.get('error') or not rows: print(wd, 'error or no rows', r.get('error')); continue
    raw = sorted(rows, key=lambda x: (-x[4], -x[5], -x[6], x[2]))[0]
    cand = [x for x in rows if x[3] >= 4] or rows
    share = sorted(cand, key=lambda x: (-(x[4] / x[3]), -(x[5] / x[3]), -(x[6] / x[3]), 0 if x[1] in dict_src else 1, x[2]))[0]
    print('%-6s %5.0f ms  %3d rows | raw   : %-6s run %8d %3d/%3d words agree: %s' % (wd, ms, len(rows), names.get(raw[1], raw[1]), raw[2], raw[4], raw[3], text(raw[2])))
    print('%-6s                   | shares: %-6s run %8d agree %.2f meanings %.2f rels %.2f of %3d: %s' % ('', names.get(share[1], share[1]), share[2], share[4] / share[3], share[5] / share[3], share[6] / share[3], share[3], text(share[2])))
