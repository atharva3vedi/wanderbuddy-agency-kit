# WanderBuddy story promo (16:9, 51.8 s)

Videos in `C:\Users\PC\Videos\WanderBuddy_Ad\story-promo\` (project files live next to them, off-repo):
- `WanderBuddy_story_promo_v1.mp4` 16:9, 1920x1080
- `WanderBuddy_story_promo_v1_9x16.mp4` 9:16, 1080x1920 (same timeline, own layout: `composition.html?ar=9x16`)
- `*_share.mp4` are smaller copies that fit the phone upload limit

All are 30 fps and -14 LUFS, with the Kokoro guide voice until the founder's takes replace it.

## Voiceover (version used: the volcano story)

Chill, first person, present tense. Place is not named, so the story stays true (it was Bali)
while every app screen shows a Thailand trip.

| Time | Line | On screen |
|---|---|---|
| 0.5 | So I'm on a group trip, and we're going up a volcano. | Volcano at night, phone lock screen 2:47, three notifications, "Group trip. Zero plan." |
| 4.0 | And the guy running the whole trip... crashes out. | "The trip lead / crashed out." His card wobbles, goes Offline |
| 6.9 | Gets completely wasted. | Card slumps |
| 8.7 | So now, it's on me. | Trip lead badge slides over to "You". "Now it's on me." |
| 10.6 | No sleep. Bit drunk myself. | Typed top line |
| 12.7 | And everyone's asking me where we're going, who paid for what, where the tickets are. | Ten chat bubbles orbit "You", each with a ukulele or vibraphone ping |
| 18.2 | I figured the travel agency would have the tech sorted. | "The agency has the tech sorted. Right?" Agency card spinning |
| 21.7 | Nope. | Red "Nope." stamp, sad-trombone wah |
| 23.0 | That's when I thought, okay. This should be one app. | "One app." letters slide together |
| 26.1 | So I built it. | Bass hit, "So I built it." |
| 28.0 | Tickets and passports, in one place. | Documents: 8 files fly into the phone |
| 31.8 | The plan, day by day, for everyone. | Itinerary: Day 2 Krabi, Phi Phi, Maya Bay, Ao Nang |
| 34.8 | Who owes who, sorted. | Budget in baht, "All settled" |
| 37.8 | Everyone's clips, one reel. | Reels grid, "Trip reel ready" |
| 40.8 | And a chat that translates, for the whole group. | Thai and Spanish messages translated |
| 43.9 | Big group, or just you. | Ten avatars, then one |
| 46.1 | This is WanderBuddy. | Logo + wordmark |
| 47.6 | It's live. Link in bio. | It's live, iPhone + Android buttons, LINK IN BIO |

## Alternate voiceover (the Reddit concert story), not produced yet

So I found ten strangers on Reddit, and we decided to go to a concert together.
Ten people who'd never met. Planning it was a mess.
Who's booking what. Who paid. Where we're staying. What time we're meeting.
I kept thinking, this should be way simpler. So I built it.
Tickets and passports, in one place. The plan, day by day, for everyone.
Who owes who, sorted. Everyone's clips, one reel.
And a chat that translates, for the whole group.
Ten strangers. Or just you. This is WanderBuddy. It's live. Link in bio.

## Check before posting

- Lines I wrote around your story: "who paid for what, where the tickets are", the lock screen
  (2:47, 52 new messages, 9% battery). Swap anything that did not happen.
- The voice is a local text-to-speech guide track (Kokoro am_michael). It is your story, so your own
  voice will land better. Record the 18 lines and the whole video re-times to your takes.
- Group translation in 2.0 is still an open check from the launch reels doc.
- 51.8 s, not 43 s: the story needs the room. A 43 s cut drops "Big group, or just you" and
  shortens the feature beats.

## Sound

Jazz lounge bed at 80 bpm (Rhodes ii-V-I-vi, upright bass, brushes), ukulele strums join under the
features. Notifications are ukulele strums and vibraphone chords; the badge hand-off is a Hawaiian
steel-guitar slide. Crickets under the volcano, birdsong and breeze under the features, ocean on the
end card. Everything is synthesized in `audio.py`, so there is nothing to license.

## Footage

Mixkit free licence (commercial use, no credit): 4428 volcano, 46878 party couch, 46128 plane wing,
6874 Krabi karst, 11197 floating market, 21237 beach sunset, 27770 Bangkok night, 9872 dusk sea.
Pexels now blocks scripted downloads.

## Founder takes

Record each line as its own file named by its number (1.m4a ... 18.m4a, any format). The numbered
list is in `vo/takes_in/LINES_TO_RECORD.txt`. Drop the files in `vo/takes_in/`, then run
`python vo/prep_takes.py vo/takes_in` (cleans, numbers, 48 kHz) and `bash rebuild.sh founder v2`
(re-times both formats to the takes, rebuilds the sound, renders and muxes 16:9 + 9:16 + share copies).

## Rebuild

From `C:\Users\PC\Videos\WanderBuddy_Ad\story-promo`:
1. `vo/lines.json` holds the lines; `vo/tts.py am_michael 1.0 michael10` voices them
   (python = `~/.cache/hyperframes/tts/venv`), `vo/build_timeline.py` lays them out and writes `timeline.js`.
2. `node render.mjs --sfx` then `node render.mjs --out video_silent.mp4` (add `--ar 9x16` for vertical).
3. `audio.py` builds `audio/mix.wav`; mux with two-pass loudnorm to -14 LUFS.
