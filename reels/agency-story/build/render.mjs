// Renders reel.html over footage.mp4 (1080x1920, 30 fps).
//   node render.mjs --stills 1.2,5.5   -> stills/<t>.jpg (page over the footage frame)
//   node render.mjs --out silent.mp4   (also writes audio/s1_sfx.json, the page's sound cues)
import { createRequire } from 'node:module';
import { spawn, spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import os from 'node:os';

const here = path.dirname(fileURLToPath(import.meta.url));
const puppeteer = createRequire('C:/Users/PC/Videos/WanderBuddy/store/graphics/appstore/build/')('puppeteer-core');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => {
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
await page.goto(pathToFileURL(path.join(here, 'reel.html')).href + (args.cc === '0' ? '?cc=0' : ''), { waitUntil: 'networkidle0' });
await page.waitForFunction('window.__ready === true', { timeout: 60000 });
const seek = t => page.evaluate(t => window.__seek(t), t);
const shot = () => page.screenshot({ type: 'png', omitBackground: true });
writeFileSync(path.join(here, 'audio', 's1_sfx.json'), JSON.stringify(await page.evaluate(() => ({ sfx: window.SFX, duration: window.__dur })), null, 1));
const footage = path.join(here, 'footage.mp4');

if (args.stills) {
  const dir = path.join(here, 'stills'); mkdirSync(dir, { recursive: true });
  for (const ts of String(args.stills).split(',')) {
    const t = +ts; await seek(t);
    const ov = path.join(dir, `_ov.png`); writeFileSync(ov, await shot());
    const f = path.join(dir, `${t.toFixed(2)}.jpg`);
    spawnSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(t), '-i', footage, '-i', ov, '-filter_complex', '[0:v][1:v]overlay=0:0', '-frames:v', '1', '-q:v', '3', f]);
    console.log(f);
  }
} else if (args.out) {
  const dur = await page.evaluate(() => window.__dur), fps = 30, N = Math.round(dur * fps);
  const out = path.join(here, args.out);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-i', footage, '-f', 'image2pipe', '-vcodec', 'png', '-framerate', String(fps), '-i', '-',
    '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p', '-frames:v', String(N),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let n = 0; n < N; n++) {
    await seek(n / fps);
    const buf = await shot();
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (n % 150 === 0) console.log(`frame ${n}/${N} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('wrote', out);
}
await browser.close();
