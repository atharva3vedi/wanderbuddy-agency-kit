// Render every slide to a PNG with headless Edge. Uses Windows system fonts,
// no CDN, no network. Run after build.mjs.
//
//   node render.mjs            all variants
//   node render.mjs ig         just the 4:5 Instagram set
//   node render.mjs tiktok     just the 9:16 TikTok set
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

const only = process.argv[2];
const manifest = JSON.parse(readFileSync(join(HERE, "manifest.json"), "utf8"))
  .filter(m => !only || m.variant === only);

for (const { html, png, w, h } of manifest) {
  const src = join(HERE, html), out = join(HERE, png);
  execFileSync(edge, [
    "--headless=new", "--disable-gpu", "--hide-scrollbars",
    "--allow-file-access-from-files",
    "--force-device-scale-factor=1", `--window-size=${w},${h}`,
    `--screenshot=${out}`, `file:///${src.replace(/\\/g, "/")}`,
  ], { stdio: "ignore" });
  console.log(`rendered ${png}`);
}
console.log(`\nDone. ${manifest.length} PNGs.`);
