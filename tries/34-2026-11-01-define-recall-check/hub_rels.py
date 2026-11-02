#!/usr/bin/env python3
# g34/hub_rels.py (2026-11-02, 03:25). The relationships from the definitions on the hub (8056), in its shapes, typed through its prompt:
#  1. relmap (marker, kind): the brain's own table of WordNet's and Wiktionary's markers and the catalog word each names (as on hp).
#  2. The define run again (the hub's run 498941 shape with the ask of HUB-RECALL): its second span lays, besides the thesaurus like/opposite
#     rows, the marker rows of this run's returns: each bracket of a return one row (its kind through relmap, its colon, its closing bracket),
#     each single-symbol target a rel row (about, kind, target, return). Hub gates: '[' 140, ']' 144, '{' 169, '}' 173, ':' 68, ';' 45, ',' 38,
#     the space 3, wn 7, wikt 3369.
#  3. define's row calls it.
# The 157 thousand points already defined on the hub are not back-populated here: the SQL form costs seconds a point (measured on hp).
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
    r = j.get("result") or {}; print("  typed -> run %s, %.1f s, reply %s" % (r.get("run"), time.time() - t0, [str(o[3])[:120] for o in (r.get("out") or []) if o[2] == "reply"]), flush=True); return r.get("run")
MAP = [('syn', 'like'), ('synonyms', 'like'), ('ant', 'opposite'), ('antonym', 'opposite'), ('antonyms', 'opposite'),
       ('hypernym', 'is'), ('instance hypernym', 'is'), ('hypernyms', 'is'),
       ('hyponym', 'includes'), ('instance hyponym', 'includes'), ('hyponyms', 'includes'), ('troponyms', 'includes'),
       ('part holonym', 'part'), ('substance holonym', 'part'), ('holonyms', 'part'),
       ('part meronym', 'has'), ('member meronym', 'has'), ('substance meronym', 'has'), ('meronyms', 'has'),
       ('member holonym', 'member'),
       ('similar to', 'similar'), ('also see', 'similar'), ('verb group', 'similar'), ('coordinate terms', 'similar'),
       ('derivationally related form', 'derived'), ('derived', 'derived'), ('pertainym', 'derived'),
       ('related', 'related'), ('entailment', 'implies'), ('cause', 'causes'), ('attribute', 'property'),
       ('domain category', 'topic'), ('topics', 'topic'), ('member of domain category', 'topic'),
       ('domain region', 'context'), ('member of domain region', 'context'), ('domain usage', 'use'), ('member of domain usage', 'use'),
       ('participle of', 'past'), ('alternative forms', 'alias')]
RELMAP = "BUILD CREATE TABLE IF NOT EXISTS relmap ( marker TEXT PRIMARY KEY , kind TEXT ) ; INSERT OR REPLACE INTO relmap ( marker , kind ) VALUES " + " , ".join("( '%s' , '%s' )" % m for m in MAP) + " ; BUILD"
LB, RB, LC, RC, COLON, SEMI, COMMA, SPACE = 140, 144, 169, 173, 68, 45, 38, 3
MARKERS = ("WITH br AS MATERIALIZED ( SELECT r.id AS run , r.about AS about , b.pos AS p0 , ( SELECT min ( pos ) FROM seq WHERE run = r.id AND pos > b.pos AND gate IN ( %d , %d ) ) AS pc , ( SELECT min ( pos ) FROM seq WHERE run = r.id AND pos > b.pos AND gate = %d ) AS pe FROM run r JOIN seq b ON b.run = r.id AND b.gate = %d WHERE r.parent = above AND r.kind = 3 AND r.arrival IN ( 7 , %d ) ) , "
           "kb AS MATERIALIZED ( SELECT br.run , br.about , br.pc , br.pe , k.gate AS kind FROM br JOIN relmap m ON m.marker = ( SELECT group_concat ( l3.symbol , ' ' ) FROM ( SELECT l2.symbol FROM seq s2 JOIN label l2 ON l2.gate = s2.gate WHERE s2.run = br.run AND s2.pos > br.p0 AND s2.pos < br.pc AND s2.gate <> %d ORDER BY s2.pos ) l3 ) JOIN label k ON k.symbol = m.kind WHERE br.pe IS NOT NULL AND ( SELECT gate FROM seq WHERE run = br.run AND pos = br.pc ) = %d ) "
           "INSERT OR IGNORE INTO rel ( gate , kind , other , run ) SELECT kb.about , kb.kind , t.gate , kb.run FROM kb JOIN seq t ON t.run = kb.run AND t.pos > kb.pc AND t.pos < kb.pe JOIN label lt ON lt.gate = t.gate WHERE lt.symbol GLOB '[A-Za-z]*' AND t.gate <> kb.about "
           "AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos - 1 ) , %d ) , ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos - 2 ) ) IN ( %d , %d , %d , %d ) "
           "AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos + 1 ) , %d ) , ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos + 2 ) ) IN ( %d , %d , %d , %d )"
           % (COLON, RB, RB, LB, WIKT, SPACE, COLON, SPACE, LC, COLON, SEMI, COMMA, SPACE, RC, SEMI, RB, COMMA))
def define_text(ask_run):
    import importlib.util
    spec = importlib.util.spec_from_file_location('hr', '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34/hub_recall.py'); hr = importlib.util.module_from_spec(spec); spec.loader.exec_module(hr)
    t = hr.define_text(ask_run); marker = "y.symbol IN ( ';' , 'like' , 'opposite' ) ) ; BUILD "
    assert t.count(marker) == 1; return t.replace(marker, "y.symbol IN ( ';' , 'like' , 'opposite' ) ) ; " + MARKERS + " ; BUILD ")
if __name__ == "__main__":
    ask_run = int(sys.argv[1])
    print("1. relmap:"); typed(RELMAP); print("   rows:", q("SELECT count(*) FROM relmap"))
    print("2. the define run with the markers:"); def_run = typed(define_text(ask_run))
    print("3. the binding:"); typed('BUILD UPDATE main."153" SET call = %d WHERE before IS 1 AND trigger IS 68 ; BUILD' % def_run)
    print("define row:", q('SELECT shard, before, trigger, call FROM main."153"'))
    open('/mnt/d/Neuron/tries/34-2026-11-01-define-recall-check/HUB-RELS-v7.txt', 'w').write("# HUB-RELS-v7.txt (2026-11-02): the relationship markers in the hub's define, typed by hub_rels.py; the define run %s.\n%s\n%s\nBUILD UPDATE main.\"153\" SET call = %s WHERE before IS 1 AND trigger IS 68 ; BUILD\n" % (def_run, RELMAP, define_text(ask_run), def_run))
