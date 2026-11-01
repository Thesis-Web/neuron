// cdp3.js (2026-11-01): open a Point Of Connection page in headless Chromium, wait until it is ready, read what it drew, press play and step,
// and report whether the history moves. env: URL, PORT, TAG, SP (where screenshots go), WAITREADY (s, default 150)
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
  const ev = async e => { const r = await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true }); return r.result && r.result.result ? r.result.result.value : JSON.stringify(r).slice(0, 300); };
  await send('Runtime.enable'); await send('Page.enable'); const t0 = Date.now(); await send('Page.navigate', { url: URL });
  const snap = async n => { const s = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(S + '/page' + process.env.TAG + n + '.png', Buffer.from(s.result.data, 'base64')); };
  const st = "JSON.stringify(window.__poc ? {ready:__poc.ready(), gates:__poc.gates(), dna:__poc.dna(), nodes:__poc.nodes(), springs:__poc.springs(), hits:__poc.cur().hits, tk:__poc.cur().tk, run:__poc.cur().run, busy:(document.getElementById('busy')||{}).textContent} : {ready:(typeof ready!=='undefined'&&ready), nodeKeys:(window.NODE?Object.keys(NODE).length:null), busy:(document.getElementById('busy')||{}).textContent})";
  const WR = +(process.env.WAITREADY || 150); let s = null;
  for (let i = 0; i < WR; i++) { await sleep(1000); s = JSON.parse(await ev(st)); if (s.ready) break; if (i % 10 === 9) console.log('waiting', i + 1, 's', JSON.stringify(s).slice(0, 200)); }
  console.log('ready after', ((Date.now() - t0) / 1000).toFixed(1), 's:', JSON.stringify(s).slice(0, 400));
  await sleep(3000); await snap(1);
  // one step forward, timed; then play for 6 s; then step back
  const tStep = await ev("(function(){ var a = performance.now(); document.getElementById('fwd').click(); return JSON.stringify({ms: performance.now() - a, tk: __poc.cur().tk, hits: __poc.cur().hits}); })()");
  console.log('one step:', tStep);
  await ev("document.getElementById('play').click(); 'ok'"); await sleep(6000);
  const after = JSON.parse(await ev(st)); console.log('after 6 s of play:', JSON.stringify(after).slice(0, 300), 'playing:', await ev("document.getElementById('play').textContent"));
  await ev("document.getElementById('play').click(); 'ok'");
  const tBack = await ev("(function(){ var a = performance.now(); document.getElementById('back').click(); return JSON.stringify({ms: performance.now() - a, tk: __poc.cur().tk}); })()");
  console.log('one step back:', tBack);
  await snap(2); console.log('exceptions', exc.slice(0, 6)); chrome.kill(); process.exit(0);
})();
