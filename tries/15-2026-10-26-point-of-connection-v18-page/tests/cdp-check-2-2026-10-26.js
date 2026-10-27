const { spawn } = require('child_process'); const fs = require('fs');
const S = process.env.S, BIN = process.env.BIN, PORT = 9334;
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=1600,1000', '--hide-scrollbars', '--remote-debugging-port=' + PORT, '--user-data-dir=' + S + '/chrome-cdp2', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let targets = null; for (let i = 0; i < 60 && !targets; i++) { await sleep(500); try { targets = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  const page = targets.find(t => t.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const waiting = {}; const errs = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && waiting[d.id]) { waiting[d.id](d); delete waiting[d.id]; } if (d.method === 'Runtime.exceptionThrown') errs.push(JSON.stringify(d.params.exceptionDetails).slice(0, 300)); };
  const send = (method, params) => new Promise(r => { const i = ++id; waiting[i] = r; ws.send(JSON.stringify({ id: i, method, params: params || {} })); });
  const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); return r.result.exceptionDetails ? 'EXC ' + JSON.stringify(r.result.exceptionDetails).slice(0, 200) : r.result.result.value; };
  const shot = async name => { const r = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(S + '/' + name + '.png', Buffer.from(r.result.data, 'base64')); };
  const until = async (expr, ms) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await ev(expr)) return true; await sleep(300); } return false; };
  await send('Runtime.enable'); await send('Page.enable'); await send('Page.navigate', { url: 'http://localhost:8018/' });
  console.log('ready:', await until('window.__poc && __poc.ready()', 60000)); await sleep(2000);
  await ev(`__poc.chooseRun(65, 3); document.querySelector('[data-panel="panel-run"]').click(); document.querySelector('[data-panel="panel-read"]').click(); 1`); await sleep(2000);
  await shot('t7-run');
  await ev(`document.getElementById('atlasbtn').click(); 1`); await sleep(3000);
  await ev(`document.getElementById('afind').value = 'dog'; document.getElementById('afind').dispatchEvent(new Event('input')); document.querySelector('#atable tr.arow').click(); 1`); await sleep(1500);
  console.log('atlas header cells:', await ev(`Array.from(document.querySelectorAll('#atable thead th')).map(t => t.innerText).join(' | ')`));
  console.log('atlas table width vs box:', await ev(`document.getElementById('atable').offsetWidth + ' / ' + document.querySelector('.atw').clientWidth`));
  await shot('t8-atlas');
  // the phone layout
  await send('Emulation.setDeviceMetricsOverride', { width: 420, height: 900, deviceScaleFactor: 1, mobile: true }); await sleep(1500);
  await ev(`document.getElementById('aclose').click(); 1`); await sleep(500);
  console.log('page scrollWidth vs 420:', await ev(`document.documentElement.scrollWidth`));
  await shot('t9-phone');
  console.log('exceptions:', errs.length ? errs.join('\n') : 'none');
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log('FAILED', e); chrome.kill(); process.exit(1); });
