# Neuron V12 — builder's sheet

Owner: James Huson. Written 2026-09-26. This sheet is handed, unchanged, to two independent builders. Their builds
will be diffed against each other and against this sheet. You are one of those builders. You have not seen the
conversation that produced this sheet and you do not need to; everything you need is here. Where this sheet is
silent, do not invent — leave a hook and write the question in `OPEN_QUESTIONS.md`.

`plan.json` ships beside this sheet. It holds the stage plan, the sheet schemas, the voice levels and the
born-with state as data. The sheet and the JSON say the same things; if they ever disagree, the JSON wins and you
report the line.

## 0. Tags

| tag | meaning | you |
|---|---|---|
| **BUILT** | exists in neuron-v11 (the reference archive, if provided) | reproduce it exactly; its regressions must stay green |
| **DESIGN** | the owner stated it | build exactly as stated; do not extend |
| **PROPOSED** | a mechanism suggested to the owner, not yet ruled on | build it only where a DESIGN item cannot run without it; say so in a comment and in `PROPOSED_USED.md` |
| **OPEN** | undecided | do not build; leave a hook and a named question |

Untagged sentences are PROPOSED unless they quote the owner or v11.

## 1. What this is

A structure born with one neuron, six blank sheets, four signals, the idea rule, the constructor principle and
the born-with heads listed in `plan.json`, taught by a separate teacher program, with no language model anywhere
in either. The structure is code you write once and
never change. Everything the student becomes is data it writes into that structure — rows, laws, DNA — mostly by
itself, after watching the teacher do it first.

