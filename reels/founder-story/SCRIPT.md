# Founder story reel: "The story of our founder"

A 9:16 reel in the format of Wabi's "The story of our CEO" (Instagram, Jan 2026): a narrator tells the
founder's story while the words appear one to three at a time over real photos, paper stickers on a
blueprint grid, and the product. Built 31 Oct 2026.

Project and output (off-repo, like the other ads): `C:\Users\PC\Videos\WanderBuddy_Ad\founder-story\`
- `WanderBuddy_founder_story.mp4`, 1080 x 1920, 30 fps, -14 LUFS.
- `bash rebuild.sh` rebuilds everything from `vo/lines.json` (about 12 minutes).

## Narration (14 lines, `vo/lines.json`)

Drafted by a Sonnet subagent (three takes), read cold by a Haiku subagent as a sceptical viewer, then
settled. Haiku's fixes: link the trip to the build, no "commit" jargon, no "CRM" or "earning revenue"
in the voice (the screen names the CRM).

| # | Line | On screen |
|---|------|-----------|
| 0 | Our founder, Atharva, once ended up running somebody else's trip. | Grid: magnifier over the founder (grant video still) |
| 1 | The night before a volcano hike, the organiser got completely drunk and crashed out. | Volcano at night; "Trip organiser" sticker swings off its nail, On duty to Offline |
| 2 | So Atharva, with no sleep and a bit drunk too, took over the whole group. | Name on the grid, founder photo, "0 hrs sleep" sticker; the group on a couch |
| 3 | Everybody kept asking. Where are we going? Who paid for what? Where are the tickets? | The group chat fills up |
| 4 | And that agency had no tech. Just WhatsApp and spreadsheets. | trip_payments_FINAL_v3.xlsx, 147 unread |
| 5 | Atharva started building the app that trip needed. | Founder at the desk |
| 6 | The first version went up on June 23rd, at 2:49 in the morning. | Terminal: real first commit e736bccb, Tue 23 Jun 2026 02:49 |
| 7 | It was meant to be a side project, something to put on a résumé. | Résumé, "WanderBuddy, a travel app" highlighted |
| 8 | Play Store first. Then friends wanted it on iPhone. | Stickers: Play Store June 2026, friends' asks, App Store August 2026 |
| 9 | The plan was to sell it. But Atharva couldn't let it go. | App icon with a FOR SALE tag that drops |
| 10 | Agencies like that one were still running trips on WhatsApp and spreadsheets, and nobody was building for them. | City at night, the spreadsheet again, black on "nobody" |
| 11 | So WanderBuddy grew up. One system that runs the agency, and an app the travellers carry. | Logo; the CRM (Travel CRM sticker); the app on a phone |
| 12 | Four months after that first version, it's a US company, already making money. | Stickers: 4 months, Delaware C-corp, First revenue |
| 13 | It all started with one bad night. This is WanderBuddy. | Founder at the waterfall, the volcano, end card |

TTS spellings: "rez-oo-may", "Wand-er Buddy", "U.S."; captions map back through each line's `cap`
(`_` folds a spoken word into the caption before it). Groq Orpheus is deterministic: the same text
gives the same take, so fix a bad read by changing the words. Free tier is 3,600 tokens a day.

## Screens (captured fresh on 31 Oct, never old screenshots)

- App: the store harness `store/graphics/appstore/build/flutter/store_screens_test.dart` (real widgets,
  fake Bangkok trip, dark theme). `home` fails since the 10-30 welcome route change; Plan is the hero.
- CRM: today's `CRM/app` as the Forest Retreat demo build (`node CRM/demo-kit/build.mjs forestretreat`),
  shot by `capture_crm.mjs` from disk. Forest Retreat is a real prospect, so the capture swaps in a
  made-up agency on the fly: Lantern Trips, Mai and Noi, teal palette, our own Mixkit stills for their
  photos. The pack on disk is untouched.

## Footage, photos, sound

- Founder: stills from `Videos\Wandabuddy bizzee grant application.mp4` and the waterfall clip in
  `Videos\Atharvafucking3vedi x WanderBuddy.mp4`.
- Footage: Mixkit free licence frames already extracted for the story promo and origin film (volcano, party, city).
- Sound: real recordings only. Bossa nova bed (Musicalmix2020, Pixabay licence) and Iowa MIS piano notes,
  both from the B2B reels, at the same levels.
