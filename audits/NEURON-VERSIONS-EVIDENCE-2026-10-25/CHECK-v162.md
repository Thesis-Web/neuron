# CHECK: Neuron 16.2 (`/home/exnulla/neuron-v16.2`) against the owner's four criteria

Read-only forensic check, 2026-10-25. Nothing in Downloads was modified. Work folder: `/tmp/claude-1000/-home-exnulla-neuron-v1/95237a7f-7d7c-47a3-a249-06f9202b6633/scratchpad/chk7/`.

## 0. What survives of 16.2, and where this evidence comes from

**The Downloads "review" folder holds no code, SQL or database.** `neuron-v16.2-review-20261013T114157Z-GtrCeC/` contains only four reports; the capture failed before any archive part was written:

- `FAILED.txt:1` — `INCOMPLETE: packaging exited with status 1. Do not treat these parts as a finished capture.`
- `READ-ME.txt:3` — `Source directory: /home/exnulla` (the script was pointed at the whole home dir, not at the 16.2 folder; `package-neuron-v16_2.sh:8` defaults to `PROJECT="${1:-/home/exnulla/neuron-v16.2}"`).
- `DIRECTORY-SIZES.txt:5,13,23,40,53,77,112,114,144,352` — the 16.2 tree as it stood on 2026-10-13: `4.2G neuron-v16.2`, `2.0G .../home` (the brain `home/cortex.db` + backups), `751M runs`, `60M audit-evidence`, `27M relay`, `21M teacher`, `4.9M l0`, `4.8M MAILBOX`, `2.8M experiments`, `16K native`.
- `package-neuron-v16_2.sh:92-94` streams `tar | gzip -1 | split`; `:17` writes FAILED.txt on any non-zero exit. No `.part-*`, `SHA256SUMS.txt`, `LARGEST-FILES.tsv` or `SYMLINKS.tsv` exists in the folder.

**The 16.2 directory no longer exists on this box** (`ls /home/exnulla/neuron-v16.2` → No such file). `/mnt/d/exnulla-archive/` is empty; `storm_run.sh:2` referred to `/mnt/d/exnulla-archive/neuron-archive-20261012/move.log`, which is gone. The owner said on 10-19 (owner words file line 4128): "in downloads I undeleted a copy of 16.2 I think, so you might be able to look at the code runs in there" — that copy is the failed capture above.

**Dating.** The name `neuron-v16.2` first appears in transcripts on 2026-09-30 (memory note `neuron_v16_2_rail.md:11`: "V16.2 was built from zero 2026-09-30 in /home/exnulla/neuron-v16.2"), not 10-08. It was rebuilt on a new bottom ("L0") on 2026-10-06 and ran until the capture attempt on 10-13. So "16.2" names two layers: the Python-host build (09-30 → 10-06) and the L0 build on top of the same `home/cortex.db` (10-06 → 10-13).

**Where the code below comes from.** Since the files are gone, their contents were recovered from tool results in session transcripts (Claude Code `~/.claude/projects/-home-exnulla/*.jsonl` + `-home-exnulla-neuron-v16-2-MAILBOX/*.jsonl`, Codex `~/.codex/sessions/**/*.jsonl`): 4,663 call/result pairs that name a 16.2 file, saved under `chk7/extract/pairs/` (raw) and `chk7/extract/pairs_dec/` (Codex JSON-escaped outputs decoded); the index is `chk7/extract/PAIRS.tsv`, the write/patch log is `chk7/extract/WRITES.tsv`, the path inventory (3,013 distinct 16.2 paths) is `chk7/inventory.txt`. Line numbers below are the original file's line numbers as shown by the capturing tool (Claude `Read` prints `cat -n`; for Codex `sed -n` captures the range is named).

The two cortex files were checked and do **not** describe 16.2 (`grep -c '16.2'` = 0 and `grep -c v16` = 0 in both `cortex_plan.html` and `cortex_slice01_erd.html`); not used.

---

## 1. Where the 16.2 brain lived and its schema

**Location:** `/home/exnulla/neuron-v16.2/home/cortex.db` (3,459 transcript mentions, the most of any 16.2 file). Entry script `home/talk.sh` was four lines (capture `pairs/2026-10-03T052221_claude_001592.txt`):

