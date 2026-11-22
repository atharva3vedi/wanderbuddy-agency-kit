// Film "Three Agencies", second cut: the screens that make the story true.
//  1. The real /trips listing page on a phone, drawing a Lantern Trips sample
//     departure (Ha Giang Loop) in place of the live RPC answers, as
//     condensed-25s/build/capture.mjs does for Krabi. Top of the page, and the
//     hold form with two travellers filled in (never submitted).
//  2. The real CRM inbox of the public demo with one of its own held-spot
//     threads given the Ha Giang trip, in this browser's copy of the sample data.
//   node build/agencies_capture2.mjs [probe]
import puppeteer from 'puppeteer-core';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens/agencies');
mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36';
const TRIP = '6f1d2c3a-4b5e-4f60-8a71-92b3c4d5e6f7';
const COVER = 'https://wgzwrrrfzxdnkrfebkqb.supabase.co/storage/v1/object/public/trip-images/showcase/hagiang.jpg';
const HOST = { name: 'Lantern Trips', slug: 'lantern-trips', verified: true, trips_run: 48, hold_days: 7,
  bio: 'Small-group trips in northern Vietnam from Hanoi: Ha Giang, Sapa, Ninh Binh.' };
const DEPS = [['2026-11-16', 3], ['2026-11-23', 6], ['2026-11-30', 8], ['2026-12-07', 10]]
  .map(([d, s], i) => ({ trip_id: i ? TRIP.slice(0, -1) + i : TRIP, start_date: d, seats_left: s }));
const T = { id: TRIP, title: 'Ha Giang Loop, small group', destination: 'Ha Giang, Vietnam', start_date: '2026-11-16', end_date: '2026-11-20', days: 5,
  price_from: 390, seats_left: 3, is_listed: true, is_full: false, pay_online: false, banner_url: COVER,
  description: 'Five days on the Ha Giang Loop with local easy riders doing the driving: Ma Pi Leng Pass, the Nho Que river by boat, three homestays. Photo: Khánh Hmoong, CC BY 2.0, Wikimedia Commons.',
  inclusions: ['Four nights in homestays', 'An easy rider and bike for each traveller', 'The Nho Que river boat', 'Bus from Hanoi and back'] };
