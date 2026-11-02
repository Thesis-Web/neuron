#!/usr/bin/env python3
# g34/make_recall3.py (2026-11-01, 18:15; 18:30: the delimiter reads are point reads by position, the kind join never passes a NULL symbol). Writes RECALL-3-nk.txt: the recall lines (RECALL-2) with the relationships laid from the
# definitions themselves. The owner: "as part of the build step relationships are populated so that the meanings have push and pull to the
# graph"; "each one of these relationships represents a mathematical formula that connects points"; "you did opposite and alike and basically
# gave up on all the rest". The sources' returns carry the relationships in brackets: WordNet `[hypernym: {stream}, {watercourse}]`,
# `[syn: {river}]`, `[part holonym: ...]`, `[similar to: ...]`, `[derivationally related form: ...]`; Wiktionary `[synonyms: a; b]`,
# `[antonyms: ...]`, `[hypernyms: ...]`, `[related: ...]`, `[derived: ...]`. One statement reads them: the marker words between `[` and `:`
# name the relationship (mapped onto the owner's catalog words, the page's kinds where they coincide: like, opposite, is, includes, part, has,
# member, similar, derived, related, implies, causes, property, topic, context, use, past, alias); every single-symbol target between the
# delimiters becomes a rel row (about, kind, target, return). Multi-word targets are not points and are left.
# The statement runs (a) in the define run's second span on this run's returns, the long way; (b) in the ask's yes-branch on the point's own
# definition rows, once, when the point holds no relationship rows beyond like/opposite/capitalized: the back-population on use.
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
CASE = 'CASE ( SELECT group_concat ( l2.symbol , \' \' ) FROM ( SELECT l3.symbol FROM seq s2 JOIN label l3 ON l3.gate = s2.gate WHERE s2.run = r.id AND s2.pos > b.pos AND s2.pos < c.pos AND s2.gate <> 3 ORDER BY s2.pos ) l2 ) ' + ' '.join("WHEN '%s' THEN '%s'" % m for m in MAP) + ' END'
def rel_stmt(source, where):
    # source: the FROM clause giving r (the return runs); where: the condition on them
    return ('INSERT OR IGNORE INTO rel ( gate , kind , other , run ) SELECT r.about , k.gate , t.gate , r.id FROM ' + source +
            ' JOIN seq b ON b.run = r.id AND b.gate = 143'
            ' JOIN seq c ON c.run = r.id AND c.gate = 68 AND c.pos = ( SELECT min ( pos ) FROM seq WHERE run = r.id AND pos > b.pos AND gate IN ( 68 , 147 ) )'
            ' JOIN label k ON k.symbol = ( ' + CASE + ' ) AND k.symbol IS NOT NULL'
            ' JOIN seq t ON t.run = r.id AND t.pos > c.pos AND t.pos < ( SELECT min ( pos ) FROM seq WHERE run = r.id AND pos > b.pos AND gate = 147 )'
            ' JOIN label lt ON lt.gate = t.gate'
            ' WHERE ' + where + " AND r.kind = 3 AND r.arrival IN ( 7 , 443 ) AND lt.symbol GLOB '[A-Za-z]*' AND t.gate <> r.about"
            ' AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = r.id AND pos = t.pos - 1 ) , 3 ) , ( SELECT gate FROM seq WHERE run = r.id AND pos = t.pos - 2 ) ) IN ( 173 , 68 , 45 , 38 )'
            ' AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = r.id AND pos = t.pos + 1 ) , 3 ) , ( SELECT gate FROM seq WHERE run = r.id AND pos = t.pos + 2 ) ) IN ( 177 , 45 , 147 , 38 )')
REL_LEARN = rel_stmt('run r', 'r.parent = above')
REL_RECALL = rel_stmt('node n JOIN run r ON r.id = n.run', 'n.gate = what AND NOT EXISTS ( SELECT 1 FROM rel WHERE gate = what AND kind NOT IN ( 138 , 139 , 464 ) )')
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
out = ["# RECALL-3-nk.txt (2026-11-01, 18:15). RECALL-2 with the relationships laid from the definitions: WordNet's and Wiktionary's bracketed",
       "# markers (syn, hypernym, hyponym, part/member holonym and meronym, similar to, derivationally related form, synonyms, antonyms, related,",
       "# derived ...) mapped onto the owner's catalog words (like, opposite, is, includes, part, has, member, similar, derived, related, implies,",
       "# causes, property, topic, context, use, past, alias); every single-symbol target becomes a rel row. Laid the long way on a define's own",
       "# returns, and once on a recall from the point's own definition rows when it holds no such rows yet (the back-population on use).",
       "# 1. The ask: the standing question, the copy of def/known/unknown, the relationship rows from the definition node, the sources only for a point with none.",
       ASK,
       "# 2. The define run: span 1 what + the ask; span 2 the relationship rows (like/opposite from the thesaurus lines, the bracketed markers from WordNet and Wiktionary); span 3 known/unknown on source returns only.",
       DEFINE,
       "# 3. define's row calls it.",
       BIND, ""]
open('/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34/RECALL-3-nk.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('RECALL-3-nk.txt written: ask %d chars, define %d chars' % (len(ASK), len(DEFINE)))
