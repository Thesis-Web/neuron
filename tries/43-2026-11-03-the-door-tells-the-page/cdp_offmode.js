// cdp_offmode.js (2026-11-03, tries/43): open a page headless, wait for __poc.ready(), read positions with "the brain's places" ON, then
// uncheck the switch (the page's own springs, v6's physics) and read how many drawn points moved in 8 s, then press the hop button three
// times and read again. Nothing is typed. usage: LD_LIBRARY_PATH=<libs> URL=... [PORT=9383] node cdp_offmode.js
const { spawn } = require('child_process');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +(process.env.PORT || 9383), URL = process.env.URL;
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
  await sleep(5000);
  const pos = () => ev("JSON.stringify(window.__poc.positions())", 30000).then(s => JSON.parse(s));
  const diff = (a, b) => { let n = 0, max = 0, keys = Object.keys(b); keys.forEach(k => { if (!a[k]) return; const d = Math.hypot(a[k][0] - b[k][0], a[k][1] - b[k][1], a[k][2] - b[k][2]); if (d > 0.5) n++; if (d > max) max = d; }); return { moved: n, of: keys.length, largest: Math.round(max) }; };
  const p0 = await pos(); await sleep(8000); const p1 = await pos();
  console.log(JSON.stringify({ mode: "the brain's places ON", in8s: diff(p0, p1), springs: await ev("window.__poc.springs()"), kinds: await ev("JSON.stringify(window.__poc.kinds())") }));
  await ev("(function () { var c = document.getElementById('brainxyz'); if (c && c.checked) c.click(); return c ? c.checked : 'no switch'; })()");
  await sleep(1000); const p2 = await pos(); await sleep(8000); const p3 = await pos();
  console.log(JSON.stringify({ mode: "the brain's places OFF (the page's own springs, v6)", firstSecond: diff(p1, p2), in8s: diff(p2, p3), springs: await ev("window.__poc.springs()") }));
  await ev("(function () { var f = document.getElementById('fwd'); for (var i = 0; i < 3; i++) f.click(); return (document.getElementById('readout') || {}).textContent; })()").then(r => console.log(JSON.stringify({ hops: r })));
  await sleep(6000); const p4 = await pos();
  console.log(JSON.stringify({ mode: 'OFF, after three hops', in6s: diff(p3, p4), readout: await ev("(document.getElementById('readout') || {}).textContent") }));
  console.log(JSON.stringify({ exceptions: exc.slice(0, 5) }));
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log(JSON.stringify({ error: e && e.message })); chrome.kill(); process.exit(1); });
