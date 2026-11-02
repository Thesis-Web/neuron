#!/usr/bin/env python3
# g35/hub_g35.py (2026-11-02): the relationship formulas, the places, the sixth's define row and the build step at birth on the hub (8056),
# every change typed through its own prompt (the lesson of 11-01: an outside connection's DDL killed its router).
#   python3 hub_g35.py formula   the formula and pull tables (FORMULA-nk.txt's first two lines, the same text on both brains)
#   python3 hub_g35.py xyz       the xyz tables, the key on rel.other, the xyz_go trigger (HUB-XYZ-v7.txt)
#   python3 hub_g35.py rebind    the sixth's define row calls the recall define 4254380
#   python3 hub_g35.py born      the define-at-birth run, the born run that lays the define row and spawns it, born's row bound, secondary_go lays the define row too
#   python3 hub_g35.py rels      the catalog relationships back-populated for the already-defined points, 500 a line, until none is left (HUB-RELS-BACKPOP)
#   python3 hub_g35.py settle N  N passes of the places over every point that holds relationship rows, 3000 points a line
import json, urllib.request, time, sys, os
B = "http://localhost:8056"; T = "/mnt/d/Neuron/tries/35-2026-11-02-relationship-formulas-and-xyz"
def post(path, obj, timeout=3500):
    rq = urllib.request.Request(B + path, data=json.dumps(obj).encode(), headers={"Content-Type": "application/json"}); return json.load(urllib.request.urlopen(rq, timeout=timeout))
def get(path, timeout=120): return json.load(urllib.request.urlopen(B + path, timeout=timeout))
def q(sql, params=[]):
    try: return post("/api/q", {"sql": sql, "params": params}, 900).get("rows")
    except Exception as e: return "ERR %s" % str(e)[:120]
def typed(line, quiet=False):
    t0 = time.time(); j = post("/api/type", {"line": line, "prompt": "main"}); jid = j.get("id")
    while jid and not j.get("done") and time.time() - t0 < 3400: time.sleep(1); j = get("/api/job?id=%s" % jid)
    r = j.get("result") or {}; rep = [str(o[3])[:160] for o in (r.get("out") or []) if o[2] == "reply"]
    if not quiet: print("  typed -> run %s, %.1f s, reply %s" % (r.get("run"), time.time() - t0, rep), flush=True)
    return r.get("run"), rep
def lines_of(path):
    return [l.strip() for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]
def define_text(ask_run):
    r = q("SELECT group_concat(l.symbol, '') FROM (SELECT s.gate FROM seq s WHERE s.run = ? ORDER BY s.pos) s JOIN label l ON l.gate = s.gate", [4254380])
    t = r[0][0]; old = "SELECT above , 23 , 1 , ( SELECT gate FROM seq WHERE run = above AND pos = ( SELECT min ( pos ) FROM seq WHERE run = above AND gate = 68 ) + 2 ) ; INSERT INTO replay ( parent , source , kind ) VALUES ( above , 4254360 , 1 ) ;"
    assert t.count(old) == 1, t[:300]
    return t.replace(old, "VALUES ( above , 23 , 1 , what ) ; INSERT INTO replay ( parent , source , kind ) VALUES ( above , %d , 1 ) ;" % ask_run)
