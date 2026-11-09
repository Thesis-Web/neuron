#!/usr/bin/env python3
# page_patch9.py (2026-11-03, tries/41): the page loads what it shows and streams the run. The owner (11-03 ~01:40): "think of it like
# google earth... zoomed way out all the information at zoomed all the way in is not loaded... when the graph isn't doing anything it should
# still be firing 2 gb of ram and 100% core???"; (02:05) "inform the cortex of your plan give it your outline and get the fix done".
# What changes in the page's text (the look, the stage, the rails, the physics of the drawing: untouched):
#   1. loadBundle() no longer asks the door for the whole brain. It reads the history (the typed lines' receipts, as before), then by key
#      only what those receipts touch: the runs by id, the labels, places, DNA rows, definition-node counts and rel rows of the gates in them,
#      the first gate of each run, the newest typed lines and out rows, the formulas, your map. Every read is a few keyed rows; nothing is
#      read whole. The bundle it hands absorb() keeps the same shape, so everything after absorb is unchanged.
#   2. The receipts of a typed line are ordered in waves: the runs of one line (the main run, its calls, its spawns) interleaved by their
#      start clock, so one press of the hop button advances every run alive at that clock by one hit (the owner: "the next hop is the next
#      hop for the main and the next hop for each of the parallel runs").
#   3. The 10-minute whole re-read is gone. Every 2 s the page asks the door's counters and the runs that ended since its last look (by id,
#      keyed); when a new typed line ended, or a run under a line the page shows, it re-reads its light bundle (a second or two) and draws.
#   4. A gate chosen or clicked that the page has not loaded is read by key then.
# Two dialects, chosen by /api/info's version: the hub (v7: a table per gate, "N" and "N.node") and the kernel (nk: the dna and node tables
# keyed by gate; no range on the timeline, so new runs are found by id).
# v4 (03:05): the hub's history holds the newest 40 typed lines, not 300: the 300 reached back into the back-population lines of tries/35 (285,619 receipts, 39 s to open).
# v3 (02:55): on the hub the history is the newest 300 typed lines with their trees' receipts (by root, by run) plus the newest 5,000 receipts
# of the brain's own runs, so a line typed hours ago still steps and the door's 50,000-receipt cap no longer decides what the page shows.
# v2 (02:40): aliased reads (l., r., x.) so the kernel's door hands them to the kernel instead of its whole-brain cache; the sub-runs of the
# newest six lines (by the ids after each line's id) and their receipts by run, so the waves hold every run of a line on both brains.
# usage: python3 page_patch9.py <page.html>     (in place; prints what it replaced)
import sys
path = sys.argv[1]; t = open(path, encoding='utf-8').read()
def cut(a_marker, b_marker, start=0):
    a = t.index(a_marker, start); b = t.index(b_marker, a) + len(b_marker); return a, b

