# WanderBuddy Cinematic Ad — Comp & Transition Map

**Path A edit sheet.** The `clips/` plates render the world + phone + interacting hand with a blank azure screen. In the edit you (1) track-and-replace the azure screen with the real UI from `screens/`, (2) build the motivated transition between each beat, (3) grade all nine to one look, (4) lay one continuous music bed. 9:16, ~40–45s, silent plates.

## Global comp notes
- **Screen replace:** the azure panel is the track target. Corner-pin / planar-track the real screen PNG onto it; the hand already taps/swipes in the plate, so time the on-screen UI reaction to the finger.
- **Grade to one look:** match white balance across beats (they roam warm↔cool); a light unifying LUT + grain sells "one continuous shot."
- **Brand blue:** azure `#1E88D6` (dark `#3FA7E6`) over ink-navy `#0B141F`.

## Per-beat map

| # | Clip | Beat / biome | Real screen (`screens/`) | Feature | Hand interaction in plate | Transition INTO next | Easter egg |
|---|---|---|---|---|---|---|---|
| 1 | `01_alpine` | Alpine dawn | `beat01_ai.png` | Create trip → AI itinerary | taps, swipes up | swipe-up carries the frame up → beach | mustard backpack |
| 2 | `02_beach` | Tropical beach | `beat02_photos-share.png` | **Capture & share a photo** | taps shutter, then share | swipe-left pushes world → Tokyo | orange cat on the boat |
| 3 | `03_tokyo` | Tokyo neon night | `beat03_community.png` | Community + chat | scrolls | a passing traveler crosses lens → market | the late runner |
| 4 | `04_market` | European market | `beat04_home-nearby.png` | Nearby + save a spot | taps to save | notification slides on-screen and wipes | cat on the crate |
| 5 | `05_group_budget` | Group dinner, dusk | `beat05_budget.png` | Split the bill | taps to split | camera orbits the phone → train | cat on the chair + receipt |
| 6 | `06_train_liveconv` | Scenic train | `beat06_liveconv.png` | Live Conversation | press-and-hold (talk) | window scenery whip-blurs → desert | cat on the seat |
| 7 | `07_desert` | Desert road | `beat07_home-route.png` | Route planning + live update | swipes to trace route | phone lifts toward skyline → rooftop | paper airplane on dash |
| 8 | `08_rooftop` | Rooftop sunset | `beat08_photos-memories.png` | Photo memories | taps to save a photo | thumb swipes up (home gesture) → ending | backpack + whole cast |
| 9 | `09_ending` | Dual-device reveal | — (logo on-screen) | — | phones settle / reveal | — | — |

Keyframe stills are in `stills/` (01, 02, 05, 06, 09 present; 03/04/07/08 = first frame of the matching clip).

## Ending build (clip `09_ending`)
- Plate: **iPhone (left) + Samsung (right)** semi-rotate to reveal the mountain logo on both screens; solid azure fill; **right ~55% left empty by design**.
- Comp your **real glyph** (`logo/glyph-white.png`) over the approximate on-screen mountain for a crisp mark.
- Fill the empty right with your **QR code + banner**.
- Add **One App. Every Journey.** and the **Google Play** badge.
- (Client chose dual-device iPhone+Samsung; the app ships Android-only.)

## Sound
- One continuous music bed (build → lift at rooftop → resolve on the logo). Plates are silent.
- Optional: soft UI ticks on taps; a sub-bass hit on the logo lock.

## Provenance
- Stills: Higgsfield `soul_cinematic` (0.12 cr each). Clips: `kling3_0` **pro** i2v, 1080p, silent (8.75 cr each).
- Clips also live on Higgsfield CDN; keep this local copy as the source of truth.
