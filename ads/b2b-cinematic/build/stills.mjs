// Flat textures and text layers, drawn in Chrome with the real brand fonts.
//   node build/stills.mjs atlas         -> screens/flap_atlas.png (split-flap glyphs)
//   node build/stills.mjs supers <film> -> render/<film>/supers/<n>.png (transparent, 1080x1920)
import puppeteer from 'puppeteer-core';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AD = path.resolve(HERE, '..');
const FONTS = path.resolve(AD, '../../../metrics/fonts');
const face = (n, f, w, s = 'normal') => `@font-face{font-family:${n};src:url('${pathToFileURL(path.join(FONTS, f)).href}');font-weight:${w};font-style:${s}}`;
const CSS = face('WbSans', 'WbSans-Regular.ttf', 400) + face('WbSans', 'WbSans-SemiBold.ttf', 600) +
  face('WbSans', 'WbSans-Bold.ttf', 700) + face('Serif', 'InstrumentSerif-Italic.ttf', 400, 'italic');

export const DRUM = " ABCDEFGHIJKLMNOPQRSTUVWXYZ9876543210.:-,'&/";
const COLS = 8, ROWS = 6, CW = 200, CH = 300;

const [mode, film] = process.argv.slice(2);
const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new', args: ['--allow-file-access-from-files', '--force-color-profile=srgb', '--font-render-hinting=none'],
});
const page = await browser.newPage();
const tmp = path.join(AD, 'render', '_page.html');
mkdirSync(path.dirname(tmp), { recursive: true });

async function shoot(html, w, h, out) {
  writeFileSync(tmp, `<!doctype html><meta charset=utf-8><style>${CSS} html,body{margin:0;background:transparent}</style>${html}`);
  await page.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0' });
  await page.evaluate(async () => { await document.fonts.ready; for (const f of document.fonts) await f.load(); });
  await page.evaluate(() => window.__draw && window.__draw());
  await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  console.log('wrote', out);
}

