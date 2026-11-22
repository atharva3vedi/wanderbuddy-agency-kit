# Four cinematic films for agencies (9:16, 24.7 s each)

One film per thing we sell an agency, each built on one picture from art or design
history, rendered in Blender 5.3 (EEVEE) on this Mac. The why and the words are in
[TREATMENT.md](TREATMENT.md).

| File | Sells | Picture |
|---|---|---|
| `out/1-departures.mp4` | The free listing on /trips | A split-flap departures board in a dark hall, one shaft of window light |
| `out/2-order.mp4` | The CRM's itinerary maker | Knolling: the week's paper squares itself up, then the real pages deal out |
| `out/3-2348.mp4` | The WhatsApp and Instagram assistant | Hopper: a closed office on a wet street, the laptop answering alone till dawn |
| `out/4-day2.mp4` | The trip app travellers join | A shanshui scroll: karst in blue-hour mist, seven boat lights, then the app |

Each has a smaller `_share.mp4` next to it. 1080 x 1920, 24 fps, H.264 + AAC, -14 LUFS.
Everything a viewer must read sits between 220 px from the top and 420 px from the bottom.

## What is real

- **Screens** (all the Lantern Trips sample agency, never a real client):
  - `screens/marketPhone.png`: the live /trips listing with the demo's sample trip (from `../condensed-25s`).
  - `screens/pages/pg*.png`: the 14 pages of the public demo's "Krabi Islands, small group" itinerary,
    captured by `build/capture_pages.mjs` (view only, nothing saved) and drawn the way the PDF prints:
    the editor's hints and add buttons hidden, an empty photo slot as a plain tint.
  - `screens/crm-itinerary_pdf.png`, `crm-inbox_assistant_pickup.png`, `app-home.png`, `app-chat.png`:
    the kit captures in `metrics/kit/screens/`. `inbox_before.png` and `inbox_reply.png` are that inbox
    capture split in two so the assistant's reply can arrive on screen.
- **Props** in film 2 (`screens/props/`, `build/stills.mjs props`) are set dressing drawn in Chrome:
  a rate sheet, an old dense PDF, a voucher, a boarding pass, a passport cover with no country, a polaroid
  of the listing's own Krabi photo, sticky notes in Bradley Hand.
- **Sound**: `marketing/music` only. The Pixabay bossa bed and the Iowa Steinway notes (E and A are
  D and G shifted a whole tone). The piano gets a room reverb; nothing is synthesized. Every note is
  listed in `out/audio/<film>.json`.
- **End card**: `app-25s/build/shots.py` end(), unchanged, at 24 fps: "For travel agencies." and
  wanderbuddyapp.com/partners.

## Rebuild

From this folder. One heavy render at a time (check `pgrep -fl Blender`). EEVEE on the M5 Pro is
about 4 s a frame at full size; `WB_QUICK=1` renders half size at a quarter of the samples for checks.

```bash
B=/Applications/Blender.app/Contents/MacOS/Blender
PY=/Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13
node build/stills.mjs atlas                       # split-flap glyphs (WbSans Bold)
node build/stills.mjs props                       # film 2's paper
node build/capture_pages.mjs                      # the real itinerary pages
$B -b --factory-startup -P build/departures.py    # render/departures/3d, 516 frames
$B -b --factory-startup -P build/order.py         # render/order/3d
$B -b --factory-startup -P build/night.py         # render/night/3d
$B -b --factory-startup -P build/day2.py -- land  # render/day2/land, 360 frames
$B -b --factory-startup -P build/day2.py -- phone # render/day2/phone, 186 frames (from 13.75 s)
$B -b --factory-startup -P build/endcard.py       # render/endcard, 84 frames
for f in departures order night day2; do node build/stills.mjs supers $f; done
$PY build/audio.py                                # out/audio/<film>.wav
python3 build/compose.py                          # out/*.mp4
```

Stills for checking: `$B -b --factory-startup -P build/order.py -- still 30 200 400`.
Re-render a range: `WB_FROM=380 WB_TO=515 $B -b --factory-startup -P build/departures.py`.
To change a word or its timing, edit `build/<film>.supers.json`, then re-run `stills.mjs supers <film>`
and `compose.py <film>`; Blender does not need to run again.

## Second pass (see TREATMENT_V2.md)

`out/v2-three-agencies.mp4` is the pilot: a Hanoi street at 23:47, 29.6 s. It has its own files and
touches none of the four films above.

