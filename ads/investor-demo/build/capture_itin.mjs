// The Krabi Islands itinerary from the public Lantern Trips demo (wanderbuddyapp.com/trydemo,
// sample data, no login), with its empty photo slots filled: the demo's itinerary only has
// two photos set, so the editor draws the rest as hatched "Cover photo" placeholders and
// the PDF as plain tint circles. Each empty slot gets a different crop of the demo's own
// two site photos (partners-media/custom/lantern.webp, saltwater.webp), the way it looks
// once an agency adds its photos. View only, nothing is saved.
//   node build/capture_itin.mjs -> screens/itinerary.png (the editor, 3200 x 2000)
//                                  screens/pages/pg00-05.png (the pages as the PDF prints)
import puppeteer from 'puppeteer-core';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SCR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens');
mkdirSync(path.join(SCR, 'pages'), { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const BASE = 'https://wanderbuddyapp.com/trydemo/app/';

async function openItin(p) {
  await p.goto(BASE + '#/studio', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2500);
  const href = await p.evaluate(() => [...document.querySelectorAll('a.sx-cardname')].find((a) => /krabi islands, small group/i.test(a.textContent))?.getAttribute('href'));
  await p.goto(BASE + href, { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(4000);
  await p.evaluate(() => { for (const b of document.querySelectorAll('button')) if (/^not now$/i.test(b.textContent.trim())) b.click(); });
  await sleep(500);
}

async function fillPhotos(p) {
  const n = await p.evaluate(() => {
    const photos = ['https://wanderbuddyapp.com/partners-media/custom/lantern.webp', 'https://wanderbuddyapp.com/partners-media/custom/saltwater.webp'];
    const crops = [['30% 45%', 1.0], ['80% 55%', 1.5], ['15% 30%', 1.8], ['60% 75%', 1.3], ['90% 25%', 1.6], ['45% 60%', 2.0]];
    let k = 0;
    for (const el of document.querySelectorAll('.ph.empty')) {
      const [pos, zoom] = crops[k % crops.length];
      el.classList.remove('empty');
      el.innerHTML = `<img src="${photos[(k + (k >> 2)) % 2]}" style="width:100%;height:100%;object-fit:cover;object-position:${pos};transform:scale(${zoom});transform-origin:${pos};display:block;border-radius:inherit">`;
      el.style.overflow = 'hidden';
      k++;
    }
    return k;
  });
  await p.evaluate(() => Promise.all([...document.images].map((i) => i.decode().catch(() => null))));
  await sleep(600);
  return n;
}

const b = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new', args: ['--force-color-profile=srgb', '--hide-scrollbars'],
});
try {
  // the editor, as the laptop shows it
  let p = await b.newPage();
  await p.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }, { name: 'prefers-reduced-motion', value: 'reduce' }]);
  await p.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
  await openItin(p);
  console.log('editor slots filled', await fillPhotos(p));
  await p.addStyleTag({ content: '*{caret-color:transparent!important;transition:none!important}' });
  await p.screenshot({ path: path.join(SCR, 'itinerary.png') });
  await p.close();

  // the pages, drawn the way the PDF prints (as ../b2b-cinematic/build/capture_pages.mjs)
  p = await b.newPage();
  await p.setViewport({ width: 2200, height: 1400, deviceScaleFactor: 2 });
  await openItin(p);
  await p.addStyleTag({ content: [
    '.sx .sp .ph.empty[data-p]{background:var(--tint)!important}',
    '.sx .sp .ph.empty i{display:none!important}',
    '.sx .sp [data-e]:empty::before{content:none!important}',
    '.sx .sp li.add,.sx .sp .pk-add,.sx .sp .fx-h{display:none!important}',
  ].join('') });
  console.log('page slots filled', await fillPhotos(p));
  const secs = (await p.$$('section.sp')).slice(-14).slice(0, 6);
  for (const [i, s] of secs.entries()) {
    await s.evaluate((x) => x.scrollIntoView({ block: 'center' }));
    await sleep(400);
    await s.screenshot({ path: path.join(SCR, 'pages', `pg${String(i).padStart(2, '0')}.png`) });
  }
  console.log('pages', secs.length);
} finally {
  await b.close();
}
