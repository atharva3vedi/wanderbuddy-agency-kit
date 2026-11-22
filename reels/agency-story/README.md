# How we got to revenue (agency story reel)

A 71-second Instagram reel (1080x1920, 30 fps, -14 LUFS, captions burned in) on why WanderBuddy went
to travel agencies and how that got us to revenue. Format taken from an editlobby founder reel
(instagram.com/reel/DYhkDnDBzKW): a hook in the first second, word-by-word captions, handwritten
accent words with a drawn stroke, cut-in cards, a black-and-white beat on the hard truth, a
three-panel strip. Built 2026-10-31, $0 spent.

- `out/WanderBuddy_HowWeGotToRevenue.mp4` (full quality) and `_share.mp4` (smaller, for phones)

## Script (Troy, Groq Orpheus)

| # | Line | On screen |
|---|------|-----------|
| 0 | Four months after we started building, WanderBuddy was making money. | Waterfall selfie, "Four months to *revenue*" from frame 0 |
| 1 | Just not from the app we set out to make. | The app in a phone, "the app" crossed out |
| 2 | In June, we started on a group travel app. | Polaroid of Atharva on the couch with the laptop |
| 3 | It all began on one trip. | Bikes on a mountain road, "*one trip*" |
| 4 | The night before a volcano hike, the trip leader got so drunk that we ended up running the group ourselves. | Pixel volcano under stars, a red-lit crowd, the ride |
| 5 | And the travel agency behind that trip had no tech at all. | "The agency's tech": three empty boxes, "*none.*" |
| 6 | By August, the app was live on both app stores. | The real app in a phone, Google Play and App Store chips |
| 7 | But most people only travel two or three times a year. | 52 weeks, three light up |
| 8 | An app you open twice a year is a hard business to make work. | Black-and-white helmet shot, "*twice a year*", music dips |
| 9 | Travel agencies, though, run trips every single week. | All 52 weeks fill, "*an agency's year*" |
| 10 | And the small ones run all of it on WhatsApp, spreadsheets and invoices made in Word. | Chats, DMs, payments_FINAL_v3.xlsx, invoice_final2.docx |
| 11 | So we went narrow, and built them a CRM. | The mess collapses into one line, "*narrow*", the CRM opens |
| 12 | Every WhatsApp and Instagram message lands in one inbox. | The inbox, WhatsApp and Instagram chips |
| 13 | They get itineraries in their own design, plus invoices and payment plans. | Lantern itinerary pages, Invoices and Payment plans chips |
| 14 | Then an agency started paying us for it. | Waterfall laugh, "Payment received" notification, "*first revenue*" |
| 15 | And every trip they run brings more travellers into our app. | Boat, dunes, lake in three panels, travellers fly into the app |
| 16 | Run a travel agency on WhatsApp and Word? | The ride, the question as one headline |
| 17 | See what we built at wanderbuddyapp.com/partners. | Blue end card, logo, URL |

Copy went through a Sonnet draft (three takes) and a cold Haiku review as a sceptical viewer.
Claims kept to what is true and already public: June start, both stores by August, the volcano
night, first agency paying. No prices, no client names, no India. The CRM shots are the public
Lantern Trips demo, never a real agency's workspace. The payment notification is an illustration
with no amount.

TTS spellings: "WanderBuddy" (no hyphen) and "wanderbuddyapp dot com, slash partners" read clean in
Whisper; "C R M". Same text gives the same Orpheus take, so reword to re-roll a line.

## Footage (ours) and sound

Clips from `E:\Phone big gb stuff` and `E:\Content\Meta glasses`, listed by path in `build/edl.json`.
Music: "Bossa Nova - Summer - Instrumental Brazil" by Musicalmix2020 (Pixabay Content License).
Piano: University of Iowa Musical Instrument Samples (free for any use). Both copied from
`WanderBuddy_Ad/b2b-reels/assets`.

## Rebuild

```bash
cd build
bash build.sh                 # cut footage, render, mix, loudness (about 15 min)
SKIP_CUT=1 bash build.sh      # when only the page or the sound changed
```

- `edl.json` = the shot list (clip, in-point, zoom, box). `python cut.py hook,tri` re-cuts those shots
  and rewrites `edl.js`, which the page reads.
- `reel.html` = every card, caption and accent word, a function of time. `node render.mjs --stills 12,30`
  writes check frames to `stills/`.
- Change a line: edit `vo/s1/lines.json`, `python vo.py s1 <i>`, `python timeline.py s1`,
  `python words.py s1`, `python captions.py s1`, then fix shot times in `edl.json` if lines moved.
  Use the hyperframes venv python (`~/.cache/hyperframes/tts/venv/Scripts/python -I`).
- Founder's own voice: record the 18 lines, drop them in `vo/s1/founder/l00.wav`..`l17.wav`, set
  `"folder": "founder"` in lines.json, then timeline, words, captions and build.

Run one render at a time.
