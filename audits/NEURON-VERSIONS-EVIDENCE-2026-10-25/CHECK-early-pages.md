# CHECK: early Neuron browser pages against the owner's four criteria

Read-only forensic check, 2026-10-25. Nothing in Downloads was modified. Copies and
line-number-preserving stripped versions (embedded data lines replaced by a placeholder) are in
`/tmp/claude-1000/-home-exnulla-neuron-v1/95237a7f-7d7c-47a3-a249-06f9202b6633/scratchpad/chk1/`.
All line numbers below refer to the original files (the stripped `.stripped.js.txt` copies keep
the same numbering).

Source files (in `/mnt/c/Users/AdLibitumVita/Downloads/`):

| file | lines | md5 | sql.js? |
|---|---|---|---|
| NEURON-ONE-SPACE-2026-10-21.html | 447 | 722e068b… | no |
| NEURON-ORGANIZED-KAOS-2026-10-21.html | 408 | e33a1eb6… | no |
| NEURON-POINT-OF-CONNECTION-2026-10-21.html | 1117 | dc9e056a… | no |
| NEURON-POINT-OF-CONNECTION-v11-other-session-2026-10-22.html | 1049 | e98c864d… | no |
| NEURON-POINT-OF-CONNECTION-v12-2026-10-22.html | 948 | 1b5b3cac… | no |
| NEURON-POINT-OF-CONNECTION-v13-2026-10-22.html | 1117 | dc9e056a… | no |
| NEURON-POINT-OF-CONNECTION-v14-2026-10-22.html | 1213 | ef749057… | **yes** (cdnjs sql.js 1.8.0, line 324) |

**v13 is byte-identical to POINT-OF-CONNECTION-2026-10-21** (same md5). Everything said about
one applies to the other; they are treated as one file below ("C / v13").

Every file loads three.js from cdnjs and holds one hand-written `<script>` block. The long
embedded lines are data, not code: `var SLICE = {...}` (60,742 chars, the owner's relation-map
slice: words with role/cls/sign and edges), `var NEURON_SOURCES = {...}` (~250 KB, dictionary
rows for 163 words), `var BODY = {...}` (v11 only, Lancaster sensorimotor norms), and
`var NEURON_SAT = {...}` (v14, the same dictionary rows reshaped as satellite corpora).

## The owner's criteria, as used here

1. **prompt → encoder → brain.** The brain is SQLite tables, one per neuron ("gate"), with DNA rows
   (arrival, remainder, trigger) and triggers.
2. **A trigger cannot create.** A string of SQL is assembled as a run by the neurons from the run
   table and output as text to mother, who places that string into the SQL prompt.
3. **Mother is a router and traverser only.** Works no data, decides nothing.
4. **Only hand-laid:** the neurons that make the table for the run, the hop, the trigger. Everything
   else is built by runs typed in. No Python/JS doing the brain's thinking, choosing, matching,
   templating, or writing brain tables.

---

## A. NEURON-ONE-SPACE-2026-10-21.html

Script: lines 138–447. Data: line 139 (`var SLICE`).

**1. SQLite brain?** No. There is no SQL engine and no SQL anywhere. The "brain" is JavaScript data:
`SLICE.words` (line 139) plus hard-coded dictionaries:

- line 142–161, `GEN.KINDS`: eighteen run kinds, each a fixed array of word tokens, e.g.
  `born: { label: 'born', col: 0xf0b429, seq: ['born','CREATE','TABLE','(','shard','INTEGER',')',';','BUILD','mother'] }` (148).
- line 207–221, `ROOTS`, `PRIME_ROOTS`, `WORD_PRIMES`: what every word "is made of" and which
  physical action it reduces to. The comment at 206 says `// MEANING-START  (all guesses, for the picture)`.

**2. New neuron/table on an unknown word?** (d) No tables per neuron at all. Nothing is created at
runtime. The `born` run is drawn as a polyline through dots named `CREATE`, `TABLE`, `(` … (148);
the token strings are never executed. Which run spawns which is hard-coded in `children()` (163–183),
e.g. `if (gate === 'store') out.push('born');` (167).

**3. The hop.** A JavaScript array index. `r.ticks = r.gates.map(function (g, i) { return start + i * step; })` (192);
`setTime` walks `for (var i = 0; i < r.ticks.length; i++) { if (r.ticks[i] <= t) ... }` (344–346).
No row, no trigger.

**4. Mother.** A dot. `var FAR = { sources: [175, 6, 0], mother: [-175, 6, 0], OUTPUT: [0, -120, 0] };` (224)
is a 3-D position. "mother" also appears as a token in the `lay` and `born` sequences (147–148). No
function named mother; nothing is executed.

