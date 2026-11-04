# compare_pick.py (tries/51): the owner, 22:05: "it's not a race... tied? meaning they said the same thing, or the value of what they said is the
# same thing, then we look to our meanings, which of the words returned actually have meanings in the graph... also relationships.. which words
# returned have defined relationships already". A read over a point's definition rows from every source: for each row, the count of its words
# (letter symbols) that another source's row also holds (agreement), the count that are defined points in the graph (meanings), the count that
# hold relationship rows (relationships). The definition: the highest agreement, then meanings, then relationships, then the lowest run; the
# candidates the dictionaries' rows (ranks 1) when the point has any, else every row. Prints the pick per word, timed, and the top rows for a few.
# The kernel's socket takes one line per request, so the SQL is joined into one line before it is sent.
import json, sys, time, urllib.request
host = sys.argv[1]; words = sys.argv[2:]
def q(sql, params=()):
    r = urllib.request.Request(host + '/api/q', data=json.dumps({'sql': sql, 'params': list(params)}).encode(), headers={'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=300))
def text(rid):
    t = json.load(urllib.request.urlopen(host + '/api/run?schema=main&id=%d' % rid, timeout=60))['run'].get('text') or ''
    i = t.find('[definition:'); return (t[i + 13:i + 95] if i >= 0 else t[:85]).replace('\n', ' ')
names = {7: 'wn', 8: 'gcide', 10: 'mwt', 11: 'moby', 12: 'map', 13: 'sqldoc', 14: 'measured', 15: 'guess', 443: 'wikt'}
SQL = """WITH w AS MATERIALIZED ( SELECT DISTINCT n.id AS row , n.source AS src , n.run AS run , s.gate AS g FROM node n JOIN seq s ON s.run = n.run JOIN label l ON l.gate = s.gate WHERE n.gate = ? AND l.symbol GLOB '[A-Za-z]*' ) ,
sc AS ( SELECT w.row , w.src , w.run , count ( * ) AS words , sum ( EXISTS ( SELECT 1 FROM w o WHERE o.g = w.g AND o.src <> w.src ) ) AS agree , sum ( EXISTS ( SELECT 1 FROM node d WHERE d.gate = w.g ) ) AS meanings , sum ( EXISTS ( SELECT 1 FROM rel r WHERE r.gate = w.g ) ) AS rels FROM w GROUP BY w.row , w.src , w.run )
SELECT sc.run , sc.src , sc.agree , sc.meanings , sc.rels , sc.words FROM sc LEFT JOIN ranks p ON p.cell = 24 AND p.source = sc.src ORDER BY %s coalesce ( p.rank , 9 ) , sc.agree DESC , sc.meanings DESC , sc.rels DESC , sc.run LIMIT %d"""
for w in words:
    g = q('SELECT gate FROM label WHERE symbol = ?', [w])['rows']
    if not g: print(w, 'no gate'); continue
    g = g[0][0]; t0 = time.perf_counter()
    r = q(' '.join(SQL.split('\n')) % ('', 3), [g]); ms = (time.perf_counter() - t0) * 1000
    if r.get('error'): print(w, 'error', r['error']); continue
    rows = r['rows']
    if not rows: print(w, 'no rows'); continue
    rid, src, agree, mean, rels, nw = rows[0]
    print('%-6s %6.0f ms  dictionaries first: run %8d %-6s agree %3d meanings %3d rels %3d of %3d words: %s' % (w, ms, rid, names.get(src, src), agree, mean, rels, nw, text(rid)))
    r2 = q(' '.join(SQL.split('\n')) % ('', 400), [g])['rows']; r2 = sorted(r2, key=lambda x: (-x[2], -x[3], -x[4], x[0]))[0]   # every source, no ranks
    if r2[0] != rid: print('%-6s        every source  : run %8d %-6s agree %3d meanings %3d rels %3d of %3d words: %s' % ('', r2[0], names.get(r2[1], r2[1]), r2[2], r2[3], r2[4], r2[5], text(r2[0])))
    if w in ('who', 'the', 'can'):
        for x in rows[1:3]: print('%-6s        next          : run %8d %-6s agree %3d meanings %3d rels %3d of %3d words: %s' % ('', x[0], names.get(x[1], x[1]), x[2], x[3], x[4], x[5], text(x[0])))
