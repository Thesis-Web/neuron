// drives the v6 page in headless Chromium over the DevTools protocol: no library, Node 22's WebSocket and fetch (as tries/15's check did)
const { spawn } = require('child_process'); const fs = require('fs');
const S = process.env.S, BIN = process.env.BIN, PORT = 9334, W = +(process.env.W || 3787), H = +(process.env.H || 1918);
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=' + W + ',' + H, '--hide-scrollbars', '--remote-debugging-port=' + PORT, '--user-data-dir=' + S + '/chrome-v6', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
let stderr = ''; chrome.stderr.on('data', d => { stderr += d; });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let targets = null;
  for (let i = 0; i < 60 && !targets; i++) { await sleep(500); try { targets = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  if (!targets) { console.log('no chrome', stderr.slice(-800)); process.exit(1); }
  const page = targets.find(t => t.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  let id = 0; const waiting = {}; const console_ = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && waiting[d.id]) { waiting[d.id](d); delete waiting[d.id]; } if (d.method === 'Runtime.exceptionThrown') console_.push('EXCEPTION ' + JSON.stringify(d.params.exceptionDetails).slice(0, 400)); if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') console_.push('console.error ' + JSON.stringify(d.params.args).slice(0, 300)); };
  const send = (method, params) => new Promise(r => { const i = ++id; waiting[i] = r; ws.send(JSON.stringify({ id: i, method, params: params || {} })); });
  const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.result.exceptionDetails) return 'EXC ' + (r.result.exceptionDetails.exception ? r.result.exceptionDetails.exception.description : JSON.stringify(r.result.exceptionDetails)).slice(0, 300); return r.result.result.value; };
  const text = sel => ev(`(document.querySelector(${JSON.stringify(sel)}) || {innerText: 'MISSING'}).innerText.replace(/\\s+/g, ' ').slice(0, 500)`);
  const shot = async name => { const r = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(S + '/' + name + '.png', Buffer.from(r.result.data, 'base64')); };
  const until = async (expr, ms) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await ev(expr)) return true; await sleep(300); } return false; };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: 'http://localhost:8056/' });
  console.log('ready:', await until('window.__poc && __poc.ready()', 90000));
  await sleep(3000);
  console.log('counts:', JSON.stringify(await ev('__poc.counts()')));
  console.log('gates', await ev('__poc.gates()'), 'dna', await ev('__poc.dna()'), 'nodes drawn', await ev('__poc.nodes()'), 'springs', await ev('__poc.springs()'), 'lonely', await ev('__poc.lonely()'));
  console.log('kinds:', JSON.stringify(await ev('__poc.kinds()')));
  console.log('cur:', JSON.stringify(await ev('__poc.cur()')), '| lines listed', await ev('__poc.lines()'));
  console.log('busy:', await text('#busy'));
  console.log('hud:', await text('#hud'));
  await shot('v6-1-open-3s');
  await sleep(9000); await shot('v6-2-open-12s');
  console.log('stretch', await ev('__poc.stretch()'));
  // step and play
  await ev(`document.querySelector('[data-panel="panel-step"]').click(); document.getElementById('fwd').click(); document.getElementById('fwd').click(); 1`);
  console.log('after two hops:', JSON.stringify(await ev('__poc.cur()')), '|', await text('#now'));
  await ev(`document.getElementById('play').click(); 1`); await sleep(4000);
  console.log('after play 4 s:', JSON.stringify(await ev('__poc.cur()')), '| readout', await text('#readout'));
  await ev(`document.getElementById('play').click(); 1`);
  await shot('v6-3-step');
  console.log('tree:', (await text('#tree')).slice(0, 300));
  // the run tab
  await ev(`document.querySelector('[data-panel="panel-run"]').click(); 1`); await sleep(1500);
  console.log('runhead:', await text('#runhead'));
  console.log('cells:', (await text('#cells')).slice(0, 400));
  console.log('builds:', (await text('#builds')).slice(0, 300));
  await shot('v6-4-run');
  // select who under neurons
  await ev(`document.querySelector('[data-panel="panel-neurons"]').click(); document.getElementById('nfind').value = 'who'; document.getElementById('nfind').dispatchEvent(new Event('input')); 1`);
  console.log('nsum:', await text('#nsum'));
  await ev(`var d = document.querySelector('#nlist [data-gate]'); d && d.click(); 1`); await sleep(1500);
  console.log('sel:', await text('#sel'));
  console.log('dna:', (await text('#dnarows')).slice(0, 400));
  console.log('defrows:', (await text('#defrows')).slice(0, 300));
  await shot('v6-5-selected');
  // type define : the through the page
  await ev(`document.querySelector('[data-panel="panel-type"]').click(); __poc.send('define : the', 'main'); 1`);
  console.log('typed; done:', await until('!__poc.busy()', 180000));
  console.log('busy:', await text('#busy'));
  await sleep(2500);
  console.log('out:', (await text('#out')).slice(0, 900));
  console.log('cur after line:', JSON.stringify(await ev('__poc.cur()')), '| kinds', JSON.stringify(await ev('__poc.kinds()')), '| nodes', await ev('__poc.nodes()'));
  await shot('v6-6-after-define-the');
  // a print line
  await ev(`__poc.send('print dna : the', 'main'); 1`);
  console.log('print done:', await until('!__poc.busy()', 120000));
  await sleep(1500);
  console.log('out after print:', (await text('#out')).slice(0, 700));
  await shot('v6-7-after-print');
  // brains tab and the atlas
  await ev(`document.querySelector('[data-panel="panel-brain"]').click(); 1`); await sleep(1500);
  console.log('counts tiles:', (await text('#counts')).slice(0, 300));
  console.log('trust:', (await text('#trust')).slice(0, 300));
  console.log('jobs:', (await text('#jobs')).slice(0, 300));
  await shot('v6-8-brains');
  await ev(`document.getElementById('atlasbtn').click(); 1`); await sleep(1500);
  console.log('atlas:', (await text('#asum')).slice(0, 300), '|', await text('#ashown'));
  await shot('v6-9-atlas');
  await ev(`document.getElementById('aclose').click(); 1`);
  // a smaller window
  await send('Emulation.setDeviceMetricsOverride', { width: 1900, height: 1000, deviceScaleFactor: 1, mobile: false }); await sleep(4000);
  await shot('v6-10-1900');
  console.log('exceptions:', console_.length ? console_.join('\n') : 'none');
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log('driver error', e); chrome.kill(); process.exit(1); });
