// Renders the bad-*.html mockups to 1290x2796 PNGs (same size as the new UI captures).
// Run from repo root: node marketing/Reels/power-of-haircut/bad/render.mjs
import { createRequire } from 'module';
import { readdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(join(here, '../../../../store/graphics/appstore/build/package.json'));
const puppeteer = require('puppeteer-core');

const browser = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--hide-scrollbars'] });
const page = await browser.newPage();
await page.setViewport({ width: 430, height: 932, deviceScaleFactor: 3 });
for (const f of readdirSync(here).filter((f) => f.endsWith('.html'))) {
  await page.goto(pathToFileURL(join(here, f)).href);
  const out = join(here, '..', 'broken', f.replace('.html', '.png'));
  await page.screenshot({ path: out });
  console.log('wrote', out);
}
await browser.close();