```bash
B=/Applications/Blender.app/Contents/MacOS/Blender
PY=/Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13
node build/agencies_capture.mjs                    # the real inbox, Ha Giang trip (screens/agencies)
node build/agencies_stills.mjs                     # the lock screens next door (set dressing)
$B -b --factory-startup -P build/agencies.py       # render/agencies/3d, 634 frames, about 45 minutes
$B -b --factory-startup -P build/endcard_v2.py     # render/endcard_v2, the two-line end card
node build/stills.mjs supers agencies              # the words (build/agencies.supers.json)
$PY build/agencies_audio.py                        # out/audio/agencies.wav (our piano notes only)
python3 build/agencies_compose.py                  # out/v2-three-agencies.mp4
```

Stills: `WB_QUICK=1 $B -b --factory-startup -P build/agencies.py -- still 30 112 340 450 560`.
Gotchas found here: a sun must clear the far side of the street to reach a shop interior; EEVEE's
shadow pool overflows with many shadowed lights (sign and fill lights have shadows off); rain is a
wrapped mesh with CONSTANT keys so a wrap never smears; the frame before each cut renders without
motion blur (`per_frame`).

### Three Agencies, second cut (`out/v3-three-agencies.mp4`, 32.3 s)

One traveller, three agencies, one winner: the one whose trip is listed on WanderBuddy.

```bash
node build/agencies_capture2.mjs                   # the real listing on a phone, the held spots in the CRM
node build/agencies_stills2.mjs                    # the phone next door (set dressing)
$B -b --factory-startup -P build/agencies2.py      # render/agencies2/3d, 698 frames
$B -b --factory-startup -P build/endcard_v3.py     # render/endcard_v3: "List your trips on WanderBuddy, free."
node build/stills.mjs supers agencies2             # the words (build/agencies2.supers.json)
$PY build/agencies2_audio.py                       # out/audio/agencies2.wav: the generated score
python3 build/agencies2_compose.py                 # out/v3-three-agencies.mp4
```

Frames 0 to 175 are the first cut's street frames (agencies.py 0 to 83 and 96 to 187), copied in and
skipped with `WB_RESUME=1`; a clean render makes the same pictures. On battery in Low Power Mode EEVEE
runs at about 11 s a frame instead of 4.

### Monsoon, Opened 3 Times, Day 2 re-scored

```bash
node build/monsoon_capture.mjs && node build/monsoon_stills.mjs      # real board and Home; the paper and the phone
$B -b --factory-startup -P build/monsoon.py                         # render/monsoon/3d, 660 frames, about 6 s a frame
node build/stills.mjs supers monsoon && $PY build/monsoon_audio.py && python3 build/monsoon_compose.py

node build/opened_capture.mjs && node build/opened_stills.mjs       # real Home, board and itinerary cover; the phones
$B -b --factory-startup -P build/opened.py                          # render/opened/3d, 650 frames (516 to 649 = agencies2 564 to 697)
node build/stills.mjs supers opened && $PY build/opened_audio.py && python3 build/opened_compose.py

$PY build/day2_audio_v2.py && python3 build/day2_compose_v2.py      # out/v2-day2.mp4, same frames as 4-day2
```

`build/score_lib.py` is the synthesizer every generated score uses. `build/opened.py` is written by
`build/_make_opened.py` from `agencies2.py`; edit `opened.py` directly from here on.

### The Reel (`out/v2-the-reel.mp4`, 35.2 s)

```bash
node build/reel_pages.mjs                          # the 14 real itinerary pages as a Ha Giang plan (screens/reel/pages)
node build/reel_capture.mjs                        # the conversation, the proposal panel, Home, the inbox
node build/reel_stills.mjs                         # her phone (set dressing)
$B -b --factory-startup -P build/reel.py           # render/reel/3d, 768 frames
node build/stills.mjs supers reel && $PY build/reel_audio.py && python3 build/reel_compose.py
```

`build/reel.py` was written by `build/_make_reel.py` from `opened.py`; edit `reel.py` directly from here on.
The pages sit on their own desk at y = 90 m, far from the street set, lit by `plan_key` (340 W area light
4.8 m up: more than that blows the cream pages out to white).

### 4:5 cuts for the LinkedIn feed (`out/linkedin/*_4x5.mp4`, 1080 x 1350)

```bash
python3 build/compose_45.py            # all five; or: python3 build/compose_45.py reel
```

No Blender: `build/compose_45.py` crops the 9:16 frames to a 1350 px window that follows each shot
(top at 150 by default; 420 for Monsoon's phone so the "113 unread" badge stays in; 330 for The Reel's
panel so its whole result card stays in), lays the words out again inside the window, and crops the end
card around its own content. The Reel's pages shot starts as a crop and pulls back to the whole 9:16
frame so all fourteen pages show. The 9:16 films in `out/` are untouched.