# ---- 1. loadBundle: light
a, b = cut("  function loadBundle() {", "    ]).then(absorb);\n  }")
LIGHT = r'''  // ---- tries/41: the page loads what it shows. Keyed reads only; the bundle keeps absorb()'s shape.
  var LIGHT = true, NK = false, LOADED = {}, LASTRUNSEEN = 0, LASTTL = 0, ROOTS = {}, HAVE = {};
  function isNK() { NK = !!(INFO && INFO.version === 'nk'); return NK; }
  function chunks(list, n) { var out = []; for (var i = 0; i < list.length; i += n) out.push(list.slice(i, i + n)); return out; }
  function marks(n) { var a = []; for (var i = 0; i < n; i++) a.push('?'); return a.join(','); }
  function qIn(sql, list, more, size) {   // sql with one %IN%; list split into chunks; rows concatenated; a refused read is an empty answer
    list = list.filter(function (x) { return x !== null && x !== undefined; }); if (!list.length) return Promise.resolve([]);
    return Promise.all(chunks(list, size || 400).map(function (c) { return q(sql.replace('%IN%', marks(c.length)), c.concat(more || [])).catch(function () { return []; }); })).then(function (parts) { return [].concat.apply([], parts); });
  }
  function qUnionTables(gates, body) {   // the hub's table per gate: one statement per 90 gates, UNION ALL; a missing table empties that chunk
    gates = gates.filter(function (g) { return g > 0; }); if (!gates.length) return Promise.resolve([]);
    return Promise.all(chunks(gates, 90).map(function (c) { var sql = c.map(function (g) { return body.replace(/%G%/g, String(g)); }).join(' UNION ALL '); return q(sql).catch(function () { return Promise.all(c.map(function (g) { return q(body.replace(/%G%/g, String(g))).catch(function () { return []; }); })).then(function (p) { return [].concat.apply([], p); }); }); })).then(function (parts) { return [].concat.apply([], parts); });
  }
  function dnaOf(gates) {   // rows [gate, shard, before, trigger, call, spawn, times]
    if (isNK()) return qIn('SELECT gate, shard, before, trigger, call, spawn, times FROM main.dna WHERE gate IN (%IN%)', gates);
    return qUnionTables(gates, 'SELECT %G% AS gate, shard, before, trigger, call, spawn, times FROM main."%G%"');
  }
  function nodesOf(gates) {   // rows [gate, source, run]
    if (isNK()) return qIn('SELECT gate, source, run FROM main.node WHERE gate IN (%IN%)', gates);
    return qUnionTables(gates, 'SELECT %G% AS gate, source, run FROM main."%G%.node"');
  }
  function gatesOfRows(rows, cols) { var s = {}; rows.forEach(function (r) { cols.forEach(function (c) { if (r[c] !== null && r[c] !== undefined && r[c] > 0) s[r[c]] = 1; }); }); return Object.keys(s).map(Number); }
  function loadBundle() {
    var core = []; for (var i = 1; i <= CORE; i++) core.push(i);
    var histQ = isNK() ? q('SELECT id, run, gate, shard FROM main.run_receipt WHERE id > ? ORDER BY id', [HISTLAST])
      : q('SELECT max(id) FROM main.run_receipt').then(function (r) { var top = r[0] ? r[0][0] : 0; return q('SELECT id, run, gate, shard FROM main.run_receipt WHERE id > ? ORDER BY id', [Math.max(HISTLAST, top - 5000)]); })   // the hub: the newest 5,000 of the brain's own runs
        .then(function (rc) {   // and the typed lines: the newest 300 inputs, their trees by root, their receipts by run (the hub's receipt_run index)
          return q("SELECT run FROM main.input WHERE run IS NOT NULL ORDER BY id DESC LIMIT 40").catch(function () { return []; }).then(function (ins) {
            var lineRuns = ins.map(function (r) { return r[0]; }).filter(function (v) { return v && !RUNHOPS[v]; });
            return qIn('SELECT r.id FROM main.run r WHERE r.root IN (%IN%)', lineRuns, [], 60).then(function (kids) {
              var want = lineRuns.concat(kids.map(function (k) { return k[0]; })).filter(function (v, i, a) { return a.indexOf(v) === i && !RUNHOPS[v]; });
              return qIn('SELECT id, run, pos, gate, shard FROM main.run_receipt WHERE run IN (%IN%)', want, [], 200).then(function (rows) {
                rows.sort(function (a, b) { return a[1] - b[1] || a[2] - b[2]; }); var seen = {}; rc.forEach(function (x) { seen[x[0]] = 1; });
                rows.forEach(function (s) { if (!seen[s[0]] && !HAVE[s[0]]) { seen[s[0]] = 1; HAVE[s[0]] = 1; var row = [s[0], s[1], s[3], s[4]]; row.sub = true; rc.push(row); } });
                return rc;
              });
            });
          });
        });
    return histQ.then(function (rc) {
      var runs = gatesOfRows(rc, [1]), gates = gatesOfRows(rc, [2]).concat(core);
      HIST.forEach(function (h) { if (!(h[1] in RUNS)) runs.push(h[1]); });   // runs seen before: kept in the table
      var runIds = Object.keys(RUNS).map(Number).concat(runs); runIds = runIds.filter(function (v, i, a) { return a.indexOf(v) === i; });
      return qIn('SELECT r.id, r.arrival, r.parent, r.root, r.kind, r.cell, r.about, r.at FROM main.run r WHERE r.id IN (%IN%)', runIds).then(function (rr) {
        var roots = gatesOfRows(rr, [3]).concat(rr.filter(function (r) { return r[3] === null; }).map(function (r) { return r[0]; }));
        roots = roots.filter(function (v, i, a) { return a.indexOf(v) === i; }); ROOTS = {}; roots.forEach(function (r) { ROOTS[r] = 1; });
        var newest = roots.slice(-6), after = []; newest.forEach(function (r) { for (var i = 1; i <= 400; i++) after.push(r + i); });   // a line's sub-runs follow its id
        var treeQ = isNK() ? qIn('SELECT r.id, r.arrival, r.parent, r.root, r.kind, r.cell, r.about, r.at FROM main.run r WHERE r.id IN (%IN%)', after, [], 400).then(function (rows) { return rows.filter(function (r) { return r[3] !== null && ROOTS[r[3]]; }); })
                            : qIn('SELECT r.id, r.arrival, r.parent, r.root, r.kind, r.cell, r.about, r.at FROM main.run r WHERE r.root IN (%IN%)', roots.slice(-40), [], 60);
        return treeQ.then(function (tree) {
          var seen = {}; var allRuns = rr.concat(tree).filter(function (r) { if (seen[r[0]]) return false; seen[r[0]] = 1; return true; });
          // the receipts of the newest lines' sub-runs, by run (the waves need every run of a line); a row already held is not taken twice
          var subRuns = allRuns.filter(function (r) { return r[3] !== null && newest.indexOf(r[3]) >= 0 && !RUNHOPS[r[0]]; }).map(function (r) { return r[0]; }).filter(function (v) { return rc.every(function (x) { return x[1] !== v; }); });
          return qIn('SELECT id, run, pos, gate, shard FROM main.run_receipt WHERE run IN (%IN%)', subRuns, [], 200).then(function (sub) {
          sub.sort(function (a, b) { return a[1] - b[1] || a[2] - b[2]; }); sub.forEach(function (s) { if (!HAVE[s[0]]) { HAVE[s[0]] = 1; var row = [s[0], s[1], s[3], s[4]]; row.sub = true; rc.push(row); } });
          gates = gates.concat(gatesOfRows(sub, [3]));
          var moreGates = gatesOfRows(allRuns, [1, 5, 6]); gates = gates.concat(moreGates).filter(function (v, i, a) { return a.indexOf(v) === i; });
          var runList = allRuns.map(function (r) { return r[0]; });
          return Promise.all([
            qIn('SELECT l.gate, l.symbol FROM main.label l WHERE l.gate IN (%IN%)', gates, [], 500),
            dnaOf(gates),
            nodesOf(gates),
            qIn('SELECT gate, kind, other, run FROM main.rel WHERE gate IN (%IN%)', gates, [], 300),
            qIn('SELECT gate, kind, other, run FROM main.rel WHERE other IN (%IN%)', gates, [], 300),
            qIn('SELECT run, gate FROM main.seq WHERE run IN (%IN%) AND pos = 1', runList),
            isNK() ? q("SELECT 'main', id, run FROM main.input WHERE run IS NOT NULL UNION ALL SELECT 'sixth', id, run FROM sixth.input WHERE run IS NOT NULL ORDER BY 1, 2").catch(function () { return []; })
                   : q("SELECT 'main', id, run FROM main.input WHERE run IS NOT NULL ORDER BY id DESC LIMIT 300").then(function (r) { return r.reverse(); }).catch(function () { return []; }),
            q('SELECT id, run, cell, value FROM main.out_user ORDER BY id DESC LIMIT 400').then(function (r) { return r.reverse(); }).catch(function () { return []; }),
            isNK() ? q("SELECT (SELECT count(*) FROM main.label), (SELECT count(*) FROM main.sqlite_master WHERE type = 'table'), (SELECT count(*) FROM main.sqlite_master WHERE type = 'trigger'), (SELECT n FROM main.shards), (SELECT count(*) FROM main.run), (SELECT count(*) FROM main.run_receipt), (SELECT count(*) FROM main.run_sheet), (SELECT count(*) FROM main.run_memory), (SELECT count(*) FROM main.timeline), (SELECT count(*) FROM main.refused), (SELECT count(*) FROM main.hop), (SELECT count(*) FROM main.run_sheet WHERE state = 0), (SELECT count(*) FROM main.run WHERE id NOT IN (SELECT run FROM main.run_memory)), (SELECT count(*) FROM main.rel), (SELECT count(*) FROM sixth.label), (SELECT count(*) FROM sixth.run), (SELECT count(*) FROM sixth.run_memory), (SELECT count(*) FROM sixth.refused), (SELECT count(*) FROM main.run WHERE kind = 3 AND arrival BETWEEN 7 AND 14)").catch(function () { return [[0]]; })
                   : Promise.all([q('SELECT max(gate) FROM main.label'), q('SELECT n FROM main.shards'), q('SELECT max(id) FROM main.run'), q('SELECT max(id) FROM main.run_receipt'), q('SELECT max(id) FROM main.timeline'), q('SELECT count(*) FROM main.refused'), q('SELECT count(*) FROM main.hop'), q('SELECT max(gate) FROM sixth.label'), q('SELECT max(id) FROM sixth.run'), q('SELECT count(*) FROM sixth.refused')].map(function (p) { return p.then(function (r) { return r[0] ? r[0][0] : 0; }).catch(function () { return 0; }); })).then(function (v) { return [[v[0], 0, 0, v[1], v[2], v[3], 0, 0, v[4], v[5], v[6], 0, 0, COUNTS.rel || 0, v[7], v[8], 0, v[9], 0]]; }),
            MAPL ? Promise.resolve(null) : q("SELECT word, text FROM map.corpus").catch(function () { return []; }),
            qIn('SELECT x.gate, x.x, x.y, x.z, x.moved FROM main.xyz x WHERE x.gate IN (%IN%)', gates, [], 500),
            q('SELECT p.kind, f.pull, f.rest, f.dx, f.dy, f.dz, f.mode FROM main.pull p JOIN main.formula f ON f.id = p.formula').catch(function () { return []; })
          ]).then(function (P) {
            // the 'definition' and 'answered' lines: from the node rows of the loaded gates (source, run) and the first symbols of those runs
            var nodeRows = P[2], defRuns = nodeRows.map(function (r) { return r[2]; }).filter(function (v, i, a) { return a.indexOf(v) === i; }).slice(0, 1200);
            return qIn('SELECT run, gate FROM main.seq WHERE run IN (%IN%)', defRuns, [], 200).then(function (sq) {
              var runAbout = {}; nodeRows.forEach(function (r) { runAbout[r[2]] = r[0]; });
              var defw = {}, seenDW = {}; sq.forEach(function (s) { var ab = runAbout[s[0]]; if (ab === undefined) return; var sym = LAB[s[1]]; var k = ab + ':' + s[1]; if (seenDW[k]) return; seenDW[k] = 1; (defw[ab] = defw[ab] || []).push([s[1], s[0]]); });
              var R6 = []; Object.keys(defw).forEach(function (ab) { defw[ab].forEach(function (p) { R6.push([+ab, p[0], p[1]]); }); });
              var ansSeen = {}, R7 = []; nodeRows.forEach(function (r) { var k = r[1] + ':' + r[0]; if (ansSeen[k]) return; ansSeen[k] = 1; R7.push([r[1], r[0], r[2]]); });
              var nodes = {}; nodeRows.forEach(function (r) { nodes[r[0]] = (nodes[r[0]] || 0) + 1; });
              var relSeen = {}, rel = []; P[3].concat(P[4]).forEach(function (r) { var k = r[0] + ':' + r[1] + ':' + r[2] + ':' + r[3]; if (relSeen[k]) return; relSeen[k] = 1; rel.push(r); });
              var first = {}; P[5].forEach(function (r) { first[r[0]] = r[1]; });
              var hop = {}; rc.forEach(function (r) { hop[r[1]] = (hop[r[1]] || 0) + 1; }); var R8 = Object.keys(hop).map(function (k) { return [+k, hop[k]]; });
              var graph = { dna: P[1], nodes: nodes, rel: rel, mem: MEMN || {}, first: first, clock: null };
              gates.forEach(function (g) { LOADED[g] = 1; });
              return absorb([P[0], graph, allRuns, P[6], P[7], P[8], R6, R7, R8, P[9], rc, P[10], P[11]]);
            });
          });
          });
        });
      });
    });
  }
  // a gate the page has not loaded (chosen, clicked, or in a run just chosen): its label, DNA rows, node count, rel rows and place, by key
  function loadGates(gates) {
    gates = gates.filter(function (g) { return g > 0 && !LOADED[g]; }).filter(function (v, i, a) { return a.indexOf(v) === i; }); if (!gates.length) return Promise.resolve();
    return Promise.all([qIn('SELECT l.gate, l.symbol FROM main.label l WHERE l.gate IN (%IN%)', gates, [], 500), dnaOf(gates), nodesOf(gates), qIn('SELECT gate, kind, other, run FROM main.rel WHERE gate IN (%IN%)', gates, [], 300), qIn('SELECT gate, kind, other, run FROM main.rel WHERE other IN (%IN%)', gates, [], 300), qIn('SELECT x.gate, x.x, x.y, x.z, x.moved FROM main.xyz x WHERE x.gate IN (%IN%)', gates, [], 500)]).then(function (P) {
      P[0].forEach(function (r) { if (LAB[r[0]] === undefined) { LAB[r[0]] = r[1]; SYM[r[1]] = r[0]; LABLIST.push(r[0]); } });
      P[1].forEach(function (d) { DNA.push(d); (DNABY[d[0]] = DNABY[d[0]] || []).push(d); SHARDROW[d[1]] = d; });
      P[2].forEach(function (r) { NODES[r[0]] = (NODES[r[0]] || 0) + 1; });
      P[3].concat(P[4]).forEach(function (r) { REL.push(r); (RELBY[r[0]] = RELBY[r[0]] || []).push(r); (RELBY[r[2]] = RELBY[r[2]] || []).push(r); });
      P[5].forEach(function (r) { XYZ[r[0]] = r; });
      gates.forEach(function (g) { LOADED[g] = 1; });
    });
  }
  function gatesOfRun(root) { var s = {}; HIST.forEach(function (h) { var R = RUNS[h[1]]; if (h[1] === root || (R && R.root === root)) s[h[2]] = 1; }); return Object.keys(s).map(Number); }'''
