// Film "Opened 3 Times": the phones. Set dressing drawn in Chrome around one real thing:
// the itinerary cover from the demo's own itinerary maker (screens/opened/cover.png).
//   node build/opened_stills.mjs -> screens/opened/lockT.png, cover_phone.png, lockW0.png, lockW1.png
import puppeteer from 'puppeteer-core';
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AD = path.resolve(HERE, '..');
const OUT = path.join(AD, 'screens', 'opened');
const sys = "-apple-system,'Helvetica Neue',Arial";
const KOMODO = 'https://wgzwrrrfzxdnkrfebkqb.supabase.co/storage/v1/object/public/trip-images/showcase/komodo.jpg';
const cover = pathToFileURL(path.join(OUT, 'cover.png')).href;
const bubble = (c) => `<svg width="76" height="76" viewBox="0 0 24 24" style="flex:none;margin-top:4px"><rect width="24" height="24" rx="6" fill="${c}"/><path d="M6 7.5h12a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-6.2L8.5 18v-2.5H6a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1z" fill="#fff"/></svg>`;
const card = (who, body, at, fresh, c = '#3E9B6B') => `<div style="margin:0 44px 22px;padding:34px 38px;border-radius:52px;background:rgba(255,255,255,${fresh ? 0.2 : 0.12});display:flex;gap:30px;align-items:flex-start">${bubble(c)}
  <div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;font:600 50px ${sys};color:#fff"><span>${who}</span><span style="font-weight:400;color:rgba(255,255,255,.62);font-size:42px">${at}</span></div>
  <div style="font:400 58px/1.16 ${sys};color:#fff;margin-top:8px">${body}</div></div></div>`;
const lock = (clock, date, cards, foot) => `<body style="margin:0;width:1290px;height:2796px;overflow:hidden;background:radial-gradient(120% 70% at 50% 0%,#1B2B3F 0%,#0B121B 60%,#070B11 100%)">
  <div style="text-align:center;padding-top:250px;font:500 62px ${sys};color:rgba(255,255,255,.82)">${date}</div>
  <div style="text-align:center;font:600 330px/1.05 ${sys};color:#fff;letter-spacing:-6px">${clock}</div>
  <div style="margin-top:150px">${cards}</div>
  <div style="position:absolute;left:0;right:0;${cards ? 'bottom:150px' : 'top:1180px'};text-align:center;font:500 ${cards ? 52 : 92}px ${sys};color:rgba(255,255,255,${cards ? 0.55 : 0.8})">${foot}</div></body>`;
const PAGES = {
  lockT: lock('20:14', 'Monday 9 November',
    card('Lantern Trips', 'Your Komodo plan is ready. Tap to open.', '20:14', true) + card('Travel & Tours', 'Komodo_4D3N_quotation_FINAL.pdf', '19:52', false, '#7A8791'), '2 new'),
  // her lock screen later on: the other agency's quotation is still sitting there unread
  lockT1: lock('07:42', 'Tuesday 10 November', card('Travel & Tours', 'Komodo_4D3N_quotation_FINAL.pdf', 'Mon', false, '#7A8791'), '1 unread'),
  lockT2: lock('22:10', 'Tuesday 10 November', card('Travel & Tours', 'Komodo_4D3N_quotation_FINAL.pdf', 'Mon', false, '#7A8791'), '1 unread'),
  lockW0: lock('09:00', 'Tuesday 10 November', '', 'No new messages'),
  lockW1: lock('09:00', 'Wednesday 11 November', '', 'No new messages'),
  // the plan as she sees it: the real cover page in a plain viewer, with the listing's own Komodo photo in its first frame
  cover_phone: `<body style="margin:0;width:1290px;height:2796px;overflow:hidden;background:#14181D;position:relative">
    <div style="padding:150px 60px 0;font:600 50px ${sys};color:#fff">Your plan from Lantern Trips</div>
    <div style="padding:12px 60px 0;font:400 40px ${sys};color:rgba(255,255,255,.6)">Komodo by phinisi · 14 pages</div>
    <img src="${cover}" style="position:absolute;left:0;top:420px;width:1290px;height:1814px">
    <div style="position:absolute;left:${Math.round(455 / 2048 * 1290 - 179)}px;top:${Math.round(420 + 600 / 2880 * 1814 - 179)}px;width:358px;height:358px;border-radius:50%;background:url('${KOMODO}') center/cover"></div>
    <div style="position:absolute;left:0;right:0;top:2330px;text-align:center;font:500 44px ${sys};color:rgba(255,255,255,.6)">1 of 14</div></body>`,
};
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--allow-file-access-from-files', '--force-color-profile=srgb'] });
try {
  const p = await b.newPage();
  await p.setViewport({ width: 1290, height: 2796, deviceScaleFactor: 1 });
  const tmp = path.join(AD, 'render', '_opened.html');
  for (const [k, html] of Object.entries(PAGES)) {
    writeFileSync(tmp, `<!doctype html><meta charset=utf-8>${html}`);
    await p.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0' });
    await p.screenshot({ path: path.join(OUT, `${k}.png`) });
    console.log('wrote', k);
  }
} finally { await b.close(); }
