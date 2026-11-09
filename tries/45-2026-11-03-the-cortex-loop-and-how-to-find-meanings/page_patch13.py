#!/usr/bin/env python3
# page_patch13.py (2026-11-03, tries/45): two counts on the page handle for the Cortex's C9 receipt (xyz entries held, memory nodes drawn).
# No change to the stage. Applies on top of page_patch12 (tries/44). usage: python3 page_patch13.py <page.html>
import sys, re
path = sys.argv[1]; t = open(path, encoding='utf-8').read()
m = re.search(r"window\.__poc = \{", t)
assert m, '__poc'
assert 'xyzHeld: function' not in t, 'already patched'
t = t[:m.end()] + " xyzHeld: function () { return Object.keys(XYZ).length; }, memNodes: function () { return Object.keys(NODE).filter(function (k) { return k.charAt(0) === 'm' && NODE[k].mesh && NODE[k].mesh.visible; }).length; }, relLines: function () { var n = 0; Object.keys(relSegs).forEach(function (k) { n += relSegs[k].pts.length / 2; }); return n; }," + t[m.end():]
# the survey of 17:50 (tries/45): under the newest 40 lines on the kernel, 231 called runs are returns (a reply like "ok", a source's returned
# text) with no statement; nine of them mention INTO or SELECT inside the returned text and were coloured as writes or reads. A branch run is
# a statement only when its text begins with BUILD or a statement word; otherwise it stays orange.
old = "    if (branch) { var kind = actionOf(hs.map(lab)) || 'branch'; hs.forEach(function (i) { ACT[i] = kind; }); return; }"
assert t.count(old) == 1, 'branch rule'
t = t.replace(old, "    if (branch) { var isStmt = false; for (var f = 0; f < 2 && f < hs.length; f++) { var first = String(lab(hs[f])).toUpperCase(); if (first === 'BUILD' || /^(INSERT|UPDATE|DELETE|SELECT|CREATE|WITH|REPLACE)$/.test(first)) isStmt = true; } var kind = (isStmt && actionOf(hs.map(lab))) || 'branch'; hs.forEach(function (i) { ACT[i] = kind; }); return; }   // tries/45: a return is not a statement; hop 0 of a called run is its arrival gate, so the statement word is looked for in the first two hops")
open(path, 'w', encoding='utf-8').write(t)
print('patched', path, ': __poc.xyzHeld, memNodes, relLines; a branch run is coloured only when its text is a statement')
