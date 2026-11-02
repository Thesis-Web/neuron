// cdp_where.js: open the page, and at given seconds pause the JS thread (Debugger.pause works while it is busy) and print where it is
const { spawn } = require('child_process');
const S = process.env.SP, BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +process.env.PORT || 9370, URL = process.env.URL;
const AT = (process.env.AT || '90,180,300').split(',').map(Number);
const chrome = spawn(BIN, ['--headless=new','--no-sandbox','--disable-gpu','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-first-run','--window-size=1800,1000','--remote-debugging-port='+PORT,'--user-data-dir='+S+'/cp'+Date.now(),'about:blank']);
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let t = null; for (let i = 0; i < 60 && !t; i++) { await sleep(500); try { t = await (await fetch('http://127.0.0.1:'+PORT+'/json')).json(); } catch (e) {} }
  if(!t){console.log('no chrome');process.exit(1)} const page = t.find(x => x.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const wait = {}; let paused = null;
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && wait[d.id]) { wait[d.id](d); delete wait[d.id]; } if (d.method === 'Debugger.paused') paused = d.params; };
  const send = (m, p) => new Promise(r => { const i = ++id; wait[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
  await send('Debugger.enable'); await send('Page.enable'); const t0 = Date.now(); await send('Page.navigate', { url: URL });
  for (const at of AT) {
    while ((Date.now() - t0) / 1000 < at) await sleep(1000);
    paused = null; send('Debugger.pause'); for (let i = 0; i < 100 && !paused; i++) await sleep(100);
    if (!paused) { console.log(at + ' s: no pause in 10 s'); continue; }
    const fr = paused.callFrames.slice(0, 8).map(f => (f.functionName || '(anon)') + ' @' + (f.location.lineNumber + 1) + ':' + f.location.columnNumber);
    console.log(at + ' s: paused at', fr.join('  <  '));
    await send('Debugger.resume');
  }
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log('error', e && e.message); chrome.kill(); process.exit(1); });
