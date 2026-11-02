#!/usr/bin/env python3
# g34/page_patch4.py (2026-11-01, 17:40). Measured with __poc.times(): at load, settle(30) over 365,737 springs took 57,880 ms (a new
# Vector3 for every term of every spring, 30 times); a step took 1,300 ms, 1,250 of it rebuilding the springs from 1.2 million relationship
# rows. Two changes, the same sums and the same drawing: (1) settle and spaceApart in three scratch vectors; (2) the relationship rows laid
# before the history's window (their lines depend only on which points exist and the space switch) are built once per change of that and
# merged into each render; the rows laid inside the window keep their per-hit rule.
import sys
D = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34/hp'
P = D + '/NEURON-POINT-OF-CONNECTION-nk-2026-10-30.html'
s = open(P, encoding='utf-8').read()
OLD_SETTLE = """  function settle(steps) {
    // springs only: no push between points, no pull toward any shell (owner, 2026-10-23). heard alone is fixed.
    for (var s = 0; s < steps; s++) {
      STEP++;
      SPRINGS.forEach(function (sp) { sp.a.f = sp.a.f || new THREE.Vector3(); sp.b.f = sp.b.f || new THREE.Vector3(); sp.a.f.set(0, 0, 0); sp.b.f.set(0, 0, 0); });
      SPRINGS.forEach(function (sp) {
        var f;
        if (sp.dir === 'across') {
          var ma = sp.b.pos.clone().negate().sub(sp.a.pos).multiplyScalar(sp.k * ACROSS), mb = sp.a.pos.clone().negate().sub(sp.b.pos).multiplyScalar(sp.k * ACROSS);
          if (!sp.a.fixed) sp.a.f.add(ma); if (!sp.b.fixed) sp.b.f.add(mb);
          var d0 = sp.b.pos.clone().sub(sp.a.pos), L0 = d0.length() || .01; f = d0.multiplyScalar(sp.k * (L0 - sp.rest) / L0 * .04);
        } else if (sp.dir) {
          f = sp.a.pos.clone().add(sp.dir.clone().multiplyScalar(sp.rest)).sub(sp.b.pos).multiplyScalar(-sp.k * .04);
        } else { var d = sp.b.pos.clone().sub(sp.a.pos), L = d.length() || .01; f = d.multiplyScalar(sp.k * (L - sp.rest) / L * .04); }
        if (!sp.a.fixed) sp.a.f.add(f); if (!sp.b.fixed) sp.b.f.sub(f);
      });
      // one scale for every point's step, never a cap per point (17.3): a cap per point breaks the balance of paired pulls
      var fl = []; SPRINGS.forEach(function (sp) { fl.push(sp.a.f.length(), sp.b.f.length()); }); fl.sort(function (a, b) { return a - b; });
      var p95 = fl.length ? fl[Math.floor(fl.length * .95)] : 0, sc = p95 > 4 ? 4 / p95 : 1;
      var mv = 0; SPRINGS.forEach(function (sp) { [sp.a, sp.b].forEach(function (n) { if (n.fixed || n.moved === STEP) return; n.moved = STEP; var s2 = n.f.clone().multiplyScalar(sc); if (s2.length() > 6) s2.setLength(6); n.pos.add(s2); if (s2.length() > mv) mv = s2.length(); }); }); LASTMOVE = mv;
      if (GAP > 0) for (var cp = 0; cp < PASSES; cp++) spaceApart();
    }
  }
"""
NEW_SETTLE = """  var _F = null, _D = null, _M = null, _FL = null;
  function settle(steps) {
    // springs only: no push between points, no pull toward any shell (owner, 2026-10-23). heard alone is fixed.
    // the same sums in three scratch vectors: a new vector per term over 365,737 springs took 58 s for 30 steps (2026-11-01)
    if (!_F) { _F = new THREE.Vector3(); _D = new THREE.Vector3(); _M = new THREE.Vector3(); }
    for (var s = 0; s < steps; s++) {
      STEP++;
      var n = SPRINGS.length, i, sp;
      for (i = 0; i < n; i++) { sp = SPRINGS[i]; sp.a.f = sp.a.f || new THREE.Vector3(); sp.b.f = sp.b.f || new THREE.Vector3(); sp.a.f.set(0, 0, 0); sp.b.f.set(0, 0, 0); }
      for (i = 0; i < n; i++) { sp = SPRINGS[i];
        if (sp.dir === 'across') {
          _M.copy(sp.b.pos).negate().sub(sp.a.pos).multiplyScalar(sp.k * ACROSS); if (!sp.a.fixed) sp.a.f.add(_M);
          _M.copy(sp.a.pos).negate().sub(sp.b.pos).multiplyScalar(sp.k * ACROSS); if (!sp.b.fixed) sp.b.f.add(_M);
          _D.copy(sp.b.pos).sub(sp.a.pos); var L0 = _D.length() || .01; _F.copy(_D).multiplyScalar(sp.k * (L0 - sp.rest) / L0 * .04);
        } else if (sp.dir) {
          _F.copy(sp.a.pos).addScaledVector(sp.dir, sp.rest).sub(sp.b.pos).multiplyScalar(-sp.k * .04);
        } else { _D.copy(sp.b.pos).sub(sp.a.pos); var L = _D.length() || .01; _F.copy(_D).multiplyScalar(sp.k * (L - sp.rest) / L * .04); }
        if (!sp.a.fixed) sp.a.f.add(_F); if (!sp.b.fixed) sp.b.f.sub(_F);
      }
      // one scale for every point's step, never a cap per point (17.3): a cap per point breaks the balance of paired pulls
      if (!_FL || _FL.length < 2 * n) _FL = new Float64Array(2 * n);
      var fl = _FL.subarray(0, 2 * n); for (i = 0; i < n; i++) { sp = SPRINGS[i]; fl[2 * i] = sp.a.f.length(); fl[2 * i + 1] = sp.b.f.length(); } fl.sort();
      var p95 = fl.length ? fl[Math.floor(fl.length * .95)] : 0, sc = p95 > 4 ? 4 / p95 : 1;
      var mv = 0; for (i = 0; i < n; i++) { sp = SPRINGS[i]; for (var w = 0; w < 2; w++) { var nd = w ? sp.b : sp.a; if (nd.fixed || nd.moved === STEP) continue; nd.moved = STEP; _M.copy(nd.f).multiplyScalar(sc); var ml = _M.length(); if (ml > 6) { _M.setLength(6); ml = 6; } nd.pos.add(_M); if (ml > mv) mv = ml; } } LASTMOVE = mv;
      if (GAP > 0) for (var cp = 0; cp < PASSES; cp++) spaceApart();
    }
  }
"""
OLD_APART = """        var d = n.pos.clone().sub(o.pos), L = d.length();
        if (L >= g) return;
        if (L < 1e-6) { d = unit('s' + n.key + '|' + o.key); L = 1e-6; }
        var push = d.normalize().multiplyScalar((g - L) / 2);
        n.pos.add(push); o.pos.sub(push);
"""
NEW_APART = """        _D.copy(n.pos).sub(o.pos); var L = _D.length();
        if (L >= g) return;
        if (L < 1e-6) { _D.copy(unit('s' + n.key + '|' + o.key)); L = 1e-6; }
        _D.normalize().multiplyScalar((g - L) / 2);
        n.pos.add(_D); o.pos.sub(_D);
"""
OLD_REL = "    REL.forEach(function (r) { if (!r[3] || RUNT0[r[3]] === undefined || RUNT0[r[3]] <= tk) add(r[0], r[2], relKind(r[1]), .8); });   // a rel row laid before this history's window is there from its start; one laid inside it appears with its run\n"
OLD_MAPL = "    if ($('mapall').checked && MAPL) MAPL.forEach(function (l) { var a = SYM[l[0]] !== undefined ? String(SYM[l[0]]) : null, b = SYM[l[2]] !== undefined ? String(SYM[l[2]]) : null; if (!a && !b) return; add(a || 'g:' + l[0], b || 'g:' + l[2], l[1], .8); });\n"
NEW_REL = ("    RELWIN.forEach(function (r) { if (RUNT0[r[3]] <= tk) add(r[0], r[2], relKind(r[1]), .8); });   // a rel row laid inside this history's window appears with its run\n"
           "    // the rel rows laid before the window are there from its start: their lines depend only on which points exist and the space switch, so they are built once per change of that and merged in (1.2 million rows a step otherwise)\n"
           "    var mapOn = $('mapall').checked && MAPL, ck = Object.keys(NODE).length + '|' + spaceOn;\n"
           "    if (RELCACHE.key !== ck) { var sagg = {}; RELSTATIC.forEach(function (r) { var a = String(r[0]), b = String(r[2]); if (a === b || !NODE[a] || !NODE[b]) return; if (!spaceOn && (a === String(G.space) || b === String(G.space))) return; var kind = relKind(r[1]), id = kind + '|' + (a < b ? a + '|' + b : b + '|' + a); if (!sagg[id]) sagg[id] = [a, b, kind, .8, 0]; sagg[id][4]++; }); RELCACHE = { key: ck, agg: sagg }; }\n"
           "    var sg = RELCACHE.agg; for (var sid in sg) { if (agg[sid]) agg[sid][4] += sg[sid][4]; else agg[sid] = mapOn ? sg[sid].slice() : sg[sid]; }\n")
