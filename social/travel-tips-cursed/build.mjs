// WanderBuddy "12 travel tips from a man who will not survive them".
//
// The cursed sibling of ../travel-tips-carousel. Same brand furniture, same layout
// engine, deliberately wrong contents. The arc is the joke:
//
//   01      cover, sets up that the narrator is doomed
//   02-05   confident, authoritative, insane travel advice
//   06      the advice starts coming apart mid sentence
//   07      he has a stroke and is removed, on the same card
//   08-09   a stranger finishes the list and accidentally gets sincere
//   10      the brand returns, deadpan, as though none of it happened
//
//   node fetch-photos.mjs && node fetch-extra.mjs   (sources, once)
//   node build.mjs && node render.mjs ig && node render.mjs tiktok
//
// House rules still apply: no em dashes, no pricing, no features we do not ship.
// The final slide is the only one making a claim, and it is a true one.
import { writeFileSync, mkdirSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));

const MARK = (w, h) => `<svg width="${w}" height="${h}" viewBox="200 180 620 520" xmlns="http://www.w3.org/2000/svg">
  <polygon points="224,512 404,296 494,422 602,224 800,512" fill="#fff"/>
  <path d="M 217 620 Q 290 584 364 620 T 512 620 T 660 620 T 807 620 L 807 692 L 217 692 Z" fill="#fff"/></svg>`;

// voice:   host (amber, default) | successor (cold, white numerals, tagged)
// state:   stutter | collapse         the narrator's exit, as css
// severed: the card where he is removed mid sentence
//
// Ten slides, because an Instagram carousel takes ten images. The cover still
// promises twelve tips and the deck stops at eight, which is the joke doing its own
// work: he never got to the rest. Slide 10 says so out loud.
const slides = [
  {
    kind: "cover", file: "01-cover", photo: "crew-01", focus: "38% 34%",
    kicker: "TWELVE (12) TRAVEL TIPS",
    head: ["12 travel tips", "from a man", "who will not survive them"],
    sub: "He does not know that yet. Swipe gently.",
  },
  {
    n: "01", file: "02-beer", photo: "beer-04", focus: "50% 45%",
    head: "have a beer at the airport at six in the morning",
    body: "It is not morning at the airport. The airport has no morning. Time was taken out of the building in 1997 for insurance reasons and never put back. Order the beer. Nobody can see you here. You are between countries and, technically, between people.",
  },
  {
    n: "02", file: "03-tip", photo: "pay-02", focus: "50% 45%",
    head: "tip everyone. and i do mean everyone",
    body: "The barman. The barber. Your hookers. The man who held the door of a building you did not enter and had no intention of entering. The sea. The sea has done nothing for you but it has been watching you all week and it knows.",
  },
  {
    n: "03", file: "04-beachman", photo: "beachman-06", focus: "50% 45%",
    head: "fall in love with the handsome man selling drugs on the beach",
    body: "Do not buy anything. That is not what he is for. Sit down. Learn his mother's name. He has a boat, a scar, and no plans whatsoever. In eleven years you will think about him while loading a dishwasher in Leicester and you will have to sit down on the floor.",
  },
  {
    n: "04", file: "05-sentence", photo: "pay-01", focus: "50% 45%",
    head: "learn one sentence in the local language and use it constantly",
    body: "Mine is 'my brother is also here'. It has never once been useful. It has never once been the wrong thing to say. A woman in Lisbon cried. I do not have a brother. I have never had a brother.",
  },
  {
    n: "05", file: "06-photocopy", photo: "docs-01", focus: "62% 46%", state: "stutter",
    head: "always keep a photocopy of your passport in a separate bag from",
    body: "from the. from the other one. sorry. from the other bag. the bag that is not this bag. give me a second, I had the whole thing a minute ago and now there is a sound",
  },
  {
    // The stroke and the removal on one card. Ten slides has no room for both, and
    // they hit harder stacked anyway.
    n: "06", file: "07-toast", photo: "blur-01", focus: "50% 50%",
    state: "collapse cut", severed: true, countOverride: "06 / --",
    head: "i can smell toast",
    body: "There is no toast. I understand that now. Tell my wife I learned to whistle in 2004 and never told anybody because I wanted one thing that was only mine. Tip seven is that you should always carry a spare pair of",
    note: "[ this account has changed hands ]",
  },
  {
    n: "07", file: "08-bruges", photo: "canal-04", focus: "50% 45%", voice: "successor",
    chip: "NEW MANAGEMENT",
    head: "do not go to bruges",
    body: "It is my understanding that I am delivering the remaining tips. I did not read the earlier ones. I was occupied. Tip seven is do not go to Bruges. I will not be elaborating and you will not be asking.",
  },
  {
    n: "08", file: "09-goanyway", photo: "trail-03", focus: "50% 50%", voice: "successor",
    tweak: "scale(1.15) translateY(-7%)",
    head: "go anyway",
    body: "The man who did this before me had been to sixty one countries and still cried at every single airport. Not from sadness. He would never say from what. Go anyway. Go while going is still a thing your body agrees to do.",
  },
  {
    // No photograph on this one. Brand navy field, subject cut out over it.
    // The subject is sources/gun.png, produced by cutout.py. If that file is not
    // there yet the slide still renders, just without it, and build.mjs says so.
    kind: "threat", file: "10-outro", cutout: "gun",
    head: ["we are done", "asking"],
    demand: "download wanderbuddy rn",
    cta: "first 500 users are free",
  },
];