```
#!/bin/bash
# Say something to the living brain:  home/talk.sh "friday ?" "fast opposite ?"
cd "$(dirname "$0")/.." || exit 1
python3 talk.py home/cortex.db "$@"
```

**Schema: shared tables, not one table per neuron.** `substrate.py` (Claude `Write`, 2026-09-30T07:45:23Z, session e7a24cd1; capture `pairs/2026-09-30T074523_claude_002718.txt`) lines 2-5:

> `"""Neuron V16.2 substrate: storage, exact matching, transactions. No mathematics, no words.`
> `A gate is a row whose identity is one expression. Everything a gate holds is a DNA row inside it (table dna, column kind):`

and the DDL, `substrate.py:40-70` (`SCHEMA = """ ... """`):

```
CREATE TABLE IF NOT EXISTS event(id INTEGER PRIMARY KEY, raw TEXT NOT NULL, meta TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS gate(id INTEGER PRIMARY KEY, expr TEXT NOT NULL UNIQUE, shown TEXT NOT NULL,
  canon TEXT NOT NULL, born_event INTEGER NOT NULL, born_how TEXT NOT NULL, source TEXT);
CREATE TABLE IF NOT EXISTS form(id INTEGER PRIMARY KEY, form TEXT NOT NULL, gate_id INTEGER NOT NULL,
  root TEXT, from_event INTEGER NOT NULL, until_event INTEGER);
CREATE TABLE IF NOT EXISTS dna(id INTEGER PRIMARY KEY, gate_id INTEGER NOT NULL, kind TEXT NOT NULL,
  row_no INTEGER, key_gate INTEGER, arrival_gate INTEGER, dest_gate INTEGER, out_gate INTEGER,
  via INTEGER, shape TEXT, cells TEXT, rev INTEGER NOT NULL DEFAULT 1, depth INTEGER NOT NULL DEFAULT 0,
  born_event INTEGER NOT NULL, until_event INTEGER);
CREATE UNIQUE INDEX IF NOT EXISTS dna_hop ON dna(gate_id, key_gate)
  WHERE kind IN ('formula','fact') AND until_event IS NULL;
```

One `gate` row = one neuron (identity = a canonical math expression, `expr`); one `dna` table holds every neuron's rows, typed by `kind` (route / formula / fact / contract / occurrence / entry / mail / definition / selector / continuation / need / feedback, `substrate.py:7-19`). Words live in `form`. Across all 148 captured DDL dumps the table set is: `event, gate, form, dna, support, ref, selref, memref, memuse, memnode, timenode, structure, storage_interface, life, inbox, outbox, work, pending, proposal, hypothesis, candidate, line, trial, cursor, report` plus views `graph_entries, graph_formulas, graph_definitions, graph_routes`. The L0 bottom (`l0/l0.py`, 10-06 on) re-declares the same `event/gate/form/dna/...` tables (`l0.py` SCHEMA, capture `pairs_dec/2026-10-09T202903_codex_004556.txt`).

**Triggers: none.** Across the 4,663 captured results, `CREATE TRIGGER` occurs 0 times (raw and decoded); the only "triggers" named anywhere are SQLite `TEMP triggers` on a *reader's own connection* used by a change-watcher, and the word "trigger" in later L0 prose. The brain had no SQL trigger of its own.

**Row counts (dated; no whole-table gate/dna count was captured after 10-07):**
- 2026-09-30 evening: `453 forms, 492 lines` (`neuron_v16_2_rail.md:20`).
- 2026-10-01T06:14Z: `select count(*) from event` → `7718` (capture `pairs/2026-10-01T061457_claude_002012.txt`).
- 2026-10-04T20:50Z: `forms total 6658` (capture `pairs/2026-10-04T205037_claude_002704.txt`).
- 2026-10-07: gate ids had reached ~697,400 (`CYCLE 697396`, `tk_take 697394`); `30875` rows keyed by `lx_names` (captures `pairs_dec/2026-10-07T020657_codex_004623.txt`, `...020714_codex_004624.txt`); "noun 17,569 rows, adjective 6,065, verb 5,690; 42,732 includes-lines" and a `(+ 1)` number line to 11,000 (/neuron skill doc in `pairs_dec/2026-10-08T050855_codex_003101.txt`).
- 2026-10-08 23:34 CDT (the Relation Map, read from `main` = cortex.db): `names` 35,597; `edges` 314,181 ints = **104,727 relation triples** in 9 kinds (alike 62,882; is 11,987; opposite 10,240; stem 8,251; suffix 6,821; has 1,656; prefix 1,421; past 1,104; singular 365); 16,398 placed points (`chk7/map/data.json`; `index.html:130`: "Read-only SQL on main's living brain: lines W -wd_rel-> section -[B]-> R for nine relations ... Points: the location layer's adopted trials"). `data.json` is a *page export*, not a brain file; no 16.2 `.db` exists in Downloads.

