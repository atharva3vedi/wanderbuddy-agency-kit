// Generates faithful WanderBuddy screen recreations (1080xH) and renders them to PNG
// via headless Chrome. Palette + styling mirror the real app (app_colors.dart) and the
// live screenshots captured from the emulator.
const fs = require('fs');
const cp = require('child_process');
const path = require('path');

const ROOT = __dirname;
const OUT = path.join(ROOT, 'ui', 'screens');
fs.mkdirSync(OUT, { recursive: true });
const PH = (n) => 'file:///' + path.join(ROOT, 'ui', 'photos', `p${n}.jpg`).replace(/\\/g, '/');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';

// ---- shared UI atoms -------------------------------------------------------
const statusbar = (dark = false) => `
<div class="sb ${dark ? 'd' : ''}">
  <div class="sb-time">9:41</div>
  <div class="sb-ic">
    <svg width="34" height="20" viewBox="0 0 34 20"><g fill="currentColor"><rect x="0" y="9" width="4" height="9" rx="1"/><rect x="6" y="6" width="4" height="12" rx="1"/><rect x="12" y="3" width="4" height="15" rx="1"/><rect x="18" y="0" width="4" height="18" rx="1"/></g></svg>
    <svg width="26" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 18.5a1.7 1.7 0 100 3.4 1.7 1.7 0 000-3.4zM4 10.7l1.9 1.9a8.6 8.6 0 0112.2 0L20 10.7a11.3 11.3 0 00-16 0zM.6 7.3L2.5 9.2a14 14 0 0119 0l1.9-1.9a16.7 16.7 0 00-22.7 0z"/></svg>
    <svg width="40" height="20" viewBox="0 0 40 20"><rect x="1" y="3" width="32" height="14" rx="4" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3.5" y="5.5" width="25" height="9" rx="2" fill="currentColor"/><rect x="35" y="7" width="3" height="6" rx="1.5" fill="currentColor"/></svg>
  </div>
</div>`;

const logoMark = (c = '#fff', s = 60) => `
<svg width="${s}" height="${s}" viewBox="0 0 100 100" fill="none">
  <path d="M50 22 L74 62 H26 Z" fill="${c}"/>
  <path d="M50 40 L62 62 H38 Z" fill="${c}" opacity=".55"/>
  <path d="M22 70 q8 -8 16 0 t16 0 t16 0" stroke="${c}" stroke-width="5" fill="none" stroke-linecap="round"/>
</svg>`;

const tabbar = (active) => {
  const tabs = ['Itinerary','Budget','Chat','Members','Photos','Translate','WanderBuddy'];
  return `<div class="tabs">${tabs.map(t=>`<div class="tab ${t===active?'on':''}">${t}</div>`).join('')}</div>`;
};

const base = (body, { h = 1920, dark = false, page } = {}) => `<!doctype html><html><head><meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  :root{
    --page:#F3F6F9; --subtle:#E5EEF5; --surface:#FFFFFF; --primary:#1E88D6; --onp:#fff;
    --accent:#E0972A; --teal:#1FA89A; --muted:#5E7386; --text:#0C1622; --border:#CFDCE6;
    --chip:#E4F1EC; --chipT:#0A3D38;
  }
  *{box-sizing:border-box;margin:0;padding:0;-webkit-font-smoothing:antialiased}
  html,body{width:1080px}
  body{font-family:'Inter',Segoe UI,Roboto,Helvetica,Arial,sans-serif;height:${h}px;
       background:${page || 'var(--page)'};color:var(--text);overflow:hidden}
  .sb{height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 44px 0 52px;color:#0C1622;font-weight:700}
  .sb.d{color:#E7F1FA}
  .sb-time{font-size:30px;letter-spacing:.5px}
  .sb-ic{display:flex;align-items:center;gap:12px}
  .appbar{height:104px;display:flex;align-items:center;gap:20px;padding:0 40px;font-size:40px;font-weight:800}
  .appbar .back{font-size:44px;font-weight:500;opacity:.9}
  .appbar .sp{flex:1}
  .appbar .act{font-size:34px;opacity:.7}
  .tabs{display:flex;gap:36px;padding:6px 40px 0;overflow:hidden;border-bottom:1.5px solid var(--border);white-space:nowrap}
  .tab{font-size:29px;font-weight:600;color:var(--muted);padding:20px 2px 24px;position:relative;flex:0 0 auto}
  .tab.on{color:var(--primary)}
  .tab.on:after{content:"";position:absolute;left:0;right:0;bottom:-1.5px;height:5px;border-radius:3px;background:var(--primary)}
  .wrap{padding:34px 40px}
  .card{background:var(--surface);border:1.5px solid var(--border);border-radius:30px;box-shadow:0 6px 22px rgba(20,45,70,.06)}
  .chip{display:inline-flex;align-items:center;background:var(--chip);color:var(--chipT);font-size:24px;font-weight:600;padding:10px 22px;border-radius:999px}
  .btn{background:var(--primary);color:#fff;font-weight:700;border-radius:999px;display:flex;align-items:center;justify-content:center}
  .muted{color:var(--muted)}
  h1.big{font-size:58px;font-weight:800;letter-spacing:-1px}
  .avrow{display:flex}
  .av{width:56px;height:56px;border-radius:50%;border:3px solid #fff;background:#cbd7e2;margin-left:-14px;display:flex;align-items:center;justify-content:center;font-weight:700;color:#fff;font-size:24px}
</style></head><body>${body}</body></html>`;

