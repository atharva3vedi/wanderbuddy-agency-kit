// The paper map of Southeast Asia the devices sit on. Natural Earth coastlines from
// world-atlas (countries-50m, already in website/node_modules), projected
// equirectangular at 7 N, drawn as SVG and rendered in Chrome.
//   node build/map.mjs -> screens/map.png (colour), screens/map_land.png (land mask for the raised paper)
// map.json records the bounds so build/demo.py can put a city at its lon/lat.
import puppeteer from 'puppeteer-core';
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AD = path.resolve(HERE, '..');
const ROOT = path.resolve(AD, '../../..');
const require = createRequire(import.meta.url);
const topo = require(path.join(ROOT, 'website/node_modules/topojson-client/dist/topojson-client.js'));
const world = JSON.parse(readFileSync(path.join(ROOT, 'website/node_modules/world-atlas/countries-50m.json'), 'utf8'));

const LON0 = 88, LON1 = 128, LAT0 = -11, LAT1 = 22, LATC = 7;
const KX = Math.cos((LATC * Math.PI) / 180);
const W = 8192;
const SCALE = W / ((LON1 - LON0) * KX); // px per degree of latitude
const H = Math.round((LAT1 - LAT0) * SCALE);
const X = (lon) => (lon - LON0) * KX * SCALE;
const Y = (lat) => (LAT1 - lat) * SCALE;

// Only rings that touch the frame (with a margin), so the path stays small.
function ringPath(ring) {
  let d = '';
  let inside = false;
  for (const [lon, lat] of ring) if (lon > LON0 - 8 && lon < LON1 + 8 && lat > LAT0 - 8 && lat < LAT1 + 8) inside = true;
  if (!inside) return '';
  ring.forEach(([lon, lat], i) => { d += (i ? 'L' : 'M') + X(lon).toFixed(1) + ' ' + Y(lat).toFixed(1); });
  return d + 'Z';
}
function geoPath(g) {
  if (!g) return '';
  if (g.type === 'Polygon') return g.coordinates.map(ringPath).join('');
  if (g.type === 'MultiPolygon') return g.coordinates.map((p) => p.map(ringPath).join('')).join('');
  if (g.type === 'MultiLineString') return g.coordinates.map((l) => l.map(([lon, lat], i) => (i ? 'L' : 'M') + X(lon).toFixed(1) + ' ' + Y(lat).toFixed(1)).join('')).join('');
  return '';
}

const land = topo.merge(world, world.objects.countries.geometries);
const borders = topo.mesh(world, world.objects.countries, (a, b) => a !== b);
const LAND = geoPath(land);
const BORD = geoPath(borders);

let grat = '';
for (let lon = 90; lon <= LON1; lon += 5) grat += `M${X(lon).toFixed(1)} 0V${H}`;
for (let lat = -10; lat <= LAT1; lat += 5) grat += `M0 ${Y(lat).toFixed(1)}H${W}`;

// The two places of the film carry ink dots; the rest of the region is faint context.
export const CITIES = {
  krabi: [98.91, 8.09], singapore: [103.82, 1.35],
};
const CONTEXT = [['Bangkok', 100.5, 13.75], ['Hanoi', 105.85, 21.03], ['Ho Chi Minh City', 106.66, 10.76], ['Phnom Penh', 104.92, 11.56],
  ['Kuala Lumpur', 101.69, 3.14], ['Manila', 120.98, 14.6], ['Bali', 115.19, -8.65], ['Jakarta', 106.85, -6.21], ['Yangon', 96.2, 16.84]];
const COUNTRIES = [['THAILAND', 101.2, 16.2], ['VIETNAM', 107.9, 14.6], ['CAMBODIA', 104.9, 13.1], ['LAOS', 103.0, 19.6], ['MYANMAR', 95.6, 20.6],
  ['MALAYSIA', 113.6, 3.0], ['INDONESIA', 114.4, -1.0], ['PHILIPPINES', 123.4, 11.4]];
const SEAS = [['Andaman Sea', 95.0, 10.0], ['Gulf of Thailand', 101.6, 9.6], ['South China Sea', 113.6, 13.5], ['Java Sea', 111.0, -5.3]];

