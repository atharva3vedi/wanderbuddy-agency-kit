// Film "The Reel": her phone. Set dressing drawn in Chrome: a plain chat with a shared reel
// (the app's own Ha Giang photo) and her question. No real app's look or name.
//   node build/reel_stills.mjs -> screens/reel/reel_dm.png (1290 x 2796)
import puppeteer from 'puppeteer-core';
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const AD = path.resolve(HERE, '..');
const sys = "-apple-system,'Helvetica Neue',Arial";
const PHOTO = 'https://wgzwrrrfzxdnkrfebkqb.supabase.co/storage/v1/object/public/trip-images/showcase/hagiang.jpg';
const html = `<body style="margin:0;width:1290px;height:2796px;overflow:hidden;background:#0E141B;position:relative;font-family:${sys}">
  <div style="padding:150px 56px 44px;display:flex;align-items:center;gap:30px;border-bottom:2px solid rgba(255,255,255,.08)">
    <div style="width:104px;height:104px;border-radius:50%;background:#1E4E8C;color:#fff;font:700 40px ${sys};display:flex;align-items:center;justify-content:center">LT</div>
    <div><div style="font:600 54px ${sys};color:#fff">Lantern Trips</div><div style="font:400 38px ${sys};color:rgba(255,255,255,.55);margin-top:4px">Travel agency · Hanoi</div></div></div>
  <div style="text-align:center;font:500 36px ${sys};color:rgba(255,255,255,.45);margin:60px 0 34px">Wednesday 23:40</div>
  <div style="display:flex;justify-content:flex-end;padding:0 56px">
    <div style="width:640px;border-radius:44px;overflow:hidden;background:#17212C">
      <div style="height:900px;background:url('${PHOTO}') center/cover;position:relative">
        <div style="position:absolute;left:36px;top:34px;font:600 34px ${sys};color:#fff;background:rgba(0,0,0,.45);padding:10px 22px;border-radius:40px">Reel</div>
        <div style="position:absolute;left:50%;top:50%;width:150px;height:150px;margin:-75px 0 0 -75px;border-radius:50%;background:rgba(0,0,0,.45)"><div style="position:absolute;left:58px;top:42px;border-left:54px solid #fff;border-top:33px solid transparent;border-bottom:33px solid transparent"></div></div></div>
      <div style="padding:30px 36px 36px;font:400 40px/1.25 ${sys};color:rgba(255,255,255,.86)">The Ha Giang loop with easy riders: Ma Pi Leng Pass, the Nho Que river, homestays</div></div></div>
  <div style="display:flex;justify-content:flex-end;padding:30px 56px 0">
    <div style="max-width:900px;background:#2E6BD6;color:#fff;border-radius:52px;padding:34px 44px;font:400 58px/1.2 ${sys}">Could you do this for 4 of us in January? 5 nights.</div></div>
  <div style="text-align:right;padding:16px 70px 0;font:400 34px ${sys};color:rgba(255,255,255,.45)">Delivered</div>
  <div style="position:absolute;left:44px;right:44px;bottom:120px;height:130px;border-radius:70px;border:2px solid rgba(255,255,255,.16);display:flex;align-items:center;padding:0 54px;font:400 44px ${sys};color:rgba(255,255,255,.4)">Message</div></body>`;
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--force-color-profile=srgb'] });
try {
  const p = await b.newPage();
  await p.setViewport({ width: 1290, height: 2796, deviceScaleFactor: 1 });
  const tmp = path.join(AD, 'render', '_reel.html');
  writeFileSync(tmp, `<!doctype html><meta charset=utf-8>${html}`);
  await p.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0' });
  await p.screenshot({ path: path.join(AD, 'screens', 'reel', 'reel_dm.png') });
  console.log('wrote reel_dm');
} finally { await b.close(); }
