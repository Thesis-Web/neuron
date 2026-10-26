# CHECK: hp, hp2 and v2 builds against the owner's four criteria

Read-only forensic check, 2026-10-25. Nothing on hp, hp2 or in Downloads was modified. Copies read here:
- A: `chk5/hp/` (scp of `hp:~/neuron-build/kernel/*.go`, `lay/*.lay`, docs; `hp:~/ndry/d.OlXe/home/brain.db` probed as `chk5/hp/probe.db`). `hp:~/own` holds one 1-byte file `up`; `hp:~/ndry/d.*` are dry-run brains (lay + brain.db + acts.log), same kernel.
- B: `chk5/hp2/` (scp of `hp2:~/neuron-build/kernel/*.go`, `lay/*.lay`, KERNEL-SPEC.md, TOLD-PROCESSES.md, ADVERSARY-FINDINGS.md, DECISIONS.md, `~/mail-to-hub/*.md`). No `.db` readable under `hp2:~`; the live brain is `/home/neuron/brain.db` (REPORT-TURN-ONE.md:3).
- C: `chk5/v2/neuron-v2/` (tar extract of `neuron-v2-experimental-2026-10-20.tar.gz`; nothing run from it).

The owner's criteria, as given:
1. prompt -> encoder -> brain; brain = SQLite tables, one per neuron ("gate"), with DNA rows (arrival, remainder, trigger) and triggers.
2. A trigger does not "presto" create; a run through the gates assembles a SQL string from the run table, outputs it to the mother, the mother pastes it into the SQL prompt.
3. Mother is only a router and traverser; works no data, decides nothing.
4. Hand-laid only: the neurons that make the run table, the hop, the trigger. No Python/JS/Go/C doing the brain's thinking, choosing, matching, templating, or writing brain tables.

---

## A. hp (`~/neuron-build`, Go kernel, "turn one" 2026-10-19)

### A1. Where the brain lives; one table per neuron?

One SQLite file mirrored into Go structs; the hop reads the Go structs, not SQL.

- `hp/store.go:3-4`: `// store.go: the brain's body on disk (one SQLite file) and its life in RAM.` / `// The kernel loads once at start, writes to RAM, and commits dirty rows each beat.`
- Fixed schema, `hp/store.go:145-165`: 12 tables `gate, shard, trig, rel, mem, timeline, label, def, receipt, source, trust, kv`. A neuron is one row of `gate`:
  `CREATE TABLE IF NOT EXISTS gate(gate INTEGER PRIMARY KEY, x REAL ..., bind TEXT NOT NULL, bval TEXT NOT NULL, miss INTEGER NOT NULL, made TEXT NOT NULL, by INTEGER NOT NULL);` (store.go:146)
- The DNA-like rows exist but in shared tables: `shard(gate, arrival, head, next, seen, right, wrong, last, made, by)` (store.go:147) and `trig(gate, arrival, head, togate, worth, made, by)` (store.go:148).
- Go mirrors: `type Gate struct { ... Shards map[[2]int]*Shard; Trigs []*Trig ... }` (store.go:18-34); `load()` reads every table into RAM at start (store.go:187-282).
- Probe of the dry-run body `hp:~/ndry/d.OlXe/home/brain.db` (copy): `sqlite_master` lists exactly those 12 tables and **0 triggers**; `gate` 1649 rows, `shard` 4221, `trig` 241; `made` column: told 1626, spawned 17, core 5, derived 1.

So: SQLite yes; one table per neuron no; DNA rows yes (arrival/head/next in `shard`) but read from Go maps; SQL triggers none.

### A2. How a new neuron is created on an unknown word -> (c) outside code composes/executes

- The hop misses in Go and pushes the run into the told miss process: `hp/run.go:315-345`
  `if sh == nil { // the miss way: the miss process decides ... r.push(gv(at.Id)); r.push(gv(r.From)) ... r.From, r.At = at.Id, miss; b.pass(r, miss); return }`
