// Renders cards.html (#1..#4) to out/card-N.png at 2x (2160x2700) with headless Chrome.
// Run: node marketing/linkedin-reply-race/render.mjs [n]
import { execFileSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const out = join(here, 'out');
mkdirSync(out, { recursive: true });
const only = process.argv[2];
for (const n of only ? [only] : ['1', '2', '3', '4']) {
  const url = `${pathToFileURL(join(here, 'cards.html')).href}#${n}`;
  execFileSync(CHROME, [
    '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
    '--force-device-scale-factor=2', '--window-size=1080,1350', '--virtual-time-budget=3000',
    `--screenshot=${join(out, `card-${n}.png`)}`, url,
  ], { stdio: 'pipe' });
  console.log(`card-${n}.png`);
}

// The LinkedIn carousel is a PDF, one card a page: out/reply-race-carousel.pdf.
if (!only) {
  const { writeFileSync } = await import('node:fs');
  const pages = ['1', '2', '3', '4'].map((n) => `<img src="card-${n}.png">`).join('');
  writeFileSync(join(out, 'carousel.html'), `<!doctype html><meta charset="utf-8"><style>@page{size:1080px 1350px;margin:0}html,body{margin:0}img{display:block;width:1080px;height:1350px;break-after:page}</style>${pages}`);
  execFileSync(CHROME, ['--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--no-pdf-header-footer',
    `--print-to-pdf=${join(out, 'reply-race-carousel.pdf')}`, pathToFileURL(join(out, 'carousel.html')).href], { stdio: 'pipe' });
  console.log('reply-race-carousel.pdf');
}
