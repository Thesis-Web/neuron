# The lay notation and the physics words (turn one and two, hp)

*Written by the lead on 2026-10-19 from the kernel as built. This is the whole interface between the lay files and the kernel. Helpers lay from this and from the blueprint; nothing else.*

## 1. The notation

One statement per line. `#` starts a comment. Names are builder-side handles (addresses), never labels: the brain never sees them. Files load in name order; a file may use names from files that load before it (`00-roots.lay` first).

```
gate NAME                       a plain gate. Passing it puts the gate itself on the pad (the meaning in hand).
gate NAME = 2                   a value gate. Passing it puts 2 on the pad.
gate NAME @ x y z               a point (default: the origin; a gate with relationships is placed by them).
gate NAME : BINDING             a kernel binding (only 00-roots.lay does this). A re-told binding keeps the gate's string.
gate NAME : plain               (turn two) a told gate made plain again: its binding, string and the hops the brain laid on it go; made told.
label NAME text text ...        texts that call the gate. One text -> one gate. Lowercase. Add lang=xx at the end for another language.
proc NAME: tok tok tok ...      a process: a string of gates. Passing NAME puts the string at the front of the remainder.
  outcome -> NAME               (indented, under a proc) a branch: when the test just before it comes out `outcome`, go to NAME.
core NAME: tok tok ...          like proc, but a core value: the kernel refuses every write to it, and keeps a persistent core memory of it.
reltype NAME fwd: tok ... back: tok ...   a relationship type with its formula strings (point in, point out).
rel FROM TYPE TO [strength] [state]       a told relationship (default strength 1, state told).
trig GATE -> PROC [worth]       a usual trigger: every time a run leaves GATE, PROC splits off as a question run (default worth 0.5).
source NAME grounded|lower|guess : prog arg arg ...   a source: CALL runs prog with these args plus the pad's args, no shell.
miss GATE PROC                  sets the gate's miss process (default: the told miss).
```

Tokens inside `proc`, `core` and `reltype` strings:

- `name`: that gate.
- `'name`: the gate as data (READ.next then the gate): it goes on the pad instead of being passed.
- `=3.5`: a told value gate holding that number (made once, reused).
- There are no text literals. Words reach the brain only through labels and sources.

A `proc` line may fill a handle that `00-roots.lay` declared (`proc miss: ...`, `proc end-of-run: ...`, `proc sixth: ...`).

## 2. How a run moves (what the kernel does, so you can lay against it)

