// Render each quote card HTML to a crisp 2160x2160 PNG with headless Edge.
// No fonts/CDN needed (uses Windows system fonts). Run after build.mjs.
//   node build.mjs && node render.mjs
import { readFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const EDGES = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
];
const edge = EDGES.find(existsSync);
if (!edge) { console.error("Microsoft Edge not found. Edit EDGES in render.mjs."); process.exit(1); }

const manifest = JSON.parse(readFileSync(join(HERE, "manifest.json"), "utf8"));
for (const { file, png } of manifest) {
  const html = join(HERE, file), out = join(HERE, png);
  execFileSync(edge, [
    "--headless=new", "--disable-gpu", "--hide-scrollbars",
    "--force-device-scale-factor=2", "--window-size=1080,1080",
    `--screenshot=${out}`, `file:///${html.replace(/\\/g, "/")}`,
  ], { stdio: "ignore" });
  console.log(`rendered ${png}`);
}
console.log(`\nDone. ${manifest.length} PNGs in marketing/ig-quote-cards/.`);
