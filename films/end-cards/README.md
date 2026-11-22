# WanderBuddy video OUTRO / end-card

A ~4.6s branded end-card appended to the UGC videos. Concept: a real ocean
(Higgsfield plate, with baked wave sound) **resolves into the logo** — the two
white peaks rise out of the sea, the wave band forms, then the `WanderBuddy`
wordmark lifts and a `Download today` amber CTA pill blooms, over the brand field
`#2072B8`. A warm TV-ad voiceover says "Travel today, with WanderBuddy," under an
ocean bed + a soft settle chime.

Why this shape (marketing research, Sep 2026):
- **2–4s end card** for TikTok/Reels; the outro rides after the UGC hook.
- **Clear CTA** lifts CTR ~45%; the **recency effect** makes the logo+name stick.
- **3C in <3s**: what it is (logo+name) / trust (clean brand) / next step (CTA).
- Store badges can *drop* conversion 10–15%, so we show the app mark, not badges.

## Pieces
- `build-outro.mjs` + `render-outro.mjs` — render the brand-exact reveal LAYERS
  (peaks, wave, wordmark, CTA) as transparent 1080x1920 PNGs, plus `card-full.png`
  (flat end-frame). Deterministic, free, pixel-perfect text. `node build-outro.mjs && node render-outro.mjs`
- `ocean.mp4` — Higgsfield `kling3_0` ocean plate (9:16, native wave audio), 10 cr.
- `outro_isla.mp4` / `outro_arthur.mp4` — the finished outro, two VO takes
  (Isla = warm female, Arthur = confident male; seed_audio TTS). `outro_silent.mp4`
  is the picture-only version.
- `V1_overview_outro_isla.mp4`, `V2_planner_outro_isla.mp4`,
  `V1_overview_outro_arthur.mp4` — UGC finals with the outro appended.

## Rebuild the composite
The exact ffmpeg graph (layer reveal + audio mix + concat onto a UGC clip) is in
the session that produced this; the reveal layergraph lives in `vg.txt` in the
scratchpad. Layers + ocean + VO are all captured here, so it can be re-cut without
spending credits. Higgsfield has **no standalone SFX/music** model — ocean sound
comes from the video plate; the chime is synthesized locally.

## Hard rules (same as the rest of marketing/)
No em dashes, no pricing, no fake features. Brand: field blue `#2072B8`, white
mark/wordmark, amber accent `#E0972A`, from `lib/theme/app_colors.dart`.

## Blender v2 (2026-09-06, `blender/build_outro.py`)

Blue field (no sand), a whitewater wave that surges up, carries the card in and
pulls back. The five elements (logo, wordmark, Download now, App Store, Google
Play) are rigid bodies on damped springs whose anchors ride the foam front; a
turbulence field jumbles them during the crash and they settle out of order as
the wave recedes. Sim is baked to keyframes.

    "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\build_outro.py -- test   # 4 stills
    "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python blender\build_outro.py -- full   # frames/
    ffmpeg -framerate 30 -i blender/frames/f_%04d.png -c:v libx264 -crf 17 -pix_fmt yuv420p blender/outro_blender_silent.mp4
    ffmpeg -i blender/outro_blender_silent.mp4 -i audio/outro_final_audio.m4a -map 0:v -map 1:a -c copy -shortest blender/outro_blender.mp4

`audio/outro_final_audio.m4a` is the locked mix (beach wash + Arthur @1.5 s + chime @3.15 s).
`blender/sim_probe.py` prints per-element trajectories for tuning (`-- '{"TURB_STRENGTH": ...}'`).
