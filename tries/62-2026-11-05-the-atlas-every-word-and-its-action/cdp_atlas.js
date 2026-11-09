// cdp_atlas.js (2026-11-05, tries/62): open the full page in the cached headless Chromium, wait for window.__poc.ready(), press the atlas
// button, wait until the atlas has read, then read what it shows: the summary, the count shown, the header, rows found by a few symbols,
// screenshot. Reads only; nothing typed into a brain. usage: URL=http://host:port/full OUT=/path/shot.png FIND=print,black node cdp_atlas.js
const { spawn } = require('child_process'); const fs = require('fs');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +(process.env.PORT || 9383), URL = process.env.URL, OUT = process.env.OUT;
const FIND = (process.env.FIND || '').split(',').filter(Boolean);
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=1800,1000', '--remote-debugging-port=' + PORT, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let t = null; for (let i = 0; i < 60 && !t; i++) { await sleep(500); try { t = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  if (!t) { console.log(JSON.stringify({ error: 'no chrome' })); process.exit(1); }
  const page = t.find(x => x.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const wait = {}; const exc = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && wait[d.id]) { wait[d.id](d); delete wait[d.id]; } if (d.method === 'Runtime.exceptionThrown') exc.push(String(d.params.exceptionDetails.exception && d.params.exceptionDetails.exception.description || d.params.exceptionDetails.text).slice(0, 300)); };
  const send = (m, p) => new Promise(r => { const i = ++id; wait[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
  const ev = (e, ms) => Promise.race([send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true }).then(r => r.result && r.result.result ? r.result.result.value : JSON.stringify(r).slice(0, 300)), sleep(ms || 30000).then(() => 'no answer in ' + (ms || 30000) + ' ms')]);
  await send('Runtime.enable'); await send('Page.enable'); const t0 = Date.now(); await send('Page.navigate', { url: URL });
  let ok = false; for (let i = 0; i < 200; i++) { await sleep(3000); const a = await ev("(window.__poc && window.__poc.ready()) ? 'ready' : 'not yet'", 15000); if (a === 'ready') { ok = true; break; } }
  if (!ok) { console.log(JSON.stringify({ error: 'never ready', exceptions: exc.slice(0, 5) })); ws.close(); chrome.kill(); process.exit(2); }
  console.log(JSON.stringify({ ready_s: Math.round((Date.now() - t0) / 1000) }));
  const t1 = Date.now(); await ev("document.getElementById('atlasbtn').click(), 'clicked'");
  let sum = ''; for (let i = 0; i < 200; i++) { await sleep(2000); sum = await ev("(document.getElementById('asum') || {}).innerText || ''"); if (sum && !/reading|walking/i.test(sum)) break; }
  console.log(JSON.stringify({ atlas_s: Math.round((Date.now() - t1) / 1000), summary: sum.replace(/\s+/g, ' ').slice(0, 900), shown: await ev("(document.getElementById('ashown') || {}).textContent"), header: await ev("[].map.call(document.querySelectorAll('#atable th'), function (x) { return x.textContent; }).join(' | ')"), firstRows: await ev("[].slice.call(document.querySelectorAll('#atable tr.arow'), 0, 3).map(function (tr) { return tr.innerText.replace(/\\s+/g, ' ').slice(0, 300); })") }));
  for (const f of FIND) {
    const r = await ev("(function () { var i = document.getElementById('afind'); i.value = " + JSON.stringify(f) + "; i.dispatchEvent(new Event('input')); return new Promise(function (ok) { setTimeout(function () { ok({ shown: document.getElementById('ashown').textContent, rows: [].slice.call(document.querySelectorAll('#atable tr.arow'), 0, 4).map(function (tr) { return [].map.call(tr.cells, function (c) { return c.innerText.replace(/\\s+/g, ' '); }).join(' ‖ ').slice(0, 700); }) }); }, 1500); }); })()", 30000);
    console.log(JSON.stringify({ find: f, result: r }));
  }
  for (const v of (process.env.SHOW || '').split(',').filter(Boolean)) {
    const r = await ev("(function () { var i = document.getElementById('afind'); i.value = ''; i.dispatchEvent(new Event('input')); var s = document.getElementById('ashow'); s.value = " + JSON.stringify(v) + "; s.dispatchEvent(new Event('change')); return new Promise(function (ok) { setTimeout(function () { ok({ option: s.options[s.selectedIndex].text, shown: document.getElementById('ashown').textContent, groups: [].map.call(document.querySelectorAll('#atable tr.agrp'), function (x) { return x.innerText.replace(/\\s+/g, ' ').slice(0, 160); }), rows: [].slice.call(document.querySelectorAll('#atable tr.arow'), 0, 60).map(function (tr) { return tr.cells[0].innerText + ' [' + ((tr.querySelector('.jt') || {}).textContent || '') + ']'; }).join(', ') }); }, 1500); }); })()", 30000);
    console.log(JSON.stringify({ show: v, result: r }));
  }
  if (process.env.DETAIL) {
    await ev("(function () { var i = document.getElementById('afind'); i.value = " + JSON.stringify(process.env.DETAIL) + "; i.dispatchEvent(new Event('input')); document.querySelector('#atable tr.arow').click(); return 1; })()");
    await sleep(4000);
    console.log(JSON.stringify({ detail: process.env.DETAIL, text: await ev("((document.querySelector('#atable tr.det') || {}).innerText || 'no detail row').slice(0, 2400)") }));
  }
  if (OUT) { await ev("(function () { var i = document.getElementById('afind'); i.value = " + JSON.stringify(process.env.SHOT || '') + "; i.dispatchEvent(new Event('input')); return 1; })()"); await sleep(1500); const s = await send('Page.captureScreenshot', { format: 'png' }); if (s.result && s.result.data) { fs.writeFileSync(OUT, Buffer.from(s.result.data, 'base64')); console.log(JSON.stringify({ screenshot: OUT, bytes: fs.statSync(OUT).size })); } }
  console.log(JSON.stringify({ exceptions: exc.slice(0, 8) }));
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log(JSON.stringify({ error: e && e.message })); chrome.kill(); process.exit(1); });
