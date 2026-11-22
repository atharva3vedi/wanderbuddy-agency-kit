// Builds the "6 apps you can delete" carousel as self-contained HTML slides,
// one file per slide per variant. Navy+amber Mission Control system, hex
// reconciled to lib/theme/app_colors.dart (dark tokens). No CDN, no fonts to
// install: uses Windows system fonts so headless Edge renders it as-is.
//
//   node build.mjs           -> build/ig/*.html (1080x1350) + build/li/*.html (1080x1080)
// Then render with render.ps1.

import { mkdirSync, writeFileSync } from 'node:fs';

// --- tokens (SoT: app_colors.dart dark) ---
const NAVY_TOP = '#17293B';   // surface
const NAVY_BOT = '#0B141F';   // bgPage
const AMBER    = '#F0A431';   // accent
const ON_AMBER = '#3A2606';
const TEXT     = '#E7F1FA';
const MUTED    = '#8DA7BC';
const CHIP_BG  = '#12202E';
const CHIP_BD  = '#25394C';

// white peaks + wave, tight viewBox lifted from assets/icon-master.svg
const MARK = `<svg class="mark" viewBox="210 210 610 500" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <polygon points="224,512 404,296 494,422 602,224 800,512" fill="#fff"/>
  <path d="M 217 620 Q 290 584 364 620 T 512 620 T 660 620 T 807 620 L 807 692 L 217 692 Z" fill="#fff"/>
</svg>`;

// amber-wrap helper: turns [['a'],['b','amber'],['c']] into html
const rich = parts => parts.map(([t, cls]) => cls === 'amber'
  ? `<span class="amber">${t}</span>` : t).join('');

const slides = [
  { id: 's1', kind: 'cover',
    kicker: 'WANDERBUDDY',
    title: [['6 apps you can '], ['delete', 'amber'], [' before your next group trip']],
    sub: 'Your group chat is quietly doing the job of six apps. Badly.' },

  { id: 's2', kind: 'app', n: 1, chip: 'Splitwise',
    line: [['Every cost splits as you go and '], ['settles', 'amber'],
           [' in everyone\'s own currency. Nobody sends the awkward money text three weeks later.']] },

  { id: 's3', kind: 'app', n: 2, chip: 'the 247-message group chat',
    line: [['The plan, the map, the money and the chat live in '], ['one place', 'amber'],
           ['. The chat stops being where decisions go to die.']] },

  { id: 's4', kind: 'app', n: 3, chip: '40 saved pins only you can see',
    line: [['One '], ['shared', 'amber'],
           [' map: everyone\'s pins, the day\'s plan, and where each other actually is, live.']] },

  { id: 's5', kind: 'app', n: 4, chip: 'the itinerary trapped in a Google Sheet',
    line: [['Say "5 days, Bangkok, cheap, hot, walkable." Get a '], ['real', 'amber'],
           [' itinerary the whole group can edit, not a tab nobody opens.']] },

  { id: 's6', kind: 'app', n: 5, chip: 'Google Translate at the dinner table',
    line: [['Everyone speaks their '], ['own language', 'amber'],
           [' into the voice room. Nobody has to switch to English.']] },

  { id: 's7', kind: 'app', n: 6, chip: 'the when2meet nobody filled in',
    line: [['Throw out some dates, everyone '], ['votes', 'amber'],
           [', and the trip picks itself.']] },

  { id: 's8', kind: 'payoff',
    title: [['That is six apps. '], ['One', 'amber'], [' trip. One app.']],
    tagline: 'Book first, figure it out together.',
    cta: 'WanderBuddy. Link in bio.' },
];

const css = (w, h) => `
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:${w}px; height:${h}px; overflow:hidden; background:${NAVY_BOT}; }
  body {
    background: radial-gradient(130% 110% at 50% 26%, ${NAVY_TOP} 0%, ${NAVY_BOT} 68%);
    color:${TEXT}; font-family:'Segoe UI', Arial, Helvetica, sans-serif;
    -webkit-font-smoothing:antialiased;
    display:flex; flex-direction:column; justify-content:center;
    padding:96px 92px 150px;
  }
  .amber { color:${AMBER}; }
  .kicker { font-size:28px; letter-spacing:.32em; color:${MUTED}; font-weight:700; margin-bottom:34px; }
  .title { font-size:92px; line-height:1.04; font-weight:800; letter-spacing:-.5px; }
  .sub { font-size:40px; line-height:1.28; color:${MUTED}; margin-top:40px; max-width:900px; }
  .counter { font-size:30px; font-weight:800; letter-spacing:.18em; color:${AMBER}; margin-bottom:40px; }
  .delete { font-size:30px; font-weight:700; letter-spacing:.22em; color:${MUTED}; margin-bottom:22px; }
  .chip {
    display:inline-block; background:${CHIP_BG}; border:2px solid ${CHIP_BD};
    border-radius:20px; padding:20px 30px; font-size:48px; font-weight:700; color:${MUTED};
    text-decoration:line-through; text-decoration-color:${AMBER}; text-decoration-thickness:5px;
  }
  .arrow { font-size:56px; color:${AMBER}; margin:30px 0 26px; line-height:1; }
  .line { font-size:52px; line-height:1.24; font-weight:600; max-width:920px; }
  .tagline { font-size:46px; color:${MUTED}; margin-top:36px; }
  .cta { font-size:36px; font-weight:800; color:${AMBER}; margin-top:44px; }
  .lockup {
    position:absolute; left:92px; bottom:70px; display:flex; align-items:center; gap:16px; opacity:.92;
  }
  .mark { height:48px; width:auto; }
  .wordmark { font-size:34px; font-weight:800; letter-spacing:.2px; }
`;

const body = s => {
  if (s.kind === 'cover')
    return `<div class="kicker">${s.kicker}</div>
      <h1 class="title">${rich(s.title)}</h1>
      <p class="sub">${s.sub}</p>`;
  if (s.kind === 'payoff')
    return `<h1 class="title">${rich(s.title)}</h1>
      <p class="tagline">${s.tagline}</p>
      <p class="cta">${s.cta}</p>`;
  // app
  return `<div class="counter">DELETE 0${s.n} / 06</div>
    <div class="delete">DELETE</div>
    <div><span class="chip">${s.chip}</span></div>
    <div class="arrow">&#8595;</div>
    <p class="line">${rich(s.line)}</p>`;
};

const page = (s, w, h) => `<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>${s.id}</title><style>${css(w, h)}</style></head>
<body>${body(s)}<div class="lockup">${MARK}<span class="wordmark">WanderBuddy</span></div></body></html>`;

const variants = { ig: [1080, 1350], li: [1080, 1080] };
for (const [name, [w, h]] of Object.entries(variants)) {
  mkdirSync(`build/${name}`, { recursive: true });
  for (const s of slides) writeFileSync(`build/${name}/${s.id}.html`, page(s, w, h));
}
console.log('built', slides.length, 'slides x', Object.keys(variants).length, 'variants');
