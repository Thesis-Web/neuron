// cdp_light.js (2026-11-03, tries/41): open a page in the cached headless Chromium, wait for the page's own ready flag (window.__poc.ready()),
// read its counts through window.__poc, step one wave, screenshot. Prints JSON lines. Nothing written to a brain.
// usage: LD_LIBRARY_PATH=<libs> URL=http://127.0.0.1:8056/ OUT=/path/shot.png node cdp_light.js
const { spawn } = require('child_process'); const fs = require('fs');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +(process.env.PORT || 9381), URL = process.env.URL, OUT = process.env.OUT;
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
  for (let i = 0; i < 120; i++) { await sleep(3000); const a = await ev("(window.__poc && window.__poc.ready()) ? 'ready' : ('not yet: ' + ((document.getElementById('busy') || {}).textContent || document.readyState).slice(0, 90))", 15000); if (i % 5 === 0 || a === 'ready') console.log(JSON.stringify({ t: Math.round((Date.now() - t0) / 1000), state: a })); if (a === 'ready') { readyAt = Date.now() - t0; break; } }
  if (readyAt === null) { console.log(JSON.stringify({ error: 'never ready', exceptions: exc.slice(0, 5) })); ws.close(); chrome.kill(); process.exit(2); }
  await sleep(6000);
  const counts = () => ev("(function () { var p = window.__poc; return JSON.stringify({ light: p.light, counts: p.counts(), gates: p.gates(), loaded: p.loaded ? p.loaded() : null, dna: p.dna(), springs: p.springs(), nodes: p.nodes(), hist: p.hist ? p.hist() : null, waves: p.waves ? p.waves() : null, cur: p.cur(), kinds: p.kinds(), busy: (document.getElementById('busy') || {}).textContent, readout: (document.getElementById('readout') || {}).textContent, hud: ((document.getElementById('hud') || {}).innerText || '').replace(/\\s+/g, ' ').slice(0, 160) }); })()", 60000);
  console.log(JSON.stringify({ at: 'ready', readyAt: Math.round(readyAt / 1000), counts: await counts() }));
  // to the start of the newest line, then one press of the hop button, twice
  // to the start of the chosen line (the newest typed line, or the one named in ROOT), then the hop button three times: each press is one wave
  const root = process.env.ROOT ? +process.env.ROOT : null;
  const chosen = await ev("(function () { var p = window.__poc, c = p.cur(), r = " + (root === null ? 'c.root' : String(root)) + "; if (r === null) return 'no line'; p.chooseRun(r, 0); return 'choosing ' + r; })()", 30000);
  console.log(JSON.stringify({ chosen })); await sleep(25000);   // chooseRun reads the line's gates by key first; on a busy hub door that takes a while
  const steps = await ev("(function () { var p = window.__poc, out = [(document.getElementById('readout') || {}).textContent + ' | tk ' + p.cur().tk + ' | ' + ((document.getElementById('hud') || {}).innerText || '').replace(/\\s+/g, ' ').slice(0, 110)]; var fwd = document.getElementById('fwd'); for (var i = 0; i < 3; i++) { fwd.click(); out.push((document.getElementById('readout') || {}).textContent + ' | tk ' + p.cur().tk + ' | ' + ((document.getElementById('hud') || {}).innerText || '').replace(/\\s+/g, ' ').slice(0, 110)); } return JSON.stringify(out); })()", 60000);
  console.log(JSON.stringify({ steps }));
  await sleep(3000);
  if (OUT) { const s = await send('Page.captureScreenshot', { format: 'png' }); if (s.result && s.result.data) { fs.writeFileSync(OUT, Buffer.from(s.result.data, 'base64')); console.log(JSON.stringify({ screenshot: OUT, bytes: fs.statSync(OUT).size })); } }
  console.log(JSON.stringify({ exceptions: exc.slice(0, 8) }));
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log(JSON.stringify({ error: e && e.message })); chrome.kill(); process.exit(1); });