t = t[:a] + LIGHT + t[b:]

# ---- 2. the history in waves: the runs of one line interleaved by their start clock
old = "    R[10].forEach(function (r) { var i = HIST.length; HIST.push(r); HISTLAST = r[0]; (RUNHOPS[r[1]] = RUNHOPS[r[1]] || []).push(i); if (FIRSTG[r[2]] === undefined) FIRSTG[r[2]] = i; if (FIRSTS[r[3]] === undefined) FIRSTS[r[3]] = i; if (RUNT0[r[1]] === undefined) RUNT0[r[1]] = i; RUNT1[r[1]] = i; });"
assert t.count(old) == 1, 'absorb history line'
new = r'''    // tries/41: the receipts of one line in waves: its runs ordered by start clock, one hit of each run alive per wave (the owner: one hop is the next hop of the main run and of every parallel run)
    var byRoot = {}, rootOrder = []; R[10].forEach(function (r) { var Rr = RUNS[r[1]], root = Rr ? (Rr.root === null ? r[1] : Rr.root) : r[1]; if (!byRoot[root]) { byRoot[root] = {}; rootOrder.push(root); } (byRoot[root][r[1]] = byRoot[root][r[1]] || []).push(r); });
    var ordered = []; rootOrder.forEach(function (root) { var runs = Object.keys(byRoot[root]).map(Number).sort(function (x, y) { var ax = RUNS[x] ? RUNS[x].at : x, ay = RUNS[y] ? RUNS[y].at : y; return ax - ay || x - y; }); var cur = runs.map(function () { return 0; }), left = 0; runs.forEach(function (rn) { left += byRoot[root][rn].length; }); var wave = 0; while (left > 0) { for (var k = 0; k < runs.length; k++) { var rows = byRoot[root][runs[k]]; if (cur[k] < rows.length) { var row = rows[cur[k]++]; row.wave = WAVEN + wave; ordered.push(row); left--; } } wave++; } WAVEN += wave; });
    ordered.forEach(function (r) { var i = HIST.length; HIST.push(r); WAVE[i] = r.wave; if (!r.sub) HISTLAST = Math.max(HISTLAST, r[0]); (RUNHOPS[r[1]] = RUNHOPS[r[1]] || []).push(i); if (FIRSTG[r[2]] === undefined) FIRSTG[r[2]] = i; if (FIRSTS[r[3]] === undefined) FIRSTS[r[3]] = i; if (RUNT0[r[1]] === undefined) RUNT0[r[1]] = i; RUNT1[r[1]] = i; });'''
