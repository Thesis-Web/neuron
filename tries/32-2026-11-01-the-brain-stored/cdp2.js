const { spawn } = require('child_process'); const fs = require('fs');
const S = process.env.SP, BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +process.env.PORT || 9344, URL = process.env.URL;
const chrome = spawn(BIN, ['--headless=new','--no-sandbox','--disable-gpu','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-first-run','--window-size=1800,1000','--remote-debugging-port='+PORT,'--user-data-dir='+S+'/cp'+Date.now(),'about:blank']);
let serr=''; chrome.stderr.on('data',d=>{serr+=d}); const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let t = null; for (let i = 0; i < 60 && !t; i++) { await sleep(500); try { t = await (await fetch('http://127.0.0.1:'+PORT+'/json')).json(); } catch (e) {} }
  if(!t){console.log('no chrome',serr.slice(-500));process.exit(1)} const page = t.find(x => x.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const wait = {}; const exc = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && wait[d.id]) { wait[d.id](d); delete wait[d.id]; } if (d.method === 'Runtime.exceptionThrown') exc.push(d.params.exceptionDetails.text + ' ' + JSON.stringify(d.params.exceptionDetails.exception && d.params.exceptionDetails.exception.description).slice(0,200)); };
  const send = (m, p) => new Promise(r => { const i = ++id; wait[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
  const ev = async e => { const r = await send('Runtime.evaluate', { expression: e, returnByValue: true }); return r.result.result ? r.result.result.value : r; };
  await send('Runtime.enable'); await send('Page.enable'); await send('Page.navigate', { url: URL });
  const snap = async n => { const s = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(S + '/page' + process.env.TAG + n + '.png', Buffer.from(s.result.data, 'base64')); };
  const st = () => process.env.TAG === 'hub' ? ev("JSON.stringify({ready:typeof ready!=='undefined'&&ready, hud:(document.getElementById('hud')||{}).innerText, busy:(document.getElementById('busy')||{}).innerText, memall:(document.getElementById('memall')||{}).checked, points:(window.NODE?Object.keys(window.NODE).length:null), hist:(window.HIST?HIST.length:null)})") : ev("JSON.stringify({ready:window.__nk&&__nk.ready(),run:window.__nk&&__nk.run(),points:window.__nk&&__nk.points(),springs:window.__nk&&__nk.springs(),busy:(document.getElementById('busy')||{}).textContent,tiles:(document.getElementById('tiles')||{}).innerText})");
  const N = +process.env.N || 5; for (let i = 0; i < N; i++) { await sleep(+process.env.WAIT || 8000); console.log(i, (await st()).slice(0, 330)); if (i === 1) await snap(1); }
  await snap(2); console.log('exceptions', exc.slice(0, 5)); chrome.kill(); process.exit(0);
})();
