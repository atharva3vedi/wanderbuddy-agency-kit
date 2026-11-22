// Renders transparent 1080x1920 text overlays in the reels' own styles (headline, big word, caption pill).
//   node overlay.mjs list.json outdir     list = [{ "name": "c00", "kind": "head|free|cc", "text": "..." }]
import { createRequire } from 'node:module';
import { readFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const puppeteer = createRequire('C:/Users/PC/Videos/WanderBuddy/store/graphics/appstore/build/')('puppeteer-core');
const [list, outdir] = [JSON.parse(readFileSync(process.argv[2], 'utf8')), process.argv[3]];
mkdirSync(outdir, { recursive: true });
const chrome = path.join(os.homedir(), '.cache/puppeteer/chrome/win64-152.0.7977.42/chrome-win64/chrome.exe');
const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ['--force-color-profile=srgb', '--disable-lcd-text', '--font-render-hinting=none'],
  defaultViewport: { width: 1080, height: 1920, deviceScaleFactor: 1 } });
const page = await browser.newPage();
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
// same type as reel.html: .head, #free, #cc span
await page.setContent(`<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@800;900&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;background:transparent;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.head{position:absolute;left:70px;right:70px;top:250px;text-align:center;font-weight:900;font-size:104px;line-height:1.02;letter-spacing:-.035em;color:#fff;text-shadow:0 10px 50px rgba(0,0,0,.55),0 2px 12px rgba(0,0,0,.5)}
.free{position:absolute;left:0;right:0;top:760px;text-align:center;font-size:300px;font-weight:900;letter-spacing:-.06em;color:#fff;text-shadow:0 20px 80px rgba(0,0,0,.6)}
.cc{position:absolute;left:0;right:0;bottom:300px;text-align:center}
.cc span{display:inline-block;max-width:940px;font-size:54px;font-weight:800;letter-spacing:-.015em;line-height:1.18;color:#fff;padding:10px 28px 14px;border-radius:18px;background:rgba(5,10,16,.62)}
</style></head><body><div id="o"></div></body></html>`, { waitUntil: 'networkidle0' });
await page.evaluate(() => document.fonts.ready);
for (const it of list) {
  // a newline in the text breaks the line; "size" overrides the font size
  const tx = esc(it.text).replace(/\n/g, '<br>'), st = it.size ? ` style="font-size:${it.size}px"` : '';
  const h = it.kind === 'cc' ? `<div class="cc"><span>${tx}</span></div>` : `<div class="${it.kind}"${st}>${tx}</div>`;
  await page.evaluate(h => { document.getElementById('o').innerHTML = h; }, h);
  await page.screenshot({ path: path.join(outdir, it.name + '.png'), omitBackground: true });
}
await browser.close();
console.log('overlays', list.length);
