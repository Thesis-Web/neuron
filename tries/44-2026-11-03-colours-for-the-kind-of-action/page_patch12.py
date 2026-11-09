#!/usr/bin/env python3
# page_patch12.py (2026-11-03, tries/44): colours for the kind of action at a hop. The owner (16:40): "possible to add colors? like when
# writing memories, reading/ fetching data, adjusting state and time, or building new formulas, applying new found meanings... etc ?"
# The statement mother is handed is the symbols between two BUILD gates of the main run, or the whole text of a called or spawned run; its
# symbols say what it does. Each hop's vertex on the run's path carries its kind's colour; a legend under "runs drawn" counts the kinds in
# the run shown up to the tick; the HUD's hop line names the kind. Applies on top of page_patch11 (tries/43). usage: python3 page_patch12.py <page.html>
import sys, re
path = sys.argv[1]; t = open(path, encoding='utf-8').read()

# 1. the kinds, their colours, the classifier, the per-hop table, and routeI (route with the hop index kept)
old = "  var relSegs = {}, runPaths = [], flashPts = [], flashPts2 = [];\n"
assert t.count(old) == 1, 'relSegs line'
block = r"""  // tries/44: the kind of action at a hop (the owner, 16:40: "colors... when writing memories, reading/fetching data, adjusting state and
  // time, or building new formulas, applying new found meanings"). The statement mother is handed is the symbols between two BUILD gates of
  // the main run, or the whole text of a called or spawned run; its symbols say what it does. The write target names the kind first (a
  // memory written from a source read is a memory), then a bare read, then any other write. The typed line's own symbols stay white; a
  // branch run whose statement reads as none stays orange.
  var ACT_COL = { memory: 0x7ed07e, read: 0x6fa8dc, state: 0xffc98a, formula: 0x9b7bd4, meaning: 0x4fb7a8, sixth: 0xe09ab8, birth: 0xa9c3dc, write: 0xe8e2a0, line: 0xf2efe6, branch: 0xf28c4b };
  var ACT_NAME = { memory: 'writing a memory', read: 'reading a source', state: 'state and time', formula: 'binding a formula', meaning: 'applying a meaning', sixth: 'asking the sixth', birth: 'a birth', write: 'another write', line: 'the line itself', branch: 'a called or spawned run, no statement read' };
  var ACT_ORDER = ['memory', 'read', 'state', 'formula', 'meaning', 'sixth', 'birth', 'write', 'line', 'branch'];
  function actionOf(words) {   // the write target names the kind (INSERT ... INTO x, UPDATE x, DELETE FROM x); a statement with no target that reads is a read
    var w = []; words.forEach(function (s) { s = String(s).toLowerCase(); if (s.trim() !== '' && s !== '"' && s !== "'") w.push(s); });
    var target = null, schema = null;
    for (var i = 0; i < w.length - 1; i++) {
      if (w[i] === 'into' || w[i] === 'update' || (w[i] === 'from' && i > 0 && w[i - 1] === 'delete')) {
        target = w[i + 1]; if ((target === 'main' || target === 'sixth') && i + 3 < w.length && w[i + 2] === '.') { schema = target; target = w[i + 3]; } break;
      }
    }
    if (schema === 'sixth' || target === 'sixth') return 'sixth';
    if (target) {
      if (/^(run_memory|memory|remember)$/.test(target)) return 'memory';
      if (/^(third|told)$/.test(target)) return 'sixth';
      if (/^(run_sheet|clock|timeline|sheet|state)$/.test(target)) return 'state';
      if (/^(formula|pull|xyz|xyz_step|xyzforce|xyzbatch|dna|hop)$/.test(target) || /^\d+$/.test(target)) return 'formula';
      if (/^(rel|belief|tried|relmap|catalog|meaning)$/.test(target)) return 'meaning';
      if (/^(label|newgate|born)$/.test(target)) return 'birth';
      return 'write';
    }
    if (w.indexOf('select') >= 0) return 'read';
    return null;
  }
  var ACT = {};   // hop index in HIST -> kind; emptied when the history is read again
  function actsOfRun(rid) {
    var hs = RUNHOPS[rid] || []; if (!hs.length || ACT[hs[0]] !== undefined) return;
    var R = RUNS[rid], branch = R && R.kind !== 0, lab = function (i) { return LAB[HIST[i][2]] || ''; };
    if (branch) { var kind = actionOf(hs.map(lab)) || 'branch'; hs.forEach(function (i) { ACT[i] = kind; }); return; }
    hs.forEach(function (i) { ACT[i] = 'line'; }); var open = -1;
    for (var k = 0; k < hs.length; k++) { if (HIST[hs[k]][2] !== G.BUILD) continue; if (open < 0) { open = k; continue; } var span = hs.slice(open, k + 1), kind2 = actionOf(span.map(lab)) || 'write'; span.forEach(function (i) { ACT[i] = kind2; }); open = -1; }
  }
  function actCounts(rid, upto) { var o = {}; (RUNHOPS[rid] || []).forEach(function (i) { if (upto !== undefined && i > upto) return; var a = ACT[i] || 'line'; o[a] = (o[a] || 0) + 1; }); return o; }
  function hexAct(a) { return '#' + ('000000' + (ACT_COL[a] || 0x9aa3ad).toString(16)).slice(-6); }
  function renderActions(rid, upto) {
    var el = $('actions'); if (!el) return;
    if (rid === null || rid === undefined) { el.innerHTML = ''; return; }
    actsOfRun(rid); var c = actCounts(rid, upto), h = '';
    ACT_ORDER.forEach(function (a) { if (!c[a]) return; h += '<span style="white-space:nowrap"><span style="color:' + hexAct(a) + '">&#9632;</span> ' + ACT_NAME[a] + ' <span class="n">' + c[a] + '</span></span> &nbsp; '; });
    el.innerHTML = h || '<span class="f">no hop yet</span>';
  }
  function routeI(idx) { var out = [], skipSpace = !$('runspace').checked; idx.forEach(function (i) { var g = HIST[i][2]; if (skipSpace && g === G.space) return; var k = String(g); if (!out.length || k !== out[out.length - 1].k) out.push({ k: k, i: i }); }); return out; }
"""
t = t.replace(old, block + old)

