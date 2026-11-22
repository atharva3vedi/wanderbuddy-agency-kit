// Real screens for the investor demo, with the Mac's own Chrome (read-only).
// CRM: the public Lantern Trips sample demo (wanderbuddyapp.com/trydemo, no login).
// Marketplace: the live /trips page, its RPCs answered with that demo's sample trip
// (as in ../../condensed-25s/build/capture.mjs), plus listing_fee answered the way
// 0227's hold_fee_quote does for a 3% agency listing, so the page draws the fee rows
// it shows for every fee listing today. Nothing is submitted.
// Usage: node capture.mjs [name ...]
import puppeteer from 'puppeteer-core';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36';
const CRM = 'https://wanderbuddyapp.com/trydemo/app/';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function settle(page) {
  await sleep(1800);
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      if (/^not now$/i.test(b.textContent.trim())) b.click();
    }
  });
  await page.addStyleTag({ content: '*{caret-color:transparent!important;animation-play-state:paused!important;transition:none!important}' });
  await sleep(500);
}

async function clickText(page, re) {
  return page.evaluate((src) => {
    const rx = new RegExp(src, 'i');
    const els = [...document.querySelectorAll('button, a, [role=button], li, tr, .row, [data-id]')];
    const el = els.find((e) => rx.test(e.textContent || '') && e.offsetParent);
    if (el) { el.click(); return el.textContent.trim().slice(0, 80); }
    return null;
  }, re.source);
}

const TRIP = '6f1d2c3a-4b5e-4f60-8a71-92b3c4d5e6f7';
const COVER = 'https://wanderbuddyapp.com/partners-media/custom/lantern.webp';
const HOST = { name: 'Lantern Trips', slug: 'lantern-trips', verified: true, trips_run: 48, hold_days: 7,
  bio: 'Small-group island trips, honeymoons and family holidays from Ao Nang, Krabi.' };
// The CRM sample's hold is for the 9 Dec departure (18 Nov and 6 more dates), so the page opens on it.
const DEPS = [['18 Nov', '2026-11-18', 5], ['25 Nov', '2026-11-25', 6], ['2 Dec', '2026-12-02', 8], ['9 Dec', '2026-12-09', 3]]
  .map(([, d, s], i) => ({ trip_id: i === 3 ? TRIP : TRIP.slice(0, -1) + i, start_date: d, seats_left: s }));
const PRICE = 690, BPS = 300;
const quote = (n) => {
  const total = PRICE * n, fee = Math.round(total * BPS) / 10000;
  return { party: n, price_total: total, currency: 'USD', bps: BPS, usd: fee, inr: null, agency_total: Math.round((total - fee) * 100) / 100, upi: false };
};
const MARKET = {
  marketplace_listings: { agency: null, packages: [{ next_trip_id: TRIP, title: 'Krabi Islands, small group', destination: 'Krabi, Thailand', days: 5,
    price_from: PRICE, seats_left: 3, banner_url: COVER, host: HOST, departures: DEPS, pay_online: false }] },
  listing_local_prices: [],
  listing_fee: { required: true, quotes: [1, 2, 3, 4, 5, 6].map(quote) },
  marketplace_listing: {
    host: HOST, departures: DEPS, me: {},
    trip: { id: TRIP, title: 'Krabi Islands, small group', destination: 'Krabi, Thailand', start_date: '2026-12-09', end_date: '2026-12-13', days: 5,
      price_from: PRICE, seats_left: 3, is_listed: true, is_full: false, pay_online: false, banner_url: COVER,
      description: 'Five days around Ao Nang with a group of up to twelve. The Hong Islands by longtail, a lagoon swim at Railay, two hotels our team uses every week.',
      inclusions: ['Four nights in two hotels', 'Longtail day to the Hong Islands', 'Airport pickup and drop', 'A local host on every day'] },
    days: [{ date: '2026-12-09', activity: 'Arrive, sunset at Ao Nang' }, { date: '2026-12-10', activity: 'Hong Islands by longtail' },
      { date: '2026-12-11', activity: 'Railay and Phra Nang Cave Beach' }],
  },
};
async function fakeMarket(page) {
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const m = req.url().match(/\/rest\/v1\/rpc\/([a-z_]+)/);
    if (m && m[1] in MARKET && req.method() === 'OPTIONS') {
      return req.respond({ status: 204, headers: { 'access-control-allow-origin': '*', 'access-control-allow-headers': 'apikey, content-type, authorization, x-client-info', 'access-control-allow-methods': 'POST, OPTIONS' } });
    }
    if (m && m[1] in MARKET) {
      return req.respond({ status: 200, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: JSON.stringify(MARKET[m[1]]) });
    }
    req.continue();
  });
}

