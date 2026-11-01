#!/bin/bash
# hub-go6.sh: the page's graph read finds each run's first symbol by the run's key, not by a sweep of seq.
log(){ echo "$(date +%H:%M:%S) $*"; }
HUB=/home/exnulla/neuron/hub; P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; log "door down"
cd $HUB/page; python3 -I - <<'PY'
s = open("serve7.py").read()
a = """    firsts = dict(db.execute(f"SELECT run, gate FROM {schema}.seq WHERE pos = 1").fetchall())"""
b = """    firsts = dict(db.execute(f"SELECT id, g FROM (SELECT id, (SELECT gate FROM {schema}.seq WHERE run = r.id AND pos = 1) AS g FROM {schema}.run r) WHERE g IS NOT NULL").fetchall())"""
assert s.count(a) == 1; open("serve7.py", "w").write(s.replace(a, b))
PY
setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; T0=$(date +%s); curl -s -m 170 -o /dev/null -w "graph read: %{http_code} %{size_download} bytes %{time_total} s\n" "http://localhost:8056/api/graph?schema=main"; curl -s -m 170 -o /dev/null -w "run list: %{http_code} %{size_download} bytes %{time_total} s\n" -H 'Content-Type: application/json' -d '{"sql":"SELECT id, arrival, parent, root, kind, cell, about, at FROM main.run ORDER BY id"}' http://localhost:8056/api/q; echo FINISHED