// ---- screens ---------------------------------------------------------------
const S = {};

// 1. ITINERARY (tall)
const itItem = (time, ic, title, sub, last=false) => `
<div class="it">
  <div class="it-t">${time}</div>
  <div class="it-rail"><div class="dot"></div>${last?'':'<div class="ln"></div>'}</div>
  <div class="it-c card"><div class="it-ic">${ic}</div><div><div class="it-ti">${title}</div><div class="muted it-sub">${sub}</div></div></div>
</div>`;
S.itinerary = base(`
${statusbar()}
<div class="appbar"><span class="back">‹</span>Iceland Ring Road <span class="sp"></span><span class="act">⋯</span></div>
<div style="padding:20px 40px 8px;display:flex;align-items:center;gap:24px">
  <div style="font-size:30px" class="muted">🇮🇸 Reykjavík · Sep 20 – Sep 29</div>
  <div class="sp" style="flex:1"></div>
  <div class="avrow"><div class="av" style="background:#1E88D6">A</div><div class="av" style="background:#1FA89A">M</div><div class="av" style="background:#E0972A">P</div><div class="av" style="background:#7A8CA3;font-size:22px">+9</div></div>
</div>
${tabbar('Itinerary')}
<div class="wrap" style="padding-top:24px">
  <div class="dayhdr">Day 1 · Sep 20</div>
  ${itItem('08:30','✈️','Flight to Keflavík','KEF · Icelandair 682')}
  ${itItem('11:00','🚐','Pick up camper van','Blue Car Rental')}
  ${itItem('14:00','🏨','Check in · Reykjavík Loft','Bankastræti 7')}
  ${itItem('17:00','🌅','Sun Voyager & harbour walk','Sæbraut',true)}
  <div class="dayhdr">Day 2 · Sep 21</div>
  ${itItem('09:00','💧','Þingvellir National Park','Golden Circle')}
  ${itItem('12:30','♨️','Geysir & Gullfoss falls','Haukadalur',true)}
</div>
<style>
  .dayhdr{font-size:34px;font-weight:800;color:var(--primary);margin:14px 6px 22px}
  .it{display:grid;grid-template-columns:120px 44px 1fr;gap:10px;align-items:stretch}
  .it-t{font-size:27px;font-weight:700;color:var(--muted);padding-top:34px;text-align:right}
  .it-rail{position:relative;display:flex;justify-content:center}
  .it-rail .dot{width:26px;height:26px;border-radius:50%;background:var(--primary);margin-top:34px;box-shadow:0 0 0 7px #DCEBF8}
  .it-rail .ln{position:absolute;top:60px;bottom:-18px;width:5px;background:var(--border);border-radius:3px}
  .it-c{display:flex;align-items:center;gap:24px;padding:26px 30px;margin-bottom:26px}
  .it-ic{width:74px;height:74px;border-radius:20px;background:var(--subtle);display:flex;align-items:center;justify-content:center;font-size:38px;flex:0 0 auto}
  .it-ti{font-size:33px;font-weight:700}
  .it-sub{font-size:26px;margin-top:6px}
</style>`, { h: 2380 });

