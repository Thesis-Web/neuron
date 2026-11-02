#!/usr/bin/env python3
# g34/page_patch3.py (2026-11-01, 17:25). Measured: with the relationship lines drawn (365,737 among 19,762 points) a step took 33 s and the
# load 118 s, the reads 3 s of it. Two changes to the page, no change to its look: (1) the render records the time of its phases (present
# set, springs, settle, segments) and __poc.times() reads them; (2) the composition table (a two-hop walk over every relationship line, for
# the side panel) is computed a quarter second after the last render instead of inside every step.
import sys
D = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34/hp'
P = D + '/NEURON-POINT-OF-CONNECTION-nk-2026-10-30.html'
s = open(P, encoding='utf-8').read()
pairs = [
    ("  function render(tk, keep) {\n",
     "  var TIMES = {}, compT = null;\n"
     "  function scheduleComposition(lines) { if (compT) clearTimeout(compT); compT = setTimeout(function () { compT = null; composition(lines); }, 250); }   // the side panel's table, after the step, not inside it\n"
     "  function render(tk, keep) {\n"),
    ("      LABLIST.forEach(function (g) { var k = String(g); if ((g === G.space && !spaceOn) || !present(g, atTk)) { hideNode(k); return; } var n = ensureNode(k); n.mesh.visible = true; if (n.label) n.label.visible = true; });\n",
     "      var _t0 = performance.now(); LABLIST.forEach(function (g) { var k = String(g); if ((g === G.space && !spaceOn) || !present(g, atTk)) { hideNode(k); return; } var n = ensureNode(k); n.mesh.visible = true; if (n.label) n.label.visible = true; });\n"),
    ("      var lines = buildSprings(atTk); composition(lines);\n      if (!keep) settle(30);\n",
     "      var _t1 = performance.now(); var lines = buildSprings(atTk); var _t2 = performance.now(); scheduleComposition(lines);\n      if (!keep) settle(30); var _t3 = performance.now();\n"),
    ("      relSegs = segs;\n",
     "      relSegs = segs; TIMES = { present: Math.round(_t1 - _t0), springs: Math.round(_t2 - _t1), settle: Math.round(_t3 - _t2), segs: Math.round(performance.now() - _t3), nsprings: SPRINGS.length, nlines: lines.length, npoints: Object.keys(NODE).length };\n"),
    ("  window.__poc = { ready: function () { return ready; },",
     "  window.__poc = { times: function () { return TIMES; }, ready: function () { return ready; },"),
]
for old, new in pairs:
    assert s.count(old) == 1, (s.count(old), old[:90])
    s = s.replace(old, new)
open(P, 'w', encoding='utf-8').write(s); print('patched', P, len(pairs))
