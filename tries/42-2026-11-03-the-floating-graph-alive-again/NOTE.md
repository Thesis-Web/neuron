# tries/42 (2026-11-03, 03:20 to 03:50): the floating graph alive again

The owner, 2026-11-03 about 03:20 (in full in `STATE-BEGIN.md`): "no point on the nk graph moves?? the pulls and pushes are wrong or not
represented... take the word how... four different shards of how dna... each one means something a little different so when the shards
are hit the graph would move... we had this before but somehow it's gone now... the points are floating points held in tension by
relationships... right now only 8 relationship lines appear... they are supposed to be nearly translucent, like 10% value... turning off
one of the eight does nothing to the graph... there is an overlay mathematical graph that is static and does not move... the points move
through this graph... a specific neuron is pulled or pushed by its relationships... as the points move their relationship to the static
graph moves... operator neurons move a lot... then settle back... pull up the first tries of v5 v6 you will see the difference... this is
a worthless graph as it sits". The pasted geometry thread is the same text kept in tries/38 (`OWNER-REFERENCE-geometry-thread-2026-11-03.md`).

`STATE-BEGIN.md`, `OUTPUT-CONTRACT.md`, `STATE-END.md`, `DIFF.md` are the formula for this turn.

## Why nothing moved: two of my own choices, read from the code and the places

1. **The page froze the points on the brain's places (tries/37, mine).** With "the brain's places" on (the default), `settle()` set each
   point where the brain holds it and returned before the spring steps. v6 (tries/19) ran the springs every frame: every kind a spring
   with its pull, rest and direction, the points settling live, a kind's checkbox removing its pull. Since tries/37 a checkbox only hid
   lines, and nothing re-settled: the owner's "turning off one of the eight does nothing".
2. **The brain moves only the landed point, never its neighbours (tries/35, mine).** At a landing with a new shard the point moves 0.04 of
   its relationships' sum, capped at 6; the points its relationships name do not react until a `settle` pass over all 722k points is asked
   for (21 s). Read from the kernel's bundle at 01:02: of 65,933 points, 65,708 have moved exactly 14 times (the fourteen passes of 11-02)
   and 109 by landings. So the brain's places are a snapshot between passes, and the page drew that snapshot.
3. **The lines.** Drawn at 22 % (memory 10 %). The whole-brain bundle of the kernel's door caps rel rows at 1,200,000, which `like` fills
   (1,199,427 of them), so the old page showed three kinds; the light page of tries/41 reads rel rows by gate and showed 20 kinds on hp.

## Built: `page_patch10.py` (on top of tries/41's patch; both page files, originals beside it)

With "the brain's places" on: a point is seeded where the brain holds it, the page's springs run live every frame by the brain's formula
rows (pull, rest, direction per kind), a kind toggled off removes its springs and the points re-settle, a point the brain moved glides to
its new place and the springs re-settle around it; the quadratic space-apart pass stays off in this mode. Lines at 10 % (memory 5 %). The
switch's label says so. Off: the page's own springs from scratch, as before. Nothing of a brain or a door changed.

This is the drawing's tension, the owner's v6, seeded by the brain's geometry. It is not yet the brain's own tension.

## Seen, then judged wrong by the owner (03:45 to 04:02)

Headless with patch10: hp ready in 6 s, 1,465 points, 3,540 springs, 463 points moved in ten seconds, `alike` off → 365 moved again;
the hub 607 points, 583 moved, then 1,196 after the toggle; both pictures a tight ball with faint lines (`hp-tension-headless.png`,
`hub-tension-headless.png`). The owner, 03:55: "yeah that is wrong, and this is why... a runs shape through the neurons is it's pattern,
it's physical shape... if every run through the neurons is the same shape then a specific run has no pattern to match, based on context
alone this cannot happen... because context will change the shape of a run, as will mood, tense, modifiers, operators, context, concept,
multipliers (adjectives, singular, plural) <--- suffix and prefixes fit in all over here also... a root having a suffix or prefix will have
a different shape run than one not... but the root will shift a little because the prefix / suffix will change the meaning". The page's
springs give every kind one pull and one rest length, so every run settles into the same ball: no pattern. `page_patch10b` (04:02, both
doors) takes the springs back out of the brain's-places mode; the lines stay at 10 %; a point sits where the brain holds it and glides
when the brain moves it. The frozen picture is back until the brain makes the shapes.

## The brain's own tension (neuron C14, the real fix, the owner's word)

The owner's model: a point is pulled or pushed by its relationships; when a point moves, the points its relationships name move; a new
shard used on a point changes the directions of its pulls a little, so the point moves a little and so do its neighbours; an operator
point moves with the run (to the cells it checks) and settles back. The kernel's `nkxyz.c` moves one point per landing and stops. The
next piece in the brain: a landing's move also steps the points its relationships name, by their own pulls, a few rounds with decay, so
the neighbours react and the graph settles back without a whole pass; `/api/moved` already carries every move to the page. The operator
point moving with the run is a formula design to lay in the brain's rows (the owner's), not mine to invent. Built on the owner's word; a
kernel change (a rebuild and a 2 s restart on its file).