// 2. BUDGET
const exp = (ic, title, who, amt, split) => `
<div class="exp card"><div class="it-ic">${ic}</div>
  <div style="flex:1"><div class="it-ti">${title}</div><div class="muted it-sub">Paid by ${who}${split?` · split ${split}`:''}</div></div>
  <div class="amt">${amt}</div></div>`;
S.budget = base(`
${statusbar()}
<div class="appbar"><span class="back">‹</span>Iceland Ring Road<span class="sp"></span></div>
${tabbar('Budget')}
<div class="wrap">
  <div class="card" style="padding:38px 40px;display:flex;align-items:center;gap:30px;margin-bottom:30px">
    <div><div class="muted" style="font-size:28px">Total trip spend</div><div style="font-size:78px;font-weight:800;letter-spacing:-2px">$4,820</div></div>
    <div class="sp" style="flex:1"></div>
    <div style="text-align:right"><div class="chip" style="background:#DFF3EC;color:#0A5C46">You're owed $85</div><div class="muted" style="font-size:26px;margin-top:14px">Your share · $402</div></div>
  </div>
  ${exp('⛽','Fuel — Ring Road','You','$120.00','12 ways')}
  ${exp('🏨','Reykjavík Loft · 2 nights','Ana','$640.00','')}
  ${exp('🍽️','Group dinner · Vík','Marco','$210.00','')}
  ${exp('♨️','Blue Lagoon tickets','You','$384.00','')}
  <div class="btn" style="height:104px;font-size:34px;margin-top:20px">Settle up</div>
</div>
<style>.exp{display:flex;align-items:center;gap:26px;padding:28px 32px;margin-bottom:24px}
.it-ic{width:74px;height:74px;border-radius:20px;background:var(--subtle);display:flex;align-items:center;justify-content:center;font-size:38px}
.it-ti{font-size:32px;font-weight:700}.it-sub{font-size:25px;margin-top:6px}.amt{font-size:36px;font-weight:800}</style>`);

// 3. CHAT (tall)
const inMsg = (name, col, txt) => `<div class="m in"><div class="av" style="background:${col};margin:0">${name[0]}</div><div><div class="nm">${name}</div><div class="bub">${txt}</div></div></div>`;
const outMsg = (txt) => `<div class="m out"><div class="bub o">${txt}</div></div>`;
const photoMsg = (n) => `<div class="m in"><div class="av" style="background:#E0972A;margin:0">P</div><div><div class="nm">Priya</div><img class="pbub" src="${PH(n)}"></div></div>`;
S.chat = base(`
${statusbar()}
<div class="appbar"><span class="back">‹</span>Iceland Ring Road<span class="sp"></span><span class="act">👥 12</span></div>
${tabbar('Chat')}
<div class="wrap" style="padding-top:30px">
  ${inMsg('Ana','#1E88D6','Camper van is booked! 🚐')}
  ${outMsg('Legend. Adding it to Day 1 now.')}
  ${inMsg('Marco','#1FA89A','Forecast is clear for Northern Lights on the 23rd 🤞')}
  ${photoMsg(4)}
  ${inMsg('Priya','#E0972A','Sunset at the harbour was unreal 🌅')}
  ${outMsg("Can't wait for this 🇮🇸")}
</div>
<div class="inbar"><div class="ipill">Message the crew…</div><div class="send">➤</div></div>
<style>
.m{display:flex;gap:20px;margin-bottom:30px;max-width:78%}
.m.in{align-self:flex-start}.wrap{display:flex;flex-direction:column}
.m.out{align-self:flex-end;margin-left:auto}
.nm{font-size:24px;font-weight:700;color:var(--muted);margin:0 0 8px 6px}
.bub{background:#fff;border:1.5px solid var(--border);padding:24px 30px;border-radius:30px 30px 30px 8px;font-size:31px;line-height:1.35;box-shadow:0 4px 14px rgba(20,45,70,.05)}
.bub.o{background:var(--primary);color:#fff;border:none;border-radius:30px 30px 8px 30px}
.pbub{width:360px;height:360px;object-fit:cover;border-radius:26px;margin-top:2px}
.inbar{position:absolute;bottom:0;left:0;right:0;height:130px;background:#fff;border-top:1.5px solid var(--border);display:flex;align-items:center;gap:22px;padding:0 40px}
.ipill{flex:1;height:82px;background:var(--subtle);border-radius:999px;display:flex;align-items:center;padding:0 34px;color:var(--muted);font-size:29px}
.send{width:82px;height:82px;border-radius:50%;background:var(--primary);color:#fff;display:flex;align-items:center;justify-content:center;font-size:34px}
</style>`, { h: 2200 });

