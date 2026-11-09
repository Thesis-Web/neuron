#!/usr/bin/env python3
# page_patch11.py (2026-11-03, tries/43): the door tells the page; the page never asks on a clock. The owner (13:30): "The page asks the door
# every two seconds whether anything moved <-- basically a timer and a sweep,,, both which just won't work in a system like this.... a webpage
# with two users, one is the back end and one is the user on the front end, both are doing things and reporting or calling to the other".
# Gone: setInterval(pollMoved) (hp: /api/moved every 2 s; the hub: a scan of xyz by its clock column every 2 s), the whole-brain re-read after
# a pass, setInterval(watch) (/api/info every 2 s). Now: one EventSource per tab on /api/stream; a move glides the held point; a run's end is
# read by its id and, when a typed line ended or a run under a line shown, the light bundle is read again; after a pass the held gates' places
# are re-read by key; a hold post after each loadGates names what the tab holds. A door without the stream is said so in a line under the
# readout, with no timer behind it. Applies on top of page_patch10b (tries/42). usage: python3 page_patch11.py <page.html>
import sys, re
path = sys.argv[1]; t = open(path, encoding='utf-8').read()

# 1. the poll block (var POLLING ... setInterval(pollMoved, 2000);) becomes the stream
m = re.search(r"  var POLLING = false, NOMOVED = false;.*?setInterval\(pollMoved, 2000\);", t, flags=re.S)
assert m and t.count('setInterval(pollMoved, 2000);') == 1, 'poll block'
stream = r"""  // tries/43: the door tells the page. No timer, no sweep (the owner, 13:30): one open connection per tab; the door writes a move (with the
  // point's place) or a run's end the moment the brain laid its receipt. A door without the stream is said so under the readout, and nothing
  // asks on a clock. The hub's door filters moves to the gates this tab holds (/api/hold); the kernel's door sends the moves since its clock.
  var TAB = Math.random().toString(36).slice(2, 10), STREAM = { state: 'not started', told: 0, moves: 0, ends: 0, passes: 0, es: null };
  function streamNote() {
    var el = $('stream');
    if (!el) { el = document.createElement('div'); el.id = 'stream'; el.style.cssText = 'font-size:11px;opacity:.75;margin-top:2px'; var r = $('readout'); if (r && r.parentNode) r.parentNode.insertBefore(el, r.nextSibling); else document.body.appendChild(el); }
    el.textContent = 'stream ' + STREAM.state + (STREAM.moves || STREAM.ends || STREAM.passes ? ' · told ' + STREAM.moves + ' moves, ' + STREAM.ends + ' run ends' + (STREAM.passes ? ', ' + STREAM.passes + ' passes' : '') : '');
  }
  function hold(gates) { if (!gates || !gates.length) return Promise.resolve(); return api('/api/hold', { tab: TAB, add: gates }).catch(function () {}); }
  function onMoves(moves) { moves.forEach(function (m) { XYZ[m[0]] = [m[0], m[1], m[2], m[3], 0]; var n = NODE[String(m[0])]; if (n && n.mesh && n.mesh.visible) n.glide = new THREE.Vector3(m[1] * SP, m[2] * SP, m[3] * SP); }); STREAM.moves += moves.length; }
  function onPass() {   // a settle pass moved every placed point: the held gates' places are read again by key, never the brain whole
    var held = Object.keys(LOADED).map(Number); STREAM.passes++; if (!held.length) return;
    qIn('SELECT x.gate, x.x, x.y, x.z, x.moved FROM main.xyz x WHERE x.gate IN (%IN%)', held, [], 500).then(function (rows) { rows.forEach(function (r) { XYZ[r[0]] = r; }); Object.keys(NODE).forEach(function (k) { var n = NODE[k], b = XYZ[+k]; if (n.mesh && n.mesh.visible && b) n.glide = new THREE.Vector3(b[1] * SP, b[2] * SP, b[3] * SP); }); }).catch(function () {});
  }
  function stream() {
    if (!window.EventSource) { STREAM.state = 'none: this browser has no event stream'; streamNote(); return; }
    var es = new EventSource(API + '/api/stream?tab=' + TAB); STREAM.es = es; STREAM.state = 'opening'; streamNote();
    es.onopen = function () { STREAM.state = 'live'; streamNote(); hold(Object.keys(LOADED).map(Number)); };
    es.onmessage = function (ev) {
      var j; try { j = JSON.parse(ev.data); } catch (e) { return; }
      if (j.hello) { STREAM.state = 'live'; streamNote(); return; }
      if (j.id) STREAM.told = j.id;
      if (j.clock) XYZCLOCK = j.clock;
      if (j.passes) onPass();
      if (j.moves && j.moves.length) onMoves(j.moves);
      var ids = [];
      if (j.ends) j.ends.forEach(function (e) { ids.push(e[0]); });
      if (j.runs && j.runs_before && j.runs > j.runs_before) for (var i = j.runs_before + 1; i <= j.runs && ids.length < 2000; i++) ids.push(i);
      if (ids.length) { STREAM.ends += ids.length; watch(ids); }
      streamNote();
    };
    es.onerror = function () { STREAM.state = es.readyState === 2 ? 'none: the door has no stream yet (the door needs its restart); nothing is asked on a clock' : 'reconnecting'; streamNote(); };
  }
  stream();"""
