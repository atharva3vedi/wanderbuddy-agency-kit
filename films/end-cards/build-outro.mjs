// WanderBuddy video OUTRO / end-card layers.
// Renders brand-exact end-card LAYERS as transparent 1080x1920 PNGs so
// autocut can animate each independently over the brand field:
//   - wordmark  "WanderBuddy"
//   - dlnow     "Download now"  (white, replaced the old amber pill)
//   - badges    App Store + Google Play download badges (app is live on both)
// The MARK itself is NOT rendered here anymore: use the real shipping icon
// assets/icon/app_icon.png (keyed to mark_t.png) so the logo is exact.
//
//   node build-outro.mjs && node render-outro.mjs
//
// Brand: field blue #2072B8 · white mark/wordmark. No em dashes, no pricing.
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const W = 1080, H = 1920;

const WORD = `
  <text x="540" y="1160" text-anchor="middle" font-size="118"
        font-family="'Roboto','Segoe UI',Arial,Helvetica,sans-serif"
        font-weight="800" letter-spacing="2" fill="#FFFFFF">WanderBuddy</text>`;

const DLNOW = `
  <text x="540" y="1300" text-anchor="middle" font-size="56"
        font-family="'Roboto','Segoe UI',Arial,Helvetica,sans-serif"
        font-weight="700" letter-spacing="1" fill="#FFFFFF">Download now</text>`;

// --- store badges (recognizable, official-style; app is on both stores) ---
const APPLE = `<path transform="translate(26,33) scale(1.55)"
  fill="#FFFFFF" d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24
  0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 8.9 7.31c1.35.07 2.29.74 3.08.8
  1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48
  7.13-.57 1.5-1.31 2.99-2.38 4.08zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29
  2.58-2.34 4.5-3.74 4.25z"/>`;

// Google Play triangle: 4 coloured faces from the centroid (reads as Play).
const PLAY = (() => {
  const tx = 30, ty = 28, s = 1.25;              // place + scale
  const P1 = [0, 0], P2 = [0, 44], P3 = [40, 22], M = [0, 22];
  const C  = [(0 + 0 + 40) / 3 * 0.9, 22];        // fold centre, nudged left
  const tri = (a, b, c, col) =>
    `<polygon points="${a[0]},${a[1]} ${b[0]},${b[1]} ${c[0]},${c[1]}" fill="${col}"/>`;
  return `<g transform="translate(${tx},${ty}) scale(${s})">
    ${tri(P1, M, C, "#EA4335")}   <!-- top-left  red   -->
    ${tri(P1, P3, C, "#00C4FF")}  <!-- top       blue  -->
    ${tri(P3, P2, C, "#00E676")}  <!-- bottom    green -->
    ${tri(P2, M, C, "#FFCE00")}   <!-- bot-left  amber -->
  </g>`;
})();

const badge = (x, mark, small, big) => `
  <g transform="translate(${x},1360)">
    <rect width="372" height="112" rx="20" fill="#000000"
          stroke="rgba(255,255,255,.28)" stroke-width="2"/>
    ${mark}
    <text x="112" y="46" font-size="21" fill="#FFFFFF"
          font-family="Arial,Helvetica,sans-serif">${small}</text>
    <text x="112" y="90" font-size="40" font-weight="700" fill="#FFFFFF"
          font-family="Arial,Helvetica,sans-serif">${big}</text>
  </g>`;

// two badges centred: total 372*2 + 32 gap = 776 -> start x=152
const BADGES = `${badge(152, APPLE, "Download on the", "App Store")}
                ${badge(556, PLAY,  "GET IT ON",       "Google Play")}`;

const svg = (inner) => `<!doctype html><html><head><meta charset="utf-8"><style>
  html,body{margin:0;padding:0;width:${W}px;height:${H}px;overflow:hidden;background:transparent;}
  svg{position:absolute;inset:0;}
</style></head><body>
  <svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">${inner}</svg>
</body></html>`;

const layers = {
  "layer-word":   WORD,
  "layer-dlnow":  DLNOW,
  "layer-badges": BADGES,
  // flat reference card on the brand field (uses the real icon at runtime)
  "card-ref":     `<rect width="${W}" height="${H}" fill="#2072B8"/>${WORD}${DLNOW}${BADGES}`,
};

const manifest = [];
for (const [name, inner] of Object.entries(layers)) {
  writeFileSync(join(HERE, `${name}.html`), svg(inner));
  manifest.push({ file: `${name}.html`, png: `${name}.png`,
    transparent: name !== "card-ref" });
}
writeFileSync(join(HERE, "layers.json"), JSON.stringify(manifest, null, 2));
console.log(`generated ${manifest.length} outro layers`);