const MARKET = {
  marketplace_listings: { agency: null, packages: [{ next_trip_id: TRIP, title: T.title, destination: T.destination, days: 5,
    price_from: 390, seats_left: 3, banner_url: COVER, host: HOST, departures: DEPS, pay_online: false }] },
  listing_local_prices: [],
  marketplace_listing: { host: HOST, departures: DEPS, me: {}, trip: T,
    days: [{ date: '2026-11-16', activity: 'Hanoi to Ha Giang town' }, { date: '2026-11-17', activity: 'Quan Ba pass to Yen Minh' },
      { date: '2026-11-18', activity: 'Ma Pi Leng Pass and the Nho Que river' }] },
};
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
const still = '*{caret-color:transparent!important;animation-play-state:paused!important;transition:none!important}';
try {
  // --- 1. the listing, on a phone ---------------------------------------------
  const p = await b.newPage();
  await p.setUserAgent(UA);
  await p.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }, { name: 'prefers-reduced-motion', value: 'reduce' }]);
  await p.setViewport({ width: 430, height: 932, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
  await p.setRequestInterception(true);
  p.on('request', (req) => {
    const m = req.url().match(/\/rest\/v1\/rpc\/([a-z_]+)/);
    if (m && m[1] in MARKET && req.method() === 'OPTIONS') return req.respond({ status: 204, headers: { 'access-control-allow-origin': '*', 'access-control-allow-headers': 'apikey, content-type, authorization, x-client-info', 'access-control-allow-methods': 'POST, OPTIONS' } });
    if (m && m[1] in MARKET) return req.respond({ status: 200, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: JSON.stringify(MARKET[m[1]]) });
    req.continue();
  });
  await p.goto('https://wanderbuddyapp.com/trips/' + TRIP, { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2500);
  await p.addStyleTag({ content: still });
  await sleep(400);
  await p.screenshot({ path: path.join(OUT, 'listing_top.png') });
  // the hold form: two travellers, a sample name. Filled in, never sent.
  await p.evaluate(() => document.getElementById('book')?.scrollIntoView({ block: 'start' }));
  await sleep(600);
  const fields = await p.evaluate(() => [...document.querySelectorAll('#book input, #book select, #book textarea, #bookForm input, #bookForm select, #bookForm textarea')].map((e) => [e.tagName, e.type, e.name, e.id, e.placeholder]));
  console.log('fields', JSON.stringify(fields));
  await p.evaluate(() => {
    const set = (el, v) => { if (!el) return; el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };
    const root = document.getElementById('bookForm') || document.getElementById('book');
    set(root.querySelector('select'), '2');
    const ins = [...root.querySelectorAll('input')];
    set(ins.find((i) => i.type === 'tel' || /whats|phone/i.test(i.name + i.id + i.placeholder)), '+420 601 234 567');
    set(ins.find((i) => /name/i.test(i.name + i.id) && i.type !== 'email'), 'Hana Novak');
    set(root.querySelector('textarea'), 'Two of us, one twin room please.');
  });
  await sleep(500);
  await p.evaluate(() => { const btn = [...document.querySelectorAll('#book button, #bookForm button')].find((x) => /hold my spot/i.test(x.textContent)); btn?.scrollIntoView({ block: 'center' }); });
  await sleep(600);
  await p.screenshot({ path: path.join(OUT, 'listing_hold.png') });
  const lb = await p.evaluate(() => {
    const r = (e) => { if (!e) return null; const q = e.getBoundingClientRect(); return [q.x, q.y, q.width, q.height].map((v) => Math.round(v)); };
    const btn = [...document.querySelectorAll('#book button, #bookForm button')].find((x) => /hold my spot/i.test(x.textContent));
    return { button: r(btn), text: document.getElementById('book')?.innerText.slice(0, 700) };
  });
  console.log('hold', JSON.stringify(lb));
  await p.close();

  // --- 2. the CRM inbox: the held spots arriving --------------------------------
  const c = await b.newPage();
  await c.emulateTimezone('Asia/Ho_Chi_Minh');
  await c.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
  await c.evaluateOnNewDocument((t) => {
    const RealDate = Date; const off = t - RealDate.now();
    // eslint-disable-next-line no-global-assign
    Date = class extends RealDate { constructor(...a) { if (a.length) super(...a); else super(RealDate.now() + off); } static now() { return RealDate.now() + off; } };
  }, Date.parse('2026-11-11T16:50:00.000Z'));               // Wed 11 Nov, 23:50 in Hanoi
  await c.goto('https://wanderbuddyapp.com/trydemo/app/#/inbox', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(3000);
  const info = await c.evaluate(() => {
    const db = JSON.parse(localStorage.getItem('wb-demo-try'));
    const AT = '2026-11-11T16:49:00.000Z';
    const th = db.tables.crm_threads.find((t) => t.data?.via === 'hold' && /Novak/.test(t.who));
    const cut = (o) => JSON.parse(JSON.stringify(o, (k, v) => typeof v === 'string' && v.length > 400 ? v.slice(0, 400) + '…' : v));
    const before = { th: cut(th), msgs: cut(db.tables.crm_messages.filter((m) => m.thread_id === th.id)), hold: cut((db.tables.dev_holds || []).find((h) => h.id === th.data.hold_id)),
      trip: cut((() => { const t = db.tables.crm_trips.find((x) => x.id === th.trip_id); return t && { id: t.id, dest: t.dest, ref: t.ref, start_on: t.start_on, end_on: t.end_on, name: t.name, wb_trip_id: t.wb_trip_id }; })()) };
    for (const m of db.tables.crm_messages.filter((x) => x.thread_id === th.id)) {
      if (m.extra?.hold_id) m.body = 'Held 2 spots on Ha Giang Loop, small group, 16 Nov 2026. Note: Two of us, one twin room please.';
      Object.assign(m, { created_at: AT, updated_at: AT, last_at: AT });
    }
    Object.assign(th, { last_at: AT, unread: true });
    const trip = db.tables.crm_trips.find((x) => x.id === th.trip_id);
    if (trip) Object.assign(trip, { name: 'Ha Giang Loop, small group', dest: 'Ha Giang, Vietnam', ref: 'HGL-261116', start_on: '2026-11-16', end_on: '2026-11-20' });
    const hold = (db.tables.dev_holds || []).find((h) => h.id === th.data.hold_id);
    if (hold) for (const k of Object.keys(hold)) if (typeof hold[k] === 'string') hold[k] = hold[k].replace(/Krabi Islands, small group/g, 'Ha Giang Loop, small group');
    localStorage.setItem('wb-demo-try', JSON.stringify(db));
    return { who: th.who, before };
  });
  if (process.argv[2] === 'probe') console.log(JSON.stringify(info.before, null, 1).slice(0, 5000));
  await c.reload({ waitUntil: 'networkidle2' });
  await sleep(2500);
  await c.evaluate(() => { for (const x of document.querySelectorAll('button')) if (/^not now$/i.test(x.textContent.trim())) x.click(); });
  await c.evaluate((who) => { [...document.querySelectorAll('button, a, [role=button], li, .row, [data-id]')].find((e) => (e.textContent || '').includes(who) && e.offsetParent)?.click(); }, info.who);
  await sleep(1500);
  await c.addStyleTag({ content: still });
  await sleep(400);
  await c.screenshot({ path: path.join(OUT, 'inbox_hold.png') });
  const boxes = await c.evaluate(() => [...document.querySelectorAll('.bubbles > *, .bubble, .convo header, .convo .head')].map((e) => { const r = e.getBoundingClientRect(); return [e.tagName, e.className, Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height), (e.textContent || '').trim().slice(0, 90)]; }));
  writeFileSync(path.join(OUT, 'inbox_hold.json'), JSON.stringify(boxes, null, 1));
  console.log('boxes', JSON.stringify(boxes));
} finally { await b.close(); }