const MONO = 'ui-monospace,SFMono-Regular,Menlo,monospace';
const label = (t, x, y, size, fill, opts = '') => `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-family="${MONO}" font-size="${size}" fill="${fill}" letter-spacing="${(size * 0.18).toFixed(1)}" ${opts}>${t}</text>`;

function svg(mask) {
  if (mask) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#000"/>
      <path d="${LAND}" fill="#fff" fill-rule="evenodd"/></svg>`;
  }
  const ctx = CONTEXT.map(([n, lon, lat]) => `<circle cx="${X(lon)}" cy="${Y(lat)}" r="9" fill="#0C1622" fill-opacity=".32"/>` +
    label(n.toUpperCase(), X(lon) + 22, Y(lat) + 13, 38, 'rgba(12,22,34,.40)')).join('');
  const cty = COUNTRIES.map(([n, lon, lat]) => label(n, X(lon), Y(lat), 64, 'rgba(12,22,34,.20)', 'text-anchor="middle" font-weight="600"')).join('');
  const seas = SEAS.map(([n, lon, lat]) => `<text x="${X(lon)}" y="${Y(lat)}" font-family="Georgia,serif" font-style="italic" font-size="70" fill="rgba(30,108,170,.30)" text-anchor="middle">${n}</text>`).join('');
  const city = ([lon, lat], name, dx, anchor) => `<circle cx="${X(lon)}" cy="${Y(lat)}" r="30" fill="none" stroke="#0C1622" stroke-width="7"/>
    <circle cx="${X(lon)}" cy="${Y(lat)}" r="14" fill="#0C1622"/>` + label(name, X(lon) + dx, Y(lat) + 24, 70, '#0C1622', `font-weight="700" text-anchor="${anchor}"`);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <defs><radialGradient id="v" cx="50%" cy="48%" r="70%"><stop offset="0" stop-color="#E4ECF4"/><stop offset="1" stop-color="#D5E0EB"/></radialGradient></defs>
    <rect width="${W}" height="${H}" fill="url(#v)"/>
    <path d="${grat}" stroke="#0C1622" stroke-opacity=".07" stroke-width="3" fill="none"/>
    <path d="${LAND}" fill="#FBFCFD" fill-rule="evenodd" stroke="#0C1622" stroke-opacity=".42" stroke-width="3.2" stroke-linejoin="round"/>
    <path d="${BORD}" stroke="#0C1622" stroke-opacity=".22" stroke-width="3" stroke-dasharray="14 10" fill="none"/>
    ${seas}${cty}${ctx}
    ${city(CITIES.krabi, 'KRABI', -52, 'end')}
    ${city(CITIES.singapore, 'SINGAPORE', 52, 'start')}
    ${[90, 95, 100, 105, 110, 115, 120, 125].map((lon) => label(lon + '°E', X(lon) + 10, H - 26, 34, 'rgba(12,22,34,.30)')).join('')}
    ${[-10, -5, 0, 5, 10, 15, 20].map((lat) => label((lat < 0 ? -lat + '°S' : lat + '°N'), 18, Y(lat) - 12, 34, 'rgba(12,22,34,.30)')).join('')}
  </svg>`;
}

const meta = { W, H, LON0, LON1, LAT0, LAT1, LATC, cities: CITIES };
writeFileSync(path.join(AD, 'screens', 'map.json'), JSON.stringify(meta, null, 1));
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--force-color-profile=srgb'] });
try {
  const p = await b.newPage();
  for (const [name, mask, scale] of [['map', false, 1], ['map_land', true, 0.5]]) {
    await p.setViewport({ width: Math.round(W * scale), height: Math.round(H * scale), deviceScaleFactor: 1 });
    const tmp = path.join(AD, 'render', `_${name}.html`);
    writeFileSync(tmp, `<!doctype html><meta charset=utf-8><body style="margin:0;overflow:hidden"><div style="transform:scale(${scale});transform-origin:0 0">${svg(mask)}</div></body>`);
    await p.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0' });
    await p.screenshot({ path: path.join(AD, 'screens', `${name}.png`) });
    console.log('wrote', name, Math.round(W * scale), Math.round(H * scale));
  }
} finally { await b.close(); }
