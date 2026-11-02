#!/usr/bin/env python3
# g34/hub_recall.py (2026-11-02, 03:10). The recall on the hub (8056, v7: SQLite tables and triggers), in the hub's own shapes, typed through
# its prompt: the owner saw define : bread cost 82,905 hits the first time and 85,066 the second, the hub's define asking the sources again.
#  1. The ask (the hub's run 10510 with the standing question first): def copied from the run that learned the point; known and unknown read
#     now from the point's node table against the definitions that exist now (the hub's own formula for them); the sources asked only when
#     the point's node table is empty. A point's node table is main."<gate>.node"; `what` is substituted by the hub into the span text.
#  2. The define run (the hub's run 498941) with the ask swapped and its known/unknown span run only on source returns.
#  3. define's row (table "153", heard before, ':' after) calls it.
import json, urllib.request, time, sys
B = "http://localhost:8056"; WIKT = 3369
def post(path, obj, timeout=1700):
    rq = urllib.request.Request(B + path, data=json.dumps(obj).encode(), headers={"Content-Type": "application/json"}); return json.load(urllib.request.urlopen(rq, timeout=timeout))
def get(path, timeout=120): return json.load(urllib.request.urlopen(B + path, timeout=timeout))
def q(sql, params=[]):
    try: return post("/api/q", {"sql": sql, "params": params}, 600).get("rows")
    except Exception as e: return "ERR %s" % str(e)[:100]
def typed(line):
    t0 = time.time(); j = post("/api/type", {"line": line, "prompt": "main"}, 1700); jid = j.get("id")
    while jid and not j.get("done") and time.time() - t0 < 1650: time.sleep(2); j = get("/api/job?id=%s" % jid)
    r = j.get("result") or {}; rep = [str(o[3])[:140] for o in (r.get("out") or []) if o[2] == "reply"]
    print("  typed -> run %s, %s runs, %s hits, %.1f s, reply %s" % (r.get("run"), r.get("runs"), r.get("hits"), time.time() - t0, rep), flush=True); return r.get("run")
SRC = ("wn", "gcide", "mwt", "moby", "map", "sqldoc", "measured", "wikt")
NODE = 'main."what.node"'
KU = ("WITH x ( g , h ) AS MATERIALIZED ( SELECT DISTINCT s.gate , EXISTS ( SELECT 1 FROM run k WHERE k.kind = 3 AND k.about = s.gate AND ( k.arrival BETWEEN 7 AND 14 OR k.arrival = %d ) ) FROM %s n JOIN run r ON r.id = n.run JOIN seq s ON s.run = r.id JOIN label l ON l.gate = s.gate WHERE r.kind = 3 AND ( r.arrival BETWEEN 7 AND 14 OR r.arrival = %d ) AND l.symbol GLOB '[A-Za-z]*' ORDER BY s.gate ) "
      "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , k.gate , 1 , coalesce ( ( SELECT group_concat ( x.g , ' ' ) FROM x WHERE x.h = ( k.symbol = 'known' ) ) , '' ) FROM label k WHERE k.symbol IN ( 'known' , 'unknown' ) AND EXISTS ( SELECT 1 FROM %s )" % (WIKT, NODE, WIKT, NODE))
ASK = ("BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 24 , 0 , NULL ) ; "
       "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 24 , 1 , value FROM run_sheet WHERE run = ( SELECT parent FROM run WHERE id = ( SELECT max ( run ) FROM %s ) ) AND cell = 24 AND state = 1 ; " % NODE
       + KU + " ; " + " ; ".join("INSERT INTO %s.inbox ( run , cell , about , word ) SELECT above , 24 , what , symbol FROM label WHERE gate = what AND NOT EXISTS ( SELECT 1 FROM %s )" % (s, NODE) for s in SRC) + " ; BUILD")
