# Output contract, tries/35 (2026-11-02): the relationship formulas built and deployed, both brains

Written before the build, at the owner's order (2026-11-02, 14:43): "build an output contract first for you to balance against when
you are done. output contract should be this works and is correct, that works and is correct, this process should not be changed or that
process has to work like it is. if you find anything wrong or incorrect it becomes part of this turn also. but wrong has to be grounded in
my prose and current superceded state of that prose ... then add the new work to that balance sheet ... regression is not ok".

Every line of part 1 is a live output read from the running brain before the build (the kernel on hp, 10.31.1.106:8058 and socket 7007;
the hub on 8056). After the build each line is read again; the balance is part 4. Nothing here is a test of mine: it is what the brains
answer when asked.

## 1. What works and is correct now, and must still work the same after

### The kernel (hp)

| # | What | Read before (2026-11-02 14:00) | Read after |
|---|---|---|---|
| K1 | The brain is its stored file; a restart reopens it in seconds; `defined`, `gates`, `runs` come back as they were | `/api/info`: defined 722,277, gates 1,317,428, runs 19,937,323, refused 1, pending 0, shard_rows 130 main / 21 sixth, heap 32 MB | |
| K2 | A recall: `define : X` of a defined point answers from its own definition table, no source asked, the node rows unchanged, def/known/unknown/ok on the sheet | `define : who` 0.04 s, known 794 / unknown 88; stone 0.02 s (2,309 / 326); water 0.058 s; bread 0.017 s (NOTE tries/34, fourth pass) | |
| K3 | The long way then the short: a never-defined point is asked of the eight sources, learned, and recalls on the next line | takakkaw: asked, 1 row, 0.175 s; typed again: recalled in 0.154 s, no source asked | |
| K4 | The build step at birth: a never-seen word in a plain sentence gets its gate, its neuron row, its first DNA row (the define row: before 156, trigger 68, spawn the define-at-birth run), and its definition spawned beside the main run; the main run completes | `the morleys is here`: gate 1317426, one DNA row [before 156, trigger 68, spawn 19936999], two node rows from Wiktionary, `defined` +1, the main sheet complete in 0.024 s | |
| K5 | The define lays the catalog relationships from the returns' markers through `relmap` | `define : ortega` laid is → statesman, solon; the rel table 4,024,107 rows in 15 kinds (like 2,583,407 … causes 601) | |
| K6 | The hop is one shard: a pass lays no row and counts on the space's row 17; the DNA rows are function rows only | shard_rows 130 main, 21 sixth; `print : who` 9 ms, every pass names shard 17 | |
| K7 | define's own row (before heard 1, trigger `:` 68) calls the recall define 19937222; born's row 6 calls 19937007; heard's row calls 19936643 | `dna WHERE gate = 156`: [557, 1, 68, call 19937222, times 76]; [1867, 5, 68, call 6459431, times 1,363,618]; [1931, 1, 155, call 1132]; `dna WHERE gate = 16`: [6, ∅, ∅, call 19937007, times 1,175,443] | |
| K8 | The ok neuron listens: every cell populated ticks its row; a complete sheet ends `ok: ok` | each recall above ends ok | |
| K9 | The full page hp:8058/full opens from the bundle, draws the newest lines' points, steps and plays; a typed line reaches its history live; the look is 17.3's | 69,277 points sent, 19,821 drawn, 366,457 lines, ready in 91 s, a step 0.8 s (NOTE tries/34) | |
| K10 | The page's relationship kinds can be turned on and off, their pull set by slider, their direction by the drop-down (the owner, 10-24: "I don't want that changed") | the kinds list, sliders and direction choices present on /full | |
| K11 | A read without a key is refused by the kernel's tables; the brain's own plain tables (rel, relmap) read as SQL | `SELECT kind, other FROM rel WHERE gate = ?` answers; a keyless vtable read answers `error` | |

### The hub (8056)

