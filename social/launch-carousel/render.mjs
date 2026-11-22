// Renders each carousel slide to a 1080x1350 JPG via headless Chrome.
// Run: node marketing/launch-carousel/render.mjs   (build.mjs must have run first)
import { createRequire } from 'node:module';
import { readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const require = createRequire(import.meta.url);
const sharp = require('C:/Users/PC/Videos/WanderBuddy/website/node_modules/sharp');

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const DIR = 'C:/Users/PC/Videos/WanderBuddy/marketing/launch-carousel';
const SCRATCH = 'C:/Users/PC/AppData/Local/Temp/claude/C--Users-PC-Videos-WanderBuddy/a1a40e29-ce00-48e5-bcc8-70c4f1736a09/scratchpad/carousel-render';
const OUT = `${DIR}/jpg`;

const html = readFileSync(`${DIR}/carousel.html`, 'utf8');
const head = html.slice(0, html.indexOf('<div class="page-head"')); // title + font links + <style>

// Pull one balanced <div class="slide" ...> … </div> out of the built page.
function sliceSlide(id) {
  const start = html.indexOf(`<div class="slide" id="${id}"`);
  if (start < 0) throw new Error(`slide ${id} not found`);
  const re = /<div\b|<\/div>/g; re.lastIndex = start;
  let depth = 0, m;
  while ((m = re.exec(html))) {
    if (m[0][1] === '/') { if (--depth === 0) return html.slice(start, m.index + 6); }
    else depth++;
  }
  throw new Error(`slide ${id} unbalanced`);
}

const OVERRIDE = `<style>
  html,body{margin:0;padding:0;width:1080px;height:1350px;overflow:hidden;background:#080f17;}
  .slide{width:1080px!important;height:1350px!important;aspect-ratio:auto!important;border-radius:0!important;box-shadow:none!important;}
  .live .pulse{animation:none!important;}
</style>`;

rmSync(SCRATCH, { recursive: true, force: true });
mkdirSync(SCRATCH, { recursive: true });
mkdirSync(OUT, { recursive: true });

const ids = ['s1', 's2', 's3', 's4', 's5'];
console.log('Rendering slides:');
for (let i = 0; i < ids.length; i++) {
  const n = String(i + 1).padStart(2, '0');
  const page = `<!doctype html><html><head>${head}${OVERRIDE}</head><body>${sliceSlide(ids[i])}</body></html>`;
  const pageFile = `${SCRATCH}/slide-${n}.html`;
  const pngFile = `${SCRATCH}/slide-${n}.png`;
  writeFileSync(pageFile, page);
  execFileSync(CHROME, [
    '--headless=new', '--disable-gpu', '--hide-scrollbars',
    '--force-device-scale-factor=1', '--window-size=1080,1350',
    '--virtual-time-budget=12000', '--run-all-compositor-stages-before-draw',
    `--user-data-dir=${SCRATCH}/profile`,
    `--screenshot=${pngFile}`, `file:///${pageFile}`,
  ], { stdio: 'ignore' });
  const jpg = `${OUT}/slide-${n}.jpg`;
  const meta = await sharp(pngFile).jpeg({ quality: 92 }).toFile(jpg);
  console.log(`  slide-${n}.jpg  ${meta.width}x${meta.height}  ${(meta.size / 1024).toFixed(0)} KB`);
}
console.log(`\n  wrote ${ids.length} JPGs to ${OUT}`);