# 2. the path keeps each hop's kind
old = "var ks = route(idx).filter(function (k) { return NODE[k] && NODE[k].mesh.visible; }); if (ks.length < 2) return; runPaths.push({ rid: rid, nodes: ks.map(function (k) { return NODE[k]; }), branch: RUNS[rid] && RUNS[rid].kind !== 0, cur: rid === runNow }); seen[rid] = 1; };"
assert t.count(old) == 1, 'addPath'
t = t.replace(old, "actsOfRun(rid); var kis = routeI(idx).filter(function (p) { return NODE[p.k] && NODE[p.k].mesh.visible; }); if (kis.length < 2) return; runPaths.push({ rid: rid, nodes: kis.map(function (p) { return NODE[p.k]; }), acts: kis.map(function (p) { return ACT[p.i] || 'line'; }), branch: RUNS[rid] && RUNS[rid].kind !== 0, cur: rid === runNow }); seen[rid] = 1; };   // tries/44: each hop's kind rides along")

# 3. the legend, rendered with the paths
old = "      Object.keys(NODE).forEach(function (k) { if (NODE[k].mesh) NODE[k].mesh.userData.hot = false; });\n"
assert t.count(old) == 1, 'hot reset line'
t = t.replace(old, "      renderActions(runNow, tk);   // tries/44: the kinds of action in the run shown, counted up to this tick\n" + old)

# 4. the drawing: one colour per vertex
m = re.search(r"runPaths\.forEach\(function \(rp\) \{ var line = new THREE\.Line\(.*?runGroup\.add\(line\); \}\);", t, flags=re.S)
assert m, 'runPaths drawing'
t = t[:m.start()] + "runPaths.forEach(function (rp) { var geo = new THREE.BufferGeometry().setFromPoints(rp.nodes.map(function (n) { return n.pos.clone().multiplyScalar(SP).add(unit('j' + rp.rid).multiplyScalar(1.2)); })); var cols = []; rp.nodes.forEach(function (n, j) { var c = new THREE.Color(ACT_COL[(rp.acts && rp.acts[j]) || (rp.branch ? 'branch' : 'line')]); cols.push(c.r, c.g, c.b); }); geo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); var line = new THREE.Line(geo, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: rp.cur ? 1 : .3 })); line.userData.run = rp.rid; runGroup.add(line); });   /* tries/44: each hop's vertex carries the colour of its kind of action */" + t[m.end():]

# 5. the HUD's hop line names the kind
old = "    var h = HIST[tk]; if (!h) return '';\n    var hs = RUNHOPS[h[1]] || [], i = hopIndex(tk), row = SHARDROW[h[3]];"
assert t.count(old) == 1, 'hopText head'
t = t.replace(old, "    var h = HIST[tk]; if (!h) return '';\n    actsOfRun(h[1]);   // tries/44\n    var hs = RUNHOPS[h[1]] || [], i = hopIndex(tk), row = SHARDROW[h[3]];")
old = "    if (h[2] === G.BUILD) s += ' · a BUILD gate';\n"
assert t.count(old) == 1, 'hopText BUILD'
t = t.replace(old, old + "    if (ACT[tk]) s += ' · ' + ACT_NAME[ACT[tk]];   // tries/44: the kind of action at this hop\n")

# 6. the legend's place in the panel
m = re.search(r'(<div class="row"><label for="runmode" class="note">runs drawn</label><select id="runmode">.*?</select></div>)', t, flags=re.S)
assert m, 'runmode row'
t = t[:m.end()] + '\n        <div id="actions" class="note" style="margin:3px 0 4px 0; line-height:1.6"></div>' + t[m.end():]

# 7. the table emptied when the history is read again
old = "RUNS = {}; CHILDREN = {}; RUNLIST = R[2].map("
assert t.count(old) == 1, 'absorb RUNS'
t = t.replace(old, "ACT = {}; " + old)

# 8. the handle for the headless check
m = re.search(r"window\.__poc = \{", t)
assert m, '__poc'
t = t[:m.end()] + " acts: function () { return CUR.run !== null ? actCounts(CUR.run, TK) : {}; }, actOf: function (i) { return ACT[i]; }, legend: function () { return ($('actions') || {}).textContent; }, paths: function () { return runPaths.map(function (rp) { var o = {}; (rp.acts || []).forEach(function (a) { o[a] = (o[a] || 0) + 1; }); return { run: rp.rid, vertices: rp.nodes.length, kinds: o, cur: rp.cur }; }); }," + t[m.end():]

open(path, 'w', encoding='utf-8').write(t)
print('patched', path, ': the run path coloured hop by hop by its kind of action; the legend under runs drawn; the HUD names the kind')
