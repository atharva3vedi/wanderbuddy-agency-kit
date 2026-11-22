// WanderBuddy Instagram quote/hook cards.
// Square 1:1 daily-feed cards in the app's dark "Mission Control" navy field,
// the same visual system as marketing/reddit-posters (so the feed reads as one
// brand). No app-screenshot dependency, so these are cheap to churn out for a
// daily cadence. One relatable planner-voice hook per card, exactly one amber
// word (the punch), locked logo footer.
//
//   node build.mjs && node render.mjs   (render.mjs shells headless Edge -> PNG)
//
// Hard rules (same everywhere): no em dashes, no pricing, no fake features.
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));

// The twin-peaks + wave mark, drawn inline (matches reddit-posters).
const MARK = (w, h) => `<svg width="${w}" height="${h}" viewBox="200 180 620 520" xmlns="http://www.w3.org/2000/svg">
  <polygon points="224,512 404,296 494,422 602,224 800,512" fill="#fff"/>
  <path d="M 217 620 Q 290 584 364 620 T 512 620 T 660 620 T 807 620 L 807 692 L 217 692 Z" fill="#fff"/></svg>`;

// Each card: file, kicker (top label), head lines (array; wrap the punch word in
// {amber:"..."} ), sub (payoff line), tag (footer right, rotates).
const cards = [
  { file: "q01-knows-the-plan", kicker: "GROUP TRIP // DAY 1",
    head: ["nobody knows", "the plan", { amber: "but you" }],
    sub: "So we put the whole trip in one place. book first, figure it out together.",
    tag: "we plan the trip. you sit down." },
  { file: "q02-zero-decisions", kicker: "THE GROUP CHAT",
    head: ["247 messages.", { amber: "zero decisions." }],
    sub: "One shared plan the whole group can actually edit. Live.",
    tag: "one app for the whole trip." },
  { file: "q03-nine-apps", kicker: "EVERY GROUP TRIP",
    head: ["nine apps.", "one", { amber: "tired friend." }],
    sub: "We made it one app, so keeping everyone alive is not all on one person.",
    tag: "book first, figure it out together." },
  { file: "q04-someone-covers-more", kicker: "WHO PAID FOR THE TAXI",
    head: ["someone always", { amber: "covers more." }],
    sub: "Split expenses that sit right next to the plan, so people actually log them.",
    tag: "we plan the trip. you sit down." },
  { file: "q05-need-a-visa", kicker: "SEEN AT THE AIRPORT",
    head: ["wait, did we", "need a", { amber: "visa?" }],
    sub: "Check entry requirements before you book, not at the gate. With official links.",
    tag: "one app for the whole trip." },
  { file: "q06-language-barrier", kicker: "THE LANGUAGE BARRIER",
    head: ["was never", "the", { amber: "fun part." }],
    sub: "A live voice room that captions the conversation in everyone's own language.",
    tag: "everyone understands each other." },
  { file: "q07-allowed-to-rest", kicker: "FOR THE FRIEND WHO PLANS EVERYTHING",
    head: ["you are", { amber: "allowed to rest." }],
    sub: "We will watch the trip.",
    tag: "we plan the trip. you sit down." },
  { file: "q08-travel-crew", kicker: "PUBLIC TRIPS",
    head: ["your next travel crew", "is", { amber: "already booking." }],
    sub: "Browse trips people are already planning. See the spots left. Join with a code.",
    tag: "find your people." },
  { file: "q09-not-surveilled", kicker: "LIVE LOCATION",
    head: ["safe,", { amber: "not surveilled." }],
    sub: "Shared with consent, on a timer you set. Off by default, always.",
    tag: "your location, your rules." },
  { file: "q10-step-two", kicker: "THE HONEST ITINERARY",
    head: ["step 1: book.", { amber: "step 2: ??????" }, "step 3: go."],
    sub: "We are pretty good at step 2.",
    tag: "book first, figure it out together." },
  { file: "q11-together", kicker: "GROUP TRAVEL",
    head: ["book first.", "figure it out", { amber: "together." }],
    sub: "The plan, the chat, the money, the map. One app for the whole trip.",
    tag: "one app for the whole trip." },
  { file: "q12-better-with-people", kicker: "SOLO, BUT NOT ALWAYS",
    head: ["some trips are", "better with", { amber: "people." }],
    sub: "Find a crew, keep it organized, and actually feel safe doing it.",
    tag: "find your people." },
  { file: "q13-out-of-your-head", kicker: "THE PLAN",
    head: ["out of your head.", "into", { amber: "one app." }],
    sub: "So you stop being the group's walking schedule for a whole trip.",
    tag: "we plan the trip. you sit down." },
  { file: "q14-keep-everyone-alive", kicker: "A GENTLE REMINDER",
    head: ["you plan every trip", "and keep", { amber: "everyone alive." }],
    sub: "This time it is not all on you.",
    tag: "book first, figure it out together." },
  { file: "q15-the-spreadsheet", kicker: "THE GROUP ITINERARY",
    head: ["the whole trip lives", "in a", { amber: "spreadsheet." }],
    sub: "Move it somewhere everyone can open, edit, and actually follow. Live.",
    tag: "one app for the whole trip." },
  { file: "q16-someone-elses-phone", kicker: "AFTER EVERY TRIP",
    head: ["the best photos", "are on", { amber: "someone else's phone." }],
    sub: "One shared feed for the whole trip, so nobody has to beg for the pictures.",
    tag: "one app for the whole trip." },
  { file: "q17-alone-not-unsafe", kicker: "SOLO TRAVEL",
    head: ["going alone", "does not mean", { amber: "unsafe." }],
    sub: "SOS, live location on your terms, and entry requirements before you fly.",
    tag: "your location, your rules." },
  { file: "q18-real-money", kicker: "AT THE COUNTER",
    head: ["how much is that", "in", { amber: "real money?" }],
    sub: "Currency and shared expenses sit right next to the plan. No mental math.",
    tag: "one app for the whole trip." },
  { file: "q19-nothing-booked", kicker: "THREE DAYS. NO PLAN.",
    head: ["you land tomorrow", "and have", { amber: "nothing booked." }],
    sub: "Tell WanderBuddy where you are going. Get a day by day plan you can edit.",
    tag: "we plan the trip. you sit down." },
  { file: "q20-never-forget-passport", kicker: "A PUBLIC SERVICE ANNOUNCEMENT",
    head: ["never forget your", "passport", { amber: "ever again." }],
    sub: `Passport, tickets and visas live in one vault, with a heads up before anything expires. <span style="opacity:.6;font-style:italic;">(unlike some who i know. cough, cough.)</span>`,
    tag: "one app for the whole trip." },
  // --- snarky batch (passport above is the header) ---
  { file: "q21-pay-you-back", kicker: "WHO OWES WHO, VOLUME 47",
    head: ["\"i'll pay", "you back.\"", { amber: "sure you will." }],
    sub: `Expenses split themselves right next to the plan. The math is done, so nobody gets to 'forget' their card. <span style="opacity:.6;font-style:italic;">(you know who you are.)</span>`,
    tag: "one app for the whole trip." },
  { file: "q22-visa-at-the-gate", kicker: "IT IS ALWAYS THE SAME PERSON",
    head: ["\"do we need", "a visa?\"", { amber: "at the gate." }],
    sub: `Entry requirements, with official links, before you book. Not while the plane is boarding without you.`,
    tag: "book first, figure it out together." },
  { file: "q23-screenshots-and-a-prayer", kicker: "THE PLAN, ALLEGEDLY",
    head: ["your plan:", "screenshots", { amber: "and a prayer." }],
    sub: `One shared plan the whole group can open and edit. Live. We retired the group's screenshot archive.`,
    tag: "one app for the whole trip." },
  { file: "q24-unpaid-tour-guide", kicker: "A ROLE YOU DID NOT APPLY FOR",
    head: ["you are the", "group's unpaid", { amber: "tour guide." }],
    sub: `Put the whole trip in one app, so keeping everyone alive stops being your full time job.`,
    tag: "we plan the trip. you sit down." },
  { file: "q25-still-just-a-chat", kicker: "SIX MONTHS OF 'WE SHOULD GO'",
    head: ["the trip you", "\"should do\" is", { amber: "still a chat." }],
    sub: `Turn the someday trip into a real one. One plan, one link, and suddenly everyone is actually in.`,
    tag: "book first, figure it out together." },
];

