// Film "Three Agencies": the real CRM inbox, from the public Lantern Trips demo
// (wanderbuddyapp.com/trydemo: the real CRM on sample data kept in this browser only).
// One of the demo's own assistant threads is given a Ha Giang trip and the pickup
// question, in this browser's copy of the sample data. Nothing is saved anywhere else.
//   node build/agencies_capture.mjs  -> screens/agencies/inbox_q.png, inbox_qa.png, inbox.json
import puppeteer from 'puppeteer-core';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens/agencies');
mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const URL = 'https://wanderbuddyapp.com/trydemo/app/#/inbox';
const Q = 'What time is pickup tomorrow?';
const A = 'Pickup is at 06:30 from the Lantern House lobby in Ha Giang town. It is the Ma Pi Leng Pass day: bring a rain jacket and VND 150,000 in cash for the Nho Que boat, it is not included.';
const Q_AT = '2026-11-12T16:47:00.000Z';   // Thu 23:47 in Hanoi
const A_AT = '2026-11-12T16:48:00.000Z';

const b = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new', args: ['--force-color-profile=srgb'],
});
try {
  const p = await b.newPage();
  await p.emulateTimezone('Asia/Ho_Chi_Minh');
  await p.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
  // The film's night: Thursday 12 Nov 2026, 23:49 in Hanoi.
  await p.evaluateOnNewDocument((t) => {
    const RealDate = Date; const off = t - RealDate.now();
    // eslint-disable-next-line no-global-assign
    Date = class extends RealDate { constructor(...a) { if (a.length) super(...a); else super(RealDate.now() + off); } static now() { return RealDate.now() + off; } };
  }, Date.parse('2026-11-12T16:49:00.000Z'));
  await p.goto(URL, { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(3000);
  for (const withAnswer of [true, false]) {
    const who = await p.evaluate((Q, A, Q_AT, A_AT, withAnswer) => {
      const db = JSON.parse(localStorage.getItem('wb-demo-try'));
      const th = db.tables.crm_threads.find((t) => t.data?.via === 'concierge' && /Grace/.test(t.who));
      const mine = db.tables.crm_messages.filter((m) => m.thread_id === th.id).sort((a, b) => a.created_at.localeCompare(b.created_at));
      const q = mine.find((m) => m.kind === 'in'), a = mine.find((m) => m.kind === 'bot');
      Object.assign(q, { body: Q, created_at: Q_AT, updated_at: Q_AT, last_at: Q_AT });
      Object.assign(a, { body: A, created_at: A_AT, updated_at: A_AT, last_at: A_AT });
      db.tables.crm_messages = db.tables.crm_messages.filter((m) => m.thread_id !== th.id).concat(withAnswer ? [q, a] : [q]);
      Object.assign(th, { last_at: withAnswer ? A_AT : Q_AT, unread: false });
      const trip = db.tables.crm_trips.find((t) => t.id === th.trip_id);
      Object.assign(trip, { dest: 'Ha Giang Loop, small group', ref: 'TR-HGL-261110-GRA' });
      trip.data.tagline = 'Ha Giang town, Ma Pi Leng Pass, the Nho Que river, three homestays';
      localStorage.setItem('wb-demo-try', JSON.stringify(db));
      return th.who;
    }, Q, A, Q_AT, A_AT, withAnswer);
    await p.reload({ waitUntil: 'networkidle2' });
    await sleep(2500);
    await p.evaluate(() => { for (const x of document.querySelectorAll('button')) if (/^not now$/i.test(x.textContent.trim())) x.click(); });
    await p.evaluate((who) => {
      const els = [...document.querySelectorAll('button, a, [role=button], li, .row, [data-id]')];
      els.find((e) => (e.textContent || '').includes(who) && e.offsetParent)?.click();
    }, who);
    await sleep(1500);
    await p.addStyleTag({ content: '*{caret-color:transparent!important;animation-play-state:paused!important;transition:none!important}' });
    await sleep(400);
    await p.screenshot({ path: path.join(OUT, withAnswer ? 'inbox_qa.png' : 'inbox_q.png') });
    if (withAnswer) {
      const boxes = await p.evaluate((Q, A) => {
        const find = (txt) => { let best = null; for (const e of document.querySelectorAll('main *, body *')) { if ((e.textContent || '').trim().startsWith(txt.slice(0, 24)) || (e.textContent || '').includes(txt.slice(0, 40))) { const r = e.getBoundingClientRect(); if (r.width > 60 && r.width < 900 && (!best || r.width * r.height < best.width * best.height) && r.height > 30) best = r; } } return best && [best.x, best.y, best.width, best.height].map((v) => Math.round(v)); };
        const cls = (txt) => { const e = [...document.querySelectorAll('*')].filter((x) => x.children.length < 6 && (x.textContent || '').includes(txt.slice(0, 30))).sort((a, b) => a.textContent.length - b.textContent.length)[0]; const chain = []; let n = e; for (let i = 0; n && i < 4; i++, n = n.parentElement) { const r = n.getBoundingClientRect(); chain.push([n.tagName, n.className, Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]); } return chain; };
        return { q: cls(Q), a: cls(A) };
      }, Q, A);
      writeFileSync(path.join(OUT, 'inbox.json'), JSON.stringify(boxes, null, 1));
      console.log(JSON.stringify(boxes));
    }
  }
} finally { await b.close(); }