**5. JS doing the brain's job.** All of it, by design of the page: which runs exist and their word
order (142–161); which gate starts which run (163–183); when each row "lands" (192); what every word
means (207–221, `primesOf` 246, `rootsOf` 247); which shell a word sits on (`shellOf` 249); the
silicon ledger counts (`counts[x]++` 345); the selected-run prose (384, 389–394).

**6. Verdict.** A diagram of the architecture, not an instance of it. Meets none of the four criteria
as code (no SQLite, no run-assembled SQL, no mother function, nothing built by typed runs). It does
not pretend otherwise: the rail says "Every word to prime and prime to action formula on this page is
my guess … The runs are the model from the last page." (132).

---

## B. NEURON-ORGANIZED-KAOS-2026-10-21.html

Script: lines 118–408. No embedded data beyond the hard-coded gate list.

**1. SQLite brain?** No. `GEN.GATES` (131–140) is a list of `[name, region]` pairs; `GEN.KINDS`
(141–160) is the same eighteen hard-coded run sequences as file A (`born` at 147).

**2. Creation.** (d). Nothing is created; `children()` (165–192) hard-codes the spawn graph exactly as
in A (`if (gate === 'store') out.push('born');` 171).

**3. The hop.** JS array index: `r.ticks = r.gates.map(...)` (203); `setTime` loop (324).

**4. Mother.** A dot: `['mother','far']` in GATES (139); `FAR = { sources: [150, 10, 0], mother: [-150, 10, 0], OUTPUT: [0, -78, 0] }` (255).
The reading panel describes her ("mother, which runs SQL text", 108); the code does not.

**5. JS doing the brain's job.** Run kinds, spawn graph, tick timing, the "runs active" sparkline
(`active[t2]++` 220), regions and colors. The panel admits: "The runs here are a model with the
owner's names for the kinds and plausible long forms." (112).

**6. Verdict.** Same as A: a picture. Meets none; honest about being a model.

---

## C. NEURON-POINT-OF-CONNECTION-2026-10-21.html  (= v13, byte-identical)

Script: 327–1117. Data: 328 (`SLICE`), 329 (`NEURON_SOURCES`). Engine: 384–800 (`var ENGINE = (function () {`).

The page's own claim (header, line 88): "The brain starts with only what has to be hand laid: fourteen
physical actions, sixteen physics tables with their triggers, mother and source. Nothing else."

**1. SQLite brain?** No. No sql.js. The brain is one JavaScript object `S`:

- `function create(slice) { var S = { tick: 0, events: [], gates: {}, nextId: 1, nextShard: 1, rels: [], relKey: {}, mems: [], memByList: {}, timeline: [], mother: 0, ... }` (388).
- A "gate" is `var g = { name: name, id: S.nextId++, origin: origin, role: role, born: S.tick, shards: [], hops: {}, defs: [], meaning: meaning, ... formula: null, gap: false };` (400).
- The six "physics tables" are JS arrays: `S.db = { state: [], memory: [], relation: [], definition: [], timeline: [], gate: [] }; S.tables = [...]` (392), written by `function dbInsert(S, t, row) { S.db = S.db || {}; (S.db[t] = S.db[t] || []).push(row); }` (386).
- There are no triggers anywhere; the word "trigger" is a field on a JS object (`trigger: null`, 618, 623) and a word in narration.

**2. New neuron on an unknown word.** (d) for neurons; the sentence claims (a)/(b) but no table is made.
`function ensureGate(S, w, run, why) { if (S.gates[w]) return S.gates[w]; var g = addGate(S, w, 'born', 'word', null); S.mother++; ev(S, { kind: 'born', gate: w, ... text: 'born ' + w + ' (gate ' + g.id + '): mother makes its table, its trigger, a blank definition node and its first row' ... }); ... }` (435–441).
The only `CREATE TABLE` that does anything is the user-typed `BUILD CREATE TABLE x ( a ) ; BUILD`
(preset 1017), which `typeLine` strips to text (`var sql = tokens.slice(1, -1).join(' '); var mr = mother(S, sql);` 704)
and `mother` regex-matches: `if ((m = /^CREATE TABLE (\S+)/i.exec(sql))) { ... S.db[m[1]] = []; ...}` (593). That is a JS array keyed by name, not a SQLite table, and it is a "plain table, not a neuron" by the page's own words (v11 line 700 says so explicitly).

