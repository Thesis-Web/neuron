// cdp_onehop.js (2026-11-03, tries/43): what one press of the hop button does. Open the page headless, wait for __poc.ready(), uncheck
// "the brain's places" (the page's own springs), go to the start of the newest line (or ROOT), then press the hop button once, twice, three
// times, reading after each: the readout (runs alive this hop), the drawn points, the loaded gates, the springs. Nothing is typed.
// usage: LD_LIBRARY_PATH=<libs> URL=... [ROOT=<run id>] [PORT=9385] node cdp_onehop.js
const { spawn } = require('child_process');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +(process.env.PORT || 9385), URL = process.env.URL, ROOT = process.env.ROOT ? +process.env.ROOT : null;
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
  await ev("(function () { var c = document.getElementById('brainxyz'); if (c && c.checked) c.click(); return c ? c.checked : 'no switch'; })()");
  const state = () => ev("(function () { var p = window.__poc; return JSON.stringify({ readout: (document.getElementById('readout') || {}).textContent, nodes: p.nodes(), loaded: p.loaded(), springs: p.springs(), cur: p.cur(), hud: ((document.getElementById('hud') || {}).innerText || '').replace(/\\s+/g, ' ').slice(0, 120) }); })()", 30000).then(s => JSON.parse(s));
  const chosen = await ev("(function () { var p = window.__poc, c = p.cur(), r = " + (ROOT === null ? 'c.root' : String(ROOT)) + "; if (r === null) return 'no line'; p.chooseRun(r, 0); return 'choosing ' + r; })()", 30000);
  console.log(JSON.stringify({ chosen })); await sleep(12000);
  console.log(JSON.stringify({ at: 'start of the line', s: await state() }));
  const presses = +(process.env.PRESSES || 3);
  for (let i = 1; i <= presses; i++) { await ev("document.getElementById('fwd').click(); 'pressed'"); await sleep(5000); console.log(JSON.stringify({ at: 'after press ' + i, s: await state() })); }
  console.log(JSON.stringify({ exceptions: exc.slice(0, 5) }));
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log(JSON.stringify({ error: e && e.message })); chrome.kill(); process.exit(1); });
