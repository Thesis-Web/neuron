---
name: project_neuron_poc171_teach_20261024
description: Point Of Connection 17.1 (2026-10-24, turn 23) - teaching process typed at the prompt (define from the SQL docs source, place from the measured source into a new 3D place table in the brain); 88-line sheet; results, wrong predictions, memory-hop limit, slowdown, homework list, where it lives, next step
metadata:
  type: project
---
Owner msg 35 (verbatim in t23/turn16/OWNER-VERBATIM.txt inside Downloads NEURON-v17.1-SOURCES-2026-10-24.tar.gz, messages 1-35): teach by prompts he can hand type; ground meanings in the SQL docs source; define from sources, then the brain's own process places meanings; later a process over all SQL words, then a word not in its corpus placed without being told; make the SQLite graph hold 3D vectors; long form (opcodes) only logged in a .md for the future kernel ("sqlite is the crutch"); "ask me if unsure".

Done and measured:
- 16.4 "measure a word" silicon = label counts, PROVEN by control: WRITE renamed WRITX in the told block's log text -> its silicon read WRITX 90 (was WRITE 104) with identical tables and output (check_measure.js).
- Told 17.1 (4 statements over 16.4): place (id, word, x, y, z, t, ended) + trigger (ends older place, logs without labels); 'measured' source (gate + told source line). sql.js has NO rtree; native SQLite 3.37.2 has rtree.
- Sources: sqldoc rebuilt by rule (first two sentences on the word's own sqlite.org page; filters added after first run picked headers/contents): 76 lines, 41 words; misses: '-' and '/' wrong lines, INTO < > <= >= punctuation none. measured: 612 rows (432 numbers hw WORD:kind text "value . how"; 180 line ends).
- Taught: define = SELECT text FROM definition WHERE word = :after AND src = 'sqldoc' ... say; place = INSERT INTO place ... 10 * CAST(text AS INTEGER) from measured hw LIKE :after || ':rows|structure|text'.
- Node run of all 88 lines (17 min): 43 place rows = 43 formula statements, all equal to the lab's lines-off places; never-told DROP 0,-10,0, substr 0,0,-10, EXCEPT 0,0,0 (stored 'except': first spelling wins). Controls: store 0,0,0; INSERT without measured rows 0,0,0. Browser: 10 lines via sheet clicks + run, places drawn from the brain's table.
- Wrong: P7 place is not fast (median 9 s, late lines 15-66 s, brain slows as it grows, 1,984 triggers). P5 untestable by teaching: a seen line (any case, same gates) is answered from memory and writes nothing.
- Homework: doc lines use 335 words, 33 SQL; none has a meaning.
- Kernel log: Downloads NEURON-KERNEL-LONG-FORM-2026-10-24.md (93 opcodes, SQLite's descriptions).

Where: artifact https://claude.ai/artifact/BmGjNbrAqya61PYw3Lq1wq; Downloads NEURON-POINT-OF-CONNECTION-v17.1-2026-10-24.html, NEURON-v17.1-TOLD-BLOCK-2026-10-24.sql, NEURON-TEACH-EXPECT/RESULTS-2026-10-24.md, NEURON-v17.1-SOURCES-2026-10-24.tar.gz.

**How to apply:** honest limit: places come from OUR measured source; the brain does not yet find meaning. Next (owner's call): the brain measures a new word itself (BUILD lines return rows/changes; EXPLAIN needs a told change) and a re-teach path past the memory hop. Related: [[project_neuron_poc17_20261024]], [[feedback_known_failures_checklist]].

Msg 36 corrections (10-24): table names CAN come from the typed line (tested: make/fill/tally things -> CREATE TABLE 'things', INSERT INTO 'things', count said 1). The memory hop (decide_go matches the line's gate list in memory; recalled = 1; no formula fires) also skips ACTIONS: the second "fill things" inserted nothing. Owner's ideas to keep: key words (define, learn, understand, apply, run, /build) choosing DNA-row types by how a run arrives; "define : car"; placement as a balance of a word's actions against its objects, verbs, modifiers (variables unknown); the SQL docs hold the bytecode docs.

Msg 37 (10-24): (a) .schema: reading an existing table's definition is one statement; the long form is for new tables. v1 mother.c = sqlite3_exec (SQL only, returns only ok/error), so shell ".schema memory" = SELECT sql FROM sqlite_master WHERE name = 'memory'. (b) A table the brain makes is a neuron g<gate> born through mother, never a table named by a word's letters ("there are no words in the graph"; my "things" test only checked quoting). (c) Owner design for source returns: the reply comes back as a RUN OF GATES headed by modifiers ("return from define : join from source X run /build <definition>") so the brain knows it asked for it and fills the primary run's sheet. Built today: reply rows -> secondary table -> sense -> definition table holds TEXT -> up to 8 rows run as 'defrow' lines (kind/direction columns mark them). Two differences = told changes, owner's call. (d) Memory is read by decide, taught formulas (how, before, after), timeline, memwrong, atlas, measure; only decide's hop skips the run. (e) No atlas file on disk (only turn17/atlas17.result.json counts); the page builds it live.

10-25, msgs 38-40: owner declined any build in this session ("no I can't trust to build it"). The unbuilt ask stands: the teaching process his way (define : X -> source -> answer returns as a run of gates headed by modifiers -> fills the primary run's data sheet -> neuron built; key words pick DNA rows; a run of words puts out the SQL). Do not start it without the owner asking.
