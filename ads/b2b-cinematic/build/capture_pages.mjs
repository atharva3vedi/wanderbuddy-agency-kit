// The real itinerary pages of the public Lantern Trips demo (wanderbuddyapp.com/trydemo,
// sample data, no login): opens the existing "Krabi Islands, small group" itinerary and
// screenshots each page (section.sp) at 2x into screens/pages/. View only, nothing is saved.
import puppeteer from 'puppeteer-core';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens/pages');
mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const b = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new', args: ['--force-color-profile=srgb'],
});
try {
  const p = await b.newPage();
  await p.setViewport({ width: 2200, height: 1400, deviceScaleFactor: 2 });
  await p.goto('https://wanderbuddyapp.com/trydemo/app/#/studio', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2500);
  const href = await p.evaluate(() => [...document.querySelectorAll('a.sx-cardname')].find((a) => /krabi islands, small group/i.test(a.textContent))?.getAttribute('href'));
  console.log('href', href);
  await p.goto('https://wanderbuddyapp.com/trydemo/app/' + href, { waitUntil: 'networkidle2', timeout: 60000 });
  const clicked = !!href;
  console.log('clicked', clicked);
  await sleep(4500);
  const n = await p.$$eval('section.sp', (s) => s.map((x) => [x.className, Math.round(x.getBoundingClientRect().width), Math.round(x.getBoundingClientRect().height)]));
  console.log('pages', JSON.stringify(n));
  // Draw them the way the PDF prints (studio.js ctx(false)): no editor hints or add
  // buttons, and an empty photo slot as a plain brand tint instead of the editor's hatching.
  await p.addStyleTag({ content: [
    '.sx .sp .ph.empty[data-p]{background:var(--tint)!important}',
    '.sx .sp .ph.empty i{display:none!important}',
    '.sx .sp [data-e]:empty::before{content:none!important}',
    '.sx .sp li.add,.sx .sp .pk-add,.sx .sp .fx-h{display:none!important}',
  ].join('') });
  await sleep(300);
  const secs = (await p.$$('section.sp')).slice(-14);
  for (const [i, s] of secs.entries()) {
    await s.evaluate((x) => x.scrollIntoView({ block: 'center' }));
    await sleep(400);
    await s.screenshot({ path: path.join(OUT, `pg${String(i).padStart(2, '0')}.png`) });
  }
  await p.screenshot({ path: path.join(OUT, '_view.png') });
} finally {
  await b.close();
}
