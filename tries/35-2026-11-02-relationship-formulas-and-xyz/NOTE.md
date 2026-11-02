# tries/35 (2026-11-02): the relationship formulas as the brains' own rows, a point's x y z moved by its relationships, both brains

The owner, 2026-11-02 14:43: "part of your hydration needs to be focused on the edge at relationships... for both the hub and the kernal...
we need those relationship formulas built and deployed such that the build new neuron step can be the most complete it has been, take your
time, correct is more important than how fast you do it ... build an output contract first ... if you find anything wrong or incorrect it
becomes part of this turn also. but wrong has to be grounded in my prose ... do not break what we have."

The contract is `OUTPUT-CONTRACT.md` (written before the build; its part 4 is the balance). The prose this is built to is the owner's of
2026-11-01 23:40 (the build step of a new neuron; the relationship catalog; "each one of these relationships represents a mathmatical
formula that connects points to eachother and pushes or pulls points away or together ... the formulas are reuseable"; "the gates x,y,z
number is determinate on state and time"; "when a shard is used on a meaning point that point will likely move on the graph, unless the
shard being used has the same meaning as the last one used"), 10-24 ("the stronger the relationship the harder the pull ... the only word
with zero pull is origin"), and 10-23 ("how on earth can the gates ... the points not have x,y,z"). Everything below is read from the
running brains (hp 10.31.1.106:8058, socket 7007; the hub 8056). Nothing is a test.

## What was wrong, by the prose (the contract's part 2)

Neither brain held a point's x, y, z; the formulas (what a kind does to the points) lived only in the page's JavaScript; nothing in a
brain pushed or pulled a point. The hub's 183,618 defined points held like/opposite rows only. The sixth's define row on both brains still
called the old define (hp 6459431, 1,363,618 times; hub 498941, 158,025 times): every define the sixth asked re-asked the sources and laid
like/opposite only. The hub's birth laid the two tables and nothing else: no define row, no definition at birth. And one more, found on
the way: since SHAPE-nk (11-01), the per-line shape cell read the first symbol's DNA row by its full key, and the kernel's dna table lays
a row for a full-key read that finds none (so a binding UPDATE has a row to write), so every new line's first symbol got a pass row
(`water [20048973, before heard, trigger is]`, `the` three rows) which its landing then used instead of the hop shard: 12 rows since the
hop fold, against "the trigger to go the hop meaning points to the same shard of dna for all points".

## The formulas as rows (both brains)

`formula (id, pull, rest, dx, dy, dz, mode)` and `pull (kind, formula)`: a kind (a gate) names its formula; several kinds name one
("the same formula for a relationship like opposite or inverse"). Mode 0 a spring along the line toward the rest length; 1 directed, the
other point rest away along (dx, dy, dz); 2 across the origin. 18 formulas, 38 kinds: alike 1 (like, synonym); across the origin 2
(opposite, antonym, inverse, contradicts); the class above 3 (is, kind, class: +y); the member below 4 (includes: −y); close 5 (has,
part, supports); member 6; similar 7; related 8; derived 9; alias 10 (alias, capitalized); the consequence east 11 (implies, causes: +x);
the base form west 12 (past: −x); before east 13; after west 14; weak 15 (topic, context, category, method); use 16; property 17; the
forms 18 (prefix, suffix, stem, begins, ends, present, singular, plural). The numbers are the page's first table (tries/34, page_patch5),
carried into the brains so the brains hold them and a typed line changes them. Typed as `FORMULA-nk.txt` on hp (ledger
`LEDGER-FORMULA-nk.md`) and the same two lines on the hub (`hub_g35.py formula`). Live: `SELECT count(*) FROM formula` 18 and
`FROM pull` 38 on both; the join lists every kind with its pull, rest and mode.

## A point's x, y, z, moved by its relationships (both brains)

`xyz (gate, x, y, z, shard, before, next, at, run, moved)`: the point's place now; the shard last used on it and that use's before and
next symbols (the hop shard "accepts the before and remainder as two variables": the same shard with another before or next is another
use); the clock and run of the last move; how many times it moved. A landing on a point whose shard, before or next differ from its last
use reads the point's relationship rows both ways (`rel WHERE gate = ?` and `WHERE other = ?`, the key `rel_other` laid), applies each
through its kind's formula to the other point's place (mode 0: pull × (L − rest)/L along the line; 1: toward the other's place minus
rest × direction, the sign flipped for a row read from the other side; 2: across the origin plus the spring), sums, steps 0.04 of the sum
capped at 6, and records shard, before, next, clock, run, moved + 1. A point never placed starts at the mean of its placed relations plus
4 times a unit vector of its own, or the unit vector alone (the page's placeNew). The point `origin` (hp 2822, hub 757) sits at 0, 0, 0 and
is not moved. A repeated identical line fires from memory and lands on nothing: the same meaning again, no move (the rule as the owner
said it).

**On the kernel** this is the landing's physics in C (`nkxyz.c`, called from `land()` for every landing that is not the arrival, the
born hop or the space), reading the brain's own `rel`, `pull` and `formula` tables (the formulas re-read every two seconds, so a typed
change is seen); the places live in a side file beside the map, `out/brain.map.xyz` (40 bytes a gate, grown as gates are born), as the
brain's own SQLite tables sit beside it; read as the table `xyz` by gate (a keyless read is refused as every kernel table's is);
`UPDATE xyz SET x = , y = , z = WHERE gate = ` sets a place. The kernel request `settle N` is the back population, the long way once:
one step of every point that holds a definition or a place, per pass. The kernel was rebuilt and started again on its file (2 s; the
brain came back: defined 722,277, runs 19,937,323, refused 1, as before). `xyz_patch.py` is the change to nk.c, nk.h, nkvt.c, nkio.c,
serve8.py and run-on-hp.sh; backups `*.before-g35` on hp.