**3. The hop.** A JavaScript `for` loop and an array search.
- `typeLine`: `var arrival = direction, pendingOp = '+'; for (var i = 0; i < tokens.length; i++) { var tk = tokens[i]; ... landOn(S, run, tk, arrival, tokens.slice(i + 1).filter(...), null); ... arrival = tk; }` (685–700).
- `landOn` (608–631): `function findShard(g, arrival, next) { for (var i = 0; i < g.shards.length; i++) if (g.shards[i].arrival === arrival && g.shards[i].next === next) return g.shards[i]; return null; }` (607); on a miss `sh = { id: S.nextShard++, arrival: arrival, next: head, trigger: null, times: 1 }; g.shards.push(sh); g.hops[head] = 1; S.mother++;` (623) and the narration `'... lay writes row s' + sh.id + ', mother lays the hop trigger ' + gname + ' → ' + head + ', the run is inserted again and the row hits.'` (624). On a hit: `'... Its own hop trigger lands the run in ' + head + '. No mother.'` (621). Neither trigger exists; the loop moves the run.
- Firing: `var fire = sh.trigger || (g.formula ? gname : null); if (fire) { ... fireWord(S, run, fire, makeFrame(...)) ... }` (629–630) — JS reads the "trigger" column and calls a JS interpreter.

**4. Mother.** `function mother(S, sql)` (582–600). She is not a router: she **is** the SQL engine,
written as regexes over JS arrays, and she decides:
- `if ((m = /^SELECT '([^']*)' = '([^']*)'$/i.exec(sql))) { eff.said = 1; return { output: m[1] === m[2] ? '1' : '0', ... text: 'compared; nothing changed' }; }` (584) — she performs the comparison.
- `/^SELECT '([^']*)' \|\| ' ' \|\| '([^']*)'$/` → `(m[1] + ' ' + m[2]).trim()` (585) — she joins.
- `/^SELECT (\w+) FROM (\w+) WHERE (\w+) (=|LIKE) '([^']*)'(?: AND (\w+) = '([^']*)')?$/` → `tb.filter(...)` over `S.db[m[2]]` (586–589) — she filters.
- `/^UPDATE gate SET meaning = '([^']*)' WHERE name = '([^']*)'$/` → `dbInsert(S, 'gate', {...})` (591).
- `/^INSERT INTO (state|memory|relation|definition|timeline) VALUES \((.*)\)$/` → builds a row object from `DBCOLS` (581, 592).
- generic CREATE/INSERT/SELECT/DELETE/UPDATE (593–597); anything else `'error: near "' + ... + '": syntax error'` (598).
- She returns canned prose (`text`) and a root ledger (`roots`) for every statement.

The SQL she runs is **composed by JS string templates**, not by a run of neurons: `viaMother(S, run, branch, frame, op, sqlWords, sqlText, cellName)` (542–550) is called from `doOp` with lines like
`"SELECT value FROM state WHERE key = '" + qa + "'"` (556), `"SELECT answer FROM memory WHERE list LIKE '%" + qa + "%'"` (557), `"INSERT INTO relation VALUES ( '" + q(subject) + "' , '" + rel + "' , '" + q(obj) + "' , ... )"` (574), `"UPDATE gate SET meaning = '" + q(a) + "' WHERE name = '" + q(subject) + "'"` (575). `sqlWalk` (537–541) then back-fills "landings" on the SQL words so the picture shows a run passing them — the picture is drawn after the fact.

Contradiction inside the file: the rail note says `mother: 'the one function beside SQLite. She does no work but traverse ... The brain cannot change her.'` (815); the code at 582–600 is a data-working, deciding pseudo-SQL.

**5. JS decisions that are the brain's job.**
- Parsing: `tokenize` (434); the line grammar `->` / `=` / `=>` / `BUILD … BUILD` by regex (650–654); `BEING`-verb subject/verb/object split in `makeFrame` (493–500); `QWORDS` (377); `SKIP` (381).
- Encoder/born: unknown-word detection `tokens.filter(function (w) { return !S.gates[w] && !HOPOPS[w]; })` (658) and the born path (660).
- Choosing sources and quotas: `take('wn', (e.wn || []).slice(0, 2)); take('gcide', (e.gcide || []).slice(0, 1)); take('mw', ... .slice(0, 2)); take('mwt', ... .slice(0, 4), 'like '); ... take('moby', ... .slice(0, 3), 'like ')` (452–453); map relations `.slice(0, 3)` (456); SQL words routed to `sqldoc` only (445).
- Ranking/agreement: `agreed = Object.keys(bySrc).filter(... >= 2).sort(...)` (471); `S.need[x]++` (475); `TRUST` weights (375) applied in `addRel` (480).
- Memory lookup and decide: `var key = direction + ' ' + tokens.join(' '), mem = S.memByList[key]` (662); reopen-on-gap regexes (663); memhit path (673–681); "decide: gate list not in memory" (682).
- Formula interpreter: `OPS` arity table (370), `OPROOT` (378), `OPERATORS` sign/scale (380, applied in `descent` 417), `fireWord` (502–529) with learned/automated thresholds (`p.receipts[rk] >= 3` 524), `PHYS_ACT` implementing memory/state/source/timeline/sense in JS (530–536), `doOp` implementing find/read/compare/join/split/move/say/write (552–579).
- Sense/mark: `if (run.expected) mark = output === run.expected ? 'right' : 'wrong'; else if (prev) mark = prev.output === output ? 'balanced' : 'shift';` (708).
- Memory and timeline writes (711–715); state write `writeState` (601–606).
- Operator trial by full replay: `['+', '-', '*', '/'].forEach(function (alt) { ... var S2 = replay(S, S.lines.length - 1); var r2 = typeLine(S2, ...) ... if (r2.output === run.expected) winner = alt; })` (720) and binding `rowB.op = winner` (722).
- Teaching writes the brain directly: `g.formula = gates;` (740), `g.meaning = act.roots; g.meaningOrigin = 'told'` (742), proc status (743); `bindRow` writes a shard with its trigger (756–757).
- Canned text: `SUGGEST` formulas (357–369), every `ev(...)` sentence, default reply `w + '?'` for words with no meaning (705), gap prose (`run.gaps.push({ need: ..., fill: ..., who: ... })` throughout).
- Counters: `S.mother++` (437, 544, 623, 704, 757), `S.sourceCalls` (457), `sh.times++`, `mem.times++`.