t = t[:m.start()] + stream + t[m.end():]

# 2. the watch timer becomes a function the stream calls with the ids of the runs that ended
m = re.search(r"  var WATCHING = false, WATCHRUNS = 0;.*?\n  \}, 2000\);", t, flags=re.S)
assert m, 'watch block'
watch = r"""  // tries/43: a run's end arrives on the stream; the runs are read by id (keyed) and, when a typed line ended or a run under a line shown
  // ended, the light bundle is read again and drawn. No timer: ids that arrive while the page is busy wait for the next event.
  var WATCHING = false, WATCHPEND = [];
  function runsById(ids) { return qIn('SELECT r.id, r.arrival, r.parent, r.root, r.kind FROM main.run r WHERE r.id IN (%IN%)', ids, [], 400); }
  function watch(ids) {
    if (ids && ids.length) WATCHPEND = WATCHPEND.concat(ids);
    if (!ready || busy || WATCHING || !WATCHPEND.length) return; WATCHING = true;
    var take = WATCHPEND.splice(0, 2000);
    runsById(take).then(function (rows) {
      var want = rows.some(function (r) { return (r[4] === 0 && r[1] === G.heard) || (r[3] !== null && ROOTS[r[3]]) || ROOTS[r[0]]; });
      if (!want || playing) return;
      return loadBundle().then(function () { renderAll(); renderOut(); refreshMem(function () { render(TK, true); }); });
    }).catch(function () {}).then(function () { WATCHING = false; if (WATCHPEND.length) watch(); });
  }"""
t = t[:m.start()] + watch + t[m.end():]

# 3. a hold post after each loadGates (the gates this tab holds: its zoom)
old = "P[5].forEach(function (r) { XYZ[r[0]] = r; });\n      gates.forEach(function (g) { LOADED[g] = 1; });"
assert t.count(old) == 1, 'loadGates end'
t = t.replace(old, "P[5].forEach(function (r) { XYZ[r[0]] = r; });\n      gates.forEach(function (g) { LOADED[g] = 1; }); hold(gates);   // tries/43: the door is told what this tab holds")

# 4. a counter of the page's own requests, for the check that nothing asks on a clock
old = "  function api(path, body) {"
assert t.count(old) == 1, 'api()'
t = t.replace(old, "  var FETCHN = 0;   // tries/43: every request this page makes, counted (the check: none in thirty seconds of silence)\n  function api(path, body) {\n    FETCHN++;")

# 5. the handle for the headless check
m = re.search(r"window\.__poc = \{", t)
assert m, '__poc'
t = t[:m.end()] + " stream: function () { return STREAM.state; }, told: function () { return STREAM.told; }, fetches: function () { return FETCHN; }, streamCounts: function () { return { moves: STREAM.moves, ends: STREAM.ends, passes: STREAM.passes }; }, tab: function () { return TAB; }," + t[m.end():]

open(path, 'w', encoding='utf-8').write(t)
print('patched', path, ': the timers are gone; one event stream per tab; a hold post after each loadGates; the fetch counter; __poc.stream()')
