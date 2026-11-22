// Captures real product screens for the 25 s ad with the Mac's own Chrome.
// CRM: the public Lantern Trips demo (wanderbuddyapp.com/trydemo, no login,
// sample data). Marketplace: the live /trips page.
// Usage: node capture.mjs [name ...]   (no names = all shots)
import puppeteer from 'puppeteer-core';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36';
const CRM = 'https://wanderbuddyapp.com/trydemo/app/';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Close the first-visit tour and keep the page still for the shot.
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
    if (el) { el.click(); return true; }
    return false;
  }, re.source);
}

// The marketplace with the demo's own sample trip (Lantern Trips, Krabi Islands
// small group, $690, from CRM/demos/try/profile.js) answered in place of the
// live RPCs, so the real page renders a listing instead of "No trips yet".
const TRIP = '6f1d2c3a-4b5e-4f60-8a71-92b3c4d5e6f7';
const COVER = 'https://wanderbuddyapp.com/partners-media/custom/lantern.webp';
const HOST = { name: 'Lantern Trips', slug: 'lantern-trips', verified: true, trips_run: 48, hold_days: 7,
  bio: 'Small-group island trips, honeymoons and family holidays from Ao Nang, Krabi.' };
const DEPS = [['16 Nov', '2026-11-16', 3], ['23 Nov', '2026-11-23', 5], ['30 Nov', '2026-11-30', 8], ['7 Dec', '2026-12-07', 9]]
  .map(([, d, s], i) => ({ trip_id: i ? TRIP.slice(0, -1) + i : TRIP, start_date: d, seats_left: s }));
const MARKET = {
  marketplace_listings: { agency: null, packages: [{ next_trip_id: TRIP, title: 'Krabi Islands, small group', destination: 'Krabi, Thailand', days: 5,
    price_from: 690, seats_left: 3, banner_url: COVER, host: HOST, departures: DEPS, pay_online: false }] },
  listing_local_prices: [],
  marketplace_listing: {
    host: HOST, departures: DEPS, me: {},
    trip: { id: TRIP, title: 'Krabi Islands, small group', destination: 'Krabi, Thailand', start_date: '2026-11-16', end_date: '2026-11-20', days: 5,
      price_from: 690, seats_left: 3, is_listed: true, is_full: false, pay_online: false, banner_url: COVER,
      description: 'Five days around Ao Nang with a group of up to twelve. The Hong Islands by longtail, a lagoon swim at Railay, two hotels our team uses every week.',
      inclusions: ['Four nights in two hotels', 'Longtail day to the Hong Islands', 'Airport pickup and drop', 'A local host on every day'] },
    days: [{ date: '2026-11-16', activity: 'Arrive, sunset at Ao Nang' }, { date: '2026-11-17', activity: 'Hong Islands by longtail' },
      { date: '2026-11-18', activity: 'Railay and Phra Nang Cave Beach' }],
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

const SHOTS = {
  home: { url: CRM + '#/home' },
  inbox: { url: CRM + '#/inbox' },
  inboxThread: { url: CRM + '#/inbox', after: async (p) => { await clickText(p, /Chloe/); await sleep(1200); } },
  trips: { url: CRM + '#/trips' },
  pipeline: { url: CRM + '#/pipeline' },
  customers: { url: CRM + '#/customers' },
  listings: { url: CRM + '#/listings' },
  studio: { url: CRM + '#/studio' },
  channels: { url: CRM + '#/channels' },
  market: { url: 'https://wanderbuddyapp.com/trips', vw: 1600, vh: 1000, before: fakeMarket },
  marketTrip: { url: 'https://wanderbuddyapp.com/trips/' + TRIP, vw: 1600, vh: 1000, before: fakeMarket },
  marketPhone: { url: 'https://wanderbuddyapp.com/trips/' + TRIP, vw: 430, vh: 932, dpr: 3, before: fakeMarket },
  // The phone in the ad scrolls this page; the sticky price bar is its own layer.
  marketPhoneFull: { url: 'https://wanderbuddyapp.com/trips/' + TRIP, vw: 430, vh: 932, dpr: 3, before: fakeMarket, full: true,
    after: async (p) => {
      await p.addStyleTag({ content: '.mbar{display:none!important}' });
      // Where the scroll should land, in CSS px from the top (x3 in the PNG).
      console.log('offsets', JSON.stringify(await p.evaluate(() => Object.fromEntries(
        [['hero', '.lhero'], ['title', 'h1'], ['dates', '.dates'], ['book', '#book'], ['form', '#bookForm'], ['height', 'body']]
          .map(([k, s]) => [k, k === 'height' ? document.documentElement.scrollHeight : Math.round(document.querySelector(s)?.getBoundingClientRect().top + scrollY)])))));
    } },
  marketPhoneBar: { url: 'https://wanderbuddyapp.com/trips/' + TRIP, vw: 430, vh: 932, dpr: 3, before: fakeMarket, el: '.mbar' },
  marketPhoneBook: { url: 'https://wanderbuddyapp.com/trips/' + TRIP + '#book', vw: 430, vh: 932, dpr: 3, before: fakeMarket,
    after: async (p) => { await p.evaluate(() => document.getElementById('book')?.scrollIntoView({ block: 'start' })); await sleep(600); } },
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
    await page.setViewport({ width: s.vw || 1600, height: s.vh || 1000, deviceScaleFactor: s.dpr || 1.5, isMobile: !!s.dpr, hasTouch: !!s.dpr });
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
