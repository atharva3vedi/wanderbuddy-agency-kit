// Fresh captures of live WanderBuddy pages at phone size via Chrome DevTools Protocol.
import { spawn } from 'node:child_process'; import fs from 'node:fs'; import path from 'node:path';
const OUT = path.resolve(process.argv[2]); const JOBS = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PROFILE = path.resolve('E:/render/india-ads/chrome-profile');
const port = 9333;
const proc = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${PROFILE}`, '--mute-audio', '--no-first-run', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ver; for (let i = 0; i < 40; i++) { try { ver = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); break; } catch { await sleep(250); } }
const ws = new WebSocket(ver.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pending = new Map(); const events = [];
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } else events.push(d); };
const send = (method, params = {}, sessionId) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params, sessionId })); });
for (const job of JOBS) {
  const { result: { targetId } } = await send('Target.createTarget', { url: 'about:blank' });
  const { result: { sessionId } } = await send('Target.attachToTarget', { targetId, flatten: true });
  const s = (m, p) => send(m, p, sessionId);
  await s('Page.enable'); await s('Runtime.enable');
  await s('Emulation.setDeviceMetricsOverride', { width: job.w || 390, height: job.h || 844, deviceScaleFactor: job.dpr || 3, mobile: job.mobile !== false });
  await s('Emulation.setUserAgentOverride', { userAgent: job.mobile === false ? 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' });
  await s('Page.navigate', { url: job.url });
  await sleep(job.wait || 6000);
  if (job.js) { const r = await s('Runtime.evaluate', { expression: job.js, awaitPromise: true, returnByValue: true }); if (r.result?.exceptionDetails) console.log('js error', job.name, JSON.stringify(r.result.exceptionDetails).slice(0, 300)); else if (r.result?.result?.value !== undefined) console.log(job.name, 'js ->', JSON.stringify(r.result.result.value).slice(0, 400)); await sleep(job.after || 2500); }
  const shot = await s('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  fs.writeFileSync(path.join(OUT, job.name + '.png'), Buffer.from(shot.result.data, 'base64'));
  console.log('saved', job.name);
  await send('Target.closeTarget', { targetId });
}
ws.close(); proc.kill();
