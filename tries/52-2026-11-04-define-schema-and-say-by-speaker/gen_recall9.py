# gen_recall9.py (tries/52): writes RECALL-9-nk.txt from the live text of the define run 19938199 plus the five spans of C26.
import sys
out = sys.argv[1]
base = open('define-run-19938199-live.txt', encoding='utf-8').read().strip()
assert base.startswith('BUILD') and base.endswith('BUILD')
L = lambda n: "( SELECT symbol FROM label WHERE gate = %d )" % n
W = lambda n: "coalesce ( ( SELECT group_concat ( l.symbol , ', ' ) FROM gs JOIN label l ON l.gate = gs.g WHERE gs.k = %d ) , '' )" % n
J = lambda n: "json ( ( SELECT json_group_array ( g ) FROM gs WHERE k = %d ) )" % n
ORD = "( SELECT group_concat ( g , ' ' ) FROM ( SELECT g FROM ( SELECT gate AS g , min ( rk ) AS a , min ( r ) AS b , min ( pos ) AS d FROM %s GROUP BY gate ) ORDER BY a , b , d ) )"
S4 = ("WITH pr AS MATERIALIZED ( SELECT n.run AS r , n.source AS u FROM node n WHERE n.gate = what UNION SELECT x.id , x.arrival FROM run x WHERE x.parent = above AND x.kind = 3 AND x.cell = 24 AND x.arrival IN ( 7 , 8 , 10 , 11 , 12 , 13 , 14 , 443 ) ) , "
      "mk AS MATERIALIZED ( SELECT pr.r , pr.u , b.pos AS p0 , ( SELECT min ( pos ) FROM seq WHERE run = pr.r AND pos > b.pos AND gate IN ( 68 , 147 ) ) AS pc , ( SELECT min ( pos ) FROM seq WHERE run = pr.r AND pos > b.pos AND gate = 147 ) AS pe FROM pr JOIN seq b ON b.run = pr.r AND b.gate = 143 WHERE ( SELECT gate FROM seq WHERE run = pr.r AND pos = b.pos + 1 ) IN ( 194 , 197 , 4675 , 290 , 204 ) ) , "
      "nm AS MATERIALIZED ( SELECT mk.r , mk.u , mk.p0 , mk.pc , mk.pe , ( SELECT group_concat ( l2.symbol , ' ' ) FROM ( SELECT l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = mk.r AND s.pos > mk.p0 AND s.pos < mk.pc AND s.gate <> 3 ORDER BY s.pos ) l2 ) AS name , CASE WHEN mk.pc = mk.p0 + 2 AND ( SELECT gate FROM seq WHERE run = mk.r AND pos = mk.p0 + 1 ) = 204 THEN 1 ELSE 0 END AS ety FROM mk WHERE mk.pc IS NOT NULL AND mk.pe IS NOT NULL AND ( SELECT gate FROM seq WHERE run = mk.r AND pos = mk.pc ) = 68 ) , "
      "tok AS MATERIALIZED ( SELECT nm.r , nm.name , nm.ety , nm.p0 , t.pos , t.gate , coalesce ( p.rank , 9 ) AS rk , ( SELECT gate FROM seq WHERE run = nm.r AND pos = t.pos - 2 ) AS v2 , ( SELECT gate FROM seq WHERE run = nm.r AND pos = t.pos - 1 ) AS v1 , ( SELECT gate FROM seq WHERE run = nm.r AND pos = t.pos + 1 ) AS x1 , ( SELECT gate FROM seq WHERE run = nm.r AND pos = t.pos + 2 ) AS x2 FROM nm JOIN seq t ON t.run = nm.r AND t.pos > nm.pc AND t.pos < nm.pe JOIN label lt ON lt.gate = t.gate LEFT JOIN ranks p ON p.cell = 24 AND p.source = nm.u WHERE lt.symbol GLOB '[A-Za-z]*' AND ( nm.ety = 1 OR nm.name IN ( 'part of speech' , 'forms' , 'conjugated form' , 'plural' ) ) ) "
      "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , c , 1 , coalesce ( v , '' ) FROM ( "
      "SELECT 441 AS c , " + ORD % "( SELECT tok.gate , tok.rk , tok.r , tok.pos FROM tok WHERE tok.name = 'part of speech' AND tok.p0 = ( SELECT min ( n2.p0 ) FROM nm n2 WHERE n2.r = tok.r AND n2.name = 'part of speech' ) UNION ALL SELECT f.g , coalesce ( p.rank , 9 ) , f.r , 0 FROM ( SELECT pr.r , pr.u , ( SELECT gate FROM seq WHERE run = pr.r ORDER BY pos LIMIT 1 ) AS g FROM pr WHERE pr.u IN ( 7 , 443 ) ) f JOIN label l ON l.gate = f.g LEFT JOIN ranks p ON p.cell = 24 AND p.source = f.u WHERE l.symbol GLOB '[A-Za-z]*' )" + " AS v "
      "UNION ALL SELECT 6332 , " + ORD % "tok WHERE tok.name IN ( 'forms' , 'conjugated form' , 'plural' ) AND NOT ( tok.x1 = 68 OR ( tok.x1 = 3 AND tok.x2 = 68 ) )" + " "
      "UNION ALL SELECT 204 , " + ORD % "tok WHERE tok.ety = 1 AND NOT ( tok.x1 = 68 OR ( tok.x1 = 3 AND tok.x2 = 68 ) )" + " "
      "UNION ALL SELECT 5516 , " + ORD % "tok WHERE tok.ety = 1 AND ( ( tok.x1 = 70 AND NOT EXISTS ( SELECT 1 FROM label y WHERE y.gate = tok.x2 AND y.symbol GLOB '[A-Za-z]*' ) ) OR ( tok.x1 = 3 AND tok.x2 = 74 ) )" + " "
      "UNION ALL SELECT 10547 , " + ORD % "tok WHERE tok.ety = 1 AND tok.v1 = 70 AND NOT EXISTS ( SELECT 1 FROM label y WHERE y.gate = tok.v2 AND y.symbol GLOB '[A-Za-z]*' )" + " ) ;")