t = t.replace(old, new)
old = "  var HIST = [], RUNHOPS = {}, FIRSTG = {}, FIRSTS = {}, RUNT0 = {}, RUNT1 = {}, TK = -1, HISTLAST = 0;"
assert t.count(old) == 1; t = t.replace(old, old + "\n  var WAVE = [], WAVEN = 0;   // tries/41: the wave (the clock tick of the line) each receipt belongs to")

# ---- 3. one press of the hop button: the whole wave
old = """  function advance(k) {
    if (TK >= HIST.length - 1) { setPlay(false); return; }
    var nt = Math.min(HIST.length - 1, TK + k);"""
assert t.count(old) == 1
new = """  function advance(k) {
    if (TK >= HIST.length - 1) { setPlay(false); return; }
    var nt = Math.min(HIST.length - 1, TK + k);
    if (k === 1 && WAVE[TK + 1] !== undefined) { nt = TK + 1; while (nt + 1 < HIST.length && WAVE[nt + 1] === WAVE[TK + 1]) nt++; }   // tries/41: one hop = every run alive at this clock, one hit each"""
t = t.replace(old, new)
old = "    $('readout').textContent = h ? 'hop ' + hi + ' of ' + (hs.length - 1) + ' in run ' + h[1] : 'hop 0 of 0';"
assert t.count(old) == 1
new = "    var alive = 0; if (h && WAVE[tk] !== undefined) { var wseen = {}; for (var wi = tk; wi >= 0 && WAVE[wi] === WAVE[tk]; wi--) wseen[HIST[wi][1]] = 1; alive = Object.keys(wseen).length; }\n    $('readout').textContent = h ? 'hop ' + hi + ' of ' + (hs.length - 1) + ' in run ' + h[1] + (alive > 1 ? ' · ' + alive + ' runs alive this hop' : '') : 'hop 0 of 0';"
t = t.replace(old, new)

