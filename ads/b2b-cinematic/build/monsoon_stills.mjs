// Film "Monsoon": the paper and the phone of the agency that does it all by hand.
// Set dressing drawn in Chrome, not product UI, and no real app's look or name.
//   node build/monsoon_stills.mjs -> screens/monsoon/props/*.png, lockN.png
import puppeteer from 'puppeteer-core';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AD = path.resolve(HERE, '..');
const OUT = path.join(AD, 'screens', 'monsoon', 'props');
mkdirSync(OUT, { recursive: true });
const hand = "font-family:'Bradley Hand',cursive;font-weight:700;color:#18222E";
const paper = 'background:#FBFBF9;';
const sys = "-apple-system,'Helvetica Neue',Arial";

const sticky = (bg, body, size = 60) => [`<div style="width:600px;height:600px;background:${bg};box-sizing:border-box;padding:64px 50px;${hand};font-size:${size}px;line-height:1.18">${body}</div>`, 600, 600];
const table = (title, file, rows) => [`<div style="width:1240px;height:1754px;${paper}box-sizing:border-box;padding:110px 90px;font:23px Arial,Helvetica,sans-serif;color:#222">
  <div style="font:bold 34px Arial">${title}</div><div style="color:#555;margin:6px 0 34px">${file} &nbsp; Sheet 1 &nbsp; USD</div>
  <table style="border-collapse:collapse;width:100%"><tr style="background:#e8ebee;font-weight:bold">${['Supplier', 'Item', 'Nights', 'Rate', 'Notes'].map((h) => `<td style="border:1px solid #c9ced4;padding:9px 10px">${h}</td>`).join('')}</tr>
  ${rows.map((r, i) => `<tr style="${i % 4 === 1 ? 'background:rgba(30,136,214,.2)' : ''}">${r.map((c, j) => `<td style="border:1px solid #c9ced4;padding:9px 10px;${j === 3 ? 'text-align:right' : ''}${j === 4 ? 'color:#2a5d9c;font-style:italic' : ''}">${c}</td>`).join('')}</tr>`).join('')}</table>
  <div style="${hand};font-size:46px;margin-top:70px;transform:rotate(-3deg)">which version is right??<br>ask boat guy again</div></div>`, 1240, 1754];
const lorem = 'Pick up from airport and transfer to hotel. Check in and free time at leisure. Evening walk to the night market (own expense). Overnight at hotel. Remark: room is subject to availability, check in time 14:00, early check in not guaranteed. Please send passport copy and confirm flight details with the team before departure. ';
const pdf = (title, file, days) => [`<div style="width:1754px;height:1240px;${paper}box-sizing:border-box;padding:80px 110px;font:22px 'Times New Roman',serif;color:#333;position:relative;overflow:hidden">
  <div style="text-align:center;font:bold 40px 'Times New Roman';text-decoration:underline">${title}</div>
  <div style="text-align:center;margin:10px 0 30px;color:#666">${file} &nbsp;&nbsp; page 1 of 9</div>
  <div style="columns:2;column-gap:60px;text-align:justify;line-height:1.32">${days.map((d) => `<p><b>${d}</b><br>${lorem}${lorem.slice(0, 180)}</p>`).join('')}</div></div>`, 1754, 1240];
