// cdp6.js (2026-11-01): the full page in headless Chromium with the sampling profiler on while it loads (where the seconds go), then two
// steps back at the end of the history, timed, then a line typed through the page's own prompt: how long until the page says it ran,
// and whether the history grew and plays. env: URL, PORT, TAG, SP, WAITREADY, LINE
const { spawn } = require('child_process'); const fs = require('fs');
const S = process.env.SP, BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +process.env.PORT || 9344, URL = process.env.URL, LINE = process.env.LINE || 'define : bread';
const chrome = spawn(BIN, ['--headless=new','--no-sandbox','--disable-gpu','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-first-run','--window-size=1800,1000','--remote-debugging-port='+PORT,'--user-data-dir='+S+'/cp'+Date.now(),'about:blank']);
let serr=''; chrome.stderr.on('data',d=>{serr+=d}); const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let t = null; for (let i = 0; i < 60 && !t; i++) { await sleep(500); try { t = await (await fetch('http://127.0.0.1:'+PORT+'/json')).json(); } catch (e) {} }
  if(!t){console.log('no chrome',serr.slice(-500));process.exit(1)} const page = t.find(x => x.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const wait = {}; const exc = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && wait[d.id]) { wait[d.id](d); delete wait[d.id]; } if (d.method === 'Runtime.exceptionThrown') exc.push(d.params.exceptionDetails.text + ' ' + JSON.stringify(d.params.exceptionDetails.exception && d.params.exceptionDetails.exception.description).slice(0,200)); };
  const send = (m, p) => new Promise(r => { const i = ++id; wait[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
  const ev = async e => { const r = await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true }); return r.result && r.result.result ? r.result.result.value : JSON.stringify(r).slice(0, 300); };
  await send('Runtime.enable'); await send('Page.enable'); await send('Profiler.enable'); await send('Profiler.setSamplingInterval', { interval: 2000 }); await send('Profiler.start');
  const t0 = Date.now(); await send('Page.navigate', { url: URL });
  const snap = async n => { const s = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(S + '/page' + process.env.TAG + n + '.png', Buffer.from(s.result.data, 'base64')); };
  const st = "JSON.stringify(window.__poc ? {ready:__poc.ready(), gates:__poc.gates(), dna:__poc.dna(), nodes:__poc.nodes(), springs:__poc.springs(), hits:__poc.cur().hits, tk:__poc.cur().tk, run:__poc.cur().run, busy:(document.getElementById('busy')||{}).textContent} : {ready:false})";
  const WR = +(process.env.WAITREADY || 150); let s = null;
  for (let i = 0; i < WR; i++) { await sleep(1000); s = JSON.parse(await ev(st)); if (s.ready) break; if (i % 20 === 19) console.log('waiting', i + 1, 's'); }
  const tReady = (Date.now() - t0) / 1000;
  const prof = await send('Profiler.stop'); const p = prof.result.profile; const byId = {}; p.nodes.forEach(n => byId[n.id] = n);
  const tot = {}; let total = 0; for (let i = 0; i < p.samples.length; i++) { const n = byId[p.samples[i]]; const dt = p.timeDeltas[i] || 0; total += dt; const k = (n.callFrame.functionName || '(anon)') + ':' + n.callFrame.lineNumber; tot[k] = (tot[k] || 0) + dt; }
  const top = Object.entries(tot).sort((a, b) => b[1] - a[1]).slice(0, 16).map(([k, v]) => k + ' ' + (v / 1e6).toFixed(1) + 's');
  console.log('ready after', tReady.toFixed(1), 's:', JSON.stringify(s).slice(0, 300));
  console.log('profile total', (total / 1e6).toFixed(1), 's; self time:', top.join(' | '));
  await sleep(2000); await snap(1);
  const st2 = "JSON.stringify({tk: __poc.cur().tk, hits: __poc.cur().hits, nodes: __poc.nodes(), springs: __poc.springs(), run: __poc.cur().run})";
  for (let i = 0; i < 2; i++) { const r = await ev("(function(){ var a = performance.now(); document.getElementById('back').click(); return JSON.stringify({ms: Math.round(performance.now() - a), tk: __poc.cur().tk, nodes: __poc.nodes(), springs: __poc.springs()}); })()"); console.log('step back ' + (i + 1) + ':', r); }
  await ev("document.getElementById('line').value = " + JSON.stringify(LINE) + "; document.getElementById('run').click(); 'ok'");
  const t1 = Date.now(); let b = '';
  for (let i = 0; i < 400; i++) { await sleep(1000); b = await ev("document.getElementById('busy').textContent"); if (/^the line ran in|refused|stopped|could not/.test(String(b))) break; }
  console.log('typed through the page: ' + ((Date.now() - t1) / 1000).toFixed(1) + ' s until: ' + String(b).slice(0, 220));
  const c1 = await ev(st2); await sleep(5000); const c2 = await ev(st2);
  console.log('right after:', c1, '| 5 s later:', c2, '| button:', await ev("document.getElementById('play').textContent"));
  await snap(2); console.log('exceptions', exc.slice(0, 6)); chrome.kill(); process.exit(0);
})();
