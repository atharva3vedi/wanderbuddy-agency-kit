# WanderBuddy — Product Hunt launch video

**Built.** `marketing/launch/ph-video/out/ph-launch.mp4` — 75.8s, 1920×1080, music bed,
no voiceover. Rebuild any time with:

```bash
cd marketing/launch/ph-video && node record.mjs && node build.mjs --speed 0.92
```

The footage is the interactive demo (`website/public/demo`, live at
wanderbuddyapp.com/demo), driven and screen-recorded by script rather than by
hand — see `ph-video/README.md` for how and for how to change it.

## Beat sheet, as shipped

Each beat holds a headline and one supporting line on the right of frame while the
phone plays the matching part of the story on the left.

| Time | Kicker | On the panel | On the phone |
|---|---|---|---|
| 0:00 | WANDERBUDDY | One app for the whole crew. | Your Trips — Bangkok Crew, Goa Reunion |
| 0:03 | BEFORE YOU GO | Your papers, offline. | Documents: passports, tickets, visa rules |
| 0:12 | ONE TRIP | The whole crew, one place. | Opening Bangkok Crew into the trip chat |
| 0:17 | DAY ONE | Everyone on one map. | Share live location, globe flies to Bangkok, crew converges on Wat Arun |
| 0:26 | THE PLAN | A plan you build together. | Propose a stop, 3 votes, it lands in the itinerary |
| 0:38 | THE MONEY | Nobody chases anybody. | Budget splits the morning, Settle with Leo |
| 0:42 | THE CREW | DMs and photos, in the trip. | Leo's DM, sending the morning's photos |
| 0:50 | 11PM, BANGKOK | An AI that knows your trip. | Ask WanderBuddy, pin the pick into tonight |
| 1:00 | THE ROOM | Talk to anyone, anywhere. | Talk to a Local, English ↔ Thai, both ways |
| 1:10 | — | (phone recentres) | End card: store QR codes, "free to join" |

The globe flying to Bangkok at 0:17 is the money shot. If you cut one clip for
social, cut that.

## Uploading it

Product Hunt's Video / Loom field takes a **YouTube or Loom URL**, not a file.

1. Upload `out/ph-launch.mp4` to YouTube as **Unlisted** (or Public — the launch
   is live either way).
2. Title it something a stranger would click: *WanderBuddy — one app for the whole
   trip*. Not "PH launch video".
3. Paste the URL into the Video / Loom field on the launch.
4. `out/poster.png` works as the YouTube thumbnail.

## If you want a voice on it

The video is captioned and works on mute, which is how most Product Hunt embeds
get watched. If you'd rather narrate it, the beat times above are the cue sheet:

> 0:00 — "My phone got stolen in Bangkok. This app is how I got the trip back."
> 0:03 — "Everything for the trip lives here. Papers first, and they work offline."
> 0:17 — "Share your location and the whole crew is on one map, heading to one place."
> 0:26 — "The plan gets built together. Anyone proposes, the group votes."
> 0:38 — "And nobody chases anybody for money. It just splits."
> 0:50 — "There's a travel AI that's actually read your trip."
> 1:00 — "And you can hand your phone to anyone. You speak yours, they hear theirs."
> 1:10 — "WanderBuddy. One app for the whole crew."

Then `node build.mjs --speed 0.92 --vo yourtake.wav`.

Record it yourself. The opening line is a true story about you, and a synthetic
voice telling it is worse than no voice at all.

## Notes

- Don't say "upvote" anywhere. Ask for feedback.
- The demo is a faithful reconstruction of the app, not a build of it. If the app's
  UI moves, update the demo first and the video follows on the next run.
