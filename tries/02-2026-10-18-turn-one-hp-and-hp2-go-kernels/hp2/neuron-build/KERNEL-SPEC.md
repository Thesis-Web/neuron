# Kernel spec for builders (turn one, hp2)

The kernel (`kernel/*.go`) is the lead's. Builders write **lay files only**. This is how lay files run.

## The step (the whole hop)

A run has `at` (gate), `from` (arrival), `rest` (the remainder; its head is next), a `pad` (a stack of values) and named `slots`.

```
if rest empty: GO to end-of-run (root run) or land-end (split run)
head = rest[0]            (raw text is first looked up in the label index)
shard = at's DNA[from, head]
no shard -> the miss way (the gate's miss process; told: `miss`)
else: drop head; if head came from input (depth 0) SPLIT the shard's triggers;
      if head is an OUTCOME: skip the rest of the test's frame (a branch is a jump)
      at = shard.next; from = the frame (or the previous gate, for input)
      pass at:  physics gate -> perform it
                process gate -> its string goes in front of rest (a call; the run is now in its frame)
                value gate   -> push its value (a number)
                any other    -> push the gate itself
```

**Triggers on a process gate** fire when the run leaves that process's frame (its own shards are left from inside it).

**Frames.** Inside a process string, the arrival is the process itself. So the shard for "at READ, inside process P, head X" is `(READ, P, X)`. Branches are keyed the same way, so two processes never collide.

**Branches.** `on P OUTCOME -> T` lays the shard `(last physics word in P, P, OUTCOME) -> T`. When the outcome comes up, the run jumps to T and **the rest of P is skipped**. When it doesn't, P just continues. Use the empty process `carry-on` for "this outcome just continues". An outcome nobody planned for goes down the miss way, which asks "I don't know what to do here" (`dunno`) and ends the run. Plan every outcome your tests can give.

**Receipts.** Rows a run writes carry a receipt to the memory of the run its tree started from; a run that wrote rows and ends without WRITE MEM gets that memory filed when it ends.

**Quoting.** Passing a process gate calls it. To push a gate as data (to SPLIT it, or to name a process), write `ITEM READ name`: READ ITEM takes the next item of the string as a value and doesn't step to it. Plain gates (types, selectors, slot names, kinds) can simply be passed; they push themselves. Value gates push their number, so use `ITEM READ ZERO` for the zero gate itself.

## The pad

- Physics words pop what they need **by kind**: "pop a gate" takes the most recent gate on the pad, "pop a number" the most recent number, "pop any" the top. A one-element list stands for its element.
- **Pad hygiene is your job.** Anything you push and don't consume stays and can be popped by a later word by mistake. Use `LAST DELETE` to drop the top and `LAST READ` to copy it. Leave the pad as you found it, except for what you mean to hand on.
- **Slots:** `value SLOTNAME SLOT WRITE` stores a value (pops the slot gate, then any value). `SLOTNAME SLOT READ` pushes it (NONE if empty). Slot names are any told gates; prefix yours with your area (for example `q-subj`, `src-word`). Split runs inherit a copy of the pad and the slots.

## Physics words (each is one gate)

| Word | Pops (top first) | Does |
|---|---|---|
| GO | target gate, arrival gate | moves the run there (no pass); skips the rest of this frame |
| SPLIT | target gate | starts a branch run at target with a copy of the pad and slots; subject = the top value under it. Worth = parent's × DEPTH |
| LAND | any | puts it on the parent's landing list |
| WAIT | — | holds until the branch runs split since the last WAIT end (a run parked on a CALL counts), at most WAITBEATS beats, then pushes **one list** of what they landed |
| END | — | stops this run (no memory written) |
| READ / WRITE / FIND / DELETE / MOVE | a selector, then its keys | see below |
| SPAWN | a point | a new gate there, with its definition memory and birth memory; pushes the gate |
| ADD SUB MUL DIV | x (top), then y = the next number or point | pushes y op x. Points: p±p, p·n, p/n, p·p = dot. One list alone: ADD sums it, MUL multiplies it. Divide by zero: NONE |
| COMPARE | x, then y | numbers: SAME/MORE/LESS (y vs x) and pushes \|y−x\|. Points: SAME if closer than a cell, else MORE, pushes the distance. Gates/text: SAME or MORE. Lists: SAME or MORE, and pushes a mask (equal places kept, different places = the `something` gate, a hole) |
| CLOCK | — | pushes now (seconds) |
| HEAR | text or a gate | text is encoded (split at spaces and symbol keys) and the pieces go at the front of rest as input (depth 0); a gate goes in front as an inner word of the current frame (not input) |
| SAY | any | needs `core-check` passed since the last act. Gate → its label; number → digits; list → each. A gate with no label: pushes it back, NONE. Everything said in one beat to one person goes out as one line |
| CALL | text (the query); uses the top-most source gate on the pad | needs `core-check-call`. Runs the source's template with the query; the run parks until the answer comes back as text on the pad (NONE on failure or empty) |

