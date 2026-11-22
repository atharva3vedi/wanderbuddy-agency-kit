// Film "The Reel": the itinerary. The real 14 pages of the public demo's itinerary maker
// (wanderbuddyapp.com/trydemo, sample data, view only, nothing saved), shown as a Ha Giang
// Loop plan: the sample trip's words are swapped from Krabi to Vietnam in this page only,
// and every photo frame is filled with the app's own Vietnam photos (the ones on its seeded
// trips: Ha Giang, Ninh Binh, Sapa, Hoi An; credits in supabase/migrations/0224, 0225).
//   node build/reel_pages.mjs [probe]  -> screens/reel/pages/pg00..13.png
import puppeteer from 'puppeteer-core';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../screens/reel/pages');
mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const STORE = 'https://wgzwrrrfzxdnkrfebkqb.supabase.co/storage/v1/object/public/trip-images/showcase/';
const PHOTOS = ['hagiang', 'ninhbinh', 'sapa', 'hoian'].map((n) => STORE + n + '.jpg');
// most specific first
const WORDS = [
  [/Five days from Ao Nang with a small group:[^.]*\./, 'Five days from Hanoi with a small group: Ninh Binh by rowing boat, the Ha Giang loop with local riders, the Nho Que river and two homestays in the hills.'],
  [/Arrive, Ao Nang beach, the night market/g, 'Arrive, the Old Quarter, a street food walk'],
  [/The Hong Islands by longtail/g, 'Ninh Binh by rowing boat'],
  [/Emerald Pool and the hot springs/g, 'Ma Pi Leng Pass and the Nho Que river'],
  [/Kayak the mangroves, a last night out/g, 'Lung Cu flag tower, a last night out'],
  [/13:00 Our driver meets you at Krabi airport arrivals: 40 minutes to your hotel in Ao Nang\. 16:00 Ao Nang beach: a first swim while the cliffs turn gold\./, '13:00 Our driver meets you at Noi Bai arrivals: 40 minutes to your hotel in the Old Quarter. 16:00 Hoan Kiem lake on foot while the light turns gold.'],
  [/19:00 Meet the group, then dinner at the Ao Nang night market:[^.]*\./, '19:00 Meet the group, then a street food walk: bun cha, banh cuon, egg coffee.'],
  [/08:30 Longtail from Ao Nang out across the bay to the Hong Islands, about an hour\. 11:00 Swim into the Hong lagoon at high tide, ringed by cliffs, and snorkel off the beach\./, '07:30 Drive to Ninh Binh, about two hours. 10:30 A rowing boat through the Tam Coc caves, rowed by foot, between the rice fields and the cliffs.'],
  [/Lunch on the boat, then a quiet beach on Koh Lao Lading\./, 'Lunch in Tam Coc, then bikes to Bich Dong pagoda.'],
  [/17:30 The sunset longtail home across the bay, back in Ao Nang around 18:30\./, '17:30 The evening bus north, in Ha Giang town by 22:30.'],
  [/08:00 Check out and drive inland to the Emerald Pool in the Thung Teao forest for a swim in clear green water\./, '08:00 Meet your easy rider and ride north over Quan Ba pass to Yen Minh for lunch.'],
  [/13:00 The hot springs at Klong Thom, then on to Klong Muang beach and your second hotel\./, '13:00 Ma Pi Leng Pass, then the boat on the Nho Que river and your homestay in Dong Van.'],
  [/A free evening on a quieter beach\./, 'Dinner with the family, and rice wine if you like.'],
  [/09:00 Kayak through the mangroves and limestone canyons of Ao Thalane with a local guide\./, '09:00 Ride to the Lung Cu flag tower at the northern tip, with a local guide.'],
  [/Free afternoon at the pool or on the beach\./, 'The Sunday market in Dong Van, then the long way back.'],
  [/19:30 Farewell dinner together, then a night out in Ao Nang for whoever wants one\./, '19:30 Farewell dinner together, then a night out in Ha Giang town for whoever wants one.'],
  [/Breakfast and a last swim\. 11:00 Transfer to Krabi airport, about 30 minutes\./g, 'Breakfast and a last coffee. 11:00 The bus back to Hanoi, about six hours.'],
  [/A trip lead from Krabi, airport to airport/, 'A trip lead from Hanoi, airport to airport'],
  [/4 nights in 2 hotels, breakfast daily/, '4 nights in a hotel and two homestays, breakfast daily'],
  [/Longtail to the Hong Islands, with lunch/, 'The Tam Coc rowing boat, with lunch'],
  [/Emerald Pool, hot springs and the mangrove kayak/, 'An easy rider and bike each on the loop'],
  [/National park fees/, 'The Nho Que river boat'],
  [/Bring a swimsuit, reef safe sunscreen, a hat and sandals you can get wet\./, 'Bring a rain jacket, a warm layer for the passes and shoes you can ride in.'],
  [/Every hotel and boat in this plan is one our team has used many times, with captains and hosts we know by name\./, 'Every homestay and rider in this plan is one our team has used many times, with hosts we know by name.'],
  [/Longtails, early/, 'On the road, early'],
  [/We leave before the day boats, so the lagoons and beaches are quiet when you get there\./, 'We leave before the tour buses, so the passes and viewpoints are quiet when you get there.'],
  [/with a trip lead from Krabi from the airport to the airport/, 'with a trip lead from Hanoi from the airport to the airport'],
  [/Sea and weather can change a boat day; your trip lead decides what is safe\./, 'Rain and fog can change a riding day; your trip lead decides what is safe.'],
  [/Andaman Breeze Hotel/g, 'Old Quarter House'],
  [/Klong Muang Garden Resort/g, 'Dong Van Hill Homestay'],
  [/Ao Nang, Krabi 81180, Thailand/g, 'Hang Bac, Hoan Kiem, Hanoi, Vietnam'],
  [/\+66 81 470 2286/g, '+84 24 3555 0186'],
  [/KRABI ISLANDS, SMALL GROUP/g, 'HA GIANG LOOP, SMALL GROUP'],
  [/Krabi Islands, small group/g, 'Ha Giang Loop, small group'],
  [/LT-KIS-/g, 'LT-HGL-'],
  [/KLONG MUANG/g, 'HA GIANG'], [/Klong Muang/g, 'Ha Giang'],
  [/AO NANG/g, 'HANOI'], [/Ao Nang/g, 'Hanoi'],
  [/Krabi/g, 'Vietnam'],
];
const b = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new', args: ['--force-color-profile=srgb'],
});
try {
  const p = await b.newPage();
  await p.setBypassCSP(true);
  await p.setViewport({ width: 2200, height: 1400, deviceScaleFactor: 2 });
  await p.goto('https://wanderbuddyapp.com/trydemo/app/#/studio', { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(2500);
  const href = await p.evaluate(() => [...document.querySelectorAll('a.sx-cardname')].find((a) => /krabi islands, small group/i.test(a.textContent))?.getAttribute('href'));
  await p.goto('https://wanderbuddyapp.com/trydemo/app/' + href, { waitUntil: 'networkidle2', timeout: 60000 });
  await sleep(4500);
  await p.addStyleTag({ content: [
    '.sx .sp .ph.empty[data-p]{background:var(--tint)!important}', '.sx .sp .ph.empty i{display:none!important}',
    '.sx .sp [data-e]:empty::before{content:none!important}', '.sx .sp li.add,.sx .sp .pk-add,.sx .sp .fx-h{display:none!important}',
  ].join('') });
  const info = await p.evaluate((WORDS, PHOTOS) => {
    const secs = [...document.querySelectorAll('section.sp')].slice(-14);
    const rx = WORDS.map(([src, flags, to]) => [new RegExp(src, flags), to]);
    let k = 0;
    const seen = [];
    for (const s of secs) {
      const tw = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
      for (let n = tw.nextNode(); n; n = tw.nextNode()) { let v = n.nodeValue; for (const [r, to] of rx) v = v.replace(r, to); n.nodeValue = v; }
      // photos: every frame gets one of the Vietnam photos, never the same twice in a row
      for (const ph of s.querySelectorAll('.ph, .circ')) {
        if (ph.dataset.vn) continue;
        ph.dataset.vn = '1';
        const src = PHOTOS[k++ % PHOTOS.length];
        const im = ph.querySelector('img');
        if (im) { im.removeAttribute('srcset'); im.src = src; im.style.objectFit = 'cover'; }
        else { ph.style.setProperty('background', `url("${src}") center/cover no-repeat`, 'important'); ph.classList.remove('empty'); for (const c of [...ph.children]) c.style.display = 'none'; }
        seen.push(ph.className + (im ? ':img' : ':bg'));
      }
    }
    return { pages: secs.length, frames: k, classes: [...new Set(seen)].slice(0, 8), left: secs.map((s) => (s.innerText.match(/Krabi|Ao Nang|Klong|longtail|Hong Islands|Thailand|Andaman/gi) || []).join(',')).filter(Boolean) };
  }, WORDS.map(([r, to]) => [r.source, r.flags, to]), PHOTOS);
  console.log(JSON.stringify(info));
  await p.waitForNetworkIdle({ idleTime: 1200, timeout: 30000 }).catch(() => {});
  await sleep(2500);
  const secs = (await p.$$('section.sp')).slice(-14);
  for (const [i, s] of secs.entries()) {
    await s.evaluate((x) => x.scrollIntoView({ block: 'center' }));
    await sleep(500);
    await s.screenshot({ path: path.join(OUT, `pg${String(i).padStart(2, '0')}.png`) });
  }
  console.log('wrote', secs.length, 'pages');
} finally {
  await b.close();
}