- The told miss way (lay notation) reaches a SPAWN gate: `hp/lay/20-memory.lay:73`: `proc miss-word: spawn swap over write-label newborn miss-born`; `hp/lay/00-roots.lay:95`: `gate spawn @ 2 6 -10 : SPAWN`.
- SPAWN is a Go `switch` case: `hp/physics.go:756-771`
  `case "SPAWN": ... ng := s.newGate(p, "", "", "spawned", r.Mem); birth := s.newMem("birth", ng.Id, ...); ... r.push(gv(ng.Id)); b.act("SPAWN run=%d gate=%d at=%s", ...)`
- `newGate` appends a Go struct and marks it dirty: `hp/store.go:408-415` `g := &Gate{Id: len(s.gates), ...}; s.gates = append(s.gates, g); s.index(g); s.touch(g)`; the row reaches SQLite as a fixed statement at commit: `hp/store.go:545` `ex("INSERT OR REPLACE INTO gate VALUES(?,?,?,?,?,?,?,?,?)", g.Id, ...)`.
- Live evidence, `chk5/hp/acts-ndry-OlXe.log`: `HEAR run=5 who=builder what="coffee"` -> `SPAWN run=5 gate=1631 at=0 0 0` -> `LABEL run=5 "coffee" -> 1631`.

No SQL text is assembled by the run; no SQLite trigger fires; the Go kernel allocates the gate and later writes a fixed INSERT.

### A3. The hop -> a kernel loop in Go

- `hp/run.go:285-286`: `// step is one hop: blueprint 7.2, and nothing else.` / `func (b *Brain) step(r *Run) {`
- Shard match in Go maps, `hp/run.go:309-313`: `sh = at.Shards[[2]int{r.From, head.G}]; if sh == nil { sh = at.Shards[[2]int{-1, head.G}] }`
- Triggers are `trig` rows fired by Go, not SQLite triggers, `hp/run.go:350-364`: `for _, t := range at.Trigs { ... if (t.Arr == -1 && t.Head == -1) || (t.Arr == r.From && t.Head == head.G) { w := t.Worth * r.Worth; if w < b.val("VALUE.floor", 0.1) { continue } ... b.split(r, t.To, subject, t, w) } }`
- Then `r.From, r.At = at.Id, sh.Next; b.pass(r, sh.Next)` (run.go:367-371). Beat loop `hp/run.go:454-539`; life loop `hp/main.go:85-97`.
- DECISIONS.md:15: `Triggers live at gate level (arrival -1, head -1 = the gate's usual triggers) plus optional per-shard rows. The step fires both.`

### A4. What the Go kernel does

Far more than exec/route. It encodes, matches, decides the miss, filters and ranks, computes, places, and writes every brain table:
- Encoder: `hp/run.go:144-175` (`encode` splits text, lowercases, looks up `label`).
- Trigger worth cut: run.go:356 (quoted above).
- Scheduling by worth: `hp/run.go:482` `sort.SliceStable(live, func(i, j int) bool { return live[i].Worth > live[j].Worth })`; budget/slice/park `run.go:472-503`.
- About 100 physics modes in one `switch` (`hp/physics.go:94-1004`): `READ.*`, `WRITE.*` (shard/rel/run/row/mark/def/label/proc/value/trig/trust), `FIND.*`, `DELETE.*`, `MOVE`, `COMPARE` (physics.go:1082-1159, decides same/more/less, list diff, point distance), arithmetic (1042-1079), `reach` (1218-1246), `place` = the tug-of-war weighted mean (1249-1285: `p := [3]float64{sum[0] / w, ...}; s.movePoint(g, p)`).
- Loader/templating: `hp/lay.go:165-532` parses the lay notation; `layShards` (537-580) lays the shard rows a process string needs.
- Writes all tables: `hp/store.go:535-633` `commit()`.
- The build's own admissions: `hp/DECISIONS.md:81` `Lead: what still decides in Go, left on purpose and logged: find-row returns the oldest row of a kind ...; trigger worth = trigger x run, under the floor is cut ...; runs are stepped by worth with the told budget, slice, park-after and step limit ...; the sixth fires on a resting beat; the tug of war's weighted mean ...; the encoder's split and lowercase`. `hp/FINDINGS.md:49` `## 4. BREAKS: the kernel is 3,227 lines`; `hp/REPORT-TURN-TWO.md` §1: `Kernel (3,466 lines; finding 4 stays open)`. `hp/REPORT-TURN-ONE.md` §3.2: `The kernel is 3,292 lines ... Nothing in it chooses a word or an answer; the size is plumbing and addressing modes.`