**6. Verdict.** A JavaScript simulation that narrates the owner's design. Breaks all four: (1) the brain
is a JS object, not SQLite; (2) no trigger exists and the SQL that reaches "mother" is JS-templated
(`viaMother` call sites 556–576), not assembled by a run; (3) mother is a regex SQL engine that compares,
joins, filters and writes; (4) encoder, decide, source, agree, memory, sense, say, teach and the formula
interpreter are all hand-written JS. The header's "Nothing else [is hand laid]" (88) is not true of the code.

---

## D. NEURON-POINT-OF-CONNECTION-v11-other-session-2026-10-22.html

Script: 283–1049. Data: 284 (`SLICE`), 285 (`NEURON_SOURCES`), 343 (`BODY`). Engine: 347–780.

Header claim (82): "Version 11. Points are meanings, numbered; words are labels the encoder attaches …
The brain starts with only what has to be hand laid: fourteen physical actions, sixteen physics tables
with their triggers, three silicon jobs, mother and source. Nothing else."

**1. SQLite brain?** No. No sql.js; not even the `S.db` arrays of C. State is `S.gates` (350, 363),
`S.rels` (506), `S.mems` (724), `S.state` (593), `S.timeline` (727). No table, no trigger.

**2. New neuron.** (d). `ensureGate` (403–411): `addGate(S, w, 'born', 'word', null); S.mother++; ev(S, { kind: 'born', ... text: 'born ' + w + ' (gate ' + g.id + '): mother makes its table, its trigger, a blank definition node and its first row' + ... })` (405–406). Only a JS object. The encoder then guesses a base form by suffix regex (`formOf` 413–427: `/ies$/`, `/(s|x|z|ch|sh)es$/`, `/ed$/`, `/ing$/`, `/est$/`, `/er$/`) and writes a `form` relation (408).
BUILD path (700): `var mt = /^CREATE TABLE (\S+)/.exec(sql); S.mother++; if (mt) { if (S.tables.indexOf(mt[1]) >= 0) output = 'error: table ' + mt[1] + ' already exists'; else { S.tables.push(mt[1]); output = 'ok'; } } else output = 'ok';` — a name pushed into an array; every other statement is answered `'ok'` without being read. The event text itself says "(a plain table, not a neuron)".

**3. The hop.** JS loop (676–696) + `landOn` (600–623), same shape as C (`g.shards.push(sh); g.hops[head] = 1; S.mother++;` 615; narration 616). New here: the operator is treated as a neuron with rows laid in JS (`og2.shards.push(orow)` 681) and the hop mechanic is chosen by the `HOPOPS` dict (337) or an `S.override` (684).

**4. Mother.** No function at all. `mother` is a counter (`S.mother++` at 405, 615, 700, 766), a far dot (`FARP` 794) and words in event text. No SQL of any kind is executed in this file.

