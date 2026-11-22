// WanderBuddy "12 travel tips nobody tells you" carousel.
//
// 14 slides: a cover, 12 tips, one CTA. Photo led rather than the flat navy
// quote-card system, because this one has to survive on a travel feed next to
// other people's holiday photos, not just on our own grid.
//
// Renders both aspect ratios from one source of truth:
//   ig      1080x1350  (4:5, the tallest Instagram allows in a carousel)
//   tiktok  1080x1920  (9:16, TikTok photo post)
//
//   node fetch-photos.mjs && node build.mjs && node render.mjs
//
// Hard rules, same as the rest of marketing/: no em dashes, no pricing, no
// features we do not ship. Every tip here is a real, checkable rule.
import { writeFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));

const MARK = (w, h) => `<svg width="${w}" height="${h}" viewBox="200 180 620 520" xmlns="http://www.w3.org/2000/svg">
  <polygon points="224,512 404,296 494,422 602,224 800,512" fill="#fff"/>
  <path d="M 217 620 Q 290 584 364 620 T 512 620 T 660 620 T 807 620 L 807 692 L 217 692 Z" fill="#fff"/></svg>`;

// focus = object-position, so the crop keeps the subject going 4:5 -> 9:16.
const slides = [
  {
    kind: "cover", file: "01-cover", photo: "crew-01", focus: "38% 34%",
    kicker: "SAVE THIS FOR YOUR NEXT TRIP",
    head: ["12 travel tips", "nobody", "actually tells you"],
    sub: "Number 4 has been quietly costing you money for years.",
  },
  {
    n: "01", file: "02-transit", photo: "corridor-01", focus: "50% 40%",
    head: "check the visa for your layover, not just your destination",
    body: "Some countries want a transit visa even if you never leave the airport. The UK, China and Canada have all turned people around for it. Check every airport printed on the ticket.",
  },
  {
    n: "02", file: "03-passport", photo: "docs-01", focus: "62% 46%",
    head: "your passport can be valid and still get you refused",
    body: "Most countries want six months left on it counting from the day you land, plus a couple of blank pages. The airline checks at the desk, so look at your expiry date before you book anything.",
  },
  {
    n: "03", file: "04-onward", photo: "board-01", focus: "50% 55%",
    head: "no onward ticket, no boarding pass",
    body: "Thailand, Indonesia, the Philippines and plenty of others want proof you are leaving before they let you in. The airline gets fined if you cannot show it, so they ask at the gate.",
  },
  {
    n: "04", file: "05-currency", photo: "card-04", focus: "50% 44%",
    head: "always let the card machine charge you in the local currency",
    body: "When it offers to bill you in your home currency instead, that is dynamic currency conversion. The rate is set by the terminal, not your bank, and it skims roughly 3 to 7 percent off every tap.",
  },
  {
    n: "05", file: "06-atm", photo: "atm-01", focus: "50% 45%",
    head: "use a real bank's ATM, never the one in arrivals",
    body: "Standalone machines in airports and tourist strips run the highest fees and the worst rates. Walk to a bank branch, decline the conversion offer again, and take out one larger amount instead of five small ones.",
  },
  {
    n: "06", file: "07-delay", photo: "delayed-04", focus: "50% 38%",
    head: "a three hour delay can be worth up to 600 euros in cash",
    body: "Flights leaving the EU or UK, and flights landing there on an EU or UK airline, carry compensation rights for long delays and cancellations. Cash, not vouchers. Nobody will offer it. You claim it yourself, and you have years to do it.",
  },
  {
    n: "07", file: "08-bagtag", photo: "checkin-01", focus: "50% 50%",
    head: "photograph your bag and its tag at drop off",
    body: "One shot of the bag, one of the barcode sticker. If it goes missing you file the claim with a photo and a tracking number instead of the words 'black, medium, sort of shiny'.",
  },
  {
    n: "08", file: "09-esim", photo: "gate-01", focus: "55% 44%",
    head: "install your eSIM before you get on the plane",
    body: "Activating one needs wifi, and airport wifi abroad often wants a local number to text you a code. Which you do not have yet. Buy it and install it at home, then switch it on when you land.",
  },
  {
    n: "09", file: "10-offline", photo: "maps-01", focus: "50% 50%",
    head: "your GPS still works with zero signal",
    body: "The chip in your phone listens to satellites, it does not talk to your carrier. Download the offline map area before you fly and the blue dot keeps moving in airplane mode. No bars, no data, no roaming bill.",
  },
  {
    n: "10", file: "11-emergency", photo: "night-01", focus: "50% 45%",
    head: "112 reaches emergency services almost anywhere in europe",
    body: "From any phone, on any network, even a locked one. Outside Europe the number changes, so look up the local one and save it before you land rather than while something is already going wrong.",
  },
  {
    n: "11", file: "12-insurance", photo: "trail-03", focus: "50% 50%", tweak: "scale(1.15) translateY(-7%)",
    head: "you may already be insured and not know it",
    body: "Plenty of credit cards include delay, baggage and medical cover if you paid for the trip on that card. Most people buy a second policy without ever checking. Search your card's benefits guide for the word travel.",
  },
  {
    n: "12", file: "13-split", photo: "table-01", focus: "50% 38%",
    head: "settle group money during the trip, not after",
    body: "Every day you leave it, it turns a little more into the thing nobody wants to bring up. Log it the same day, split it the same day, come home still liking each other.",
  },
  {
    kind: "cta", file: "14-outro", photo: "sunset-01", focus: "50% 45%", tweak: "scale(1.10) translateY(-5%)",
    kicker: "ONE LAST THING",
    head: ["we built the app", "that remembers", "all of this"],
    body: "WanderBuddy keeps the plan, the entry rules, the documents and the money in one place, so the whole group is finally looking at the same trip. Free to join.",
    cta: "link in bio",
  },
];