---

## 2. How a new neuron / word was added

**Python, by direct row writes; never a run that assembled SQL for a router.**

`learn.py` (Claude `Write` 2026-09-30T07:50:45Z; capture `pairs/2026-09-30T075045_claude_002722.txt`) line 2: `"""Learning: the only place mathematics is done in V16.2. One lesson at a time.` Word placement, `learn.py:82-97`:

```
def place(sub, ctx, form: str, expr, event: int, source=None):
    """Put a word on the gate for expr. Returns (gate, report) or (None, conflict)."""
    k = canon.key(expr)
    existed = sub.gate_id(k)
    ...
    gid, _ = sub.add_gate(k, canon.shown(expr), canon.VERSION, event, "placed", source)
    sub.set_form(form, gid, event, canon.root(expr))
```

Which formula/place a new word gets was chosen by Python: `learn.py` `choose()`/`fits()` (~297-333) iterate a candidate library and write `INSERT INTO hypothesis(rel, formula, status, reason, event_id)` with `"chosen"`/`"rejected"`; `canon.py` solved coefficient families (`canon.solutions`, `canon.between`; README capture `pairs/2026-10-02T224836_codex_003219.txt`: "This is the mother doing the mathematics, as `choose()` already was").

Structural neurons were made at genesis by `alive.py:76-84` (`_genesis`): `for name, sym in substrate.STRUCT.items(): gid, _ = sub.add_gate(f"Symbol('{sym}')", sym, "symbol", ev, "structure")`.

After the 10-06 rebuild, words/bodies were added by **lesson files typed by the LLMs and loaded through `python3 l0.py teach <db> <file>`** (`l0.py` docstring, capture `pairs_dec/2026-10-09T202903_codex_004556.txt`): the file format is `word NAME` / `means NAME <stack words>` / `run NAME`, e.g. `l0/m4_text.lessons:27` `word tx_cfg`, `:96` `means tx_epoch_now PUSH tx_cfg PUSH tx_ep READ`, `:155` `means tx_step PUSH rt_cur GET PUSH rt_k GET READ PUSH rt_d LET PUSH tx_s_nohop PUSH rt_d GET IF tx_pk_hop CALL` (capture `pairs/2026-10-06T195503_claude_000955.txt`). `l0/LOAD_ORDER` lists the hand-written layers: `load wm3.img, load m1_sc4.img, teach m1_b.lessons, teach m2r3_walker.lessons, teach m4_text.lessons, teach m5_words.lessons, teach k6_quiet.lessons, teach lf_l0.lessons, teach hc_l0.lessons, teach sl_l0.lessons, teach m3r3_cycle.lessons, teach m6_keywords.lessons, teach m6_understand.lessons, teach who_l0.lessons, teach sv_l0.lessons` (capture `pairs/2026-10-07T011127_claude_000286.txt`).

The owner's own record of this on 10-05 (memory `feedback_neuron_engine_lane_scope.md:19-21`): "learned mostly means 'an agent wrote it in neuron language' <-- that is not fucking learning ... Partials count: 10,013 programs, brain-authored 0."

---

## 3. The hop / traversal

**A Python walker (09-30 → 10-06), then a Python/C stack interpreter (10-06 → 10-13). No trigger hop anywhere.**

`physics.py` (Claude `Write` 2026-09-30T08:56:13Z; capture `pairs/2026-09-30T085613_claude_002731.txt`) lines 2-9:

> `"""Runtime physics: activation hopping through learned structure. No mathematics, no words.`
> `A run is a string of gates. Standing at a gate, having arrived with a receipt, the next gate in the string is the key: the route row for (gate, arrival, key) names the next gate and the next receipt. The first time a step is taken in a context the row is laid from what the gate already holds for that key (a formula shard, a fact shard) or, with nothing there, the run enters the key's own gate.`

