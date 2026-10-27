// drives the page in headless Chromium over the DevTools protocol: no library, Node 22's WebSocket and fetch
const { spawn } = require('child_process'); const fs = require('fs');
const S = process.env.S, BIN = process.env.BIN, PORT = 9333;
const chrome = spawn(BIN, ['--headless=new', '--no-sandbox', '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run', '--window-size=1600,1000', '--hide-scrollbars', '--remote-debugging-port=' + PORT, '--user-data-dir=' + S + '/chrome-cdp', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
let stderr = ''; chrome.stderr.on('data', d => { stderr += d; });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let targets = null;
  for (let i = 0; i < 60 && !targets; i++) { await sleep(500); try { targets = await (await fetch('http://127.0.0.1:' + PORT + '/json')).json(); } catch (e) {} }
  if (!targets) { console.log('no chrome', stderr.slice(-500)); process.exit(1); }
  const page = targets.find(t => t.type === 'page'); const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  let id = 0; const waiting = {}; const console_ = [];
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && waiting[d.id]) { waiting[d.id](d); delete waiting[d.id]; } if (d.method === 'Runtime.exceptionThrown') console_.push('EXCEPTION ' + JSON.stringify(d.params.exceptionDetails.exception && d.params.exceptionDetails.exception.description || d.params.exceptionDetails.text).slice(0, 300)); if (d.method === 'Runtime.consoleAPICalled' && d.params.type !== 'log') console_.push(d.params.type + ' ' + d.params.args.map(a => a.value || a.description).join(' ').slice(0, 200)); };
  const send = (method, params) => new Promise(r => { const i = ++id; waiting[i] = r; ws.send(JSON.stringify({ id: i, method, params: params || {} })); });
  const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.result.exceptionDetails) return 'EXC ' + (r.result.exceptionDetails.exception || {}).description; return r.result.result.value; };
  const text = sel => ev(`(document.querySelector(${JSON.stringify(sel)}) || {innerText: 'MISSING'}).innerText.replace(/\\s+/g, ' ').slice(0, 420)`);
  const shot = async name => { const r = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(S + '/' + name + '.png', Buffer.from(r.result.data, 'base64')); };
  const until = async (expr, ms) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await ev(expr)) return true; await sleep(300); } return false; };
  await send('Runtime.enable'); await send('Page.enable');
  await send('Page.navigate', { url: 'http://localhost:8018/' });
  console.log('ready:', await until('window.__poc && __poc.ready()', 60000));
  await sleep(2500);
  console.log('counts:', JSON.stringify(await ev('__poc.counts()')), 'nodes', await ev('__poc.nodes()'), 'springs', await ev('__poc.springs()'));
  console.log('cur:', JSON.stringify(await ev('__poc.cur()')));
  console.log('busy line:', await text('#busy'));
  await shot('t1-open');
  // tabs: step on the right, neurons on the left
  await ev(`document.querySelector('[data-panel="panel-step"]').click(); document.querySelector('[data-panel="panel-neurons"]').click(); 1`);
  console.log('step hidden?', await ev(`document.getElementById('panel-step').hidden`), 'type hidden?', await ev(`document.getElementById('panel-type').hidden`), 'neurons hidden?', await ev(`document.getElementById('panel-neurons').hidden`));
  // step a few hops, then play through
  await ev(`document.getElementById('fwd').click(); document.getElementById('fwd').click(); 1`);
  console.log('after two hops:', JSON.stringify(await ev('__poc.cur()')), '|', await text('#now'));
  await ev(`document.getElementById('play').click(); 1`); await sleep(4000);
  console.log('after play 4 s:', JSON.stringify(await ev('__poc.cur()')), '| readout', await text('#readout'));
  await ev(`document.getElementById('play').click(); 1`);
  await shot('t2-step');
  // the neurons list: click dog
  await ev(`document.getElementById('nfind').value = 'dog'; document.getElementById('nfind').dispatchEvent(new Event('input')); 1`);
  console.log('nsum:', await text('#nsum'));
  await ev(`var d = document.querySelector('#nlist [data-gate="293"]'); d && d.click(); 1`);
  await sleep(1500);
  console.log('sel hidden?', await ev(`document.getElementById('panel-sel').hidden`));
  console.log('sel:', await text('#sel'));
  console.log('dna:', await text('#dnarows'));
  console.log('defrows:', await text('#defrows'));
  console.log('gatesql:', (await text('#gatesql')).slice(0, 160));
  await shot('t3-selected');
  // the run tab for the define formula run 65 (a child of the define : dog line)
  await ev(`__poc.chooseRun(65, 3); document.querySelector('[data-panel="panel-run"]').click(); 1`); await sleep(2000);
  console.log('runhead:', await text('#runhead'));
  console.log('cells:', (await text('#cells')).slice(0, 300));
  console.log('builds:', (await text('#builds')).slice(0, 400));
  console.log('runrows:', (await text('#runrows')).slice(0, 300));
  await shot('t4-run');
  // type a known line through the door and wait
  await ev(`document.querySelector('[data-panel="panel-type"]').click(); __poc.send('define : cat'); 1`);
  console.log('typed; done:', await until('!__poc.busy()', 120000));
  console.log('busy line:', await text('#busy'));
  console.log('cur after line:', JSON.stringify(await ev('__poc.cur()')), '| counts', JSON.stringify(await ev('__poc.counts()')));
  console.log('lines list tail:', (await text('#llist')).slice(-300));
  // brain tab, trigger SQL
  await ev(`document.querySelector('[data-panel="panel-brain"]').click(); document.querySelector('#tlist [data-trig="hop_go"]').click(); 1`); await sleep(1500);
  console.log('tsql:', (await text('#tsql')).slice(0, 200));
  console.log('flist:', await text('#flist'));
  await shot('t5-brain');
  // the atlas
  await ev(`document.getElementById('atlasbtn').click(); 1`); await sleep(3000);
  console.log('asum:', await text('#asum'));
  console.log('atlas rows:', await ev(`document.querySelectorAll('#atable tr.arow').length`));
  await ev(`document.getElementById('afind').value = 'dog'; document.getElementById('afind').dispatchEvent(new Event('input')); document.querySelector('#atable tr.arow').click(); 1`); await sleep(1500);
  console.log('atlas detail:', (await text('#atable tr.det')).slice(0, 400));
  await shot('t6-atlas');
  await ev(`document.getElementById('aclose').click(); 1`);
  console.log('console:', console_.length ? console_.join('\n  ') : 'nothing but logs');
  ws.close(); chrome.kill(); process.exit(0);
})().catch(e => { console.log('FAILED', e); chrome.kill(); process.exit(1); });
