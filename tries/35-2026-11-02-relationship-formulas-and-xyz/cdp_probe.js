// cdp_probe.js: open the page and ask it every 5 s whether its thread answers (a 20 s deadline per ask), for up to PROBE_S seconds
const { spawn } = require('child_process');
const S = process.env.SP, BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +process.env.PORT || 9360, URL = process.env.URL, PROBE_S = +(process.env.PROBE_S || 240);
const chrome = spawn(BIN, ['--headless=new','--no-sandbox','--disable-gpu','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-first-run','--window-size=1800,1000','--remote-debugging-port='+PORT,'--user-data-dir='+S+'/cp'+Date.now(),'about:blank']);
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let t = null; for (let i = 0; i < 60 && !t; i++) { await sleep(500); try { t = await (await fetch('http://127.0.0.1:'+PORT+'/json')).json(); } catch (e) {} }
  if(!t){console.log('no chrome');process.exit(1)} const page = t.find(x => x.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const wait = {}; const exc = []; const logs = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && wait[d.id]) { wait[d.id](d); delete wait[d.id]; } if (d.method === 'Runtime.exceptionThrown') exc.push((d.params.exceptionDetails.text || '') + ' ' + JSON.stringify(d.params.exceptionDetails.exception && d.params.exceptionDetails.exception.description).slice(0,300)); if (d.method === 'Runtime.consoleAPICalled') logs.push(d.params.args.map(a => a.value || a.description).join(' ').slice(0, 200)); };
  const send = (m, p) => new Promise(r => { const i = ++id; wait[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
  const ev = (e, ms) => Promise.race([send('Runtime.evaluate', { expression: e, returnByValue: true }).then(r => r.result && r.result.result ? r.result.result.value : JSON.stringify(r).slice(0, 200)), sleep(ms).then(() => 'NO ANSWER in ' + ms + ' ms')]);
  await send('Runtime.enable'); await send('Page.enable'); const t0 = Date.now(); await send('Page.navigate', { url: URL });
  for (let i = 0; i < PROBE_S / 5; i++) { await sleep(5000); const a = await ev("document.readyState + ' ready=' + (typeof ready !== 'undefined' ? ready : '?') + ' busy=' + ((document.getElementById('busy')||{}).textContent||'') + ' nodes=' + (window.NODE ? Object.keys(NODE).length : '?') + ' hist=' + (window.HIST ? HIST.length : '?')", 20000); console.log(((Date.now() - t0) / 1000).toFixed(0) + ' s:', a, '| exceptions', exc.length, '| console', logs.length); if (exc.length) { console.log(exc.slice(0, 3)); } if (logs.length) console.log('console:', logs.slice(-3)); if (/ready=true/.test(a)) break; }
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log('error', e && e.message); chrome.kill(); process.exit(1); });