const headHTML = lines => lines.map(l =>
  typeof l === "string" ? l : `<span class="amber">${l.amber}</span>`
).join("<br>");

const doc = c => `<!doctype html><html><head><meta charset="utf-8"><style>
  :root{ --amber:#F2A93B; }
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:1080px;height:1080px;}
  body{
    background:radial-gradient(130% 100% at 25% 8%, #1c3a5c 0%, #10233c 46%, #0a1622 100%);
    font-family:Arial, Helvetica, sans-serif; color:#fff; position:relative; overflow:hidden;
  }
  .ghost{ position:absolute; right:-150px; bottom:-130px; width:760px; opacity:.06; transform:rotate(-4deg); }
  .frame{ position:absolute; inset:34px; border:2px solid rgba(255,255,255,.42); }
  .pad{ position:absolute; inset:34px; padding:64px 70px 54px; display:flex; flex-direction:column; height:calc(1080px - 68px); }
  .kicker{ font-family:Consolas,"Courier New",monospace; font-size:26px; letter-spacing:.18em;
    color:rgba(255,255,255,.62); text-transform:uppercase; }
  .head{ margin-top:auto; margin-bottom:22px; font-weight:900; font-size:104px; line-height:.98;
    letter-spacing:-.02em; }
  .head .amber{ color:var(--amber); }
  .rule{ width:132px; height:5px; background:var(--amber); border-radius:3px; margin:6px 0 26px; }
  .sub{ font-size:37px; line-height:1.3; color:rgba(255,255,255,.9); max-width:900px; }
  .foot{ margin-top:44px; display:flex; justify-content:space-between; align-items:center;
    border-top:2px solid rgba(255,255,255,.3); padding-top:20px; }
  .brand{ display:flex; align-items:center; gap:18px; }
  .wordmark{ font-weight:800; font-size:38px; }
  .tag{ font-size:23px; color:rgba(255,255,255,.82); text-align:right; white-space:nowrap; }
</style></head>
<body>
  <div class="ghost">${MARK(760, 672)}</div>
  <div class="frame"></div>
  <div class="pad">
    <div class="kicker">${c.kicker}</div>
    <div class="head">${headHTML(c.head)}</div>
    <div class="rule"></div>
    <div class="sub">${c.sub}</div>
    <div class="foot">
      <div class="brand">${MARK(72, 66)}<span class="wordmark">WanderBuddy</span></div>
      <div class="tag">${c.tag}</div>
    </div>
  </div>
</body></html>`;

const manifest = [];
for (const c of cards) {
  writeFileSync(join(HERE, `${c.file}.html`), doc(c));
  manifest.push({ file: `${c.file}.html`, png: `${c.file}.png` });
}
writeFileSync(join(HERE, "manifest.json"), JSON.stringify(manifest, null, 2));
console.log(`generated ${cards.length} IG quote cards`);