// Offcuts from the fourteen slide version, kept for a TikTok long cut or a second
// post. TikTok photo posts are not capped at ten the way an IG carousel is. Give one
// a file name and an `n`, drop it back into `slides`, and it renders like the rest.
export const reserve = [
  { photo: "train-05", focus: "50% 45%",
    head: "never look directly at a swiss train conductor",
    body: "They are legally required to be beautiful. It is in the constitution. Article nine. Look at the seat in front of you and count to forty. By then he will have taken something from you that you cannot itemise." },
  { photo: "van-03", focus: "50% 48%",
    head: "there is no third rome",
    body: "There are two. The one you are thinking of, and the other one. If a man offers to drive you to the third Rome, that is a van. Do not get in the van. Wave, though. Be pleasant about it. He is doing his best." },
  { photo: "pack-02", focus: "50% 46%", voice: "successor",
    head: "pack one item you would be embarrassed to die with",
    body: "It keeps you careful. Mine is a small ceramic frog. I have been extremely careful for nine years and I have never once been photographed." },
];

const SIZES = { ig: [1080, 1350], tiktok: [1080, 1920] };

const css = (W, H) => {
  const k = H / 1350;
  const px = n => `${Math.round(n * k)}px`;
  return `
  :root{ --amber:#F2A93B; --ink:#060E18; --wrong:#D9503F; --cold:#B9C6D2; }
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:${W}px;height:${H}px;overflow:hidden;}
  body{ background:var(--ink); color:#fff; position:relative;
    font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif; -webkit-font-smoothing:antialiased; }
  .shot{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
    filter:saturate(1.06) contrast(1.04); }
  .scrim{ position:absolute; inset:0; background:
    linear-gradient(180deg, rgba(6,14,24,.62) 0%, rgba(6,14,24,.16) 12%,
      rgba(6,14,24,0) 28%, rgba(6,14,24,.12) 44%, rgba(6,14,24,.70) 65%,
      rgba(6,14,24,.95) 83%, #060E18 100%); }
  .pad{ position:absolute; inset:0; padding:${px(58)} ${px(62)} ${px(56)};
    display:flex; flex-direction:column; }

  .top{ display:flex; align-items:center; justify-content:space-between; }
  .brand{ display:flex; align-items:center; gap:${px(13)}; opacity:.92; }
  .wordmark{ font-weight:700; font-size:${px(28)}; letter-spacing:.01em; }
  .count{ font-family:Consolas,"Courier New",monospace; font-size:${px(24)};
    letter-spacing:.16em; color:rgba(255,255,255,.72); }

  .body{ margin-top:auto; }
  .num{ font-weight:900; font-size:${px(112)}; line-height:.82; color:var(--amber);
    letter-spacing:-.04em; margin-bottom:${px(18)}; }
  .head{ font-weight:900; font-size:${px(74)}; line-height:1.0; letter-spacing:-.028em;
    text-shadow:0 ${px(2)} ${px(26)} rgba(0,0,0,.5); }
  .rule{ width:${px(96)}; height:${px(5)}; background:var(--amber); border-radius:${px(3)};
    margin:${px(24)} 0 ${px(22)}; }
  .copy{ font-size:${px(32)}; line-height:1.38; color:rgba(255,255,255,.9);
    max-width:${px(890)}; text-shadow:0 ${px(1)} ${px(16)} rgba(0,0,0,.55); }

  .foot{ margin-top:${px(36)}; display:flex; align-items:center; justify-content:space-between;
    border-top:${px(2)} solid rgba(255,255,255,.22); padding-top:${px(20)}; }
  .foot .tag{ font-size:${px(24)}; color:rgba(255,255,255,.74); }
  .swipe{ font-size:${px(25)}; font-weight:700; color:var(--amber); letter-spacing:.02em; }

  /* ---- stage one: the sentence starts eating itself ---- */
  .stutter .head{ color:#fff;
    text-shadow:${px(9)} ${px(8)} 0 rgba(217,80,63,.62),
                ${px(19)} ${px(16)} 0 rgba(217,80,63,.26),
                0 ${px(2)} ${px(26)} rgba(0,0,0,.5); }
  .stutter .copy{ color:rgba(255,255,255,.72); }

  /* ---- stage two: the narrator comes apart ---- */
  .collapse .wordmark{ letter-spacing:${px(9)}; opacity:.55; }
  .collapse .num{ color:var(--wrong); transform:rotate(-4deg) translateX(${px(-6)}); opacity:.85; }
  .collapse .head{ letter-spacing:${px(3)}; color:#fff; }
  .collapse .rule{ background:var(--wrong); width:${px(52)}; }
  .collapse .copy{ color:rgba(255,255,255,.8); }
  .collapse .swipe{ color:var(--wrong); }

  /* ---- stage three: the sentence simply stops ---- */
  .cut .caret{ display:inline-block; width:${px(18)}; height:${px(30)};
    background:var(--wrong); vertical-align:${px(-4)}; margin-left:${px(9)}; }
  .cut .band{ margin-top:${px(30)}; border-top:${px(3)} solid var(--wrong);
    height:${px(118)}; background:#03080E; }
  .cut .note{ font-family:Consolas,"Courier New",monospace; font-size:${px(23)};
    letter-spacing:.14em; color:rgba(255,255,255,.42); margin-top:${px(18)}; }
  .cut .swipe{ color:rgba(255,255,255,.4); }

  /* ---- the successor. same furniture, colder hands ---- */
  .successor .shot{ filter:saturate(.42) contrast(1.1) brightness(.88); }
  .successor .num{ color:#fff; }
  .successor .rule{ background:var(--cold); width:${px(60)}; }
  .successor .swipe{ color:var(--cold); }
  .chip{ display:inline-block; font-family:Consolas,"Courier New",monospace;
    font-size:${px(22)}; letter-spacing:.2em; color:#0B1622; background:var(--cold);
    padding:${px(8)} ${px(15)}; border-radius:${px(3)}; margin-bottom:${px(20)}; }

  /* cover */
  .cover .kicker{ font-family:Consolas,"Courier New",monospace; font-size:${px(26)};
    letter-spacing:.2em; color:var(--amber); margin-bottom:${px(26)}; }
  .cover .head{ font-size:${px(94)}; line-height:.95; letter-spacing:-.035em; }
  .cover .head em{ font-style:normal; color:var(--amber); }
  .cover .copy{ margin-top:${px(28)}; font-size:${px(35)}; }

  /* ---- the closer. brand navy field, no photograph, subject cut out on top ---- */
  body.threat{ background:radial-gradient(130% 100% at 25% 8%,
    #1c3a5c 0%, #10233c 46%, #0a1622 100%); }
  /* Geometry is set per aspect rather than scaled from one number. The artwork is
     only 420x640, so the 9:16 canvas will happily blow it up past 2x and go soft,
     and a subject sized for 4:5 lands straight on top of the headline at 9:16. */
  .threat .subject{ position:absolute; object-fit:contain; object-position:top right;
    filter:drop-shadow(0 ${px(28)} ${px(50)} rgba(0,0,0,.62));
    /* the source ends on a flat cut across the wrist, which reads as a severed hand
       floating on the navy. Dissolve the last stretch into the background instead. */
    -webkit-mask-image:linear-gradient(180deg, #000 72%, rgba(0,0,0,.55) 88%, transparent 100%);
    mask-image:linear-gradient(180deg, #000 72%, rgba(0,0,0,.55) 88%, transparent 100%); }
  ${H > 1500
    ? `.threat .subject{ right:${px(-26)}; top:${px(150)}; width:${px(700)}; max-height:${px(660)}; }`
    : `.threat .subject{ right:${px(-30)}; top:${px(118)}; width:${px(830)}; max-height:${px(742)}; }`}
  /* keeps the headline readable where the subject overlaps it */
  .threat .floor{ position:absolute; left:0; right:0; bottom:0; height:52%;
    background:linear-gradient(180deg, rgba(10,22,34,0) 0%, rgba(10,22,34,.72) 42%,
      rgba(10,22,34,.94) 72%, #0a1622 100%); }
  .threat .head{ font-size:${px(96)}; line-height:.94; letter-spacing:-.035em; }
  .threat .head em{ font-style:normal; color:var(--amber); }
  .threat .demand{ margin-top:${px(26)}; font-weight:800; font-size:${px(46)};
    line-height:1.08; letter-spacing:-.02em; }
  .threat .pill{ display:inline-block; margin-top:${px(26)}; background:var(--amber); color:#10233C;
    font-weight:800; font-size:${px(31)}; letter-spacing:.02em;
    padding:${px(18)} ${px(36)}; border-radius:${px(100)}; }
`;
};

