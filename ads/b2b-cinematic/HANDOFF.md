# Handoff (all four films finished 2026-11-11)

Read README.md (commands) and TREATMENT.md (the four films and their words) first.
Nothing is committed; this folder is untracked. No render is running.

## Where each film stands

| Film | `out/` file | State |
|---|---|---|
| 1 Departures | `1-departures.mp4` | Final. Frames 380 to 515 re-rendered with the new ending: the phone sits lower and smaller, the ring on Hold my spot is above the Reels zone. |
| 2 Order | `2-order.mp4` | Final. |
| 3 23:48 | `3-2348.mp4` | Final. Frames 283 to 515 re-rendered (brighter street, the traveller's full question on screen). The second line now ends at 10.2 s (was 11.4 s) in `build/night.supers.json`, because its last second sat white on the white inbox. |
| 4 Day 2 | `4-day2.mp4` | Final, re-cut from complete frames. |

All eight files (four films and their `_share` copies) decode end to end: 1080 x 1920, 593 frames, 24.7 s, -13.7 to -14.1 LUFS.

## Open choices for the founder

- Film 1 shows the listing's own price (US$690) on the phone, as the earlier 30 s ad did.
- Film 2 has no last line: white text did not read on the pale pages, so the ring on the CRM's Ask line carries it.
- Film 3's closing line ("It answers from your trip plan, day and night.") crosses the lit laptop in the wide shot: the word "from" sits on its screen. It reads, but moving it needs a new place in the frame (below it runs into the Reels zone, above is the bright window).
- No voiceover in any film (music and words only); Hannah could be added later with the b2b-reels recipe.

## Second pass (2026-11-11)

The founder found the four films above too simple and too alike (same music), and all Krabi.
TREATMENT_V2.md has the new set: five films, five countries, each a small story with a loser.

- **Built:** film 1, Three Agencies (Hanoi, Ha Giang Loop), as the pilot: `out/v2-three-agencies.mp4`
  and `_share`, 1080 x 1920, 29.6 s, 710 frames, -14.0 LUFS, decodes end to end. Rebuild commands are
  at the bottom of README.md.
- **Stand-ins in the pilot:** the score is our own piano notes only, and there is no rain or shutter
  sound. MUSIC_SHORTLIST.md lists licensed tracks to pick from; nothing has been downloaded.
- **Weakest shot:** the dawn street (20.5 s on) is flatter and more low-poly than the night shots.
- **Waiting on the founder:** whether this style is right for the other three films (Monsoon,
  Opened 3 Times, Empty Seats) and a new score for Day 2; which tracks to download.
- Nothing is committed. The four first-pass files in `out/` are untouched.

### Second cut of the pilot (2026-11-11, afternoon)

The founder preferred the first pitch (one traveller, three agencies) and asked for one clear winner
and how it won by using WanderBuddy, and said the music can be generated.

- **Built:** `out/v3-three-agencies.mp4` and `_share`: 1080 x 1920, 32.3 s, 775 frames, -13.7 LUFS,
  decodes end to end. The winner is Lantern Trips, because its trip is listed on WanderBuddy: she
  holds two spots on the real listing at 23:49 and it lands in the real CRM inbox. The azure ring
  lands on its sign at dawn. End card: "List your trips on WanderBuddy, free."
- **Why the listing and not an auto-reply:** nothing answers a new enquiry by itself today. A message
  to an agency's number only goes into its inbox; the assistant answers travellers on a live trip.
- **Score:** generated in `build/agencies2_audio.py` (synthesized strings, pulse, rain, two low hits,
  real piano notes). Measured, never listened to: the founder has to judge it by ear.
- **Kept:** `out/v2-three-agencies.mp4`, the first cut (the assistant answering a pickup question).
- **Still waiting on the founder:** whether to build Monsoon, Opened 3 Times and Empty Seats this way.
  Empty Seats was the free-listing film; this cut now covers the listing, so it may not be needed.

### The rest of the second pass (2026-11-11, 16:20)

The founder said "Yes, build the rest".

| Film | File | State |
|---|---|---|
| Three Agencies, second cut | `out/v3-three-agencies.mp4` | Done (see above). |
| Day 2, own score | `out/v2-day2.mp4` | Done: same frames as `4-day2.mp4`, generated score, 24.7 s, -13.4 LUFS, decodes end to end. |
| Monsoon | `out/v2-monsoon.mp4` | Screens, props, scene, captions and score done. Render running: `render/monsoon/3d`, 660 frames. |
| Opened 3 Times | `out/v2-opened-3-times.mp4` | Screens, props, scene, captions and score done. Render queued behind Monsoon. |
| Empty Seats | none | Not built: Three Agencies now sells the free listing. |

`build/_queue_rest.sh <monsoon blender pid>` is running: it waits for the Monsoon render, cuts it, copies the
dawn-street frames into `render/opened/3d`, renders Opened 3 Times with `WB_RESUME=1` and cuts it.
If the Mac slept through it, finish by hand with the commands at the bottom of README.md
(`WB_RESUME=1` skips frames already on disk).

Every generated score was measured, never listened to. The founder judges the sound.

### Second pass complete (2026-11-12, 13:30)

All renders finished once the Mac was awake and on power. Each file is 1080 x 1920, 24 fps, decodes end
to end, with a `_share` copy:

| File | Length | Loudness |
|---|---|---|
| `out/v3-three-agencies.mp4` | 32.3 s | -13.7 LUFS |
| `out/v2-monsoon.mp4` | 30.7 s | -13.8 LUFS |
| `out/v2-opened-3-times.mp4` | 30.3 s | -13.7 LUFS |
| `out/v2-day2.mp4` | 24.7 s | -13.4 LUFS |

No render is running. `build/_queue_rest.sh` and `build/_make_opened.py` were one-offs and can be deleted.
Waiting on the founder: the verdict on the pictures and, above all, the generated scores, which nobody has
listened to. Nothing is committed; the whole folder is untracked.

### Rendering faults fixed (2026-11-12, 14:20)

The founder flagged rendering issues in Opened 3 Times (the music was fine). Three faults, fixed in the
scripts by `build/_fix_screens.py` and re-rendered with `build/_rerender_fixes.sh` (both one-offs):

1. Phone screen images were square planes, so their corners stuck out past the rounded glass. They are
   rounded slabs now. This was also in Three Agencies (her phone, the phone next door) and Monsoon (the phone).
2. The laptop's change of screen was a crossfade during a camera pan, which ghosted into a double image
   (EEVEE runs two motion-blur steps). It is a cut now. This was also in Monsoon.
3. Opened 3 Times only: her phone went black between opens. It now shows her lock screen, Tuesday 07:42 and
   Tuesday 22:10, with the other agency's quotation still unread.

Re-rendered: opened 0 to 239 and 352 to 419; monsoon 0 to 83 and 440 to 515; agencies2 192 to 347 and
468 to 563. All three films re-cut, same lengths and scores, every frame valid, each decodes end to end.

### Blue alignment fixed (2026-11-12, 15:40)

The founder flagged a "blue aligning issue". Three were found and fixed (`build/_fix_blue.py`,
`build/_rerender_blue.sh`, both one-offs), in every film they touch:

1. The azure ring on the Lantern Trips sign was taller than the gap under the balcony: its top edge was
   hidden and it read as a lopsided U. It now hugs the sign (3.78 x 0.63 m at z 3.23).
2. The ring on a Home row sat on the next row's border. It is 4 px shorter.
3. End cards: the mark and wordmark sat 14.5 px right of centre while the lines under them were centred
   (the wordmark width in `endcard.py` is an estimate). `endcard_v2.py` and `endcard_v3.py` move the lockup
   14.5 px left; measured centre is now 540.5 of 1080. The first-pass `endcard.py` still has the offset, so
   `v2-day2.mp4` now uses the `endcard_v2` card ("You run the trips. WanderBuddy runs the rest.").

All four second-pass films re-cut and decode end to end. Next: a sixth film on the itinerary maker and
the assistant (script in TREATMENT_V2.md, film 6), waiting on the founder's go.

### Film 6, The Reel (2026-11-12, 16:25)

The founder asked for a film on the itinerary maker and the assistant, then said "Yes, build it".

- **Built:** `out/v2-the-reel.mp4` and `_share`: 1080 x 1920, 35.2 s, 845 frames, -13.7 LUFS, every frame
  valid, decodes end to end. Script and what is real in TREATMENT_V2.md (Film 6); commands in README.md.
- **Honesty limits kept:** the panel's speed is the demo's stand-in, so its clock and "Ready in 4 seconds"
  are hidden and no caption says how fast it is. The AI is never shown sending anything or closing alone:
  the captions say "You press one button" and "You press Send".
- **Known soft spots:** only four real Vietnam photos exist, so they repeat across the fourteen pages; the
  "Your package" page's price line renders with a highlight that reads like a strikethrough (it does in
  the demo too), so the film never goes close on it.
- The second-pass set is now five films: three-agencies (v3), monsoon, opened-3-times, day2, the-reel.
  No render is running. Nothing is committed.

### 4:5 LinkedIn cuts (2026-11-12, 22:00)

The founder asked whether the films were optimised for LinkedIn, then for 4:5 cuts. Made with
`build/compose_45.py` (crops, no re-render): `out/linkedin/v3-three-agencies_4x5.mp4`, `v2-monsoon_4x5.mp4`,
`v2-opened-3-times_4x5.mp4`, `v2-day2_4x5.mp4`, `v2-the-reel_4x5.mp4`. Each 1080 x 1350, same length and
score as its 9:16 film, decodes end to end, -13.4 to -13.8 LUFS, 6 to 14 MB.
What a 4:5 cut loses: the bottom of the phones (the listing's price bar, "1 of 14"), some road and desk.
Nothing is committed.
