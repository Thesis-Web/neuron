# tries/59 derive_gen.py: the derivation run as one line file, DERIVE-nk.txt. It names no word. Bound to `derive : X`.
# H1a (after run 1, tries/59 CRITERIA.md): the operational meaning of X is the grounded points named in the gloss of its first
# WordNet verb sense (first by node id), in gloss order, the first as the shard's call and the second as its spawn; a grounded point is
# one whose shard the teacher confirmed (belief correct > 0, the brain's own record), and its run is that shard's call. The evidence is kept in the table derived. A sense shard
# (C21, keyed by an example's context) takes the composition of ITS sense's gloss, when it holds no call yet. No grounded word: unresolved.
SR = "( SELECT n.run FROM node n WHERE n.gate = what AND n.source = 7 AND ( SELECT gate FROM seq WHERE run = n.run ORDER BY pos LIMIT 1 ) = {gate:verb} ORDER BY n.id LIMIT 1 )"
def C(sr): return "( SELECT min ( pos ) FROM seq WHERE run = %s AND gate = 68 )" % sr
def E(sr): return "coalesce ( ( SELECT min ( pos ) FROM seq WHERE run = %s AND gate IN ( {gate:[} , {gate:\"} ) ) , 999999999 )" % sr
def chosen(g): return ("( SELECT d.call FROM belief b JOIN dna d ON d.gate = b.gate AND d.shard = b.shard WHERE b.gate = %s AND b.correct > 0 AND d.call IS NOT NULL ORDER BY b.correct DESC , b.shard LIMIT 1 )" % g)
def grounded(sr):   # the believed points of the gloss of sense run sr, in gloss order (ord, pos, gate); used only in the main evidence rows
    return ("( SELECT row_number ( ) OVER ( ORDER BY s.pos ) AS ord , s.pos AS pos , s.gate AS gate FROM seq s WHERE s.run = %s AND s.pos > %s AND s.pos < %s AND s.gate <> what "
            "AND EXISTS ( SELECT 1 FROM belief b WHERE b.gate = s.gate AND b.correct > 0 ) )" % (sr, C(sr), E(sr)))
def kth_gate(sr, k):   # the k-th believed point of the gloss, as a correlated scalar
    return ("( SELECT s.gate FROM seq s WHERE s.run = %s AND s.pos > %s AND s.pos < %s AND s.gate <> what AND EXISTS ( SELECT 1 FROM belief b WHERE b.gate = s.gate AND b.correct > 0 ) ORDER BY s.pos LIMIT 1 OFFSET %d )" % (sr, C(sr), E(sr), k - 1))
def nth(sr, k): return chosen(kth_gate(sr, k))
what_span = ("INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , ( SELECT gate FROM seq WHERE run = above AND pos = ( SELECT min ( pos ) FROM seq WHERE run = above AND gate = 68 ) + 2 ) ; "
             "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 25 , 0 , NULL )")
evidence = ("INSERT INTO derived ( gate , shard , sense_run , ord , word , word_gate , run_used , at_clock , run ) SELECT what , NULL , %s , g.ord , ( SELECT symbol FROM label WHERE gate = g.gate ) , g.gate , %s , ( SELECT n FROM clock ) , me FROM %s g" % (SR, chosen("g.gate"), grounded(SR)))
unresolved = ("INSERT INTO derived ( gate , shard , sense_run , ord , word , word_gate , run_used , at_clock , run ) SELECT what , NULL , %s , 0 , 'unresolved' , NULL , NULL , ( SELECT n FROM clock ) , me "
              "WHERE NOT EXISTS ( SELECT 1 FROM %s g )" % (SR, grounded(SR)))
shard = ("INSERT INTO dna ( gate , shard , before , trigger , call , spawn , times ) SELECT what , NULL , 1 , 68 , %s , %s , 0 WHERE %s IS NOT NULL" % (nth(SR, 1), nth(SR, 2), nth(SR, 1)))
# a keyed dna read by (gate, before, trigger) lays the shard when absent (the kernel bridge, seen 11-04 20:2x on abdicate): read by gate only
belief = ("INSERT OR IGNORE INTO belief ( gate , shard , correct , incorrect , at , run ) SELECT what , ( SELECT shard FROM dna WHERE gate = what AND before + 0 = 1 AND trigger + 0 = 68 ) , 0 , 0 , ( SELECT n FROM clock ) , me "
          "WHERE ( SELECT call FROM dna WHERE gate = what AND before + 0 = 1 AND trigger + 0 = 68 ) IS NOT NULL")
# the sense shards of X (C21): each takes its own sense's composition, when it holds no call
SSR = "( SELECT run FROM sense_shard ss WHERE ss.gate = dna.gate AND ss.shard = dna.shard ORDER BY run LIMIT 1 )"
sense_up = ("UPDATE dna SET call = %s , spawn = %s WHERE gate = what AND call IS NULL AND spawn IS NULL AND shard IN ( SELECT shard FROM sense_shard WHERE gate = what )" % (nth(SSR, 1), nth(SSR, 2)))
sense_ev = " ; ".join("INSERT INTO derived ( gate , shard , sense_run , ord , word , word_gate , run_used , at_clock , run ) SELECT what , ss.shard , ss.run , %d , ( SELECT symbol FROM label WHERE gate = %s ) , %s , %s , ( SELECT n FROM clock ) , me FROM sense_shard ss WHERE ss.gate = what AND %s IS NOT NULL" % (k, kth_gate("ss.run", k), kth_gate("ss.run", k), nth("ss.run", k), kth_gate("ss.run", k)) for k in (1, 2))
say = "SELECT ord , shard , word , run_used , sense_run FROM derived WHERE gate = what AND run = me ORDER BY shard , ord"
lines = ["# DERIVE-nk.txt (tries/59, 2026-11-04, H1a): the derivation run. The believed points of the first WordNet verb gloss, in order, as call and spawn.",
         "# 1. the evidence table",
         "BUILD CREATE TABLE IF NOT EXISTS derived ( id INTEGER PRIMARY KEY , gate INTEGER , shard INTEGER , sense_run INTEGER , ord INTEGER , word TEXT , word_gate INTEGER , run_used INTEGER , at_clock INTEGER , run INTEGER ) ; BUILD",
         "# 2. the derivation run: what; the evidence rows (or unresolved); the (heard, :) shard with call and spawn; the belief as a guess; the sense shards by their own glosses; the say",
         "BUILD " + what_span + " ; BUILD BUILD " + evidence + " ; " + unresolved + " ; " + shard + " ; " + belief + " ; " + sense_ev + " ; " + sense_up + " ; BUILD BUILD " + say + " ; BUILD BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 25 , 1 , reply ) ; BUILD",
         "# 3. derive's row at (heard, :) calls it",
         "BUILD INSERT INTO dna ( gate , shard , before , trigger , call , spawn , times ) VALUES ( {gate:derive} , NULL , 1 , 68 , {run:2} , NULL , 0 ) ; UPDATE dna SET call = {run:2} WHERE gate = {gate:derive} AND before = 1 AND trigger = 68 ; BUILD"]
open('DERIVE-nk.txt', 'w').write('\n'.join(lines) + '\n'); print('DERIVE-nk.txt:', sum(len(l) for l in lines if l.startswith('BUILD')), 'bytes')
