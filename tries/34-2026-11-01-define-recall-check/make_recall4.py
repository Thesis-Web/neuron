#!/usr/bin/env python3
# g34/make_recall4.py (2026-11-01, 18:20). RECALL-3's relationship statement cost 58 s on river's 184 old returns: SQLite evaluated the
# bracket's marker (a group_concat over the return's symbols) and its closing position again for every symbol inside every bracket, and
# Wiktionary's example brackets run to hundreds of symbols. Here each bracket is one row of a materialized table (its return, its marker's
# kind, its colon and its closing bracket), only brackets whose marker the catalog names are kept, and the targets are walked once per kept
# bracket with point reads for the delimiters. The same statement in the define's second span (this run's returns) and in the ask's
# yes-branch (the point's own definition rows, once). Also written: the SELECT form of the recall statement, to time it as a read first.
import sys
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
CASE = "CASE ( SELECT group_concat ( l3.symbol , ' ' ) FROM ( SELECT l2.symbol FROM seq s2 JOIN label l2 ON l2.gate = s2.gate WHERE s2.run = br.run AND s2.pos > br.p0 AND s2.pos < br.pc AND s2.gate <> 3 ORDER BY s2.pos ) l3 ) " + ' '.join("WHEN '%s' THEN '%s'" % m for m in MAP) + ' END'
def rel_cte(source, where):
    return ('WITH br AS MATERIALIZED ( SELECT r.id AS run , r.about AS about , b.pos AS p0 , ( SELECT min ( pos ) FROM seq WHERE run = r.id AND pos > b.pos AND gate IN ( 68 , 147 ) ) AS pc , ( SELECT min ( pos ) FROM seq WHERE run = r.id AND pos > b.pos AND gate = 147 ) AS pe FROM ' + source +
            ' JOIN seq b ON b.run = r.id AND b.gate = 143 WHERE ' + where + ' AND r.kind = 3 AND r.arrival IN ( 7 , 443 ) ) , '
            'kb AS MATERIALIZED ( SELECT br.run , br.about , br.pc , br.pe , k.gate AS kind FROM br JOIN label k ON k.symbol = ( ' + CASE + ' ) AND k.symbol IS NOT NULL WHERE br.pe IS NOT NULL AND ( SELECT gate FROM seq WHERE run = br.run AND pos = br.pc ) = 68 ) ')
def rel_insert(source, where):
    return (rel_cte(source, where) + 'INSERT OR IGNORE INTO rel ( gate , kind , other , run ) SELECT kb.about , kb.kind , t.gate , kb.run FROM kb JOIN seq t ON t.run = kb.run AND t.pos > kb.pc AND t.pos < kb.pe JOIN label lt ON lt.gate = t.gate'
            " WHERE lt.symbol GLOB '[A-Za-z]*' AND t.gate <> kb.about"
            ' AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos - 1 ) , 3 ) , ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos - 2 ) ) IN ( 173 , 68 , 45 , 38 )'
            ' AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos + 1 ) , 3 ) , ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos + 2 ) ) IN ( 177 , 45 , 147 , 38 )')
def rel_select(gate):
    return (rel_cte('node n JOIN run r ON r.id = n.run', 'n.gate = %d' % gate) + 'SELECT count ( * ) , count ( DISTINCT kb.kind ) FROM kb JOIN seq t ON t.run = kb.run AND t.pos > kb.pc AND t.pos < kb.pe JOIN label lt ON lt.gate = t.gate'
            " WHERE lt.symbol GLOB '[A-Za-z]*' AND t.gate <> kb.about"
            ' AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos - 1 ) , 3 ) , ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos - 2 ) ) IN ( 173 , 68 , 45 , 38 )'
            ' AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos + 1 ) , 3 ) , ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos + 2 ) ) IN ( 177 , 45 , 147 , 38 )')
REL_LEARN = rel_insert('run r', 'r.parent = above')
REL_RECALL = rel_insert('node n JOIN run r ON r.id = n.run', 'n.gate = what AND NOT EXISTS ( SELECT 1 FROM rel WHERE gate = what AND kind NOT IN ( 138 , 139 , 464 ) )')
INBOX = ' ; '.join('INSERT INTO %s.inbox ( run , cell , about , word ) SELECT above , 24 , what , symbol FROM label WHERE gate = what AND NOT EXISTS ( SELECT 1 FROM node WHERE gate = what )' % s for s in ('wn', 'gcide', 'mwt', 'moby', 'map', 'sqldoc', 'measured', 'wikt'))
ASK = ('BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 24 , 0 , NULL ) ; '
       'INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , cell , state , value FROM run_sheet WHERE run = ( SELECT parent FROM run WHERE id = ( SELECT max ( run ) FROM node WHERE gate = what ) ) AND cell IN ( 24 , ( SELECT gate FROM label WHERE symbol = \'known\' ) , ( SELECT gate FROM label WHERE symbol = \'unknown\' ) ) AND state = 1 ; '
       + REL_RECALL + ' ; ' + INBOX + ' ; BUILD')
