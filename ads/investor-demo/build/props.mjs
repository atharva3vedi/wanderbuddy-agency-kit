// Set dressing drawn in Chrome, not product UI: the traveller's boarding pass and
// three plain lock screens for her phone (no real app's look, as in b2b-cinematic).
//   node build/props.mjs -> screens/boarding.png, lockEve.png, lock2347.png, lock2348.png
import puppeteer from 'puppeteer-core';
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AD = path.resolve(HERE, '..');
const SCR = path.join(AD, 'screens');
const SYS = "-apple-system,'Helvetica Neue',Arial";
const MONO = 'ui-monospace,SFMono-Regular,Menlo,monospace';

const bubble = '<svg width="76" height="76" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#3E9B6B"/><path d="M6 7.5h12a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-6.2L8.5 18v-2.5H6a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1z" fill="#fff"/></svg>';
const note = (who, t, body) => `<div style="margin:0 44px 22px;padding:36px 40px;border-radius:52px;background:rgba(255,255,255,.2);display:flex;gap:30px;align-items:flex-start">
  <div style="flex:none;margin-top:4px">${bubble}</div>
  <div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;font:600 52px ${SYS};color:#fff"><span>${who}</span><span style="font-weight:400;color:rgba(255,255,255,.62);font-size:42px">${t}</span></div>
  <div style="font:400 64px/1.18 ${SYS};color:#fff;margin-top:10px">${body}</div></div></div>`;
const lock = (date, clock, notes, foot) => `<body style="margin:0;width:1290px;height:2796px;overflow:hidden;background:radial-gradient(120% 70% at 50% 0%,#1B2B3F 0%,#0B121B 60%,#070B11 100%)">
  <div style="text-align:center;padding-top:250px;font:500 62px ${SYS};color:rgba(255,255,255,.82)">${date}</div>
  <div style="text-align:center;font:600 330px/1.05 ${SYS};color:#fff;letter-spacing:-6px">${clock}</div>
  <div style="margin-top:150px">${notes}</div>
  <div style="position:absolute;left:0;right:0;bottom:150px;text-align:center;font:500 44px ${SYS};color:rgba(255,255,255,.5)">${foot}</div></body>`;

// Three friends in the group chat, the way a phone shows them on the lock screen.
const msg = (who, t, body) => `<div style="margin:0 44px 18px;padding:30px 36px;border-radius:52px;background:rgba(255,255,255,.17);display:flex;gap:28px;align-items:flex-start">
  <div style="flex:none;margin-top:4px">${bubble}</div>
  <div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;font:600 48px ${SYS};color:#fff"><span>${who}</span><span style="font-weight:400;color:rgba(255,255,255,.62);font-size:40px">${t}</span></div>
  <div style="font:400 58px/1.18 ${SYS};color:#fff;margin-top:8px">${body}</div></div></div>`;

