// Film "The Reel": the real CRM of the public Lantern Trips demo (sample data, this browser only).
//  1. A sample Instagram conversation with a reel is added to this browser's copy of the data and
//     the real "Turn into a proposal" is pressed on it. In the demo the reading and writing are done
//     by its built-in stand-in for the model: the steps and the layout are real, the timing is not,
//     so the panel's clock and its "Ready in N seconds" line are hidden before the screenshot.
//  2. Home, with the row the CRM shows when a traveller picks an option on the plan and taps Book.
//  3. The inbox on the trip: the pickup question and the assistant's answer from the trip plan.
//   node build/reel_capture.mjs -> screens/reel/thread.png, proposal_run.png, proposal_done.png,
//                                  home_book.png, inbox_q.png, inbox_qa.png, boxes.json
import puppeteer from 'puppeteer-core';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens/reel');
mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const APP = 'https://wanderbuddyapp.com/trydemo/app/';
const TRIPS = ['Ha Giang Loop, small group', 'Ninh Binh by boat', 'Sapa terraces', 'Hoi An, slow', 'Ha Long Bay'];
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--force-color-profile=srgb'] });
const still = '*{caret-color:transparent!important}.toast,.toasts,[class*=toast]{display:none!important}';
const boxes = {};
const rect = (sel) => `(() => { const e = ${sel}; if (!e) return null; const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(Math.round); })()`;
async function fresh(nowIso) {
  const p = await b.newPage();
  await p.emulateTimezone('Asia/Ho_Chi_Minh');
  await p.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
  await p.evaluateOnNewDocument((t) => {
    const RealDate = Date; const off = t - RealDate.now();
    // eslint-disable-next-line no-global-assign
    Date = class extends RealDate { constructor(...a) { if (a.length) super(...a); else super(RealDate.now() + off); } static now() { return RealDate.now() + off; } };
  }, Date.parse(nowIso));
  return p;
}
const settle = async (p) => { await sleep(2500); await p.evaluate(() => { for (const x of document.querySelectorAll('button')) if (/^not now$/i.test(x.textContent.trim())) x.click(); }); await p.addStyleTag({ content: still }); await sleep(400); };
const openThread = (p, who, hint) => p.evaluate((who, hint) => { [...document.querySelectorAll('button, a, [role=button], li, .row, [data-id]')].find((e) => (e.textContent || '').includes(who) && (!hint || (e.textContent || '').includes(hint)) && e.offsetParent)?.click(); }, who, hint);
try {
  // --- 1. the reel, and the proposal ------------------------------------------------
  let p = await fresh('2026-11-11T16:41:00.000Z');               // Wed 11 Nov, 23:41 in Hanoi
  await p.goto(APP + '#/inbox', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(3000);
  await p.evaluate((TRIPS) => {
    const db = JSON.parse(localStorage.getItem('wb-demo-try'));
    const swap = (s, i) => typeof s === 'string' ? s.replace(/Krabi Islands, small group|Railay honeymoon|Phuket family|Krabi, Thailand/g, TRIPS[i % TRIPS.length]) : s;
    const walk = (o, i) => { if (Array.isArray(o)) return o.map((v) => walk(v, i)); if (o && typeof o === 'object') { for (const k of Object.keys(o)) o[k] = walk(o[k], i); return o; } return swap(o, i); };
    let n = 0; const byE = {};
    for (const e of db.tables.crm_enquiries) { byE[e.id] = n; walk(e, n++); }
    for (const t of db.tables.crm_threads) walk(t, t.enquiry_id in byE ? byE[t.enquiry_id] : n++);
    for (const t of db.tables.crm_trips) walk(t, n++);
    for (const t of db.tables.crm_tasks || []) walk(t, n++);
    for (const m of db.tables.crm_messages) walk(m, n++);
    const at = (s) => new Date(Date.parse('2026-11-11T16:40:00.000Z') + s * 1000).toISOString();
    const pid = db.tables.crm_threads[0].partner_id;
    const id = crypto.randomUUID();
    db.tables.crm_threads.push({ id, partner_id: pid, channel: 'Instagram DM', external_id: '17841400099', who: 'Mia Novak', unread: true, last_at: at(20), data: { via: 'channel' }, is_sample: true, created_at: at(0), updated_at: at(20) });
    const msg = (s, body) => ({ id: crypto.randomUUID(), partner_id: pid, thread_id: id, kind: 'in', body, via: 'channel', extra: {}, created_at: at(s), updated_at: at(s), last_at: at(s), is_sample: true });
    db.tables.crm_messages.push(msg(0, '[Shared a reel] https://www.instagram.com/reel/DCx7haGiang/ The Ha Giang loop in Vietnam with easy riders: Ma Pi Leng Pass, the Nho Que river, homestays'));
    db.tables.crm_messages.push(msg(20, 'Could you do this for 4 of us in January? 5 nights. We are friends from Prague.'));
    localStorage.setItem('wb-demo-try', JSON.stringify(db));
  }, TRIPS);
  await p.reload({ waitUntil: 'networkidle2' });
  await settle(p);
  await openThread(p, 'Mia Novak');
  await sleep(1500);
  await p.screenshot({ path: path.join(OUT, 'thread.png') });
  const BTN = "[...document.querySelectorAll('button')].find((x) => /Turn into a proposal/.test(x.textContent) && x.offsetParent)";
  boxes.thread = { button: await p.evaluate(rect(BTN)), strip: await p.evaluate(rect(`(${BTN})?.parentElement`)), bubbles: await p.evaluate(rect("document.querySelector('.bubbles')")) };
  await p.evaluate(`(${BTN})?.click()`);
  await sleep(1300);
  await p.addStyleTag({ content: '.pr-clock{visibility:hidden!important}' });
  await p.screenshot({ path: path.join(OUT, 'proposal_run.png') });
  for (let i = 0; i < 40; i++) { await sleep(1000); if (await p.evaluate(() => !document.querySelector('.pr-steps li.doing') && !!document.querySelector('.pr-out')?.innerText.trim())) break; }
  await sleep(800);
  await p.evaluate(() => { for (const e of document.querySelectorAll('body *')) if (/^\s*New enquiry:/.test(e.textContent) && getComputedStyle(e).position === 'fixed') e.style.display = 'none'; });
  await p.evaluate(() => { for (const e of document.querySelectorAll('.pr-out *')) if (/^\s*Ready in \d+ seconds?\s*$/.test(e.textContent) && e.children.length <= 1) e.style.display = 'none'; });
  await sleep(300);
  await p.screenshot({ path: path.join(OUT, 'proposal_done.png') });
  boxes.proposal = { drawer: await p.evaluate(rect("document.querySelector('.pr-body')?.closest('aside, .drawer, [class*=drawer]')")), steps: await p.evaluate(rect("document.querySelector('.pr-steps')")), out: await p.evaluate(rect("document.querySelector('.pr-out')")),
    text: await p.evaluate(() => document.querySelector('.pr-body')?.innerText.replace(/\s+/g, ' ').slice(0, 700)) };
  // --- 2. Home: she picked an option and tapped Book -----------------------------------
  await p.evaluate(() => {
    const db = JSON.parse(localStorage.getItem('wb-demo-try'));
    const th = db.tables.crm_threads.find((t) => /tapped Book/.test(t.data?.suggestion || ''));
    th.who = 'Mia Novak';
    th.data.suggestion = 'Mia picked Option B and tapped Book. Send the deposit link: 30% is $1,037.';
    th.last_at = new Date(Date.now() - 4 * 60000).toISOString();
    localStorage.setItem('wb-demo-try', JSON.stringify(db));
  });
  await p.goto(APP + '#/home', { waitUntil: 'networkidle2' });
  await p.reload({ waitUntil: 'networkidle2' });
  await settle(p);
  boxes.home = await p.evaluate(() => {
    const c = [...document.querySelectorAll('main section.card')].find((e) => /Needs you today/.test(e.textContent));
    c.scrollIntoView({ block: 'start' });
    document.scrollingElement.scrollTop -= 96;
    const row = [...c.querySelectorAll('.row')].find((e) => /tapped Book/.test(e.textContent));
    const r = (e) => { const q = e.getBoundingClientRect(); return [q.x, q.y, q.width, q.height].map((v) => Math.round(v)); };
    return { card: r(c), row: row ? r(row) : null, text: row?.textContent.trim().replace(/\s+/g, ' ') };
  });
  await sleep(500);
  await p.screenshot({ path: path.join(OUT, 'home_book.png') });
  await p.close();
  // --- 3. on the trip, 23:47 ---------------------------------------------------------------
  p = await fresh('2027-01-14T16:49:00.000Z');                  // Thu 14 Jan 2027, 23:49 in Hanoi
  await p.goto(APP + '#/inbox', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2500);
  const Q = 'What time is pickup tomorrow?';
  const A = 'Pickup is at 06:30 from the Lantern House lobby in Ha Giang town. It is the Ma Pi Leng Pass day: bring a rain jacket and VND 150,000 in cash for the Nho Que boat, it is not included.';
  for (const withAnswer of [true, false]) {
    await p.evaluate((Q, A, withAnswer) => {
      const db = JSON.parse(localStorage.getItem('wb-demo-try'));
      const Q_AT = '2027-01-14T16:47:00.000Z', A_AT = '2027-01-14T16:48:00.000Z';
      const th = db.tables.crm_threads.find((t) => t.data?.via === 'concierge' && (/Grace/.test(t.who) || t.data.film));
      th.who = 'Mia Novak'; th.data.film = true;
      const mine = db.tables.crm_messages.filter((m) => m.thread_id === th.id).sort((a, b) => a.created_at.localeCompare(b.created_at));
      const q = mine.find((m) => m.kind === 'in'), a = mine.find((m) => m.kind === 'bot') || { ...q, id: crypto.randomUUID(), kind: 'bot', extra: {} };
      Object.assign(q, { body: Q, created_at: Q_AT, updated_at: Q_AT, last_at: Q_AT });
      Object.assign(a, { body: A, created_at: A_AT, updated_at: A_AT, last_at: A_AT });
      db.tables.crm_messages = db.tables.crm_messages.filter((m) => m.thread_id !== th.id).concat(withAnswer ? [q, a] : [q]);
      Object.assign(th, { last_at: withAnswer ? A_AT : Q_AT, unread: false });
      const trip = db.tables.crm_trips.find((t) => t.id === th.trip_id);
      Object.assign(trip, { name: 'Mia Novak', dest: 'Ha Giang Loop, small group', ref: 'TR-HGL-270112-MIA', start_on: '2027-01-12', end_on: '2027-01-17', value: 3445 });
      Object.assign(trip.data, { short: 'Mia +3', pax: 4, party: '4 friends', joined: 4, whatsapp: 4 });
      for (const s of trip.data.schedule || []) s.paid = true;
      localStorage.setItem('wb-demo-try', JSON.stringify(db));
    }, Q, A, withAnswer);
    await p.reload({ waitUntil: 'networkidle2' });
    await settle(p);
    await openThread(p, 'Mia Novak', withAnswer ? 'Pickup' : 'What time');
    await sleep(1500);
    await p.screenshot({ path: path.join(OUT, withAnswer ? 'inbox_qa.png' : 'inbox_q.png') });
    if (withAnswer) boxes.inbox = { q: await p.evaluate(rect("document.querySelector('.bubble.in')")), a: await p.evaluate(rect("document.querySelector('.bubble.bot')")), head: await p.evaluate(() => document.querySelector('.convo header')?.innerText.replace(/\s+/g, ' ')) };
  }
  writeFileSync(path.join(OUT, 'boxes.json'), JSON.stringify(boxes, null, 1));
  console.log(JSON.stringify(boxes, null, 1));
} finally { await b.close(); }