// 4. PHOTOS GRID
S.photos_grid = base(`
${statusbar()}
<div class="appbar"><span class="back">‹</span>Photos<span class="sp"></span><span class="act">🗺️</span></div>
<div style="display:flex;align-items:center;gap:20px;padding:16px 40px 26px">
  <div class="chip" style="background:#fff;border:1.5px solid var(--border);color:var(--text);font-size:27px;padding:16px 28px">All places ▾</div>
  <div class="muted" style="font-size:27px">128 photos · 12 people</div>
  <div class="sp" style="flex:1"></div>
  <div class="chip" style="background:var(--primary);color:#fff">⬇ HD</div>
</div>
<div class="grid">${[1,2,3,4,5,6,7,8,9,1,2,3].map((n,i)=>`<div class="ph"><img src="${PH(n)}">${i===0?'<span class="hd">HD</span>':''}</div>`).join('')}</div>
<style>.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:0 8px}
.ph{position:relative;aspect-ratio:1;overflow:hidden}.ph img{width:100%;height:100%;object-fit:cover}
.hd{position:absolute;top:14px;right:14px;background:rgba(12,22,34,.72);color:#fff;font-size:20px;font-weight:700;padding:6px 14px;border-radius:8px}</style>`);

// 4b. PHOTOS MAP (dark)
S.photos_map = base(`
${statusbar(true)}
<div class="appbar" style="color:#E7F1FA"><span class="back">‹</span>Photo map<span class="sp"></span><span class="act">▦</span></div>
<div class="map">
  <div class="road r1"></div><div class="road r2"></div><div class="road r3"></div>
  ${[[300,520,1],[720,430,2],[520,760,5],[820,980,6],[360,1050,4],[640,1240,9]].map(([x,y,n])=>`<div class="pin" style="left:${x}px;top:${y}px"><img src="${PH(n)}"></div>`).join('')}
  <div class="mcard"><div style="font-size:30px;font-weight:700">📍 Vík í Mýrdal</div><div class="muted" style="font-size:25px;color:#8DA7BC;margin-top:6px">18 photos · tap a pin to view</div></div>
</div>
<style>body{background:#0B141F}
.map{position:absolute;inset:104px 0 0;background:radial-gradient(1200px 900px at 40% 30%,#16293b,#0B141F 70%);overflow:hidden}
.road{position:absolute;height:10px;background:#24384c;border-radius:6px;filter:blur(.5px)}
.r1{width:900px;top:600px;left:-60px;transform:rotate(-14deg)}
.r2{width:760px;top:900px;left:200px;transform:rotate(20deg)}
.r3{width:1000px;top:1200px;left:-40px;transform:rotate(-8deg)}
.pin{position:absolute;width:120px;height:120px;transform:translate(-50%,-50%)}
.pin img{width:100%;height:100%;object-fit:cover;border-radius:22px;border:5px solid #3FA7E6;box-shadow:0 10px 26px rgba(0,0,0,.5)}
.pin:after{content:"";position:absolute;left:50%;bottom:-16px;transform:translateX(-50%);border:14px solid transparent;border-top-color:#3FA7E6}
.mcard{position:absolute;left:40px;right:40px;bottom:60px;background:#17293B;border:1.5px solid #25394C;border-radius:28px;padding:34px 40px;color:#E7F1FA}</style>`);