// The friend's DM to our Instagram account, @wanderbuddyapp. Plain set dressing (a neutral chat,
// not Instagram's own look). The bot's words are the real ones from supabase/functions:
// insp_saving (whatsapp-webhook/i18n.ts) and insp_enriched, which the Instagram bot sends for a
// linked traveller's reel. The three places are sample content for the app's sample reel.
const MARK = path.resolve(HERE, '../../../../website/public/brand/mark.svg');
const dm = `<body style="margin:0;width:1290px;height:2796px;overflow:hidden;background:#0B1018;font-family:${SYS};color:#fff">
  <div style="height:250px"></div>
  <div style="display:flex;align-items:center;gap:30px;padding:0 54px 40px;border-bottom:2px solid rgba(255,255,255,.10)">
    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>
    <img src="file://${MARK}" width="118" height="118" style="border-radius:59px">
    <div><div style="font:600 58px/1.1 ${SYS}">wanderbuddyapp</div><div style="font:400 40px/1.3 ${SYS};color:rgba(255,255,255,.55)">WanderBuddy · Instagram DM</div></div>
  </div>
  <div style="padding:60px 54px 0">
    <div style="text-align:center;font:400 38px ${SYS};color:rgba(255,255,255,.45);margin-bottom:46px">Today 21:20</div>
    <div style="display:flex;justify-content:flex-end;margin-bottom:44px">
      <div style="width:700px;border-radius:56px;overflow:hidden;background:#243041">
        <div style="height:640px;background:linear-gradient(160deg,#35506E 0%,#1B2736 60%,#10161F 100%);position:relative">
          <div style="position:absolute;left:50%;top:50%;margin:-88px 0 0 -88px;width:176px;height:176px;border-radius:88px;background:rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center">
            <svg width="76" height="76" viewBox="0 0 24 24" fill="#fff"><path d="M8 5.5v13l11-6.5z"/></svg></div>
          <div style="position:absolute;left:34px;top:30px;font:600 38px ${SYS};letter-spacing:.02em;color:rgba(255,255,255,.8)">Reel</div>
        </div>
        <div style="padding:30px 38px 36px;font:600 46px/1.25 ${SYS}">Bangkok street food you have to try</div>
      </div>
    </div>
    <div style="width:880px;border-radius:56px;background:#1D2736;padding:38px 46px;font:400 52px/1.32 ${SYS};margin-bottom:26px">Got it ✨ reading your reel now, I'll message you what I find in a moment.</div>
    <div style="width:880px;border-radius:56px;background:#1D2736;padding:38px 46px;font:400 52px/1.32 ${SYS}">Nice find ✨ Bangkok: Yaowarat Road, Thip Samai, Jay Fai.<br><br>I'll use these when you plan. Open WanderBuddy: wanderbuddyapp.com</div>
  </div>
  <div style="position:absolute;left:54px;right:54px;bottom:160px;height:130px;border-radius:65px;border:2px solid rgba(255,255,255,.18);display:flex;align-items:center;padding:0 52px;font:400 48px ${SYS};color:rgba(255,255,255,.4)">Message...</div>
</body>`;

const SHOTS = {
  igDM: { w: 1290, h: 2796, html: dm },
  lockCrew: { w: 1290, h: 2796, html: lock('Sunday 4 October', '21:15',
    msg('Bangkok Crew', '21:14', 'Maya: Which dates work for everyone?') + msg('Bangkok Crew', '21:14', 'Leo: Where was the street food place') + msg('Bangkok Crew', '21:15', 'Priya: I paid for the boat. Who owes me?'), '3 unread') },
  lockEve: { w: 1290, h: 2796, html: lock('Thursday 12 November', '19:42', '', '') },
  lock2347: { w: 1290, h: 2796, html: lock('Thursday 10 December', '23:47', '', 'No new messages') },
  lock2348: { w: 1290, h: 2796, html: lock('Thursday 10 December', '23:48',
    note('Lantern Trips', 'now', 'Assistant, from your trip plan: Pickup is at 07:30 from the Lantern Basecamp lobby.'), '1 unread') },
  // Her flight in, in the same plain mono as the knolling props of the "Order" film.
  boarding: { w: 480, h: 1140, html: `<body style="margin:0;width:480px;height:1140px;background:#F4F6F8;font:500 30px/1.45 ${MONO};color:#1C2733">
    <div style="padding:42px 34px 0"><div style="font-weight:700;font-size:34px;letter-spacing:.12em">BOARDING PASS</div>
    <div style="margin-top:36px">SINGAPORE SIN<br>&#8594; KRABI KBV</div>
    <div style="margin-top:34px">9 DEC 07:55<br>SEAT 12A<br>GATE C21</div>
    <div style="margin-top:34px">NOVAK/HANA</div>
    <div style="margin-top:38px;height:200px;background:repeating-linear-gradient(90deg,#1C2733 0 3px,transparent 3px 7px,#1C2733 7px 8px,transparent 8px 12px,#1C2733 12px 16px,transparent 16px 19px)"></div></div>
    <div style="position:absolute;left:0;right:0;top:860px;border-top:3px dashed #B9C3CE"></div>
    <div style="position:absolute;left:34px;top:900px">SIN &#8594; KBV<br>12A · 9 DEC</div></body>` },
};

const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--force-color-profile=srgb'] });
try {
  const p = await b.newPage();
  for (const [name, s] of Object.entries(SHOTS)) {
    await p.setViewport({ width: s.w, height: s.h, deviceScaleFactor: 1 });
    const tmp = path.join(AD, 'render', `_${name}.html`);
    writeFileSync(tmp, `<!doctype html><meta charset=utf-8>${s.html}`);
    await p.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0' });
    await p.screenshot({ path: path.join(SCR, `${name}.png`) });
    console.log('wrote', name);
  }
} finally { await b.close(); }