SPAN1 = 'BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , ( SELECT gate FROM seq WHERE run = above AND pos = ( SELECT min ( pos ) FROM seq WHERE run = above AND gate = 68 ) + 2 ) ; INSERT INTO replay ( parent , source , kind ) VALUES ( above , {run:1} , 1 ) ; BUILD'
SPAN2 = ("BUILD INSERT OR IGNORE INTO rel ( gate , kind , other , run ) SELECT r.about , k.gate , s.gate , r.id FROM run r JOIN seq k ON k.run = r.id AND k.gate IN ( SELECT gate FROM label WHERE symbol IN ( 'like' , 'opposite' ) ) JOIN seq s ON s.run = r.id AND s.pos > k.pos JOIN label l ON l.gate = s.gate WHERE r.kind = 3 AND r.arrival IN ( 10 , 11 , 12 ) AND r.parent = above AND l.symbol GLOB '[A-Za-z]*' AND NOT ( l.symbol = 'of' AND s.pos = k.pos + 2 ) AND NOT EXISTS ( SELECT 1 FROM seq z JOIN label y ON y.gate = z.gate WHERE z.run = r.id AND z.pos > k.pos AND z.pos < s.pos AND y.symbol IN ( ';' , 'like' , 'opposite' ) ) ; "
         + REL_LEARN + ' ; BUILD')
SPAN3 = ("BUILD WITH x ( g , h ) AS MATERIALIZED ( SELECT DISTINCT s.gate , EXISTS ( SELECT 1 FROM node n WHERE n.gate = s.gate AND n.source <> 15 ) FROM run r JOIN seq s ON s.run = r.id JOIN label l ON l.gate = s.gate WHERE r.kind = 3 AND r.arrival IN ( 7 , 8 , 10 , 11 , 12 , 13 , 14 , ( SELECT gate FROM label WHERE symbol = 'wikt' ) ) AND r.parent = above AND l.symbol GLOB '[A-Za-z]*' ORDER BY s.gate ) INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , k.gate , 1 , coalesce ( ( SELECT group_concat ( x.g , ' ' ) FROM x WHERE x.h = ( k.symbol = 'known' ) ) , '' ) FROM label k WHERE k.symbol IN ( 'known' , 'unknown' ) AND EXISTS ( SELECT 1 FROM run WHERE parent = above AND kind = 3 AND arrival IN ( 7 , 8 , 10 , 11 , 12 , 13 , 14 , ( SELECT gate FROM label WHERE symbol = 'wikt' ) ) ) ; BUILD")
DEFINE = SPAN1 + ' ' + SPAN2 + ' ' + SPAN3
BIND = 'BUILD UPDATE dna SET call = {run:2} WHERE gate = {gate:define} AND before = 1 AND trigger = 68 ; BUILD'
D = '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34'
open(D + '/RECALL-4-nk.txt', 'w', encoding='utf-8').write('\n'.join([
    "# RECALL-4-nk.txt (2026-11-01, 18:20). RECALL-3's lines with the relationship statement reshaped: each bracket of a return is one row",
    "# (its marker mapped onto the catalog's word, its colon, its closing bracket), only the brackets the catalog names are walked, each once.",
    "# RECALL-3's form walked every symbol of every bracket and re-read the marker for each: 58 s on river's 184 returns.",
    "# 1. The ask: the standing question; the copy of def/known/unknown; the relationship rows from the definition node, once; the sources only for a point with none.",
    ASK,
    "# 2. The define run: what and the ask; the relationship rows (thesaurus like/opposite; WordNet's and Wiktionary's markers); known/unknown on source returns only.",
    DEFINE,
    "# 3. define's row calls it.",
    BIND, ""]))
open(D + '/rel_select_river.sql', 'w').write(rel_select(3393))
open(D + '/rel_select_stone.sql', 'w').write(rel_select(924))
open(D + '/rel_select_know.sql', 'w').write(rel_select(26))
print('RECALL-4-nk.txt written: ask %d chars, define %d chars; rel_select_*.sql written' % (len(ASK), len(DEFINE)))
