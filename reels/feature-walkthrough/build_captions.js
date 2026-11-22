// Renders transparent 1080x1920 caption/title overlays via headless Chrome.
const fs = require('fs'); const cp = require('child_process'); const path = require('path');
const ROOT = __dirname; const OUT = path.join(ROOT, 'ui', 'caps'); fs.mkdirSync(OUT, { recursive: true });
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';

const CSS = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}
body{width:1080px;height:1920px;font-family:'Inter',Segoe UI,Roboto,sans-serif;overflow:hidden;background:transparent}
.lower{position:absolute;left:56px;bottom:150px;right:56px}
.kick{display:inline-block;background:#1E88D6;color:#fff;font-size:26px;font-weight:800;letter-spacing:2px;padding:12px 26px;border-radius:12px;margin-bottom:22px;box-shadow:0 10px 30px rgba(30,136,214,.45)}
.ttl{font-size:74px;font-weight:900;color:#fff;letter-spacing:-1.5px;line-height:1.02;text-shadow:0 4px 30px rgba(6,18,28,.65),0 2px 6px rgba(6,18,28,.5)}
.sub{font-size:36px;font-weight:600;color:#EAF2FA;margin-top:18px;text-shadow:0 3px 16px rgba(6,18,28,.8)}
.scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(6,18,28,.55) 0%,rgba(6,18,28,.12) 34%,transparent 55%)}
/* center title */
.center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:24px}
.center .brand{font-size:104px;font-weight:900;color:#fff;letter-spacing:-2px;text-shadow:0 6px 40px rgba(6,18,28,.7)}
.center .tag{font-size:44px;font-weight:600;color:#EAF2FA;text-shadow:0 3px 20px rgba(6,18,28,.8)}
.center .pill{margin-top:10px;font-size:30px;font-weight:800;letter-spacing:2px;color:#0C1622;background:#F0A431;padding:16px 34px;border-radius:999px}
`;
const logo = (c='#fff',s=132)=>`<svg width="${s}" height="${s}" viewBox="0 0 100 100"><path d="M50 22 L74 62 H26 Z" fill="${c}"/><path d="M50 40 L62 62 H38 Z" fill="${c}" opacity=".55"/><path d="M22 70 q8 -8 16 0 t16 0 t16 0" stroke="${c}" stroke-width="5" fill="none" stroke-linecap="round"/></svg>`;
const page = (inner)=>`<!doctype html><meta charset="utf-8"><style>${CSS}</style>${inner}`;

const lower=(kick,ttl,sub,scrim=true)=>page(`${scrim?'<div class="scrim"></div>':''}<div class="lower"><span class="kick">${kick}</span><div class="ttl">${ttl}</div><div class="sub">${sub}</div></div>`);

const items = {
  intro:  page(`<div class="center">${logo('#fff',150)}<div class="brand">WanderBuddy</div><div class="tag">Your whole trip. One app.</div></div>`),
  cap1: lower('FEATURE 01','Shared Itinerary','Plan every day together — updates live'),
  cap2: lower('FEATURE 02','Group Budget','Track expenses & split fairly'),
  cap3: lower('FEATURE 03','Group Chat','One thread for the whole crew'),
  cap4: lower('FEATURE 04','Shared Photos','Filter by place · download in HD'),
  cap5: lower('FEATURE 05','Live Translation','Talk with the locals, in real time'),
  cap6: lower('FEATURE 06','Live Location · Road-Trip','See who’s ahead, behind & how far'),
  cap7: lower('FEATURE 07','Discover & AI','Find real trips · plan with AI'),
  cap8: lower('FEATURE 08','Safety','Emergency help, one tap away'),
  cap9: lower('PRICING','Simple & honest','Free to start · no ads, ever'),
  endcard: page(`<div style="position:absolute;inset:0;background:linear-gradient(160deg,#0B141F,#14283b 60%,#0B141F)"></div><div class="center">${logo('#fff',170)}<div class="brand">WanderBuddy</div><div class="tag">Travel together, perfectly in sync.</div><div class="pill">FREE ON iOS &amp; ANDROID</div></div>`),
};
for (const [name, html] of Object.entries(items)){
  const f=path.join(OUT,name+'.html'); fs.writeFileSync(f,html);
  const png=path.join(OUT,name+'.png');
  cp.execSync(`"${CHROME}" --headless=new --hide-scrollbars --disable-gpu --force-device-scale-factor=1 --default-background-color=00000000 --window-size=1080,1920 --screenshot="${png}" "${f}"`,{stdio:'ignore'});
  console.log('cap',name);
}
console.log('DONE');