In v11 a curriculum pushed laws straight into the organism and the organism replied in English from turn one.
In V12 the student cannot speak at birth. DESIGN (owner's words, condensed): it has four signals. It earns each level of voice by solving something the
teacher does not help with. It learns by observing the teacher write into its senses, then doing it itself, then
being corrected. It will be wrong, and its wrong answers are kept, because a student that only ever holds right
answers cannot learn from a mistake.

Learned outcome the owner wants from V12: roughly 80 to 128 turns of *learned* content, reaching probability and
statistics, at the cost of as many teacher turns as it takes (DESIGN) (500–600 is acceptable; `plan.json` caps the sum at
600). Every one of the machine's cores is used (DESIGN).

## 2. Vocabulary

- **neuron** — an exact normal-form term with a stable id. `0` is neuron 1.
- **gate** — a neuron's input or output. A gate has a key (the expression that arrives or leaves) and a global
  number. The expression *is* the gate's location in the graph (DESIGN: "the gate expressions are the graph locations").
  That the inverse of gate `x+1` is found through its arrival forms is PROPOSED, built on v11's inverse binding.
- **DNA row (shard)** — `(gate, remainder) → (out gate, out remainder, kind, steps, laws, lesson, uses)`, with one
  global shard number (DESIGN). A neuron's DNA is the set of rows keyed by it.
- **arrival form** — every expression that ever resolved to a neuron's identity, kept at the neuron.
- **watch** — a stuck terminal records the neurons it consulted; when one changes, only the watchers are re-examined.
- **law** — a rewrite rule `lhs -> rhs` with variables. Kinds: `taught`, `proved`, `confirmed`, `believed`.
- **sheet** — one of six tables, one row per event, that the student's senses are. Teacher and student both write
  rows. The structure executes a row's `APPLY`.
- **observer** — the student's reader of sheets. Its input each turn is the set of cells that changed (DESIGN).
- **voice** — the student's only output channel (DESIGN). Levels (the count of six is PROPOSED; the owner said "a little,
  more, a lot", each unlocked by a harder math problem the teacher does not help with); born at level 0.
- **receipt** — the numbered string of a run: neuron#, in-gate#, shard#, out-gate#, repeated until out == in.
- **structure** — code. Locked after birth (DESIGN). Hash-checked (PROPOSED).
- **learned** — data. Rows, laws, DNA, neurons. Never edited by hand after birth.

## 3. Structure (locked)

Everything in this section is code you write. After the student is born, a test asserts the hashes of these
modules do not change for the rest of the run. Nothing in section 3 may be edited to make a stage pass.

### 3.1 Terms and identity (BUILT)

- Terms: `num 0`, `sym name`, `var name`, `app head args...`.
- Numbers are unary at birth: `1` is `S(0)`, `2` is `S(S(0))`. `P` is predecessor.
- `identity_of: term → neuron id`. Content addressing: an arriving term *is* its address. No search.
- `memo: expression → neuron` for every expression ever resolved.
- Storage id is the older on merge.
- Canonical form is a string; equality is string equality. `num` holds one digit; numerals are S-chains after encoding.
- Born-with heads in v11 also include `cons`/`nil` (sequences), `isa`/`said` (fact heads) and `true`/`false`
  (`brain.py:33–36, :71`). Whether V12 is born with them or must earn them is OPEN (owner: the structure is capable
  of all language, but the student has to learn to turn it on).

### 3.2 DNA, forms, watches (BUILT)

- `dna[(gate, remainder)] = [out_gate, out_remainder, kind, steps, laws, lesson, uses]`, kinds
  `birth | continuation | reduction | memo | reuse`.
- DESIGN, new in V12: neuron ids, gate numbers and shard numbers are three global counters (v11 numbers neurons
  only; gates are neuron ids and DNA rows have no sequence).
- `forms[neuron]` = arrival forms; a merged neuron's old term becomes a form of the survivor.
- Inverse binding: a law variable may bind through arrival forms of the identity it matches (`sub(9,6)` answers
  because 9 was reached as `add(3,6)`).
- `watch_forms`, `watch_child`: terminals watch what they consulted. New laws and new forms re-examine watchers
  only. Nothing global is ever rescanned.
- Merge (BUILT, one fix DESIGN): DNA rows, forms, watches and visits move to the survivor; a `continuation` row is
  written from the old term to the new identity; the old id keeps `merged_into`. Fix: when the survivor already
  holds a row with the same remainder key, keep both — mark the older `superseded_by` — never drop one.

### 3.3 Reduce (BUILT)

Leftmost-innermost pending subterm; a law applies when it matches at the root of that subterm, its domains hold,
and (if ordered) the result is strictly smaller under the law's order. Incremental pending search. Size brake at
depth 4,000 reported as `too large for me`, never a crash. Step cap 200,000 reported as `my laws loop on this`.
When no law applies, the subterm is a new terminal neuron.

Parallel: reductions run in waves; N worker processes reduce against the wave-start snapshot and the parent
commits in canonical order. N = every logical core (`os.cpu_count()`) by default on every entry point (v11's
mailbox path had regressed to 1 — do not repeat that). One worker and N workers build byte-identical organisms; this
is a test.

### 3.4 Induction and proof (BUILT)

- Idea rule: when several arrival forms meet at one identity, the varying values become variables and the
  equation is a conjecture. Conjectures are proposed, never installed by this rule.
- A conjecture is judged only after every variable has taken two distinct values.
- Proof by the constructor principle: a claim about all states of a sort holds if it holds at the base and
  survives every declared constructor of that sort (numbers over 0 with S and P; sequences over nil with cons).
- Installed as `proved:n` only by proof. Teacher `yes` installs as `confirmed:n`, never as proved.
- NEW (PROPOSED mechanism for the owner's DESIGN that wrong beliefs are kept, see §4.3): the student may install
  its own conjecture as `believed:n` with lower priority than every taught or proved law. Beliefs are kept when
  refuted; they are marked, not deleted.

### 3.5 Memory tiers (BUILT)

active (touched within 3 turns) / persistent (5 visits, or named by a law) / compressed (arrival forms leave the
live index for a cold store after 6 cold turns; identity, DNA and watches stay). Touching a cold neuron warms it.
Nothing is deleted, ever.

### 3.6 The six sheets (DESIGN; columns PROPOSED)

Six tables, one row per event, in one SQL database (SQLite with WAL is acceptable for V12; the schema is what
matters). Every row has `turn`, `seq` (global), `who ∈ {teacher, student, structure}`, and the sheet's columns
from `plan.json`:

| sheet | question | columns |
|---|---|---|
| hearing | what was said, by whom | WHO · KIND · SAID · APPLY |
| sight | where in the structure | ENTERED AT · BORN · TOUCHED · MERGED |
| touch | how much contact | STEPS · SECONDS · LANES · BRAKES |
| smell | with what, using what | LAWS USED · LESSON · RECEIPT |
| taste | to what effect | STATUS · DNA+ · PROVED · RIGHT/WRONG |
| internal | why | EVENT · CAUSE · EXPECTED · QUESTION |

Rules:
- DESIGN: the senses are the only way in. Nothing reaches the organism except through a sheet row. The teacher
  does not call the organism; the teacher writes a row. PROPOSED: only hearing rows carry `APPLY`.
- PROPOSED: `APPLY` on a hearing row is the mechanism by which a cell reaches DNA. `APPLY ∈ {none, install, ask, prove,
  observe, define, fact, say, yes, no}`. The structure executes it and writes the consequences as rows on the other
  five sheets with `who = structure`. A hearing row with `APPLY = none` is only evidence — it changes no neuron.
- PROPOSED: `WHO` on the hearing row is whoever wrote it. At S1 the teacher writes first; the student's garbage rows follow. The student may write hearing rows
  with `APPLY` from the moment it can (§4.2); the structure records them with `who = student`.
- PROPOSED: `RIGHT/WRONG` on taste is written only by the teacher (praise or correction), never by the structure, never by
  the student.
- PROPOSED: `CAUSE` on internal is written by whoever applied the row (their `seq`) — or is NULL. A NULL cause is what
  generates a `why` (§3.8).
- PROPOSED: TOUCHED counts states re-examined by a law, not only states whose `last_turn` moved (v11 under-reported this).
- DESIGN: sheets are append-only (nothing is deleted).

### 3.7 The observer (DESIGN; loop PROPOSED)

Each turn, after the structure has applied every row with `APPLY`, the student's observer receives
`SELECT * FROM cells WHERE turn = t` across the six sheets — the change-set. From the change-set it may: (a) form conjectures by the idea rule over rows that co-occurred; (b) write
its own hearing rows (a `me do`); (c) emit a voice signal or utterance at its current level; (d) leave an
obligation on the internal sheet. Whether the student may also read its own DNA directly is OPEN (owner:
the student is the organism plus its observer; the observer sees only sheets).

### 3.8 Obligations and why (BUILT order; PROPOSED insertions)

End of every turn, the smallest open obligation becomes the student's output at its voice level. BUILT order:
contradiction → unknown word / unknown op → best unproved conjecture. PROPOSED insertions: refuted expectation
after contradiction; change with NULL cause after that. A pending obligation is re-validated every turn and
withdrawn with the reason when the graph settles it (BUILT). How an obligation maps to a level-0..2 emission
(which signal, which pointer) is PROPOSED, keeping the owner's meanings: smile → no open obligation; cry → an
open desire nothing has addressed; crying → the first teacher row that addressed it was not what was desired (a
refuted expectation, or a row that contradicts a belief); screaming → a second teacher row addressed it and it is
still open; at level 1 the pointer is the offending cell. PROPOSED recursion stop: a `why` is settled when its cause chain reaches a law, a stored fact, or a
teacher row; otherwise it waits in the queue at its priority. PROPOSED: the queue is budgeted; ten whys never outrank one
contradiction.

### 3.9 Voice (DESIGN; the specific gates PROPOSED)

Output channel. Level 0 at birth: `smile`, `cry`, `crying`, `screaming` (meanings in `plan.json`). Each higher
level is unlocked by an event the teacher does not assist with, checked by the structure, never granted by the
teacher:

| level | can emit | unlocked when |
|---|---|---|
| 0 signals | the four signals | born |
| 1 point | a cell id or neuron id | the change-set contains a cell the student wrote itself |
| 2 echo | a stored expression, verbatim | the student applies a row itself and the change matches a teacher demonstration of the same kind |
| 3 answer | a computed value with its receipt | first law proved by induction, unaided |
| 4 explain | a cause chain | a `why` answered from the receipt, unaided |
| 5 speak | sentences (cons chains) | a word gate gets a DNA path to a numeric gate, written by the student |

(The gates are PROPOSED; the owner's constraint is that each unlock is a harder problem solved unaided, that the
teacher never helps with it, and that voice grows "a little, more, a lot".)

PROPOSED: below its level, the student's attempt to emit is recorded on the hearing sheet as a `say` row with
`who = student` and is not delivered to the teacher. The teacher sees only what the level allows.

### 3.10 Receipt (DESIGN: every neuron, gate and shard is numbered and the numbers string into the receipt of the
run; the alternation grammar below is PROPOSED, decoded from the owner's sketch)

Every resolved arrival stores `receipt = [i, s, o, i, s, o, ...]` of global numbers — in-gate, shard, out-gate,
repeated, ending the first time out == in (each out-gate is the next hop's in-gate, so it is stored once). The
neuron number is the gate's owner; it is rendered, not stored: `n1·i0·s1·o1 · n2·i1·s3·o1` is the sketch's run 2,
stored as `[0, 1, 1, 3, 1]`.
The receipt is the run's key. `why EXPR` walks it. The RECEIPT column on smell holds it.

### 3.11 Teacher (DESIGN; grading PROPOSED)

A separate process. A scripted chat bot with branching, no model. It:
- writes hearing rows (`SAID`, `KIND`, `APPLY`), always in front of the student (the student's next change-set
  contains the row and its consequences);
- reads the student's voice output and the taste/internal sheets;
- asks, after a demonstration, who / what / when / where / how / why / source / with what / using what / to what
  effect — whichever apply — as hearing rows with `APPLY = ask`;
- asks "can you do it yourself" and waits for a student-written hearing row;
- writes RIGHT/WRONG on taste: praise on a match, a correction row on a mismatch (a hint, a re-demonstration, a
  different route — never the answer as a fact);
- re-teaches a different way when the student is wrong (PROPOSED trigger: wrong twice the same way); moves on
  when the stage's `expect` list is met (PROPOSED);
- PROPOSED: stops a stage at `teacher_turns_max` and writes `STAGE_STUCK.md` with the change-sets of the last
  five turns.

The teacher never touches DNA, never edits a sheet row, never grants a voice level, and does not script the
student's answers.

## 4. Learned (mutable, never hand-edited)

### 4.1 What the student may change
Rows it writes; laws it installs (`believed`); DNA rows the structure writes because of its applies; its voice
level (earned); relations rows in later stages (OPEN in V12).

### 4.2 "Me do" (DESIGN: observe, then do, then be corrected; garbage kept)
From S1 on, the student may write hearing rows with `APPLY`. Its first ones are expected to be garbage — a
constructor applied to a sentence, an ill-formed term. The structure records them with `who = student`,
executes what is executable, and (PROPOSED) refuses what is not as a taste row with STATUS `refused: <reason>`;
the teacher grades. Garbage is kept. Nothing is cleaned up. (v11 installs variable-free laws such as
`neg(0) -> 0`; a base case is not garbage.)

### 4.3 Mistakes (DESIGN: wrong beliefs are kept so the contrast can be reasoned about; the `believed` /
`refuted` / `episode` mechanism is PROPOSED)
The student may install a conjecture as `believed:n` (lower priority than taught and proved). A belief that is
contradicted by a teacher row, a proof, or its own cases is marked `refuted` with the refuting `seq`, kept, and
an `episode` row is written: `(goal, plan_receipt, outcome, valence)` with valence from the teacher's RIGHT/WRONG.
On a later miss, episodes whose receipt shares a prefix with the current one are consulted (PROPOSED read path).
Contrast is the point (owner): a wrong `2+2` next to a right one, both with receipts.

## 5. Curriculum (S1–S4 and S10 are what v11 taught, BUILT; S5–S9 are PROPOSED toward the owner's target of
reasoning maths, statistics and probabilities; the learned-turn budget of 80–128 is DESIGN)

Stages S0–S10 are in `plan.json` with `learned_turns`, `teacher_turns_max`, what the teacher does, what the
student is expected to do, the `expect` list (the gate to the next stage), and the voice level expected at the
end. Summary:

| stage | content | learned turns | voice by end |
|---|---|---|---|
| S0 birth | 0, six blank sheets, four signals | 0 | 0 |
| S1 constructors | S, P | 1–4 | 1 |
| S2 addition | five laws; the student proves lemmas, left zero, commutativity | 5–16 | 2 |
| S3 negation, subtraction | neg, sub; why negative | 17–24 | 3 |
| S4 multiplication, powers | mul, pow; 2^10 by unary; "why did you gain 968 neurons" | 25–34 | 4 |
| S5 positional notation | digits, carry, revisit; 100*100 | 35–44 | 4 |
| S6 division, gcd, fractions | v7 numeric closure | 45–56 | 4 |
| S7 order, logic, conditionals | lt/eq/gt, and/or/not, if | 57–68 | 4 |
| S8 counting, sets, ratio | lists, length, member, count-if, ratio in lowest terms | 69–84 | 4 |
| S9 probability, statistics | sum, mean, frequency, P(event) = count-if/length; EXPECTED vs outcome | 85–104 | 4 |
| S10 words as gates | sentences, isa; a word joins a number by a student-written row | 105–128 | 5 |

S1–S4 and S10's language part are what v11 did in 51 turns; their measured turn ranges are in `plan.json`
(`v11_turns`). The exact laws for S5–S9 are PROPOSED (S5–S6 from v5–v7's own laws; S7–S9 the simplest
definitions that keep everything a rewrite rule). A "learned turn" (PROPOSED definition) is a turn whose
change-set contains a row the student wrote, or an answer it gave; S1's learned turns are the teacher's
demonstrations the student observed.

PROPOSED: sessions are files: `sessions/S0.txt … S10.txt`, one teacher line per turn, with branch markers for re-teach and
correction. The teacher program reads them; the student never does.

## 6. Run configuration (PROPOSED except the lane count, which is DESIGN: all cores)

- Lanes: `os.cpu_count()` on every entry point; recorded on the touch sheet as LANES each turn.
- Store: one SQL database file per student home (`home/student.db`), six sheet tables plus the thirteen organism
  tables (`neurons, dna, forms, memo, arrivals, laws, watches, lessons, conjectures, induced, words, definitions,
  contradictions`) plus `episodes`, `obligations`, `voice`. The pickle is retired. The state signature is computed
  from the tables alone.
- Two processes: `teacher` and `student`, communicating only through the database. Neither imports the other.
- `report.py` prints every number that appears in `RESULTS_V12.md`. No number in that file is typed by hand.
- Journal: one JSON line per turn with the change-set summary, the voice output, the stage, the signature.

## 7. Acceptance (all, or it is not V12)

1. Structure hashes unchanged from S0 through the end of the run (test).
2. Physics regressions from v11, if the archive is provided: genesis `a1d27ba6…`, first-day replay
   `f521c5dc…` through the old mailbox path kept as a regression harness, `./validate.sh` green. If the archive is
   not provided, the physics tests in §3 must pass on your own implementation.
3. One lane and N lanes produce byte-identical organisms; N = cpu_count is the default and is journaled.
4. S0: the student emits `cry` and nothing else; all sheets empty; voice 0.
5. S2: four laws proved unaided; voice reaches 2 by the structure's gate, not by teacher grant; at least one
   `believed` law refuted and kept, with an episode row.
6. S4: `2^10 = 1024`; the student's `why` for the births is answered from the receipt (voice 4).
7. S5: `100*100` without a brake; both routes recoverable from DNA.
8. S9: mean and P(event) over given lists; at least one refuted EXPECTED asked about unaided.
9. S10: a DNA path from a word gate to a numeric gate written by the student; one sentence emitted at voice 5.
10. Every stage reached is recorded with learned-turn count and teacher-turn count; the run reports which stage
    it reached and why it stopped.
11. No LLM, no network, no helper that computes outside the laws. Grep-tested.
12. The owner's four-run sketch as a unit test. The sketch (DESIGN): four nodes with per-node DNA tables; runs
    `0`, `0+1`, `1+1`, `1+2` produce outputs `000`, `01131`, `14262`, `18393`; read as gate_in · shard · gate_out
    alternation terminating when out == in (grammar PROPOSED), the receipts are `0 0 0`, `0 1 1 3 1`,
    `1 4 2 6 2`, `1 8 3 9 3`. The test asserts only the seven shards that appear (0, 1, 3, 4, 6, 8, 9); the
    allocation order of shards 2, 5, 7, 10–13 is OPEN.

A stage the student cannot pass is a result, not a failure of the build. Report it with `STAGE_STUCK.md`.

## 8. Anti-drift rules

1. A lesson is a process with variables, or it is not a lesson (DESIGN). A ground fact (`+(-1,-3) -> -4`) is
   refused (PROPOSED wording: `that is an answer, not a process`), except a constructor base case (`x + 0`,
   `neg(0)`) where the only constant is a declared base. `op NAME/ARITY on BASE` is the declaration (BUILT).
   Note: v11 installs variable-free laws unless they clash; this rule tightens it.
2. DESIGN: no LLM in the loop, in either process. No embeddings. No network.
3. DESIGN: no helper. If the organism cannot compute something, it says so at its voice level or stays silent.
4. Every number in prose is printed by `report.py`.
5. DESIGN: structure is locked after birth; the hash test (PROPOSED) is how it is enforced. If a stage seems to need a structure change, stop,
   write the change you think is needed in `OPEN_QUESTIONS.md`, and continue with the stage marked stuck.
6. DESIGN: the teacher never grants a voice level, never writes DNA, never writes a `proved` law.
7. The student's observer reads change-sets. Whether the student may read its own DNA directly is OPEN.
8. DESIGN: keep everything. No deletion, no cleanup, no "fixing" a garbage row.

## 9. Deliverables and the diff protocol

Deliver a tarball with:
- `structure/` (locked code), `teacher/`, `student/`, `sessions/`, `tests/`, `report.py`, `start.sh`
- `SHA256_MANIFEST.txt`; `STRUCTURE_HASHES.txt` (recorded at S0 and at the end; must match)
- `RESULTS_V12.md` printed by `report.py`: stage reached, learned turns, teacher turns, voice level, laws by kind,
  neurons, DNA rows, beliefs refuted, episodes, signatures per stage
- `PROPOSED_USED.md`: every PROPOSED item you built and why a DESIGN item needed it
- `OPEN_QUESTIONS.md`: everything you did not build because the sheet was silent
- `STAGE_STUCK.md` if any stage was stopped by `teacher_turns_max`

The owner will diff the two builds for drift, invention and hallucination (DESIGN). PROPOSED diff points:
stage reached, per-stage signatures, the contents of `PROPOSED_USED.md` and `OPEN_QUESTIONS.md`, and the
change-sets of the first ten turns. A build that reaches a later stage by adding anything not in this sheet
loses to a build that stopped early and reported why.

## 10. Handoff — paste this to the builder

> Build Neuron V12 from `NEURON_V12_BUILDERS_SHEET.md` and `plan.json`. If `neuron-v11-20260925_201315.tar.gz`
> is attached, section 3's physics must reproduce its signatures; if not, implement section 3 as written. Section
> 3 is structure: write it once, hash it at birth, never change it. Sections 4–5 are what the student learns;
> you do not write that data — the teacher and the student do, at run time. Build the teacher and the student as
> separate processes sharing one database. Run S0 through as far as the student gets on every core of this
> machine. Every tag means what section 0 says. Where the sheet is silent, do not invent: leave a hook and write
> the question in `OPEN_QUESTIONS.md`. No LLM anywhere. Print every number in `RESULTS_V12.md` from `report.py`.
> Deliver the tarball described in section 9.
