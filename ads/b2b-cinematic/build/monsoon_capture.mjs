// Film "Monsoon": the real CRM of the public Lantern Trips demo (sample data, kept in this
// browser only), with its sample enquiries spread over five trips in five countries instead
// of three in Krabi. Pipeline board, Pipeline "Action now", and Home.
//   node build/monsoon_capture.mjs -> screens/monsoon/board.png, action.png, home.png, boxes.json
import puppeteer from 'puppeteer-core';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens/monsoon');
mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const TRIPS = ['Angkor at dawn', 'Komodo by phinisi', 'Luang Prabang, slow', 'Penang food trail', 'Sapa terraces'];
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--force-color-profile=srgb'] });
const still = '*{caret-color:transparent!important;animation-play-state:paused!important;transition:none!important}';
try {
  const p = await b.newPage();
  await p.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
  await p.goto('https://wanderbuddyapp.com/trydemo/app/#/pipeline', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(3000);
  await p.evaluate((TRIPS) => {
    const db = JSON.parse(localStorage.getItem('wb-demo-try'));
    const swap = (s, i) => typeof s === 'string' ? s.replace(/Krabi Islands, small group|Railay honeymoon|Phuket family|Krabi, Thailand/g, TRIPS[i % TRIPS.length]) : s;
    const walk = (o, i) => { if (Array.isArray(o)) return o.map((v) => walk(v, i)); if (o && typeof o === 'object') { for (const k of Object.keys(o)) o[k] = walk(o[k], i); return o; } return swap(o, i); };
    let n = 0;
    const byE = {};
    for (const e of db.tables.crm_enquiries) { byE[e.id] = n; walk(e, n++); }
    for (const t of db.tables.crm_threads) walk(t, t.enquiry_id in byE ? byE[t.enquiry_id] : n++);
    for (const t of db.tables.crm_trips) walk(t, n++);
    for (const t of db.tables.crm_tasks || []) walk(t, t.link?.enquiry in byE ? byE[t.link.enquiry] : n++);
    for (const m of db.tables.crm_messages) walk(m, n++);
    localStorage.setItem('wb-demo-try', JSON.stringify(db));
  }, TRIPS);
  const boxes = {};
  const shoot = async (hash, name, click) => {
    await p.goto('https://wanderbuddyapp.com/trydemo/app/#/' + hash, { waitUntil: 'networkidle2' });
    await p.reload({ waitUntil: 'networkidle2' });
    await sleep(2500);
    await p.evaluate(() => { for (const x of document.querySelectorAll('button')) if (/^not now$/i.test(x.textContent.trim())) x.click(); });
    if (click) { await p.evaluate((label) => { [...document.querySelectorAll('button, a, [role=tab]')].find((e) => e.textContent.trim() === label && e.offsetParent)?.click(); }, click); await sleep(1500); }
    await p.addStyleTag({ content: still + '.sample-bar,.samplebar{display:none!important}' });
    await sleep(400);
    await p.screenshot({ path: path.join(OUT, name + '.png') });
    boxes[name] = await p.evaluate(() => [...document.querySelectorAll('main h1, main h2, main h3, main section, main .card, main .col, main [class*=col], main [class*=lane], main li, main tr')].slice(0, 80).map((e) => { const r = e.getBoundingClientRect(); return [e.tagName, String(e.className).slice(0, 30), Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height), (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60)]; }).filter((x) => x[4] > 40 && x[3] < 1000 && x[3] >= 0));
  };
  await shoot('pipeline', 'action');
  await shoot('pipeline', 'board', 'Board');
  await shoot('home', 'home');
  // Home again, scrolled so "Needs you today" sits near the top of the screen.
  const row = await p.evaluate(() => {
    const card = [...document.querySelectorAll('main section.card')].find((e) => /Needs you today/.test(e.textContent));
    card.scrollIntoView({ block: 'start' });
    const sc = [document.scrollingElement, ...document.querySelectorAll('main, .main, .content')].find((e) => e && e.scrollTop > 0) || document.scrollingElement;
    sc.scrollTop -= 96;
    const r = (e) => { const q = e.getBoundingClientRect(); return [q.x, q.y, q.width, q.height].map((v) => Math.round(v)); };
    const first = [...card.querySelectorAll('li, .row, a, div')].find((e) => /^\s*Erik Lindqvist/.test(e.textContent) && e.getBoundingClientRect().height < 110 && e.getBoundingClientRect().width > 500);
    return { card: r(card), erik: first ? r(first) : null, scroller: sc.tagName + '.' + sc.className };
  });
  await sleep(500);
  await p.screenshot({ path: path.join(OUT, 'home_needs.png') });
  boxes.home_needs = row;
  console.log('home_needs', JSON.stringify(row));
  writeFileSync(path.join(OUT, 'boxes.json'), JSON.stringify(boxes, null, 1));
  console.log('ok', Object.keys(boxes).map((k) => k + ':' + boxes[k].length).join(' '));
} finally { await b.close(); }