SEC_OLD = "SELECT mother('INSERT INTO main.\"' || about || '.node\" (source, run) VALUES (?, ?)', arrival, id) FROM run WHERE id = (SELECT max(id) FROM run) AND about IS NOT NULL AND EXISTS (SELECT 1 FROM seq WHERE run = (SELECT max(id) FROM run) AND pos = 1);"
def main():
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what == "formula":
        for l in lines_of(T + "/FORMULA-nk.txt")[:2]: typed(l)
        print("formula", q("SELECT count(*) FROM formula"), "pull", q("SELECT count(*) FROM pull"))
        print(q("SELECT l.symbol, p.formula, f.pull, f.rest, f.mode FROM pull p JOIN formula f ON f.id = p.formula JOIN label l ON l.gate = p.kind ORDER BY p.formula"))
    elif what == "xyz":
        for l in lines_of(T + "/HUB-XYZ-v7.txt"): typed(l)
        print("xyz", q("SELECT * FROM xyz"), "trigger", q("SELECT name FROM sqlite_master WHERE type = 'trigger' AND name = 'xyz_go'"), "index", q("SELECT name FROM sqlite_master WHERE type = 'index' AND tbl_name = 'rel'"))
    elif what == "rebind":
        typed('BUILD UPDATE main."153" SET call = 4254380 WHERE before IS 5 AND trigger IS 68 ; BUILD')
        print(q('SELECT shard, before, trigger, call, times FROM main."153"'))
    elif what == "born":
        print("1. the define-at-birth run (the hub's define 4254380 with the point from the sheet):"); r1, _ = typed(define_text(4254360))
        born = 'BUILD CREATE TABLE "newgate" ( shard INTEGER PRIMARY KEY , before INTEGER , trigger INTEGER , call INTEGER , spawn INTEGER , times INTEGER ) ; CREATE TABLE "newgate.node" ( id INTEGER PRIMARY KEY , source INTEGER , run INTEGER ) ; INSERT INTO "newgate" ( shard , before , trigger , call , spawn , times ) VALUES ( ( SELECT n + 1 FROM shards ) , 153 , 68 , NULL , %d , 0 ) ; UPDATE shards SET n = n + 1 ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( me , 23 , 1 , newgate ) ; INSERT INTO replay ( parent , source , kind ) VALUES ( me , %d , 2 ) ; BUILD' % (r1, r1)
        print("2. the born run (the two tables, the define row, what = newgate, the spawn):"); r2, _ = typed(born)
        print("3. born's row calls it:"); typed('BUILD UPDATE main."16" SET call = %d WHERE shard = 6 ; BUILD' % r2)
        print("   born rows:", q('SELECT shard, before, trigger, call, spawn, times FROM main."16"'))
        sec = q("SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = 'secondary_go'")[0][0]
        assert sec.count(SEC_OLD) == 1, sec[-400:]
        add = "SELECT mother('INSERT INTO main.\"' || about || '\" (shard, before, trigger, call, spawn, times) SELECT (SELECT n + 1 FROM main.shards), 153, 68, NULL, %d, 0 WHERE NOT EXISTS (SELECT 1 FROM main.\"' || about || '\"); UPDATE main.shards SET n = n + 1 WHERE (SELECT max(shard) FROM main.\"' || about || '\") = n + 1') FROM run WHERE id = (SELECT max(id) FROM run) AND about IS NOT NULL AND EXISTS (SELECT 1 FROM seq WHERE run = (SELECT max(id) FROM run) AND pos = 1);" % r1
        new = sec.replace(SEC_OLD, SEC_OLD + "\n  " + add)
        open(T + "/hub-secondary_go-before-2026-11-02.sql", "w").write(sec + "\n"); open(T + "/hub-secondary_go-after-2026-11-02.sql", "w").write(new + "\n")
        print("4. secondary_go lays the define row for a point it births:"); typed("BUILD DROP TRIGGER secondary_go ; " + new + " ; BUILD")
        print("   trigger:", q("SELECT length(sql) FROM sqlite_master WHERE type = 'trigger' AND name = 'secondary_go'"))
        open(T + "/HUB-BORN-v7.txt", "w").write("# HUB-BORN-v7.txt (2026-11-02): the build step at birth on the hub, typed by hub_g35.py born. The owner (11-01): 'once a meaning point or gate is built, the dna table is built and populted with it's first row which is ALWAYS the define row ... this first define dna row spawns the defintion of that new gate.. immediately'. The define-at-birth run %s, the born run %s.\n%s\n%s\nBUILD UPDATE main.\"16\" SET call = %s WHERE shard = 6 ; BUILD\nBUILD DROP TRIGGER secondary_go ; %s ; BUILD\n" % (r1, r2, define_text(4254360), born, r2, new))
    elif what == "rels":
        typed("BUILD CREATE TABLE IF NOT EXISTS relsdone ( g INTEGER PRIMARY KEY ) ; CREATE TABLE IF NOT EXISTS relsbatch ( g INTEGER PRIMARY KEY ) ; BUILD")
        line = lines_of(T + "/HUB-RELS-BACKPOP-v7.txt")[0]; n = 0; t0 = time.time()
        while True:
            run, rep = typed(line, quiet=True); n += 1
            done = q("SELECT count(*) FROM relsdone"); batch = q("SELECT count(*) FROM relsbatch")
            print("  line %d run %s: done %s, this batch %s, reply %s, %.0f s" % (n, run, done, batch, rep[-1][:60] if rep else None, time.time() - t0), flush=True)
            if not batch or batch[0][0] == 0: break
            time.sleep(3)   # the chain gets the router between lines
        print(q("SELECT l.symbol, c FROM (SELECT kind, count(*) c FROM rel GROUP BY kind) r JOIN label l ON l.gate = r.kind ORDER BY c DESC"))
    elif what == "settle":
        passes = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        typed("BUILD CREATE TABLE IF NOT EXISTS xyzbatch ( g INTEGER PRIMARY KEY , done INTEGER ) ; CREATE TABLE IF NOT EXISTS xyzforce ( g INTEGER PRIMARY KEY , fx REAL , fy REAL , fz REAL , sc REAL ) ; DELETE FROM xyzbatch ; BUILD", quiet=True)
        place, step = lines_of(T + "/HUB-SETTLE-v7.txt")[:2]
        def loop(line, label):
            n = 0; t0 = time.time(); last = -1
            while True:
                run, rep = typed(line, quiet=True); n += 1; tot = q("SELECT count(*) FROM xyzbatch"); tot = tot[0][0] if isinstance(tot, list) and tot else -2
                if n % 10 == 0: print("  %s: line %d, %s points so far, %.0f s" % (label, n, tot, time.time() - t0), flush=True)
                if tot == last or tot < 0: break
                last = tot; time.sleep(1)
            print("  %s: %d lines, %s points, %.0f s" % (label, n, last, time.time() - t0), flush=True)
        if "steps" not in sys.argv: print("placing every point that holds relationship rows, 3000 a line:", flush=True); loop(place, "place")
        print("  placed:", q("SELECT count(*) FROM xyz"), flush=True)
        for p in range(passes):
            typed("BUILD DELETE FROM xyzbatch ; BUILD", quiet=True)
            print("pass %d of %d: one step of every placed point, 3000 a line:" % (p + 1, passes), flush=True); loop(step, "step")
            print("  sample:", q("SELECT l.symbol, round(x, 1), round(y, 1), round(z, 1), moved FROM xyz JOIN label l ON l.gate = xyz.gate WHERE l.symbol IN ('water', 'ice', 'stone', 'bread', 'origin', 'hinge')"), flush=True)
    else: print(__doc__)
if __name__ == "__main__": main()