**5. JS doing the brain's job** (everything in C, plus):
- `PRIME_ROOTS` assigns a physical action to every prime (290–296), e.g. `people:['FIND','ADD']` — the assignment the next versions say "was an assignment and is gone".
- Morphology: `formOf` (413–427).
- Relation derivation from dictionary text by regex: `/\[syn: ([^\]]+)\]/`, `/\[ant: ([^\]]+)\]/` (460); genus = first noun after an article, `/^\s*(?:a|an|the|any|some)\s+([a-z][a-z' -]*?)(?=\s+(?:with|that|which|who|...)\b|...)/i` (465); written when `srcs.length >= 2` else "guess" (470); limits `out(like, 'alike', 6); out(opp, 'opposite', 3); out(genus, 'is', 2);` (471).
- Candidate meaning compilation: `compileMeaning` (475–487) picks `parts` from agreed words that already mean something and scores with `bodyBalance` (598, cosine over the Lancaster channels) against thresholds `bb.cos >= .88 ? 'held' : bb.cos >= .72 ? 'undecided' : 'does not balance'` (483).
- Sleep passes: `recompile` (489–495) and `readAll` (496–502) run every one of the 163 source words at page load (`ENGINE.readAll(S)` 1042, 1044).
- Shape/metaphor: `shapeSim` Levenshtein (597) and `if (best && bs >= .75) { run.shapeOf = best.id; ... 'A metaphor candidate by shape' }` (704).
- `physicsRun` implements memory/state/source/sense/agree/timeline/SPLIT/JOIN in JS (573–589); `doOp` (543–571).
- Operator trial via `cloneS` (596) over `['continue','step back','test','choose']` (713) and the brain "writes it into the row's trigger column itself" `if (winner) o.row.trigger = winner;` (721).
- `choices` arrays from alike relations (730); `JOBS` (339); `CHANNEL_PORT` (344).

**6. Verdict.** Breaks all four, more deeply than C: no SQL engine at all (not even a fake one), mother is a counter, and the brain's derivations (relations, candidate meanings, body-balance test, morphology, metaphor-by-shape) are JS algorithms with hand-picked thresholds. The header's "Nothing else" (82) is not true of the code.

---

## E. NEURON-POINT-OF-CONNECTION-v12-2026-10-22.html

Script: 286–948. Data: 287 (`SLICE`), 288 (`NEURON_SOURCES`). Engine: 337–699.

Header claim (81): identical to C ("sixteen physics tables with their triggers, mother and source. Nothing else").

**1. SQLite brain?** No. JS object `S` (340, gate object 351). `S.db` exists only lazily inside `mother()` (`S.db = S.db || {};` 495). `PRIME_ROOTS = {}` (296) with the note "No table says what a prime does. One did, from the first version (people as FIND and ADD); it was an assignment and is gone."

**2. New neuron.** (d). `ensureGate` (386–392), same narration (389). BUILD → `mother()` (606 → 494): `if ((m = /^CREATE TABLE (\S+)/i.exec(sql))) { ... S.db[m[1]] = []; eff.tables = 1; ... S.tables.push(m[1]); }` (496) — JS array.

**3. The hop.** JS loop (588–602) + `landOn` (511–534): `sh = { id: S.nextShard++, arrival: arrival, next: head, trigger: null, times: 1 }; g.shards.push(sh); g.hops[head] = 1; S.mother++;` (526); narration "mother lays the hop trigger" (527).

**4. Mother.** `function mother(S, sql)` (494–503): five regexes (CREATE / INSERT / SELECT / DELETE / UPDATE) over `S.db` arrays; `INSERT` stores the raw `VALUES (...)` text (`S.db[m[1]].push(vals)` 497); `SELECT` returns `S.db[m[1]].join(' | ')` (498); else `'error: near "...": syntax error'` (501). Reached only from the BUILD path (606). Unlike C, `doOp` here does **not** go through mother: find/read/compare/write act directly on `S.mems`, `S.state`, `S.rels` (466–491). So mother is a toy SQL for the BUILD demo, and the brain's reads/writes bypass her entirely.

**5. JS doing the brain's job.** As C minus the `viaMother` templates: tokenize/grammar (553–557); unknown detection (561); source quotas (399–403) and agreement (408–414); `makeFrame` (423–430); `fireWord`/`OPS` (432–456); `PHYS_ACT` (457–463); `doOp` (464–492); `descent`/`OPERATORS` (356–383); memory/decide (565–585); sense/mark (609–612); trial by `replay` (618–625) binding `rowB.op = winner` (624); `teach` writes `g.formula = gates;` (640) and meaning from `actionOf` (642); `bindRow` (649–660); `contrast`/`meaningOf` measurement (661–689); `SUGGEST` (316–327); default output `w + '?'` (607); counters.

**6. Verdict.** Breaks all four. Brain is JS; mother is a five-regex pseudo-SQL used only for BUILD; the brain's own reads and writes never touch her; hop is a loop; thinking is JS. Header "Nothing else" (81) is not true of the code.

---

## F. NEURON-POINT-OF-CONNECTION-v14-2026-10-22.html

Script: 325–1213. Data: 326 (`SLICE`), 327 (`NEURON_SAT`). Engine: 373–876. sql.js: `<script src="https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/sql-asm-memory-growth.js">` (324); `initSqlJs().then(function (SQL) { ENGINE.init(SQL); S = ENGINE.create(SLICE, NEURON_SAT); boot(); })` (1211).

Header claim (98): "Here mother runs real SQLite in your browser. The sources are separate databases with mailboxes. A word's formula is a row the brain holds, and what comes back from outside is checked before it is used." Engine comment (329–330): "The JavaScript here plays the part of the SQLite triggers of the told physics; it decides nothing a neuron should decide."

