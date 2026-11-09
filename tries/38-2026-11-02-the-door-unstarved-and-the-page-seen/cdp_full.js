// cdp_full.js (2026-11-02, tries/38): open hp's full page in the cached headless Chromium, wait until the page says ready, then read the
// page's own state: the brain's-places switch, the points drawn, the springs, the XYZ entries, the history; choose the newest run with hops
// so the memory nodes of the chosen line are asked for, count them; screenshot. Prints JSON lines. No brain is written.
// readiness (third run): the HUD at 'hit N of N' with points drawn (the second run never met ready or TK >= HIST.length - 1 in 900 s). (second run): the page's ready flag, or the history replayed to its last hit with points drawn (the first run saw the HUD at 'hit 88602 of 88602' for 5 min with ready still false)
// usage: URL=http://10.31.1.106:8058/full OUT=/path/shot.png node cdp_full.js
const { spawn } = require('child_process'); const fs = require('fs');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +(process.env.PORT || 9377), URL = process.env.URL, OUT = process.env.OUT;
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=1800,1000', '--remote-debugging-port=' + PORT, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let t = null; for (let i = 0; i < 60 && !t; i++) { await sleep(500); try { t = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  if (!t) { console.log(JSON.stringify({ error: 'no chrome' })); process.exit(1); }
  const page = t.find(x => x.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const wait = {}; const exc = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && wait[d.id]) { wait[d.id](d); delete wait[d.id]; } if (d.method === 'Runtime.exceptionThrown') exc.push(String(d.params.exceptionDetails.exception && d.params.exceptionDetails.exception.description || d.params.exceptionDetails.text).slice(0, 160)); };
  const send = (m, p) => new Promise(r => { const i = ++id; wait[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
  const ev = (e, ms) => Promise.race([send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true }).then(r => r.result && r.result.result ? r.result.result.value : JSON.stringify(r).slice(0, 300)), sleep(ms || 30000).then(() => 'no answer in ' + (ms || 30000) + ' ms')]);
  await send('Runtime.enable'); await send('Page.enable'); const t0 = Date.now(); await send('Page.navigate', { url: URL });
  let readyAt = null;
  for (let i = 0; i < 150; i++) { await sleep(5000); const a = await ev("((function () { var h = document.getElementById('hud'); var m = h && /hit (\\d+) of (\\d+)/.exec(h.innerText); return !!(m && m[1] === m[2]); })()) ? 'ready' : ('not yet: ' + (document.getElementById('hud') ? document.getElementById('hud').innerText.slice(0, 80) : document.readyState))", 20000); console.log(JSON.stringify({ t: Math.round((Date.now() - t0) / 1000), state: a })); if (a === 'ready') { readyAt = Date.now() - t0; break; } }
  if (readyAt === null) { console.log(JSON.stringify({ error: 'the page never became ready', exceptions: exc.slice(0, 5) })); ws.close(); chrome.kill(); process.exit(2); }
  await sleep(8000);   // the first frames, the fit
  // fourth run: the page's variables are function-scoped (not reachable from the console), so only the DOM is read: the HUD, the kinds rail, the panels
  const dom = () => ev(`(function () { var hud = document.getElementById('hud'); var boxes = Array.prototype.slice.call(document.querySelectorAll('#reltypes input[type=checkbox]'));
    var sw = {}; Array.prototype.slice.call(document.querySelectorAll('input[type=checkbox][id]')).forEach(function (c) { sw[c.id] = c.checked; });
    var panels = {}; Array.prototype.slice.call(document.querySelectorAll('aside .inner, aside section, aside div[id]')).slice(0, 12).forEach(function (p) { if (p.id) panels[p.id] = (p.innerText || '').replace(/\s+/g, ' ').slice(0, 220); });
    return JSON.stringify({ hud: hud ? hud.innerText.replace(/\s+/g, ' ').slice(0, 200) : null, kinds: boxes.length, kindsOn: boxes.filter(function (b) { return b.checked; }).length, switches: sw, canvas: (function () { var c = document.querySelector('canvas'); return c ? [c.width, c.height] : null; })(), panels: panels }); })()`, 60000);
  console.log(JSON.stringify({ at: 'history at its last hit', readyAt: Math.round(readyAt / 1000), dom: await dom() }));
  if (OUT) { const s = await send('Page.captureScreenshot', { format: 'png' }); if (s.result && s.result.data) { fs.writeFileSync(OUT, Buffer.from(s.result.data, 'base64')); console.log(JSON.stringify({ screenshot: OUT, bytes: fs.statSync(OUT).size })); } }
  console.log(JSON.stringify({ exceptions: exc.slice(0, 6) }));
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log(JSON.stringify({ error: e && e.message })); chrome.kill(); process.exit(1); });
