// Top-up fetcher. The main fetch-photos.mjs hammers Pexels fast enough that it
// starts serving empty search pages after ~30 requests, so this one goes slowly,
// retries, and only chases the queries that came back with nothing.
//
//   node fetch-extra.mjs
//
// Same licence story as fetch-photos.mjs: Pexels Licence, commercial use, no
// attribution required. Provenance lands in sources/index.json alongside the rest.
import { writeFileSync, readFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, "sources");
const IDX = join(OUT, "index.json");
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36";

const wanted = [
  ["beachman", "man silhouette beach sunset"],
  ["canal",    "bruges canal houses"],
  ["van",      "van parked road"],
  ["curtain",  "hotel room window light"],
  ["pack",     "suitcase packing clothes"],
  ["office",   "empty office chair desk"],
  ["blur",     "night city lights bokeh"],
  ["train",    "train platform station"],
];

const sleep = ms => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
const curl = (url, binary) => execFileSync("curl", [
  "-sL", "-m", "60", "-A", UA, "-H", "accept-language: en-US,en;q=0.9", url,
], { maxBuffer: 128 * 1024 * 1024, encoding: binary ? "buffer" : "utf8" });

const index = existsSync(IDX) ? JSON.parse(readFileSync(IDX, "utf8")) : {};

for (const [slug, query] of wanted) {
  if (Object.keys(index).some(k => k.startsWith(slug + "-"))) { console.log(`${slug}  already have`); continue; }
  let paths = [];
  for (let attempt = 1; attempt <= 4 && paths.length === 0; attempt++) {
    sleep(attempt * 6000);                       // back off harder every retry
    try {
      const html = curl(`https://www.pexels.com/search/${encodeURIComponent(query)}/`, false);
      paths = [...new Set([...html.matchAll(/images\.pexels\.com\/photos\/(\d+)\/([a-z0-9-]+\.jpe?g)/g)]
        .map(m => `${m[1]}/${m[2]}`))].slice(0, 6);
    } catch (e) { console.error(`  ! ${slug} attempt ${attempt}: ${e.message}`); }
  }
  console.log(`${slug}  "${query}"  ->  ${paths.length}`);
  paths.forEach((path, i) => {
    const name = `${slug}-${String(i + 1).padStart(2, "0")}`;
    const id = path.split("/")[0];
    index[name] = { pexelsId: id, page: `https://www.pexels.com/photo/${id}/`, query, licence: "Pexels Licence" };
    const file = join(OUT, `${name}.jpg`);
    if (existsSync(file)) return;
    const bytes = curl(`https://images.pexels.com/photos/${path}?auto=compress&cs=tinysrgb&w=2400`, true);
    if (bytes.length < 5000) return;
    writeFileSync(file, bytes);
    console.log(`    ${name}.jpg  (pexels ${id})`);
  });
  writeFileSync(IDX, JSON.stringify(index, null, 2));
}
console.log(`\n${Object.keys(index).length} sources indexed`);