// Two travellers, her number, name and note typed in (the same as the CRM sample's hold), as she would before paying the fee.
async function fillHold(p) {
  await p.evaluate(() => {
    const f = document.getElementById('bookForm');
    if (!f) return;
    const set = (n, v) => { const el = f.elements[n]; if (el) { el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); } };
    set('party', '2');
    set('phone', '+420 603 118 274');
    set('note', 'Can we add a night on Railay after the trip?');
    set('name', 'Hana Novak');
  });
  await sleep(400);
}

const SHOTS = {
  listings: { url: CRM + '#/listings' },
  inbox: { url: CRM + '#/inbox' },
  inboxHold: { url: CRM + '#/inbox', after: async (p) => { console.log('clicked', await clickText(p, /Hana/)); await sleep(1400); } },
  itinerary: { url: CRM + '#/itineraries', after: async (p) => { console.log('clicked', await clickText(p, /Krabi Islands/)); await sleep(1600); } },
  marketPhoneFull: { url: 'https://wanderbuddyapp.com/trips/' + TRIP, vw: 430, vh: 932, dpr: 3, before: fakeMarket, full: true,
    after: async (p) => {
      await fillHold(p);
      await p.addStyleTag({ content: '.mbar{display:none!important}' });
      console.log('offsets', JSON.stringify(await p.evaluate(() => Object.fromEntries(
        [['hero', '.lhero'], ['title', 'h1'], ['dates', '.dates'], ['book', '#book'], ['form', '#bookForm'], ['split', '#split'], ['btn', '#bookBtn'], ['height', 'body']]
          .map(([k, s]) => [k, k === 'height' ? document.documentElement.scrollHeight : Math.round(document.querySelector(s)?.getBoundingClientRect().top + scrollY)])))));
      console.log('split', await p.evaluate(() => document.getElementById('split')?.innerText));
    } },
  marketPhoneBar: { url: 'https://wanderbuddyapp.com/trips/' + TRIP, vw: 430, vh: 932, dpr: 3, before: fakeMarket, el: '.mbar' },
};

const want = process.argv.slice(2);
const names = want.length ? want : Object.keys(SHOTS);
const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
try {
  for (const name of names) {
    const s = SHOTS[name];
    const page = await browser.newPage();
    await page.setUserAgent(UA);
    await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }, { name: 'prefers-reduced-motion', value: 'reduce' }]);
    await page.setViewport({ width: s.vw || 1600, height: s.vh || 1000, deviceScaleFactor: s.dpr || 2, isMobile: !!s.dpr, hasTouch: !!s.dpr });
    if (s.before) await s.before(page);
    await page.goto(s.url, { waitUntil: 'networkidle2', timeout: 60000 });
    await settle(page);
    if (s.after) { await s.after(page); await settle(page); }
    const file = path.join(OUT, `${name}.png`);
    if (s.el) await (await page.$(s.el)).screenshot({ path: file });
    else await page.screenshot({ path: file, fullPage: !!s.full });
    console.log('saved', file, await page.title());
    await page.close();
  }
} finally {
  await browser.close();
}
