#!/usr/bin/env python3
# page_patch10.py (2026-11-03, tries/42): the floating graph alive again. The owner (03:20): "no point on the nk graph moves?? ... the points are
# floating points held in tension by relationships ... turning off one of the eight does nothing to the graph, the points are static?????
# that is not correct ... they are supposed to be nearly translucent .. like 10% value". Since tries/37 (mine) the page, with "the brain's
# places" on, set each point where the brain holds it and returned before its spring steps, so nothing moved and a kind's checkbox only hid
# lines. Now, with the switch on: a point is seeded where the brain holds it, the page's springs run live every frame by the brain's formula
# rows (as v6 did with its own), a kind toggled off removes its springs and the points re-settle, a point the brain moved glides there and
# the springs re-settle around it. The quadratic space-apart pass stays off in this mode (tries/35: it made the seeded drawing crawl). Lines
# at 10 % (memory 5 %). Applies on top of page_patch9 (tries/41). usage: python3 page_patch10.py <page.html>
import sys
path = sys.argv[1]; t = open(path, encoding='utf-8').read()
old = "    if (brainOn()) { Object.keys(NODE).forEach(function (k) { var n = NODE[k]; if (n.glide) { n.pos.lerp(n.glide, 0.25); if (n.pos.distanceTo(n.glide) < 0.05) { n.pos.copy(n.glide); n.glide = null; } } else if (n.unplaced && !n.mem && !n.ghost && brainPos(k, n)) {} }); placeNew(); _apartMs = 0; return; }"
assert t.count(old) == 1, 'settle brainOn branch'
new = "    var brainLive = brainOn();   // tries/42: the brain's places seed the points and its moves glide them; the springs run on regardless, so the lines' tension is live and a kind toggled off lets the points re-settle\n    if (brainLive) { Object.keys(NODE).forEach(function (k) { var n = NODE[k]; if (n.glide) { n.pos.lerp(n.glide, 0.25); if (n.pos.distanceTo(n.glide) < 0.05) { n.pos.copy(n.glide); n.glide = null; } } else if (n.unplaced && !n.mem && !n.ghost && brainPos(k, n)) {} }); placeNew(); }"
t = t.replace(old, new)
old = "if (GAP > 0) for (var cp = 0; cp < PASSES; cp++) spaceApart();"   # the hub's page has it bare, the kernel's timed
assert t.count(old) == 1, 'spaceApart line'
t = t.replace(old, "if (GAP > 0 && !brainLive) for (var cp = 0; cp < PASSES; cp++) spaceApart();   /* tries/42: no space-apart pass in the brain's-places mode (quadratic over the seeded cloud) */")
old = "opacity: sp.kind === 'memory' ? .1 : .22"
assert t.count(old) == 1, 'opacity'
t = t.replace(old, "opacity: sp.kind === 'memory' ? .05 : .1")
old = "the brain's places (a point sits where the brain holds it, times the spacing; it moves when the brain moves it; off: the page's own springs)"
if t.count(old) == 1:
    t = t.replace(old, "the brain's places (a point is seeded where the brain holds it, times the spacing, then held in tension by its lines' pulls, the brain's formula rows; when the brain moves it, it glides there; off: the page's own springs from scratch)")
else:
    print('note: the switch label text differs on this page; left as is')
open(path, 'w', encoding='utf-8').write(t)
print('patched', path, ': springs live under the brain\'s places, no space-apart in that mode, lines at 10 %')