Live on hp: `water` held no place; `define : water` (a repeated line, fired from memory) left none; `water is wet` (a new line) placed
water at 2.46, −2.08, −2.33 and wet at 3.10, 1.66, 0.04, each `moved 1`, `run 19937378`, water's last use `shard 20048973, before heard,
next is` (that shard is one of the stray shape rows, see below), wet's `shard 17 (the hop), before is, next ∅`. `define : nunavut` (never
defined): asked, 3 node rows, relationships `like Nunavut, part Canada, is territory, is district, is dominion, derived abbreviation`,
placed (0.16, −0.22, −0.96, moved 1); typed again: 3 rows (no source asked), the place unchanged (the same shard, before and next).
`define : zebu` (defined before): recalled in 0.022 s, `is Brahman, is Brahma, is Brahmin, derived zebuine, related cattabu, member Bos`,
placed at its first use; again: 0.008 s, unchanged. Ten settle passes (`settle-g35.log`): 722,333 points, 722,213 placed in the first
pass (21.0 s), 722,332 moved in each of the next (21.0 s each). After them: water 0.97, 2.96, −0.28 (moved 13), stone −2.75, 11.64, −0.13,
bread 0.49, 6.56, 0.81, hinge −3.03, −0.23, −2.89, origin 0, 0, 0; water's `is` relations sit above it (element y 10.8, food 17.2, thing
11.6; water y 2.96), its `has` relations near it (reservoir −1.9, 0.2, 2.4; oxygen −4.9, −0.4, 0.3; hydrogen −5.4, 4.9, 0.8). A recall
after all this: who 0.055 s, stone 0.020, bread 0.014, water 0.023, hinge 0.013, 11 runs each, no source asked, node rows unchanged
(who 40, stone 1,048, bread 340).

**On the hub** it is the trigger `xyz_go AFTER INSERT ON hit` (the hub's SQL, `HUB-XYZ-v7.txt`, written by `hub_lines_gen.py` so the
law is written once for the hub's three lines): the same placement, the same pulls (the sum into the one-row table `xyz_step`, the capped
step applied), the same condition on shard, before (`hit.kb`) and next (`hit.kn`). Typed through the hub's prompt after its two reads were
run as plain reads on the live hub (the place read for water 0.017 s, the pulls read 0.006 s). Live: `water is wet` placed water
(0.14, 0.06, −0.99; shard 17, before heard, next is), is, wet (2.67, 1.15, −3.88); refused 0 / 0. The back population (`HUB-SETTLE-v7.txt`:
a placing line and a stepping line, 3,000 points each, typed until their batch is empty, `hub_g35.py settle 5`) ran after the
relationships below: 71,542 points placed (every point that is the `gate` of a relationship row; 25 lines, 174 s), then five passes of one
step each (25 lines a pass, 149 to 220 s a pass). My first stepping line moved nothing: its forces read named the batch inside a FROM
subquery (`FROM xyzbatch b , ( SELECT ... WHERE gate = b.g ) q`), which SQLite refuses ("no such column: b.g"; it has no lateral join), and
the line's reply carried the error while the batch cursor walked on; written again as two plain joins (`hub_lines_gen.py`), checked as a
read on the live hub (water's pull −62.9, 57.8, −9.6 before the cap; a batch of 3,000 in 0.81 s), and the five passes run again
(`hub-settle2.log`). After them: water −0.8, 7.6, −5.2 (moved 6), stone −1.8, 8.8, −1.7, bread 1.0, 3.3, −2.1, ice 7.6, −6.4, −0.7, hinge
−2.2, −0.9, 0.9, origin 0, 0, 0; water's `is` relations above it (thing y 9.3, element 11.3, food 13.2, supply 12.6, provide 19.3). Then
`define : stone`, `bread`, `who`, `water` typed: 1.0, 1.0, 2.0, 1.0 s (2 to 6 s before today), no source asked (0 returns under each,
node rows 524, 170, 92, 370 unchanged), each point moved once more by the landing (shard 17, before `:`, next ∅; moved 7). 71,546 places
in all, 71,541 moved more than once; the symbols of my typed lines moved most (one 40,427 times: a comma lands with another before and
next in every line).

## The hub's defined points get the catalog relationships; the sixth's define row; the hub's birth

**The catalog kinds on the hub.** The define's own marker span (HUB-RELS-v7.txt) over the WordNet and Wiktionary returns of 500 points
a line, keyed by `run.about` (the index `run_about`): measured 0.02 to 0.18 s a point as a plain read before, 500 points in about 7 s as
a typed line (`HUB-RELS-BACKPOP-v7.txt`, `relsdone` keeps the place, `hub_g35.py rels` types it until the batch is empty, 3 s between
lines so the chain and the owner get the router). Live, 214 lines, 2,616 s (6 to 10 s a line, two spikes while the pages were being read):
106,518 points read (every point with a WordNet or Wiktionary return), the rel table 2,592,414 → 3,301,054 rows; the kinds before: like
2,303,454, opposite 366, has 2, member 1; after: like 2,444,349, derived 244,691, includes 158,519, is 135,630, topic 119,993, related
98,339, similar 56,892, opposite 17,581, has 9,717, part 7,776, member 2,901, property 2,736, implies 1,399, causes 531 (14 kinds; the
hub's thesaurus rows never carried `capitalized`). `water` on the hub now `is thing, element, food, supply, fill, provide, fluid, liquid,
wet, facility, furnish, render`, as on hp.

**The sixth's define row** calls the recall define on both brains: hp `UPDATE dna SET call = 19937222 WHERE gate = 156 AND before = 5
AND trigger = 68` (`REBIND-g35-nk.txt`); the hub `UPDATE main."153" SET call = 4254380 WHERE before IS 5 AND trigger IS 68`. Live: hp's
row [1867, 5, 68, call 19937222], its times 1,363,618 → 1,363,629 by the end of the day (the sixth's own defines ran through it); the
hub's [18574, 5, 68, call 4254380], times 158,025 → 160,764 by 15:20 (the hub's chain kept typing its defines through it; refused 0 / 0
throughout). A define the sixth asks now answers from the point's own table when
it has one and lays the catalog relationships when it learns.

**The hub's birth** (`HUB-BORN-v7.txt`, `hub_g35.py born`): the define-at-birth run (the hub's define 4254380 with the point taken from
the sheet, `VALUES (above, 23, 1, what)`), the born run laid again (the two tables, the define row `[before 153, trigger 68, spawn the
define-at-birth run]` with the shard counter bumped, `what = newgate` on its own sheet, the spawn), born's row 6 bound to it (`main."16"`:
[6, ∅, ∅, call 4554230]); `secondary_go` lays the define row too when it births a point for an arriving return (the trigger before and
after in `hub-secondary_go-before/after-2026-11-02.sql`; the hub's trigger text 2,262 characters). Live: `the takakkaw is here`, a plain
sentence with a word the hub had never seen: gate 786913, its table's one row `[1342406, before 153, trigger 68, spawn 4554222, times 0]`,
one node row (WordNet), relationships `like Takakkaw, is falls, is waterfall`, placed (0.84, −0.11, −0.53); then `define : takakkaw`: no
source asked (1 node row), the place moved (moved 2: another before and next). Typing the born line itself replied "table newgate already
exists" and the define-at-birth line "no such column: above", as every BUILD line typed to be called does.

## The shape row (the fault found on the way)

`SHAPE-2-nk.txt`: the per-line run's shape cell reads the first symbol's DNA row with `before + 0 = 1 AND trigger + 0 = (next)`, keyed by
the gate alone, so the kernel's dna table lays nothing; heard's row calls it (19937672). Live: `the zebu is near the okapi` (known words,
a new line): shard_rows 137 → 137. The twelve rows laid before stay (water's [20048973, heard, is] among them: a landing on water after
heard and before is still uses it; deleting rows is the owner's word).

## The pages (the look unchanged)

`page_patch6.py` on both pages (the kernel's and the hub's): the kinds' pull sliders and direction choices start from the brain's `pull`
and `formula` rows (once per load; a slider or drop-down moved after that rules the drawing); a point the brain has placed starts its
drawing there instead of at its neighbours' mean; a clicked point's panel shows the brain's x, y, z, how many times it moved, the run,
clock, shard, before and next of its last move, beside the page's own drawn place. The kernel's door answers the two reads from the
bundle (`serve8.py`; the bundle carries `xyz` of the included points and the `formula` rows): `/api/graph` answers in 1.2 s with 64,858
points, 1,200,000 relationship rows, 64,920 places and 38 formula rows; the two reads the page adds answer from it.

A first form of the patch also started a point's drawing at the brain's place. The brain's places after ten passes of 0.04 a step sit
within a cube of some thirty units while the page's rest lengths are 10 to 64 and its space-apart grid 15: twenty thousand points seeded
into a few grid cells make the space-apart pass quadratic. Taken out again (`page_patch6b.py`): the page draws as before, the brain's
place is read on click.

**What the headless browser showed today.** The kernel's full page answered its first probe at 30 s (`the brains are open: 1,317,441
gates, 137 shards, 19,937,745 runs`), and paused with the debugger at 75 s it was inside `spaceApart` under `settle` under `render`, at
150 s in the door's fetch helper, at 240 s in `frame` (the animation loop): the page runs; it is 17.3's physics at work (the space-apart
pass, three a step, the page's cost as written on 11-01). Its ready time and a step's time could not be measured today: the hub's chain
runs on this box all day (load 3 to 6), and the software-rendered browser never gets the thread long enough to answer; the unpatched page
served for one probe gave the same silence (`probe-before.log`), the light page answered every five seconds (`probe-light.log`). The last
measurement with the box quiet stands: ready in 57 s with 69,490 points sent, 20,126 drawn, 373,118 springs (14:28, before the patch).
The hub's page rendered after its patch (`hub-page-after-g35.png`: the stage, the lines, the panels, the hit readout) but did not finish
its reads in 563 s with the box quiet (`hubafter2.log`): its door reads the whole graph (`read_graph`: every rel row), and the rel table
grew from 2.59 to 3.30 million rows today; on 11-01 the page opened in about 70 s with 2.3 million. The hub page's whole-graph read is
the hub door's design (the kernel's page reads a bundle); a cost of the back population, stated here, the owner's call. The page-scope
variables are not visible to the debugger's evaluate (the kernel page exports `__poc` for that; the hub page does not), so the sliders'
defaults were read from the DOM only (alike 1, is +y, opposite across, the same values as the brain's rows). The owner's browser is the
check of the sliders' defaults and the clicked point's place; the reads they make answer on both doors.

## Not done, and the owner's calls

- The "kind's own vector" direction (the mean displacement of a kind's pairs) is offered on the page and is not a brain formula (mode) yet.
- Triads and larger ("some are between multiply points a triad, or 4 or 5"): not laid; a formula over three or more points is the owner's call on which first.
- A point's history of places (every move as a row) is not kept: `xyz` holds the place now and the state and time of the last move.
- The twelve stray shape rows on hp stay (the owner's word on deleting rows).
- On the hub, a point born by a return before 11-02 holds no define row (the trigger lays it from now on).
- The hub's page: its `ready` could not be read in headless Chromium here (455 s before the patch, 710 s after, its whole-graph reads queued behind the typed lines), as on 11-01; the screenshot after the patch (`hub-page-after-g35.png`) shows the stage drawn, the kinds, the panels and the hit readout. The owner's browser is the check.
- The hub's step passes: the first stepping line's error went unseen for five passes because the loop read only the batch count, not the reply; the lines' replies are read now (hub_g35.py prints them).

## Files

`OUTPUT-CONTRACT.md`; `nkxyz.c`, `xyz_patch.py` (the kernel; the sources as they run in `tries/28/kernel`); `FORMULA-nk.txt`,
`REBIND-g35-nk.txt`, `SHAPE-2-nk.txt` and their ledgers; `settle-g35.log`; `hub_g35.py`, `hub_lines_gen.py`, `HUB-XYZ-v7.txt`,
`HUB-SETTLE-v7.txt`, `HUB-RELS-BACKPOP-v7.txt`, `HUB-BORN-v7.txt`, `hub-secondary_go-before/after-2026-11-02.sql`; `page_patch6.py`,
`hub-page-before-g35.html`, `cdp9.js`.
