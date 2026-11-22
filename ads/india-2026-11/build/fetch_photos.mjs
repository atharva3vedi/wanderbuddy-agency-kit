// Fetch Commons originals (2560 px wide thumbs) + license metadata into a folder.
import fs from 'node:fs'; import path from 'node:path';
const out = process.argv[2];
const UA = { 'User-Agent': 'WanderBuddyAdBuilder/1.0 (marketing stills)' };
const FILES = {
  'root-bridge': 'File:Double Decker Living Tree Root Bridges, Meghalaya.jpg',
  'dawki': 'File:Umngot river, Dawki.jpg',
  'umngot': 'File:UMNGOT RIVER.jpg',
  'nongjrong': 'File:Midnight Nongjrong.jpg',
  'nohkalikai': 'File:Powerful Nohkalikai Waterfall.jpg',
  'blue-mountain': 'File:2007-blue-mountain-np.jpg',
  'vantawng': 'File:Vantawng waterfall, Mizoram,India.JPG',
  'hmuifang': 'File:Hmuifang tlang.jpg',
};
const meta = {};
for (const [key, title] of Object.entries(FILES)) {
  const u = new URL('https://commons.wikimedia.org/w/api.php');
  Object.entries({ action: 'query', format: 'json', prop: 'imageinfo', titles: title, iiprop: 'url|size|extmetadata', iiurlwidth: '2560', formatversion: '2' }).forEach(([k, v]) => u.searchParams.set(k, v));
  const j = await (await fetch(u, { headers: UA })).json();
  const ii = j.query.pages[0].imageinfo?.[0];
  if (!ii) { console.log('MISSING', key); continue; }
  const src = ii.width <= 2560 ? ii.url : ii.thumburl;
  const r = await fetch(src, { headers: UA });
  const buf = Buffer.from(await r.arrayBuffer());
  fs.writeFileSync(path.join(out, key + '.jpg'), buf);
  const m = ii.extmetadata || {};
  meta[key] = { title, w: ii.width, h: ii.height, author: (m.Artist?.value || '').replace(/<[^>]+>/g, '').trim(), license: m.LicenseShortName?.value, bytes: buf.length };
  console.log(key, ii.width + 'x' + ii.height, meta[key].license, meta[key].author, buf.length);
  await new Promise(r => setTimeout(r, 600));
}
fs.writeFileSync(path.join(out, 'credits.json'), JSON.stringify(meta, null, 2));