The step and the loop, `physics.py:52-65` and `:68-170`:

```
def _step(sub, cur: int, arrival: int, key: int, out, event: int, root: int, relations, strict: bool = True):
    r = sub.route(cur, arrival, key)
    if r is not None:
        return r
    s = sub.hop(cur, key)
    ...
    return sub.row(sub.add_route(cur, arrival, key, dest, out(), via, how, event))

def walk(sub, content: list[int], event: int, record: bool = True, inert: bool = False, ...):
    ...
    while frames:
        f = frames[-1]
        ...
        steps += 1
        if steps > LIMIT:
            w["interrupted"] = True
        ...
        r = _step(sub, w["cur"], w["receipt"], key, out, event, root, relations, strict=not inert)
```

with `LIMIT = 20000` (`physics.py:42`) and a direct `sub.db.execute("UPDATE dna SET dest_gate=? WHERE id=?", ...)` at `:117`. `substrate.hop` (`substrate.py:279-281`) is one `SELECT * FROM dna WHERE gate_id=? AND key_gate=? AND kind IN ('formula','fact') AND until_event IS NULL`. The heartbeat is `alive.py:144-173` (`cycle` / `_take`): `rep = self.learn.lesson(sub, self, ev)` (165), `_, gates, _ = encoder.encode(sub, raw)` (170), `physics.run(sub, gates, ...)` (172).

From 10-06 the walk was re-expressed as stack words in `l0/m2r3_walker.lessons` and `m4_text.lessons` (`tx_step` above), and the thing that *executes* those words is `l0/l0.py` — a Python interpreter with an optional C step loop (`import l0vm as NATIVE`): `l0.py` docstring: `"""L0 rev 3: the bottom of the neuron computer. Physics only: no words, no choices. ... What this file does: each tick it runs the stored body of the role CYCLE and carries out the primitives that body names.`; `STEP_LIMIT = 5_000_000` (`l0.py:44`); `PRIMITIVES = ("READ","LINK","END","NEW","FIND","UPTICK","PUSH","LET","GET","EQ","IF","CALL","AGAIN","IN","OUT","CLOCK","FORGET")`; `def run(self, gate, stack)` at `l0.py:828` (`while frames: ... k = body[i] ... name = op.get(k) ... elif name == "PUSH": ...`), `def tick(self)` at `:942` (`"""One tick: CYCLE's body runs inside one transaction ... A tick that wrote nothing is rolled back whole"""`; `self.db.execute("BEGIN IMMEDIATE") ... stack = self.run(cycle, [])`), `def live(db)` at `:1098` (captures `pairs_dec/2026-10-08T050905_codex_003102.txt`, `pairs_dec/2026-10-07T085444_codex_003165.txt`).

---

## 4. Outside code and what it decided

All of it LLM-authored. `chk7/extract/WRITES.tsv`: the first writes are Claude `Write` calls on 2026-09-30T07:45-08:06Z creating `canon.py, encoder.py, physics.py, learn.py, alive.py, teacher/formulas.json, teacher/curriculum_16_2.json, experiment.py, test_v16_2.py, README.md`; in total 114 Claude `Write`/`Edit` events and 1,042 Codex shell patch/write commands touched 16.2 paths (most-written: `l0/l0.py` 38, `README.md` 28, `physics.py` 23, `learn.py` 21, `talk.py` 12, `substrate.py` 11, `alive.py` 11, `instructions.py` 10).

