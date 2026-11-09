# tries/58: the kernel door as a module: type a line, keyed reads, a run's sheet. Every mother reply read back.
import json, re, sys, time, urllib.request
class Door:
    def __init__(self, door): self.door = door
    def post(self, path, body):
        r = urllib.request.Request(self.door + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
        return json.load(urllib.request.urlopen(r, timeout=600))
    def q(self, sql, params=()): return self.post('/api/q', {'sql': sql, 'params': list(params)}).get('rows') or []
    def gate(self, sym):
        rows = self.q('SELECT gate FROM label WHERE symbol = ?', [sym]); return rows[0][0] if rows else None
    def sym(self, g):
        rows = self.q('SELECT symbol FROM label WHERE gate = ?', [g]); return rows[0][0] if rows else '?'
    def typed(self, line, quiet=False):
        t = time.time(); j = self.post('/api/type', {'line': line}); r = j.get('result') or {}
        if not quiet: print('typed %-48s run %s, %s runs, %s hits, %s born, %s refused, %.3f s' % (line[:48], r.get('run'), r.get('runs'), r.get('hits'), r.get('born'), r.get('refused'), r.get('seconds') or (time.time() - t)))
        return r
    def run(self, rid): return json.load(urllib.request.urlopen(self.door + '/api/run?schema=main&id=%d' % rid, timeout=120))
    def sheet(self, rid):
        x = self.run(rid); return {c[0]: (c[2], c[3]) for c in (x.get('cells') or [])}
    def replies(self, rid):
        # every mother reply under this run and its kids: the reply cell 22 texts
        x = self.run(rid); out = []
        for c in (x.get('cells') or []):
            if c[0] == 22 and isinstance(c[3], dict): out.append(c[3].get('text'))
        for k in (x.get('kids') or []):
            kid = k if isinstance(k, int) else k.get('id') if isinstance(k, dict) else None
            if kid: out += self.replies(kid)
        return out
    def resolve(self, line, runs):
        # {gate:word} and {run:N} as nkbottom.py does: N = the Nth typed run of this file (1-based)
        line = re.sub(r'\{gate:([^}]+)\}', lambda m: str(self.gate(m.group(1)) or 'NOGATE'), line)
        return re.sub(r'\{run:(\d+)\}', lambda m: str(runs[int(m.group(1)) - 1]), line)
