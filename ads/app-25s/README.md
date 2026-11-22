# App-only 25 s cut of the mega cinematic ad

`app-25s.mp4`: 1920x1080, 30 fps, 25.000 s, AAC 48 kHz, mixed to -14 LUFS.
A condensed, app-only version of the 2:26 LinkedIn ad posted 11-06. The
CRM + App + Marketplace version is in `../condensed-25s/` (another session).

## Storyboard

| Time | Shot | On screen | Headline |
|---|---|---|---|
| 0.0-7.0 | `panic` | Dark. A phone at 05:02, buzzing; 28 traveller questions burst out of it at once ("Where do we meet the driver?", "I can't find my passport", "What time is pickup?", "Can I fly my drone at Maya Bay?"...) and pile up in depth. At 6.1 s they fall back into the phone, which turns into the WanderBuddy icon. | Every question lands on *you.* (the one serif word) |
| 7.0-8.7 | `logo` | Match cut to the light ground: the icon slides left and the wordmark comes in. | (lockup) |
| 8.7-12.1 | `docs` | Real Documents screen, Krabi Islands trip; ring on "Lantern Basecamp, Ao Nang (Lantern Trips voucher)". | Your vouchers, on their phone. |
| 12.1-15.6 | `plan` | Real Plan and Map screens; ring on "17:30 Sunset at Wat Arun". | Your plan, on their map. |
| 15.6-19.0 | `ideas` | Real Ideas screen, Krabi trip; ring on "Night kayak with the glowing plankton, 4 of 7 said yes". | Their ideas, put to a vote. |
| 19.0-22.4 | `assist` | Real group chat (Mai's pickup reminder) with the assistant's real reply lifted in front: "Assistant, from your trip plan: Pickup is at 07:30 from the Lantern Basecamp lobby..."; ring on the reply. | Answers from your trip plan. |
| 22.4-25.0 | `end` | 0.3 s crossfade to brand blue #2072B8: the peaks rise from the sea, the wave forms, the wordmark lifts, wanderbuddyapp.com/partners. | (end card) |

Every cut after 7.0 s sits on a downbeat of the bossa bed (140 BPM, 2 bars per beat).

## Sources (all real, nothing generated)

- `screens/app-documents.png`, `app-ideas.png`, `app-chat.png`: the app kit in `metrics/kit/screens/` (Krabi Islands, Small Group, Lantern Trips).
- `screens/plan.png`, `map.png`: `store/graphics/appstore/build/screens_v2/` (Flutter harness, real widgets). These two belong to the harness's own sample trip ("Bangkok Crew"); the camera frames the itinerary below the trip name. No Krabi plan or map screen exists on this Mac.
- `screens/assistant-reply.png`: a crop of `metrics/kit/screens/crm-inbox_assistant_pickup.png` (the traveller's question and the assistant's WhatsApp answer, no CRM chrome).
- `screens/mark-tile.svg`, `word.svg`: copied from `website/partials/brand-mark.html` and `brand-word.html`, imported into Blender as curves (not redrawn).
- `screens/shadow.png`, `grounds/*.png`: generated with ffmpeg (a soft shadow; the site's light page with its azure and teal washes, no amber; the panic's dark vignette).
- Audio: `marketing/music/` only. Piano notes (Iowa samples) for the panic pings, the collapse run, the logo chord, the ring taps and the end run; the Pixabay bossa bed from its own first downbeat at 7.0 s. See `audio/score.json`.
- Lantern Trips and its travellers (Sam Reed, Maya Reed, Ken Walsh...) are the invented sample agency. No stock clip is used.

## The traveller cut (9:16): `app-25s-travellers-9x16.mp4`

The same 25 s and the same cuts on the bossa downbeats, for Reels and TikTok, talking to travellers,
not agencies. No agency appears: every screen is the app's own sample friends' trip, Bangkok Crew
(`screens/dates.png`, `vote.png`, `reels.png`, `budget.png` from `screens_v2`). Lantern Trips'
listing is left out on purpose: in a traveller ad an invented agency's trip would read as bookable.

| Time | Shot | On screen | Headline |
|---|---|---|---|
| 0.0-7.0 | `panic` | 23:47, a phone buzzing with the Bangkok Crew group chat: "Maya: Which dates work for everyone?", "Priya: I paid for the boat. Who owes me?", "Leo: Scroll up, I sent it last week"... They fall back into the phone, which becomes the app icon. | Every group trip starts like *this.* |
| 7.0-8.7 | `logo` | The icon slides up into the lockup. | (lockup) |
| 8.7-12.1 | `dates` | Dates sheet lifts off the screen; ring on "Everyone is free 16 to 23 Oct". | Dates everyone can make. |
| 12.1-15.6 | `vote` | Proposed stops lift off; ring on "Muay Thai at Rajadamnern Stadium, Voted". | Vote on what to do. |
| 15.6-19.0 | `reels` | The saved reel "Bangkok street food you have to try, 3 places" lifts off. | Saved reels become places. |
| 19.0-22.4 | `budget` | The Settle up box lifts off. | Split costs, settle up. |
| 22.4-25.0 | `end` | Brand blue, the peaks, the wordmark, "Plan your trip together." and wanderbuddyapp.com. | (end card) |

The line is the codex's traveller line for while bookings are not live in the app ("Plan your trip
together"); nothing in the cut claims you can pay for a trip in the app.
Everything a viewer must read sits between 220 px from the top and 420 px from the bottom, clear of
the Reels and TikTok buttons and captions. Rebuild with `WB_TL=timeline_travellers.json` for the
shots and `python3 build/edit.py --tl timeline_travellers.json --render <frames dir>`; frames land in
`<frames dir>/trav_<shot>/`.

## Rebuild

Blender 5.3 (`/Applications/Blender.app`), Cycles on Metal. One heavy render at a time on this Mac: check `pgrep -fl Blender` first.

```
B=/Applications/Blender.app/Contents/MacOS/Blender
export WB_OUT=<frames dir>          # defaults to render/ here (large; not for git)
for s in panic panic_ov logo docs plan ideas assist end; do
  $B -b --factory-startup -P build/shots.py -- $s
done
python3 build/edit.py --render "$WB_OUT"
```

Stills for checking: `$B -b --factory-startup -P build/shots.py -- docs still 0 40 90`.
`WB_SAMPLES_SCALE=0.5` halves the samples for drafts.

- `build/timeline.json`: shot ranges, the panic's questions and spawn frames, each beat's screen, headline, phone pose and ring rectangle (fractions of the screen image).
- `build/wb.py`: scene, materials, the phone (after `store/graphics/appstore/build/pop/scene.py`), ring, text, SVG import.
- `build/shots.py`: one builder per shot.
- `build/edit.py`: the score and loudnorm, then the cut (grounds, overlays, concat, crossfade, x264 BT.709).
