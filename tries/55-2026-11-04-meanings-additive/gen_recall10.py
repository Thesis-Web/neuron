# gen_recall10.py (tries/55): RECALL-10 = the live define run's text (read back symbol by symbol from the kernel) plus the formula span F and the
# guess cell: a newly defined point that has no action of its own, is related by a mutual one-word thesaurus like row to an acting root (a point
# whose action was not itself borrowed), and whose definition rows hold that root's word, takes the root's shards as a guess (belief 0/0,
# tried outcome 2 = by formula, unjudged), and the line's sheet shows guess 15 = the root. The owner, 11-04 05:00: "if you find a formula that
# works, back pop it and let the sixth work it into the cascade".
import json, sys, urllib.request
door, out = sys.argv[1], sys.argv[2]
def post(path, body):
    r = urllib.request.Request(door + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r, timeout=300))
def q(sql): return post('/api/q', {'sql': sql, 'params': []})['rows']
define_run = int(sys.argv[3]) if len(sys.argv) > 3 else q("SELECT call FROM dna WHERE gate = 156 AND before = 1 AND trigger = 68")[0][0]
base = q("SELECT group_concat(symbol, '') FROM (SELECT l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = %d ORDER BY s.pos)" % define_run)[0][0].strip()
assert base.startswith('BUILD') and base.endswith('BUILD') and base.count('BUILD') == 16, base.count('BUILD')
# the root k for the point: mutual one-word like/similar rows to an acting point that is not itself a borrower, whose word is in the point's definition rows
ROOT = ("( SELECT r.other FROM rel r JOIN rel m ON m.gate = r.other AND m.other = what AND m.kind IN ( 138 , 530 ) WHERE r.gate = what AND r.kind IN ( 138 , 530 ) AND r.other <> what "
        "AND ( SELECT count ( * ) FROM seq WHERE run = r.run ) = 3 AND ( SELECT count ( * ) FROM seq WHERE run = m.run ) = 3 "
        "AND EXISTS ( SELECT 1 FROM dna WHERE gate = r.other AND ( call IS NOT NULL OR spawn IS NOT NULL ) ) "
        "AND NOT EXISTS ( SELECT 1 FROM tried WHERE gate = r.other ) "
        "AND NOT EXISTS ( SELECT 1 FROM tried WHERE gate = what AND other = r.other AND outcome = 0 ) "
        "AND EXISTS ( SELECT 1 FROM node n JOIN seq s ON s.run = n.run AND s.gate = r.other WHERE n.gate = what AND n.source IN ( 7 , 443 ) AND s.pos < ( SELECT min ( pos ) FROM seq WHERE run = n.run ) + 14 AND ( SELECT gate FROM seq WHERE run = n.run ORDER BY pos LIMIT 1 ) <> 143 ) "
        "AND NOT EXISTS ( SELECT 1 FROM dna WHERE gate = what AND ( call IS NOT NULL OR spawn IS NOT NULL ) ) "
        "ORDER BY r.run LIMIT 1 )")
# 1 the root into the guess cell 15 of the line; 2 the root's shards laid on the point; 3 belief 0/0 (a guess); 4 tried outcome 2 (by the formula, unjudged)
S_F = ("INSERT INTO run_sheet ( run , cell , state , value ) SELECT above , 15 , 1 , g FROM ( SELECT " + ROOT + " AS g ) WHERE g IS NOT NULL ; "
       "INSERT INTO dna ( gate , shard , before , trigger , call , spawn , times ) SELECT what , NULL , d.before , d.trigger , d.call , d.spawn , 0 FROM dna d WHERE d.gate = ( SELECT CAST ( value AS INTEGER ) FROM run_sheet WHERE run = above AND cell = 15 ) AND ( d.call IS NOT NULL OR d.spawn IS NOT NULL ) AND EXISTS ( SELECT 1 FROM run_sheet WHERE run = above AND cell = 15 ) ; "
       "INSERT OR REPLACE INTO belief ( gate , shard , correct , incorrect , at , run ) SELECT what , d.shard , 0 , 0 , ( SELECT n FROM clock ) , above FROM dna d WHERE d.gate = what AND ( d.call IS NOT NULL OR d.spawn IS NOT NULL ) AND EXISTS ( SELECT 1 FROM run_sheet WHERE run = above AND cell = 15 ) AND NOT EXISTS ( SELECT 1 FROM belief WHERE gate = what AND shard = d.shard ) ; "
       "INSERT OR REPLACE INTO tried ( gate , other , outcome , run , at ) SELECT what , CAST ( value AS INTEGER ) , 2 , above , ( SELECT n FROM clock ) FROM run_sheet WHERE run = above AND cell = 15 ;")
line = base + ' BUILD ' + S_F + ' BUILD'
forbidden = {'me', 'newgate', 'reply', 'def', 'say', 'know', 'remember', 'shape', 'ok', 'known', 'unknown', 'class', 'like', 'opposite', 'similar', 'tense', 'prefix', 'suffix', 'etymology', 'guess', 'how', 'action', 'against'}
bad = [t for t in S_F.split(' ') if t.lower() in forbidden]; assert not bad, bad
hdr = open(sys.argv[4] if len(sys.argv) > 4 else 'recall10_header.txt').read()
open(out, 'w', encoding='utf-8').write(hdr + line + "\n# 2. define's (heard, :) row calls it.\nBUILD UPDATE dna SET call = {run:1} WHERE gate = 156 AND before = 1 AND trigger = 68 ; BUILD\n# 3. define's (the sixth, :) row calls it.\nBUILD UPDATE dna SET call = {run:1} WHERE gate = 156 AND before = 5 AND trigger = 68 ; BUILD\n")
print('RECALL-10 line 1: %d chars, %d BUILD symbols; base from run %d; the F span %d chars' % (len(line), line.count('BUILD'), define_run, len(S_F)))
