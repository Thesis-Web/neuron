
  // ---- the view at a hit of the history (17.3's viewAt, from the receipt table): what the brain held then, and the hop being stepped
  function route(idx) { var out = [], skipSpace = !$('runspace').checked; idx.forEach(function (i) { var g = HIST[i][2]; if (skipSpace && g === G.space) return; var k = String(g); if (k !== out[out.length - 1]) out.push(k); }); return out; }
  var relSegs = {}, runPaths = [], flashPts = [], flashPts2 = [];
  function hopIndex(tk) { var h = HIST[tk]; if (!h) return -1; var hs = RUNHOPS[h[1]] || []; for (var i = 0; i < hs.length; i++) if (hs[i] === tk) return i; return -1; }
  function hopText(tk) {
    var h = HIST[tk]; if (!h) return '';
    var hs = RUNHOPS[h[1]] || [], i = hopIndex(tk), row = SHARDROW[h[3]];
    var s = 'hit ' + tk + ' of ' + (HIST.length - 1) + ' · run ' + h[1] + ', hop ' + i + ' of ' + (hs.length - 1) + ' · ' + nameOf(h[2]) + ' (gate ' + h[2] + ') · shard ' + h[3];
    if (row) s += ' · before ' + (row[2] === null ? '∅' : nameOf(row[2])) + ', trigger ' + (row[3] === null ? (i >= hs.length - 1 ? '∅ (the run ends here)' : '∅ (row 0: excited, not arrived at along the line)') : nameOf(row[3])) + (row[4] !== null ? ' · calls run ' + row[4] : '') + (row[5] !== null ? ' · spawns run ' + row[5] : '') + ' · times ' + row[6];
    else s += ' · (that shard is not in any DNA table now)';
    if (h[2] === G.BUILD) s += ' · a BUILD gate';
    return s;
  }
  function memRowsWanted() {
    var all = $('memall').checked;
    if (all) return q('SELECT run, gate, shard, input FROM main.run_memory ORDER BY run');
    if (CUR.root === null) return Promise.resolve([]);
    return q('SELECT m.run, m.gate, m.shard, m.input FROM main.run_memory m JOIN main.run r ON r.id = m.run WHERE r.root = ? OR r.id = ? ORDER BY m.run', [CUR.root, CUR.root]);
  }
  var memKey = null;
  function refreshMem(then) { var key = ($('memall').checked ? 'all' : 'root:' + CUR.root) + ':' + COUNTS.memory; if (key === memKey) { then(); return; } memRowsWanted().then(function (rows) { MEMROWS = rows; memKey = key; then(); }).catch(function () { then(); }); }
  function present(g, tk) { return g <= CORE || (FIRSTG[g] !== undefined && FIRSTG[g] <= tk); }
  function render(tk, keep) {
    if (!ready) return;
    if (tk === undefined || tk === null || tk < 0) tk = -1; if (tk > HIST.length - 1) tk = HIST.length - 1;
    TK = tk; var h = tk >= 0 ? HIST[tk] : null;
    var runNow = h ? h[1] : null; if (runNow !== CUR.run) { CUR.run = runNow; var R = RUNS[runNow]; CUR.root = R ? (R.root === null ? runNow : R.root) : null; renderTree(); if (!playing) renderRun(); else runStale = true; }
    if (hasGL) {
      var spaceOn = $('spacept').checked, gl = $('ghostlabels').checked, mapOn = $('mapall').checked && MAPL, atTk = tk < 0 ? -1 : tk;
      LABLIST.forEach(function (g) { var k = String(g); if ((g === G.space && !spaceOn) || !present(g, atTk)) { hideNode(k); return; } var n = ensureNode(k); n.mesh.visible = true; if (n.label) n.label.visible = true; });
      var memSeen = {}; if (RELSET.memory.on) MEMROWS.forEach(function (m) { if (RUNT1[m[0]] === undefined || RUNT1[m[0]] > atTk) return; var k = 'm:' + m[0]; memSeen[k] = 1; var n = ensureNode(k); n.mesh.visible = true; });
      var ghostSeen = {}; if (mapOn) MAPL.forEach(function (l) { var a = SYM[l[0]] !== undefined && present(SYM[l[0]], atTk), b = SYM[l[2]] !== undefined && present(SYM[l[2]], atTk); if (!a && !b) return; if (!a) ghostSeen['g:' + l[0]] = 1; if (!b) ghostSeen['g:' + l[2]] = 1; });
      Object.keys(ghostSeen).forEach(function (k) { var n = ensureNode(k); n.mesh.visible = true; if (n.label) n.label.visible = gl; });
      Object.keys(NODE).forEach(function (k) { if ((k.charAt(0) === 'm' && !memSeen[k]) || (k.charAt(0) === 'g' && !ghostSeen[k])) hideNode(k); });
      var lines = buildSprings(atTk); composition(lines);
      if (!keep) settle(30);
      var segs = {}; SPRINGS.forEach(function (sp) { if (!segs[sp.kind]) segs[sp.kind] = { pts: [], color: REL_COL[sp.kind] || 0x9aa3ad, opacity: sp.kind === 'memory' ? .1 : .22 }; segs[sp.kind].pts.push(sp.a.pos, sp.b.pos); });
      relSegs = segs;
      runPaths = []; var mode = $('runmode').value;
      if (mode !== 'none' && h) {
        var seen = {};
        var addPath = function (rid, upto) { var hs = RUNHOPS[rid] || [], idx = []; for (var i = 0; i < hs.length && hs[i] <= upto; i++) idx.push(hs[i]); var ks = route(idx).filter(function (k) { return NODE[k] && NODE[k].mesh.visible; }); if (ks.length < 2) return; runPaths.push({ rid: rid, nodes: ks.map(function (k) { return NODE[k]; }), branch: RUNS[rid] && RUNS[rid].kind !== 0, cur: rid === runNow }); seen[rid] = 1; };
        addPath(runNow, tk);
        if (mode === 'line' && CUR.root !== null) runsOfRoot(CUR.root).forEach(function (r) { if (!seen[r.id] && RUNT0[r.id] !== undefined && RUNT0[r.id] <= tk) addPath(r.id, tk); });
      }
      Object.keys(NODE).forEach(function (k) { if (NODE[k].mesh) NODE[k].mesh.userData.hot = false; });
      flashPts = []; flashPts2 = [];
      if (h && NODE[String(h[2])] && NODE[String(h[2])].mesh.visible) { var hn = NODE[String(h[2])]; hn.mesh.userData.hot = true; var row = SHARDROW[h[3]]; if (row) { if (row[3] !== null && NODE[String(row[3])] && NODE[String(row[3])].mesh.visible) flashPts.push([hn, NODE[String(row[3])]]); [row[4], row[5]].forEach(function (rr) { if (rr !== null && FIRST[rr] !== undefined && NODE[String(FIRST[rr])] && NODE[String(FIRST[rr])].mesh.visible) flashPts2.push([hn, NODE[String(FIRST[rr])]]); }); } }
      if (SELG !== null && NODE[String(SELG)] && NODE[String(SELG)].mesh.visible) NODE[String(SELG)].mesh.userData.hot = true;
    }
    var hs = h ? (RUNHOPS[h[1]] || []) : [], hi = h ? hopIndex(tk) : -1;
    $('readout').textContent = h ? 'hop ' + hi + ' of ' + (hs.length - 1) + ' in run ' + h[1] : 'hop 0 of 0';
    $('time').max = Math.max(0, hs.length - 1); $('time').value = Math.max(0, hi);
    $('hist').max = Math.max(0, HIST.length - 1); $('hist').value = Math.max(0, tk);
    $('histout').textContent = HIST.length ? 'hit ' + Math.max(0, tk) + ' of ' + (HIST.length - 1) + (tk < 0 ? ': before the first line, the hand-laid core alone' : tk === HIST.length - 1 ? ': the brain as it stands now' : '') : 'hit 0 of 0';
    if (h) { var ht = hopText(tk); $('now').innerHTML = '<span class="k">receipt row ' + h[0] + '</span><span>' + esc(ht) + '</span>'; $('hud').innerHTML = '<b>run ' + h[1] + ' · ' + esc(RUNS[h[1]] ? KINDNAME[RUNS[h[1]].kind] + ' from ' + nameOf(RUNS[h[1]].arrival) : '') + (lineOf(h[1]) ? ' · ' + esc(lineOf(h[1]).slice(0, 70)) : '') + '</b><span class="ev">' + esc(ht) + '</span>'; }
    else { $('now').innerHTML = '<span class="k">this hop</span><span>' + (HIST.length ? 'Before the first hit: the hand-laid core alone. Press play.' : 'No run yet. Type a line.') + '</span>'; $('hud').innerHTML = '<b>' + esc(COUNTS.label ? fmtN(COUNTS.label) + ' gates, ' + fmtN(COUNTS.shards) + ' shards, ' + fmtN(COUNTS.run) + ' runs, ' + fmtN(COUNTS.rel) + ' relationship rows' : 'reading the brain') + '</b>'; }
    renderLog(tk);
  }
  var fitLeft = 0, SP = 21, axesGroup = hasGL ? new THREE.Group() : null, axesL = 0, axesSP = 0; if (hasGL) scene.add(axesGroup);
  function drawAxes(force) {
    if (!hasGL) return;
    var on = $('axes').checked; axesGroup.visible = on; if (!on) return;
    var r = 30; Object.keys(NODE).forEach(function (k) { var n = NODE[k]; if (n.mesh && n.mesh.visible) r = Math.max(r, n.pos.length()); });
    var L = Math.ceil(r * 1.1 / 10) * 10;
    if (!force && L === axesL && SP === axesSP) return; axesL = L; axesSP = SP;
    while (axesGroup.children.length) { var c = axesGroup.children.pop(); if (c.geometry) c.geometry.dispose(); if (c.material) { if (c.material.map) c.material.map.dispose(); c.material.dispose(); } }
    [[0, 0xd9725f, 'x'], [1, 0x8fcf8f, 'y'], [2, 0x7fa8e0, 'z']].forEach(function (ax) {
      var pts = [], i = ax[0], e = function (v) { var p = new THREE.Vector3(); p.setComponent(i, v * SP); return p; };
      pts.push(e(-L), e(L));
      for (var t = -L; t <= L; t += 10) { if (t === 0) continue; var a = e(t), b = e(t), d = 1.2 * SP, o = (i + 1) % 3; a.setComponent(o, -d); b.setComponent(o, d); pts.push(a, b); }
      var line = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: ax[1], transparent: true, opacity: .28, depthTest: false })); line.renderOrder = 999; axesGroup.add(line);
      var col = '#' + ('000000' + ax[1].toString(16)).slice(-6);
      [['+' + ax[2], L], ['-' + ax[2], -L]].forEach(function (lb) { var s = makeLabel(lb[0], col, 14, true); s.material.opacity = .6; s.position.copy(e(lb[1] * 1.05)); s.renderOrder = 999; axesGroup.add(s); });
      for (var u = -L + 10; u < L; u += 10) { if (u === 0) continue; var s2 = makeLabel(String(u), col, 10, true); s2.material.opacity = .5; s2.position.copy(e(u)); s2.renderOrder = 999; axesGroup.add(s2); }
    });
  }
  function redrawLines() {
    if (!hasGL) return;
    var rs = {}; Object.keys(relSegs).forEach(function (k) { rs[k] = { pts: relSegs[k].pts.map(function (p) { return p.clone().multiplyScalar(SP); }), color: relSegs[k].color, opacity: relSegs[k].opacity }; }); drawLines(relGroup, rs);
    while (runGroup.children.length) { var c = runGroup.children.pop(); c.geometry.dispose(); c.material.dispose(); }
    runPaths.forEach(function (rp) { var line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(rp.nodes.map(function (n) { return n.pos.clone().multiplyScalar(SP).add(unit('j' + rp.rid).multiplyScalar(1.2)); })), new THREE.LineBasicMaterial({ color: rp.branch ? 0xf28c4b : 0xf2efe6, transparent: true, opacity: rp.cur ? 1 : .3 })); line.userData.run = rp.rid; runGroup.add(line); });
    var fp = []; flashPts.forEach(function (p) { fp.push(p[0].pos.clone().multiplyScalar(SP), p[1].pos.clone().multiplyScalar(SP)); }); flashGeo.dispose(); flashGeo = new THREE.BufferGeometry().setFromPoints(fp); flash.geometry = flashGeo; flash.visible = fp.length > 0;
    var fp2 = []; flashPts2.forEach(function (p) { fp2.push(p[0].pos.clone().multiplyScalar(SP), p[1].pos.clone().multiplyScalar(SP)); }); flashGeo2.dispose(); flashGeo2 = new THREE.BufferGeometry().setFromPoints(fp2); flash2.geometry = flashGeo2; flash2.visible = fp2.length > 0;
  }

  // ---- the hop log (the receipt of the run being stepped)
  function renderLog(tk) {
    var log = $('log'), h = HIST[tk]; if (!h) { log.innerHTML = '<div><span class="note">No run chosen.</span></div>'; return; }
    var hs = RUNHOPS[h[1]] || [], hi = hopIndex(tk), a = Math.max(0, hi - 30), b = Math.min(hs.length - 1, hi + 30), out = '';
    for (var i = a; i <= b; i++) { var e = HIST[hs[i]], row = SHARDROW[e[3]]; out += '<div class="' + (i === hi ? 'cur' : '') + '" data-t="' + hs[i] + '"><span class="t">' + i + '</span><span class="k">' + esc(nameOf(e[2])) + '</span><span>shard ' + e[3] + (row ? ': ' + esc(row[2] === null ? '∅' : nameOf(row[2])) + ' → ' + esc(row[3] === null ? '\u2205' : nameOf(row[3])) + (row[4] !== null ? ', calls ' + row[4] : '') + (row[5] !== null ? ', spawns ' + row[5] : '') + ' ×' + row[6] : '') + '</span></div>'; }
    log.innerHTML = out; var cur = log.querySelector('.cur'); if (cur) log.scrollTop = cur.offsetTop - log.clientHeight / 2 + cur.offsetHeight / 2;
  }
  $('log').addEventListener('click', function (e) { var d = e.target.closest('[data-t]'); if (d) { setPlay(false); render(parseInt(d.getAttribute('data-t'), 10), true); } });

  // ---- choosing a run: the history goes to its first hop (or the hop given)
  function runsOfRoot(root) { return RUNLIST.filter(function (r) { return r.root === root || r.id === root; }); }
  function depthOf(id) { var d = 0, r = RUNS[id]; while (r && r.parent !== null && RUNS[r.parent] && d < 40) { d++; r = RUNS[r.parent]; } return d; }
  function chooseRun(id, hop, then) {
    var R = RUNS[id]; if (!R) return; var hs = RUNHOPS[id] || [];
    CUR.run = id; CUR.root = R.root === null ? id : R.root;
    refreshMem(function () { renderTree(); renderRun(); render(hs.length ? hs[Math.min(hs.length - 1, hop || 0)] : TK, true); if (then) then(); });
  }
  function renderTree() {
    var el = $('tree'); if (CUR.root === null) { el.innerHTML = '<div><span class="note">No line chosen.</span></div>'; $('treesum').textContent = ''; return; }
    var kind = $('treekind').value, runs = runsOfRoot(CUR.root);
    var draw = function () { var h = '', shown = 0; runs.forEach(function (r) { if (kind !== 'all' && String(r.kind) !== kind) return; if (shown++ > 600) return; h += '<div class="' + (r.id === CUR.run ? 'last' : '') + '" data-run="' + r.id + '" style="padding-left:' + (7 + 10 * Math.min(6, depthOf(r.id))) + 'px"><span>' + r.id + '</span><span>' + esc(KINDNAME[r.kind]) + ' from ' + esc(nameOf(r.arrival)) + (r.cell !== null ? ' → cell ' + esc(nameOf(r.cell)) : '') + (r.about !== null ? ' about ' + esc(nameOf(r.about)) : '') + (lineOf(r.id) ? ': ' + esc(lineOf(r.id).slice(0, 48)) : '') + '</span><span class="m">' + (HOPCOUNT[r.id] ? fmtN(HOPCOUNT[r.id]) + ' hops' : '') + '</span></div>'; }); el.innerHTML = h || '<div><span class="note">No run of that kind.</span></div>'; var cur = el.querySelector('.last'); if (cur) el.scrollTop = cur.offsetTop - el.clientHeight / 2; };
    draw();
    var counts = {}; runs.forEach(function (r) { counts[r.kind] = (counts[r.kind] || 0) + 1; });
    $('treesum').textContent = runs.length + ' runs under root ' + CUR.root + ' (' + Object.keys(counts).map(function (k) { return counts[k] + ' ' + KINDNAME[k].replace(/^a /, '') + (counts[k] > 1 ? 's' : ''); }).join(', ') + ')';
    var root = CUR.root; decodeMany(runs.slice(0, 200).map(function (r) { return r.id; })).then(function () { if (CUR.root === root) draw(); });
  }
  $('tree').addEventListener('click', function (e) { var d = e.target.closest('[data-run]'); if (d) { setPlay(false); chooseRun(parseInt(d.getAttribute('data-run'), 10), 0); } });
  $('treekind').addEventListener('change', renderTree);

  // ---- a cell, read back through the encoder: what the page shows for a run_sheet value
  function isPointer(cell, v) { return POINTERS[cell] && v !== null && /^\d+$/.test(String(v)) && +v > 0 && RUNS[+v]; }
  function cellHTML(cell, v, state) {
    var name = LAB[cell] || ('#' + cell);
    if (state === 0 || v === null) return '<span class="e">∅ empty</span>';
    if (isPointer(cell, v)) { var R = RUNS[+v]; return '<span data-run="' + v + '" style="cursor:pointer;text-decoration:underline">run ' + v + '</span> <span class="f">from ' + esc(nameOf(R.arrival)) + ':</span> ' + replyHTML(lineOf(+v)); }
    if (cell === G.me || cell === G.above) return '<span data-run="' + esc(v) + '" style="cursor:pointer;text-decoration:underline">run ' + esc(v) + '</span>';
    if (cell === G.shape && /^\d+$/.test(String(v)) && +v > 0) return '<span data-run="' + esc(v) + '" style="cursor:pointer;text-decoration:underline">run ' + esc(v) + '</span> <span class="f">a formula used before</span>' + (lineOf(+v) ? ': ' + esc(lineOf(+v).slice(0, 60)) : '');
    if (name === 'known' || name === 'unknown') { var gs = String(v).trim().split(/\s+/).filter(Boolean); if (!gs.length) return '<span class="f">none</span>'; return gs.map(function (g) { return '<span data-gate="' + g + '" style="cursor:pointer">' + esc(nameOf(+g)) + '</span>'; }).join(', ') + ' <span class="f">(' + gs.length + ')</span>'; }
    if (/^\d+$/.test(String(v)) && LAB[+v] !== undefined && cell !== G.know) return '<span data-gate="' + esc(v) + '" style="cursor:pointer">' + esc(nameOf(+v)) + '</span> <span class="f">gate ' + esc(v) + '</span>';
    return esc(v);
  }
  function replyHTML(text) {
    if (text === null || text === undefined) return '<span class="f">(not read yet)</span>';
    if (text.indexOf('\n') < 0 && text.indexOf(' | ') < 0) return esc(text.length > 400 ? text.slice(0, 400) + '…' : text);
    var rows = text.split('\n').slice(0, 80), h = '<table class="cells" style="margin-top:3px">';
    rows.forEach(function (r) { h += '<tr>' + r.split(' | ').map(function (c) { return '<td>' + (c === '' ? '<span class="f">∅</span>' : /^\d+$/.test(c) && LAB[+c] !== undefined ? esc(c) + ' <span class="f">' + esc(nameOf(+c)) + '</span>' : esc(c.length > 160 ? c.slice(0, 160) + '…' : c)) + '</td>'; }).join('') + '</tr>'; });
    return h + '</table>' + (text.split('\n').length > 80 ? '<span class="f">… ' + text.split('\n').length + ' rows</span>' : '');
  }
  function cellsTable(rows) { return '<tr><th>cell</th><th>value, read back</th></tr>' + rows.map(function (c) { return '<tr><td' + (c[1] === 0 ? ' class="e"' : '') + '>' + esc(nameOf(c[0])) + ' <span class="f">' + c[0] + '</span></td><td>' + cellHTML(c[0], c[2], c[1]) + '</td></tr>'; }).join(''); }
  function pointerRuns(rows) { var out = []; rows.forEach(function (c) { if (isPointer(c[0], c[2])) out.push(+c[2]); if ((c[0] === G.shape) && /^\d+$/.test(String(c[2])) && +c[2] > 0) out.push(+c[2]); }); return out; }

  // ---- the run tab: the run row, its sheet, what went between the BUILDs and what came back, the gaps, the sources, the memory row
  function renderRun() {
    var id = CUR.run, R = RUNS[id]; if (!R) { $('runhead').innerHTML = '<span class="m">No run chosen.</span>'; return; }
    decodeRun(id).then(function (text) {
      var h = '<b>run ' + id + '</b><span class="m">' + esc(KINDNAME[R.kind]) + ' arriving from ' + esc(nameOf(R.arrival)) + (R.parent !== null ? ' · under run ' + R.parent : ' · a root') + ' · root ' + R.root + ' · at ' + R.at + (R.cell !== null ? ' · fills cell ' + esc(nameOf(R.cell)) : '') + (R.about !== null ? ' · about ' + esc(nameOf(R.about)) : '') + (HOPCOUNT[id] ? ' · ' + fmtN(HOPCOUNT[id]) + ' hops' : '') + '</span>';
      h += '<span class="mono">' + esc(text.slice(0, 600)) + (text.length > 600 ? ' … (' + fmtN(text.length) + ' characters)' : '') + '</span>';
      var kids = CHILDREN[id] || []; if (kids.length) h += '<span class="m">' + kids.length + (kids.length === 1 ? ' run under it' : ' runs under it') + ': ' + kids.slice(0, 14).map(function (k) { return '<span data-run="' + k + '" style="cursor:pointer;text-decoration:underline">' + k + '</span>'; }).join(', ') + (kids.length > 14 ? ' …' : '') + '</span>';
      $('runhead').innerHTML = h;
    });
    var draw = function (rows) {
      var ptrs = pointerRuns(rows);
      decodeMany(ptrs).then(function () { $('cells').innerHTML = rows.length ? cellsTable(rows) : '<tr><td class="f">Run ' + id + ' has no cells.</td></tr>'; });
      // between the BUILDs: the gates between two BUILD hits in this run's receipt, the holes filled from the sheets of this run, its parent and grandparent
      var fills = {}; var chain = [id, R.parent, R.parent !== null && RUNS[R.parent] ? RUNS[R.parent].parent : null].filter(function (x) { return x !== null && x !== undefined; });
      Promise.all(chain.map(function (r) { return SHEET[r] ? Promise.resolve(SHEET[r]) : q('SELECT cell, state, value FROM main.run_sheet WHERE run = ? ORDER BY cell', [r]).then(function (rr) { SHEET[r] = rr; return rr; }); })).then(function (sheets) {
        sheets.forEach(function (sh) { sh.forEach(function (c) { if (c[1] === 1 && fills[c[0]] === undefined) fills[c[0]] = c[2]; }); });
        var builds = [], hops = (RUNHOPS[id] || []).map(function (i) { return HIST[i]; }), open = -1;
        hops.forEach(function (hp, i) { if (hp[2] !== G.BUILD) return; if (open < 0) open = i; else { builds.push(hops.slice(open + 1, i).map(function (x) { return fills[x[2]] !== undefined ? String(fills[x[2]]) : (LAB[x[2]] !== undefined ? LAB[x[2]] : '#' + x[2]); }).join('')); open = -1; } });
        var replies = (CHILDREN[id] || []).filter(function (k) { return RUNS[k].kind === 3 && RUNS[k].arrival === G.mother; });
        decodeMany(replies).then(function () {
          var hb = ''; builds.forEach(function (t2, k) { hb += '<div class="gap" style="border-left-color:var(--accent)"><div class="q">' + esc(t2.trim().slice(0, 1200)) + (t2.length > 1200 ? ' …' : '') + '</div><div class="who">' + (replies[k] !== undefined ? 'mother answered in run <span data-run="' + replies[k] + '" style="cursor:pointer;text-decoration:underline">' + replies[k] + '</span>: ' : 'no answer run for this pair') + '</div>' + (replies[k] !== undefined ? '<div class="mono">' + replyHTML(lineOf(replies[k])) + '</div>' : '') + '</div>'; });
          $('builds').innerHTML = hb || '<span class="note">' + (hops.length ? 'No pair of BUILD gates in this run\'s receipt.' : 'Nothing yet.') + '</span>';
        });
      });
      var empty = rows.filter(function (c) { return c[1] === 0; });
      $('gaps').innerHTML = empty.length ? empty.map(function (c) { return '<div class="gap"><div>' + esc(nameOf(c[0])) + ' <span class="who">cell ' + c[0] + '</span></div><div class="who">declared, never filled: the run does not complete; the sixth is told and asks why</div></div>'; }).join('') : '<span class="note">' + (rows.length ? 'Every declared cell is filled.' : 'No cells.') + '</span>';
    };
    if (SHEET[id]) draw(SHEET[id]); else q('SELECT cell, state, value FROM main.run_sheet WHERE run = ? ORDER BY cell', [id]).then(function (rows) { SHEET[id] = rows; if (CUR.run === id) draw(rows); }).catch(function (e) { $('cells').innerHTML = '<tr><td class="e">' + esc(e.message) + '</td></tr>'; });
    // the sources, as this run heard them: the returns under it by arrival
    (function () {
      var about = null, byArr = {}; (CHILDREN[id] || []).forEach(function (k) { var K = RUNS[k]; if (K.kind === 3) { (byArr[K.arrival] = byArr[K.arrival] || []).push(k); if (K.about !== null) about = K.about; } });
      if (about === null && !Object.keys(byArr).length) { $('sources').innerHTML = '<div><span class="m">—</span><span>this run asked no source; its returns, if any, are under the line it is part of</span><span></span></div>'; return; }
      var h = about !== null ? '<div><span class="m">about</span><span><b>' + esc(nameOf(about)) + '</b> (gate ' + about + ')</span><span></span></div>' : '';
      SOURCES.forEach(function (s) { var ks = byArr[s[0]] || []; h += '<div' + (ks.length ? ' data-run="' + ks[0] + '"' : '') + '><span class="m">' + esc(s[1]) + '</span><span>' + (ks.length ? ks.length + ' return' + (ks.length > 1 ? 's' : '') + ': runs ' + ks.slice(0, 8).join(', ') + (ks.length > 8 ? ' …' : '') : '<span class="m">nothing came back</span>') + '</span><span class="m">' + esc(s[2]) + '</span></div>'; });
      if (byArr[G.mother]) h += '<div data-run="' + byArr[G.mother][0] + '"><span class="m">mother</span><span>' + byArr[G.mother].length + ' answer' + (byArr[G.mother].length > 1 ? 's' : '') + ': runs ' + byArr[G.mother].slice(0, 8).join(', ') + '</span><span class="m">the SQL prompt</span></div>';
      $('sources').innerHTML = h;
    })();
    q('SELECT m.input, m.source, m.gate, m.shard, m.at, t.id, t.key1, t.key2 FROM main.run_memory m LEFT JOIN main.timeline t ON t.run = m.run WHERE m.run = ?', [id]).then(function (rows) {
      var r = rows[0]; $('memrow').innerHTML = r ? '<span class="k">memory</span><span>on gate ' + r[2] + ' ' + esc(nameOf(r[2])) + ', shard ' + r[3] + ', at ' + r[4] + ', spoken by ' + esc(nameOf(r[1])) + '</span><span class="k">input</span><span class="mono">' + esc(String(r[0]).slice(0, 160)) + '</span><span class="k">timeline</span><span>row ' + r[5] + ' · key words ' + esc(nameOf(r[6])) + ', ' + esc(nameOf(r[7])) + '</span>' : '<span class="k">memory</span><span>this run has not ended: no memory row, no timeline row</span>';
    });
  }
  ['runhead', 'cells', 'builds', 'sources', 'out', 'sel', 'defrows', 'memrows', 'jobs', 'llist', 'sixthruns'].forEach(function (id) { $(id).addEventListener('click', function (e) { var d = e.target.closest('[data-run]'); if (d && d.getAttribute('data-run')) { setPlay(false); chooseRun(parseInt(d.getAttribute('data-run'), 10), 0); if (id !== 'out') showTab('panel-step'); return; } var g = e.target.closest('[data-gate]'); if (g) { showNode(parseInt(g.getAttribute('data-gate'), 10)); showTab('panel-sel'); } }); });

  // ---- what came out: the newest typed lines, each with its data sheet read back
  var SHOWN = [];   // the runs of the lines typed in this page, newest first
  function renderOut() {
    var el = $('out'); if (!SHOWN.length) { el.innerHTML = '<span class="note">Nothing typed yet in this page. The newest line\'s data sheet appears here, each cell read back through the encoder.</span>'; return; }
    var items = SHOWN.slice(0, 6);
    Promise.all(items.map(function (it) { return it.schema === 'sixth' ? Promise.resolve([]) : (SHEET[it.run] ? Promise.resolve(SHEET[it.run]) : q('SELECT cell, state, value FROM main.run_sheet WHERE run = ? ORDER BY cell', [it.run]).then(function (rows) { SHEET[it.run] = rows; return rows; })); })).then(function (sheets) {
      var ptrs = []; sheets.forEach(function (rows) { ptrs = ptrs.concat(pointerRuns(rows)); });
      return decodeMany(ptrs).then(function () { return sheets; });
    }).then(function (sheets) {
      el.innerHTML = items.map(function (it, i) {
        var rows = sheets[i], outs = OUTBY[it.run] || [], h = '<div class="sel" style="margin-bottom:8px"><b>' + esc(it.line.slice(0, 120)) + (it.line.length > 120 ? ' …' : '') + '</b><span class="m">' + (it.schema === 'sixth' ? 'the sixth\'s prompt' : 'the user\'s prompt') + ' · run <span data-run="' + it.run + '" style="cursor:pointer;text-decoration:underline">' + it.run + '</span>' + (it.r ? ' · ' + it.r.runs + ' runs, ' + fmtN(it.r.hits) + ' hits, ' + it.r.born + ' born, ' + it.r.seconds.toFixed(2) + ' s' + (it.r.refused ? ', <span class="e">' + it.r.refused + ' refused by SQLite</span>' : '') : '') + '</span>';
        if (it.schema === 'sixth') { h += '<span class="m">' + (it.r && it.r.out.length ? it.r.out.map(function (o) { return esc(o[0] + ' run ' + o[1] + ' · ' + o[2] + ': ' + o[3]); }).join('<br>') : 'the sixth\'s out mailbox got nothing') + '</span>'; return h + '</div>'; }
        if (rows.length) h += '<div class="tw"><table class="cells">' + cellsTable(rows) + '</table></div>';
        var others = {}; (it.r ? it.r.out : []).forEach(function (o) { if (o[0] === 'main' && o[1] !== it.run) others[o[1]] = 1; });
        var ok = Object.keys(others); if (ok.length) h += '<span class="m">also completed by this line, and said: run' + (ok.length > 1 ? 's ' : ' ') + ok.map(function (r) { return '<span data-run="' + r + '" style="cursor:pointer;text-decoration:underline">' + r + '</span>'; }).join(', ') + ' (an older run whose empty cell was filled now)</span>';
        if (!outs.length) h += '<span class="m">' + (rows.some(function (c) { return c[1] === 0; }) ? 'not complete: a declared cell is still empty, so nothing went to the out mailbox; the sixth is told' : 'the out mailbox got nothing from this run') + '</span>';
        return h + '</div>';
      }).join('');
    });
  }

  // ---- typing: a line goes through the door into the prompt's input table; the page waits, then reads the brain again
  var LAST = null;
  function send(line, prompt) {
    if (!ready || busy || !line) return; busy = true; var t0 = Date.now(); prompt = prompt || $('prompt').value;
    setBusy('the brain is running "' + line.slice(0, 80) + '"…');
    api('/api/type', { line: line, prompt: prompt }).then(function (j) { poll(j.id, t0, line, prompt); }).catch(function (e) { busy = false; setBusy('the door refused the line: ' + e.message); });
  }
  function poll(id, t0, line, prompt) {
    api('/api/job?id=' + id).then(function (j) {
      if (!j.done) { setBusy('the brain is running "' + line.slice(0, 60) + '": ' + Math.round((Date.now() - t0) / 1000) + ' s so far. A new word the sources hold takes a few seconds: every symbol of its definitions is born.'); setTimeout(function () { poll(id, t0, line, prompt); }, 500); return; }
      afterLine(j, line, prompt);
    }).catch(function () { setTimeout(function () { poll(id, t0, line, prompt); }, 2000); });
  }
  function afterLine(j, line, prompt) {
    loadBundle().then(function () {
      busy = false; LAST = j; var r = j.result;
      if (j.error || !r) { setBusy('the line stopped: ' + (j.error || 'no result')); return; }
      SHOWN.unshift({ line: line, schema: r.schema, run: r.run, r: r });
      setBusy('the line ran in ' + r.seconds.toFixed(2) + ' s: ' + r.runs + ' runs, ' + fmtN(r.hits) + ' hits, ' + r.born + ' born' + (r.refused ? ', ' + r.refused + ' refused by SQLite' : '') + '. ' + fmtN(COUNTS.label) + ' gates, ' + fmtN(COUNTS.shards) + ' shards in the brain now.');
      renderAll(); renderOut(); readLines();
      if (r.schema === 'main' && RUNS[r.run]) chooseRun(r.run, 0, function () { pickSpeed(r.hits); setPlay(true); }); else render(TK, true);
    }).catch(function (e) { busy = false; setBusy('the line ran, but the page could not read the brain again: ' + e.message); });
  }
  function typeLine() { var v = $('line').value.trim(); if (!v) return; var prompt = $('prompt').value; if (v.indexOf('6> ') === 0) { prompt = 'sixth'; v = v.slice(3); } $('line').value = ''; send(v, prompt); }
  $('run').addEventListener('click', typeLine); $('line').addEventListener('keydown', function (e) { if (e.key === 'Enter') typeLine(); });
  // the lines files: each line clicked goes into the prompt; nothing types a file by itself
  var LINESF = [];
  function readLines() { return api('/api/lines').then(function (j) { LINESF = j.lines || []; renderSheets(); }).catch(function (e) { $('tsheet').innerHTML = '<div><span></span><span class="m">' + esc(e.message) + '</span><span></span></div>'; }); }
  function renderSheets() {
    var hide = $('hidetyped').checked;
    ['tools', 'first'].forEach(function (which) {
      var el = $(which === 'tools' ? 'tsheet' : 'fsheet'), h = '';
      LINESF.filter(function (l) { return l.file === which; }).forEach(function (l, i) { if (hide && l.run) return; h += '<div data-i="' + LINESF.indexOf(l) + '" title="' + esc(l.note) + '"' + (l.run ? ' style="opacity:.6"' : '') + '><span>' + l.k + '</span><span>' + esc(l.line.length > 110 ? l.line.slice(0, 110) + '…' : l.line) + (l.note ? '<br><span class="m">' + esc(l.note.length > 150 ? l.note.slice(0, 150) + '…' : l.note) + '</span>' : '') + '</span><span class="m">' + (l.run ? 'run <span data-run="' + l.run + '">' + l.run + '</span>' : 'to the prompt') + '</span></div>'; });
      el.innerHTML = h || '<div><span></span><span class="m">' + (which === 'tools' ? 'LINES-v6.txt not found beside the brain' : 'FIRST-RUNS-v6 not found') + '</span><span></span></div>';
    });
  }
  $('hidetyped').addEventListener('change', renderSheets);
  ['tsheet', 'fsheet'].forEach(function (id) { $(id).addEventListener('click', function (e) { var r = e.target.closest('[data-run]'); if (r) { setPlay(false); chooseRun(parseInt(r.getAttribute('data-run'), 10), 0); showTab('panel-step'); return; } var d = e.target.closest('[data-i]'); if (!d) return; var l = LINESF[+d.getAttribute('data-i')]; if (!l) return; var line = l.line; if (line.indexOf('6> ') === 0) { $('prompt').value = 'sixth'; line = line.slice(3); } else $('prompt').value = 'main'; $('line').value = line; $('line').focus(); Array.prototype.forEach.call($(id).children, function (c) { c.classList.toggle('last', c === d); }); }); });
  function renderLines() {
    var h = '', rows = INPUTS.slice().reverse().slice(0, 120);
    decodeMany(rows.filter(function (x) { return x.schema === 'main'; }).map(function (x) { return x.run; })).then(function () {
      rows.forEach(function (x) { var outs = x.schema === 'main' ? (OUTBY[x.run] || []) : []; h += '<div class="' + (x.run === CUR.root && x.schema === 'main' ? 'last' : '') + '" data-run="' + (x.schema === 'main' ? x.run : '') + '"><span>' + x.run + '</span><span>' + esc(x.schema === 'main' ? (lineOf(x.run) || '').slice(0, 90) : 'a line at the sixth\'s prompt') + '</span><span class="m">' + (x.schema === 'sixth' ? 'sixth' : outs.length ? outs.length + ' cells out' : RUNS[x.run] && CHILDREN[x.run] ? 'not complete' : '') + '</span></div>'; });
      $('llist').innerHTML = h || '<div><span class="note">Nothing typed yet.</span></div>';
    });
  }
  $('fresh').addEventListener('click', function () { if (!ready || busy) return; if (!confirm('Lay both eggs and the source brains again? The brains as they stand are overwritten in the brain folder.')) return; busy = true; setBusy('laying the eggs…'); api('/api/fresh', {}).then(function (j) { var p2 = function () { api('/api/job?id=' + j.id).then(function (x) { if (!x.done) { setTimeout(p2, 500); return; } busy = false; if (x.error) { setBusy('error: ' + x.error); return; } HIST = []; RUNHOPS = {}; FIRSTG = {}; FIRSTS = {}; RUNT0 = {}; RUNT1 = {}; HISTLAST = 0; TK = -1; SHEET = {}; TEXT = {}; CUR = { root: null, run: null }; SHOWN = []; Object.keys(NODE).forEach(function (k) { hideNode(k); }); loadBundle().then(function () { renderAll(); renderOut(); readLines(); render(-1); setBusy('fresh brains: the bare core. Type the lines under Type, one at a time.'); }); }); }; p2(); }).catch(function (e) { busy = false; setBusy(e.message); }); });

  // the speed for a line just typed: the one that plays its hits in about twenty seconds, from the choices offered, never faster than 600 a second
  function pickSpeed(hits) { var want = Math.max(8, (hits || 0) / 20), opts = [2, 8, 30, 120, 600], v = 600; for (var i = 0; i < opts.length; i++) if (opts[i] >= want) { v = opts[i]; break; } $('speed').value = String(v); }
  // ---- transport: the history is stepped hit by hit; play goes on through the brain's order, into the next run, unless told to stay in this run
  var playing = false, acc = 0, runStale = false;
  function setPlay(v) { playing = v; $('play').setAttribute('aria-pressed', String(v)); $('play').textContent = v ? 'pause' : 'play'; if (!v && runStale) { runStale = false; renderRun(); } }
  $('back').addEventListener('click', function () { setPlay(false); if (TK > -1) render(TK - 1, true); });
  $('fwd').addEventListener('click', function () { setPlay(false); advance(1); });
  $('play').addEventListener('click', function () { setPlay(!playing); if (playing && TK >= HIST.length - 1) render(-1, true); });
  $('time').addEventListener('input', function () { setPlay(false); var hs = CUR.run !== null ? (RUNHOPS[CUR.run] || []) : []; var i = parseInt($('time').value, 10); if (hs.length) render(hs[Math.min(hs.length - 1, Math.max(0, i))], true); });
  $('hist').addEventListener('input', function () { setPlay(false); render(parseInt($('hist').value, 10), true); });
  $('tostart').addEventListener('click', function () { setPlay(false); render(-1, true); userZoomed = false; fitLeft = 120; });
  $('tonow').addEventListener('click', function () { setPlay(false); render(HIST.length - 1, true); userZoomed = false; fitLeft = 120; });
  var spinning = false; $('spin').addEventListener('click', function () { spinning = !spinning; $('spin').setAttribute('aria-pressed', String(spinning)); });
  function advance(k) {
    if (TK >= HIST.length - 1) { setPlay(false); return; }
    var nt = Math.min(HIST.length - 1, TK + k);
    if (!$('followrun').checked && CUR.run !== null) { var hs = RUNHOPS[CUR.run] || [], last = hs.length ? hs[hs.length - 1] : TK; if (TK >= last) { setPlay(false); return; } nt = Math.min(nt, last); }
    render(nt, true);
  }
