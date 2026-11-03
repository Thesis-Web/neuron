#!/usr/bin/env python3
# g36/hub_meaning.py (2026-11-02): the meaning question and the correct / incorrect answers on the hub (8056), MEANING-nk.txt in the hub's
# dialect (a point's rows are its own table main."G", read and written through mother; the hub's gates), typed through the hub's prompt.
#   python3 hub_meaning.py lay            type the lines (the run numbers filled as they come back), write HUB-MEANING-v7.txt
#   python3 hub_meaning.py ask LINE...    type questions or answers and print each line's sheet (how, guess, action, against, belief)
#   python3 hub_meaning.py state          belief, tried, the keys' rows
import json, urllib.request, time, sys, os
sys.path.insert(0, "/mnt/d/Neuron/tries/35-2026-11-02-relationship-formulas-and-xyz"); import hub_g35 as H
T = "/mnt/d/Neuron/tries/36-2026-11-02-meaning-of-actions-by-trial"
# the hub's gates: cells how 300, guess 15, action 405, against 677, belief 235; the words memory 241, relationship 8421, definition 969, none 1415;
# keys meaning 265, correct 233, incorrect 237; ':' 68, heard 1, the sixth 5; the sources 7..15 and wikt 3369
HOW, GUESS, ACTION, AGAINST, BELIEF = 300, 15, 405, 677, 235
MEMORY, RELATIONSHIP, DEFINITION, NONE = 241, 8421, 969, 1415
REL_Q = "( SELECT other AS c , kind FROM rel WHERE gate = what UNION ALL SELECT gate , kind FROM rel WHERE other = what ) q"
CAND = "q.c <> what AND q.c NOT IN ( SELECT other FROM tried WHERE gate = what AND outcome = 0 ) AND mother ( 'SELECT 1 FROM main.\"' || q.c || '\" WHERE call IS NOT NULL OR spawn IS NOT NULL LIMIT 1' ) = '1'"
POINT = "( CASE WHEN ( SELECT value FROM run_sheet WHERE run = above AND cell = %d ) = '%d' THEN ( SELECT value FROM run_sheet WHERE run = above AND cell = %d ) ELSE what END )" % (HOW, RELATIONSHIP, GUESS)
LINES = {
 "tables": "BUILD CREATE TABLE IF NOT EXISTS belief ( gate INTEGER , shard INTEGER , correct INTEGER , incorrect INTEGER , at INTEGER , run INTEGER , PRIMARY KEY ( gate , shard ) ) ; CREATE TABLE IF NOT EXISTS tried ( gate INTEGER , other INTEGER , outcome INTEGER , run INTEGER , at INTEGER , PRIMARY KEY ( gate , other ) ) ; BUILD",
 "answer": ("BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , %d , 1 , CASE WHEN mother ( 'SELECT 1 FROM main.\"' || what || '\" WHERE call IS NOT NULL OR spawn IS NOT NULL LIMIT 1' ) = '1' THEN %d WHEN EXISTS ( SELECT 1 FROM %s JOIN pull p ON p.kind = q.kind WHERE %s ) THEN %d WHEN mother ( 'SELECT 1 FROM main.\"' || what || '.node\" LIMIT 1' ) = '1' THEN %d ELSE %d END ; "
            "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , %d , 1 , ( SELECT q.c FROM %s JOIN pull p ON p.kind = q.kind JOIN formula f ON f.id = p.formula WHERE %s ORDER BY f.pull DESC , q.c LIMIT 1 ) WHERE ( SELECT value FROM run_sheet WHERE run = above AND cell = %d ) = '%d' ; "
            "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , %d , 1 , coalesce ( nullif ( mother ( 'SELECT group_concat ( coalesce ( ( SELECT symbol FROM main.label WHERE gate = d.before ) , ''none'' ) || '' '' || coalesce ( ( SELECT symbol FROM main.label WHERE gate = d.trigger ) , ''end'' ) || '' '' || coalesce ( d.call , d.spawn ) , '' ; '' ) FROM main.\"' || %s || '\" d WHERE d.call IS NOT NULL OR d.spawn IS NOT NULL' ) , 'ok' ) , 'none' ) ; "
            "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , %d , 1 , coalesce ( ( SELECT group_concat ( DISTINCT l.symbol ) FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run IN ( SELECT value FROM json_each ( '[' || mother ( 'SELECT group_concat ( coalesce ( call , spawn ) ) FROM main.\"' || %s || '\" WHERE call IS NOT NULL OR spawn IS NOT NULL' ) || ']' ) ) AND ( l.symbol IN ( SELECT name FROM main.sqlite_master WHERE type = 'table' AND name NOT GLOB '[0-9]*' ) OR s.gate IN ( 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 3369 ) ) ) , 'none' ) WHERE ( SELECT value FROM run_sheet WHERE run = above AND cell = %d ) IN ( '%d' , '%d' ) ; "
            "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , %d , 1 , 'none' WHERE ( SELECT value FROM run_sheet WHERE run = above AND cell = %d ) NOT IN ( '%d' , '%d' ) ; "
            "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , %d , 1 , coalesce ( ( SELECT sum ( correct ) - sum ( incorrect ) FROM belief WHERE gate = what ) , 0 ) ; BUILD BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 25 , 1 , reply ) ; BUILD"
            % (HOW, MEMORY, REL_Q, CAND, RELATIONSHIP, DEFINITION, NONE, GUESS, REL_Q, CAND, HOW, RELATIONSHIP, ACTION, POINT, AGAINST, POINT, HOW, MEMORY, RELATIONSHIP, AGAINST, HOW, MEMORY, RELATIONSHIP, BELIEF)),
 "question": "BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , ( SELECT gate FROM seq WHERE run = above AND pos = ( SELECT min ( pos ) FROM seq WHERE run = above AND gate = 68 ) + 2 ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 25 , 0 , NULL ) ; INSERT INTO replay ( parent , source , kind ) VALUES ( above , {answer} , 1 ) ; BUILD",
 "bind_meaning": "BUILD INSERT INTO main.\"265\" ( shard , before , trigger , call , spawn , times ) SELECT n + 1 , 1 , 68 , {question} , NULL , 0 FROM shards WHERE NOT EXISTS ( SELECT 1 FROM main.\"265\" WHERE before IS 1 AND trigger IS 68 ) ; UPDATE shards SET n = n + 1 WHERE ( SELECT max ( shard ) FROM main.\"265\" ) = n + 1 ; UPDATE main.\"265\" SET call = {question} WHERE before IS 1 AND trigger IS 68 ; BUILD",
 "correct": ("BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , CAST ( ( SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = above AND s.pos > ( SELECT min ( pos ) FROM seq WHERE run = above AND gate = 68 ) + 1 ORDER BY s.pos ) ) AS INTEGER ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 25 , 0 , NULL ) ; BUILD "
             "BUILD SELECT mother ( 'INSERT INTO main.\"' || x.g || '\" ( shard , before , trigger , call , spawn , times ) SELECT ( SELECT n FROM main.shards ) + row_number ( ) OVER ( ORDER BY shard ) , before , trigger , call , spawn , 0 FROM main.\"' || y.c || '\" WHERE call IS NOT NULL OR spawn IS NOT NULL ; UPDATE main.shards SET n = n + ( SELECT count ( * ) FROM main.\"' || y.c || '\" WHERE call IS NOT NULL OR spawn IS NOT NULL )' ) FROM ( SELECT value AS g FROM run_sheet WHERE run = what AND cell = 23 ) x JOIN ( SELECT value AS c FROM run_sheet WHERE run = what AND cell = %d ) y WHERE ( SELECT value FROM run_sheet WHERE run = what AND cell = %d ) = '%d' ; "
             "INSERT OR REPLACE INTO tried ( gate , other , outcome , run , at ) SELECT CAST ( x.g AS INTEGER ) , CAST ( y.c AS INTEGER ) , 1 , what , ( SELECT n FROM clock ) FROM ( SELECT value AS g FROM run_sheet WHERE run = what AND cell = 23 ) x JOIN ( SELECT value AS c FROM run_sheet WHERE run = what AND cell = %d ) y WHERE ( SELECT value FROM run_sheet WHERE run = what AND cell = %d ) = '%d' ; "
             "INSERT OR REPLACE INTO belief ( gate , shard , correct , incorrect , at , run ) SELECT CAST ( x.g AS INTEGER ) , d.value , coalesce ( b.correct , 0 ) + 1 , coalesce ( b.incorrect , 0 ) , ( SELECT n FROM clock ) , what FROM ( SELECT value AS g FROM run_sheet WHERE run = what AND cell = 23 ) x JOIN json_each ( '[' || mother ( 'SELECT group_concat ( shard ) FROM main.\"' || x.g || '\" WHERE call IS NOT NULL OR spawn IS NOT NULL' ) || ']' ) d LEFT JOIN belief b ON b.gate = CAST ( x.g AS INTEGER ) AND b.shard = d.value WHERE ( SELECT value FROM run_sheet WHERE run = what AND cell = %d ) IN ( '%d' , '%d' ) ; "
             "UPDATE guess.guesses SET correct = correct + 1 , solved = solved + 1 , belief = min ( 1.0 , belief + 0.25 ) WHERE asked_by = what ; BUILD BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 25 , 1 , reply ) ; BUILD"
             % (GUESS, HOW, RELATIONSHIP, GUESS, HOW, RELATIONSHIP, HOW, MEMORY, RELATIONSHIP)),
 "incorrect": ("BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , CAST ( ( SELECT group_concat ( symbol , '' ) FROM ( SELECT l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = above AND s.pos > ( SELECT min ( pos ) FROM seq WHERE run = above AND gate = 68 ) + 1 ORDER BY s.pos ) ) AS INTEGER ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 25 , 0 , NULL ) ; BUILD "
               "BUILD INSERT OR REPLACE INTO belief ( gate , shard , correct , incorrect , at , run ) SELECT CAST ( x.g AS INTEGER ) , d.value , coalesce ( b.correct , 0 ) , coalesce ( b.incorrect , 0 ) + 1 , ( SELECT n FROM clock ) , what FROM ( SELECT value AS g FROM run_sheet WHERE run = what AND cell = 23 ) x JOIN json_each ( '[' || mother ( 'SELECT group_concat ( shard ) FROM main.\"' || x.g || '\" WHERE call IS NOT NULL OR spawn IS NOT NULL' ) || ']' ) d LEFT JOIN belief b ON b.gate = CAST ( x.g AS INTEGER ) AND b.shard = d.value WHERE ( SELECT value FROM run_sheet WHERE run = what AND cell = %d ) = '%d' ; "
               "INSERT OR REPLACE INTO tried ( gate , other , outcome , run , at ) SELECT CAST ( x.g AS INTEGER ) , CAST ( y.c AS INTEGER ) , 0 , what , ( SELECT n FROM clock ) FROM ( SELECT value AS g FROM run_sheet WHERE run = what AND cell = 23 ) x JOIN ( SELECT value AS c FROM run_sheet WHERE run = what AND cell = %d ) y WHERE ( SELECT value FROM run_sheet WHERE run = what AND cell = %d ) = '%d' ; "
               "UPDATE guess.guesses SET incorrect = incorrect + 1 , belief = max ( 0.0 , belief - 0.25 ) WHERE asked_by = what ; BUILD "
               "BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , CAST ( value AS INTEGER ) FROM run_sheet WHERE run = what AND cell = 23 ; INSERT INTO replay ( parent , source , kind ) VALUES ( above , {answer} , 2 ) ; BUILD"
               % (HOW, MEMORY, GUESS, HOW, RELATIONSHIP)),
 "bind_correct": "BUILD UPDATE main.\"233\" SET call = {correct} WHERE before IS 1 AND trigger IS 68 ; BUILD",
 "bind_incorrect": "BUILD UPDATE main.\"237\" SET call = {incorrect} WHERE before IS 1 AND trigger IS 68 ; BUILD",
}
ORDER = ["tables", "answer", "question", "bind_meaning", "correct", "incorrect", "bind_correct", "bind_incorrect"]
def sheet(run):
    rows = H.q("SELECT cell, state, value FROM run_sheet WHERE run = ? ORDER BY cell", [run]); names = {HOW: "how", GUESS: "guess", ACTION: "action", AGAINST: "against", BELIEF: "belief", 23: "what", 25: "say"}
    for c, st, v in rows or []:
        n = names.get(c)
        if not n: continue
        if n in ("how", "guess") and v and str(v).isdigit(): s = H.q("SELECT symbol FROM label WHERE gate = ?", [int(v)]); v = "%s (%s)" % (s[0][0] if s else "?", v)
        if n == "say" and v and str(v).isdigit():
            t = H.q("SELECT substr(value, 1, 160) FROM run_sheet WHERE run = ? AND cell = 22", [int(v)]); v = "%s -> %s" % (v, (t[0][0] if t else "")[:120])
        print("   %-8s state %s: %s" % (n, st, str(v)[:260]))
