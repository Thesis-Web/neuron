// cdp-light.js (2026-10-30): the light page driven in headless Chromium over the DevTools protocol (as tries/19's check did)
const { spawn } = require('child_process'); const fs = require('fs');
const S = process.env.S, BIN = process.env.BIN, PORT = 9335, URL = process.env.URL || 'http://10.31.1.106:8058/', W = 1800, H = 1000;
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=' + W + ',' + H, '--hide-scrollbars', '--remote-debugging-port=' + PORT, 'about:blank']);
let stderr = ''; chrome.stderr.on('data', d => { stderr += d; });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let targets = null;
  for (let i = 0; i < 60 && !targets; i++) { await sleep(500); try { targets = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  if (!targets) { console.log('no chrome', stderr.slice(-800)); process.exit(1); }
  const page = targets.find(t => t.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  let id = 0; const waiting = {}; const exc = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && waiting[d.id]) { waiting[d.id](d); delete waiting[d.id]; } if (d.method === 'Runtime.exceptionThrown') exc.push(JSON.stringify(d.params.exceptionDetails.exception && d.params.exceptionDetails.exception.description || d.params.exceptionDetails.text).slice(0, 300)); };
  const send = (method, params) => new Promise(r => { const i = ++id; waiting[i] = r; ws.send(JSON.stringify({ id: i, method, params: params || {} })); });
  const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.result.exceptionDetails) return 'EXC ' + JSON.stringify(r.result.exceptionDetails).slice(0, 200); return r.result.result.value; };
  const text = sel => ev(`(document.querySelector(${JSON.stringify(sel)}) || {innerText: 'MISSING'}).innerText.replace(/\\s+/g, ' ').slice(0, 400)`);
  const shot = async name => { const r = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(S + '/' + name + '.png', Buffer.from(r.result.data, 'base64')); };
  const until = async (expr, ms) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await ev(expr)) return Date.now() - t0; await sleep(200); } return false; };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  const t0 = Date.now(); await send('Page.navigate', { url: URL });
  console.log('ready after ms:', await until('window.__nk && __nk.ready()', 60000));
  await sleep(2500);
  console.log('hud:', await text('#hud')); console.log('busy:', await text('#busy'));
  console.log('run', await ev('__nk.run()'), 'hops', await ev('__nk.hops()'), 'points', await ev('__nk.points()'), 'springs', await ev('__nk.springs()'));
  console.log('readout:', await text('#readout')); console.log('runhead:', await text('#runhead')); console.log('cells:', (await text('#cells')).slice(0, 300)); console.log('back:', (await text('#back')).slice(0, 300));
  await shot('light-1-open');
  await ev(`document.getElementById('stepb').click(); document.getElementById('stepb').click(); 1`); await sleep(300); console.log('after two steps back:', await text('#readout'));
  // a define the sixth sent, loaded by click on the told list
  const told = await ev(`(function(){ var d = document.querySelectorAll('#told div'); for (var i = 0; i < d.length; i++) if (d[i].textContent.indexOf('define') >= 0) { d[i].click(); return d[i].textContent; } return null; })()`);
  console.log('clicked told line:', told); console.log('loaded after ms:', await until(`document.getElementById('busy').textContent.indexOf('runs,') > 0 && __nk.run() !== ${await ev('__nk.run()')}`, 60000));
  await sleep(2500); console.log('busy:', await text('#busy')); console.log('run', await ev('__nk.run()'), 'hops', await ev('__nk.hops()'), 'points', await ev('__nk.points()'), 'springs', await ev('__nk.springs()'));
  console.log('tree head:', (await text('#tree')).slice(0, 240)); await shot('light-2-define');
  await ev(`__nk.load(185); 1`); await until(`__nk.run() === 185`, 30000); await sleep(2000); console.log('run 185:', await text('#busy')); console.log('readout:', await text('#readout'));
  await ev(`document.querySelector('#stagewrap canvas') && 1`);
  await shot('light-3-who');
  // type through the page
  await ev(`__nk.send('print dna : who', 'main'); 1`); console.log('typed, loaded after ms:', await until(`document.getElementById('busy').textContent.indexOf('the line ran') === 0`, 60000)); await sleep(3000);
  console.log('busy:', await text('#busy')); console.log('cells after:', (await text('#cells')).slice(0, 400)); console.log('newest head:', (await text('#newest')).slice(0, 120)); await shot('light-4-typed');
  await ev(`document.getElementById('gap').value = 120; document.getElementById('gap').dispatchEvent(new Event('input')); 1`); await sleep(2500); await shot('light-5-gap120');
  console.log('exceptions:', exc.length ? exc : 'none'); chrome.kill(); process.exit(0);
})();