**1. SQLite brain?** Partly. Real SQLite exists under the page, but it does not hold the neurons.

What is in SQLite:
- `var db = S.sql = new SQL.Database();` (387).
- Six physics tables: `db.run("CREATE TABLE state(key TEXT, value TEXT, t INTEGER); CREATE TABLE memory(id INTEGER, list TEXT, output TEXT, answer TEXT); CREATE TABLE relation(a TEXT, rel TEXT, b TEXT, trust REAL DEFAULT 0.6); CREATE TABLE definition(word TEXT, src TEXT, hw TEXT, text TEXT); CREATE TABLE timeline(t INTEGER, mem INTEGER); CREATE TABLE formula(word TEXT, gates TEXT, origin TEXT DEFAULT 'told', t INTEGER DEFAULT 0, ended INTEGER DEFAULT 0);"` (392).
- Two real triggers that call back into JS through registered functions: `"CREATE TRIGGER relation_drawn AFTER INSERT ON relation BEGIN SELECT drawrel(NEW.a, NEW.rel, NEW.b, NEW.trust); END;"` (393) and `"CREATE TRIGGER formula_written AFTER INSERT ON formula BEGIN SELECT formulawritten(NEW.word, NEW.gates, NEW.origin); END;"` (394); `db.create_function('drawrel', ...)`, `('formulawritten', ...)`, `('satwork', ...)` (388–390).
- Seven attached in-memory satellite databases (`ATTACH ':memory:' AS wn` … 399) each with `corpus`, `inbox`, `outbox` and a SQL trigger that does the lookup: `"CREATE TRIGGER " + s + ".work AFTER INSERT ON inbox BEGIN INSERT INTO outbox SELECT NEW.ask, NEW.word, hw, text FROM corpus WHERE word = NEW.word; SELECT satwork(...); DELETE FROM inbox WHERE ask = NEW.ask; END;"` (401).

What is **not** in SQLite:
- The neurons. `addGate` (407–414) still makes `var g = { name: name, id: S.nextId++, origin: origin, role: role, born: S.tick, shards: [], hops: {}, defs: [], formula: null, formulaOrigin: null, measured: {}, sourced: false };` in the `S.gates` dict.
- The DNA rows (`shards`) and hop "triggers" (`g.hops[head] = 1`): JS objects (610, 615).
- The formula a gate runs: the `formula_written` trigger copies the SQL row **out** into the JS gate (`onFormula`: `g.formula = tokenize(gates); g.formulaOrigin = origin;` 432), and `fireWord` reads `g.formula` (566), not the table.
- Relations: `onRelation` copies each inserted row into `S.rels` for drawing (427).

So SQLite is a ledger beside a JS brain: the JS writes it and reads it, and two triggers mirror writes back into JS memory.

**2. New neuron on an unknown word.** (d) for neurons. `ensureGate` (415–421): `var g = addGate(S, w, 'born', 'word'); S.mother++; ev(S, { kind: 'born', ... text: 'born ' + w + ' (gate ' + g.id + '): mother makes its table, its trigger, a blank definition node and its first row' ... })` (417–418). No `CREATE TABLE <word>` is ever issued; grep finds CREATE TABLE only at 392 (schema), 400 (satellites), 230 (an HTML doc row) and 1093 (a preset the user types).

Where SQL *is* assembled from gate tokens and handed to mother (the nearest any file comes to criterion 2):
- A word's formula may contain SQL. `fireWord` (572–583): `if (SQL_VERB[w]) { var j = i; while (j < gates.length && gates[j] !== ';') j++; var stmt = gates.slice(i, Math.min(j + 1, gates.length)); ... var text = stmt.map(function (t) { return t[0] === ':' ? sqlQuote(val(frame, t)) : t; }).join(' '); var res = sendOut(S, run, branch, text); ...}`. The statement text is the formula's own tokens with holes filled; it goes to `mother()` as text (504). But: the statement boundary is decided by the JS table `SQL_VERB = { SELECT: 1, INSERT: 1, UPDATE: 1, DELETE: 1, CREATE: 1, WITH: 1 }` (359) and the quoting by `sqlQuote` (469); no trigger does it; and no formula ever makes a neuron table.
- BUILD lines: `sendOut(S, run, run, tokens.slice(1, -1).join(' '))` (735).
- Formulas themselves are written to the `formula` table by a JS template, not by a run: `physWriteFormula`: `S.sql.run("UPDATE formula SET ended = 1 WHERE word = ? AND ended = 0", [word]); S.sql.run("INSERT INTO formula (word, gates, origin, t) VALUES (?, ?, ?, ?)", ...)` (444), called from `teach` (773).