def define_text(ask_run):
    return ("BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , ( SELECT gate FROM seq WHERE run = above AND pos = ( SELECT min ( pos ) FROM seq WHERE run = above AND gate = 68 ) + 2 ) ; INSERT INTO replay ( parent , source , kind ) VALUES ( above , %d , 1 ) ; BUILD " % ask_run
            + "BUILD INSERT OR IGNORE INTO rel ( gate , kind , other , run ) SELECT r.about , k.gate , s.gate , r.id FROM run r JOIN seq k ON k.run = r.id AND k.gate IN ( SELECT gate FROM label WHERE symbol IN ( 'like' , 'opposite' ) ) JOIN seq s ON s.run = r.id AND s.pos > k.pos JOIN label l ON l.gate = s.gate WHERE r.kind = 3 AND r.arrival IN ( 10 , 11 , 12 ) AND r.parent = above AND l.symbol GLOB '[A-Za-z]*' AND NOT ( l.symbol = 'of' AND s.pos = k.pos + 2 ) AND NOT EXISTS ( SELECT 1 FROM seq z JOIN label y ON y.gate = z.gate WHERE z.run = r.id AND z.pos > k.pos AND z.pos < s.pos AND y.symbol IN ( ';' , 'like' , 'opposite' ) ) ; BUILD "
            + "BUILD WITH x ( g , h ) AS MATERIALIZED ( SELECT DISTINCT s.gate , EXISTS ( SELECT 1 FROM run k WHERE k.kind = 3 AND k.about = s.gate AND ( k.arrival BETWEEN 7 AND 14 OR k.arrival = ( SELECT gate FROM label WHERE symbol = 'wikt' ) ) ) FROM run r JOIN seq s ON s.run = r.id JOIN label l ON l.gate = s.gate WHERE r.kind = 3 AND ( r.arrival BETWEEN 7 AND 14 OR r.arrival = ( SELECT gate FROM label WHERE symbol = 'wikt' ) ) AND r.parent = above AND l.symbol GLOB '[A-Za-z]*' ORDER BY s.gate ) INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , k.gate , 1 , coalesce ( ( SELECT group_concat ( x.g , ' ' ) FROM x WHERE x.h = ( k.symbol = 'known' ) ) , '' ) FROM label k WHERE k.symbol IN ( 'known' , 'unknown' ) AND EXISTS ( SELECT 1 FROM run WHERE parent = above AND kind = 3 AND ( arrival BETWEEN 7 AND 14 OR arrival = ( SELECT gate FROM label WHERE symbol = 'wikt' ) ) ) ; BUILD")
def bind_text(define_run): return 'BUILD UPDATE main."153" SET call = %d WHERE before IS 1 AND trigger IS 68 ; BUILD' % define_run
def hits_of(run): return q("SELECT count(*) FROM run_receipt WHERE run IN (SELECT id FROM run WHERE root = ?)", [run])
def sheet(run): return q("SELECT cell, state, substr(value, 1, 50), length(value) FROM run_sheet WHERE run = ? ORDER BY cell", [run])
def define(word):
    t0 = time.time(); r = post("/api/type", {"line": "define : " + word, "prompt": "main"}, 1700); jid = r.get("id")
    while jid and not r.get("done") and time.time() - t0 < 1650: time.sleep(1); r = get("/api/job?id=%s" % jid)
    x = r.get("result") or {}; run = x.get("run")
    g = q("SELECT gate FROM label WHERE symbol = ?", [word]); g = g[0][0] if g else None
    nodes = q('SELECT count(*) FROM "%d.node"' % g) if g else None
    returns = q("SELECT count(*) FROM run WHERE root = ? AND kind = 3 AND (arrival BETWEEN 7 AND 14 OR arrival = ?)", [run, WIKT])
    print("  define : %s -> run %s, %.2f s wall, %s kernel runs, hits %s, source returns %s, node rows %s, sheet %s" % (word, run, time.time() - t0, x.get("runs"), hits_of(run), returns, nodes, [(c[0], c[1], c[3]) for c in (sheet(run) or []) if c[0] in (24, 147, 152, 81)]), flush=True)
if __name__ == "__main__":
    print("define row before:", q('SELECT shard, before, trigger, call FROM main."153"'))
    print("1. the ask:"); ask_run = typed(ASK)
    print("2. the define run:"); def_run = typed(define_text(ask_run))
    print("3. the binding:"); typed(bind_text(def_run))
    print("define row after:", q('SELECT shard, before, trigger, call FROM main."153"'))
    open('/mnt/d/Neuron/tries/34-2026-11-01-define-recall-check/HUB-RECALL-v7.txt', 'w').write("# HUB-RECALL-v7.txt (2026-11-02, 03:10): the recall on the hub, typed through its prompt by hub_recall.py; the runs: ask %s, define %s.\n%s\n%s\n%s\n" % (ask_run, def_run, ASK, define_text(ask_run), bind_text(def_run)))
    print("live:"); define("who"); define("bread"); define("who")