| File (lines, 09-30 Write unless noted) | What it decided |
|---|---|
| `substrate.py` (482) | storage, gate identity by canonical expression, receipt gate = `g1*M + g2*M**2 ...` (`receipt()` :322-334), every `SELECT`/`INSERT` on `dna`/`gate`/`form` |
| `physics.py` (328; 33,797 bytes by 09-30 18:15) | the walker: which row is the next hop, laying route rows, excursions `( )`, `again`, step limit, when a run "stops on a need" |
| `learn.py` (650) | word placement (`place`), formula choice (`choose`/`fits`), definitions (`write_def`), selectors, work queue (`work`/`do_work`), proposals, relocation (`merge`/`relocate`), lesson parsing (`lesson_relation/definition/means/name/answer`) |
| `canon.py` | the mathematics: `apply`, `inverse`, `between`, `solutions`, 16-formula library + 240 enumerated (`neuron_v16_2_rail.md:21-22`) |
| `encoder.py` | tokenizing (`tokens()` :24 regex), meaning choice when a word has several gates (`_resolve` :40-59: "a word with several meanings is taken in the meaning that stands on one of them"), clock forms, decode |
| `alive.py` (235) | the life loop, genesis gates, clock sense, inbox take, calling learn then physics, mailbox |
| `instructions.py` (Codex, 09-30) | 31 stack opcodes (`OPS = ('PUSH','DUP',...,'QUERY','INSERT','ASSEMBLE',...)`), the VM that ran 43 supplied ALL-CAPS programs (`teacher/compiler_runs.json`, `structural_runs.json`) |
| `talk.py`, `grow.py`, `structure.py`, `migrate_graph.py`, `experiment.py`, `test_v16_2.py` | CLI, teaching files, installing programs, migrations, tests |
| `native/neuronvm.c` (10-05), `l0vm.c` (10-06) | C step loops for the opcode VM and the L0 bottom |
| `l0/l0.py` (≥1,098 lines, 10-06 →) | the tick, the primitive interpreter, interning/hashing (`intern`, `_gate`), working-memory rules, rollback on fault, step/depth limits, `teach`/`say` terminals |
| `l0/*.lessons` (15 files + 2 images) | the "neuron code" — written by LLMs in text files and loaded by `l0.py teach` |

The 16.2 README's own list (capture `pairs_dec/2026-10-07T183531_codex_003144.txt`, section "Graph-owned writing and clock links"): "**Remaining Python:** clock-prefix construction, selecting the previous time node, starting the graph programs, the relink scan, occurrence/entry allocation and the same-run continuation heuristic; meaning selection; formula search; definition inference; feedback/generalization; relocation policy; work scheduling." Its START_HERE (10-02, capture `pairs/2026-10-03T052221_claude_001592.txt`): "Still decided by the host (the mother) ... Formula generation/search/fit/revision, meaning selection, definition inference, feedback/generalization, semantic relocation acceptance, scheduling/propagation, and the occurrence → timeline → output continuation. Supplied, not learned: 43 ALL-CAPS graph programs".

"Mother" in 16.2 meant this whole Python host, and the owner's order of 10-06 (memory `neuron_mother_disconnected_20261006.md:8,12,16`): owner 214 "get rid of the fucking mother ... disconnect the mother code completely ... then you can fucking do it correctly for the first time... in neuron code"; done by commenting out `alive.py, encoder.py, instructions.py, learn.py, migrate_graph.py, physics.py, structure.py, substrate.py, talk.py, and native/neuronvm.c`; "the owner sees the mother still running the brain: it encoded input, decided unheard/conclude, scheduled thinking and executed everything. The neuron code was never in control."

---

## 5. "Physics" in 16.2, how much, and the owner's remark

In the owner's sense (hand-laid SQL that acts inside SQLite): **none beyond DDL.** The only hand-laid SQL was the `CREATE TABLE/INDEX/VIEW` set in `substrate.SCHEMA` and `l0.SCHEMA` (~25 tables, 4 views); every action (hop, lay, choose, encode, tick, commit/rollback) was a Python or C statement issuing SELECT/INSERT/UPDATE. 0 triggers.

In 16.2's own vocabulary "physics" meant the host's runtime code: `physics.py` (the walker, 328 lines on 09-30, ~34 KB by evening) and, from 10-06, the L0 "bottom" that the owner approved as the minimal primitive set (memory `feedback_neuron_own_kernel_minimal_physics.md:7,13`: owner 215 "if for now it has to have a set of primitives that wraps it. Physics.. then ok.. but that's it... nothing else"; owner 216 "that sounds like a list of primitives, and physics... those are apporved... finally"): 17 primitives + ports + tick, in `l0.py` (≥1,098 lines) + `l0vm.c`.

