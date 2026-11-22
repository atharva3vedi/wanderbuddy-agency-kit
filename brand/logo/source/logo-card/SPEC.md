# WanderBuddy — Beach-to-Logo Transition (production spec)

The intro that opens every video. It is not a gimmick: **your logo is a beach.**
The mark is two white peaks (a headland) over a white wave band on sky-blue. So
the transition is a *match-cut* where a real beach resolves into the mark. The
world becomes the logo.

You chose "spec only, I produce." This is the spec: exact Higgsfield prompts,
frame timing, three production routes ranked, and the ffmpeg recipe. The **back
half (the logo reveal) is automated** in `../ugc-autocut/` so you only ever
generate the beach plate; the mark, the flood, and the wordmark render
deterministically and free.

Brand truth (from `lib/theme/app_colors.dart` and `assets/icon-master.svg`):
- Logo field blue: `#2072B8`
- App azure: `#1E88D6` · teal: `#1FA89A` · amber: `#E0972A` · ink-navy: `#0B141F`
- Mark: two white triangular peaks + a white wave band, white wordmark below.

---

## The beat sheet (3.0s hero, 30fps = 90 frames)

| Frames | Time | What happens |
| --- | --- | --- |
| 0-33 | 0.00-1.10s | Real beach. A **twin-peaked headland** sits on the horizon, dead-center. Slow push-in. A wave advances in the foreground. Graded azure/teal. |
| 33-45 | 1.10-1.50s | The foreground wave surges toward camera; white foam starts climbing the frame from the bottom. |
| 45-51 | 1.50-1.70s | **Foam fills the frame — pure white. This is the cut point.** The crash hides the transition. |
| 51-72 | 1.70-2.40s | Foam recedes, but it recedes onto the **flat logo**: the white peaks + wave band, now geometric, on the blue field `#2072B8`. The horizon has become the mark. |
| 72-90 | 2.40-3.00s | Wordmark `WanderBuddy` rises in under the mark. Hold one beat. Cut out (to app footage / content). |

The magic is in frames 45-51: the real breaking wave and the logo's wave band are
the same white shape, so the eye accepts the swap.

**Two other lengths, same beats compressed:**
- **1.5s social punch** (45f): beach 0-18, foam 18-24, logo reveal 24-45. No
  wordmark rise, mark is just there. Use on TikTok/Reels where the first second is
  sacred.
- **2.0s ASO/App-Preview** (60f): beach 0-24, foam 24-30, logo+wordmark 30-60.

---

## Route B (RECOMMENDED) — the foam luma-wipe

The most elegant and the most on-brand: real water literally becomes the logo's
wave. Two Higgsfield plates, then `ugc-autocut` does the wipe.

### Plate 1 — the approach (Higgsfield `generate_image` → `generate_video`)
IMG prompt:
```
Empty tropical beach at blue-golden hour, a dramatic twin-peaked rocky headland
on the horizon with two distinct triangular peaks, calm sea, wet sand reflecting
the sky, low camera near the waterline, perfectly symmetrical composition centered
on the twin peaks, cinematic teal and azure color grade, soft atmospheric haze,
no people, no boats, no text, 9:16 vertical
```
Negative:
```
people, boats, buildings, text, watermark, birds, palm trees on the horizon,
harsh lens flare, tilted horizon, jpeg artifacts
```
Motion: image-to-video, **5s, 9:16**, preset **slow push in**. Note: "slow dolly
push toward the twin peaks, gentle sea, foreground water advancing." Keep the
horizon level and centered.

### Plate 2 — the crash (the wipe material)
IMG prompt:
```
A large ocean wave breaking directly toward the camera, an explosion of white
foam and sea spray filling most of the frame from the bottom up, water surging
over the lens, backlit blue-golden hour, motion blur in the spray, no people, no
text, 9:16 vertical
```
Motion: image-to-video, **5s, 9:16**, preset **crash zoom / push in**. Note: "the
wave breaks and white foam rushes up and fills the entire frame."

### The composite (automated)
`ugc-autocut` treats the frame where foam peaks (near white) as a luma matte and
wipes from the beach into the rendered logo card. The recipe it runs:
```
# beach plate → foam crash → white peak used as a wipe into logo-card.png
ffmpeg -i approach.mp4 -i crash.mp4 -loop 1 -i logo-card.png \
  -filter_complex "
    [0:v]trim=0:1.5,setpts=PTS-STARTPTS,scale=1080:1920,setsar=1[a];
    [1:v]trim=0:0.5,setpts=PTS-STARTPTS,scale=1080:1920,setsar=1[b];
    [2:v]trim=0:1.5,scale=1080:1920,setsar=1[c];
    [a][b]xfade=transition=fade:duration=0.25:offset=1.25[ab];
    [ab][c]xfade=transition=hlwind:duration=0.35:offset=1.75,format=yuv420p[v]
  " -map "[v]" -r 30 -c:v libx264 -crf 18 -pix_fmt yuv420p intro.mp4
```
(`ugc-autocut` swaps in a true luma wipe from the foam when the crash plate is
clean; `hlwind`/`fade` is the reliable fallback. You do not run this by hand —
`node autocut.mjs intro.json` does.)

---

## Route A (SAFE) — whip-pan match cut

Cheapest, near-impossible to get wrong. One plate + a whip. Use if you want it
shipped today.

- One plate: the **approach** clip above, but add a fast horizontal camera whip at
  the end (motion note: "ends on a fast whip pan to the right").
- `ugc-autocut` cuts on the whip's motion blur into the logo card, which enters
  with a matching whip. The eye reads it as one continuous move.
- Transition in the recipe: `xfade=transition=wiperight:duration=0.18`.

---

## Route C (AMBITIOUS) — direct AI morph

The most "how did they do that," the least predictable. Use Higgsfield keyframe /
start-end frame:
- **Start frame:** the beach still (Plate 1 image).
- **End frame:** `logo-card.png` (rendered from `logo-card.html`).
- Let the model interpolate beach → mark over ~1.2s.

Risk: morphs can go mushy in the middle. Generate 2-3, keep the cleanest, and
still hand it to `ugc-autocut` to add the wordmark rise and trim to length. Only
spend the video credits here once Route B is already banked as your safe intro.

---

## Sound (do not skip — this is half the "sick")

- A low azure swell / ambient pad under the beach (your `assemble.js` already
  builds a warm pad bed; reuse it).
- A soft **whoosh** timed to the foam fill (frame 45).
- A single clean **bloom/chime** on the mark settle (frame 51), one note, in key
  with the pad.
- Audio cuts one beat *before* the picture on the hand-off out. Silence for 3
  frames before the content starts reads as intentional.

---

## Assets in this folder

- `logo-card.html` — the reveal end-frame at 1080×1920: blue field `#2072B8`,
  centered white mark, wordmark. Render it to `logo-card.png` with
  `node render-logo-card.mjs` (headless Edge, same method as `ig-quote-cards`).
- `intro.example.json` — the `ugc-autocut` script that produces the intro. Run:
  `node ../ugc-autocut/autocut.mjs marketing/logo-transition/intro.example.json`.

## Once, then never again

Generate the two plates once. Render the logo card once. After that the intro is a
deterministic composite: every video gets the exact same branded open at zero
credits, and you can regenerate all of them if you ever change the plate.