def main():
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what == "lay":
        runs = {}; out = ["# HUB-MEANING-v7.txt (2026-11-02): MEANING-nk.txt in the hub's dialect, typed by hub_meaning.py lay. The runs: " ]
        for k in ORDER:
            line = LINES[k]
            for name, r in runs.items(): line = line.replace("{%s}" % name, str(r))
            print("--", k); run, rep = H.typed(line); runs[k] = run; out.append("# %s: run %s, reply %s\n%s" % (k, run, (rep[-1][:80] if rep else None), line))
        out[0] += ", ".join("%s %s" % (k, v) for k, v in runs.items())
        open(T + "/HUB-MEANING-v7.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
        print("rows:", H.q('SELECT shard, before, trigger, call FROM main."265"'), H.q('SELECT shard, before, trigger, call FROM main."233"'), H.q('SELECT shard, before, trigger, call FROM main."237"'))
    elif what == "ask":
        for line in sys.argv[2:]:
            t0 = time.time(); run, rep = H.typed(line, quiet=True); print("== %-22s run %s  %.1f s" % (line, run, time.time() - t0)); sheet(run)
    elif what == "state":
        print("belief:", H.q("SELECT l.symbol, count(*), sum(b.correct), sum(b.incorrect) FROM belief b JOIN label l ON l.gate = b.gate GROUP BY b.gate"))
        print("tried:", H.q("SELECT l.symbol, m.symbol, t.outcome, t.run FROM tried t JOIN label l ON l.gate = t.gate JOIN label m ON m.gate = t.other"))
        for w in sys.argv[2:]:
            g = H.q("SELECT gate FROM label WHERE symbol = ?", [w]); g = g[0][0] if g else None
            print(w, g, H.q('SELECT shard, before, trigger, call, spawn, times FROM main."%d"' % g) if g else None)
    else: print(__doc__)
if __name__ == "__main__": main()
