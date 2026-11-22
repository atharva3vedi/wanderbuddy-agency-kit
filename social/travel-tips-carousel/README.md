# Travel tips carousel

A 14 slide photo carousel for Instagram and TikTok: a cover, 12 genuinely
non-obvious travel tips, and one CTA slide. Photo led rather than the flat navy
`marketing/ig-quote-cards` system, because this one has to hold its own on a
travel feed next to other people's holiday photos.

```bash
node fetch-photos.mjs   # sources/ + sources/index.json   (only needed once)
node build.mjs          # build/{ig,tiktok}/*.html + manifest.json
node render.mjs         # out/{ig,tiktok}/*.png
node render.mjs ig      # just one variant
```

Output:

| Variant | Size | Where |
|---|---|---|
| `out/ig/` | 1080x1350 (4:5) | Instagram carousel, the tallest IG allows |
| `out/tiktok/` | 1080x1920 (9:16) | TikTok photo post, IG Stories |

Copy for both platforms is in [CAPTIONS.md](CAPTIONS.md).

## Where the photos come from

Pexels, under the [Pexels Licence](https://www.pexels.com/license/): free to use,
commercial use allowed, no attribution required, modification allowed.
`sources/index.json` records the Pexels id, source page and search query behind
every file, so provenance is checkable later.

**Not Instagram.** Photos on Instagram belong to the people who shot them.
Reposting them inside a branded WanderBuddy carousel is a takedown notice, or a
bill, waiting to arrive. Pexels gets the same candid travel aesthetic with none
of that exposure. If you ever do want a specific creator's shot, ask them and get
it in writing, then drop the file into `sources/` and point the slide at it.

## Editing

Everything is in the `slides` array at the top of `build.mjs`.

- `photo` is a filename stem in `sources/`.
- `focus` is a CSS `object-position`. It decides what survives the crop when the
  same photo is squeezed from 4:5 into 9:16, so check both variants after changing it.
- `tweak` is an optional CSS transform, for shots whose subject sits so low in the
  frame that it would otherwise render entirely behind the copy. Use it sparingly,
  it costs resolution.

Type scales off the canvas height, so both variants stay proportional from one
set of numbers.

## House rules

Same as the rest of `marketing/`: no em dashes, no pricing, no features we do not
ship. Beyond that, every tip on these cards is a real rule that a reader can go
and verify, because a carousel of confident nonsense is worse than no carousel.
See the accuracy notes at the bottom of CAPTIONS.md before answering comments.