### A5. Any path where a run assembles SQL that a mother pastes?

None. Every SQL statement in the kernel is a fixed literal with bound parameters: schema `store.go:171`, load SELECTs `store.go:196-262`, commit INSERT/DELETE `store.go:545-628`, `store.go:495` (`SELECT body FROM mem WHERE id=?`), `lay.go:27` (`SELECT k,v FROM kv WHERE k LIKE 'name:%'`). `grep -n "Exec(\|Query(\|QueryRow("` over `hp/*.go` returns only those five sites. The word "mother" appears nowhere in hp's docs (`grep -i mother *.md`: no hits).

### A6. Verdict (hp)

Fails all four. The brain is 12 fixed SQLite tables mirrored into Go RAM (not one table per neuron); a new neuron is a Go struct append inside a `SPAWN` switch case, written later by a fixed INSERT (not a run-assembled SQL string); the hop, trigger firing, encoder, miss decision, worth ranking, comparison, placement and every table write are in a 3.2-3.5k-line Go kernel; the only hand-laid "runs" are lay-notation strings interpreted by that kernel.

---

## B. hp2 (`~/neuron-build`, Go kernel, "turn one hp2" 2026-10-19)

### B1. Where the brain lives; one table per neuron?

Same shape as hp: one SQLite file, loaded into Go structs, written back as a queue of fixed statements.

- `hp2/store.go:3-5`: `// The store: the brain in RAM, its body in brain.db. Every write goes to RAM` / `// and queues one statement; the queue is committed at the end of each beat.` / `// Absent is no row: optional things live in their own tables.`
- Fixed schema `hp2/store.go:174-200`, 20 tables: `gate, phys, val, proc, name, label, shard, trig, usual, rel, sect, mem, msig, mbody, mout, tl, src, trust, core, meta`. A neuron is one `gate` row: `CREATE TABLE IF NOT EXISTS gate(g INTEGER PRIMARY KEY, x REAL ..., miss INTEGER NOT NULL, made INTEGER NOT NULL, rcpt INTEGER NOT NULL);` (store.go:175).
- DNA-like rows in shared tables: `shard(g, arr, head, next, ...)` (store.go:182), `trig(g, arr, head, out, worth)` (store.go:183), `usual(g, out, worth)` (store.go:184).
- Go mirror: `type Gate struct { P [3]float64; Miss, Made, Rcpt int64; Phys string; ... Proc []int64; Sh map[SK]*Shard; Usual []Trig; Out map[[2]int64]*Rel; Sect ...; Labels ... }` (store.go:118-130); `load()` store.go:235-301.
- KERNEL-SPEC.md:3: `The kernel (kernel/*.go) is the lead's. Builders write **lay files only**.`

Not one table per neuron; no SQLite triggers in the schema.

### B2. How a new neuron is created on an unknown word -> (c) outside code composes/executes

