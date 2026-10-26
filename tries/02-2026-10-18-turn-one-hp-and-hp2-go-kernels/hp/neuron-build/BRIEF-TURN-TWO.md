# BRIEF-TURN-TWO: what every builder of turn two works under

*From the lead, 2026-10-19 12:20. Turn two is open on the live body (the owner's word, 12:05). Read `BRIEF-COMMON.md` §A (the three rules and the traps, word for word) and §C (how you work) first; they bind you here exactly as in turn one. Then `LAY-NOTATION.md` (the interface), `lay/00-roots.lay` (the names), `NEURON-MEANING-BLUEPRINT-2026-10-19.md` (the scope of this turn) and `MEANING-GAP-2026-10-19.md` (where the live body stands). Then your own area's files. Nothing else unless your brief says so.*

## A. What this turn is

Turn one built the whole baby and marked told ends at 08:39. The owner then wrote the meaning blueprint: a word's meaning is the code it makes the silicon run; a definition is a spec, not the meaning; words are compiled into formulas of the meanings the brain already has (roots, primes, other compiled words), tested by balance, held, wired to the word's gate, and used as hops. **Everything in that blueprint is a guess, not a rule. The graph decides by balance.** Your first guesses are guesses too: mark them so in the rows (a `guesses` row, a relationship with state `guess`, a comment in the lay file), never as known.

Where the meaning blueprint and the first blueprint differ on meaning or learning, the meaning blueprint wins. Everything else in the first blueprint and the guide stands.

## B. The contract (names everyone uses)

Everything in `BRIEF-COMMON.md` §B stands. Added for turn two:

- **`meaning`** (00-roots.lay, a handle like `learn`): `g --`. The meaning way on gate g, filled by builder M in `45-meaning.lay`. The sixth splits it as a question run on a gap row's gate (builder E2 lays that). It must: with section 3 of g empty, split `source-check` on g and keep the gap row (bounded: the row's seen count against a told `gap-tries`, then the row is dropped and the word stays a bare name); with section 3 held and g bare (read-bind none), compile; with g wired, test or nothing.
- **A meaning** is a gate with a binding: `read-bind` found. A bare gate (`read-bind` none: a spawned word, a key) has no meaning. **A hole** is `w-something` (a what-hole) or `w-someone` (a who-hole).
- **The definition memory's sections** (`read-def g n`, `write-def g n text`): 3 the spec (source texts, one line per source), 4 built from (the meaning gates a formula is made of), 6 action (the kernel shows the binding and the triggers; the compile adds its formula line), 9 derived (what the brain worked out: applied-in receipts).
- **Wiring** is `write-proc g l` (a list of gates becomes g's string; the kernel lays the hops; g is made=derived by the run). The kernel refuses it on core gates and physics gates; a told prime (a `proc`) may be rewritten: that is the brain refitting a first guess.
- **Running a list of gates as a branch:** `'use-run swap split` with the list as the subject; `proc use-run: write-rest` (builder M lays it). The branch's end-of-run lands its memory id on the parent (B's remember); `read-mem` on it gives the outcome text.
- **`wait`** holds the run until its branches land **or a beat passes**. A long branch (a text of hundreds of words) takes more than one beat; loop `wait` behind a test on `read-pad` until what you expect has landed, bounded by a told count.
- **Lists:** `compare` on two lists gives the count of items that disagree (same when 0). `add` on a list appends an item. `read-count`, `read-item`, `read-pick` as in the notation. A text cannot be itemized: to walk a text's words, `split` a run with the text as its subject and take the words with `read-word` (a word with a label arrives as its gate, else as raw text).
- **States as names in hand:** `state-guess` (roots). Builder M lays `held` and `understood` as plain gates in 45-meaning.lay (names in hand, no English label: they are said as their address until the brain names them).

## C. Who builds what

| builder | file | area |
|---|---|---|
| M | `lay/45-meaning.lay` (new) | the meaning way: gap, spec, compile, test, hold, wire, use, senses, holes asking |
| A2 | `lay/10-told.lay` (edits) | the primes as the first-guess layer: labels for the unlabeled four, actions for the inert nine, the worksheet's guesses as `guess` relationships, the hole action for w-something and w-someone |
| E2 | `lay/50-learning.lay` (edits) | the sixth learns meanings first (gap list first, `meaning` instead of `answer`), the fit way moves its offset gate instead of spawning one |
| lead | kernel, 00-roots, 30-questions, 40-sources, sources/bin, merge, re-tell, report | told-opens; the reading way spawns nothing for prose and writes no co-occurrence lines; know-this flags a word with a spec and no action; the scripts' cut |

No builder edits another builder's file. 45 loads after 10, 20, 30, 40 and before 50, 60: M may name A's, B's, C's, D's gates; E2 may name M's `meaning` only through the roots handle.

## D. Dry runs

`tools/dryrun.sh -i "line" ... lay/NN-yours.lay [other files]` as in BRIEF-COMMON §C. It births a scratch brain from `00-roots.lay`, `tools/dev-miss.lay` and the files you give, inside a 1.5 GB cap. **Run one dry run at a time, `-s` at most 25 seconds**: this is a two-core machine carrying the live brain and three builders. The live brain (`/home/neuron`, user neuron) is never touched by a builder: no `neuron lay`, no `neuron talk` to it, no reading its body. Query your scratch brain with `sqlite3 -readonly DIR/home/brain.db`. Passing another builder's handle in your dry run does nothing unless you include their file; include `lay/10-told.lay` `lay/20-memory.lay` `lay/30-questions.lay` `lay/40-sources.lay` with `-n` when you need the real miss, memory and questions (B lays the real miss and end-of-run; `-n` leaves dev-miss out). Source calls in a dry run reach the real dictionaries on this machine (dict, wn) and the network; keep the inputs few.

## E. Reports

As BRIEF-COMMON §C: the file; every process with its token count and one line on what it does; the dry-run acts and rows that show each one working and the ones that do not; what you could not do and why; gaps left on purpose; one line per decision the documents leave open. **Hard limit: stop after 90 minutes of work or 12 dry runs, whichever comes first, and report.** A part at root level (the smallest version that works) is fine; a stub is cheating; nothing from your own head is laid as fact.