// 5. TRANSLATE
S.translate = base(`
${statusbar()}
<div class="appbar"><span class="back">‹</span>Translate<span class="sp"></span></div>
${tabbar('Translate')}
<div class="wrap">
  <div class="langrow"><div class="lang">English ▾</div><div class="swap">⇄</div><div class="lang">Icelandic ▾</div></div>
  <div class="card" style="padding:38px 40px;margin-bottom:26px"><div class="muted" style="font-size:26px;margin-bottom:16px">You say</div><div style="font-size:40px;font-weight:600;line-height:1.3">Where is the nearest hot spring?</div></div>
  <div class="card" style="padding:38px 40px;background:#EAF4FC;border-color:#BFDDF4"><div style="display:flex;align-items:center;gap:16px;margin-bottom:16px"><div class="muted" style="font-size:26px;color:#1E88D6;font-weight:700">Icelandic</div><div class="sp" style="flex:1"></div><div style="font-size:36px">🔊</div></div><div style="font-size:44px;font-weight:700;line-height:1.3;color:#0C1622">Hvar er næsti heiti hver?</div></div>
  <div class="talk"><div class="mic">🎙️</div><div><div style="font-size:32px;font-weight:700">Talk to a local</div><div class="muted" style="font-size:25px">Two-way voice, hands-free</div></div></div>
</div>
<style>.langrow{display:flex;align-items:center;gap:24px;margin-bottom:30px}
.lang{flex:1;background:#fff;border:1.5px solid var(--border);border-radius:22px;padding:26px;text-align:center;font-size:31px;font-weight:700}
.swap{font-size:40px;color:var(--primary)}
.talk{display:flex;align-items:center;gap:26px;margin-top:34px;background:#fff;border:1.5px solid var(--border);border-radius:28px;padding:30px 36px}
.mic{width:88px;height:88px;border-radius:50%;background:var(--primary);color:#fff;display:flex;align-items:center;justify-content:center;font-size:40px}</style>`);

// 6. LIVE CONVERSATION
const lc = (name, col, lang, orig, tr) => `
<div class="lcm"><div class="av" style="background:${col};margin:0">${name[0]}</div>
 <div class="lcb"><div class="lch"><b>${name}</b><span class="lctag">${lang}</span></div>
  <div class="lco">${orig}</div><div class="lct">${tr}</div></div></div>`;
S.liveconv = base(`
${statusbar()}
<div class="appbar"><span class="back">‹</span>Live Conversation<span class="sp"></span><span class="live">● LIVE</span></div>
<div style="padding:10px 40px 4px;display:flex;gap:14px;flex-wrap:wrap">
  <div class="chip">🇬🇧 You · English</div><div class="chip">🇪🇸 Elena · Spanish</div><div class="chip">🇯🇵 Kenji · Japanese</div></div>
<div class="wrap" style="padding-top:24px">
  ${lc('Elena','#E0972A','ES → EN','¿Vamos a la playa mañana?','Shall we go to the beach tomorrow?')}
  ${lc('You','#1E88D6','EN','Yes — let’s meet at nine.','· sent to the room, translated live')}
  ${lc('Kenji','#1FA89A','JP → EN','海が本当に綺麗ですね','The sea is really beautiful.')}
</div>
<div class="listen"><div class="wave"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div><div style="font-size:30px;font-weight:700;color:var(--primary)">Listening — everyone in their own language</div></div>
<style>.live{color:#E5484D;font-size:26px;font-weight:800}
.lcm{display:flex;gap:22px;margin-bottom:34px}
.lcb{flex:1;background:#fff;border:1.5px solid var(--border);border-radius:28px;padding:26px 32px;box-shadow:0 4px 14px rgba(20,45,70,.05)}
.lch{display:flex;align-items:center;gap:16px;font-size:28px}.lctag{font-size:22px;color:var(--primary);background:#E7F2FB;padding:5px 16px;border-radius:999px;font-weight:700}
.lco{font-size:29px;color:var(--muted);margin:14px 0 6px}
.lct{font-size:35px;font-weight:700;line-height:1.3}
.listen{position:absolute;bottom:50px;left:40px;right:40px;background:#fff;border:1.5px solid var(--border);border-radius:28px;padding:30px;display:flex;align-items:center;gap:26px;justify-content:center}
.wave{display:flex;align-items:center;gap:8px;height:60px}
.wave span{width:9px;background:var(--primary);border-radius:6px}
.wave span:nth-child(1){height:24px}.wave span:nth-child(2){height:48px}.wave span:nth-child(3){height:34px}.wave span:nth-child(4){height:60px}.wave span:nth-child(5){height:30px}.wave span:nth-child(6){height:50px}.wave span:nth-child(7){height:22px}</style>`);

