const { spawn } = require('child_process'); const fs = require('fs');
const S = process.env.S, BIN = process.env.BIN, PORT = 9336, W = +(process.env.W || 3787), H = +(process.env.H || 1918);
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=' + W + ',' + H, '--hide-scrollbars', '--remote-debugging-port=' + PORT, '--user-data-dir=' + S + '/chrome-v6c', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let targets = null; for (let i = 0; i < 60 && !targets; i++) { await sleep(500); try { targets = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  const page = targets.find(t => t.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const waiting = {}; const errs = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && waiting[d.id]) { waiting[d.id](d); delete waiting[d.id]; } if (d.method === 'Runtime.exceptionThrown') errs.push(JSON.stringify(d.params.exceptionDetails).slice(0, 400)); };
  const send = (method, params) => new Promise(r => { const i = ++id; waiting[i] = r; ws.send(JSON.stringify({ id: i, method, params: params || {} })); });
  const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); return r.result.exceptionDetails ? 'EXC ' + JSON.stringify(r.result.exceptionDetails).slice(0, 300) : r.result.result.value; };
  const text = sel => ev(`(document.querySelector(${JSON.stringify(sel)}) || {innerText: 'MISSING'}).innerText.replace(/\\s+/g, ' ').slice(0, 500)`);
  const shot = async name => { const r = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(S + '/' + name + '.png', Buffer.from(r.result.data, 'base64')); };
  const until = async (expr, ms) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await ev(expr)) return true; await sleep(300); } return false; };
  await send('Runtime.enable'); await send('Page.enable'); await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: 'http://localhost:8056/' }); console.log('ready', await until('window.__poc && __poc.ready()', 90000)); await sleep(3000);
  console.log('cur now:', JSON.stringify(await ev('__poc.cur()')), 'nodes', await ev('__poc.nodes()'), 'springs', await ev('__poc.springs()'));
  await shot('h1-now');
  await ev(`document.querySelector('[data-panel="panel-step"]').click(); document.getElementById('tostart').click(); 1`); await sleep(2500);
  console.log('at start:', JSON.stringify(await ev('__poc.cur()')), 'nodes', await ev('__poc.nodes()'), 'springs', await ev('__poc.springs()'), '|', await text('#histout'));
  await shot('h2-start');
  await ev(`document.getElementById('speed').value = '120'; document.getElementById('play').click(); 1`); await sleep(6000);
  console.log('after 6 s play:', JSON.stringify(await ev('__poc.cur()')), 'nodes', await ev('__poc.nodes()'), 'springs', await ev('__poc.springs()'), '|', await text('#histout'));
  await shot('h3-play-6s');
  await sleep(12000);
  console.log('after 18 s play:', JSON.stringify(await ev('__poc.cur()')), 'nodes', await ev('__poc.nodes()'), 'springs', await ev('__poc.springs()'), '|', await text('#now'));
  await shot('h4-play-18s');
  await ev(`document.getElementById('play').click(); 1`);
  // jump the history slider to the middle
  await ev(`var s = document.getElementById('hist'); s.value = Math.floor(s.max / 2); s.dispatchEvent(new Event('input')); 1`); await sleep(2500);
  console.log('mid:', JSON.stringify(await ev('__poc.cur()')), 'nodes', await ev('__poc.nodes()'), '|', await text('#readout'), '|', (await text('#log')).slice(0, 200));
  await shot('h5-mid');
  await ev(`document.getElementById('tonow').click(); 1`); await sleep(2500);
  console.log('now again:', JSON.stringify(await ev('__poc.cur()')), 'nodes', await ev('__poc.nodes()'));
  // the run tab at now and the hop slider
  await ev(`document.querySelector('[data-panel="panel-run"]').click(); 1`); await sleep(1200);
  console.log('runhead:', (await text('#runhead')).slice(0, 200)); console.log('builds:', (await text('#builds')).slice(0, 200));
  await ev(`document.querySelector('[data-panel="panel-step"]').click(); var t = document.getElementById('time'); t.value = 3; t.dispatchEvent(new Event('input')); 1`); await sleep(800);
  console.log('hop slider 3:', await text('#readout'), '|', (await text('#now')).slice(0, 160));
  console.log('errors:', errs.length ? errs.join('\n') : 'none');
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log('driver error', e); chrome.kill(); process.exit(1); });
