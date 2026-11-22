// Builds the self-contained carousel: redacts the Bangkok report, normalizes
// every photo, and inlines them as data URIs into carousel.html.
// Run: node marketing/launch-carousel/build.mjs
import { createRequire } from 'node:module';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const require = createRequire(import.meta.url);
const sharp = require('C:/Users/PC/Videos/WanderBuddy/website/node_modules/sharp');

const DIR = 'C:/Users/PC/Videos/WanderBuddy/marketing/launch-carousel';
const P = (f) => `${DIR}/photos/${f}`;

// token -> source file (relative to /photos)
const MAP = {
  note1:      'WhatsApp Image 2026-08-26 at 00.02.03.jpeg',
  note2:      'WhatsApp Image 2026-08-26 at 00.02.03 (1).jpeg',
  note3:      'WhatsApp Image 2026-08-26 at 00.02.03 (2).jpeg',
  'rej-google':  'Screenshot 2026-07-22 184219.png',
  'rej-apple1':  'Screenshot 2026-08-07 021244.png',
  'rej-apple2':  'Screenshot 2026-08-12 230251.png',
  chat:       'Screenshot 2026-08-26 002837.png',
  mac:        'Screenshot 2026-08-21 050859.png',
  approved:   'Screenshot 2026-08-24 233255.png',
};
const BANGKOK_SRC = 'WhatsApp Image 2026-08-26 at 00.02.40 (1).jpeg'; // report-in-hand, street

async function encode(file) {
  const ext = path.extname(file).toLowerCase();
  const s = sharp(P(file)).rotate().resize({ width: 1120, height: 1120, fit: 'inside', withoutEnlargement: true });
  if (ext === '.png') return { mime: 'image/png', buf: await s.png({ compressionLevel: 9 }).toBuffer() };
  return { mime: 'image/jpeg', buf: await s.jpeg({ quality: 86 }).toBuffer() };
}

async function redactBangkok() {
  const norm = await sharp(P(BANGKOK_SRC)).rotate()
    .resize({ width: 1200, height: 1200, fit: 'inside', withoutEnlargement: true }).toBuffer();
  const { width: W, height: H } = await sharp(norm).metadata();
  // Generous cover of the held document (all PII lives here).
  const left = Math.round(W * 0.06), top = Math.round(H * 0.34);
  const w = Math.min(Math.round(W * 0.88), W - left), h = Math.min(Math.round(H * 0.54), H - top);
  const region = await sharp(norm).extract({ left, top, width: w, height: h }).blur(26).toBuffer();
  const out = await sharp(norm).composite([{ input: region, left, top }]).jpeg({ quality: 82 }).toBuffer();
  writeFileSync(`${DIR}/photos/s5-bangkok-redacted.jpg`, out); // audit copy
  return { mime: 'image/jpeg', buf: out };
}

const dataURI = (mime, buf) => `data:${mime};base64,${buf.toString('base64')}`;

(async () => {
  let html = readFileSync(`${DIR}/carousel.src.html`, 'utf8');
  let total = 0;
  const put = (token, mime, buf) => {
    total += buf.length;
    const uri = dataURI(mime, buf);
    const needle = `data-photo="${token}"`;
    if (!html.includes(needle)) throw new Error(`token not found in template: ${token}`);
    html = html.split(needle).join(`src="${uri}"`);
    console.log(`  ${token.padEnd(12)} ${(buf.length / 1024).toFixed(0).padStart(4)} KB`);
  };

  console.log('Encoding photos:');
  for (const [token, file] of Object.entries(MAP)) {
    const { mime, buf } = await encode(file);
    put(token, mime, buf);
  }
  const bk = await redactBangkok();
  put('bangkok', bk.mime, bk.buf);

  // guard: every placeholder consumed
  const leftover = html.match(/data-photo="[^"]+"/g);
  if (leftover) throw new Error(`unfilled placeholders: ${leftover.join(', ')}`);

  writeFileSync(`${DIR}/carousel.html`, html);
  console.log(`\n  images total ${(total / 1024).toFixed(0)} KB  ·  html ${(html.length / 1024).toFixed(0)} KB`);
  console.log('  wrote carousel.html');

  // ---- Print variant: strip the web chrome, keep only the 5 slides ----
  const printHtml = html
    .replace(/<div class="page-head">[\s\S]*?<\/div>\s*/, '')
    .replace(/<div class="chrome">[\s\S]*?<\/div>\s*/g, '')
    .replace(/<div class="note">[\s\S]*?<\/div>\s*/, '');
  mkdirSync(`${DIR}/print`, { recursive: true });
  writeFileSync(`${DIR}/print/carousel-print.html`, printHtml);
  writeFileSync(`${DIR}/print/README.md`, README);
  console.log('  wrote print/carousel-print.html + README.md');
})().catch((e) => { console.error('BUILD FAILED:', e.message); process.exit(1); });

const README = `# Print → PDF (LinkedIn carousel)

\`carousel-print.html\` is the launch carousel with the web chrome removed — just
the five slides, all images embedded, ready to export as a PDF carousel.

## Export (use Chrome)
1. Open \`carousel-print.html\` in Chrome.
2. Ctrl + P.
3. Destination: **Save as PDF**.
4. **Margins: None**  ·  **Scale: 100 (Default)**  ·  Layout: Portrait.
5. More settings → **Background graphics: ON** (so the dark slides render).
6. Save → a 5-page PDF, each page 1080 × 1350 (4:5).

## Post to LinkedIn
New post → **Add a document** → upload the PDF → give it a title → post.
LinkedIn shows the pages as a swipeable carousel.

Regenerate after edits: \`node ../build.mjs\`
`;