try {
  if (mode === 'atlas') {
    // White glyphs on transparent, one per cell, cap height centred on the cell's middle
    // so the hinge line cuts every letter in half, as on a Solari board.
    const html = `<canvas id=c width=${COLS * CW} height=${ROWS * CH}></canvas><script>
      window.__draw = async () => { await document.fonts.load('700 230px WbSans'); const g = c.getContext('2d'); const D = ${JSON.stringify(DRUM)};
        g.fillStyle = '#fff'; g.font = '700 230px WbSans'; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
        const cap = g.measureText('H').actualBoundingBoxAscent;
        for (let i = 0; i < D.length; i++) { const x = (i % ${COLS}) * ${CW} + ${CW / 2}, y = Math.floor(i / ${COLS}) * ${CH} + ${CH / 2};
          g.save(); g.translate(x, y + cap / 2); g.scale(0.8, 1); g.fillText(D[i], 0, 0); g.restore(); } };</script>`;
    await shoot(html, COLS * CW, ROWS * CH, path.join(AD, 'screens', 'flap_atlas.png'));
  } else if (mode === 'props') {
    // Film 2's desk: the paper an agency's week is made of. Set dressing, not product UI.
    const out = path.join(AD, 'screens', 'props');
    mkdirSync(out, { recursive: true });
    const hand = "font-family:'Bradley Hand',cursive;font-weight:700;color:#18222E";
    const photo = pathToFileURL(path.join(AD, 'screens', 'krabi_photo.png')).href;
    const paper = 'background:#FBFBF9;';
    const sticky = (bg, body, size = 64) => [`<div style="width:600px;height:600px;background:${bg};box-sizing:border-box;padding:70px 56px;${hand};font-size:${size}px;line-height:1.18">${body}</div>`, 600, 600];
    const rows = [
      ['Andaman Breeze Hotel', 'Twin, breakfast', '2', '2,400', ''],
      ['Klong Muang Garden Resort', 'Twin, pool view', '2', '3,100', 'ask re late c/o'],
      ['Longtail, Hong Islands', 'Per boat, 8 max', '1', '3,500', ''],
      ['Speedboat, Phi Phi', 'Per seat', '1', '1,450', 'park fee cash'],
      ['Mangrove kayak', 'Per person', '1', '900', ''],
      ['Airport transfer KBV', 'Van, 10 seats', '2', '1,200', ''],
      ['Cooking class', 'Per person', '1', '1,100', 'veg ok?'],
      ['Emerald Pool + hot springs', 'Per person', '1', '650', ''],
      ['Farewell dinner', 'Per person', '1', '800', ''],
      ['Trip captain', 'Per day', '5', '2,000', ''],
    ];
    const tr = rows.map((r, i) => `<tr style="${i === 1 || i === 3 ? 'background:rgba(30,136,214,.22)' : ''}">${r.map((c, j) => `<td style="border:1px solid #c9ced4;padding:9px 10px;${j === 3 ? 'text-align:right' : ''}${j === 4 ? 'color:#2a5d9c;font-style:italic' : ''}">${c}</td>`).join('')}</tr>`).join('');
    const days = ['DAY 1 ARRIVAL KRABI', 'DAY 2 HONG ISLAND TOUR', 'DAY 3 EMERALD POOL HOT SPRING', 'DAY 4 MANGROVE KAYAK', 'DAY 5 DEPARTURE'];
    const lorem = 'Pick up from Krabi International Airport and transfer to hotel in Ao Nang. Check in and free time at leisure. Evening walk to Ao Nang beach and night market (own expense). Overnight at hotel. Remark: room is subject to availability, check in time 14:00, early check in not guaranteed. Please bring passport copy and confirm flight details with the team before departure. ';
    const items = {
      sticky_pickup: sticky('#CFE3F6', 'pickup 7:30??<br>lobby or pier?<br><span style="font-size:52px">ask Mai</span>'),
      sticky_diet: sticky('#CDEBE4', '2 veg<br>1 nut allergy<br>(Ana)'),
      sticky_line: sticky('#DCEBF9', 'Krabi Islands,<br>small group<br>Chloe + Ana<br>10 March, 5 days', 60),
      rate_sheet: [`<div style="width:1240px;height:1754px;${paper}box-sizing:border-box;padding:110px 90px;font:23px Arial,Helvetica,sans-serif;color:#222">
        <div style="font:bold 34px Arial">Krabi rates 2026</div><div style="color:#555;margin:6px 0 34px">rates_krabi_v4_FINAL.xlsx &nbsp; Sheet 1 &nbsp; THB</div>
        <table style="border-collapse:collapse;width:100%"><tr style="background:#e8ebee;font-weight:bold">${['Supplier', 'Item', 'Nights', 'Rate', 'Notes'].map((h) => `<td style="border:1px solid #c9ced4;padding:9px 10px">${h}</td>`).join('')}</tr>${tr}</table>
        <div style="${hand};font-size:46px;margin-top:70px;transform:rotate(-3deg)">check longtail price w/ Somchai<br>2 of 6 rooms left??</div></div>`, 1240, 1754],
      old_pdf: [`<div style="width:1754px;height:1240px;${paper}box-sizing:border-box;padding:80px 110px;font:22px 'Times New Roman',serif;color:#333;position:relative;overflow:hidden">
        <div style="text-align:center;font:bold 40px 'Times New Roman';text-decoration:underline">KRABI ISLAND TOUR PACKAGE 5D4N</div>
        <div style="text-align:center;margin:10px 0 30px;color:#666">ITINERARY_Krabi_v7_FINAL(2).pdf &nbsp;&nbsp; page 1 of 9</div>
        <div style="columns:2;column-gap:60px;text-align:justify;line-height:1.32">${days.map((d) => `<p><b>${d}</b><br>${lorem}${lorem.slice(0, 180)}</p>`).join('')}</div>
        <div style="position:absolute;left:1120px;top:640px;width:330px;height:330px;border-radius:50%;box-shadow:inset 0 0 0 14px rgba(110,92,74,.22),inset 0 0 0 22px rgba(110,92,74,.08)"></div></div>`, 1754, 1240],
      voucher: [`<div style="width:600px;height:1272px;${paper}box-sizing:border-box;padding:70px 56px;font:28px Menlo,monospace;color:#222;line-height:1.5;border-top:6px dashed #c9ced4">
        <div style="font:bold 40px Menlo">HOTEL VOUCHER</div><br>ANDAMAN BREEZE HOTEL<br>AO NANG, KRABI<br><br>GUEST&nbsp;&nbsp; CHLOE + 1<br>IN&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10 MAR<br>NIGHTS&nbsp; 2<br>ROOM&nbsp;&nbsp;&nbsp; TWIN<br><br>REF LT-KIS-2026<br><br><div style="${hand};font-size:44px;transform:rotate(-4deg);color:#24507f">sent? resend!!</div></div>`, 600, 1272],
      boarding: [`<div style="width:480px;height:1140px;background:#F4F6F8;box-sizing:border-box;padding:56px 44px;font:26px Menlo,monospace;color:#1d2733;line-height:1.5">
        <div style="font:bold 30px Menlo;letter-spacing:2px">BOARDING PASS</div><br>BANGKOK BKK<br>&rarr; KRABI KBV<br><br>10 MAR 09:40<br>SEAT 14A<br>GATE 3<br><br><div style="height:260px;background:repeating-linear-gradient(90deg,#1d2733 0 3px,transparent 3px 7px,#1d2733 7px 9px,transparent 9px 14px)"></div></div>`, 480, 1140],
      passport: [`<div style="width:528px;height:750px;background:#1B2A44;box-sizing:border-box;padding:110px 0;text-align:center;color:#C9D2DC;font:600 40px WbSans;letter-spacing:10px">PASSPORT
        <div style="width:170px;height:170px;margin:120px auto 0;border:4px solid #C9D2DC;border-radius:50%;opacity:.8;background:radial-gradient(circle,transparent 48%,transparent 49%),linear-gradient(#C9D2DC,#C9D2DC) center/4px 100% no-repeat,linear-gradient(#C9D2DC,#C9D2DC) center/100% 4px no-repeat"></div>
        <div style="width:64px;height:44px;margin:150px auto 0;border:3px solid #C9D2DC;border-radius:8px;opacity:.7"></div></div>`, 528, 750],
      polaroid: [`<div style="width:528px;height:642px;background:#F7F7F5;box-sizing:border-box;padding:30px 30px 0">
        <div style="width:468px;height:468px;background:url('${photo}') center/cover"></div>
        <div style="${hand};font-size:46px;text-align:center;margin-top:26px">Krabi, last March</div></div>`, 528, 642],
      phone_back: [`<div style="width:716px;height:1550px;background:#1a222c;border-radius:110px;position:relative">
        <div style="position:absolute;left:46px;top:46px;width:300px;height:300px;border-radius:70px;background:#222c38"></div></div>`, 716, 1550],
    };
    const only = film ? film.split(',') : Object.keys(items);
    for (const k of only) {
      const [html, w, h] = items[k];
      await shoot(html, w, h, path.join(out, `${k}.png`));
    }
  } else if (mode === 'supers') {
    // One PNG per line of words. Layout: left-aligned block, white or ink, WbSans Bold,
    // one Instrument Serif italic word marked *like this*. y is the block's centre in px.
    const spec = JSON.parse(readFileSync(path.join(HERE, `${film}.supers.json`), 'utf8'));
    const out = path.join(AD, 'render', film, 'supers');
    mkdirSync(out, { recursive: true });
    for (const [i, s] of spec.supers.entries()) {
      const words = s.text.replace(/\*(.+?)\*/g, '<i>$1</i>').split('\n').join('<br>');
      const color = s.color || spec.color || '#FFFFFF';
      const shadow = s.shadow ?? spec.shadow ?? true;
      const size = s.size || spec.size || 76;
      const align = s.align || spec.align || 'left';
      const x = s.x ?? spec.x ?? 84;
      const html = `<div style="position:absolute;left:${align === 'center' ? 0 : x}px;right:${align === 'center' ? 0 : 84}px;top:${s.y}px;transform:translateY(-50%);
        font:700 ${size}px/1.08 WbSans;letter-spacing:-0.012em;color:${color};text-align:${align};
        ${shadow ? 'text-shadow:0 2px 24px rgba(6,12,20,.55),0 1px 3px rgba(6,12,20,.35);' : ''}">${words}</div>
        <style>i{font:italic 400 ${Math.round(size * 1.18)}px/1 Serif;letter-spacing:0}</style>`;
      await shoot(html, 1080, 1920, path.join(out, `${i}.png`));
    }
  }
} finally {
  await browser.close();
}