# ---- 4. a run chosen or a gate shown that is not loaded: read it by key first
old = """  function chooseRun(id, hop, then) {
    var R = RUNS[id]; if (!R) return; var hs = RUNHOPS[id] || [];
    CUR.run = id; CUR.root = R.root === null ? id : R.root;
    refreshMem(function () { renderTree(); renderRun(); render(hs.length ? hs[Math.min(hs.length - 1, hop || 0)] : TK, true); if (then) then(); });"""
assert t.count(old) == 1
new = """  function chooseRun(id, hop, then) {
    var R = RUNS[id]; if (!R) return; var hs = RUNHOPS[id] || [];
    CUR.run = id; CUR.root = R.root === null ? id : R.root;
    loadGates(gatesOfRun(CUR.root)).catch(function () {}).then(function () { refreshMem(function () { renderTree(); renderRun(); render(hs.length ? hs[Math.min(hs.length - 1, hop || 0)] : TK, true); if (then) then(); }); });"""
t = t.replace(old, new)
old = """  function showNode(g) {
    if (LAB[g] === undefined) return; SELG = g; var role = roleOf(g);"""
assert t.count(old) == 1
new = """  function showNode(g) {
    if (!LOADED[g]) { loadGates([g]).catch(function () {}).then(function () { if (LAB[g] !== undefined) showNode(g); }); return; }
    if (LAB[g] === undefined) return; SELG = g; var role = roleOf(g);"""