### Selectors (push the selector gate just before the word)

**READ:** `ITEM` (quote next item) · `LAST` (copy top) · `KIND` (peek top → outcome GATE/NUMBER/TEXT/POINT/LIST) · `MAT MFROM MHEAD` (the last miss) · `SUBJ` (the run's subject) · `WANT` · `WHO WHAT WHERE` (text) · `WHY` (number: the memory id of what the brain last did for this person) · `MODE` (the run's made-mode gate) · `START` (the gate the run started at) · `MINE` (→ YES if the brain started this run tree itself, NO if a person did) · `SLOT` (slot) · `MSIG` (memory id → its signature list) · `SIG` (list of the run's input gates so far) · `TRAIL` (list of gates it hit) · `REL` (type, a → strongest b) · `RELS` (type, a → list of b, strongest first) · `STRENGTH`/`STATE` (b, type, a) · `POINT` (g → point) · `VALUE` (g) · `LABEL` (g → text) · `SECTION`/`SECTIONS` (section gate, g → latest / list) · `PROC` (g → list) · `USUAL` (g → list of trigger gates) · `WORTH` (trigger, g) · `SHARD` (head, arrival, g → next) · memory fields, each popping a memory id number: `OUTCOME BODY RIGHT WRONG SEEN HOME TIME TIER FID MADE` (`MADE` with a gate on top gives the gate's made) · `SHAPE` (memory id → its path redrawn from today's points, then its stored shape, as two texts: COMPARE them) · `SIZE` (gates) · `ACTIVE` (memories) · `COUNT FIRST REST` (pop a list) · `TRUST` (topic, source → right count, then wrong count; `trust-weight` in 10-types makes the weight) · `GROUNDED` (peeks the top-most gate: a grounded source → YES, ungrounded → NO, not a source → NONE).
Absent → NONE at the head.

**WRITE:** `SHARD` (next, head, arrival, g; a new shard copies g's usual triggers; a trigger's worth is read from its gate when it fires) · `LABEL` (g, then text) · `REL` (strength number, b, type, a; state from the run's mode) · `STATE` (state, b, type, a) · `VALUE` (number, g) · `SECTION` (value, section, g) · `PROC` (list, g; needs `core-check-proc`) · `USUAL` (worth, trigger, g) · `MEM` (outcome: this run's memory. Same signature → same row, new time; pushes the memory id. Same signature with a different outcome → pushes id and the new outcome, outcome MORE) · `RIGHT WRONG TOUCH` (memory id) · `OUTCOME BODY` (value, memory id) · `SHIFT` (new outcome, memory id: a truth-shift row; pushes its id) · `TODO` (kind gate, then subject: a memory on one of the sixth's lists, one per subject and kind) · `MADE` (gate: sets the run's mode: TOLD SOURCED DERIVED SPAWNED GUESS) · `WANT` (any) · `TRUST` (YES/NO, topic, source) · `SLOT` (slot, value).

**FIND (index only, never a scan):** `SIG` (this run's signature → memory id) · `LABEL`/`LABELS` (text → gate / list) · `POINT` (point → the gate there) · `NEAR` (point → list of gates in the cell and its neighbours) · `VALUE` (number → gate) · `TIME` (t1, t0 → list of memory ids, at most 64; oldest first, or newest first when t0 > t1) · `SHAPE` (→ list of memory ids of runs shaped like this one) · `KIND` (kind → the item of that list touched least recently; whether it's due is the sixth's own judgement; `WRITE TOUCH` counts a try) · `HOME` (kind, g → latest memory of that kind at g, e.g. `DEF`, `BIRTH`) .

**DELETE:** `LAST` (drop top) · `REL` (b, type, a) · `SHARD` (head, arrival, g) · `USUAL` (trigger, g) · `MEM` (id). **MOVE:** `POINT` (point, g) · `TIER` (tier, memory id) · `FID` (fidelity gate, memory id).

The kernel refuses every write to a gate marked `core`.

## Lay notation

```
gate NAME [phys WORD] [val N] [at X Y Z] [core]
label LANG "TEXT" NAME          (LANG en for words; the decoder says en labels first)
proc NAME = ITEM ITEM ...       (an empty string is allowed: proc carry-on =)
on NAME OUTCOME -> TARGET
trig NAME -> QUESTION [WORTH]   (a usual trigger: shards on NAME fire it as a branch run)
rel A TYPE B [STRENGTH]
sect NAME SECTION VALUE         (a gate name, a number, or "text")
unrel A TYPE B                  (takes back a told line, before told ends)
source NAME grounded|ungrounded TEMPLATE   (%s = the shell-quoted query)
```
A name must be declared (`gate` or `proc`) in the same file or an earlier one before it's used. To use a gate another area defines, forward-declare it with a bare `gate NAME` line.

## What exists (files 00–25, the lead's)

- `00-roots`: physics gates, selectors, outcomes (NONE SAME MORE LESS GATE NUMBER TEXT POINT LIST YES NO), made kinds (TOLD SOURCED DERIVED SPAWNED GUESS), states (GUESS BELIEF GROUNDED-STATE CONTRADICTED TOLD), tiers (ACTIVE PERSISTENT LONG), fidelity (EXACT CONDENSED HIGHLIGHTS), memory kinds (RUN DEF BIRTH LAID BORN TOLDEND RESUMED PARKED SHIFT CORRECTION), the sixth's lists (GAP IMBALANCE TEST-GUESS QUESTION SLOW), sections (sec-address sec-labels sec-sources sec-built sec-rels sec-action sec-use sec-truth sec-derived), told values (BEAT BUDGET STUCK DEPTH PATIENCE PARK CELL).
- `05-keys`: a gate per key (`key-a` … `key-qmark` …).
- `10-types`: `carry-on`; types `t-same t-opposite t-kind-of t-part-of t-like t-cause t-before t-used-for t-describes t-supports t-contradicts t-derived-from`, each with a formula in `sec-action`; `relate` (pad: a type b strength → writes the relationship and moves b toward f(a)); `one`.
- `20-core`: `miss`, `end-of-run`, `land-end`, `stuck`, the core values, and `core-check` (before SAY), `core-check-call` (before CALL), `core-check-proc` (before WRITE PROC).
- `25-numbers`: zero, one, two; plus minus times divided (their `sec-action` names ADD SUB MUL DIV); `equals` (memory first, the long way on a miss).

## Shared gates between areas (the only way pieces meet)

| Gate | Owner | Called how |
|---|---|---|
| `what-is-this` | questions | SPLIT on a newborn word; subject = the new gate |
| `dunno` | questions | SPLIT where a run got stuck; subject = the gate |
| `ask-name` | questions | called with an unlabeled gate on top of the pad |
| `source-check` | sources | SPLIT with subject = a gate to read up on |
| `belief` | questions/balance | called when a source contradicts what is held |
| `backpop` | learning | called with a memory id on top (a shift, a correction, a kept formula, a source change) |
| `hc` | memory | the HC: condense memories older than a day |
| `sleep` | learning | the sixth calls it when active memory passes a mark |
| `sixth` | learning | the kernel starts it on a beat with nothing else to do; it must END without writing when nothing is due |
| `when-did` | memory | answers "what did you do <when>?" from the timeline |
| `heard` | questions | end-of-run calls it on every root run before the memory is written; the run's outcome is on top of the pad and must be left there. It handles input that answers the brain's last act (READ WHY): a name for an unlabeled gate, a yes or a no |

## How to try your file (pre-birth dev brain; never the real one)

```
/tmp/claude-1000/nb/devup.sh NAME          # fresh dev brain with every lay/*.lay, born
export NEURON_HOME=/tmp/claude-1000/nb/NAME
printf 'some words\n' | timeout 5 /home/james/neuron-build/kernel/neuron talk
tail -50 $NEURON_HOME/acts.log             # what it did
sqlite3 -readonly $NEURON_HOME/brain.db 'select ...'   # its rows (the db is committed every beat)
kill $(cat $NEURON_HOME/pid)               # when done
```
Use your own NAME. The loader prints errors (unknown gate, branch conflict) when you lay a file.

## Memory bodies are not all in RAM (lead, 09:30, owner's HC order)
A memory in the LONG tier keeps its body on disk only. `READ BODY` still works on it (read from disk for that read). Don't rely on a body staying in RAM, and don't expect a long-term memory's body to be exact: a condensed one holds highlights; `rebuild` (60-memory) brings back a run from them. `READ ACTIVE` counts memories in the ACTIVE tier only.
