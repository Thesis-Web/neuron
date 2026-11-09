// cdp_colors.js (2026-11-03, tries/44): open a page headless, wait for __poc.ready(), uncheck "the brain's places" (the page's own springs),
// choose ROOT (or the newest line) at hop 0, set "runs drawn" to every run of this line, press the hop button PRESSES times, then read the
// kinds of action on every path drawn (__poc.paths()), the counts for the run shown (__poc.acts()), the legend text and the HUD line.
// Nothing is typed. usage: LD_LIBRARY_PATH=<libs> URL=... [ROOT=<run>] [PRESSES=8] [OUT=shot.png] [PORT=9388] node cdp_colors.js
const { spawn } = require('child_process'); const fs = require('fs');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +(process.env.PORT || 9388), URL = process.env.URL, OUT = process.env.OUT, ROOT = process.env.ROOT ? +process.env.ROOT : null, PRESSES = +(process.env.PRESSES || 8);
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
  await send('Runtime.enable'); await send('Page.enable'); await send('Page.navigate', { url: URL });
  let ok = false; for (let i = 0; i < 100; i++) { await sleep(3000); const a = await ev("(window.__poc && window.__poc.ready()) ? 'ready' : 'no'", 15000); if (a === 'ready') { ok = true; break; } }
  if (!ok) { console.log(JSON.stringify({ error: 'never ready' })); chrome.kill(); process.exit(2); }
  await sleep(4000);
  await ev("(function () { var c = document.getElementById('brainxyz'); if (c && c.checked) c.click(); var s = document.getElementById('runmode'); if (s) { s.value = 'line'; s.dispatchEvent(new Event('change')); } return 'set'; })()");
  const chosen = await ev("(function () { var p = window.__poc, c = p.cur(), r = " + (ROOT === null ? 'c.root' : String(ROOT)) + "; if (r === null) return 'no line'; p.chooseRun(r, 0); return 'choosing ' + r; })()", 30000);
  console.log(JSON.stringify({ chosen })); await sleep(12000);
  const state = () => ev("(function () { var p = window.__poc; return JSON.stringify({ readout: (document.getElementById('readout') || {}).textContent, acts: p.acts(), legend: p.legend(), paths: p.paths(), hud: ((document.getElementById('hud') || {}).innerText || '').replace(/\\s+/g, ' ').slice(0, 220) }); })()", 30000).then(s => JSON.parse(s));
  console.log(JSON.stringify({ at: 'start', s: await state() }));
  for (let i = 1; i <= PRESSES; i++) { await ev("document.getElementById('fwd').click(); 'pressed'"); await sleep(2500); if (i === PRESSES || i % 4 === 0) console.log(JSON.stringify({ at: 'after press ' + i, s: await state() })); }
  await sleep(4000);
  if (OUT) { const s = await send('Page.captureScreenshot', { format: 'png' }); if (s.result && s.result.data) { fs.writeFileSync(OUT, Buffer.from(s.result.data, 'base64')); console.log(JSON.stringify({ screenshot: OUT, bytes: fs.statSync(OUT).size })); } }
  console.log(JSON.stringify({ exceptions: exc.slice(0, 5) }));
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log(JSON.stringify({ error: e && e.message })); chrome.kill(); process.exit(1); });
