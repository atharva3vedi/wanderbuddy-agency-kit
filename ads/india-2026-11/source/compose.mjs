// Type layer over each Blender render: one headline, the WanderBuddy logo, and the photo credit.
// Writes one HTML page per ad and size, then a jobs file for capture.mjs (exact pixel size, DPR 1).
import fs from 'node:fs';
const R = 'E:/render/india-ads';
const FONT = 'file:///C:/Users/PC/Videos/WanderBuddy/website/public/fonts/InstrumentSerif-Regular.ttf';
const INTER = 'file:///C:/Users/PC/Videos/WanderBuddy/website/public/fonts/Inter-Regular.ttf';
const LOGO_DARK = 'file:///C:/Users/PC/Videos/WanderBuddy/website/public/brand/logo-on-dark.svg';
const LOGO_LIGHT = 'file:///C:/Users/PC/Videos/WanderBuddy/website/public/brand/logo.svg';
const ADS = [
  { id: 'root-bridge', bg: 'root-bridge', head: 'Walk across a bridge of living roots.', credit: 'Photo: Arijit Sahu, CC BY-SA 4.0', tone: 'dark' },
  { id: 'umngot', bg: 'umngot', head: 'A river so clear you can see the stones.', credit: 'Photo: Diablo0769, CC BY-SA 4.0', tone: 'dark' },
  { id: 'mizoram', bg: 'mizoram', head: 'Mizoram, off the usual list.', credit: 'Photo: Suaktawta, CC BY-SA 4.0', tone: 'dark' },
  { id: 'taj', bg: 'taj', head: 'Agra, Mathura and Vrindavan, planned by locals.', credit: 'Photo: Shagil Kannur, CC BY-SA 3.0', tone: 'dark' },
  { id: 'finder-a', bg: 'finder', head: 'Type your trip. Meet the agency that runs it.', credit: '', tone: 'light' },
  { id: 'finder-b', bg: 'finder', head: 'Find your ideal travel agency today.', credit: '', tone: 'light' },
];
const SIZES = { '45': { w: 1080, h: 1350, top: 72, fs: 96, maxw: 900, logoBottom: 56 }, '916': { w: 1080, h: 1920, top: 250, fs: 104, maxw: 940, logoBottom: 330 } };
fs.mkdirSync(`${R}/html`, { recursive: true }); fs.mkdirSync(`${R}/final`, { recursive: true });
const jobs = [];
for (const ad of ADS) for (const [k, s] of Object.entries(SIZES)) {
  const dark = ad.tone === 'dark';
  const ink = dark ? '#FFFFFF' : '#0C1622';
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:IS;src:url('${FONT}')}
@font-face{font-family:IN;src:url('${INTER}')}
html,body{margin:0;padding:0;width:${s.w}px;height:${s.h}px;overflow:hidden}
.f{position:relative;width:${s.w}px;height:${s.h}px;background:url('file:///${R}/renders/${ad.bg}-${k}.png') center/cover no-repeat}
.top{position:absolute;inset:0 0 auto 0;height:${Math.round(s.h * (k === '45' ? 0.48 : 0.42))}px;background:${dark ? 'linear-gradient(to bottom,rgba(4,10,18,.62) 0%,rgba(4,10,18,.34) 45%,rgba(4,10,18,0) 100%)' : 'none'}}
.bot{position:absolute;inset:auto 0 0 0;height:${Math.round(s.h * 0.30)}px;background:${dark ? 'linear-gradient(to top,rgba(4,10,18,.55) 0%,rgba(4,10,18,0) 100%)' : 'none'}}
h1{position:absolute;left:64px;top:${s.top}px;margin:0;max-width:${s.maxw}px;font:400 ${s.fs}px/1.02 IS,serif;letter-spacing:-.012em;color:${ink};${dark ? 'text-shadow:0 2px 28px rgba(0,0,0,.35)' : ''}}
.logo{position:absolute;left:64px;bottom:${s.logoBottom}px;height:48px}
.cr{position:absolute;right:40px;bottom:${s.logoBottom + 14}px;font:400 19px/1 IN,sans-serif;color:#fff}
</style></head><body><div class="f"><div class="top"></div><div class="bot"></div>
<h1>${ad.head}</h1><img class="logo" src="${dark ? LOGO_DARK : LOGO_LIGHT}">${ad.credit ? `<div class="cr">${ad.credit}</div>` : ''}</div></body></html>`;
  const file = `${R}/html/${ad.id}-${k}.html`; fs.writeFileSync(file, html);
  jobs.push({ name: `${ad.id}-${k}`, url: 'file:///' + file, w: s.w, h: s.h, dpr: 1, mobile: false, wait: 1500 });
}
fs.writeFileSync(`${R}/scripts/jobs-compose.json`, JSON.stringify(jobs));
console.log(jobs.length, 'pages');
