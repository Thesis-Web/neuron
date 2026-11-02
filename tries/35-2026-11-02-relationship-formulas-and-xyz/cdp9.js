// cdp9.js (2026-11-02): open a Point Of Connection page in headless Chromium, wait until it is ready, read what it drew, read the kinds'
// pulls and directions as the page holds them (from the brain's formula rows), click a point (showNode) and read its panel (the brain's
// place), step, play, screenshot. env: URL, PORT, TAG, SP (where screenshots go), WAITREADY (s, default 300), WORD (the point to show)
const { spawn } = require('child_process'); const fs = require('fs');
const S = process.env.SP, BIN = '/home/exnulla/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', PORT = +process.env.PORT || 9344, URL = process.env.URL, WORD = process.env.WORD || 'water';
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
  const st = "JSON.stringify({ready:(typeof ready!=='undefined'&&ready), nodeKeys:(window.NODE?Object.keys(NODE).length:null), springs:(window.SPRINGS?SPRINGS.length:null), hist:(window.HIST?HIST.length:null), busy:(document.getElementById('busy')||{}).textContent})";
  const WR = +(process.env.WAITREADY || 300); let s = null;
  for (let i = 0; i < WR; i++) { await sleep(1000); s = JSON.parse(await ev(st)); if (s.ready) break; if (i % 30 === 29) console.log('waiting', i + 1, 's', JSON.stringify(s).slice(0, 200)); }
  console.log('ready after', ((Date.now() - t0) / 1000).toFixed(1), 's:', JSON.stringify(s).slice(0, 400));
  await sleep(3000); await snap(1);
  console.log('kinds (pull, dir, rest) as the page holds them:', await ev("JSON.stringify(Object.keys(RELSET).filter(function(k){return ['alike','opposite','is','includes','has','part','member','similar','related','derived-from','alias','implies','causes','past','topic','use','property','inverse','contradicts'].indexOf(k)>=0}).map(function(k){return [k, RELSET[k].w, RELSET[k].dir, REST[k]]}))"));
  console.log('formula rows applied:', await ev("JSON.stringify({applied: typeof FORMULA_APPLIED !== 'undefined' ? FORMULA_APPLIED : 'n/a', xyz: typeof XYZ !== 'undefined' ? Object.keys(XYZ).length : 'n/a'})"));
  console.log('slider of alike / select of is in the DOM:', await ev("JSON.stringify([ (document.querySelector('input[data-relw=\"alike\"]')||{}).value, (document.querySelector('select[data-reldir=\"is\"]')||{}).value, (document.querySelector('select[data-reldir=\"opposite\"]')||{}).value ])"));
  const g = await ev("String(SYM['" + WORD + "'])"); console.log('gate of', WORD, g);
  await ev("showNode(" + g + "); showTab('panel-sel'); 'ok'"); await sleep(4000);
  console.log('panel of', WORD + ':', JSON.stringify(await ev("document.getElementById('sel').innerText")).slice(0, 900));
  console.log('drawn at (the page) vs the brain:', await ev("JSON.stringify({page: NODE['" + g + "'] ? [NODE['" + g + "'].pos.x, NODE['" + g + "'].pos.y, NODE['" + g + "'].pos.z] : null, brain: XYZ && XYZ[" + g + "] ? XYZ[" + g + "].slice(1) : null})"));
  await snap(2);
  const s1 = JSON.parse(await ev(st)); const tA = Date.now(); await ev("document.getElementById('fwd').click(); 'ok'"); await sleep(1500); const s2 = JSON.parse(await ev(st)); console.log('step: hist', s1.hist, '->', s2.hist, 'tk', await ev("String(TK)"), ((Date.now() - tA) / 1000).toFixed(1), 's');
  await ev("document.getElementById('play').click(); 'ok'"); await sleep(6000); console.log('after 6 s of play: tk', await ev("String(TK)"), 'playing', await ev("String(playing)"));
  await ev("document.getElementById('play').click(); 'ok'");
  console.log('exceptions:', exc.length, exc.slice(0, 3));
  await snap(3); ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log('error', e && e.message); chrome.kill(); process.exit(1); });