const SIZES = { ig: [1080, 1350], tiktok: [1080, 1920] };

const css = (W, H) => {
  const k = H / 1350;                        // scale type with the canvas
  const px = n => `${Math.round(n * k)}px`;
  return `
  :root{ --amber:#F2A93B; --ink:#060E18; }
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:${W}px;height:${H}px;overflow:hidden;}
  body{ background:var(--ink); color:#fff; position:relative;
    font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif; -webkit-font-smoothing:antialiased; }
  .shot{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
    filter:saturate(1.06) contrast(1.04); }
  .shot.tweak{ transform-origin:50% 50%; }
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
  .head{ font-weight:900; font-size:${px(78)}; line-height:1.0; letter-spacing:-.028em;
    text-shadow:0 ${px(2)} ${px(26)} rgba(0,0,0,.5); }
  .rule{ width:${px(96)}; height:${px(5)}; background:var(--amber); border-radius:${px(3)};
    margin:${px(24)} 0 ${px(22)}; }
  .copy{ font-size:${px(33)}; line-height:1.38; color:rgba(255,255,255,.9);
    max-width:${px(880)}; text-shadow:0 ${px(1)} ${px(16)} rgba(0,0,0,.55); }

  .foot{ margin-top:${px(38)}; display:flex; align-items:center; justify-content:space-between;
    border-top:${px(2)} solid rgba(255,255,255,.22); padding-top:${px(20)}; }
  .foot .tag{ font-size:${px(24)}; color:rgba(255,255,255,.74); }
  .swipe{ font-size:${px(25)}; font-weight:700; color:var(--amber); letter-spacing:.02em; }

  /* cover */
  .cover .kicker{ font-family:Consolas,"Courier New",monospace; font-size:${px(26)};
    letter-spacing:.2em; color:var(--amber); margin-bottom:${px(26)}; }
  .cover .head{ font-size:${px(104)}; line-height:.95; letter-spacing:-.035em; }
  .cover .head em{ font-style:normal; color:var(--amber); }
  .cover .copy{ margin-top:${px(28)}; font-size:${px(35)}; }

  /* cta */
  /* the outro sits on open sky, so the label needs its own ground to read on */
  .cta .kicker{ display:inline-block; font-family:Consolas,"Courier New",monospace;
    font-size:${px(24)}; letter-spacing:.2em; color:var(--amber); margin-bottom:${px(24)};
    background:rgba(6,14,24,.62); padding:${px(9)} ${px(16)}; border-radius:${px(4)}; }
  .cta .head{ font-size:${px(92)}; line-height:.98; }
  .cta .head em{ font-style:normal; color:var(--amber); }
  .cta .pill{ display:inline-block; margin-top:${px(30)}; background:var(--amber); color:#10233C;
    font-weight:800; font-size:${px(30)}; letter-spacing:.02em;
    padding:${px(17)} ${px(34)}; border-radius:${px(100)}; }
`;
};

const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");

const doc = (s, i, W, H) => {
  const count = `${String(i + 1).padStart(2, "0")} / ${slides.length}`;
  const tweak = s.tweak ? ` transform:${s.tweak};` : "";
  const shot = `<img class="shot${s.tweak ? " tweak" : ""}" src="../../sources/${s.photo}.jpg" style="object-position:${s.focus};${tweak}">`;
  const top = `<div class="top">
      <div class="brand">${MARK(Math.round(34 * H / 1350), Math.round(31 * H / 1350))}<span class="wordmark">WanderBuddy</span></div>
      <div class="count">${count}</div>
    </div>`;

  let inner;
  if (s.kind === "cover") {
    inner = `<div class="body">
      <div class="kicker">${s.kicker}</div>
      <div class="head">${s.head.map((l, j) => j === 1 ? `<em>${esc(l)}</em>` : esc(l)).join("<br>")}</div>
      <div class="copy">${esc(s.sub)}</div>
      <div class="foot"><div class="tag">wanderbuddyapp.com</div><div class="swipe">swipe &rarr;</div></div>
    </div>`;
  } else if (s.kind === "cta") {
    inner = `<div class="body">
      <div class="kicker">${s.kicker}</div>
      <div class="head">${s.head.map((l, j) => j === 2 ? `<em>${esc(l)}</em>` : esc(l)).join("<br>")}</div>
      <div class="rule"></div>
      <div class="copy">${esc(s.body)}</div>
      <div class="pill">${esc(s.cta)}</div>
      <div class="foot"><div class="tag">wanderbuddyapp.com</div><div class="swipe">save this &darr;</div></div>
    </div>`;
  } else {
    inner = `<div class="body">
      <div class="num">${s.n}</div>
      <div class="head">${esc(s.head)}</div>
      <div class="rule"></div>
      <div class="copy">${esc(s.body)}</div>
      <div class="foot"><div class="tag">wanderbuddyapp.com</div><div class="swipe">swipe &rarr;</div></div>
    </div>`;
  }

  return `<!doctype html><html><head><meta charset="utf-8"><style>${css(W, H)}</style></head>
<body class="${s.kind || "tip"}">${shot}<div class="scrim"></div><div class="pad">${top}${inner}</div></body></html>`;
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
