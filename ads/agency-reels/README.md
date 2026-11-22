# B2B listing reels

Three Instagram reels asking travel agencies to list their trips on WanderBuddy. Scripts, claim
notes and post captions: `SCRIPTS.md`. Approved 2026-10-28 (all three).

## Status

| Reel | File | Length | State |
|---|---|---|---|
| 2 Post #214 | `out/WanderBuddy_B2B_Reel2_Post214.mp4` | 28.7s | Done (v3) |
| 3 Three questions | `out/WanderBuddy_B2B_Reel3_ThreeQuestions.mp4` | 32.0s | Done (v3) |
| 1 Walk-in | `out/WanderBuddy_B2B_Reel1_WalkIn.mp4` | 35.6s | Done, animated skit (`?reel=r1`) |

Each has a smaller `_share.mp4` copy (same edit, for phones). All 1080x1920, 30 fps, -14 LUFS, captions burned in, $0 spent: Hannah on the Groq free tier, a Pixabay
bossa nova track and University of Iowa piano notes in `assets/` (licences in SCRIPTS.md).

## What's where

- `build/reel.html`: all three animated reels (one page, `?reel=r1`, `r2` or `r3`), every frame a
  function of time. `build/render.mjs` renders it.
- `build/vo/<reel>/lines.json`: the lines and the voice (Hannah). `vo.py` records them, `timeline.py` lays them out,
  `check_vo.py` transcribes them back with Whisper.
- `build/audio.py`: the bossa nova track, piano notes on the page's cues, voice ducking, one
  soundtrack across the reel and the end card.
- `build/build.sh <reel> <name>`: frames, soundtrack, end card, loudness, into `out/`.
- `endcard/`: the Blender wave outro with "DM us your trips" and no store badges (`endcard.mp4`).
- `reel1/`: the two inserts (trip card, CRM) and `edit.json`. `build/reel1.py --probe`
  transcribes the takes in `reel1_takes/`; `build/reel1.py` cuts the reel from `edit.json` with
  captions from the founder's own words.

## Rebuild

```bash
cd build
bash build.sh r2 WanderBuddy_B2B_Reel2_Post214
bash build.sh r3 WanderBuddy_B2B_Reel3_ThreeQuestions
bash build.sh r1 WanderBuddy_B2B_Reel1_WalkIn
```

Change a line: edit `vo/<reel>/lines.json`, then `python vo.py <reel> <line index>`,
`python timeline.py <reel>`, `python check_vo.py <reel>`, then `build.sh`. Same input text gives
the same Orpheus take, so change the wording to get a new one. Use the hyperframes venv python
(`~/.cache/hyperframes/tts/venv/Scripts/python -I`), as in `build.sh`.

Run one render at a time.