// 7. ROAD-TRIP (dark map)
S.roadtrip = base(`
${statusbar(true)}
<div class="appbar" style="color:#E7F1FA"><span class="back">‹</span>Road-trip mode<span class="sp"></span><span class="live">● LIVE</span></div>
<div class="map">
  <svg class="route" viewBox="0 0 1080 1500" preserveAspectRatio="none">
    <path d="M180 1280 C 360 1120, 260 900, 470 820 S 760 700, 700 470 S 820 240, 900 180" stroke="#3FA7E6" stroke-width="14" fill="none" stroke-linecap="round" opacity=".95"/>
  </svg>
  <div class="wp" style="left:900px;top:180px">🏁</div>
  <div class="me" style="left:470px;top:820px"><div class="ping"></div><b>You</b></div>
  <div class="mem b" style="left:700px;top:470px"><span></span>Ana</div>
  <div class="mem o" style="left:300px;top:1150px"><span></span>Marco</div>
  <div class="panel">
    <div class="pr"><div class="pd" style="background:#35C9BC"></div>Ana<span class="sp2"></span><b>4.2 km ahead</b> · 6 min</div>
    <div class="pr me2"><div class="pd" style="background:#3FA7E6"></div>You<span class="sp2"></span><b>on route</b></div>
    <div class="pr"><div class="pd" style="background:#E0972A"></div>Marco<span class="sp2"></span><b>2.1 km behind</b> · 3 min</div>
    <div class="nx">🏁 Next stop · Vík — 38 km to go</div>
  </div>
</div>
<style>body{background:#0B141F}
.map{position:absolute;inset:104px 0 0;background:radial-gradient(1100px 900px at 60% 25%,#16293b,#0B141F 72%);overflow:hidden}
.route{position:absolute;inset:0;width:100%;height:100%}
.wp{position:absolute;font-size:52px;transform:translate(-50%,-50%)}
.me,.mem{position:absolute;transform:translate(-50%,-50%);color:#fff;font-size:26px;font-weight:700;display:flex;flex-direction:column;align-items:center;gap:8px;text-shadow:0 2px 6px rgba(0,0,0,.6)}
.me .ping{width:38px;height:38px;border-radius:50%;background:#3FA7E6;box-shadow:0 0 0 12px rgba(63,167,230,.28)}
.mem span{width:34px;height:34px;border-radius:50%;display:block}
.mem.b span{background:#35C9BC;box-shadow:0 0 0 9px rgba(53,201,188,.25)}
.mem.o span{background:#E0972A;box-shadow:0 0 0 9px rgba(224,151,42,.25)}
.panel{position:absolute;left:36px;right:36px;bottom:54px;background:#17293B;border:1.5px solid #25394C;border-radius:30px;padding:34px 40px;color:#E7F1FA}
.pr{display:flex;align-items:center;gap:20px;font-size:31px;padding:16px 0;border-bottom:1px solid #22374a}
.pr.me2{color:#8FB8D8}.pr b{font-weight:800}.pd{width:26px;height:26px;border-radius:50%}.sp2{flex:1}
.nx{margin-top:20px;font-size:30px;font-weight:700;color:#3FA7E6}
.live{color:#E5484D;font-size:26px;font-weight:800}</style>`);