const passport = (name, no) => [`<div style="width:1250px;height:880px;background:#EEF1EE;box-sizing:border-box;padding:60px 70px;font:30px Menlo,monospace;color:#28323c;position:relative">
  <div style="font:700 34px ${sys};letter-spacing:8px;color:#5b6772">PASSPORT &nbsp; COPY</div>
  <div style="display:flex;gap:60px;margin-top:50px"><div style="width:300px;height:390px;background:linear-gradient(#c9d2d8,#aab5bd);position:relative;overflow:hidden"><div style="position:absolute;left:90px;top:70px;width:120px;height:120px;border-radius:50%;background:#7d8a94"></div><div style="position:absolute;left:35px;top:215px;width:230px;height:260px;border-radius:50% 50% 0 0;background:#7d8a94"></div></div>
  <div style="line-height:1.9">Surname<br><b>${name.split(' ')[0]}</b><br>Given names<br><b>${name.split(' ').slice(1).join(' ')}</b><br>Passport no.<br><b>${no}</b></div></div>
  <div style="position:absolute;left:70px;right:70px;bottom:60px;font-size:32px;letter-spacing:3px;color:#4a5560">P&lt;XXX${name.replace(/ /g, '&lt;&lt;').toUpperCase()}&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;<br>${no}&lt;4XXX9001012F3101011&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;06</div>
  <div style="position:absolute;right:60px;top:50px;${hand};font-size:44px;transform:rotate(6deg);color:#2a5d9c">which trip??</div></div>`, 1250, 880];
const transfer = (amt, from, note) => [`<div style="width:700px;height:1500px;background:#F4F6F8;box-sizing:border-box;padding:90px 60px;font:34px ${sys};color:#1d2733">
  <div style="font-weight:600;color:#6b7783;font-size:30px">Transfer received</div>
  <div style="font:700 96px ${sys};margin:40px 0 10px">US$${amt}</div><div style="color:#2a8a57;font-weight:600">Completed</div>
  <div style="margin-top:90px;line-height:2.1;border-top:2px solid #d9dee3;padding-top:40px">From<br><b>${from}</b><br>Reference<br><b>${note}</b><br>Date<br><b>10 Nov 2026</b></div>
  <div style="${hand};font-size:56px;margin-top:90px;transform:rotate(-4deg);color:#24507f">for which booking?</div></div>`, 700, 1500];
const chat = (who, lines) => [`<div style="width:700px;height:1500px;background:#E9EEF1;box-sizing:border-box;font:36px/1.25 ${sys};color:#16202a">
  <div style="background:#2F6E63;color:#fff;padding:64px 44px 34px;font-weight:600;font-size:40px">${who}</div>
  <div style="padding:40px 34px">${lines.map(([me, t, at]) => `<div style="display:flex;justify-content:${me ? 'flex-end' : 'flex-start'};margin-bottom:26px"><div style="max-width:78%;background:${me ? '#D6F0DC' : '#fff'};border-radius:26px;padding:22px 28px;box-shadow:0 2px 3px rgba(0,0,0,.08)">${t}<div style="text-align:right;font-size:24px;color:#7a8690;margin-top:6px">${at}</div></div></div>`).join('')}</div></div>`, 700, 1500];
