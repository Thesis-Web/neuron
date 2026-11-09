#!/usr/bin/env python3
# page_patch8.py (2026-11-02, tries/38): the pages stop starving the door. The owner (22:10): "you found the problem on the hub ... fix it???".
# From 19:39:58 to 22:14 the hub's router ran no hop: the page re-read its whole bundle every 120 s (the graph, the run table, label,
# out_user, the counts) whether or not anything changed and whether or not the last re-read had finished, and polled the places every 2 s
# with no guard; every one of those is a read on the brain's one connection between two hops, queued faster than it was served.
# Two changes to the page's text, the look untouched:
#   1. the re-read (every 10 min now, was 2) first asks the door's own counters (/api/info, not a read of the brain) and re-reads the bundle only when they
#      moved since the last bundle, and never while a re-read is still in flight;
#   2. pollMoved runs one poll at a time, and a door that has no /api/moved (the hub's) is asked once and then read by its table.
# usage: python3 page_patch8.py <page.html>     (patches in place; prints what it replaced)
import sys
path = sys.argv[1]; t = open(path, encoding='utf-8').read()

# 1. the re-read
if 'setInterval(function reread() {' not in t:
    print('no periodic re-read in this page (the kernel\'s page has none); only the poll is patched'); a = b = None
else:
    a = t.index('setInterval(function reread() {'); b = t.index('}, 120000);', a) + len('}, 120000);')
    old = t[a:b]; assert 'loadBundle().then(function () { renderAll(); renderOut(); refreshMem(function () { render(TK, true); }); })' in old, old
if a is not None:
  new = ("var REREADING = false, REREAD_MARK = null;   // tries/38: one re-read at a time, and only when the brain moved\n"
       "  setInterval(function reread() { if (!ready || busy || playing || REREADING) return;\n"
       "    api('/api/info').then(function (info) {   // the door's own counters, not a read of the brain\n"
       "      var mark = JSON.stringify(info.stats ? info.stats.main.runs : (info.routers ? info.routers.main.hops : null));\n"
       "      if (mark === REREAD_MARK) return; REREAD_MARK = mark; REREADING = true;\n"
       "      return loadBundle().then(function () { renderAll(); renderOut(); refreshMem(function () { render(TK, true); }); }).catch(function () {}).then(function () { REREADING = false; });\n"
       "    }).catch(function () {}); }, 600000);   // tries/38: every 10 min, not 2: a whole-bundle re-read costs the brain ~46 s of its one connection")
  t = t[:a] + new + t[b:]

# 2. the poll of moved points
a = t.index('  function pollMoved() {'); b = t.index('  setInterval(pollMoved, 2000);', a)
old = t[a:b]; assert "/api/moved?since=" in old and "q('SELECT gate, x, y, z, at FROM main.xyz WHERE at > ? ORDER BY at LIMIT 20000', [XYZCLOCK])" in old, old
new = ("  var POLLING = false, NOMOVED = false;   // tries/38: one poll at a time; a door without /api/moved is read by its table from then on\n"
       "  function pollMoved() {\n"
       "    if (!ready || !brainOn() || POLLING) return; POLLING = true;\n"
       "    function fromTable() { return q('SELECT gate, x, y, z, at FROM main.xyz WHERE at > ? ORDER BY at LIMIT 20000', [XYZCLOCK]).then(function (rows) { rows.forEach(function (m) { XYZ[m[0]] = [m[0], m[1], m[2], m[3], 0]; var n = NODE[String(m[0])]; if (n && n.mesh && n.mesh.visible) n.glide = new THREE.Vector3(m[1] * SP, m[2] * SP, m[3] * SP); if (m[4] > XYZCLOCK) XYZCLOCK = m[4]; }); }); }\n"
       "    var p = NOMOVED ? fromTable() : api('/api/moved?since=' + XYZCLOCK).then(function (j) { if (j.passes) { api('/api/graph?fresh=1').then(function (g) { XYZ = {}; (g.xyz || []).forEach(function (r) { XYZ[r[0]] = r; }); Object.keys(NODE).forEach(function (k) { if (NODE[k].mesh && NODE[k].mesh.visible) brainPos(k, NODE[k]); }); }); }\n"
       "      (j.moved || []).forEach(function (m) { XYZ[m[0]] = [m[0], m[1], m[2], m[3], 0]; var n = NODE[String(m[0])]; if (n && n.mesh && n.mesh.visible) { n.glide = new THREE.Vector3(m[1] * SP, m[2] * SP, m[3] * SP); } });\n"
       "      if (j.clock) XYZCLOCK = j.clock; }).catch(function (e) { if (e && /no such path/.test(String(e.message))) NOMOVED = true; return fromTable(); });\n"
       "    p.catch(function () {}).then(function () { POLLING = false; });\n"
       "  }\n")
t = t[:a] + new + t[b:]
open(path, 'w', encoding='utf-8').write(t)
print('patched', path, ': the re-read guarded and keyed on the door counters; the poll one at a time, /api/moved remembered')