// 8. WANDERBUDDY AI
S.ai = base(`
${statusbar()}
<div class="appbar"><span class="back">‹</span>WanderBuddy AI<span class="sp"></span><span class="act">✨</span></div>
${tabbar('WanderBuddy')}
<div class="wrap" style="padding-top:30px">
  <div class="q">Plan a rainy day in Reykjavík ☔</div>
  <div class="a card">
    <div class="ai-h">✨ Here's a cosy rainy-day plan:</div>
    <div class="ai-l"><b>10:00</b> — Perlan museum & planetarium</div>
    <div class="ai-l"><b>12:30</b> — Lunch at Grandi food hall</div>
    <div class="ai-l"><b>14:30</b> — Reykjavík Art Museum</div>
    <div class="ai-l"><b>18:00</b> — Soak at Sky Lagoon</div>
    <div class="addbtn">✨ Add all to Day 4</div>
  </div>
  <div class="q">Any local dish we must try?</div>
</div>
<style>.wrap{display:flex;flex-direction:column}
.q{align-self:flex-end;background:var(--primary);color:#fff;font-size:31px;font-weight:600;padding:24px 32px;border-radius:30px 30px 8px 30px;margin-bottom:28px;max-width:74%}
.a{align-self:flex-start;max-width:90%;padding:34px 38px;margin-bottom:28px}
.ai-h{font-size:32px;font-weight:800;margin-bottom:22px}
.ai-l{font-size:30px;padding:14px 0;border-bottom:1px solid var(--border)}
.addbtn{margin-top:26px;background:#E7F2FB;color:#1E88D6;font-weight:800;font-size:30px;text-align:center;padding:26px;border-radius:20px}</style>`);

// 9. SAFETY
S.safety = base(`
${statusbar()}
<div class="appbar"><span class="back">‹</span>Safety<span class="sp"></span></div>
<div class="wrap" style="padding-top:20px">
  <div class="sos"><div class="sos-i">🆘</div><div><div style="font-size:40px;font-weight:800">Emergency SOS</div><div style="font-size:27px;opacity:.9">Call local services & alert your crew</div></div></div>
  <div class="srow card"><div class="it-ic">📞</div><div style="flex:1"><div class="it-ti">Local emergency</div><div class="muted it-sub">Iceland · Police, Fire, Ambulance</div></div><div class="call">112</div></div>
  <div class="srow card"><div class="it-ic">🏥</div><div style="flex:1"><div class="it-ti">Nearest hospital</div><div class="muted it-sub">Landspítali · 2.4 km</div></div><div class="act2">Go</div></div>
  <div class="srow card"><div class="it-ic">🏛️</div><div style="flex:1"><div class="it-ti">Your embassy</div><div class="muted it-sub">Reykjavík · consular contacts</div></div><div class="act2">View</div></div>
  <div class="srow card"><div class="it-ic">📵</div><div style="flex:1"><div class="it-ti">Stolen-phone checklist</div><div class="muted it-sub">Lock, wipe, report — step by step</div></div><div class="act2">Open</div></div>
</div>
<style>.sos{display:flex;align-items:center;gap:28px;background:linear-gradient(135deg,#E5484D,#B4262B);color:#fff;border-radius:30px;padding:40px 40px;margin-bottom:34px;box-shadow:0 12px 30px rgba(200,40,45,.32)}
.sos-i{font-size:64px}
.srow{display:flex;align-items:center;gap:26px;padding:30px 34px;margin-bottom:24px}
.it-ic{width:80px;height:80px;border-radius:22px;background:var(--subtle);display:flex;align-items:center;justify-content:center;font-size:40px}
.it-ti{font-size:33px;font-weight:700}.it-sub{font-size:25px;margin-top:6px}
.call{background:#E5484D;color:#fff;font-weight:800;font-size:34px;padding:16px 34px;border-radius:999px}
.act2{color:var(--primary);font-weight:700;font-size:30px}</style>`);