S5 = ("WITH z AS MATERIALIZED ( SELECT q.kind , q.o FROM ( SELECT kind , o , min ( m ) AS m FROM ( SELECT r.kind , r.other AS o , r.run AS m FROM rel r WHERE r.gate = what AND r.kind IN ( 138 , 139 , 530 ) UNION ALL SELECT r.kind , r.gate , r.run FROM rel r WHERE r.other = what AND r.kind IN ( 138 , 139 , 530 ) ) GROUP BY kind , o ) q ORDER BY q.m ) "
      "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , k.c , 1 , coalesce ( ( SELECT group_concat ( z.o , ' ' ) FROM z WHERE z.kind = k.c ) , '' ) FROM ( SELECT 138 AS c UNION ALL SELECT 139 UNION ALL SELECT 530 ) k ;")
S6 = "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 25 , 0 , NULL ) ;"
DEFRUN = "( SELECT CAST ( value AS INTEGER ) FROM run_sheet WHERE run = above AND cell = 24 )"
DEFTEXT = "coalesce ( substr ( ( SELECT group_concat ( l.symbol , '' ) FROM ( SELECT l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run = %s ORDER BY s.pos ) l ) , 1 , 200 ) , '' )" % DEFRUN
human = "( SELECT symbol FROM label WHERE gate = what )"
for n in (138, 530, 139, 441, 6332, 5516, 10547, 204):
    human += " || ' | ' || " + L(n) + " || ': ' || " + W(n)
human += " || ' | ' || " + L(24) + " || ': ' || " + DEFTEXT
machine = "json_object ( " + L(23) + " , what , " + L(24) + " , " + DEFRUN + " , " + " , ".join(L(n) + " , " + J(n) for n in (441, 138, 139, 530, 6332, 5516, 10547, 204, 150, 155)) + " )"
S7 = ("WITH RECURSIVE c ( k , rest ) AS ( SELECT s.cell , s.value || ' ' FROM run_sheet s WHERE s.run = above AND s.cell IN ( 441 , 138 , 139 , 530 , 6332 , 5516 , 10547 , 204 , 150 , 155 ) ) , "
      "sp ( k , g , rest ) AS ( SELECT k , '' , rest FROM c UNION ALL SELECT k , substr ( rest , 1 , instr ( rest , ' ' ) - 1 ) , substr ( rest , instr ( rest , ' ' ) + 1 ) FROM sp WHERE rest <> '' ) , "
      "gs AS MATERIALIZED ( SELECT k , CAST ( g AS INTEGER ) AS g FROM sp WHERE g <> '' ) "
      "SELECT CASE WHEN ( SELECT arrival FROM run WHERE id = above ) = 5 THEN " + machine + " ELSE " + human + " END ;")
S8 = "INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 25 , 1 , reply ) ;"
spans = [S4, S5, S6, S7, S8]
# the trap: a cell name written bare is replaced by that cell's value when the span decodes (nk.c decode_span); 'from' is SQL's FROM and no define cell
forbidden = {'me', 'newgate', 'reply', 'def', 'say', 'know', 'remember', 'shape', 'ok', 'known', 'unknown', 'class', 'like', 'opposite', 'similar', 'tense', 'prefix', 'suffix', 'etymology'}
for i, s in enumerate(spans, 4):
    bad = [t for t in s.split(' ') if t.lower() in forbidden and not (i == 8 and t == 'reply')]
    assert not bad, (i, bad)
line = base + ' ' + ' '.join('BUILD ' + s + ' BUILD' for s in spans)
hdr = open('recall9_header.txt', encoding='utf-8').read()
with open(out, 'w', encoding='utf-8') as f:
    f.write(hdr + line + "\n# 2. define's (heard, :) row calls it.\nBUILD UPDATE dna SET call = {run:1} WHERE gate = 156 AND before = 1 AND trigger = 68 ; BUILD\n# 3. define's (the sixth, :) row calls it.\nBUILD UPDATE dna SET call = {run:1} WHERE gate = 156 AND before = 5 AND trigger = 68 ; BUILD\n")
print('line 1:', len(line), 'chars,', line.count('BUILD'), 'BUILD symbols; spans 4-8:', [len(s) for s in spans])
