// Screenshots overlay.html at 30 fps into ../render/v30_<fmt>/overlay/####.png
// (transparent). 16:9 by default, 9:16 with --916.
// Usage: node overlay.mjs [--916] [first last] | node overlay.mjs [--916] --stills t,t,...
import puppeteer from 'puppeteer-core';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { mkdirSync } from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FPS = 30, LAST = 30 * FPS;
let args = process.argv.slice(2);
const portrait = args.includes('--916');
args = args.filter((a) => a !== '--916');
const fmt = portrait ? '916' : '169';
const stills = args[0] === '--stills' ? args[1].split(',').map(Number) : null;
const OUT = path.resolve(HERE, `../render/v30_${fmt}`, stills ? 'overlay_stills' : 'overlay');
mkdirSync(OUT, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new', args: ['--allow-file-access-from-files', '--force-color-profile=srgb', '--font-render-hinting=none'],
});
try {
  const page = await browser.newPage();
  await page.setViewport(portrait ? { width: 1080, height: 1920, deviceScaleFactor: 1 } : { width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(HERE, 'overlay.html')).href + (portrait ? '?f=916' : ''), { waitUntil: 'networkidle0' });
  await page.evaluate(() => window.__ready);
  const frames = stills ? stills.map((t) => Math.round(t * FPS) + 1) : [];
  if (!stills) {
    const [a, b] = args.length >= 2 ? args.map(Number) : [1, LAST];
    for (let f = a; f <= b; f++) frames.push(f);
  }
  for (const f of frames) {
    await page.evaluate((t) => window.__seek(t), (f - 1) / FPS);
    const name = stills ? `t_${((f - 1) / FPS).toFixed(2)}.png` : `${String(f).padStart(4, '0')}.png`;
    await page.screenshot({ path: path.join(OUT, name), omitBackground: true });
  }
  console.log('overlay frames:', frames.length, '->', OUT);
} finally {
  await browser.close();
}
