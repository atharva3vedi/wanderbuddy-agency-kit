// Screenshots overlay.html at 24 fps into ../render/overlay/####.png (transparent).
// Usage: node overlay.mjs [first last] | node overlay.mjs --stills t,t,...
import puppeteer from 'puppeteer-core';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { mkdirSync } from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FPS = 24, DUR = 119, LAST = DUR * FPS - 1;
const args = process.argv.slice(2);
const stills = args[0] === '--stills' ? args[1].split(',').map(Number) : null;
const OUT = path.resolve(HERE, '../render', stills ? 'overlay_stills' : 'overlay');
mkdirSync(OUT, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new', args: ['--allow-file-access-from-files', '--force-color-profile=srgb', '--font-render-hinting=none'],
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(HERE, 'overlay.html')).href, { waitUntil: 'networkidle0' });
  await page.evaluate(() => window.__ready);
  const frames = stills ? stills.map((t) => Math.round(t * FPS)) : [];
  if (!stills) {
    const [a, b] = args.length >= 2 ? args.map(Number) : [0, LAST];
    for (let f = a; f <= b; f++) frames.push(f);
  }
  for (const f of frames) {
    await page.evaluate((t) => window.__seek(t), f / FPS);
    const name = stills ? `t_${(f / FPS).toFixed(2)}.png` : `${String(f).padStart(4, '0')}.png`;
    await page.screenshot({ path: path.join(OUT, name), omitBackground: true });
  }
  console.log('overlay frames:', frames.length, '->', OUT);
} finally {
  await browser.close();
}