const items = {
  sticky_tan: sticky('#CFE3F6', 'call Mr Tan<br>back!!<br><span style="font-size:48px">(3rd time)</span>'),
  sticky_paid: sticky('#CDEBE4', 'who paid<br>$420 ??'),
  sticky_pass: sticky('#DCEBF9', 'Ana passport<br>still missing', 56),
  sticky_boat: sticky('#CFE3F6', 'Komodo boat<br>full on 23rd?'),
  sticky_quote: sticky('#CDEBE4', 'send quote v3<br>to the Lees<br>TODAY', 56),
  sticky_date: sticky('#DCEBF9', '23 or 24 Nov??<br>check chat'),
  rates_komodo: table('Komodo rates 2026', 'rates_komodo_v4_FINAL.xlsx', [['Phinisi, 3 nights', 'Per cabin', '3', '840', ''], ['Ranger fee, Komodo', 'Per person', '1', '22', 'cash only'], ['Airport transfer LBJ', 'Van', '2', '35', ''], ['Padar sunrise hike', 'Per person', '1', '0', ''], ['Snorkel gear', 'Per set', '3', '18', 'ask'], ['Hotel, Labuan Bajo', 'Twin', '1', '64', 'late c/o?'], ['Trip captain', 'Per day', '4', '60', '']]),
  rates_angkor: table('Angkor rates 2026', 'angkor_rates_new(2).xlsx', [['Temple pass, 3 days', 'Per person', '3', '62', ''], ['Tuk-tuk, sunrise', 'Per day', '2', '25', ''], ['Hotel, Siem Reap', 'Twin, pool', '2', '58', 'full 23rd?'], ['Guide, licensed', 'Per day', '2', '45', ''], ['Tonle Sap boat', 'Per person', '1', '20', ''], ['Airport transfer SAI', 'Van', '2', '30', '']]),
  pdf_angkor: pdf('ANGKOR WAT TOUR PACKAGE 3D2N', 'ITINERARY_Angkor_v7_FINAL(2).pdf', ['DAY 1 ARRIVAL SIEM REAP', 'DAY 2 ANGKOR WAT SUNRISE', 'DAY 3 TONLE SAP / DEPARTURE']),
  pdf_sapa: pdf('SAPA TREKKING PACKAGE 3D2N', 'Sapa_trek_itinerary_NEW_final.pdf', ['DAY 1 HANOI TO SAPA', 'DAY 2 LAO CHAI TA VAN TREK', 'DAY 3 FANSIPAN / RETURN']),
  pdf_komodo: pdf('KOMODO SAILING TRIP 4D3N', 'komodo_sailing_v3_clientcopy.pdf', ['DAY 1 LABUAN BAJO, BOARD BOAT', 'DAY 2 PADAR ISLAND SUNRISE', 'DAY 3 KOMODO, PINK BEACH', 'DAY 4 MANTA POINT / RETURN']),
  passport_a: passport('TAN WEI LING', 'K4471209'),
  passport_b: passport('COSTA ANA MARIA', 'P7730518'),
  passport_c: passport('WALKER THOMAS', 'N2284670'),
  transfer_a: transfer('420.00', 'K. TAN', '(none)'),
  transfer_b: transfer('1,100.00', 'T WALKER', 'trip deposit'),
  chat_a: chat('+65 9xxx 2231', [[0, 'Hi how much for 4 pax Komodo?', '21:02'], [0, 'Also can we change date to 23?', '21:03'], [1, 'Let me check and revert', '23:40'], [0, 'Hello?', '08:15']]),
  chat_b: chat('Ana (Angkor??)', [[0, 'Passport pics attached', '14:20'], [0, 'Did you get them?', '18:44'], [1, 'Sorry which trip is this for', '09:02']]),
  chat_c: chat('Tom W', [[0, 'Sent the transfer, pls check', '10:11'], [0, 'Can you confirm our booking?', '16:30'], [0, '??', '21:54']]),
  chat_d: chat('Unknown number', [[0, 'Is Sapa trek OK for kids?', '07:48'], [0, 'And price for 2 adults 2 kids', '07:49']]),
  boarding: [`<div style="width:480px;height:1140px;background:#F4F6F8;box-sizing:border-box;padding:56px 44px;font:26px Menlo,monospace;color:#1d2733;line-height:1.5"><div style="font:bold 30px Menlo;letter-spacing:2px">BOARDING PASS</div><br>SINGAPORE SIN<br>&rarr; LABUAN BAJO LBJ<br><br>23 NOV 07:15<br>SEAT 9C<br>GATE 12<br><br><div style="height:260px;background:repeating-linear-gradient(90deg,#1d2733 0 3px,transparent 3px 7px,#1d2733 7px 9px,transparent 9px 14px)"></div></div>`, 480, 1140],
  sheet: [`<div style="width:1754px;height:1240px;background:#fff;box-sizing:border-box;padding:40px;font:20px Arial;color:#222"><div style="font:bold 26px Arial;color:#1d6f42;margin-bottom:14px">bookings_NOV_master_v9 (Mai's copy).xlsx</div><table style="border-collapse:collapse;width:100%">${Array.from({ length: 26 }, (_, r) => `<tr>${Array.from({ length: 9 }, (_, c) => `<td style="border:1px solid #cfd4d9;padding:7px 8px;height:22px;${r === 0 ? 'background:#e8ebee;font-weight:bold' : (r * 7 + c * 3) % 11 === 0 ? 'background:#fff3b0' : (r + c) % 13 === 0 ? 'background:#f8c9c9' : ''}">${r === 0 ? ['Name', 'Trip', 'Date', 'Pax', 'Quote', 'Paid?', 'Passport', 'Notes', 'Who'][c] : c === 0 ? ['Tan', 'Costa', 'Walker', 'Lee', 'Novak', 'Becker', 'Rossi'][r % 7] : c === 1 ? ['Komodo', 'Angkor', 'Sapa', 'Penang', 'L. Prabang'][r % 5] : c === 5 ? ['?', 'yes', 'half', '', '??'][r % 5] : c === 6 ? ['', 'ok', 'missing', ''][r % 4] : ''}</td>`).join('')}</tr>`).join('')}</table></div>`, 1754, 1240],
};
const NOTES = ['How much for 4 pax Komodo?', 'Sent the transfer, pls check', 'Passport pics attached', 'Can we change to the 23rd?', 'Is Sapa OK for kids?', 'Hello??', 'Pls confirm our booking', 'Do you have Penang food trip Dec?'];
const lock = (n, shown) => `<body style="margin:0;width:1290px;height:2796px;overflow:hidden;background:radial-gradient(120% 70% at 50% 0%,#1B2B3F 0%,#0B121B 60%,#070B11 100%)">
  <div style="text-align:center;padding-top:230px;font:500 62px ${sys};color:rgba(255,255,255,.82)">Tuesday 10 November</div>
  <div style="text-align:center;font:600 300px/1.05 ${sys};color:#fff;letter-spacing:-6px">21:${String(14 + shown * 3).padStart(2, '0')}</div>
  <div style="margin-top:110px">${NOTES.slice(0, shown).reverse().map((t, k) => `<div style="margin:0 44px 18px;padding:28px 34px;border-radius:48px;background:rgba(255,255,255,${k === 0 ? 0.2 : 0.11});display:flex;gap:26px;align-items:center"><svg width="70" height="70" viewBox="0 0 24 24" style="flex:none"><rect width="24" height="24" rx="6" fill="${k % 3 === 2 ? '#B0477E' : '#3E9B6B'}"/><path d="M6 7.5h12a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-6.2L8.5 18v-2.5H6a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1z" fill="#fff"/></svg><div style="font:400 ${k === 0 ? 54 : 46}px/1.15 ${sys};color:#fff">${t}</div></div>`).join('')}</div>
  <div style="position:absolute;left:0;right:0;bottom:170px;text-align:center"><span style="display:inline-block;background:#D8453C;color:#fff;font:700 110px ${sys};padding:26px 70px;border-radius:120px">${n} unread</span></div></body>`;

