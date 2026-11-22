# Reel: "i could never overthink my trip" (steak POV)

Relatable 9:16 meme reel, ~19.6s, 1080x1920 / 30fps. Built 2026-09-20.

**Final:** `overthink_my_trip.mp4`

## Concept
First-person "shot on iPhone" POV b-roll (hands only, no faces) of eating steak
while travelling, with on-screen captions carrying the joke, then the WanderBuddy
punchline + the approved brand outro.

- 0.0-5.0s  clip 01 (steak cut)      -> "i could never be a person / who overthinks my trip"
- 5.0-10.0s clip 02 (plane/passport) -> "no 47 tabs. / no 2am “what if it rains”."
- 10-12.5s  clip 03 (steak + ocean)  -> "planned in 5 minutes. / not 5 weeks."
- 12.5-15s  logo icon                -> "thanks to WanderBuddy. / or something."
- 15-19.6s  `marketing/outro/outro.mp4` (wave -> wordmark -> Download now)
- WanderBuddy app-icon badge watermarked top-left across the b-roll.

## Sources
- `clips/` = the three raw Seedance clips (720x1280, 24fps, no audio, no watermark).
  Model `dreamina-seedance-2-5-260628`, seeds 27529 / 77672 / 89281.
- Logo = `assets/icon/app_icon.png` (rounded in post). Captions rendered
  deterministically with PIL (never by the video model).
- Audio = subtle ambient bed on the b-roll + the outro's own VO/chime. Swap in
  trending audio in-app if desired.

## Rebuild
Overlay/caption assets + ffmpeg graph live in the session scratchpad
(`steakreel/make_assets.py`, `vg.txt`). Regenerate clips via the `seedance` MCP,
re-run the PIL asset script, then the 3-stage ffmpeg assembly (body -> captions ->
concat outro).
