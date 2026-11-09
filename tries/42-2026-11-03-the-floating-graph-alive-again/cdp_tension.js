// cdp_tension.js (2026-11-03, tries/42): open a page headless, wait for window.__poc.ready(), read the drawn points' positions twice ten
// seconds apart (do they move?), click the `alike` kind off, read again (do they re-settle?), screenshot. Prints JSON lines. No brain written.
// usage: LD_LIBRARY_PATH=<libs> URL=http://10.31.1.106:8058/full OUT=/path/shot.png node cdp_tension.js
const { spawn } = require('child_process'); const fs = require('fs');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +(process.env.PORT || 9391), URL = process.env.URL, OUT = process.env.OUT;
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
  let readyAt = null;
  for (let i = 0; i < 120; i++) { await sleep(3000); const a = await ev("(window.__poc && window.__poc.ready()) ? 'ready' : 'not yet'", 15000); if (a === 'ready') { readyAt = Date.now() - t0; break; } }
  if (readyAt === null) { console.log(JSON.stringify({ error: 'never ready', exceptions: exc.slice(0, 5) })); ws.close(); chrome.kill(); process.exit(2); }
  await sleep(6000);
  const snap = () => ev("JSON.stringify({ n: Object.keys(window.__poc.positions()).length, springs: window.__poc.springs(), brain: document.getElementById('brainxyz').checked, pos: window.__poc.positions() })", 60000).then(s => JSON.parse(s));
  const diff = (a, b) => { let moved = 0, total = 0, maxd = 0; Object.keys(a.pos).forEach(k => { if (!b.pos[k]) return; total++; const d = Math.hypot(a.pos[k][0] - b.pos[k][0], a.pos[k][1] - b.pos[k][1], a.pos[k][2] - b.pos[k][2]); if (d > 0.05) moved++; if (d > maxd) maxd = d; }); return { moved, total, maxd: Math.round(maxd * 100) / 100 }; };
  const s1 = await snap(); await sleep(10000); const s2 = await snap();
  console.log(JSON.stringify({ readyAt: Math.round(readyAt / 1000), brainPlaces: s1.brain, points: s1.n, springs: s1.springs, tenSeconds: diff(s1, s2) }));
  const clicked = await ev("(function () { var c = document.querySelector('#reltypes input[data-rel=\"alike\"]'); if (!c) return 'no alike checkbox'; c.click(); return 'alike ' + (c.checked ? 'on' : 'off'); })()", 30000);
  await sleep(10000); const s3 = await snap();
  console.log(JSON.stringify({ clicked, springsAfter: s3.springs, afterToggle: diff(s2, s3) }));
  if (OUT) { const s = await send('Page.captureScreenshot', { format: 'png' }); if (s.result && s.result.data) { fs.writeFileSync(OUT, Buffer.from(s.result.data, 'base64')); console.log(JSON.stringify({ screenshot: OUT, bytes: fs.statSync(OUT).size })); } }
  console.log(JSON.stringify({ exceptions: exc.slice(0, 6) }));
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log(JSON.stringify({ error: e && e.message })); chrome.kill(); process.exit(1); });