t = t.replace(old, new)

# ---- 5. the stream in place of the 10-minute whole re-read (the hub's page has it; the kernel's has none)
if "  var REREADING = false, REREAD_MARK = null;" in t:
    a = t.index("  var REREADING = false, REREAD_MARK = null;"); b = t.index("}, 600000);", a); b = t.index("\n", b) + 1
    t = t[:a] + t[b:]
anchor = "  open(0);\n"
assert t.count(anchor) == 1
STREAM = r'''  open(0);
  // tries/41: the stream. Every 2 s: the door's counters (not a read of the brain); when runs ended since the last look, the ones by id
  // (keyed) tell whether a new typed line ended or a run under a line the page shows; then the light bundle is read again and drawn.
  var WATCHING = false, WATCHRUNS = 0;
  function newRunsSince(last, upto) { var ids = []; for (var i = last + 1; i <= upto && ids.length < 2000; i++) ids.push(i); return qIn('SELECT r.id, r.arrival, r.parent, r.root, r.kind FROM main.run r WHERE r.id IN (%IN%)', ids, [], 400); }
  setInterval(function watch() {
    if (!ready || busy || WATCHING) return; WATCHING = true;
    api('/api/info').then(function (info) {
      var upto = info.stats ? info.stats.main.runs : null;
      var p = upto !== null ? Promise.resolve(upto) : q('SELECT max(id) FROM main.run').then(function (r) { return r[0] ? r[0][0] : 0; });
      return p.then(function (top) {
        if (!WATCHRUNS) { WATCHRUNS = top; return; }
        if (top <= WATCHRUNS) return;
        return newRunsSince(WATCHRUNS, top).then(function (rows) {
          WATCHRUNS = top;
          var want = rows.some(function (r) { return (r[4] === 0 && r[1] === G.heard) || (r[3] !== null && ROOTS[r[3]]) || ROOTS[r[0]]; });
          if (!want || playing) return;
          return loadBundle().then(function () { renderAll(); renderOut(); refreshMem(function () { render(TK, true); }); });
        });
      });
    }).catch(function () {}).then(function () { WATCHING = false; });
  }, 2000);
'''
t = t.replace(anchor, STREAM)
# the lines-to-type read and the typed-line path stay as they are: afterLine() reads the light bundle (now a second or two)
assert t.count("window.__poc = {") == 1; t = t.replace("window.__poc = {", "window.__poc = { light: true, hist: function () { return HIST.length; }, waves: function () { return WAVEN; }, loaded: function () { return Object.keys(LOADED).length; },")
open(path, 'w', encoding='utf-8').write(t)
print('patched', path, ': light bundle, waves, wave hop, keyed loads on choose/show, the stream in place of the re-read')
