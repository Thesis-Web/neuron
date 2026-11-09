#!/usr/bin/env python3
# page_patch10b.py (2026-11-03 ~04:00, tries/42): the owner on patch10's result (03:55): "yeah that is wrong, and this is why... a runs shape
# through the neurons is it's pattern, it's physical shape... if every run through the neurons is the same shape then a specific run has no
# pattern to match... context will change the shape of a run, as will mood, tense, modifiers, operators, context, concept, multipliers...
# a root having a suffix or prefix will have a different shape run than one not". The page's generic springs (one pull and rest per kind)
# pulled every run into the same ball: taken back out of the brain's-places mode. What stays of patch10: lines at 10 %, the label. A point
# sits where the brain holds it and glides when the brain moves it; the shape is the brain's to make (neuron C14). Applies on top of patch10.
import sys
path = sys.argv[1]; t = open(path, encoding='utf-8').read()
old = "    if (brainLive) { Object.keys(NODE).forEach(function (k) { var n = NODE[k]; if (n.glide) { n.pos.lerp(n.glide, 0.25); if (n.pos.distanceTo(n.glide) < 0.05) { n.pos.copy(n.glide); n.glide = null; } } else if (n.unplaced && !n.mem && !n.ghost && brainPos(k, n)) {} }); placeNew(); }"
assert t.count(old) == 1, 'patch10 settle line'
t = t.replace(old, "    if (brainLive) { Object.keys(NODE).forEach(function (k) { var n = NODE[k]; if (n.glide) { n.pos.lerp(n.glide, 0.25); if (n.pos.distanceTo(n.glide) < 0.05) { n.pos.copy(n.glide); n.glide = null; } } else if (n.unplaced && !n.mem && !n.ghost && brainPos(k, n)) {} }); placeNew(); _apartMs = 0; return; }   // tries/42 (10b): no page springs here: they made every run the same ball (the owner, 03:55); the shape is the brain's")
old = "the brain's places (a point is seeded where the brain holds it, times the spacing, then held in tension by its lines' pulls, the brain's formula rows; when the brain moves it, it glides there; off: the page's own springs from scratch)"
if t.count(old) == 1: t = t.replace(old, "the brain's places (a point sits where the brain holds it, times the spacing, and glides when the brain moves it: the shape is the brain's pulls per shard, not the page's springs; off: the page's own springs, one shape for every run)")
open(path, 'w', encoding='utf-8').write(t); print('patched', path, ': the page springs out of the brain\'s-places mode again; lines stay at 10 %')
