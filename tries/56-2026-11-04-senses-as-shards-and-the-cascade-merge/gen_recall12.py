# gen_recall12.py (tries/56): RECALL-12 = the define run as the kernel holds it (RECALL-11, read back symbol by symbol) plus two spans for C21:
# the sense cell 187 (the point's WordNet and Wiktionary sense rows as a run list) and the sense shards: every occurrence of the point inside a
# sense row between two word symbols gives a context pair (before, after); a dna shard keyed by that pair with no call, and a sense table row
# (gate, shard, run) naming the sense row. The owner, 11-03 20:10: "each of those uses likely points to a different dna shard of that neuron".
import json, sys, urllib.request
door, out, base_run = sys.argv[1], sys.argv[2], int(sys.argv[3])
def post(path, body):
    r = urllib.request.Request(door + path, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r, timeout=300))
def q(sql): return post('/api/q', {'sql': sql, 'params': []})['rows']
base = q("SELECT group_concat(symbol, '') FROM (SELECT l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = %d ORDER BY s.pos)" % base_run)[0][0].strip()
assert base.startswith('BUILD') and base.endswith('BUILD') and base.count('BUILD') == 18, base.count('BUILD')
SR = "SELECT n.run AS r FROM node n WHERE n.gate = what AND n.source IN ( 7 , 443 ) AND ( SELECT gate FROM seq WHERE run = n.run ORDER BY pos LIMIT 1 ) <> 143"
S_SENSE = "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 187 , 1 , coalesce ( ( SELECT group_concat ( r , ' ' ) FROM ( " + SR + " ORDER BY n.run ) ) , '' ) ;"
OC = ("WITH sr AS MATERIALIZED ( " + SR + " ) , oc AS MATERIALIZED ( SELECT sr.r , s.pos , "
      "( SELECT t.gate FROM seq t WHERE t.run = sr.r AND t.pos < s.pos AND t.gate <> 3 ORDER BY t.pos DESC LIMIT 1 ) AS bf , "
      "( SELECT t.gate FROM seq t WHERE t.run = sr.r AND t.pos > s.pos AND t.gate <> 3 ORDER BY t.pos LIMIT 1 ) AS nx "
      "FROM sr JOIN seq s ON s.run = sr.r AND s.gate = what ) , "
      "ok2 AS MATERIALIZED ( SELECT oc.r , oc.bf , oc.nx FROM oc JOIN label lb ON lb.gate = oc.bf JOIN label ln ON ln.gate = oc.nx WHERE lb.symbol GLOB '[A-Za-z]*' AND ln.symbol GLOB '[A-Za-z]*' ) ")
S_SHARDS = ("CREATE TABLE IF NOT EXISTS sense_shard ( gate INTEGER , shard INTEGER , run INTEGER , PRIMARY KEY ( gate , shard , run ) ) ; "
            + OC + "INSERT INTO dna ( gate , shard , before , trigger , call , spawn , times ) SELECT DISTINCT what , NULL , ok2.bf , ok2.nx , NULL , NULL , 0 FROM ok2 WHERE NOT EXISTS ( SELECT 1 FROM dna d WHERE d.gate = what AND d.before = ok2.bf AND d.trigger = ok2.nx ) ; "
            + OC + "INSERT OR IGNORE INTO sense_shard ( gate , shard , run ) SELECT what , d.shard , ok2.r FROM ok2 JOIN dna d ON d.gate = what AND d.before = ok2.bf AND d.trigger = ok2.nx ;")
for s in (S_SENSE, S_SHARDS):
    bad = [t for t in s.split(' ') if t.lower() in {'me', 'newgate', 'reply', 'def', 'say', 'know', 'remember', 'shape', 'ok', 'known', 'unknown', 'class', 'like', 'opposite', 'similar', 'tense', 'prefix', 'suffix', 'etymology', 'guess', 'sense', 'how', 'action', 'against'}]; assert not bad, bad
line = base + ' BUILD ' + S_SENSE + ' BUILD BUILD ' + S_SHARDS + ' BUILD'
hdr = open('recall12_header.txt').read()
open(out, 'w', encoding='utf-8').write(hdr + line + "\n# 2. define's (heard, :) row calls it.\nBUILD UPDATE dna SET call = {run:1} WHERE gate = 156 AND before = 1 AND trigger = 68 ; BUILD\n# 3. define's (the sixth, :) row calls it.\nBUILD UPDATE dna SET call = {run:1} WHERE gate = 156 AND before = 5 AND trigger = 68 ; BUILD\n")
print('RECALL-12 line 1: %d chars, %d BUILD symbols; base run %d' % (len(line), line.count('BUILD'), base_run))
