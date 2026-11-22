# Investor product demo, "One app, both ways to run a trip"

`out/wanderbuddy-investor-demo.mp4`: 1920 x 1080, 24 fps, 119 s, AAC, -14 LUFS.
`out/wanderbuddy-investor-demo_agency-only.mp4` is the earlier 86 s cut with no friends' act.
`out/wanderbuddy-investor-demo_share.mp4` is the smaller copy for email and decks.
SCRIPT.md has the story, the beats as built and the open choices.

## Layers

- **3D** (`build/demo.py`, Blender 5.3 EEVEE): two renders. The agency film is the original
  timeline (`render/3d`, frames 0-1920). The friends' act (B2C) is `WB_ACT=1`, frames 168-959 of
  the 119 s film (`render/3d_act`), with the agency scene held as it is at 7.0 s; `compose.sh`
  puts it in at 7 s and moves the agency film 792 frames (33 s) later. Both ends match, so no
  frame is re-rendered when a caption changes. The paper map, the laptop on Krabi, the
  phone on Singapore, the arc, the cards that lift off the screens, the itinerary pages,
  day to night to day. Every moving thing is a pure function of t, keyed on every frame.
  Shared helpers come from `../b2b-cinematic/build/film.py`.
- **Overlay** (`build/overlay.html`, a pure function of `__seek(t)`): captions, the
  lockup, the model lines, the end card. Change a word there, then re-run `overlay.mjs`
  and `compose.sh`; Blender does not need to run again.
- **Music** (`build/score.py`, with `../b2b-cinematic/build/score_lib.py`): the Pixabay
  bossa nova bed from `marketing/music` with the real Iowa Steinway notes on top.

## Where every screen comes from

| File in `screens/` | Source |
|---|---|
| b2c_dates, b2c_vote, b2c_reels, b2c_budget, card(Dates, Vote, Reel, Settle) | the app's own sample friends' trip, Bangkok Crew, from `../app-25s/screens` (Flutter harness, real widgets); the cards are the same crops the traveller ad lifts |
| b2c_igconnect (+ cardIgSteps), b2c_live (+ cardLive) | the app's Connect Instagram screen (`metrics/kit/screens/app-instagram.png`) and the Live location screen (`store/graphics/appstore/build/screens_v2/iceland/live_composited.png`; its rows are Maya, Leo and Priya, its map is the harness's Iceland sample) |
| crm-app_dashboard (+ cardAddon) | the CRM's WanderBuddy page (`metrics/kit/screens/crm-app_dashboard.png`), the app as an add-on |
| listings, inbox, inboxHold | the public Lantern Trips sample demo, wanderbuddyapp.com/trydemo (`build/capture.mjs`) |
| marketPhoneFull, marketPhoneBar | the live /trips page, its RPCs answered with that demo's sample trip and `listing_fee` answered as 0227 does for a 3% listing (`build/capture.mjs`); nothing is submitted |
| app-home, app-documents, app-chat, crm-inbox_assistant_pickup | the kit in `metrics/kit/screens/` |
| itinerary, pages/pg00-05 | the Krabi Islands itinerary of the public demo, its empty photo slots filled with crops of the demo's own two photos (`build/capture_itin.mjs`) |
| passport, rate_sheet | props from `../b2b-cinematic/screens/props/` |
| card*.png | crops of the screens above (the rows that lift off) |
| map.png, map_land.png, map.json | `build/map.mjs`, Natural Earth 50m from `website/node_modules/world-atlas` |
| igDM (+ cardIgDm), lockCrew, lockEve, lock2347, lock2348, boarding | `build/props.mjs`, plain set dressing, not product UI. igDM is the friend's DM to @wanderbuddyapp with the bot's real replies (`insp_saving`, `insp_enriched`) |

## Rebuild

From this folder. Needs Blender 5.3, ffmpeg, Node and Google Chrome; `build/node_modules`
links to `../condensed-25s/build/node_modules` (puppeteer-core).

```bash
B=/Applications/Blender.app/Contents/MacOS/Blender
node build/capture.mjs              # real screens -> screens/
node build/capture_itin.mjs         # the itinerary editor and pages, photo slots filled
node build/map.mjs                  # the map -> screens/map*.png
node build/props.mjs                # lock screens, boarding pass
WB_QUICK=1 $B -b --factory-startup -P build/demo.py -- stills 13.5,25.5,64   # half-size checks -> render/stills
$B -b --factory-startup -P build/demo.py -- anim          # the agency film, frames 0-1920 -> render/3d, about 3 s a frame on the M5 Pro
WB_ACT=1 $B -b --factory-startup -P build/demo.py -- anim # the friends' act, frames 168-959 -> render/3d_act
node build/overlay.mjs              # 2856 overlay frames -> render/overlay
/Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13 build/score.py   # out/score.wav (bossa bed + piano)
bash build/compose.sh               # out/wanderbuddy-investor-demo.mp4 and _share
```

`WB_FROM`/`WB_TO` re-render a range of frames; `WB_RESUME=1` skips frames already on disk.
One heavy render at a time on this Mac (`pgrep -fl "Blender -b"` first), on power, lid open.