**3. The hop.** Still a JS loop. `typeLine`: `for (var i = 0; i < tokens.length; i++) { ... landOn(S, run, tk, arrival, tokens.slice(i + 1).filter(...), build ? 'build' : null); ... arrival = tk; }` (718–731). `landOn` (601–631) with `findShard` over the JS array (600), `g.shards.push(sh); g.hops[head] = 1; S.mother++;` (615) and the narration "mother lays the hop trigger … the run is inserted again and the row hits" (616). The two real SQL triggers fire on `relation`/`formula` inserts (393–394), not on a hop; the satellite trigger (401) does a lookup, not a hop. The failed-ask step-back picks an alternate shard in JS (`g.shards.forEach(function (x) { if (!alt && x !== sh && x.trigger && ...) alt = x; })` 627).

**4. Mother.** `function mother(S, text)` (451–466). The function itself is close to the owner's words:
`try { res = S.sql.exec(text); changes = S.sql.getRowsModified(); } catch (e) { err = e.message; res = []; }` (454); counts `sqlite_master` before/after (453, 455); picks up every satellite outbox the `satwork` callback reported populated during the exec and empties it (`rows(S, "SELECT hw, text FROM " + p.sat + ".outbox WHERE ask = ?", [p.ask]); S.sql.run("DELETE FROM " + p.sat + ".outbox WHERE ask = ?", [p.ask]);` 457–458); and regex-scans the text for `\b(\w+)\.inbox\b` to list which sats were "carried" to (462). She returns rows, error, change count, tables made, picked, carried, waiting. Comment 449–450: "she does no work but the traverse."

Beyond that, her return path does the brain's sense work in JS, in `sendOut` (502–533):
- `measuredRoots(r)` (471) attributes READ/SAY/WRITE/SUBTRACT/SPAWN/FIND/COMPARE/CALL/MOVE counts from the statement's first word and a `\bWHERE\b` regex.
- `checkReturn` (474–491) decides which returned rows are kept or set aside by comparing headwords (`if (base === p.word) kept.push(...) else if (base.toLowerCase() === p.word.toLowerCase()) aside.push(...)` 478–481), updates `S.trust[sat]` counters (483), writes prose for "asked for? / needed? / asked wrong?" (484–486), and only kept rows are written to `definition` (`physWriteDefinition` 522).
- `checkSql` (492–500) decides asked/needed/wrong for plain statements; `branch.failed` is set from it (580) and drives the step-back (626).
- `cell(...)` fills (521, 530).

**5. JS doing the brain's job.**
- Parsing: `tokenize` (377), line grammar regexes (674–678), `isLiteral` (371), `BEING`/`QWORDS` (364, 368), `makeFrame` (542–549).
- Encoder/born: unknown detection (682); `bornRun` (647–664) fires source, runs the definition rows as branches, fires derive/deduce; `agreeStep` (638–646) agreement count and `S.need`.
- Formula interpreter: statement splitting by `SQL_VERB` and `sqlQuote` (572–583); `PHYS_ACT` memory/state/source/timeline/sense/say in JS (550–557), with memory/state read through JS-written SQL (`physReadMemory`: `"SELECT answer, output FROM memory WHERE list = ? ORDER BY id DESC LIMIT 1"` 445; `physReadState` 440); learned/automated thresholds (593–594).
- Physics tables written by JS templates, not by runs: `physWriteState` (439), `physWriteMemory` (441), `physCorrectMemory` (442), `physWriteTimeline` (443), `physWriteFormula` (444), `physWriteDefinition` (446).
- Decide/memory: `S.memByList[key]` (686), reopen regexes (688–695), memhit (705–713).
- Sense/mark (738–742); operator trial by full `replay` with a fresh SQLite each (752) and `rowB.op = winner` (754).
- Mother's return path: `measuredRoots`, `checkReturn`, `checkSql`, trust counters (471–500).
- `onRelation` dedupe key and trust (423–429).
- Canned text: `SUGGEST` formulas, now SQL text (878–888, e.g. `derive` = `"INSERT INTO formula ( word , gates , origin ) SELECT :subject , gates , 'derived' FROM formula WHERE ended = 0 AND word IN ( SELECT b FROM relation WHERE a = :subject AND rel = 'like' ) ..."` 883), labelled "my hypothesis, typed for you to test, never a meaning laid by code" (1079); every `ev()` sentence; default reply `w + '?'` (736); gap prose.
- Counters: `S.mother++` (417, 452, 615, 817), `S.trust[...]` (483), `sh.times++`, `mem.times++`.

