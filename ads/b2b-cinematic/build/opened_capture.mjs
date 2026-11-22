// Film "Opened 3 Times": the real CRM of the public Lantern Trips demo (sample data, this
// browser only). One sample couple's quote is for Komodo and has been opened three times:
// the pipeline board shows "Opened 3x", Home says to call. Then the same board once they book.
// Also the cover of the itinerary they were sent, from the demo's own itinerary maker.
//   node build/opened_capture.mjs -> screens/opened/board_hot.png, home_hot.png, board_booked.png, cover.png, boxes.json
import puppeteer from 'puppeteer-core';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens/opened');
mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const TRIPS = ['Angkor at dawn', 'Komodo by phinisi', 'Luang Prabang, slow', 'Penang food trail', 'Sapa terraces'];
const KOMODO = 'https://wgzwrrrfzxdnkrfebkqb.supabase.co/storage/v1/object/public/trip-images/showcase/komodo.jpg';
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--force-color-profile=srgb'] });
const still = '*{caret-color:transparent!important;animation-play-state:paused!important;transition:none!important}';
const boxes = {};
try {
  const p = await b.newPage();
  await p.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
  await p.goto('https://wanderbuddyapp.com/trydemo/app/#/pipeline', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(3000);
  const edit = (stage) => p.evaluate((TRIPS, stage) => {
    const db = JSON.parse(localStorage.getItem('wb-demo-try'));
    if (!db.__spread) {
      const swap = (s, i) => typeof s === 'string' ? s.replace(/Krabi Islands, small group|Railay honeymoon|Phuket family|Krabi, Thailand/g, TRIPS[i % TRIPS.length]) : s;
      const walk = (o, i) => { if (Array.isArray(o)) return o.map((v) => walk(v, i)); if (o && typeof o === 'object') { for (const k of Object.keys(o)) o[k] = walk(o[k], i); return o; } return swap(o, i); };
      let n = 0; const byE = {};
      for (const e of db.tables.crm_enquiries) { byE[e.id] = n; walk(e, n++); }
      for (const t of db.tables.crm_threads) walk(t, t.enquiry_id in byE ? byE[t.enquiry_id] : n++);
      for (const t of db.tables.crm_trips) walk(t, n++);
      for (const t of db.tables.crm_tasks || []) walk(t, t.link?.enquiry in byE ? byE[t.link.enquiry] : n++);
      db.__spread = true;
    }
    const e = db.tables.crm_enquiries.find((x) => /Lukas & Sophie/.test(x.name));
    Object.assign(e, { dest: 'Komodo by phinisi', stage, value: 2240 });
    Object.assign(e.data, { quotes: 2 });
    // the CRM's own rule (router.js): a sent quote opened 2 or more times in the last 3 days is hot
    Object.assign(e, stage === 'Quote sent' ? { quote_views: 3, quote_viewed_at: new Date(Date.now() - 3600e3).toISOString() } : { quote_views: 3 });
    if (stage === 'Booked') { e.created_at = new Date().toISOString(); e.data.bookedOn = new Date().toISOString().slice(0, 10); }
    localStorage.setItem('wb-demo-try', JSON.stringify(db));
    return e.id;
  }, TRIPS, stage);
  const open = async (hash, click) => {
    await p.goto('https://wanderbuddyapp.com/trydemo/app/#/' + hash, { waitUntil: 'networkidle2' });
    await p.reload({ waitUntil: 'networkidle2' });
    await sleep(2500);
    await p.evaluate(() => { for (const x of document.querySelectorAll('button')) if (/^not now$/i.test(x.textContent.trim())) x.click(); });
    if (click) { await p.evaluate((label) => { [...document.querySelectorAll('button, a, [role=tab]')].find((e) => e.textContent.trim() === label && e.offsetParent)?.click(); }, click); await sleep(1500); }
    await p.addStyleTag({ content: still });
    await sleep(400);
  };
  const card = () => p.evaluate(() => { const e = [...document.querySelectorAll('main .col *')].filter((x) => /^Lukas & Sophie/.test((x.textContent || '').trim()) && x.getBoundingClientRect().height > 80 && x.getBoundingClientRect().height < 320).sort((a, b) => a.getBoundingClientRect().height - b.getBoundingClientRect().height)[0]; if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height), e.textContent.trim().replace(/\s+/g, ' ').slice(0, 120)]; });
  await edit('Quote sent');
  await open('pipeline', 'Board');
  await p.screenshot({ path: path.join(OUT, 'board_hot.png') });
  boxes.board_hot = await card();
  await open('home');
  boxes.home_hot = await p.evaluate(() => {
    const c = [...document.querySelectorAll('main section.card')].find((e) => /Needs you today/.test(e.textContent));
    c.scrollIntoView({ block: 'start' });
    document.scrollingElement.scrollTop -= 96;
    const row = [...c.querySelectorAll('button.row, a.row, .row')].find((e) => /Opened quote/.test(e.textContent));
    const r = (e) => { const q = e.getBoundingClientRect(); return [q.x, q.y, q.width, q.height].map((v) => Math.round(v)); };
    return row ? [...r(row), row.textContent.trim().replace(/\s+/g, ' ')] : null;
  });
  await sleep(500);
  await p.screenshot({ path: path.join(OUT, 'home_hot.png') });
  await edit('Booked');
  await open('pipeline', 'Board');
  await p.screenshot({ path: path.join(OUT, 'board_booked.png') });
  boxes.board_booked = await card();
  // the itinerary cover, portrait
  await p.setViewport({ width: 2200, height: 2000, deviceScaleFactor: 2 });
  await p.goto('https://wanderbuddyapp.com/trydemo/app/#/studio', { waitUntil: 'networkidle2' });
  await sleep(2500);
  const href = await p.evaluate(() => [...document.querySelectorAll('a.sx-cardname')].find((a) => /small group/i.test(a.textContent))?.getAttribute('href'));
  await p.goto('https://wanderbuddyapp.com/trydemo/app/' + href, { waitUntil: 'networkidle2' });
  await sleep(4000);
  await p.evaluate(() => { [...document.querySelectorAll('button, [role=tab], label')].find((e) => e.textContent.trim() === 'Portrait' && e.offsetParent)?.click(); });
  await sleep(2500);
  await p.addStyleTag({ content: '.sx .sp .ph.empty[data-p]{background:var(--tint)!important}.sx .sp .ph.empty i{display:none!important}.sx .sp [data-e]:empty::before{content:none!important}.sx .sp li.add,.sx .sp .pk-add,.sx .sp .fx-h{display:none!important}' });
  boxes.cover = await p.evaluate((KOMODO) => {
    const s = [...document.querySelectorAll('section.sp')].sort((a, b) => b.getBoundingClientRect().width - a.getBoundingClientRect().width)[0];
    s.setAttribute('data-shot', '1');
    const tw = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
    const seen = [];
    for (let n = tw.nextNode(); n; n = tw.nextNode()) { if (n.nodeValue.trim()) seen.push(n.nodeValue.trim().slice(0, 60)); n.nodeValue = n.nodeValue.replace(/KRABI ISLANDS, SMALL GROUP/g, 'KOMODO BY PHINISI').replace(/Krabi Islands,? small group|Krabi Islands/g, 'Komodo by phinisi').replace(/Five days from Ao Nang with a small group[^.]*\./, 'Four days from Labuan Bajo with a small group: Padar at sunrise, the dragons with a ranger, three nights on a wooden phinisi.').replace(/Krabi, Thailand/g, 'Komodo, Indonesia').replace(/Ao Nang, Krabi 81180, Thailand/g, 'Hang Bac, Hoan Kiem, Hanoi, Vietnam').replace(/LT-KIS-/g, 'LT-KMD-'); }
    const imgs = [...s.querySelectorAll('img, [style*="background-image"]')].map((e) => e.tagName + ':' + (e.getAttribute('src') || e.style.backgroundImage).slice(0, 80));
    for (const im of s.querySelectorAll('img')) if (/lantern\.webp|saltwater\.webp/.test(im.src)) { im.removeAttribute('srcset'); im.src = KOMODO; }
    const r = s.getBoundingClientRect();
    return { size: [Math.round(r.width), Math.round(r.height)], seen: seen.slice(0, 14), imgs: imgs.slice(0, 6) };
  }, KOMODO);
  await sleep(2500);
  await p.addStyleTag({ content: '.sample-bar,[class*=sample],.sx-tip,.sx-hint{display:none!important}' });
  const sec = await p.$('section.sp[data-shot]');
  await sec.evaluate((x) => x.scrollIntoView({ block: 'center' }));
  await sleep(500);
  await sec.screenshot({ path: path.join(OUT, 'cover.png') });
  writeFileSync(path.join(OUT, 'boxes.json'), JSON.stringify(boxes, null, 1));
  console.log(JSON.stringify(boxes, null, 1));
} finally { await b.close(); }