const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");

// Slides with a `cutout` composite over the brand field instead of a photograph.
// Missing file is not fatal: the slide renders without it and we warn once.
const cutoutPath = name => join(HERE, "sources", `${name}.png`);
const missingCutouts = new Set();

const doc = (s, i, W, H) => {
  const count = s.countOverride || `${String(i + 1).padStart(2, "0")} / ${slides.length}`;
  const tweak = s.tweak ? ` transform:${s.tweak};` : "";
  let shot = "";
  if (s.cutout) {
    if (existsSync(cutoutPath(s.cutout))) {
      shot = `<img class="subject" src="../../sources/${s.cutout}.png">`;
    } else {
      missingCutouts.add(s.cutout);
    }
    shot += `<div class="floor"></div>`;
  } else if (s.photo) {
    shot = `<img class="shot" src="../../sources/${s.photo}.jpg" style="object-position:${s.focus};${tweak}"><div class="scrim"></div>`;
  }
  const top = `<div class="top">
      <div class="brand">${MARK(Math.round(34 * H / 1350), Math.round(31 * H / 1350))}<span class="wordmark">WanderBuddy</span></div>
      <div class="count">${esc(count)}</div>
    </div>`;
  const classes = [s.kind || "tip", s.state, s.voice].filter(Boolean).join(" ");

  let inner;
  if (s.kind === "threat") {
    inner = `<div class="body">
      <div class="head">${s.head.map((l, j) => j === 1 ? `<em>${esc(l)}</em>` : esc(l)).join("<br>")}</div>
      <div class="rule"></div>
      <div class="demand">${esc(s.demand)}</div>
      <div class="pill">${esc(s.cta)}</div>
      <div class="foot"><div class="tag">wanderbuddyapp.com</div><div class="swipe">save this &darr;</div></div>
    </div>`;
  } else if (s.kind === "cover") {
    inner = `<div class="body">
      <div class="kicker">${s.kicker}</div>
      <div class="head">${s.head.map((l, j) => j === 2 ? `<em>${esc(l)}</em>` : esc(l)).join("<br>")}</div>
      <div class="copy">${esc(s.sub)}</div>
      <div class="foot"><div class="tag">wanderbuddyapp.com</div><div class="swipe">swipe &rarr;</div></div>
    </div>`;
  } else if (s.severed) {
    // He gets most of a sentence out. The caret is where he stopped.
    inner = `<div class="body">
      <div class="num">${s.n}</div>
      <div class="head">${esc(s.head)}</div>
      <div class="rule"></div>
      <div class="copy">${esc(s.body)}<span class="caret"></span></div>
      <div class="band"></div>
      <div class="note">${esc(s.note)}</div>
      <div class="foot"><div class="tag">wanderbuddyapp.com</div><div class="swipe">swipe &rarr;</div></div>
    </div>`;
  } else {
    inner = `<div class="body">
      ${s.chip ? `<div class="chip">${esc(s.chip)}</div>` : ""}
      <div class="num">${s.n}</div>
      <div class="head">${esc(s.head)}</div>
      <div class="rule"></div>
      <div class="copy">${esc(s.body)}</div>
      <div class="foot"><div class="tag">wanderbuddyapp.com</div><div class="swipe">swipe &rarr;</div></div>
    </div>`;
  }

  return `<!doctype html><html><head><meta charset="utf-8"><style>${css(W, H)}</style></head>
<body class="${classes}">${shot}<div class="pad">${top}${inner}</div></body></html>`;
};

const manifest = [];
for (const [variant, [W, H]] of Object.entries(SIZES)) {
  mkdirSync(join(HERE, "build", variant), { recursive: true });
  mkdirSync(join(HERE, "out", variant), { recursive: true });
  slides.forEach((s, i) => {
    writeFileSync(join(HERE, "build", variant, `${s.file}.html`), doc(s, i, W, H));
    manifest.push({ variant, w: W, h: H, html: `build/${variant}/${s.file}.html`, png: `out/${variant}/${s.file}.png` });
  });
}
writeFileSync(join(HERE, "manifest.json"), JSON.stringify(manifest, null, 2));
console.log(`generated ${slides.length} slides x ${Object.keys(SIZES).length} sizes = ${manifest.length} pages`);
for (const name of missingCutouts) {
  console.warn(`\n  ! sources/${name}.png is missing, so slide 10 rendered without its subject.`);
  console.warn(`    Drop the artwork in as sources/${name}-src.png and run:`);
  console.warn(`      python cutout.py sources/${name}-src.png sources/${name}.png`);
  console.warn(`      node build.mjs && node render.mjs ig && node render.mjs tiktok`);
}
