// Film "Three Agencies", second cut: the phone in the shop next door, her question and her answer. Set dressing
// drawn in Chrome (a plain lock screen, no real app's look), not product UI.
//   node build/agencies_stills2.mjs -> screens/agencies/lockA.png, lockB.png (1290 x 2796)
import puppeteer from 'puppeteer-core';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AD = path.resolve(HERE, '..');
const OUT = path.join(AD, 'screens', 'agencies');
mkdirSync(OUT, { recursive: true });
const NOTES = [
  ['23:47', 'Hi! Is the 16 Nov Ha Giang loop open? We are 2 people.'],
  ['09:06', 'Thanks, but we already booked with Lantern Trips.'],
];
const STATES = [['23:47', 'Wednesday 11 November', 1], ['09:06', 'Thursday 12 November', 2]];
const bubble = '<svg width="76" height="76" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#3E9B6B"/><path d="M6 7.5h12a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-6.2L8.5 18v-2.5H6a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1z" fill="#fff"/></svg>';
const card = ([t, body], fresh) => `<div style="margin:0 44px 22px;padding:34px 38px;border-radius:52px;background:rgba(255,255,255,${fresh ? 0.2 : 0.11});display:flex;gap:30px;align-items:flex-start">
  <div style="flex:none;margin-top:4px">${bubble}</div>
  <div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;font:600 50px -apple-system,'Helvetica Neue',Arial;color:#fff"><span>Hana Novak</span><span style="font-weight:400;color:rgba(255,255,255,.62);font-size:42px">${t}</span></div>
  <div style="font:400 ${fresh ? 72 : 52}px/1.16 -apple-system,'Helvetica Neue',Arial;color:#fff;margin-top:8px">${body}</div></div></div>`;
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--force-color-profile=srgb'] });
try {
  const p = await b.newPage();
  await p.setViewport({ width: 1290, height: 2796, deviceScaleFactor: 1 });
  const tmp = path.join(AD, 'render', '_lock2.html');
  for (const [i, [clock, date, n]] of STATES.entries()) {
    const cards = NOTES.slice(0, n).map((x, k) => card(x, k === n - 1)).reverse().join('');
    writeFileSync(tmp, `<!doctype html><meta charset=utf-8><body style="margin:0;width:1290px;height:2796px;overflow:hidden;background:radial-gradient(120% 70% at 50% 0%,#1B2B3F 0%,#0B121B 60%,#070B11 100%)">
      <div style="text-align:center;padding-top:250px;font:500 62px -apple-system,'Helvetica Neue',Arial;color:rgba(255,255,255,.82)">${date}</div>
      <div style="text-align:center;font:600 330px/1.05 -apple-system,'Helvetica Neue',Arial;color:#fff;letter-spacing:-6px">${clock}</div>
      <div style="margin-top:150px">${cards}</div>
      <div style="position:absolute;left:0;right:0;bottom:150px;text-align:center;font:500 44px -apple-system,'Helvetica Neue',Arial;color:rgba(255,255,255,.5)">${n} unread</div></body>`);
    await p.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0' });
    await p.screenshot({ path: path.join(OUT, `lock${'AB'[i]}.png`) });
    console.log('wrote lock', i);
  }
} finally { await b.close(); }
