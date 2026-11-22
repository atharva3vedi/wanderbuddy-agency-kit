# Travel tips carousel, cursed edition

10 slides in exactly the same brand furniture as
[`../travel-tips-carousel`](../travel-tips-carousel), containing exactly the wrong
advice. A man delivers twelve travel tips, does not make it past tip six, and is
replaced mid sentence by someone who did not read the earlier ones.

Ten because that is what an Instagram carousel takes. The cover still promises twelve
tips and the deck stops at eight, which is the joke doing its own work: he never got
to the rest. Slide 10 says so out loud. Three offcut tips live in the `reserve` array
in `build.mjs` for a longer TikTok cut.

The straight carousel is the sibling folder. This one does not replace it. Post copy
and the in character comment replies are in [CAPTIONS.md](CAPTIONS.md).

```bash
node fetch-photos.mjs   # bulk sources
node fetch-extra.mjs    # the ones Pexels throttled, slowly, with retries
node build.mjs          # build/{ig,tiktok}/*.html + manifest.json
node render.mjs ig      # out/ig/*.png    1080x1350
node render.mjs tiktok  # out/tiktok/*.png 1080x1920
```

| Variant | Size | Where |
|---|---|---|
| `out/ig/` | 1080x1350 (4:5) | Instagram carousel |
| `out/tiktok/` | 1080x1920 (9:16) | TikTok photo post, Stories |

## How the deterioration is built

The joke is structural, so it lives in two per slide fields rather than in the copy.

`state` runs the narrator's exit:

- `stutter` (slide 6). The headline gets a red offset ghost behind it via layered
  `text-shadow`. An earlier version used `::after` with `z-index:-1`, which renders
  behind the opaque body and is invisible. Do not go back to that.
- `collapse cut` plus `severed: true` (slide 7). The stroke and the removal share one
  card, because ten slides has no room for both and they hit harder stacked. Wordmark
  letter spacing blows out, the numeral goes red and tilts, the body copy runs on and
  then simply stops at a solid red caret, a black band takes the space where the rest
  of the advice would have been, and `countOverride` drops the counter to `06 / --`
  because the carousel has stopped being certain how long it is.

`voice: "successor"` covers slides 8 and 9: numerals go white instead of amber, the
accent turns cold grey, and the photograph is graded down to `saturate(.42)`. Same
layout, different hands. Slide 8 also carries a `NEW MANAGEMENT` chip so the handover
reads even if someone lands mid carousel.

## The closing slide

Slide 10 is the only one with no photograph. It is the brand navy field
(`radial-gradient` off `#1c3a5c`, the same one `../ig-quote-cards` uses) with a cut out
subject composited on top, a gun pointed at the reader over "we are done asking".

The subject comes from `sources/gun.png`, which is produced by `cutout.py`:

```bash
python cutout.py sources/gun-src.png sources/gun.png
node build.mjs && node render.mjs ig && node render.mjs tiktok
```

`cutout.py` handles both shapes of source file. If the image already carries real
transparency it only trims the dead margin, because stock cutouts usually come with a
lot of it and it wrecks the composition. If the background is flat it flood fills
inward from every edge with a tolerance, which beats a global colour key because it
will not punch holes through matching colours inside the subject. Either way the alpha
edge gets about a pixel of feather so the subject does not read as a sticker.

**The slide renders fine without it.** If `sources/gun.png` is absent, `build.mjs`
prints the commands above and lays the slide out as type on navy. That is also the
fallback worth reaching for if TikTok suppresses the weapon version: drop the `cutout`
field and the copy still lands.

## Editing

Everything is the `slides` array at the top of `build.mjs`.

- `photo` is a filename stem in `sources/`, `cutout` is one for a composited PNG.
- `focus` is a CSS `object-position`, which decides what survives the 4:5 to 9:16 crop.
  Check both variants after changing it.
- `tweak` is an optional transform for subjects sitting too low in frame. Costs resolution.
- `state`, `voice`, `chip`, `severed`, `countOverride` drive everything described above.
- `reserve` holds the offcuts. Give one a `file` and an `n` and move it into `slides`.

Render each variant separately. Doing all twenty PNGs in one `node render.mjs` runs past
a two minute command timeout.

## Photos

Pexels, under the [Pexels Licence](https://www.pexels.com/license/): commercial use,
no attribution required. `sources/index.json` records the Pexels id, source page and
search query for every file. Same reasoning as the sibling folder: reposting somebody's
Instagram photography under our logo is a takedown waiting to arrive.

`fetch-photos.mjs` moves fast enough that Pexels starts serving empty search pages
after roughly thirty requests. `fetch-extra.mjs` exists to pick up whatever came back
with nothing, slowly, with backoff. Run it second, not instead.

## Before you post

Read the risk section at the bottom of CAPTIONS.md. Short version: organic is fine,
never put ad spend behind this one, and the safer swaps for slides 3 and 4 are written
out there ready to paste.