- The hop misses in Go and interrupts into the told miss process: `hp2/step.go:300-312` `// miss: like an interrupt. The run keeps the miss and goes to the gate's miss process.` ... `r.Ev, r.Tail = [3]Item{{G: r.At}, {G: r.From}, r.Rest[0]}, len(r.Rest); r.InMiss++; r.At, r.From = m, m; k.pass(r, r.Rest[0].D)`
- The told miss way reaches `SPAWN`: `hp2/lay/20-core.lay:16` `proc miss = MHEAD READ KIND READ`; `:33` `proc miss-word = mw-anchor f-later SPAWN LAST READ LABEL WRITE ITEM READ what-is-this SPLIT GAP TODO WRITE miss-back`; `hp2/lay/00-roots.lay:18` `gate SPAWN phys SPAWN`.
- SPAWN is Go: `hp2/step.go:655-656` `case "SPAWN": k.spawn(r)`; `hp2/rw.go:468-485` `func (k *K) spawn(r *Run) { p, ok := k.pop(r, 'p'); if !ok { k.calls(r, "born"); return } birth := k.newMem(...); g := k.newGate(p.P, r.Made, birth.ID); ... k.push(r, gv(g)) }`
- `hp2/store.go:437-445` `func (b *Brain) newGate(p [3]float64, made, rcpt int64) int64 { g := int64(len(b.G)); ... b.G = append(b.G, gt); b.gridAdd(g); b.q("INSERT INTO gate VALUES(?,?,?,?,?,?,?)", g, p[0], p[1], p[2], gt.Miss, made, rcpt); return g }`
- Live evidence (the build's own mail), `hp2/mail-to-hub/20261019-1521-first-word-wired-live.md`: `Word: impolite#14627 ... Wired: select str from proc where g=14627 -> 87898 35422, that is [#87898 mn-unhole].`

### B3. The hop -> a kernel loop in Go

- `hp2/step.go:180-181`: `// step is the whole hop.` / `func (k *K) step(r *Run) {`
- Shard lookup in a Go map, `step.go:215-221`: `if h.G >= 0 { s = k.G[r.At].Sh[SK{r.From, h.G}] }; if s == nil { k.miss(r, k.G[r.At].Miss); return }`
- Triggers fired in Go, `step.go:226-229`: `for _, t := range s.Out { k.split(r, t.Out, k.perform("split-worth", k.worth(r.At, t), r.Worth)) }`; `fire()` `step.go:257-266` for process-gate "usual" triggers.
- `KERNEL-SPEC.md:9-21` is the pseudocode of this loop (`shard = at's DNA[from, head]` / `no shard -> the miss way` ...). Beat: `hp2/step.go:418-481` `tick()`; life loop `hp2/main.go:80-97`.

### B4. What the Go kernel does

`hp2/step.go:3-4` claims `// Runs, the step, and the physics words. The step never chooses: the shard holds the way, and a miss goes to neuron code (the gate's miss process).` hp2 does push more choices back into lay (`hand()` step.go:325-334 hands candidate lists to told procs `which-head`, `which-label`, `which-gate`, `strongest`; `perform()` step.go:271-288 runs told worth formulas). But the kernel still:
- Encodes: `hp2/port.go:253-275` `func encode(s string) []Item` (split on space/symbol).
- Picks a single-label gate itself: `step.go:206-213` `if gs := k.labelGates(h.T); len(gs) == 1 { h.G = gs[0] } else if len(gs) > 1 { ... k.miss(r, k.nm("which-head")) }`.
- Ranks and schedules: `step.go:439` `sort.SliceStable(k.runs, func(i, j int) bool { return k.runs[i].Worth > k.runs[j].Worth })`; budget/slice/park `step.go:440-475`.
- Computes: `compare` step.go:602-623, `pmath`/`math` 547-600, `shapeOf` 400-416 (27-direction code), `lines()` sort by strength rw.go:56-69, `WRITE SHIFT` builds the then/now row rw.go:383-397, `writeMem` rw.go:440-456.
- CALLs a shell with a template: `rw.go:721` `cmd = strings.ReplaceAll(s.How, "%s", shq(arg.T))`; `hp2/port.go:208` `c := exec.CommandContext(ctx, "sh", "-c", cmd)`.
- Parses lay notation and lays shards by walking strings: `hp2/lay.go:68-148`, `walk` lay.go:272-305.
- Writes every table via `q()` (store.go:347, 437-639; rw.go:430, 500-501, 509).
- Adversary (same session): `hp2/ADVERSARY-FINDINGS.md:8` `## 1. Kernel is 2,507 lines ... [major]`; `:832` `### R2-8. Know-how still in Go that the brain cannot read or rewrite: which line is "strongest", which gate a word means, which label is said, which point is "near", what a truth shift is, how worth falls, when the sixth may run. Kernel 2,587 lines`. Mail 1347: `the kernel at 2,823 lines`. DECISIONS.md:94, :101, :130 record choices moved out of Go after rounds.
- Extra: the brain was given its own Go source and a swap path (`step.go:421-430`, mail 1435 `the brain can now read, change, build and switch to its own kernel`), i.e. the thinking medium is explicitly Go.

### B5. Any path where a run assembles SQL that a mother pastes?

None. SQL in the kernel is fixed literals: schema `store.go:207`, load `store.go:241-300`, every `b.q("INSERT ...")`/`UPDATE`/`DELETE` in store.go and rw.go, `main.go:141` (`DELETE FROM meta WHERE k='told_ended'`), `store.go:626-627` (`"DELETE FROM "+t+"=?"` over a fixed list of four table names). `grep -n "db\.Exec\|db\.Query"` -> store.go:207, 225, 611 only. No "mother" in any hp2 doc.

### B6. Verdict (hp2)

Fails all four. Same architecture as hp: 20 fixed tables in brain.db mirrored into Go, hop and trigger firing in Go `step()`, neuron creation by Go `spawn()`/`newGate()` with a fixed INSERT, no run-assembled SQL. It is better than hp at deferring choices to told lay strings (`hand`, `perform`, miss-as-interrupt), but the "mother" is a 2.5-2.8k-line Go kernel that encodes, ranks, compares, templates CALLs, and writes the brain.

---

## C. v2 (`neuron-v2-experimental-2026-10-20.tar.gz`, C executor + SQL programs)

### C1. Where the brain lives; one table per neuron?

- SQLite file: `install.sh:45` `"$STAGE/neuron" "$STAGE/brain.db" --init "$STAGE/seed.sql"`; `talk`/`say` wrappers run `"$HERE/neuron" "$HERE/brain.db" --talk|--say`.
- Fixed schema `schema.sql` (44 tables, 2 views; `seed.sql` contains 44 `CREATE TABLE`, 0 `CREATE TRIGGER`). A neuron is a `gate` row: `schema.sql:8` `CREATE TABLE gate(id INTEGER PRIMARY KEY, born INTEGER NOT NULL REFERENCES event(id), kind TEXT NOT NULL CHECK(kind IN ('process','symbol','sql-atom','learned','composition','unknown')));`
- DNA rows: `schema.sql:15` `CREATE TABLE dna(id INTEGER PRIMARY KEY, gate ..., arrival INTEGER REFERENCES gate(id), head INTEGER REFERENCES gate(id), head_mode TEXT ... CHECK(head_mode IN ('any','end','exact')), program INTEGER NOT NULL REFERENCES code(id), provenance ..., parameters TEXT ..., previous INTEGER REFERENCES dna(id));` plus `active_dna` (schema.sql:16). `docs/ARCHITECTURE.md:7`: `There is no duplicate next INTEGER per DNA row. The remaining process sequence already carries the continuation.`
- Triggers: `schema.sql:18` `CREATE TABLE excitation(id ..., dna INTEGER NOT NULL REFERENCES dna(id), target INTEGER NOT NULL REFERENCES gate(id), role TEXT NOT NULL, provenance ...)`. The C authorizer denies SQLite triggers on brain tables: `src/kernel.c:337-338` `if(action==SQLITE_DROP_TABLE||...||action==SQLITE_CREATE_TRIGGER){ if(!a||strncmp(a,"u_",2))return SQLITE_DENY; }`.
- Explicitly not one table per neuron: `docs/ARCHITECTURE.md:75` `A fixed set of tables stores many logical neurons, avoiding a separate SQLite B-tree per gate/definition.` Seed: 564 gates (same line).

### C2. How a new neuron is created on an unknown word -> (d) nothing for an unknown word; told commands create gates by SQL stored in DNA; `table NAME` is (a)-like

- An unknown word creates nothing. `input.dispatch` (docs/CODE-MAP.json gate 2; built from `tools/build_seed.py:50-56`): `UPDATE run SET result=json_object('state','UNKNOWN','uninterpreted_input',(SELECT body FROM input WHERE run=:run), 'supported_syntax',coalesce((SELECT usage FROM command WHERE atom=json_extract(:ctx,'$.args[0]')),'help'),'authority','no-meaning-invented') WHERE id=:run AND json_extract(:ctx,'$.entry') IS NULL;` README.md:7: `It accepts the explicit instructions below, not unrestricted English.`
- Gates are created only by told instructions whose program is SQL stored in the graph and executed by C:
  - `example NAME X Y`: `tools/build_seed.py:93-99` (`ensure_cap`, emitted into the graph) `INSERT INTO gate(born,kind) SELECT :origin,'learned' WHERE NOT EXISTS(SELECT 1 FROM capability WHERE name={name_id});`
  - `compose`: `build_seed.py:199` `INSERT INTO gate(born,kind) SELECT :origin,'composition' WHERE {ctx('valid')};`
  - `table NAME`: `build_seed.py:371, 380` `INSERT INTO gate(born,kind) SELECT :origin,'sql-atom' ...` / `INSERT INTO gate(born,kind) VALUES(:origin,'process');` then `INSERT INTO dna(...)`, `INSERT INTO active_dna(...)` (:382-383).
- Learning installs new DNA by SQL (`learn.install`, CODE-MAP gate 11): `INSERT INTO dna(gate,program,provenance,parameters,previous) SELECT c.gate,12,... ; DELETE FROM active_dna WHERE gate=...; INSERT INTO active_dna(...)`.

So the creating code is SQL text living in `code_atom` rows, run by the executor; but it is hand-written at build time by Python (`tools/build_seed.py:2` `Build-time only. Hand-lays the declared seed, never runs in the brain.`), and it fires on a fixed command grammar, not on an unknown word.

### C3. The hop -> a kernel loop in C over SQL rows

- `src/kernel.c:488-579` `static int step(void)`:
  - picks the run: `:490` `SELECT id,origin,coalesce(arrival,0),json_extract(rest,'$[0]'),coalesce(json_extract(rest,'$[1]'),0),depth FROM run WHERE state='ready' ORDER BY turn,id LIMIT 1`
  - picks the DNA: `:506` `SELECT d.id,d.program,d.parameters,(d.arrival IS NOT NULL)+(d.head_mode<>'any') AS specificity FROM active_dna a JOIN dna d ON d.id=a.dna WHERE a.gate=? AND (d.arrival IS NULL OR d.arrival=?) AND (d.head_mode='any' OR (d.head_mode='end' AND ?=0) OR (d.head_mode='exact' AND d.head=?)) ORDER BY specificity DESC,d.id`; `:513` `fault(id,"no applicable DNA; unknown is not a fabricated continuation")`; `:522` `fault(id,"ambiguous equally specific DNA")`
  - assembles the program string from atoms: `:371-386` `program()`: `SELECT a.text FROM code_atom ca JOIN spelling s ON s.gate=ca.gate JOIN atom a ON a.id=s.atom WHERE ca.code=? ORDER BY ca.pos` concatenated with `sqlite3_str_appendall`; hash-checked `:532-546`.
  - pops the head: `:548` `UPDATE run SET current=?,rest=json_remove(rest,'$[0]'),steps=steps+1,...`; traces `:552`; executes `:557` `execute(text,id,gate,dna,origin,arrival,head,params,&error)`.
  - fires triggers (excitations) itself: `:573` `INSERT INTO run(parent,root,origin,role,rest,pad,depth) SELECT r.id,r.root,r.origin,e.role,json_array(e.target),r.pad,r.depth+1 FROM excitation e JOIN run r ON r.id=? WHERE e.dna=?`
- `drain()` `:580-588` loops `step()` up to `STEP_CAP 12000`; no daemon (README.md:39 `No daemon continues work after the program exits.`).

Not a per-row SQLite trigger; a C loop that reads DNA rows and runs the stored SQL.

### C4. What the C kernel does

- Its own statement, `src/kernel.c:1-5`: `/* Neuron V2 physical executor. No vocabulary dispatch, inference, fitting, correction, belief, summarization, or command handlers live here. All of those (where implemented) are versioned graph programs in brain.db. This file implements SQL execution, lexical byte transport, scheduling, atom emission, immutable-evidence enforcement and bounded source I/O. */`
- Concretely in C: the encoder/lexer `lex()` `:102-174` (whitespace/word/quoted-string framing with byte offsets, registered as a SQL function `:345`); `sha256`, `finite_real`, `source_get` (libcurl, allowlisted hosts `:233-239`) host functions; the authorizer `:327-342`; run selection order and WAIT rule `:489-490`; DNA selection policy (specificity ranking, ambiguity fault) `:506-524`; hash verification; trace insert; excitation fork `:573`; fault handling `:466-487`; outbox printing `:589-597`; `--init`, `--say`, `--talk`, `--resume` transports.
- Not in C: command dispatch (`input.dispatch`), affine fit (`learn.fit`, CODE-MAP gate 9: `(SELECT (b.y-a.y)/(b.x-a.x) FROM example a,example b ...)`), install (`learn.install`), task choice (`work.choose`: `SELECT id FROM task WHERE state='pending' ORDER BY id LIMIT 1`), memory write (`run.end`). These are 51 told SQL programs (CODE-MAP.json: 51 entries; e.g. `learn.fit` 1122 atoms, `sql.table` 1113 atoms) written by `tools/build_seed.py` + `tools/seed_extensions.py` at build time. `docs/ARCHITECTURE.md:17`: `Build-time Python emits the seed. It has no runtime role.` `:15`: `Some told SQL programs are substantial, and the command grammar is explicit. Moving those programs into the database is a narrower achievement than a learned, meaning-grounded universal language.`
- Also, the only mutable brain tables are those not in the C `immutable[]` list `:30-32` (`"atom","label","run_receipt",...,"excitation"` are UPDATE/DELETE-denied in graph mode).

### C5. Any path where a run assembles SQL that the executor pastes?

Yes, one, and it is the general mechanism in miniature:
- Every DNA program is stored as an ordered atom sequence (`code_atom` -> `spelling` -> `atom.text`), concatenated by C `program()` (kernel.c:371-386) and executed by `execute()` (kernel.c:395-465). The kernel "pastes" whatever string the rows spell.
- `table NAME` composes a *new* string at run time: `tools/build_seed.py:366-385` (`sql.table`): fills the hole of the told template `'CREATE TABLE IDENTIFIER (id INTEGER PRIMARY KEY, value TEXT NOT NULL);'` (`build_seed.py:452`, stored in `sql_template` `:454`) with a new quoted-identifier atom (`INSERT INTO code_atom(code,pos,gate) SELECT ..., CASE WHEN ca.pos=t.hole THEN {identifier_gate} ELSE ca.gate END FROM sql_template t JOIN code_atom ca ON ca.code=t.code WHERE t.name='create-user-table'`), creates a `gate`+`dna`+`active_dna` for it, and prepends the generated gate to the run's remainder (`prepend(json_array(generated_gate, sql.verify))`), so the next `step()` concatenates and executes `CREATE TABLE "u_NAME" (...)`. `docs/ARCHITECTURE.md:53-61`: `table NAME uses a graph-stored template and shared SQL-atom references to construct a new executable program for: CREATE TABLE "u_NAME" (id INTEGER PRIMARY KEY, value TEXT NOT NULL); ... The template itself is told. This proves this particular compositional construction path, not autonomous discovery of arbitrary schemas or complete SQL competence.`
- Limits: one template, one fixed schema, `u_` prefix enforced by the authorizer (kernel.c:340); not triggered by an unknown word; the 50 other programs' SQL was typed by the builder in Python, not assembled by runs.

### C6. Verdict (v2)

Closest of the three to criteria 2 and 3: the executor only routes/traverses and pastes the SQL that rows spell (with a small selection policy: run order, DNA specificity, ambiguity fault, excitation fork, lexer in C); `table NAME` is a genuine run-assembled-SQL path. Fails criterion 1 (44 fixed tables, no per-neuron table, DNA has arrival/head but no "next", triggers are `excitation` rows forked by C) and criterion 4 (the brain's thinking is 51 hand-laid SQL programs emitted by Python at build time; an unknown word yields `UNKNOWN` and spawns nothing; learning is affine-only). The package says so itself: BUILD-STATUS.md:3 `Full requested outcome: NOT_DEMONSTRATED.`

---

## Compact table

| build | brain where | creation (a/b/c/d + cite) | hop (+ cite) | kernel does | run-assembled SQL path? | verdict |
|---|---|---|---|---|---|---|
| A hp (Go) | one `brain.db`, 12 fixed tables (`gate, shard, trig, ...` store.go:145-165) loaded into Go structs (store.go:3-4,187); 0 SQLite triggers; neuron = `gate` row, DNA = `shard(gate,arrival,head,next)` rows | (c) Go `SPAWN` case physics.go:756 -> `newGate` store.go:408 -> fixed `INSERT OR REPLACE INTO gate` at commit store.go:545; reached via told `miss-word: spawn ...` 20-memory.lay:73 after a Go miss run.go:315-345 | Go loop `step()` run.go:286; shard map lookup run.go:310; triggers fired by Go run.go:350-364; beat run.go:454 | encoder, shard match, miss, worth floor, worth sort, budget/park, ~100 physics ops incl. COMPARE/FIND/place weighted mean, lay parser + shard templating, writes all tables (3.2-3.5k lines; DECISIONS.md:81 lists "what still decides in Go") | none (only fixed SQL literals: store.go:171,196-262,495,545-628; lay.go:27) | fails 1-4 |
| B hp2 (Go) | one `brain.db`, 20 fixed tables (store.go:174-200) in Go structs, writes queued as fixed statements (store.go:3-5,347); neuron = `gate` row, DNA = `shard(g,arr,head,next)`, `trig`, `usual` | (c) Go `SPAWN` step.go:655 -> `spawn()` rw.go:468 -> `newGate` + `INSERT INTO gate` store.go:437-443; reached via told `miss-word = ... SPAWN ...` 20-core.lay:33 after Go `miss()` step.go:300-312 | Go loop `step()` step.go:181; `Sh[SK{from,head}]` step.go:217; triggers split by Go step.go:227, `fire()` step.go:259; KERNEL-SPEC.md:9-21 | encoder port.go:253; single-label pick step.go:207; worth sort step.go:439; park; compare/math/shapeOf; WRITE SHIFT, writeMem; CALL via `sh -c` port.go:208; lay walker lay.go:272; writes all tables; defers some choices to told procs via `hand()`/`perform()` (2.5-2.8k lines; adversary R2-8 ADVERSARY-FINDINGS.md:832) | none (fixed literals only; `db.Exec/Query` at store.go:207,225,611) | fails 1-4 (closer than hp on moving choices into lay) |
| C v2 (C + SQL) | `brain.db`, 44 fixed tables (schema.sql); `dna(gate,arrival,head,head_mode,program)` schema.sql:15, no `next` (ARCHITECTURE.md:7); triggers = `excitation` rows schema.sql:18; 0 SQLite triggers; "fixed set of tables stores many logical neurons" ARCHITECTURE.md:75 | (d) for an unknown word: `input.dispatch` returns `UNKNOWN`, no gate; told commands create gates via SQL stored in DNA programs (`ensure_cap` build_seed.py:95; `sql.table` :371,:380); `table NAME` is (a)-like: atoms -> `code_atom` -> C concatenates -> executes | C loop `step()` kernel.c:488: run `ORDER BY turn,id` :490, DNA by specificity :506, `program()` concatenation :371, `execute()` :557, excitation fork :573; `drain()` :580 | executes SQL, lexes input in C (:102), sha256/finite_real/source_get, authorizer, scheduling + DNA selection policy, hash check, trace, fork; no dispatch/fit/meaning in C (kernel.c:1-5) - those are 51 told SQL programs from build-time Python (build_seed.py:2) | YES, one: `table NAME` fills a told template hole and the executor runs the assembled `CREATE TABLE "u_NAME"` (build_seed.py:366-385; ARCHITECTURE.md:53-61); all other programs are hand-typed SQL | passes 2-3 in spirit (string from rows -> executor pastes; small policy in C), fails 1 and 4 |
