// Renders reel.html frame by frame (1080x1920, 30 fps).
//   node render.mjs r2 --stills 1.2,5.5     -> stills/r2_1.20.jpg
//   node render.mjs r2 --out r2_silent.mp4   (also writes r2_sfx.json, the page's sound cues)
//   node render.mjs r2 --out ../reel1/insert_card.mp4 --from 6.3 --to 10.8 --cc 0   (a silent piece, no captions)
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import os from 'node:os';

const here = path.dirname(fileURLToPath(import.meta.url));
const puppeteer = createRequire('C:/Users/PC/Videos/WanderBuddy/store/graphics/appstore/build/')('puppeteer-core');
const reel = process.argv[2];
const args = Object.fromEntries(process.argv.slice(3).reduce((a, v, i, arr) => {
  if (v.startsWith('--')) a.push([v.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]);
  return a;
}, []));
const chrome = path.join(os.homedir(), '.cache/puppeteer/chrome/win64-152.0.7977.42/chrome-win64/chrome.exe');
const browser = await puppeteer.launch({
  executablePath: chrome, headless: true,
  args: ['--allow-file-access-from-files', '--force-color-profile=srgb', '--hide-scrollbars', '--disable-lcd-text', '--font-render-hinting=none'],
  defaultViewport: { width: 1080, height: 1920, deviceScaleFactor: 1 },
});
const page = await browser.newPage();
page.on('console', m => { if (m.type() === 'error') console.log('[page]', m.text()); });
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.goto(pathToFileURL(path.join(here, 'reel.html')).href + '?reel=' + reel + (args.cc === '0' ? '&cc=0' : ''), { waitUntil: 'networkidle0' });
await page.waitForFunction('window.__ready === true', { timeout: 60000 });
const seek = t => page.evaluate(t => window.__seek(t), t);
writeFileSync(path.join(here, 'audio', reel + '_sfx.json'), JSON.stringify(await page.evaluate(() => ({ sfx: window.SFX, duration: window.__dur, cues: window.TL.cues })), null, 1));

if (args.stills) {
  const dir = path.join(here, 'stills'); mkdirSync(dir, { recursive: true });
  for (const ts of String(args.stills).split(',')) {
    const t = +ts; await seek(t); await seek(t);
    const f = path.join(dir, `${reel}_${t.toFixed(2)}.jpg`);
    await page.screenshot({ path: f, type: 'jpeg', quality: 85 });
    console.log(f);
  }
} else if (args.out) {
  const dur = await page.evaluate(() => window.__dur), fps = 30;
  const out = path.join(here, args.out);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n0 = Math.round(+(args.from || 0) * fps), n1 = Math.round(+(args.to || dur) * fps), t0 = Date.now();
  for (let n = n0; n < n1; n++) {
    await seek(n / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (n % 90 === 0) console.log(`frame ${n}/${n1} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('wrote', out);
}
await browser.close();