The remark "16.2 had almost not physics" (owner 380, 2026-10-16 08:27 UTC; owner words file line 1947; memory `feedback_neuron_brain_writes_all_code_380.md:11`): "from this point on you never write py, or sql or sh code.... if it has to be written then neuron has to write it.. but we already proved that neuron can write all of it,, 16.2 had almost not physics..." Two readings, both supported:
- (a) the L0 reading: the hand-laid bottom was deliberately tiny (17 primitives) and everything above it — walker, text, words, cycle, sleep, who, save — was "neuron code" (`l0/*.lessons`, 15 layers). This is the sense he uses it in: proof that the brain's layer can hold all behaviour.
- (b) the SQLite reading: nothing in the database acted on its own (no triggers, no SQL assembled by runs), so almost nothing was "physics" in the 10-16-onward sense either.
What 16.2 did NOT prove: that the brain *wrote* that neuron code. Every `.lessons` line was typed by an LLM and loaded with `l0.py teach`; the same memory note says so (`...380.md:15`: "V16.2's walker and layers were our code, not the brain's"; `feedback_neuron_backpop_sleep_belief_246.md:17-18`, owner 246: "the LLM writes the neuron code, but in the end the brain will build it").

Other owner statements about 16.2 (all in `NEURON-OWNER-WORDS-ALL-SESSIONS-2026-09-16-to-10-25.md`): line 1560 (10-08) "start over .... using 16.2 as a guide line"; 1718 (10-16) "Only the mother can do this... hmm you told me that wasn't true in 16.2"; 1821 "maybe the way there were done in 16.2 is more correct maybe not"; 2909 (10-21) "much of 16 version was built before we understood triggers, and/or how the sql write process looked and worked"; 3659 (10-17) "it took about 200 million tokens to get there all laid by llms... and it cannot learn"; 4128 (10-19) "before with zero py outside we were able to make runs through neurons that get, read, write, copy, move data from one run to another ... I am assuming they were built incorrect". Also `NEURON-NOW-Interview-2026-10-18.md:212`: "The problem is the farthest you ever got was 16.2, and it was completely wrong. But it had belief, and it had all these things in it, but it was built wrong, because you never started it correctly."

---

## 6. Verdict against the four criteria

| Criterion (owner's words) | 16.2 | Evidence |
|---|---|---|
| prompt → encoder → brain; brain = SQLite, one table per neuron with DNA rows + triggers | **Fails on form.** Encoder = `encoder.py` (Python) then `lx_*` lessons; brain = shared `gate`/`dna`/`form` tables, 0 triggers | `substrate.py:40-70`; 0 × `CREATE TRIGGER` in 4,663 captures |
| a trigger cannot create; a run assembles an SQL string, mother pastes it | **Fails.** No run ever produced SQL text; Python (`physics._step` → `sub.add_route`, `learn.place` → `sub.add_gate`) and later `l0.py` wrote rows directly with `db.execute` | `physics.py:52-65,117`; `learn.py:82-97`; `l0.py:942-` |
| mother = router + traverser only | **Fails.** "Mother" = the whole Python host, which encoded, chose meanings, fit formulas, scheduled and executed (owner 214 on 10-06 ordered it disconnected for exactly this); the L0 bottom still interprets, hashes, limits and rolls back | README "Remaining Python"; `neuron_mother_disconnected_20261006.md:16` |
| only table-maker / hop / trigger hand-laid; all else built by typed runs | **Fails.** Everything hand-laid by LLM tool calls (114 Claude writes, 1,042 Codex patches); lessons typed in files and loaded by `l0.py teach`; "10,013 programs, brain-authored 0" | `WRITES.tsv`; `LOAD_ORDER`; `feedback_neuron_engine_lane_scope.md:21` |

One line: 16.2 was an LLM-written Python/C host over shared SQLite tables (`gate`/`dna`/`form`, no triggers, no run-assembled SQL) whose "neuron code" layers were typed lesson files, so it meets none of the four criteria; what it did show — and what the owner's "almost not physics" points at — is that a ~17-primitive bottom can carry all behaviour in stored bodies, which is a different claim from the brain writing them.

## Appendix: files produced in chk7/
- `CHECK-v162.md` (this file); `inventory.py` + `inventory.txt` (3,013 16.2 paths with mention counts and first-seen dates); `extract.py` + `extract/` (`PAIRS.tsv`, `WRITES.tsv`, `LATEST.tsv`, `pairs/`, `pairs_dec/`); `decode.py`; `map/` (`index.html`, `data.json` from `Neuron Relation Map.zip`, nothing run).