OLD_VARS = "  var SPRINGS = [], ALLLINES = [], MEMROWS = [];\n"
NEW_VARS = "  var SPRINGS = [], ALLLINES = [], MEMROWS = [], RELSTATIC = [], RELWIN = [], RELCACHE = { key: null, agg: null };\n"
OLD_HOPC = "    HOPCOUNT = {}; R[8].forEach(function (r) { HOPCOUNT[r[0]] = r[1]; });\n"
NEW_HOPC = ("    RELSTATIC = []; RELWIN = []; RELCACHE = { key: null, agg: null }; REL.forEach(function (r) { if (!r[3] || RUNT0[r[3]] === undefined) RELSTATIC.push(r); else RELWIN.push(r); });   // laid before this history's window, or inside it\n"
            "    HOPCOUNT = {}; R[8].forEach(function (r) { HOPCOUNT[r[0]] = r[1]; });\n")
for old, new in [(OLD_SETTLE, NEW_SETTLE), (OLD_APART, NEW_APART), (OLD_REL + OLD_MAPL, NEW_REL + OLD_MAPL), (OLD_VARS, NEW_VARS), (OLD_HOPC, NEW_HOPC)]:
    assert s.count(old) == 1, (s.count(old), old[:100])
    s = s.replace(old, new)
open(P, 'w', encoding='utf-8').write(s); print('patched', P, 5)
