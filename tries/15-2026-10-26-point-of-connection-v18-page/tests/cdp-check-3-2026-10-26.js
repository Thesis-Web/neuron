const { spawn } = require('child_process'); const fs = require('fs');
const S = process.env.S, BIN = process.env.BIN, PORT = 9337;
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=3787,1918', '--hide-scrollbars', '--remote-debugging-port=' + PORT, '--user-data-dir=' + S + '/prof5', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let targets = null; for (let i = 0; i < 60 && !targets; i++) { await sleep(500); try { targets = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  const page = targets.find(t => t.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const waiting = {}; const errs = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && waiting[d.id]) { waiting[d.id](d); delete waiting[d.id]; } if (d.method === 'Runtime.exceptionThrown') errs.push(JSON.stringify(d.params.exceptionDetails).slice(0, 300)); };
  const send = (method, params) => new Promise(r => { const i = ++id; waiting[i] = r; ws.send(JSON.stringify({ id: i, method, params: params || {} })); });
  const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); return r.result.exceptionDetails ? 'EXC ' + JSON.stringify(r.result.exceptionDetails).slice(0, 300) : r.result.result.value; };
  const shot = async name => { const r = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(S + '/' + name + '.png', Buffer.from(r.result.data, 'base64')); };
  const until = async (expr, ms) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await ev(expr)) return true; await sleep(300); } return false; };
  const stats = async (tag) => {
    const o = JSON.parse(await ev(`JSON.stringify(__poc.positions())`)); const ks = Object.keys(o);
    const rs = ks.map(k => Math.hypot(...o[k])).sort((a, b) => a - b); const q = p => rs[Math.floor(rs.length * p)].toFixed(1);
    console.log(tag, 'points', ks.length, '| r50/r95/max', q(.5), q(.95), rs[rs.length - 1].toFixed(1), '| springs', await ev(`__poc.springs()`), '| space switch', await ev(`document.getElementById('spacelines').checked`));
  };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 3787, height: 1918, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: 'http://localhost:8018/' });
  console.log('ready:', await until('window.__poc && __poc.ready()', 60000));
  await sleep(3000); await stats('3787 wide, 3 s:'); await shot('w1-3787-3s');
  await sleep(9000); await stats('3787 wide, 12 s:'); await shot('w2-3787-12s');
  await send('Emulation.setDeviceMetricsOverride', { width: 1900, height: 1000, deviceScaleFactor: 1, mobile: false }); await sleep(6000);
  await stats('1900 wide:'); await shot('w3-1900');
  console.log('exceptions:', errs.length ? errs.join('\n') : 'none');
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log('FAILED', e); chrome.kill(); process.exit(1); });
