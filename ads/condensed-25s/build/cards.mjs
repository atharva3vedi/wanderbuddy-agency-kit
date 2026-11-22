// Renders every [data-shot] in cards.html to ../cards/<id>.png on a
// transparent background (2x). Usage: node cards.mjs [id ...]
import puppeteer from 'puppeteer-core';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { readFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '../cards');
const ROOT = path.resolve(HERE, '../../../..');
mkdirSync(OUT, { recursive: true });

// The end card's lockup: the real logo with the tile left out (the glyph sits
// on the azure card the way the old end card had it) and the word in white.
const dark = readFileSync(path.join(ROOT, 'website/public/brand/logo-on-dark.svg'), 'utf8')
  .replace(/<!--[\s\S]*?-->/g, '')
  .replace('<rect width="1024" height="1024" rx="200" fill="#2072B8"/>', '')
  .replace(/fill="#E7F1FA"/g, 'fill="#FFFFFF"');
const endLogo = 'data:image/svg+xml;base64,' + Buffer.from(dark).toString('base64');

const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new', args: ['--allow-file-access-from-files', '--force-color-profile=srgb'],
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 2400, height: 1600, deviceScaleFactor: 2 });
  await page.goto(pathToFileURL(path.join(HERE, 'cards.html')).href, { waitUntil: 'networkidle0' });
  await page.evaluate((src) => {
    const w = document.getElementById('word');
    w.src = src;
    w.style.height = '200px';
    w.previousElementSibling.remove(); // the glyph is inside the lockup already
  }, endLogo);
  await page.evaluate(() => document.fonts.ready);
  await new Promise((r) => setTimeout(r, 400));
  const want = process.argv.slice(2);
  const els = await page.$$('[data-shot]');
  for (const el of els) {
    const id = await el.evaluate((e) => e.dataset.shot);
    if (want.length && !want.includes(id)) continue;
    await el.screenshot({ path: path.join(OUT, `${id}.png`), omitBackground: true });
  }
  console.log('rendered', els.length, 'shots to', OUT);
} finally {
  await browser.close();
}
