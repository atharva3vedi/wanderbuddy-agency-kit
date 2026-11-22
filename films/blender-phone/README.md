# Pop-out screenshot set (WanderBuddy 2.0)

The 2.0 listing set. Same story beats as the flat set one folder up (one
headline per frame, the jet that leaves the globe on the first frame and flies
level through the set), rebuilt in 3D and taken travel-anywhere: Sam's crew
(Maya, Leo, Priya) plans Tokyo, saves a Bali reel, votes and splits costs in
Lisbon, drives Iceland's Ring Road, talks Spanish in Mexico City, and the last
frame's globe lights up routes from London to all of them.

- Every phone is a modelled phone in Blender with the real 2.0 screen on it
  (the Flutter harness in `../build/flutter`, fake data, no personal data),
  turned and leaning a little differently on each frame, same size and height.
- No default art: the Tokyo trip wears a real photo cover and the crew have
  profile photos (avatars, plan and budget stacks, live rows), and the same
  photos are on the 3D tokens and map pins.
- The part of the screen each frame is about lifts off the glass toward you,
  out of an empty recessed slot: the trip card, the idea votes, the day chips
  and the vote, "You get back 30 EUR" and the crew, the passport row, the
  readiness rows, the live-location rows, the translated line.
- 3D props carry the feature: crew tokens, checks, coins in EUR/USD/GBP/JPY,
  a passport, a 5/5 ring, map pins, the globe with its routes, the jet.
- The frames form one panorama (the idea of the Figma template set): one night
  sky, trip-light glows and a level route line run under all of them, and
  props (tokens, coins, the passport, pins, globes) cross frame edges on
  purpose. Cards with text always stay inside their own frame.
  (`build/pop/edge_check.py` is for a no-spill variant: it flags anything
  solid at a frame edge.)

## What to upload

- `apple/`: 10 frames at 1284x2778, RGB, upload 01 to 10 in order.
- `play/`: 8 frames at 1080x1920 (drops entry requirements and language) and
  `feature-graphic-1024x500.png`.

## Figma

"WanderBuddy 2.0 Store Screenshots" in the founder's drafts, built by
`../build/pop/dist/pop-figma.js`: two pages (App Store, Google Play), each one
panorama frame with export slices over the screenshots. Headlines are live
text, glows are plain ellipses, the 3D layers are image fills.

## Rebuilding

Phone screens, only when the app UI or the fixtures change (repo root; each
`SCENE` writes `build/screens_v2/<scene>/`):

```
python store/graphics/appstore/build/flutter/make_inter_thai.py
C:\flutter\bin\flutter test store/graphics/appstore/build/flutter/store_screens_test.dart --dart-define=SCENE=tokyo --dart-define=SHOT=home,plan,documents,prepare,reels
C:\flutter\bin\flutter test store/graphics/appstore/build/flutter/store_screens_test.dart --dart-define=SCENE=lisbon --dart-define=SHOT=plan,budget
C:\flutter\bin\flutter test store/graphics/appstore/build/flutter/store_screens_test.dart --dart-define=SCENE=iceland --dart-define=SHOT=live
C:\flutter\bin\flutter test store/graphics/appstore/build/flutter/store_screens_test.dart --dart-define=SCENE=spanish --dart-define=SHOT=translate
python store/graphics/appstore/build/live_map.py iceland <lat> <lng> <zoom> 480
```

(`<lat> <lng> <zoom>` = the iceland run's `LIVE: camera` line; it was
63.79024 -20.54719 7.69. Each scene leaves a ~125 MB compile in
`build/test_cache`; clear it if C: is tight.)

Then, from `store/graphics/appstore`:

```
node build/pop/textures.mjs
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python build/pop/scene.py -- 01
python build/pop/edge_check.py
node build/pop/compose.mjs
node build/pop/figma.mjs
```

`scene.py` renders one frame per run (ids 01 to 10 and `fg`, about 30 s each
on the RTX 5070 Ti; add `preview` for a fast 40% draft). Everything about a
frame (which screen, its phone angle, which crop lifts and how far, props) is in
`build/pop/frames.json` (`pose` at the top is only the fallback); the panorama
(glows, route, headline fit) is in `compose.mjs`.