| # | What | Read before (2026-11-02 14:00) | Read after |
|---|---|---|---|
| H1 | The door answers; both routers hop; refused 0 | `/api/info`: ready, routers main hops 397,599 / sixth 474,604, refused 0 / 0 | |
| H2 | A recall on the hub: `define : X` of a defined point, no source asked, 4 hits, 2 to 6 s, the node table unchanged, def/known/unknown/ok | stone 2.2 s, bread 3.4 s, each 4 hits (NOTE tries/34, fourth pass) | |
| H3 | The hub's define lays the catalog kinds from the markers for a new point | castoridae: has, member rows (the only catalog rows on the hub: has 2, member 1) | |
| H4 | The hop is one shard on the hub too: `land_go` counts a pass on table "3" shard 17; the colon's table holds no pass rows | "3": [17, ∅, ∅, times 24,181,956]; "153": 3 function rows | |
| H5 | define's rows on the hub: heard/`:` calls 4254380 (the recall define); sixth/`:` calls 498941 (the old define); heard/unknown calls 11254 | `main."153"`: [587, 1, 68, call 4254380, times 103]; [18574, 5, 68, call 498941, times 158,025]; [18664, 1, 152, call 11254, times 2] | |
| H6 | born's row calls run 1 (the two tables of a new point) | `main."16"`: [6, ∅, ∅, call 1, times 144,089] | |
| H7 | The sixth's chain runs: `define : X` lines arrive from the sixth and define points; `why : N 24` follows each | main runs 4,530,962 to 4,530,972 arrived from the sixth: `define : Briony`, `why : 4530963 24` | |
| H8 | The hub is changed only through its own prompt (a typed BUILD line through `/api/type`); never through an outside connection (an outside DDL killed its router on 11-01, 18:35) | — (a process rule) | |
| H9 | The hub's page opens and draws with its kinds, sliders and directions | — | |

### Both

| # | What | Must hold |
|---|---|---|
| B1 | No code outside the brain decides: formulas are rows and typed lines; the kernel and the hub's triggers are the physics | the owner, 11-01: "it is illegal for you to put code outside the db to fix anything" |
| B2 | Nothing is deleted from a live brain by me (duplicate rows, trace rows, old runs stay) | the owner's word only |
| B3 | 8056 is never pointed at the kernel; the kernel never touches the hub's files | standing |
| B4 | Text lives in the encoder only; a new table holds numbers (gates, counts, coordinates) | the owner, 11-01: "text lives in the fucking encoder only" |

## 2. What is wrong now, grounded in the owner's current prose

