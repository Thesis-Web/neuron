#!/bin/bash
# hub-go3.sh: a profile in the router, as the kernel has: what each hop costs, read from the running brain at /api/prof.
log(){ echo "$(date +%H:%M:%S) $*"; }
HUB=/home/exnulla/neuron/hub; P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; log "door down"
cd $HUB/brain; python3 - <<'PY'
s = open("bottom7.py").read()
a = "            text = row[1] or ''; params = tuple(row[2:2 + text.count('?')])\n            try:\n                if params or ';' not in text: db.execute(text, params)"
b = "            text = row[1] or ''; params = tuple(row[2:2 + text.count('?')]); t0 = time.perf_counter()\n            try:\n                if params or ';' not in text: db.execute(text, params)"
assert s.count(a) == 1; s = s.replace(a, b)
a = "            n += 1\n            self.serve()"
b = "            p = self.prof.setdefault(s + ' ' + text[:40], [0, 0.0]); p[0] += 1; p[1] += time.perf_counter() - t0\n            n += 1\n            self.serve()"
assert s.count(a) == 1; s = s.replace(a, b)
a = "        db.execute('COMMIT'); self.commits += 1; self.hops[s] += n"
b = "        t0 = time.perf_counter(); db.execute('COMMIT'); p = self.prof.setdefault('COMMIT', [0, 0.0]); p[0] += 1; p[1] += time.perf_counter() - t0; self.commits += 1; self.hops[s] += n"
assert s.count(a) == 1; s = s.replace(a, b)
a = "            try: out['result'] = fn(self.db)\n            except Exception as e: out['error'] = e\n            out['done'].set()\n    def batch"
b = "            t0 = time.perf_counter()\n            try: out['result'] = fn(self.db)\n            except Exception as e: out['error'] = e\n            p = self.prof.setdefault('door job', [0, 0.0]); p[0] += 1; p[1] += time.perf_counter() - t0\n            out['done'].set()\n    def batch"
assert s.count(a) == 1; s = s.replace(a, b)
a = "        self.jobs = queue.Queue()\n"
b = a + "        self.prof = {}\n"
assert s.count(a) == 1; open("bottom7.py", "w").write(s.replace(a, b))
s = open("../page/serve7.py").read()
a = "        if u.path == '/api/job':"
b = "        if u.path == '/api/prof': return self.send(200, {k: v for k, v in sorted(STATE['env'].router.prof.items(), key=lambda x: -x[1][1])[:16]})\n" + a
assert s.count(a) == 1; open("../page/serve7.py", "w").write(s.replace(a, b))
PY
cd $HUB/page; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; echo FINISHED
