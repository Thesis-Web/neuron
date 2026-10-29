(function () {
  var $ = function (id) { return document.getElementById(id); };
  function esc(s) { return String(s === null || s === undefined ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmtN(n) { return (n === null || n === undefined) ? '' : Number(n).toLocaleString(); }

  // ---- the door: the page served by serve6.py talks to the same origin; opened as a file it talks to localhost:8056
  var API = /^https?:$/.test(location.protocol) ? '' : 'http://localhost:8056';
  function api(path, body) {
    var opt = body === undefined ? {} : { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) };
    return fetch(API + path, opt).then(function (r) { return r.json().then(function (j) { if (!r.ok) { var e = new Error(j.error || ('HTTP ' + r.status)); e.busy = j.busy; throw e; } return j; }); });
  }
  function q(sql, params) { return api('/api/q', { sql: sql, params: params || [] }).then(function (j) { return j.rows; }); }

  // ---- tabs: each rail shows one panel at a time; the one chosen is remembered in this browser only
  function showTab(panel) {
    var p = $(panel); if (!p) return; var aside = p.parentNode, bar = aside.querySelector('.tabs');
    bar.querySelectorAll('button[data-panel]').forEach(function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-panel') === panel)); });
    aside.querySelectorAll('.inner').forEach(function (x) { x.hidden = x.id !== panel; });
    try { localStorage.setItem('poc6.' + bar.getAttribute('data-for'), panel); } catch (e) {}
  }
  document.querySelectorAll('.tabs').forEach(function (bar) {
    bar.addEventListener('click', function (e) { var b = e.target.closest('button[data-panel]'); if (b) showTab(b.getAttribute('data-panel')); });
    var kept = null; try { kept = localStorage.getItem('poc6.' + bar.getAttribute('data-for')); } catch (e) {}
    if (kept && $(kept)) showTab(kept);
  });

  // ---- the brain's tables, as the page holds them after each read. The fresh egg's gate numbers that the physics uses are named here once.
  var G = { heard: 1, said: 2, space: 3, mother: 4, sixth: 5, main: 6, guess: 15, born: 16, me: 19, above: 20, newgate: 21, reply: 22, what: 23, def: 24, say: 25, know: 26, remember: 27, shape: 28, BUILD: 29, colon: 68 };
  var SOURCES = [[7, 'wn', 'WordNet'], [8, 'gcide', 'Webster 1913'], [9, 'mw', 'MW Collegiate'], [10, 'mwt', 'MW thesaurus'], [11, 'moby', 'Moby'], [12, 'map', 'your map'], [13, 'sqldoc', 'SQLite docs'], [14, 'measured', 'measured'], [15, 'guess', 'the guessing brain']];
  var SRCNAME = {}; SOURCES.forEach(function (s) { SRCNAME[s[0]] = s[2]; });
  var CORE = 80, POINTERS = { 22: 1, 24: 1, 25: 1, 27: 1 };
  var LAB = {}, SYM = {}, LABLIST = [], DNA = [], DNABY = {}, SHARDROW = {}, NODES = {}, REL = [], RELBY = {}, MEMN = {}, FIRST = {}, RUNS = {}, RUNLIST = [], CHILDREN = {}, COUNTS = {}, INPUTS = [], OUTBY = {}, DEFW = {}, ANSW = [], MAPL = null, HOPCOUNT = {};
  var ready = false, busy = false, T = -1, SELG = null, INFO = null;
  var SHEET = {}, TEXT = {};   // run -> sheet rows; run -> its line read back through the encoder
  // the history: every receipt row of the brain, in the order the brain wrote them (17.3 replayed its event log; v6 replays the receipt table)
  var HIST = [], RUNHOPS = {}, FIRSTG = {}, FIRSTS = {}, RUNT0 = {}, RUNT1 = {}, TK = -1, HISTLAST = 0;
  var CUR = { root: null, run: null };
  function loadBundle() {
    return Promise.all([
      q('SELECT gate, symbol FROM main.label ORDER BY gate'),
      api('/api/graph?schema=main'),
      q('SELECT id, arrival, parent, root, kind, cell, about, at FROM main.run ORDER BY id'),
      q("SELECT 'main', id, run FROM main.input WHERE run IS NOT NULL UNION ALL SELECT 'sixth', id, run FROM sixth.input WHERE run IS NOT NULL ORDER BY 1, 2"),
      q('SELECT id, run, cell, value FROM main.out_user ORDER BY id'),
      q("SELECT (SELECT count(*) FROM main.label), (SELECT count(*) FROM main.sqlite_master WHERE type = 'table'), (SELECT count(*) FROM main.sqlite_master WHERE type = 'trigger'), (SELECT n FROM main.shards), (SELECT count(*) FROM main.run), (SELECT count(*) FROM main.run_receipt), (SELECT count(*) FROM main.run_sheet), (SELECT count(*) FROM main.run_memory), (SELECT count(*) FROM main.timeline), (SELECT count(*) FROM main.refused), (SELECT count(*) FROM main.hop), (SELECT count(*) FROM main.run_sheet WHERE state = 0), (SELECT count(*) FROM main.run WHERE id NOT IN (SELECT run FROM main.run_memory)), (SELECT count(*) FROM main.rel), (SELECT count(*) FROM sixth.label), (SELECT count(*) FROM sixth.run), (SELECT count(*) FROM sixth.run_memory), (SELECT count(*) FROM sixth.refused), (SELECT count(*) FROM main.run WHERE kind = 3 AND arrival BETWEEN 7 AND 14)"),
      q('SELECT r.about, s.gate, min(r.id) FROM main.run r JOIN main.seq s ON s.run = r.id JOIN main.label l ON l.gate = s.gate WHERE r.kind = 3 AND r.arrival BETWEEN 7 AND 14 AND r.about IS NOT NULL AND l.symbol GLOB \'[A-Za-z]*\' GROUP BY r.about, s.gate'),
      q('SELECT arrival, about, min(id) FROM main.run WHERE kind = 3 AND about IS NOT NULL AND arrival BETWEEN 7 AND 15 GROUP BY arrival, about'),
      q('SELECT run, count(*) FROM main.run_receipt GROUP BY run'),
      MAPL ? Promise.resolve(null) : q("SELECT word, text FROM map.corpus"),
      q('SELECT id, run, gate, shard FROM main.run_receipt WHERE id > ? ORDER BY id', [HISTLAST])
    ]).then(absorb);
  }
  function absorb(R) {
    LAB = {}; SYM = {}; LABLIST = R[0].map(function (r) { LAB[r[0]] = r[1]; SYM[r[1]] = r[0]; return r[0]; });
    var g = R[1]; DNA = g.dna; NODES = g.nodes || {}; REL = g.rel || []; MEMN = g.mem || {}; FIRST = g.first || {};
    DNABY = {}; SHARDROW = {}; DNA.forEach(function (d) { (DNABY[d[0]] = DNABY[d[0]] || []).push(d); SHARDROW[d[1]] = d; }); Object.keys(DNABY).forEach(function (k) { DNABY[k].sort(function (a, b) { return a[1] - b[1]; }); });
    RELBY = {}; REL.forEach(function (r) { (RELBY[r[0]] = RELBY[r[0]] || []).push(r); (RELBY[r[2]] = RELBY[r[2]] || []).push(r); });
    RUNS = {}; CHILDREN = {}; RUNLIST = R[2].map(function (r) { var x = { id: r[0], arrival: r[1], parent: r[2], root: r[3], kind: r[4], cell: r[5], about: r[6], at: r[7] }; RUNS[r[0]] = x; if (r[2] !== null) (CHILDREN[r[2]] = CHILDREN[r[2]] || []).push(r[0]); return x; });
    INPUTS = R[3].map(function (r) { return { schema: r[0], id: r[1], run: r[2] }; });
    OUTBY = {}; R[4].forEach(function (r) { (OUTBY[r[1]] = OUTBY[r[1]] || []).push({ id: r[0], cell: r[2], value: r[3] }); });
    var c = R[5][0]; COUNTS = { label: c[0], tables: c[1], triggers: c[2], shards: c[3], run: c[4], receipts: c[5], sheet: c[6], memory: c[7], timeline: c[8], refused: c[9], hop: c[10], empty: c[11], unended: c[12], rel: c[13], s_label: c[14], s_run: c[15], s_memory: c[16], s_refused: c[17], returns: c[18] };
    DEFW = {}; R[6].forEach(function (r) { (DEFW[r[0]] = DEFW[r[0]] || []).push([r[1], r[2]]); });
    ANSW = R[7];
    R[10].forEach(function (r) { var i = HIST.length; HIST.push(r); HISTLAST = r[0]; (RUNHOPS[r[1]] = RUNHOPS[r[1]] || []).push(i); if (FIRSTG[r[2]] === undefined) FIRSTG[r[2]] = i; if (FIRSTS[r[3]] === undefined) FIRSTS[r[3]] = i; if (RUNT0[r[1]] === undefined) RUNT0[r[1]] = i; RUNT1[r[1]] = i; });
    HOPCOUNT = {}; R[8].forEach(function (r) { HOPCOUNT[r[0]] = r[1]; });
    if (R[9]) { MAPL = []; R[9].forEach(function (r) { var m = /^(like|opposite(?: of)?)\s+(.+)$/.exec(r[1]); if (!m) return; var kind = m[1].indexOf('opposite') === 0 ? 'opposite' : 'alike'; m[2].split(/\s*,\s*/).forEach(function (o) { o = o.trim(); if (o) MAPL.push([r[0], kind, o]); }); }); }
  }
  function roleOf(g) { if (g === G.heard) return 'heard'; if (g === G.said || g === G.mother || g === G.sixth || g === G.main) return 'arrival'; if (g >= 7 && g <= 15) return 'source'; if (g === G.space) return 'space'; if (g <= CORE) return 'core'; return 'born'; }
  var ROLETEXT = { heard: 'heard, the arrival gate of every typed line: the one fixed point', arrival: 'an arrival gate, hand-laid: the first row of a line arrives from it', source: 'a source brain: its own database with a corpus, an inbox, an outbox and its own trigger; its gate is where its returns arrive from', space: 'the space neuron: one shard, counted every time a run passes a space', core: 'hand-laid: one of the 80 neurons laid before any line (its label row, its DNA table, its definition node)', born: 'born by the born run, the moment a line first reached it' };
  function hasCall(g) { var d = DNABY[g] || []; for (var i = 0; i < d.length; i++) if (d[i][4] !== null || d[i][5] !== null) return true; return false; }
  function nameOf(g) { var s = LAB[g]; if (s === undefined) return '#' + g; return s === ' ' ? '␣' : s === '\n' ? '⏎' : s; }
  function lineOf(run) { return TEXT[run] !== undefined ? TEXT[run] : null; }
  function decodeRun(run) { if (TEXT[run] !== undefined) return Promise.resolve(TEXT[run]); return q("SELECT group_concat(symbol, '') FROM (SELECT l.symbol FROM main.seq s JOIN main.label l ON l.gate = s.gate WHERE s.run = ? ORDER BY s.pos)", [run]).then(function (r) { TEXT[run] = (r[0] && r[0][0]) || ''; return TEXT[run]; }); }
  function decodeMany(runs) { var need = runs.filter(function (r) { return TEXT[r] === undefined; }); if (!need.length) return Promise.resolve(); return q("SELECT s.run, group_concat(l.symbol, '') FROM (SELECT run, pos, gate FROM main.seq WHERE run IN (" + need.map(function () { return '?'; }).join(',') + ") ORDER BY run, pos) s JOIN main.label l ON l.gate = s.gate GROUP BY s.run", need).then(function (rows) { need.forEach(function (r) { TEXT[r] = ''; }); rows.forEach(function (r) { TEXT[r[0]] = r[1] || ''; }); }); }
  function setBusy(t) { $('busy').textContent = t; }
  var KINDNAME = ['a line', 'a call', 'a spawn', 'a return'];

  // ---- the stage (17.3's drawing: springs only, one fixed point, a space between points)
  var hasGL = true, renderer, scene, camera;
  try { if (!window.THREE) throw new Error('no three'); renderer = new THREE.WebGLRenderer({ canvas: $('c'), antialias: true }); } catch (e) { hasGL = false; $('err').style.display = 'flex'; }
  if (hasGL) { renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); scene = new THREE.Scene(); scene.background = new THREE.Color(0x0c0e12); camera = new THREE.PerspectiveCamera(40, 1, 1, 400000); }
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function unit(seed) { var a = (hash('a' + seed) / 4294967296) * 2 * Math.PI, z = (hash('z' + seed) / 4294967296) * 2 - 1, r = Math.sqrt(1 - z * z); return new THREE.Vector3(r * Math.cos(a), r * Math.sin(a), z); }
  var dotGeo = hasGL ? new THREE.SphereGeometry(1, 10, 10) : null, dotGroup, labelGroup, relGroup, runGroup, flash, flashGeo, flash2, flashGeo2;
  if (hasGL) { dotGroup = new THREE.Group(); labelGroup = new THREE.Group(); relGroup = new THREE.Group(); runGroup = new THREE.Group(); [dotGroup, labelGroup, relGroup, runGroup].forEach(function (g) { scene.add(g); }); flashGeo = new THREE.BufferGeometry(); flash = new THREE.LineSegments(flashGeo, new THREE.LineBasicMaterial({ color: 0xfff1a8, transparent: true, opacity: .95 })); scene.add(flash); flashGeo2 = new THREE.BufferGeometry(); flash2 = new THREE.LineSegments(flashGeo2, new THREE.LineBasicMaterial({ color: 0xf28c4b, transparent: true, opacity: .95 })); scene.add(flash2); }
  var NODE = {};   // key (a gate as a string, 'm:<run>' for a memory node, 'g:<word>' for a word of your map the brain has no gate for) -> {mesh, label, pos, fixed, ghost}
  function colorOf(k) {
    if (k.charAt(0) === 'm') return 0x7ed07e; if (k.charAt(0) === 'g') return 0x8b95a2;
    var g = +k, r = roleOf(g); if (r === 'heard') return 0xfff1a8; if (r === 'source') return 0x8fd3c1; if (r === 'arrival') return 0xffffff; if (hasCall(g)) return 0xf28c4b;
    if (r === 'core' || r === 'space') return NODES[g] > 0 ? 0xbfc6cf : 0x9aa3ad; return NODES[g] > 0 ? 0xa9c3dc : 0x6f7a86;
  }
  function sizeOf(k) { if (k.charAt(0) === 'm') return .55; if (k.charAt(0) === 'g') return .55; var g = +k, r = roleOf(g); return r === 'heard' ? 2.4 : r === 'source' ? 2.4 : r === 'arrival' ? 1.6 : hasCall(g) ? 1.3 : 1.0; }
  function labelOf(k) { if (k.charAt(0) === 'm') return 'memory ' + k.slice(2); if (k.charAt(0) === 'g') return k.slice(2); return nameOf(+k); }
  function makeLabel(text, css, px, centered) { var c = document.createElement('canvas'), ctx = c.getContext('2d'); ctx.font = '500 26px "IBM Plex Mono", Consolas, monospace'; var w = Math.ceil(ctx.measureText(text).width) + 14; c.width = w; c.height = 36; ctx.font = '500 26px "IBM Plex Mono", Consolas, monospace'; ctx.fillStyle = css; ctx.textBaseline = 'middle'; ctx.fillText(text, 7, 18); var tex = new THREE.CanvasTexture(c); tex.minFilter = THREE.LinearFilter; var sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false, opacity: .92, sizeAttenuation: false })); if (!centered) sp.center.set(.5, -.35); sp.userData.px = px; sp.userData.aspect = w / 36; sizeLabel(sp); return sp; }
  function stageH() { return (renderer && renderer.domElement.clientHeight) || 800; }
  function sizeLabel(sp) { var y = sp.userData.px * 0.728 / stageH(); sp.scale.set(y * sp.userData.aspect, y, 1); }
  function ensureNode(k) {
    var n = NODE[k];
    if (!n) {
      // a new point has no place until its lines give it one: it waits at origin and is placed beside its neighbours once the lines are known
      var fixed = k === String(G.heard), p = new THREE.Vector3(0, 0, 0);
      n = NODE[k] = { key: k, pos: p, fixed: fixed, unplaced: !fixed, ghost: k.charAt(0) === 'g', mem: k.charAt(0) === 'm' };
      if (hasGL) {
        var col = colorOf(k), r = sizeOf(k);
        n.mesh = new THREE.Mesh(dotGeo, new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: n.ghost ? .4 : .92 })); n.mesh.scale.setScalar(r); n.mesh.position.copy(n.pos); n.mesh.userData = { base: r, key: k }; dotGroup.add(n.mesh);
        if (!n.mem) { n.label = makeLabel(labelOf(k), '#' + ('000000' + col.toString(16)).slice(-6), (k === String(G.heard) || roleOf(+k) === 'source') ? 15 : n.ghost ? 10 : 12); n.label.position.copy(n.pos); labelGroup.add(n.label); }
      }
    } else if (hasGL) { var c2 = colorOf(k); if (n.mesh.material.color.getHex() !== c2) { n.mesh.material.color.setHex(c2); n.mesh.scale.setScalar(sizeOf(k)); n.mesh.userData.base = sizeOf(k); if (n.label) { labelGroup.remove(n.label); n.label.material.map.dispose(); n.label.material.dispose(); n.label = makeLabel(labelOf(k), '#' + ('000000' + c2.toString(16)).slice(-6), 12); labelGroup.add(n.label); } } }
    return n;
  }
  function hideNode(k) { var n = NODE[k]; if (!n || !n.mesh) return; n.mesh.visible = false; if (n.label) n.label.visible = false; }

  // ---- the kinds of line, the pull law, the settle (17.3's; the kinds are v6's rows)
  var REL_TYPES = [['dna before', 0.6, 'a DNA row: the symbol before, to this one'], ['dna trigger', 0.6, 'a DNA row: this symbol to the one the run goes on to'], ['dna call', 0.8, 'a DNA row\'s call: this symbol to the first gate of the run it replays and takes the answer from'], ['dna spawn', 0.8, 'a DNA row\'s spawn: this symbol to the first gate of the run it sends off'],
    ['made-of', 0.5, 'a symbol with a call, to each gate the run it calls passes'], ['definition', 0.4, 'a symbol to the words of the lines its sources returned (its definition node)'], ['answered', 0.4, 'a source brain to the symbols it answered'], ['memory', 0.5, 'a memory node (a run_memory row) to the shard\'s gate it ended on and the words of its line'],
    ['alike', 1.0, 'like; a rel row from the thesaurus, Moby or your map'], ['opposite', 1.0, 'opposite; a rel row'], ['is', 0.9, 'kind, class; in your map'], ['includes', 0.9, ''], ['inverse', 0.9, ''], ['contradicts', 0.8, ''], ['supports', 0.7, ''], ['has', 0.7, 'in your map'], ['part', 0.7, ''], ['similar', 0.6, ''], ['prefix', 0.5, 'in your map'], ['begins', 0.5, ''], ['suffix', 0.5, 'in your map'], ['ends', 0.5, ''], ['stem', 0.5, 'in your map'], ['past', 0.5, 'in your map'], ['present', 0.5, ''], ['singular', 0.5, 'in your map'], ['plural', 0.5, ''], ['derived-from', 0.5, ''], ['use', 0.4, ''], ['before', 0.4, ''], ['after', 0.4, ''], ['topic', 0.3, ''], ['context', 0.3, ''], ['category', 0.3, ''], ['method', 0.3, '']];
  var REL_OF = { like: 'alike', alike: 'alike', similar: 'similar', opposite: 'opposite', inverse: 'inverse', kind: 'is', class: 'is', has: 'has', part: 'part', before: 'before', after: 'after', topic: 'topic', context: 'context', category: 'category', method: 'method', use: 'use', supports: 'supports', contradicts: 'contradicts', derived: 'derived-from', includes: 'includes', begins: 'begins', ends: 'ends', present: 'present', plural: 'plural' };
  var REL_COL = { 'dna before': 0x8fd3c1, 'dna trigger': 0xd8d4c8, 'dna call': 0xf28c4b, 'dna spawn': 0xffc98a, 'made-of': 0xe8e2a0, definition: 0x8ea3b8, answered: 0x6fb8a8, memory: 0x7ed07e, alike: 0x4f9bd9, opposite: 0xe0573f, is: 0x9b7bd4, includes: 0xb59ae0, inverse: 0xd97b4f, contradicts: 0xc24f8a, supports: 0x4fb7a8, has: 0x6fa8dc, part: 0x8cb8e0, similar: 0x7fc2e8, prefix: 0xa8a070, begins: 0x5fc89a, suffix: 0xb0a860, ends: 0x4fb8c0, stem: 0x98a860, past: 0x8fb070, present: 0xe09ab8, singular: 0x90b888, plural: 0xe0a060, 'derived-from': 0xd0a050, use: 0xc8b070, before: 0x70b0c0, after: 0x60a0b8, topic: 0x909cb0, context: 0x98a4b8, category: 0xa0acc0, method: 0xa8b4c8 };
  var REST = { 'dna before': 14, 'dna trigger': 14, 'dna call': 16, 'dna spawn': 16, 'made-of': 16, definition: 18, answered: 22, memory: 12, alike: 10, similar: 14, is: 22, includes: 22, has: 24, part: 24, opposite: 64, inverse: 64, contradicts: 64 };
  function hexOf(r) { return '#' + ('000000' + (REL_COL[r] || 0x9aa3ad).toString(16)).slice(-6); }
  var DIRS = [['', 'any way'], ['x', 'east +x'], ['-x', 'west -x'], ['y', 'north +y'], ['-y', 'south -y'], ['z', 'up +z'], ['-z', 'down -z'], ['across', 'across origin']];
  var DEFAULT_DIR = { opposite: 'across', inverse: 'across', contradicts: 'across' };
  function dirVec(d) { if (!d || d === 'across') return null; var v = new THREE.Vector3(); v.setComponent({ x: 0, y: 1, z: 2 }[d.slice(-1)], d[0] === '-' ? -1 : 1); return v; }
  var RELSET = {};
  function kindRow(k, w, title) { return '<input type="checkbox" data-rel="' + esc(k) + '" checked aria-label="' + esc(k) + ' on or off"><span class="sw" style="background:' + hexOf(k) + '"></span><span title="' + esc(title || '') + '">' + esc(k) + '</span><input type="range" min="0" max="1" step="0.05" value="' + w + '" data-relw="' + esc(k) + '" aria-label="' + esc(k) + ' pull"><span class="n" id="rc-' + esc(k).replace(/[^a-z0-9]/gi, '_') + '">0</span><select class="dir" data-reldir="' + esc(k) + '" aria-label="' + esc(k) + ' direction">' + DIRS.map(function (d) { return '<option value="' + d[0] + '"' + ((DEFAULT_DIR[k] || '') === d[0] ? ' selected' : '') + '>' + d[1] + '</option>'; }).join('') + '</select>'; }
  function addKind(k, w, title) { if (RELSET[k]) return; RELSET[k] = { on: true, w: w, dir: DEFAULT_DIR[k] || '' }; $('reltypes').insertAdjacentHTML('beforeend', kindRow(k, w, title)); }
  (function () {
    REL_TYPES.forEach(function (r) { addKind(r[0], r[1], r[2]); });
    $('reltypes').addEventListener('change', function (e) { var k = e.target.getAttribute('data-rel'), d = e.target.getAttribute('data-reldir'); if (k) { RELSET[k].on = e.target.checked; render(TK, true); reshape(); } if (d) { RELSET[d].dir = e.target.value; render(TK, true); reshape(); } });
    $('reltypes').addEventListener('input', function (e) { var k = e.target.getAttribute('data-relw'); if (k) { RELSET[k].w = parseFloat(e.target.value); render(TK, true); reshape(); } });
    $('spacing').addEventListener('input', function () { SP = parseFloat($('spacing').value); $('spv').textContent = '×' + SP; drawAxes(true); });
    $('axes').addEventListener('change', function () { drawAxes(true); });
    $('gap').addEventListener('input', function () { GAP = parseFloat($('gap').value); $('gapv').textContent = GAP; reshape(); });
    $('fitall').addEventListener('click', function () { userZoomed = false; fitLeft = 120; });
    ['mapall', 'ghostlabels', 'spacept', 'runspace', 'memall', 'runmode'].forEach(function (id) { $(id).addEventListener('change', function () { var go = function () { render(TK, true); if (id !== 'runmode' && id !== 'runspace') reshape(); }; if (id === 'memall') refreshMem(go); else go(); }); });
  })();
  var SPRINGS = [], ALLLINES = [], MEMROWS = [];
  function relKind(kindGate) { var s = LAB[kindGate]; if (s === undefined) return 'rel #' + kindGate; var k = REL_OF[s] || s; if (!RELSET[k]) addKind(k, 0.5, 'a rel row: the kind word ' + s); return k; }
  function buildSprings(tk) {
    var agg = {}, spaceOn = $('spacept').checked, atRun = function (run) { return run !== null && run !== undefined && RUNT0[run] !== undefined && RUNT0[run] <= tk; };
    function add(a, b, kind, trust) { a = String(a); b = String(b); if (a === b) return; if (!NODE[a] || !NODE[b]) return; if (!spaceOn && (a === String(G.space) || b === String(G.space))) return; var id = kind + '|' + (a < b ? a + '|' + b : b + '|' + a); if (!agg[id]) agg[id] = [a, b, kind, trust, 0]; agg[id][4]++; }
    DNA.forEach(function (d) { var g = d[0]; if (FIRSTS[d[1]] === undefined || FIRSTS[d[1]] > tk) return; if (d[2] !== null) add(d[2], g, 'dna before', 1); if (d[3] !== null) add(g, d[3], 'dna trigger', 1); if (d[4] !== null && FIRST[d[4]] !== undefined && atRun(d[4])) add(g, FIRST[d[4]], 'dna call', 1); if (d[5] !== null && FIRST[d[5]] !== undefined && atRun(d[5])) add(g, FIRST[d[5]], 'dna spawn', 1); });
    Object.keys(MADEOF).forEach(function (g) { MADEOF[g].forEach(function (x) { add(g, x, 'made-of', 1); }); });
    Object.keys(DEFW).forEach(function (g) { DEFW[g].forEach(function (x) { if (atRun(x[1])) add(g, x[0], 'definition', .6); }); });
    ANSW.forEach(function (p) { if (atRun(p[2])) add(p[0], p[1], 'answered', 1); });
    MEMROWS.forEach(function (m) { var k = 'm:' + m[0]; if (!NODE[k] || !NODE[k].mesh.visible) return; add(k, m[1], 'memory', 1); String(m[3] || '').split(' ').forEach(function (x) { if (x && +x !== G.space) add(k, x, 'memory', 1); }); });
    REL.forEach(function (r) { if (atRun(r[3])) add(r[0], r[2], relKind(r[1]), .8); });
    if ($('mapall').checked && MAPL) MAPL.forEach(function (l) { var a = SYM[l[0]] !== undefined ? String(SYM[l[0]]) : null, b = SYM[l[2]] !== undefined ? String(SYM[l[2]]) : null; if (!a && !b) return; add(a || 'g:' + l[0], b || 'g:' + l[2], l[1], .8); });
    var lines = Object.keys(agg).map(function (id) { return agg[id]; }), count = {};
    lines.forEach(function (l) { count[l[2]] = (count[l[2]] || 0) + 1; });
    Object.keys(RELSET).forEach(function (k) { var c = $('rc-' + k.replace(/[^a-z0-9]/gi, '_')); if (c) c.textContent = fmtN(count[k] || 0); });
    var vis = function (k) { var n = NODE[k]; return n && (!hasGL || n.mesh.visible); };
    // the pull law: the kind's pull (its slider), times the line's trust, times how much of that kind the brain holds; a row laid again pulls harder
    SPRINGS = lines.filter(function (l) { return RELSET[l[2]] && RELSET[l[2]].on && vis(l[0]) && vis(l[1]); }).map(function (l) {
      return { a: NODE[l[0]], b: NODE[l[1]], k: RELSET[l[2]].w * l[3] * (.5 + .5 * Math.min(1, count[l[2]] / 40)) * (1 + Math.log(l[4])), rest: REST[l[2]] || 30, kind: l[2], names: [l[0], l[1]], dir: RELSET[l[2]].dir === 'across' ? 'across' : dirVec(RELSET[l[2]].dir) }; });
    placeNew();
    ALLLINES = lines;
    return lines;
  }
  var MADEOF = {};
  function placeNew() {
    var nb = {}; SPRINGS.forEach(function (sp) { (nb[sp.names[0]] = nb[sp.names[0]] || []).push(sp.b); (nb[sp.names[1]] = nb[sp.names[1]] || []).push(sp.a); });
    for (var pass = 0; pass < 4; pass++) Object.keys(NODE).forEach(function (k) {
      var n = NODE[k]; if (!n.unplaced) return; var placed = (nb[k] || []).filter(function (m) { return !m.unplaced; }); if (!placed.length && pass < 3) return;
      var c = new THREE.Vector3(); placed.forEach(function (m) { c.add(m.pos); }); if (placed.length) c.multiplyScalar(1 / placed.length);
      n.pos.copy(c.add(unit('u' + k).multiplyScalar(placed.length ? 4 : 1))); n.unplaced = false;
    });
  }
  var STEP = 0, LASTMOVE = 0;
  function settle(steps) {
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
  var GAP = 15, ACROSS = .25, PASSES = 3;
  function spaceApart() {
    var pts = Object.keys(NODE).map(function (k) { return NODE[k]; }).filter(function (n) { return !hasGL || n.mesh.visible; }), cell = {}, g = GAP;
    pts.forEach(function (n) { var k = Math.floor(n.pos.x / g) + ',' + Math.floor(n.pos.y / g) + ',' + Math.floor(n.pos.z / g); (cell[k] = cell[k] || []).push(n); });
    pts.forEach(function (n) {
      var cx = Math.floor(n.pos.x / g), cy = Math.floor(n.pos.y / g), cz = Math.floor(n.pos.z / g);
      for (var i = -1; i <= 1; i++) for (var j = -1; j <= 1; j++) for (var k = -1; k <= 1; k++) (cell[(cx + i) + ',' + (cy + j) + ',' + (cz + k)] || []).forEach(function (o) {
        if (o === n || n.fixed || o.fixed) return;
        var d = n.pos.clone().sub(o.pos), L = d.length();
        if (L >= g) return;
        if (L < 1e-6) { d = unit('s' + n.key + '|' + o.key); L = 1e-6; }
        var push = d.normalize().multiplyScalar((g - L) / 2);
        n.pos.add(push); o.pos.sub(push);
      });
    });
  }
  var reshapeLeft = 0; function reshape() { if (!hasGL) return; settle(40); reshapeLeft = 90; }
  function drawLines(group, segs) { while (group.children.length) { var c = group.children.pop(); c.geometry.dispose(); c.material.dispose(); } Object.keys(segs).forEach(function (key) { var sg = segs[key]; if (!sg.pts.length) return; group.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(sg.pts), new THREE.LineBasicMaterial({ color: sg.color, transparent: true, opacity: sg.opacity }))); }); }
  function composition(lines) {
    var adj = {}; function add(r, a, b) { adj[r] = adj[r] || {}; (adj[r][a] = adj[r][a] || {})[b] = 1; }
    lines.forEach(function (l) { if (!RELSET[l[2]] || !RELSET[l[2]].on || l[2].indexOf('dna') === 0 || l[2] === 'memory' || l[2] === 'made-of' || l[2] === 'answered' || l[2] === 'definition') return; add(l[2], l[0], l[1]); if (l[2] === 'alike' || l[2] === 'opposite') add(l[2], l[1], l[0]); });
    var rels = Object.keys(adj), out = [];
    rels.forEach(function (r1) { rels.forEach(function (r2) { var n = 0, back = 0, hit = {}; Object.keys(adj[r1]).forEach(function (a) { Object.keys(adj[r1][a]).forEach(function (b) { var m2 = adj[r2][b]; if (!m2) return; Object.keys(m2).forEach(function (c) { if (c === a) { back++; return; } n++; rels.forEach(function (r3) { if (adj[r3][a] && adj[r3][a][c]) hit[r3] = (hit[r3] || 0) + 1; }); }); }); }); if (n || back) { var best = Object.keys(hit).sort(function (x, y) { return hit[y] - hit[x]; })[0]; out.push([r1, r2, n, back, best || null, best ? hit[best] : 0]); } }); });
    var h = '<tr><th>R1 then R2</th><th>paths</th><th>back</th><th>lands on</th></tr>';
    out.sort(function (a, b) { return b[2] - a[2]; }).slice(0, 10).forEach(function (r) { h += '<tr><td><span style="color:' + hexOf(r[0]) + '">' + esc(r[0]) + '</span> then <span style="color:' + hexOf(r[1]) + '">' + esc(r[1]) + '</span></td><td>' + r[2] + '</td><td>' + r[3] + '</td><td>' + (r[4] ? '<span style="color:' + hexOf(r[4]) + '">' + esc(r[4]) + '</span> ' + (r[2] ? Math.round(100 * r[5] / r[2]) + '%' : '') : '<span class="f">none</span>') + '</td></tr>'; });
    $('comp').innerHTML = out.length ? h : '<tr><td class="f">No two relationship lines join yet.</td></tr>';
  }
