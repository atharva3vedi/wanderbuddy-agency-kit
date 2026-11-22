// Render the WanderBuddy logo reveal frames to 1080x1920 PNGs with headless Edge.
// Produces logo-card.png (mark + wordmark) and logo-mark.png (mark only).
// No CDN/fonts needed (Windows system fonts).  Run:  node render-logo-card.mjs
import { existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const EDGES = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
];
const edge = EDGES.find(existsSync);
if (!edge) { console.error("Microsoft Edge not found. Edit EDGES in render-logo-card.mjs."); process.exit(1); }

const html = join(HERE, "logo-card.html").replace(/\\/g, "/");
const shots = [
  { q: "",      png: "logo-card.png" }, // mark + wordmark (final reveal frame)
  { q: "?mark", png: "logo-mark.png" }, // mark only (the settle beat)
];
for (const { q, png } of shots) {
  const out = join(HERE, png);
  execFileSync(edge, [
    "--headless=new", "--disable-gpu", "--hide-scrollbars",
    "--force-device-scale-factor=1", "--window-size=1080,1920",
    `--screenshot=${out}`, `file:///${html}${q}`,
  ], { stdio: "ignore" });
  console.log(`rendered ${png}`);
}
console.log("\nDone. logo-card.png + logo-mark.png (1080x1920) in marketing/logo-transition/.");
