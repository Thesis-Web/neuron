// tries/62: inside the headless page, time the walk's 18 fetches alone, then the atlas walk itself with the page's frame count, to find where its time goes
const { spawn } = require('child_process');
const BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = 9385, URL = process.env.URL;
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=1800,1000', '--remote-debugging-port=' + PORT, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let t = null; for (let i = 0; i < 60 && !t; i++) { await sleep(500); try { t = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  const page = t.find(x => x.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const wait = {}; ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && wait[d.id]) { wait[d.id](d); delete wait[d.id]; } };
  const send = (m, p) => new Promise(r => { const i = ++id; wait[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
  const ev = (e) => send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true }).then(r => r.result && r.result.result ? r.result.result.value : JSON.stringify(r).slice(0, 300));
  await send('Runtime.enable'); await send('Page.navigate', { url: URL });
  for (let i = 0; i < 100; i++) { await sleep(2000); if (await ev("!!(window.__poc && window.__poc.ready())")) break; }
  await sleep(4000);
  const fetches = await ev(`(async function () {
    var info = await (await fetch('/api/info')).json(), top = info.stats.main.gates, sql = 'WITH RECURSIVE g(x) AS (SELECT ? UNION ALL SELECT x + 1 FROM g WHERE x < ?) SELECT g.x, l.symbol, n.nodes, n.shards, n.memories, round(p.x, 1), round(p.y, 1), round(p.z, 1) FROM g JOIN main.neuron n ON n.gate = g.x JOIN main.label l ON l.gate = g.x LEFT JOIN main.xyz p ON p.gate = g.x WHERE n.nodes > 0 OR n.shards > 0';
    var t0 = performance.now(), per = [], rows = 0;
    for (var a = 1; a <= top; a += 100000) { var t = performance.now(); var j = await (await fetch('/api/q', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ sql: sql, params: [a, Math.min(top, a + 99999)] }) })).json(); rows += (j.rows || []).length; per.push(Math.round(performance.now() - t)); }
    return JSON.stringify({ fetches_ms: Math.round(performance.now() - t0), rows: rows, per_chunk_ms: per });
  })()`);
  console.log('the 18 fetches alone, in the page:', fetches);
  let frames = await ev("new Promise(function (ok) { var n = 0, t0 = performance.now(); function f() { n++; if (performance.now() - t0 < 2000) requestAnimationFrame(f); else ok(n); } requestAnimationFrame(f); })");
  console.log('frames the page draws in 2 s (its stage loop, swiftshader):', frames);
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log('error', e && e.message); chrome.kill(); process.exit(1); });
