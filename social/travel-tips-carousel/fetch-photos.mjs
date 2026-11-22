// Sources the carousel photography from Pexels.
//
// Pexels Licence: free to use, commercial use allowed, no attribution required,
// modification allowed. That is why this is Pexels and not Instagram: photos on
// Instagram belong to the people who shot them and reposting them inside a
// branded WanderBuddy carousel is a takedown (or a bill) waiting to happen.
//
// No API key needed. We read the public search page and take the CDN urls it
// already serves, at 2400px so a 9:16 crop is still sharp. curl, not node's
// fetch, because Pexels 403s undici's TLS fingerprint.
//
//   node fetch-photos.mjs        -> sources/ + sources/index.json (provenance)
//
// Re-running is cheap: existing files are skipped, the index is always rewritten.
import { writeFileSync, mkdirSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, "sources");
mkdirSync(OUT, { recursive: true });

const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36";
const PER_QUERY = 6;
const WIDTH = 2400;

// slug -> search query. Slugs are stable; build.mjs picks by "<slug>-NN".
const queries = [
  ["crew",      "friends taking photo travel city street"],
  ["corridor",  "airport transit terminal walking"],
  ["passport",  "hand holding passport travel document"],
  ["board",     "airport departure board traveller"],
  ["pay",       "paying at street market vendor"],
  ["atm",       "atm machine street cash"],
  ["waiting",   "man sitting airport window waiting flight"],
  ["checkin",   "suitcase luggage check in airport"],
  ["gate",      "woman using phone airport lounge window"],
  ["maps",      "looking at phone map street city travel"],
  ["night",     "woman walking city street night lights"],
  ["trail",     "hiking mountain trail traveller backpack"],
  ["table",     "friends dinner table restaurant toast"],
  ["sunset",    "group of friends sitting viewpoint sunset"],
  ["docs",      "passport boarding pass travel documents flat lay"],
  ["delayed",   "airport terminal seats waiting passengers"],
  ["card",      "credit card payment terminal machine hand"],
];

const curl = (url, binary) => execFileSync("curl", [
  "-sL", "-m", "60", "-A", UA, "-H", "accept-language: en-US,en;q=0.9", url,
], { maxBuffer: 128 * 1024 * 1024, encoding: binary ? "buffer" : "utf8" });

const index = {};
for (const [slug, query] of queries) {
  let paths = [];
  try {
    const html = curl(`https://www.pexels.com/search/${encodeURIComponent(query)}/`, false);
    paths = [...new Set([...html.matchAll(/images\.pexels\.com\/photos\/(\d+)\/([a-z0-9-]+\.jpe?g)/g)]
      .map(m => `${m[1]}/${m[2]}`))].slice(0, PER_QUERY);
  } catch (e) { console.error(`  ! ${slug}: ${e.message}`); continue; }

  console.log(`${slug}  "${query}"  ->  ${paths.length}`);
  paths.forEach((path, i) => {
    const name = `${slug}-${String(i + 1).padStart(2, "0")}`;
    const id = path.split("/")[0];
    index[name] = { pexelsId: id, page: `https://www.pexels.com/photo/${id}/`, query, licence: "Pexels Licence" };
    const file = join(OUT, `${name}.jpg`);
    if (existsSync(file)) return;
    const bytes = curl(`https://images.pexels.com/photos/${path}?auto=compress&cs=tinysrgb&w=${WIDTH}`, true);
    if (bytes.length < 5000) { console.error(`    ! ${name} empty`); return; }
    writeFileSync(file, bytes);
    console.log(`    ${name}.jpg  (pexels ${id})`);
  });
}
writeFileSync(join(OUT, "index.json"), JSON.stringify(index, null, 2));
console.log(`\n${Object.keys(index).length} sources indexed in sources/index.json`);
