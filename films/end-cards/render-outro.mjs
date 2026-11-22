// Render each outro layer HTML to a 1080x1920 PNG with headless Edge.
// Transparent layers use --default-background-color=00000000 (RGBA, alpha=00).
//   node build-outro.mjs && node render-outro.mjs
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
if (!edge) { console.error("Microsoft Edge not found."); process.exit(1); }

const manifest = JSON.parse(readFileSync(join(HERE, "layers.json"), "utf8"));
for (const { file, png, transparent } of manifest) {
  const html = join(HERE, file), out = join(HERE, png);
  const args = [
    "--headless=new", "--disable-gpu", "--hide-scrollbars",
    "--force-device-scale-factor=1", "--window-size=1080,1920",
  ];
  if (transparent) args.push("--default-background-color=00000000");
  args.push(`--screenshot=${out}`, `file:///${html.replace(/\\/g, "/")}`);
  execFileSync(edge, args, { stdio: "ignore" });
  console.log(`rendered ${png}${transparent ? " (transparent)" : ""}`);
}
console.log(`\nDone. ${manifest.length} PNGs in marketing/outro/.`);