**6. Verdict.** The first file with a real SQLite under it, and the only one where text assembled from a run's own gate tokens is handed to a mother who pastes it into the SQL prompt (BUILD at 735; formula statements at 572–583 → 504 → 454): partial credit on criterion 2 and on the "router/traverser" half of criterion 3. Breaks: (1) neurons, DNA rows and hop triggers are JS objects, never tables (`addGate` 407–414, `landOn` 601–631); SQLite holds six physics tables and a formula ledger that a trigger copies back into JS; (2) the statement splitter and hole-quoting are JS, no trigger assembles anything, and no run ever creates a neuron table; (3) mother's return path (`sendOut`, `measuredRoots`, `checkReturn`, `checkSql`, 471–533) decides and works data; (4) the physics tables are written by JS templates (439–446) and the encoder/decide/born/agree/sense/formula interpreter are hand-written JS. Far more than "the table for the run, the hop, the trigger" is hand-laid.

---

## Cross-file notes

- Every POC page's header says the brain starts with "sixteen physics tables with their triggers" (C 88, D 82, E 81). In C, D and E no table or trigger exists; the sixteen are entries of the JS array `PHYSICS` (C 338–355) with `does:` prose. In F, six physics tables and two triggers exist (392–394); the other ten "physics" are still JS.
- Every POC `ensureGate` emits the sentence "mother makes its table, its trigger, a blank definition node and its first row" (C 438, D 406, E 389, F 418) and none of them makes a table or trigger. The narration is ahead of the mechanism in all four.
- The hop is the same JS loop in all four POC versions (`landOn` + `for (var i = 0; i < tokens.length; i++)`), with the words "hop trigger" appearing only in event text and as `g.hops[head] = 1`.
- The lineage of "mother": A/B a dot; D a counter; C a regex SQL engine that also compares and joins; E a five-regex pseudo-SQL for the BUILD demo only; F real SQLite via `S.sql.exec(text)` with a JS checking layer on her return path.
- v13 (2026-10-22) is byte-for-byte the 2026-10-21 POC file; the "13" name adds nothing to the code.

## Compact table

| file | brain in SQLite? | creation mechanism | hop mechanism | mother | verdict |
|---|---|---|---|---|---|
| ONE-SPACE 10-21 | no; JS dicts `SLICE`, `GEN.KINDS` (139, 142–161) | (d) none; `born` is a token list drawn as a line (148) | JS array index `r.ticks = r.gates.map(...)` (192), loop 344 | a 3-D point `FAR.mother` (224); no function | diagram; meets none, admits "all guesses" (132, 206) |
| ORGANIZED-KAOS 10-21 | no; `GEN.GATES`/`KINDS` (131–160) | (d) none; `children()` hard-codes spawns (165–192) | JS array index (203), loop 324 | a point `FAR.mother` (255), `['mother','far']` (139) | diagram; meets none, says "a model" (112) |
| POC 10-21 (= v13, same md5) | no; JS object `S`, arrays `S.db` (388, 392, 400) | (d); `ensureGate` makes a JS object + sentence (435–441); BUILD CREATE → regex `S.db[name] = []` (593) | JS `for` loop (686–700) + `landOn`/`findShard` on arrays (607–631); "hop trigger" is text (624) | `function mother(S, sql)` regex SQL engine that compares/joins/filters/writes (582–600); SQL she runs is JS-templated (556–576) | breaks all four; "Nothing else hand laid" (88) untrue |
| POC v11 other-session 10-22 | no; JS object, no `S.db` at all (350, 363) | (d); `ensureGate` (403–411); BUILD → `/^CREATE TABLE/` pushes a name (700) | JS loop (676–696) + `landOn` (600–623); operator rows in JS (681) | none; `S.mother++` counter only (405, 615, 700, 766) | breaks all four, deepest: relations/meanings/morphology/body-cosine are JS algorithms (413–502, 598) |
| POC v12 10-22 | no; JS object (340, 351) | (d); `ensureGate` (386–392); BUILD → regex `S.db[name] = []` (496) | JS loop (588–602) + `landOn` (511–534) | `function mother(S, sql)` five regexes over arrays (494–503), BUILD only (606); brain reads/writes bypass her (466–491) | breaks all four |
| POC v13 10-22 | identical to POC 10-21 | identical | identical | identical | identical |
| POC v14 10-22 | partly: sql.js real (324, 387); six physics tables + 2 triggers (392–394) + 7 satellite DBs with lookup triggers (398–403); neurons/DNA rows/hops stay JS (407–414, 610–615) | (d) for neurons (`ensureGate` 415–421, no CREATE TABLE per word); run-token SQL does reach mother as text for BUILD (735) and formula statements (572–583), split/quoted by JS (359, 469) | JS loop (718–731) + `landOn` (601–631); SQL triggers fire on relation/formula inserts, not hops | `function mother(S, text)`: `S.sql.exec(text)` + outbox pickup (451–466), close to "router"; but `sendOut`/`checkReturn`/`checkSql`/`measuredRoots` decide and work data (471–533) | partial on 2 and the router half of 3; breaks 1 and 4; physics tables written by JS templates (439–446) |
