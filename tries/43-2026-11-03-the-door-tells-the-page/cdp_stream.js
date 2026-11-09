// cdp_stream.js (2026-11-03, tries/43): open a page in the cached headless Chromium, wait for window.__poc.ready(), read the stream's state
// and the page's own request count, hold still for SILENCE ms and read the count again (the check: the page asks nothing on a clock), then,
// when LINE is set, type that line through the door and watch the stream carry its run's end and the page redraw. Prints JSON lines.
// usage: LD_LIBRARY_PATH=<libs> URL=http://host:port/ [LINE='cold water freezes'] [SILENCE=30000] [OUT=/path/shot.png] [PORT=9381] node cdp_stream.js
const { spawn } = require('child_process'); const fs = require('fs');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +(process.env.PORT || 9381), URL = process.env.URL, OUT = process.env.OUT, LINE = process.env.LINE || '', SILENCE = +(process.env.SILENCE || 30000);
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
  await sleep(4000);
  const state = () => ev("(function () { var p = window.__poc; return JSON.stringify({ stream: p.stream(), told: p.told(), counts: p.streamCounts(), fetches: p.fetches(), loaded: p.loaded(), nodes: p.nodes(), hist: p.hist(), cur: p.cur(), readout: (document.getElementById('readout') || {}).textContent, streamLine: (document.getElementById('stream') || {}).textContent, hud: ((document.getElementById('hud') || {}).innerText || '').replace(/\\s+/g, ' ').slice(0, 140) }); })()", 30000);
  const s0 = JSON.parse(await state()); console.log(JSON.stringify({ at: 'ready', readyAt: Math.round(readyAt / 1000), s: s0 }));
  await sleep(SILENCE);
  const s1 = JSON.parse(await state()); console.log(JSON.stringify({ at: 'after ' + Math.round(SILENCE / 1000) + ' s of silence', requestsMade: s1.fetches - s0.fetches, s: s1 }));
  if (LINE) {
    const t1 = Date.now();
    const r = await fetch(URL.replace(/\/[^\/]*$/, '') + '/api/type', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ line: LINE }) }).then(x => x.json()).catch(e => ({ error: String(e) }));
    console.log(JSON.stringify({ typed: LINE, doorAnsweredIn: Math.round((Date.now() - t1) / 1000) + ' s', run: r.result && r.result.run, error: r.error }));
    // watch the stream carry it: the counts the moment the page hears, then after it redrew
    let heardAt = null; for (let i = 0; i < 40; i++) { await sleep(250); const s = JSON.parse(await state()); if (s.counts.ends > s1.counts.ends || s.counts.moves > s1.counts.moves) { heardAt = Date.now() - t1; console.log(JSON.stringify({ at: 'the stream told the page', afterMs: heardAt, counts: s.counts, told: s.told })); break; } }
    if (heardAt === null) console.log(JSON.stringify({ at: 'the stream told nothing in 10 s' }));
    await sleep(8000);
    const s2 = JSON.parse(await state()); console.log(JSON.stringify({ at: 'after the line', requestsMade: s2.fetches - s1.fetches, s: s2 }));
  }
  if (OUT) { const s = await send('Page.captureScreenshot', { format: 'png' }); if (s.result && s.result.data) { fs.writeFileSync(OUT, Buffer.from(s.result.data, 'base64')); console.log(JSON.stringify({ screenshot: OUT, bytes: fs.statSync(OUT).size })); } }
  console.log(JSON.stringify({ exceptions: exc.slice(0, 8) }));
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log(JSON.stringify({ error: e && e.message })); chrome.kill(); process.exit(1); });
