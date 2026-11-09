// cdp_c9.js (2026-11-03, tries/45): the Cortex's C9 expected output, read live: a headless run of the kernel page reports the counts
// (visible points, springs drawn, relationship lines drawn, xyz entries held, memory nodes drawn for the chosen line and after a point is
// clicked) and saves a screenshot. The brain's places switch is left as the page has it (on). Prints JSON lines; nothing is typed.
// usage: LD_LIBRARY_PATH=<libs> URL=http://10.31.1.106:8058/full OUT=/path/shot.png [PORT=9392] node cdp_c9.js
const { spawn } = require('child_process'); const fs = require('fs');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +(process.env.PORT || 9392), URL = process.env.URL, OUT = process.env.OUT;
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=1800,1000', '--remote-debugging-port=' + PORT, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let t = null; for (let i = 0; i < 60 && !t; i++) { await sleep(500); try { t = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  if (!t) { console.log(JSON.stringify({ error: 'no chrome' })); process.exit(1); }
  const page = t.find(x => x.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const wait = {}; const exc = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && wait[d.id]) { wait[d.id](d); delete wait[d.id]; } if (d.method === 'Runtime.exceptionThrown') exc.push(String(d.params.exceptionDetails.exception && d.params.exceptionDetails.exception.description || d.params.exceptionDetails.text).slice(0, 200)); };
  const send = (m, p) => new Promise(r => { const i = ++id; wait[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
  const ev = (e, ms) => Promise.race([send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true }).then(r => r.result && r.result.result ? r.result.result.value : JSON.stringify(r).slice(0, 300)), sleep(ms || 30000).then(() => 'no answer in ' + (ms || 30000) + ' ms')]);
  await send('Runtime.enable'); await send('Page.enable'); const t0 = Date.now(); await send('Page.navigate', { url: URL });
  let readyAt = null; for (let i = 0; i < 100; i++) { await sleep(3000); const a = await ev("(window.__poc && window.__poc.ready()) ? 'ready' : 'no'", 15000); if (a === 'ready') { readyAt = Date.now() - t0; break; } }
  if (readyAt === null) { console.log(JSON.stringify({ error: 'never ready', exceptions: exc.slice(0, 5) })); chrome.kill(); process.exit(2); }
  await sleep(6000);
  const state = () => ev("(function () { var p = window.__poc; return JSON.stringify({ brainPlacesOn: !!(document.getElementById('brainxyz') || {}).checked, visiblePoints: p.nodes(), springsDrawn: p.springs(), relLinesDrawn: p.relLines(), relKinds: Object.keys(p.kinds()).length, xyzEntries: p.xyzHeld(), memoryNodesDrawn: p.memNodes(), gatesLoaded: p.loaded(), historyHits: p.hist(), cur: p.cur(), stream: p.stream(), readout: (document.getElementById('readout') || {}).textContent }); })()", 30000).then(s => JSON.parse(s));
  const s0 = await state(); console.log(JSON.stringify({ at: 'ready', readyAtSeconds: Math.round(readyAt / 1000), url: URL, counts: s0 }));
  // the newest line chosen at its last hop, so the memory nodes of that line are asked for; then its first point clicked
  await ev("(function () { var p = window.__poc, c = p.cur(); if (c.root !== null) p.chooseRun(c.root, 9999); return 'chosen'; })()", 30000); await sleep(10000);
  const s1 = await state(); console.log(JSON.stringify({ at: 'the newest line chosen at its last hop', counts: s1 }));
  const clicked = await ev("(function () { var p = window.__poc, keys = Object.keys(p.positions()); var g = null; for (var i = 0; i < keys.length; i++) { if (/^\\d+$/.test(keys[i]) && +keys[i] > 100) { g = +keys[i]; break; } } if (g === null) return 'no point'; p.showNode(g); return 'clicked gate ' + g; })()", 30000);
  await sleep(8000); const s2 = await state(); console.log(JSON.stringify({ at: 'after a point was clicked', clicked, counts: s2 }));
  if (OUT) { const s = await send('Page.captureScreenshot', { format: 'png' }); if (s.result && s.result.data) { fs.writeFileSync(OUT, Buffer.from(s.result.data, 'base64')); console.log(JSON.stringify({ screenshot: OUT, bytes: fs.statSync(OUT).size })); } }
  console.log(JSON.stringify({ exceptions: exc.slice(0, 6) }));
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log(JSON.stringify({ error: e && e.message })); chrome.kill(); process.exit(1); });