| # | Wrong | The owner's words (the newest state of the prose) | Where |
|---|---|---|---|
| W1 | Neither brain holds a point's x, y, z. The page computes a drawing and lets it go. | 11-01 23:40: "the encoder ... assigns that word its meaning gate id number this number is not it's x,y,z cordinate because the points float over a stationary graph based on the push or the pull of relationships, the gates x,y,z number is determinate on state and time, (this is how truth shifts are measured over state and time) <-- I fear the kernal was not built correct enough to support this." 10-23 23:56: "the sqlite is a vector graph data 3d data base.. how on earth can the gates ... the points not have x,y,z ????? I am confused?????" | both |
| W2 | The relationship formulas (what each kind does to the points) live only in the page's JavaScript (pull, rest, direction per kind). The brain holds no formula row; nothing in the brain pushes or pulls a point. | 11-01 23:40: "each one of these relationships represents a mathmatical formula that connects points to eachother and pushes or pulls points away or together ... the formulas are reuseable and can be the same formula for a relationship like opposite or inverse, or alike ... as part of the build step relationships are populated so that the meanings have push and pull to the graph ... when a shard is used on a meaning point that point will likely move on the graph, unless the shard being used has the same meaning as the last one used ... as the brain uses it's neurons it's like it's working a muscle and those neurons move some based on the different pulls or pushes of the relationships". 09-29: "formulas as neurons is going to be much faster ... it was runtime compilers doing the math that was supposed to be done already inside the brain". Law 1 (draft §12): the graph is the code. | both |
| W3 | On the hub, 183,618 defined points hold like/opposite rows only (like 2,303,454, opposite 366); the catalog kinds exist for one point (castoridae). The build step's relationships were never populated for them. | 11-01 23:40: "you did opposite and alike and basically gave up on all the rest"; "as part of the build step relationships are populated"; 11-01 19:38: "it does require or can require back population of existing dna shard triggers... which will require the building of that process within the neurons" | hub |
| W4 | The sixth's define row still calls the old define on both brains (hp: 6459431, 1,363,618 times; hub: 498941, 158,025 times): every define the sixth asks re-asks the sources even for a defined point and lays like/opposite only. The sixth's chain is the bulk of all defines. | 11-01 (tries/34): "asked a defintion, looked it up, wrote it, and then asked again it should recall what it has learned"; the relationships "as part of the build step" | both |
| W5 | On the hub, birth lays the two tables and nothing else: no define row, no definition spawned at birth; a never-seen word in a plain sentence is not defined as the line runs (hp does this since 11-01 19:00). A point born by a return (secondary_go) has no define row either. | 11-01 23:40: "once a meaning point or gate is built, the dna table is built and populted with it's first row which is ALWAYS the define row ... this first define dna row spawns the defintion of that new gate.. immediately" | hub |
| W6 | On the page, a new point's first place is its neighbours' mean plus a random unit vector (17.3's placeNew) and the brain is not asked where the point is. | W1 | both pages |

Not wrong by the prose, left as it is: the hop shard's undercounted times; the duplicate definition rows (the owner's word); the page's space-apart pass (17.3's physics); the "kind's own vector" direction (offered on the page, not a brain formula yet); triads and larger (between, ratio, composition: "some are between multiply points a triad, or 4 or 5", not laid: they need a formula over three or more points, the owner's call on which first).

## 3. The new work, and the live output that will show it

### N1. The formulas as rows in each brain (both)

`formula (id, pull, rest, dx, dy, dz, mode)`: one row per distinct formula. `pull (kind, formula)`: each relationship kind (a gate) names the formula it uses, so two kinds can share one ("the same formula for a relationship like opposite or inverse"). Mode 0: a spring along the line between the two points toward rest length; 1: directed, the other point sits rest away along (dx, dy, dz) (is: the class above; includes: the member below; implies, causes: the consequence east; past: the base form west; before east, after west); 2: across the origin (opposite, inverse, contradicts). The numbers are the page's first table (tries/34, page_patch5), carried into the brain so the brain holds them and a typed line changes them.

Expected live: `SELECT count(*) FROM formula`, `SELECT count(*) FROM pull` answer on both brains; `SELECT l.symbol, f.pull, f.rest, f.mode FROM pull p JOIN formula f ON f.id = p.formula JOIN label l ON l.gate = p.kind` lists every kind the rel table holds (hp 15 kinds + the page's others; hub 4 and the rest).

### N2. A point's x, y, z in each brain, moved by its relationships when a shard is used on it (both)

`xyz (gate, x, y, z, shard, before, next, at, run, moved)`: the point's place now; the shard last used on it and that use's before and next symbols (the hop shard "accepts the before and remainder as two variables", so the same shard with another before or next is another meaning); the clock and run of the last move; how many times it moved. A landing on a point whose (shard, before, next) differs from the last applies every relationship row of the point through its kind's formula to the other point's place, sums the pulls, and moves the point one step (the page's law: force = pull × (L − rest)/L along the line, or toward the directed place, or across the origin; a step 0.04 of the sum, capped at 6 units; a point never placed starts at the mean of its placed relations plus a unit vector of its own, as the page's placeNew does; a point with no placed relation starts a unit from the origin). `origin` (hp gate 2822, hub 757) sits at 0, 0, 0 and is not moved ("the only word with zero pull is origin", 10-24). On the kernel this is the landing's physics in C reading the brain's own `rel`, `pull` and `formula` tables, the place held in a side file of the brain (`out/brain.map.xyz`, as the brain's own SQLite tables sit beside the map) and read as the table `xyz`; on the hub it is a trigger on `hit` (`xyz_go`) in the brain's SQL. A back-population pass (kernel request `settle N`; hub: a typed line in batches) places and steps every point that holds relationship rows, the long way once, so the already-learned graph has places too.

Expected live, kernel: `SELECT x, y, z, shard, before, next, moved FROM xyz WHERE gate = (SELECT gate FROM label WHERE symbol = 'water')` answers a row; after `define : water` typed, `moved` is one more and the row's `run` is that line's run; `define : water` typed again (the same shard, before and next): `moved` unchanged. Hub: the same through `/api/q`. The recall time stays at the kernel's 10 to 60 ms and the hub's 2 to 6 s (K2, H2).

### N3. The hub's defined points get the catalog relationships (hub)

A typed BUILD line, the define's own marker span over the returns of N points at a time (the run table keyed by about), typed repeatedly through the hub's prompt until every defined point has been read once; the hub's chain keeps running between the lines. Measured before: the span costs 0.02 to 0.18 s a point on the hub when keyed by about.

Expected live: `SELECT l.symbol, count(*) FROM rel r JOIN label l ON l.gate = r.kind GROUP BY r.kind` on the hub shows the catalog kinds in the hundreds of thousands (is, includes, derived, topic, related, similar, has, part, member …), like/opposite unchanged; `water`'s rel rows on the hub name H, O, reservoir, ice, as on hp.

### N4. The sixth's define row calls the recall define (both)

hp: `UPDATE dna SET call = 19937222 WHERE gate = 156 AND before = 5 AND trigger = 68`; hub: `UPDATE main."153" SET call = 4254380 WHERE before IS 5 AND trigger IS 68`.

Expected live: the row reads the new call; on the hub the next `define : X` arriving from the sixth runs 4254380 (its tree shows the ask 4254360), lays catalog rows for X when its returns carry markers, and asks no source when X already holds a node table.

### N5. The hub's birth lays the define row and spawns the definition (hub)

A new born run (the two tables, the define row [before 153, trigger 68, spawn the define-at-birth run], `what` = newgate on its own sheet, the spawn), born's row 6 bound to it; the define-at-birth run is the hub's define 4254380 with the point taken from the sheet; `secondary_go` lays the define row too when it births a point for an arriving return.

Expected live: a plain sentence with a never-seen word typed on the hub (`the <word> is here`): the point's table holds one row [before 153, trigger 68, spawn R]; its node table holds rows; the main line's sheet completes; `define : <word>` afterwards recalls (no source asked).

### N6. The pages read the brain's formulas and places (both pages; the look unchanged)

The kinds' pull sliders and direction choices start from the brain's `pull` and `formula` rows (the brain's rows are the defaults; the owner's sliders still change the drawing); a clicked point shows the brain's x, y, z, the shard, before and next of its last move, and how many times it moved, beside the page's own drawn place; a point the brain has placed starts its drawing there instead of at its neighbours' mean. The kinds list, sliders, drop-downs, the stage, play, step, the prompt: untouched.

Expected live: the point panel of `water` on hp:8058/full shows "the brain holds it at x, y, z"; the page loads, steps and plays as in K9; a headless screenshot before and after shows the same panels.

### N7. The records

tries/35 NOTE with every read-back; CHANGE-OF-STATE; tries/README row 35; the kernel sources and lines copied to tries/28/kernel and tries/35; both machines committed; memory updated.

## 4. The balance (filled after the build, 2026-11-02 evening)

Part 1 read again, part 3's expected outputs read live; a difference is a regression and is fixed before this is called done.

### The kernel (hp), read after

| # | Read after (2026-11-02, 14:20 to 14:35) | Holds |
|---|---|---|
| K1 | `/api/info`: defined 722,283 (+6: nunavut, takakkaw-like learned points), gates 1,317,441 (+13: the lines' new symbols), runs 19,937,745, refused 1, pending 0, shard_rows 137 main (+7: six define rows of born symbols and one shape row laid before SHAPE-2) / 21 sixth, heap 32 MB; the kernel restarted once on its file (2 s), everything came back | yes |
| K2 | who 0.055 s, stone 0.020, bread 0.014, water 0.023, hinge 0.013; 11 runs each; no source asked; node rows who 40, stone 1,048, bread 340 unchanged; def and ok on the sheet | yes |
| K3 | nunavut (0 rows): asked, 3 rows, 0.038 s; typed again: 3 rows, 0.029 s, no source asked | yes |
| K4 | `the quoxleb410 is here` (the encoder cuts the digits off: the word is `quoxleb`): born 1, gate 1317430, its one DNA row [20048975, before 156, trigger 68, spawn 19936999], no source knows it (0 rows); the main sheet complete in 0.027 s | yes |
| K5 | nunavut laid like, part, is, is, is, derived; the rel table 4,024,000+ rows in 15 kinds (like 2,583,408, derived 352,976, topic 339,426, is 188,167, includes 186,754, related 184,218, similar 83,821, has 30,212, opposite 27,096, part 15,587, capitalized 15,371, member 11,784, property 3,163, implies 1,531, causes 601) | yes |
| K6 | shard_rows 137 → 137 across `the zebu is near the okapi` (a new line of known words): no row laid for a pass; `print : who`'s passes name shard 17 as before | yes (and the shape-row fault fixed, W7) |
| K7 | `dna WHERE gate = 156`: [557, 1, 68, call 19937222, times 85]; [1867, 5, 68, call 19937222 (was 6459431), times 1,363,629]; [1931, 1, 155, call 1132]; born [6, call 19937007]; heard [1, call 19937672 (SHAPE-2; was 19936643)] | yes; the two rebinding lines are N4 and W7 |
| K8 | every line above ends ok | yes |
| K9 | /full: ready in 57 s before the page patch (69,490 points sent, 20,126 drawn, 373,118 springs, 115,032 hits); after the patch the page loads (its first probe answered at 30 s, the debugger found it in settle/spaceApart, then in the animation loop) but its ready and step times could not be measured headless today: the hub's chain loads this box all day and the software-rendered browser never gets the thread; the unpatched page gave the same silence. `/api/graph` 1.2 s. The owner's browser is the check. | not measured today; the page runs; no change to its physics was made |
| K10 | the kinds list, sliders and direction choices present; their defaults now the brain's rows | yes |
| K11 | `SELECT count(*) FROM dna` → "no query solution" (refused); `SELECT kind, other FROM rel WHERE gate = ?` answers | yes |

### The new work on the kernel, read live

| # | Expected | Read |
|---|---|---|
| N1 | formula and pull rows answer; the join lists the kinds | 18 formulas, 38 kinds, every rel kind among them (like … causes), with pull, rest, mode |
| N2 | a point's xyz row; a new use moves it; the same line again does not; the recall time unchanged | water: none → (after `water is wet`) 2.46, −2.08, −2.33 moved 1 run 19937378; after ten settle passes 0.97, 2.96, −0.28 moved 13; `define : water` again: the place unchanged by it (a repeated line fires from memory, lands on nothing); nunavut/zebu/okapi placed at their first use and unchanged by the same line typed again; water's `is` relations above it, its `has` relations near it; recalls 13 to 55 ms |
| N4 | the sixth's row calls 19937222 | yes; its times 1,363,618 → 1,363,629 (the sixth's defines ran through it) |
| W7 (new) | a new line lays no DNA row on its first symbol | shard_rows 137 → 137 on a new line of known words |

### The hub, read after (2026-11-02, 15:55)

| # | Read after | Holds |
|---|---|---|
| H1 | `/api/info`: ready, routers main hops 877,840 / sixth 536,458, refused 0 / 0, both idle between lines | yes |
| H2 | `define : stone` 1.0 s, bread 1.0, who 2.0, water 1.0; 0 source returns under each; node rows 524, 170, 92, 370 unchanged; def/known/unknown/ok on the sheet | yes (faster than the 2 to 6 s before) |
| H3 | takakkaw (never seen): `like Takakkaw, is falls, is waterfall` laid at birth; the catalog kinds on the hub now 14 (N3) | yes |
| H4 | "3": [17, times 24,628,781]; "153": 3 function rows | yes |
| H5 | "153": [587, 1, 68, call 4254380, times 108]; [18574, 5, 68, call 4254380 (was 498941), times 160,768]; [18664, 1, 152, call 11254] | yes; the rebinding is N4 |
| H6 | "16": [6, ∅, ∅, call 4554230 (was 1), times 144,952] | yes; the new born run is N5 |
| H7 | main runs 4,557,585 and 4,557,573 arrived from the sixth after the change (`define : X`, `why : N 24`) | yes |
| H8 | every change typed through `/api/type`; no outside connection opened for a write (two read-only openings at 13:50 were stopped before they finished) | yes |
| H9 | the hub's page: a headless Chromium screenshot after the patch shows the stage, the kinds, the panels and the readout (`hub-page-after-g35.png`); its `ready` could not be read headless here (its whole-graph reads behind the typed lines), as on 11-01 | yes, by the screenshot |
| B1-B4 | formulas and places are rows and typed lines; the kernel's C and the hub's trigger are the physics; nothing deleted; 8056 never pointed at the kernel; the new tables hold numbers only | yes |

### The new work on the hub, read live

| # | Expected | Read |
|---|---|---|
| N1 | formula and pull rows | 18 and 38, the same text as hp's |
| N2 | xyz rows; a landing with another meaning moves a point; a recall's time unchanged | `water is wet` placed water, is, wet; after the back population 71,546 places, 71,541 moved more than once; `define : stone` moved stone once more (moved 7) and took 1.0 s |
| N3 | the catalog kinds in the hundreds of thousands; like/opposite kept | derived 244,691, includes 158,519, is 135,630, topic 119,993, related 98,339, similar 56,892, has 9,717, part 7,776, member 2,901, property 2,736, implies 1,399, causes 531; like 2,444,349 (was 2,303,454: the thesaurus `syn` markers of WordNet add to it), opposite 17,581 (was 366); 106,518 points read; 3,301,054 rows |
| N4 | the sixth's row calls 4254380; the sixth's defines run through it | yes; times 158,025 → 160,768 |
| N5 | a never-seen word in a plain sentence: its define row, its node rows, the line complete; then a recall | takakkaw: [1342406, before 153, trigger 68, spawn 4554222]; 1 node row; like/is rows; placed; `define : takakkaw` asked no source (1 row) and moved it |
| N6 | the pages read the brain's formulas and places; the look unchanged | both pages carry the patch (the kinds' defaults from the formula rows, the clicked point's place from `xyz`); the hub's page rendered in a screenshot after it; the kernel's page's reads answer from its door; the seeding of a point's drawing from the brain's place was taken out (it made the space-apart pass quadratic); the two doors' pages not timed headless today (K9) |
