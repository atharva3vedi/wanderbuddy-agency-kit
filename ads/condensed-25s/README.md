# 30 s ad: the panic, then the marketplace, CRM and app together

A short cut of the 2:26 cinematic agency ad that went on LinkedIn on 11-06. The first cut (25 s, 11-10) is `out/wanderbuddy-25s.mp4`. The current one is 30 s, in two shapes:

- `out/wanderbuddy-30s.mp4` (16:9, 1920x1080)
- `out/wanderbuddy-30s_9x16.mp4` (9:16, 1080x1920)

Each has a smaller `_share` copy next to it.

| Time | What happens |
|---|---|
| 0 to 7 s | **The panic, all at once.** A dark desk, Word itineraries landing, a phone buzzing under banners, chat bubbles and a broken sheet piling up. Each bubble plays WhatsApp's own incoming-message tone over a low piano pulse. Captions: "You started an agency to *sell* trips." and "Not to scroll 400 messages for one PDF." |
| 7 s | Everything is pulled into the middle. A light disc with the one azure ring opens onto the brand, and the lockup appears. |
| 9 to 12 s | **The marketplace**: the real /trips page with the sample trip, scrolling to Hold my spot. Line: "Brings travellers ready to book." The hold flies into the laptop. |
| 13 to 17 s | **The CRM**: Listings with holds waiting ("Runs the business."), then the WhatsApp thread in the inbox ("Every chat, one inbox."), then Trips. The plan flies to the second phone. |
| 18 to 23 s | **The app**: the plan ("Runs the trip."), then the group's live map. The camera pushes in and Maya, Leo and Priya's rows lift off the screen ("The whole group, live on one map."). |
| 24 to 26 s | All three on one thread. Line: "Everything in one place." |
| 26 to 30 s | Azure end card: "Ready to upgrade? Message us today.", the lockup, wanderbuddyapp.com/partners, with the end card's own piano. |

## Where the material comes from

- **CRM:** the public Lantern Trips demo (`/trydemo`, sample data), captured with headless Chrome.
- **Marketplace:** the live `/trips` page, with the demo's own sample trip answered in place of the empty live listing RPCs (`build/capture.mjs`).
- **App:** the real 2.0 screens in `store/graphics/appstore/build/screens_v2`. The live map is `iceland/live_composited.png`, and the rows that lift off are crops of that same screen.
- **Sound:** `marketing/music` (piano notes, the bossa bed, the end card's piano). The one exception is `audio/whatsapp_incoming.m4a`, WhatsApp's default incoming-message tone, copied from the Mac WhatsApp app. The founder chose it on 11-10 knowing it is Meta's sound and not licensed for ads; swap it for a licensed ping if a platform objects.

## Rebuild

Run these from this folder. They need Blender 5.3 (`brew install --cask blender`), ffmpeg, Node and Google Chrome. Add `--916` to the Blender and overlay steps, and `916` to compose, for the 9:16 cut.

```bash
cd build && npm i && cd ..
node build/capture.mjs                 # real screens -> screens/
node build/cards.mjs                   # flat props, chips, lockups -> cards/
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build/build.py -- stills 1,10.2,21.8   # half-size checks
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build/build.py -- anim                 # 796 frames, about 13 min on the M5 Pro
node build/overlay.mjs                 # captions, ring, lines, end card -> render/v30_169/overlay/
python3 build/audio.py                 # out/audio30.wav, -14 LUFS two-pass
bash build/compose.sh                  # out/wanderbuddy-30s.mp4 and _share copy
```

To change a word or a timing, edit `build/overlay.html` (a pure function of `__seek(t)`, with a 9:16 layout under `?f=916`). Then re-run `overlay.mjs` and `compose.sh`; Blender does not need to run again.