const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--force-color-profile=srgb'] });
try {
  const p = await b.newPage();
  const tmp = path.join(AD, 'render', '_monsoon.html');
  for (const [k, [html, w, h]] of Object.entries(items)) {
    writeFileSync(tmp, `<!doctype html><meta charset=utf-8><style>html,body{margin:0}</style>${html}`);
    await p.setViewport({ width: w, height: h, deviceScaleFactor: 0.5 });
    await p.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0' });
    await p.screenshot({ path: path.join(OUT, `${k}.png`), clip: { x: 0, y: 0, width: w, height: h } });
  }
  await p.setViewport({ width: 1290, height: 2796, deviceScaleFactor: 1 });
  for (const [i, [n, shown]] of [[12, 3], [47, 5], [113, 8]].entries()) {
    writeFileSync(tmp, `<!doctype html><meta charset=utf-8>${lock(n, shown)}`);
    await p.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0' });
    await p.screenshot({ path: path.join(AD, 'screens', 'monsoon', `lock${i}.png`) });
  }
  writeFileSync(path.join(OUT, 'sizes.json'), JSON.stringify(Object.fromEntries(Object.entries(items).map(([k, [, w, h]]) => [k, [w, h]]))));
  console.log('wrote', Object.keys(items).length, 'props and 3 lock screens');
} finally { await b.close(); }