- A run has `at`, `from` (arrival), `rest` (the remainder; its head is next), `pad` (a stack), `want`, `trail`, `worth`, and who/what/when/where/why/how.
- **One step:** head = first of rest. shard = at.DNA[from, head], else at.DNA[-1, head] (the gate's usual way). No shard -> the miss process. Else drop the head, fire at's triggers, go to shard.next and pass it.
- **Passing a gate:** plain -> pushes itself; value -> pushes its number; proc -> its string goes to the front of rest; reltype -> reach (§4); physics -> the word runs (names are the lowercase forms in 00-roots.lay: go, split, land, wait, end, dup, drop, swap, over, read-next, write-mem, find-label, add, compare, clock, hear, say, call, spawn, move, ...); outcome/tier/state/fid gates -> nothing (they are names in hand; `'found` puts one on the pad).
- **Tests** (find-*, compare, read-* that can fail, hear) put an outcome gate at the head of rest. The shard (test, arrival, outcome) picks the branch. **Lay each test first in its own small proc** so its arrival is unique (the arrival of a proc's first gate is the proc gate itself). Without a branch the run passes the outcome gate (nothing happens) and goes on.
- **Loops:** a proc whose string ends with its own name, behind a test.
- **The miss process** is entered with `[at, from, at, from, head]` pushed on the pad (head is a gate or a raw text word; at/from twice so one pair feeds write-shard and one feeds GO). It must end with `go`, which pops `from` then `at` and resumes the run; the head is still at the front of rest, so the shard just written is used.
- **End of run:** when rest empties the kernel puts the end-of-run proc on rest once. Its string must write the memory (write-mem) and then end. A run that passes `end` earlier writes nothing.
- **Triggers:** a trigger run starts at PROC with the subject gate on its pad, worth = trigger worth × parent worth, why = the parent's why (the memory the input answers); read-parent gives the parent's memory id. Under the told floor it is parked instead (a `parked` row), never dropped.
- **The sixth** (PROC.sixth) is started on a beat with spare capacity and no live runs, as a run from the `self` port with who = self. If it passes `end` with nothing to do, nothing is written.
- **Inputs** from `neuron talk` start a run at the `talk` port gate with rest = the encoded line (labels -> gates, unlabeled words -> raw text). why = the memory of the last thing the brain said on that connection.
- **Kinds, tiers, states, fidelity** are gates: `'tier-long`, `'state-guess`, `'fid-highlights`, and list kinds are plain gates you lay (`gate gap`, then `'gap`). The kernel names a row kind by the gate's binding suffix, else its label, else #n. Reserved kinds (the kernel's own; name them with the roots gates kind-run, kind-birth, kind-shift, kind-parked, kind-core, kind-born, kind-told, kind-outage): run, birth, shift, parked, core, born, told, outage.

## 3. The physics words: pad in, pad out

Notation: `a b -- c` means pops b then a (b was on top), pushes c. `-> found|none` means it also puts that outcome at the head of rest. `n` number, `g` gate, `t` text, `v` point (x y z), `l` list, `m` mark.

**Run**
| word | pad | does |
|---|---|---|
| go | at from -- | resumes the run at `at` with arrival `from` (the miss process ends with it) |
| split | g subject -- | starts a branch run at g carrying subject (a text subject is encoded as the child's input words, taken by read-word) |
| land | x -- | puts x on the parent run's pad (or back on its own if it has no parent) |
| wait | -- | holds this run until its branch runs land, or a beat passes |
| end | -- | stops this run; nothing is written |
| dup, drop, swap, over, rot | the usual stack moves (rot: a b c -- b c a) | |

**Read: the run itself**
| word | pad | does |
|---|---|---|
| read-next | -- x | takes the head of rest as data (`'name` lays this) |
| read-head | -- x -> found/none | peeks at the head of rest |
| read-word | -- x -> found/none | the next word of this run's own input: a reading run (split with a text subject) holds its words here, and its process takes them one at a time; `write-rest` on the word hops it (an unknown word spawns through the miss way and the gate lands on the pad) |
| read-mark | -- m | a mark; SAY says down to it |
| read-list | x.. n -- l | pops n items into a list |
| read-tomark | x.. m -- l | pops the items above the mark (and the mark) into a list |
| read-count | l -- n | items in a list (words in a text) |
| read-item | l i -- x -> found/none | the i-th item |
| read-pick | l i -- l x -> found/none | the i-th item, keeping the list |
| read-pad | -- n | items on the pad |
| read-at, read-from | -- g | where the run is / came from |
| read-self | -- n | this run's memory id |
| read-parent | -- n -> found/none | the parent run's memory id |
| read-who, read-what, read-where, read-how | -- t | from the encoder |
| read-when | -- n | the input's time (ms) |
| read-why | -- n -> found/none | the memory this input answers |
| read-want | -- x -> found/none | the wanted outcome |
| read-depth, read-steps, read-worth | -- n | |
| read-sig, read-shape | -- t | this run's signature / shape |
| read-trail | -- l | the gates hit so far |
| read-mytrig | -- g g -> found/none | the trigger (gate, proc) that started this run |

**Read: rows reachable from a gate**
| word | pad | does |
|---|---|---|
| read-point | g -- v | |
| read-value | g -- n -> found/none | |
| read-bind | g -- t x -> found/none | binding kind, and its value / string / word |
| read-label | g -- t -> found/none | the first label |
| read-made | g -- t n | made (told/sourced/derived/spawned/core), by (memory) |
| read-rel | g type -- l -> found/none | the gates g relates to by type |
| read-relin | g type -- l -> found/none | the gates related to g by type |
| read-rels | g -- l -> found/none | every relationship: [type other strength state] (strength negative for incoming) |
| read-strength | from type to -- n t -> found/none | strength and state |
| read-shard | g arrival head -- next seen right wrong -> found/none | |
| read-trig | g -- l -> found/none | [proc worth] per usual trigger |
| read-def | g section -- l -> found/none | one section of the definition memory (1 address, 2 labels, 3 source texts, 4 built from, 5 relationships, 6 action, 7 use, 8 truth, 9 derived) |
| read-mem | n -- outcome seen right wrong last -> found/none | a memory's counts |
| read-body | n -- t fidelity -> found/none | a memory's body (the trail, or highlights) |
| read-memkind | n -- kind tier -> found/none | a memory's kind and tier as texts |
| read-trailof | n -- l -> found/none | a memory's trail as a list of [gate arrival head] lists (empty once condensed) |
| read-input | n -- l t -> found/none | a memory's own input gates as a list, and its shape |
| read-row | n -- key home body outcome -> found/none | a list row |
| read-use | g -- l -> found/none | memories (ids) the gate was used in |
| read-size | -- gates mems active | the brain's own size |
| read-source | g -- n -> found/none | 2 grounded, 1 to a degree, 0 never |
| read-trust | source topic -- right wrong weight -> found/none | |

**Write**
| word | pad | does |
|---|---|---|
| write-rest | g or l -- | puts it at the front of rest: "run this" |
| write-want | x -- | |
| write-shard | g arrival head next -- | lays or rewrites the way |
| write-rel | from type to strength state -- | lays or rewrites a relationship; both ends are re-placed by the formulas |
| write-strength | from type to delta -- | |
| write-mem | outcome -- n | this run's memory: same signature, same row, new time; shape change -> a shift row. Also receipts from the input's gates. |
| write-row | kind home key outcome body -- n | a list row (gap, imbalance, guess, parked question, slow, ...): same key, same row. A gate key is its number; the kernel's own rows (core, birth) are keyed the same way |
| write-mark | n yes/no -- | marks a memory and the shards in its trail right or wrong |
| write-outcome | n x -- | |
| write-body | n body fid -- | rewrites a memory's body (the HC condensing) |
| write-def | g section text -- | adds a line to a definition section |
| write-label | text g -- | |
| write-proc | g l -- | binds a gate to a string of gates, and lays its shards |
| write-value | g n -- | |
| write-trig | g proc worth -- | adds or re-weighs a usual trigger |
| write-trust | source topic right wrong weight -- | |
| write-receipt | g n -- | a use receipt from gate to memory |

**Spawn, delete, move**
| word | pad | does |
|---|---|---|
| spawn | [v] -- g | a new gate (at v if a point is on top, else the origin) with its birth memory |
| delete-rel | from type to -- | |
| delete-shard | g arrival head -- | |
| delete-def | g section line -- | |
| delete-row | n -- | |
| delete-trig | g proc -- | |
| delete-label | text -- | |
| move | g v -- | moves a point |
| move-mem | n tier -- | moves a memory between tiers |

**Find (index only)**
| word | pad | does |
|---|---|---|
| find-point | v -- l -> found/none | gates in that grid cell and its neighbours, nearest first |
| find-label | t or g -- g -> found/none | a text that is an address (#n) finds gate n |
| find-sig | t -- n -> found/none | the memory for a run signature |
| find-shape | t -- l -> found/none | memories with that shape (not this run's own) |
| find-time | from to -- l -> found/none | memories between two times |
| find-value | n -- l -> found/none | gates holding that value |
| find-row | kind -- n -> found/none | the oldest row of a kind |
| find-rowkey | kind key -- n -> found/none | |

**Math**
| word | pad | does |
|---|---|---|
| add sub mul div | a b -- c | numbers, points, number×point; n DIV v is inversion through the unit sphere (v/|v|²); list ADD x appends |
| compare | a b -- d -> same/more/less | numbers: d = a−b. points or gates: distance (same under 0.5). lists: count of items that disagree. texts: equal or not. |

**Outside**
| word | pad | does |
|---|---|---|
| clock | -- n | now, ms |
| hear | -- t -> found/none | the answer to this run's last CALL (the run is held until it arrives) |
| say | x.. m -- | says the items above the mark (or the whole pad) through the run's port: gates by label (no label: #n), numbers, texts |
| call | source args -- | runs the source's program with args (a list or one item); then HEAR |

Every write is refused (outcome `no`, and a REFUSE line in acts.log) when it touches a core-value gate or memory.

## 4. Reach along a relationship type

Passing a reltype gate with a gate on the pad: `g opposite` -- `l -> found/none`. The stored lines first; if there are none, the type's fwd formula is applied to g's point and the gates at that point are found. The formulas are strings over the math words with the point on the pad, for example `fwd: =-1 mul back: =-1 mul`.

## 5. Rules for every lay file (from the blueprint and the guide)

- Lay actions and structure. Lay no definitions, no facts, no relationships from your own head (relationships between told roots that the blueprint itself names are allowed and are marked told).
- No words, sentences, replies or templates. The brain says gates by their labels and nothing else.
- Every gate you lay must do something when passed, or be a name in hand. Say what passing it does in a comment.
- Each process at root level: the smallest version that works, a handful of gates. Split long ones into named steps.
- Every FIND is an index lookup. No loops over a whole table.
- Nothing is a stub. A process that just ENDs so the part looks present is cheating.
- Only your own files. Pieces meet through the names in 00-roots.lay, the names the lead lists in your brief, and the physics words.

## 6. Turn two additions

- `neuron told-opens` (lay port head TOLD-OPENS) reopens the told base after told ends: kv told=open, a told row "told opens" on the timeline; `neuron told-ends` closes it again.
- The roots handle `meaning` (g --) is the meaning way (45-meaning.lay): gap, spec, compile, test, hold, wire, use. A meaning is a gate with a binding (`read-bind` found); a hole is `w-something` or `w-someone` (10-told.lay: a hole takes a bound gate in hand under it, else stands).
- Inside the miss way the quiet mark stands: leaving a test's outcome gate after a miss excursion fires no triggers.
- `write-proc g l` with an empty list makes g plain again (the brain changes its mind back): binding, string and the hops laid on g go; made derived.
- The brain's own code is a set of grounded sources (src-kernel-*, src-lay-*: `cat` of /opt/neuron/kernel/*.go and /opt/neuron/lay/*.lay); own-code (40-sources) reads each once onto section 3 of w-i.
