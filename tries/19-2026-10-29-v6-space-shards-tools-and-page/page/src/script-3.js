
  // ---- selected: a gate read in full from the brain's tables
  function showNode(g) {
    if (LAB[g] === undefined) return; SELG = g; var role = roleOf(g);
    var h = '<b>' + esc(nameOf(g)) + '</b><span class="m">gate ' + g + ' · ' + esc(ROLETEXT[role] || role) + (hasCall(g) ? ' · a shard of it calls or spawns a run' : '') + '</span>';
    var lineBy = {}; ALLLINES.forEach(function (l) { if (l[0] === String(g) || l[1] === String(g)) lineBy[l[2]] = (lineBy[l[2]] || 0) + 1; });
    h += '<span class="m">lines: ' + (Object.keys(lineBy).length ? Object.keys(lineBy).sort().map(function (k) { return esc(k) + ' ' + lineBy[k]; }).join(', ') : 'none') + '</span>';
    h += '<span class="m">' + (NODES[g] || 0) + ' definition rows · ' + ((RELBY[g] || []).length) + ' relationship rows · ' + (MEMN[g] || 0) + ' memory nodes · ' + ((DNABY[g] || []).length) + ' DNA rows</span>';
    var n = NODE[String(g)]; if (n && n.mesh && n.mesh.visible) h += '<span class="m">drawn at ' + n.pos.x.toFixed(1) + ', ' + n.pos.y.toFixed(1) + ', ' + n.pos.z.toFixed(1) + ' (the page\'s drawing, not the brain\'s)</span>';
    h += '<span class="m" id="bornin">' + (g > CORE ? 'reading the run that bore it…' : 'laid by hand in the egg, before any line') + '</span>';
    $('sel').innerHTML = h;
    if (g > CORE) q('SELECT run FROM main.run_sheet WHERE cell = ? AND value = ? ORDER BY run LIMIT 1', [G.newgate, String(g)]).then(function (r) { var el = $('bornin'); if (!el || SELG !== g) return; if (!r.length) { el.textContent = 'born: no line\'s newgate cell names it (born by a typed line whose cell was overwritten, or by a return)'; return; } el.innerHTML = 'born inline in run <span data-run="' + r[0][0] + '" style="cursor:pointer;text-decoration:underline">' + r[0][0] + '</span>' + (lineOf(r[0][0]) ? ': ' + esc(lineOf(r[0][0]).slice(0, 80)) : ''); decodeRun(r[0][0]).then(function (t2) { if (SELG === g && el.isConnected) el.innerHTML = 'born inline in run <span data-run="' + r[0][0] + '" style="cursor:pointer;text-decoration:underline">' + r[0][0] + '</span>: ' + esc(t2.slice(0, 80)); }); });
    var rows = DNABY[g] || [], hd = '<tr><th>shard</th><th>before</th><th>trigger</th><th>call</th><th>spawn</th><th>times</th></tr>';
    rows.forEach(function (r) { hd += '<tr><td>' + r[1] + '</td><td>' + (r[2] === null ? '<span class="f">∅</span>' : esc(nameOf(r[2])) + ' <span class="f">' + r[2] + '</span>') + '</td><td>' + (r[3] === null ? '<span class="f">∅ end</span>' : esc(nameOf(r[3])) + ' <span class="f">' + r[3] + '</span>') + '</td><td>' + (r[4] === null ? '' : '<span class="ok" data-run="' + r[4] + '" style="cursor:pointer;text-decoration:underline">run ' + r[4] + '</span>') + '</td><td>' + (r[5] === null ? '' : '<span class="ok" data-run="' + r[5] + '" style="cursor:pointer;text-decoration:underline">run ' + r[5] + '</span>') + '</td><td>' + r[6] + '</td></tr>'; });
    $('dnarows').innerHTML = rows.length ? hd + '<tr><td colspan="6" class="f">table "' + g + '": ' + rows.length + ' DNA rows; a row is keyed by the symbol before and the symbol the run goes on to, the space skipped (v6)</td></tr>' : '<tr><td class="f">table "' + g + '" holds no DNA rows: no run has landed here yet</td></tr>';
    $('defrows').innerHTML = '<div><span class="m">…</span><span>reading "' + g + '.node"</span><span></span></div>';
    q('SELECT id, source, run FROM main."' + g + '.node" ORDER BY id').then(function (nr) {
      if (SELG !== g) return;
      if (!nr.length) { $('defrows').innerHTML = '<div><span class="m">none</span><span>no return has landed here: ' + (g > CORE ? 'define : ' + esc(nameOf(g)) + ' has not been typed, or no source holds it' : 'a hand-laid neuron no line has defined') + '</span><span></span></div>'; return; }
      decodeMany(nr.map(function (r) { return r[2]; })).then(function () { if (SELG !== g) return; $('defrows').innerHTML = nr.map(function (r) { return '<div data-run="' + r[2] + '"><span class="m">' + r[0] + '</span><span><b>' + esc(SRCNAME[r[1]] || nameOf(r[1])) + '</b>: ' + esc((lineOf(r[2]) || '').slice(0, 220)) + '</span><span class="m">run ' + r[2] + '</span></div>'; }).join(''); });
    }).catch(function () { $('defrows').innerHTML = '<div><span class="m">?</span><span>no node table named "' + g + '.node"</span><span></span></div>'; });
    var rels = RELBY[g] || [];
    $('relrows').innerHTML = rels.length ? rels.map(function (r) { return '<div data-run="' + r[3] + '"><span class="m">' + esc(relKind(r[1])) + '</span><span>' + esc(nameOf(r[0])) + ' <b>' + esc(nameOf(r[1])) + '</b> ' + esc(nameOf(r[2])) + '</span><span class="m">from run ' + r[3] + '</span></div>'; }).join('') : '<div><span class="m">none</span><span>no rel row names this gate</span><span></span></div>';
    q('SELECT run, shard, at, input FROM main.run_memory WHERE gate = ? ORDER BY run DESC LIMIT 60', [g]).then(function (mr) { if (SELG !== g) return; $('memrows').innerHTML = mr.length ? mr.map(function (r) { return '<div data-run="' + r[0] + '"><span class="m">' + r[1] + '</span><span>run ' + r[0] + ' ended on shard ' + r[1] + ' at ' + r[2] + ' · line as gates: ' + esc(String(r[3]).slice(0, 60)) + '</span><span class="m">memory</span></div>'; }).join('') + (mr.length === 60 ? '<div><span></span><span class="m">the newest 60 of ' + (MEMN[g] || 0) + '</span><span></span></div>' : '') : '<div><span class="m">none</span><span>no run has ended at this neuron</span><span></span></div>'; });
    render(TK, true);
  }

  // ---- the neurons tab: every gate in label
  function renderNeurons() {
    var find = $('nfind').value.trim().toLowerCase(), role = $('nrole').value, h = '', n = 0, c = { core: 0, born: 0, call: 0, node: 0 };
    LABLIST.forEach(function (g) {
      var r = roleOf(g), isCore = g <= CORE, hc = hasCall(g), nd = NODES[g] > 0; if (isCore) c.core++; else c.born++; if (hc) c.call++; if (nd) c.node++;
      var s = LAB[g]; if (find && s.toLowerCase().indexOf(find) < 0) return;
      if (role === 'core' && !isCore) return; if (role === 'born' && isCore) return; if (role === 'call' && !hc) return; if (role === 'node' && !nd) return; if (role === 'rel' && !(RELBY[g] || []).length) return; if (role === 'source' && r !== 'source') return;
      if (n++ > 2500) return;
      var dr = (DNABY[g] || []).length, df = NODES[g] || 0, rl = (RELBY[g] || []).length, mm = MEMN[g] || 0;
      h += '<div class="' + (g === SELG ? 'last' : '') + '" data-gate="' + g + '"><span>' + g + '</span><span>' + esc(nameOf(g)) + ' <span class="m">' + (r === 'core' || r === 'born' ? (hc ? 'with a call' : r) : r) + '</span></span><span class="m">' + (dr ? dr + ' dna' : '') + (df ? (dr ? ', ' : '') + df + ' def' : '') + (rl ? ', ' + rl + ' rel' : '') + (mm ? ', ' + mm + ' mem' : '') + '</span></div>';
    });
    $('nlist').innerHTML = h || '<div><span class="note">No gate matches.</span></div>';
    $('nsum').textContent = fmtN(LABLIST.length) + ' gates: ' + c.core + ' hand-laid, ' + fmtN(c.born) + ' born, ' + c.call + ' with a call or spawn, ' + c.node + ' with definition rows; ' + n + ' shown';
  }
  $('nfind').addEventListener('input', renderNeurons); $('nrole').addEventListener('change', renderNeurons);
  $('nlist').addEventListener('click', function (e) { var d = e.target.closest('[data-gate]'); if (d) { showNode(parseInt(d.getAttribute('data-gate'), 10)); renderNeurons(); showTab('panel-sel'); } });

  // ---- the brains tab
  function renderBrain() {
    var items = [[COUNTS.label, 'gates in the encoder'], [COUNTS.tables, 'tables'], [COUNTS.triggers, 'triggers (physics)'], [COUNTS.shards, 'shards, one sequence'], [COUNTS.run, 'runs'], [COUNTS.receipts, 'hits (receipt rows)'], [COUNTS.memory, 'memories'], [COUNTS.timeline, 'timeline rows'], [COUNTS.sheet, 'cells'], [COUNTS.rel, 'relationship rows'], [COUNTS.returns, 'source returns'], [COUNTS.empty, 'cells still empty'], [COUNTS.unended, 'runs without an end'], [COUNTS.refused, 'refused by SQLite'], [COUNTS.hop, 'in the hop table now']];
    $('counts').innerHTML = items.map(function (it) { return '<div class="stat"><b>' + fmtN(it[0]) + '</b><span>' + it[1] + '</span></div>'; }).join('');
    var kv = INFO ? [['brain', INFO.brain], ['sixth', INFO.sixth], ['sources', INFO.sources], ['SQLite', INFO.sqlite]] : [];
    $('binfo').innerHTML = kv.map(function (x) { return '<span class="k">' + esc(x[0]) + '</span><span style="overflow-wrap:anywhere">' + esc(x[1]) + '</span>'; }).join('');
    // sources: asked = the define lines' asks (returns by arrival; silent = asked about a symbol and sent nothing, counted from the runs that asked)
    var asked = {}, ret = {}, silent = {}; RUNLIST.forEach(function (r) { if (r.kind === 3 && r.arrival >= 7 && r.arrival <= 15) { ret[r.arrival] = (ret[r.arrival] || 0) + 1; (asked[r.arrival] = asked[r.arrival] || {})[r.about] = 1; } });
    var abouts = {}; RUNLIST.forEach(function (r) { if (r.kind === 3 && r.about !== null && r.arrival >= 7 && r.arrival <= 14) abouts[r.about] = 1; }); var nAbout = Object.keys(abouts).length;
    var ht = '<tr><th>source</th><th>symbols answered</th><th>lines returned</th><th>silent on</th></tr>';
    SOURCES.forEach(function (s) { var na = Object.keys(asked[s[0]] || {}).length; ht += '<tr><td>' + esc(s[2]) + ' <span class="f">' + esc(s[1]) + '</span></td><td>' + na + '</td><td class="ok">' + (ret[s[0]] || 0) + '</td><td class="e">' + (s[0] === 15 ? '' : Math.max(0, nAbout - na)) + '</td></tr>'; });
    $('trust').innerHTML = nAbout ? ht : '<tr><td class="f">No source asked yet: type define : who.</td></tr>';
    var jobs = DNA.filter(function (d) { return d[4] !== null || d[5] !== null; });
    decodeMany(jobs.map(function (d) { return d[4] !== null ? d[4] : d[5]; })).then(function () { $('jobs').innerHTML = jobs.map(function (d) { var r = d[4] !== null ? d[4] : d[5]; return '<div data-run="' + r + '"><span>' + d[0] + '</span><span><b>' + esc(nameOf(d[0])) + '</b> shard ' + d[1] + ' (' + esc(d[2] === null ? '∅' : nameOf(d[2])) + ' → ' + esc(d[3] === null ? '∅' : nameOf(d[3])) + ') ' + (d[4] !== null ? 'calls' : 'spawns') + ' run ' + r + ': ' + esc((lineOf(r) || '').slice(0, 90)) + '</span><span class="m">×' + d[6] + '</span></div>'; }).join('') || '<div><span></span><span class="m">no shard carries a call yet</span><span></span></div>'; });
    $('sixthcounts').innerHTML = [['gates', COUNTS.s_label], ['runs', COUNTS.s_run], ['memories', COUNTS.s_memory], ['refused', COUNTS.s_refused]].map(function (x) { return '<span class="k">' + x[0] + '</span><span>' + fmtN(x[1]) + '</span>'; }).join('');
    q("SELECT 'told', t.run, (SELECT group_concat(symbol,'') FROM (SELECT l.symbol FROM sixth.seq s JOIN sixth.label l ON l.gate = s.gate WHERE s.run = t.run ORDER BY s.pos)), NULL FROM sixth.third t UNION ALL SELECT 'asked main', t.run, (SELECT group_concat(symbol,'') FROM (SELECT l.symbol FROM main.seq s JOIN main.label l ON l.gate = s.gate WHERE s.run = t.run ORDER BY s.pos)), t.run FROM main.third t UNION ALL SELECT 'its line', i.run, (SELECT group_concat(symbol,'') FROM (SELECT l.symbol FROM sixth.seq s JOIN sixth.label l ON l.gate = s.gate WHERE s.run = i.run ORDER BY s.pos)), NULL FROM sixth.input i ORDER BY 2 DESC LIMIT 60").then(function (rows) { $('sixthruns').innerHTML = rows.map(function (r) { return '<div' + (r[3] ? ' data-run="' + r[3] + '"' : '') + '><span>' + r[1] + '</span><span>' + esc(String(r[2] || '').slice(0, 120)) + '</span><span class="m">' + r[0] + '</span></div>'; }).join('') || '<div><span></span><span class="m">nothing yet</span><span></span></div>'; });
    q("SELECT id, word, guess, confidence, belief, used, solved, correct, incorrect, asked_by FROM guess.guesses ORDER BY id DESC LIMIT 40").then(function (rows) { $('guesses').innerHTML = (rows.length ? '<tr><th>#</th><th>symbol</th><th>guess</th><th>conf</th><th>belief</th><th>used</th><th>solved</th><th>✓</th><th>✗</th><th>asked by</th></tr>' + rows.map(function (r) { return '<tr>' + r.map(function (v, i) { return '<td' + (i === 1 ? ' class="ok"' : '') + '>' + esc(v === null ? '?' : (typeof v === 'number' && i >= 3 && i <= 4 ? v.toFixed(2) : v)) + '</td>'; }).join('') + '</tr>'; }).join('') : '<tr><td class="f">No guess asked yet.</td></tr>'); });
    q("SELECT 'main', id, substr(text, 1, 110), error FROM main.refused UNION ALL SELECT 'sixth', id, substr(text, 1, 110), error FROM sixth.refused ORDER BY 2 DESC LIMIT 30").then(function (rows) { $('refused').innerHTML = rows.map(function (r) { return '<div><span>' + r[1] + '</span><span>' + esc(r[2]) + '<br><span class="m">' + esc(r[3]) + '</span></span><span class="m">' + r[0] + '</span></div>'; }).join('') || '<div><span></span><span class="m">nothing refused</span><span></span></div>'; });
  }
  function renderAll() { renderLines(); renderNeurons(); renderBrain(); renderTree(); renderRun(); }

  // ---- the atlas: every gate, by symbol A to Z, with its table, its rows and where the drawing has it
  var AT = null, ATOPEN = -1;
  function atlasRows() {
    var lineBy = {}; ALLLINES.forEach(function (l) { [l[0], l[1]].forEach(function (k) { var o = lineBy[k] = lineBy[k] || {}; o[l[2]] = (o[l[2]] || 0) + 1; }); });
    var out = LABLIST.map(function (g) {
      var n = NODE[String(g)], drawn = n && n.mesh && n.mesh.visible, role = roleOf(g);
      return { gate: g, label: nameOf(g), role: role, call: hasCall(g), pos: drawn ? [n.pos.x, n.pos.y, n.pos.z] : null, why: drawn ? '' : 'not drawn', dna: DNABY[g] || [], defs: NODES[g] || 0, rels: (RELBY[g] || []).length, mem: MEMN[g] || 0, lines: lineBy[String(g)] || {} };
    });
    out.sort(function (a, b) { var x = a.label.toLowerCase(), y = b.label.toLowerCase(); return x < y ? -1 : x > y ? 1 : a.gate - b.gate; });
    return out;
  }
  function fx(v) { return (Math.abs(v) < .05 ? 0 : v).toFixed(1); }
  function atlasDraw() {
    if (!AT) return;
    var qf = $('afind').value.trim().toLowerCase(), show = $('ashow').value, n = 0;
    var rows = AT.rows.filter(function (r) { if (qf && r.label.toLowerCase().indexOf(qf) < 0) return false; if (show === 'node') return r.defs > 0; if (show === 'call') return r.call; if (show === 'rel') return r.rels > 0; if (show === 'drawn') return !!r.pos; return true; });
    var h = '<thead><tr><th>symbol</th><th>x</th><th>y</th><th>z</th><th>gate</th><th>DNA rows (shard: before → trigger, call, spawn, times)</th><th>definition rows</th><th>rel</th><th>memory nodes</th><th>what it is</th><th>lines</th></tr></thead><tbody>';
    rows.forEach(function (r, i) {
      var dna = r.dna.slice(0, 3).map(function (d) { return d[1] + ': ' + esc(d[2] === null ? '∅' : nameOf(d[2])) + ' → ' + esc(d[3] === null ? 'end' : nameOf(d[3])) + (d[4] !== null ? ', calls ' + d[4] : '') + (d[5] !== null ? ', spawns ' + d[5] : '') + ', ×' + d[6]; }).join('<br>') + (r.dna.length > 3 ? '<br><span class="m">+' + (r.dna.length - 3) + ' more</span>' : '');
      var ln = Object.keys(r.lines).sort().map(function (k) { return esc(k) + ' ' + r.lines[k]; }).join('<br>');
      h += '<tr class="arow" data-i="' + i + '"><td>' + esc(r.label) + '</td>' + (r.pos ? '<td class="n">' + fx(r.pos[0]) + '</td><td class="n">' + fx(r.pos[1]) + '</td><td class="n">' + fx(r.pos[2]) + '</td>' : '<td colspan="3" class="m">' + esc(r.why) + '</td>') + '<td class="n">' + r.gate + '</td><td>' + dna + '</td><td class="n">' + r.defs + '</td><td class="n">' + r.rels + '</td><td class="n">' + r.mem + '</td><td>' + esc(r.role === 'core' || r.role === 'born' ? (r.role + (r.call ? ', with a call or spawn' : '')) : ROLETEXT[r.role] || r.role) + '</td><td style="white-space:nowrap">' + ln + '</td></tr>';
      if (i === ATOPEN) h += '<tr class="det"><td colspan="11"><div class="dt">' + atlasDetail(r) + '</div></td></tr>';
      n++;
    });
    $('atable').innerHTML = h + '</tbody>'; $('ashown').textContent = n + ' shown';
  }
  function atlasDetail(r) {
    var h = '<b>' + esc(r.label) + '</b> <span class="m">gate ' + r.gate + ' · ' + esc(ROLETEXT[r.role] || r.role) + '</span>';
    h += '\nposition (the drawing\'s units): ' + (r.pos ? fx(r.pos[0]) + ', ' + fx(r.pos[1]) + ', ' + fx(r.pos[2]) + '; distance from origin ' + Math.hypot(r.pos[0], r.pos[1], r.pos[2]).toFixed(1) : r.why);
    h += '\n\ntable "' + r.gate + '": ' + r.dna.length + ' DNA rows' + (r.dna.length ? '\nshard | before | trigger | call | spawn | times\n' + r.dna.map(function (d) { return d[1] + ' | ' + esc(d[2] === null ? '∅' : nameOf(d[2]) + ' (' + d[2] + ')') + ' | ' + esc(d[3] === null ? '∅ end' : nameOf(d[3]) + ' (' + d[3] + ')') + ' | ' + (d[4] === null ? '' : d[4]) + ' | ' + (d[5] === null ? '' : d[5]) + ' | ' + d[6]; }).join('\n') : '');
    h += '\n\ntable "' + r.gate + '.node": ' + r.defs + ' rows · rel rows: ' + r.rels + ' · memory nodes: ' + r.mem;
    var ln = Object.keys(r.lines); h += '\n\nlines: ' + (ln.length ? ln.sort().map(function (k) { return esc(k) + ' ' + r.lines[k]; }).join(', ') : 'none');
    return h;
  }
  function atlasRead() {
    $('asum').textContent = 'reading the brain…';
    AT = { rows: atlasRows(), step: STEP, move: LASTMOVE }; ATOPEN = -1;
    var c = {}; AT.rows.forEach(function (r) { c[r.role] = (c[r.role] || 0) + 1; });
    $('asum').innerHTML = '<b>' + fmtN(AT.rows.length) + ' gates.</b> ' + ['heard', 'arrival', 'source', 'space', 'core', 'born'].map(function (k) { return fmtN(c[k] || 0) + ' ' + k; }).join(', ') + '. ' + fmtN(DNA.length) + ' DNA rows over every neuron table, ' + fmtN(COUNTS.shards) + ' shards, ' + fmtN(COUNTS.rel) + ' relationship rows.<br><span class="m">Read from the brain as it stands. x, y, z are where the drawing has put each point at step ' + AT.step + '; in that step the lines moved a point at most ' + AT.move.toFixed(2) + '. The brain holds no positions.</span>';
    atlasDraw();
  }
  $('atlasbtn').addEventListener('click', function () { if (!ready) return; $('atlas').hidden = false; atlasRead(); });
  $('aclose').addEventListener('click', function () { $('atlas').hidden = true; });
  $('arefresh').addEventListener('click', function () { atlasRead(); });
  $('afind').addEventListener('input', function () { ATOPEN = -1; atlasDraw(); });
  $('ashow').addEventListener('change', function () { ATOPEN = -1; atlasDraw(); });
  $('atable').addEventListener('click', function (ev) { var tr = ev.target.closest('tr.arow'); if (!tr) return; var i = +tr.getAttribute('data-i'); if (ev.detail === 2 && AT.rows[i]) { $('atlas').hidden = true; showNode(AT.rows[i].gate); showTab('panel-sel'); return; } ATOPEN = ATOPEN === i ? -1 : i; atlasDraw(); });

  // ---- opening: the door, then the brain's tables
  function newestLineRun() { var root = null; INPUTS.forEach(function (x) { if (x.schema === 'main' && RUNS[x.run]) root = x.run; }); return root; }
  function open(tries) {
    api('/api/info').then(function (info) {
      INFO = info;
      if (info.error) { $('hud').innerHTML = '<b>the door could not open the brain</b><span class="ev">' + esc(info.error) + '</span>'; return; }
      if (!info.ready) { $('hud').innerHTML = '<b>the door is opening the brains</b>'; setTimeout(function () { open(tries); }, 1000); return; }
      if (info.busy) { $('hud').innerHTML = '<b>the brain is running a line typed before this page opened</b><span class="ev">' + esc(info.busy.line || '') + '</span>'; setTimeout(function () { open(tries); }, 2000); return; }
      $('hud').innerHTML = '<b>reading the brain’s tables</b>';
      return loadBundle().then(function () {
        ready = true; fitLeft = 240; renderAll(); readLines(); renderOut();
        render(HIST.length - 1, false); var root = newestLineRun(); if (root && RUNS[root]) { CUR.run = root; CUR.root = RUNS[root].root === null ? root : RUNS[root].root; refreshMem(function () { renderTree(); renderRun(); render(HIST.length - 1, true); }); }
        setBusy('the brains are open: ' + fmtN(COUNTS.label) + ' gates, ' + fmtN(COUNTS.shards) + ' shards, ' + fmtN(COUNTS.run) + ' runs. Type a line.');
      });
    }).catch(function (e) {
      if (e.busy) { $('hud').innerHTML = '<b>the brain is running a line typed elsewhere</b><span class="ev">' + esc(e.busy.line || '') + ' · waiting</span>'; setTimeout(function () { open(tries); }, 2000); return; }
      $('hud').innerHTML = '<b>the brain’s door is not open</b><span class="ev">' + esc(e.message) + '. Start it from the page folder: python3 serve6.py, then open http://localhost:8056/ . Trying again…</span>';
      setTimeout(function () { open((tries || 0) + 1); }, 3000);
    });
  }
  open(0);

  // ---- camera, pointer, frame (17.3's)
  var theta = 0, phi = 1.45, dist = 160, tgt = hasGL ? new THREE.Vector3(0, 0, 0) : null;
  function updateCam() { camera.position.set(tgt.x + dist * Math.sin(phi) * Math.sin(theta), tgt.y + dist * Math.cos(phi), tgt.z + dist * Math.sin(phi) * Math.cos(theta)); camera.lookAt(tgt); }
  window.__poc = { ready: function () { return ready; }, busy: function () { return busy; }, counts: function () { return COUNTS; }, gates: function () { return LABLIST.length; }, dna: function () { return DNA.length; }, springs: function () { return SPRINGS.length; }, nodes: function () { return Object.keys(NODE).filter(function (k) { return NODE[k].mesh && NODE[k].mesh.visible; }).length; },
    kinds: function () { var o = {}; SPRINGS.forEach(function (sp) { o[sp.kind] = (o[sp.kind] || 0) + 1; }); return o; },
    positions: function () { var o = {}; Object.keys(NODE).forEach(function (k) { if (NODE[k].mesh && NODE[k].mesh.visible) o[k] = [NODE[k].pos.x, NODE[k].pos.y, NODE[k].pos.z]; }); return o; },
    cur: function () { return { root: CUR.root, run: CUR.run, hops: CUR.run !== null ? (RUNHOPS[CUR.run] || []).length : 0, tk: TK, hits: HIST.length }; }, chooseRun: chooseRun, showNode: showNode, send: send, render: render, last: function () { return LAST; }, shown: function () { return SHOWN.length; }, lines: function () { return LINESF.length; },
    stretch: function () { var s = 0; SPRINGS.forEach(function (sp) { s += Math.abs(sp.a.pos.distanceTo(sp.b.pos) - sp.rest) / sp.rest; }); return SPRINGS.length ? s / SPRINGS.length : 0; },
    lonely: function () { var linked = {}; SPRINGS.forEach(function (sp) { linked[sp.names[0]] = 1; linked[sp.names[1]] = 1; }); var n = 0; Object.keys(NODE).forEach(function (k) { if (!linked[k] && NODE[k].mesh && NODE[k].mesh.visible) n++; }); return n; } };
  if (hasGL) {
    var canvas = $('c'), ptrs = {}, dragging = false, moved = false, lastX = 0, lastY = 0, pinchD = 0, userZoomed = false;
    canvas.addEventListener('pointerdown', function (e) { ptrs[e.pointerId] = [e.clientX, e.clientY]; dragging = true; moved = false; lastX = e.clientX; lastY = e.clientY; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener('pointermove', function (e) { if (!dragging) return; ptrs[e.pointerId] = [e.clientX, e.clientY]; var ids = Object.keys(ptrs); if (ids.length >= 2) { var a = ptrs[ids[0]], b = ptrs[ids[1]], d = Math.hypot(a[0] - b[0], a[1] - b[1]); if (pinchD) dist = Math.min(300000, Math.max(5, dist * pinchD / d)); pinchD = d; moved = true; userZoomed = true; return; } var dx = e.clientX - lastX, dy = e.clientY - lastY; lastX = e.clientX; lastY = e.clientY; if (Math.abs(dx) + Math.abs(dy) > 2) moved = true; theta -= dx * .005; phi = Math.min(Math.PI - .05, Math.max(.05, phi - dy * .005)); });
    function up(e) { delete ptrs[e.pointerId]; if (Object.keys(ptrs).length < 2) pinchD = 0; if (Object.keys(ptrs).length === 0) { dragging = false; if (!moved) pick(e); } }
    canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
    canvas.addEventListener('wheel', function (e) { e.preventDefault(); userZoomed = true; dist = Math.min(300000, Math.max(5, dist * (1 + e.deltaY * .0012))); }, { passive: false });
    var ray = new THREE.Raycaster();
    function pick(e) { var rect = canvas.getBoundingClientRect(), v = new THREE.Vector2(((e.clientX - rect.left) / rect.width) * 2 - 1, -((e.clientY - rect.top) / rect.height) * 2 + 1); ray.setFromCamera(v, camera); var hit = ray.intersectObjects(dotGroup.children.filter(function (m) { return m.visible; }), false); if (hit.length) { var k = hit[0].object.userData.key; if (k.charAt(0) === 'm') { setPlay(false); chooseRun(+k.slice(2), 0); showTab('panel-run'); return; } if (k.charAt(0) === 'g') { $('sel').innerHTML = '<b>' + esc(k.slice(2)) + '</b><span class="m">a word of your relation map the brain has no gate for yet. Type define : ' + esc(k.slice(2)) + ' and it is born.</span>'; showTab('panel-sel'); return; } showNode(+k); showTab('panel-sel'); return; } SELG = null; $('sel').innerHTML = '<span class="m">Click a dot on the stage, or a gate under neurons.</span>'; render(TK, true); }
    function resize() { var w = $('stage').clientWidth, h = $('stage').clientHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
    // the drawing keeps growing after it opens (the gap pushes the ball out); the view follows until the radius holds still, unless the wheel was used
    var fitR = 0; function fit() { if (userZoomed) return; var rs = []; Object.keys(NODE).forEach(function (k) { var n = NODE[k]; if (n.mesh && n.mesh.visible) rs.push(n.pos.length() * SP); }); if (!rs.length) return; rs.sort(function (a, b) { return a - b; }); var r = rs[Math.floor(rs.length * .95)] || rs[rs.length - 1]; if (Math.abs(r - fitR) > fitR * .01) { fitR = r; fitLeft = Math.max(fitLeft, 60); } if (fitLeft <= 0) return; fitLeft--; var want = Math.max(40, r * 1.15 / Math.tan(20 * Math.PI / 180) / Math.min(1, camera.aspect)); dist += (want - dist) * .05; }
    window.addEventListener('resize', resize);
    var last = performance.now();
    function frame(now) {
      var dt = (now - last) / 1000; last = now;
      if (spinning && !dragging) theta += dt * .08;
      if (ready) fit();
      if (ready) { settle(reshapeLeft > 0 ? 6 : 2); if (reshapeLeft > 0) reshapeLeft--; Object.keys(NODE).forEach(function (k) { var n = NODE[k]; if (n.mesh) { n.mesh.position.copy(n.pos).multiplyScalar(SP); if (n.mesh.visible) n.mesh.scale.setScalar(n.mesh.userData.base * 3.5 * (n.mesh.userData.hot ? 2 : 1) * 0.728 * camera.position.distanceTo(n.mesh.position) / stageH()); if (n.label) { sizeLabel(n.label); n.label.position.copy(n.mesh.position); } } }); redrawLines(); drawAxes(false); axesGroup.children.forEach(function (c) { if (c.userData.px) sizeLabel(c); }); }
      if (playing) { acc += dt; var per = 1 / parseFloat($('speed').value); if (acc > per) { var k = Math.max(1, Math.floor(acc / per)); acc = 0; advance(k); } }
      updateCam(); renderer.render(scene, camera); requestAnimationFrame(frame);
    }
    resize(); requestAnimationFrame(frame);
  } else {
    var lastT = performance.now();
    (function tick(now) { if (playing) { var per = 1000 / parseFloat($('speed').value); if (now - lastT > per) { lastT = now; advance(1); } } window.requestAnimationFrame(tick); })(performance.now());
  }
})();