// 10. COMPARE (Free vs Premium)
const crow = (label, free, prem, hi=false) => `
<div class="crow ${hi?'hi':''}"><div class="cl">${label}</div><div class="cf">${free}</div><div class="cp">${prem}</div></div>`;
S.compare = base(`
${statusbar()}
<div style="text-align:center;padding:50px 40px 10px"><h1 class="big">Free is genuinely free.</h1><div class="muted" style="font-size:32px;margin-top:14px">Premium unlocks scale for bigger crews.</div></div>
<div class="wrap" style="padding-top:30px">
  <div class="chead"><div class="cl"></div><div class="cf">Free</div><div class="cp">Premium ★</div></div>
  ${crow('Trip members','10','100','hi')}
  ${crow('Shared storage','2 GB','27 GB','hi')}
  ${crow('Itinerary, budget & chat','✓','✓')}
  ${crow('Live translation','✓','✓')}
  ${crow('HD photo download','✓','✓')}
  ${crow('Road-trip live location','✓','✓')}
  ${crow('Ads','None','None')}
</div>
<style>.chead,.crow{display:grid;grid-template-columns:1.5fr 1fr 1fr;align-items:center;text-align:center}
.chead{padding:0 10px 22px;font-size:30px;font-weight:800}
.chead .cp,.crow .cp{color:#1E88D6}
.chead .cl{text-align:left}
.crow{background:#fff;border:1.5px solid var(--border);border-radius:22px;padding:30px 24px;margin-bottom:18px;font-size:32px}
.crow .cl{text-align:left;font-weight:600;padding-left:14px}
.crow .cf{color:var(--muted);font-weight:700}
.crow .cp{font-weight:800}
.crow.hi{border-color:#8FC5EE;background:#F1F8FE}
.crow.hi .cp{font-size:40px}</style>`);

// 11. PRICING
S.pricing = base(`
${statusbar()}
<div style="text-align:center;padding:56px 40px 6px">${logoMark('#1E88D6',72)}<h1 class="big" style="margin-top:20px">Go Premium</h1><div class="muted" style="font-size:30px;margin-top:12px">Cancel anytime · No ads, ever</div></div>
<div class="wrap" style="padding-top:34px">
  <div class="plan"><div><div class="pt">Monthly</div><div class="ps muted">Billed monthly</div></div><div class="pp">$6.99<span>/mo</span></div></div>
  <div class="plan best"><div class="badge">BEST VALUE · SAVE 28%</div><div><div class="pt">Yearly</div><div class="ps">Just $5.00 / month</div></div><div class="pp">$59.99<span>/yr</span></div></div>
  <div class="plan"><div><div class="pt">Lifetime</div><div class="ps muted">Pay once, yours forever</div></div><div class="pp">$100<span></span></div></div>
  <div class="btn cta">Start 7-day free trial</div>
  <div class="muted" style="text-align:center;font-size:26px;margin-top:24px">Then your plan renews. Cancel in one tap.</div>
</div>
<style>.plan{background:#fff;border:2px solid var(--border);border-radius:28px;padding:38px 40px;margin-bottom:26px;display:flex;align-items:center;position:relative}
.plan .pt{font-size:38px;font-weight:800}.plan .ps{font-size:27px;margin-top:8px;color:#1FA89A;font-weight:700}
.plan .pp{margin-left:auto;font-size:52px;font-weight:800}.plan .pp span{font-size:28px;color:var(--muted);font-weight:600}
.plan.best{border-color:#1E88D6;background:#F1F8FE;box-shadow:0 14px 34px rgba(30,136,214,.16)}
.badge{position:absolute;top:-22px;left:40px;background:#1E88D6;color:#fff;font-size:22px;font-weight:800;letter-spacing:.5px;padding:9px 22px;border-radius:999px}
.cta{height:120px;font-size:38px;margin-top:16px;box-shadow:0 14px 30px rgba(30,136,214,.3)}</style>`);

// ---- render ----------------------------------------------------------------
const heights = { itinerary:2380, chat:2200 };
const order = Object.keys(S);
for (const name of order) {
  const file = path.join(OUT, name + '.html');
  fs.writeFileSync(file, S[name]);
  const h = heights[name] || 1920;
  const png = path.join(OUT, name + '.png');
  cp.execSync(`"${CHROME}" --headless=new --hide-scrollbars --disable-gpu --force-device-scale-factor=1 --default-background-color=00000000 --window-size=1080,${h} --screenshot="${png}" "${file}"`, { stdio: 'ignore' });
  console.log('rendered', name, h);
}
console.log('DONE', order.length);
