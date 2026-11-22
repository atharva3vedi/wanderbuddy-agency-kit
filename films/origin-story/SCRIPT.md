# Origin story film: "Every company has an origin story"

How a GitHub repo became a US startup, as a 60-second reel plus a three-part series, with the
real CRM (Lantern Trips demo agency) and the real iPhone app.

v2 (27 Oct 2026), in `C:\Users\PC\Videos\WanderBuddy_Ad\origin-story\`:
- `WanderBuddy_origin_60s_v2.mp4` (16:9) and `WanderBuddy_origin_60s_v2_9x16.mp4`
- `WanderBuddy_origin_part1_v2*.mp4` the repo, `part2` the CRM, `part3` the app and the company.
  Each part opens on a "Part n of 3" chip; parts 1 and 2 close on a "Part n+1" card.

v1 (1:53, pitched-down Kokoro narrator) was rejected as too long with a bad voice. Its sources are in
`v1_src/` there.

## Narration (18 lines, `vo/lines.json`)

| # | Line | On screen |
|---|------|-----------|
| 0 | Every company has an origin story. | Serif title on ink |
| 1 | Ours started in June, with a GitHub repo. | Terminal: real first commit `e736bcc`, "Tue 23 June 2026, 02:49" |
| 2 | A travel app, built to look good on a résumé. | Résumé, "WanderBuddy, a travel app" highlighted |
| 3 | Play Store first. Then friends wanted it on iPhone. | Android listing, friends' bubbles, iPhone listing |
| 4 | The plan was to sell it. | App icon with a FOR SALE tag |
| 5 | But the builder couldn't let it go. | The string snaps, the tag falls. End of part 1 |
| 6 | Out there, small travel agencies were running dream trips on WhatsApp and spreadsheets. | Bangkok at night, agency pins, chats, payments_FINAL_v3.xlsx, notes, 02:13 |
| 7 | Nobody was building for them. | Freeze |
| 8 | So the app grew up. | Everything collapses into the icon |
| 9 | This is WanderBuddy, the travel CRM. | Logo, the CRM rises |
| 10 | Every enquiry, one inbox, answered even at two a.m. | Channels fire into the inbox, the 01:13 assistant reply |
| 11 | Every lead, from hello to paid. | Pipeline New to Paid, invoice in four currencies, PAID |
| 12 | Itineraries in minutes, in their own design. | Real Lantern Journal PDF pages, three colourways |
| 13 | And an AI that knows every trip. | Ask WanderBuddy answers "Who should I call today?". End of part 2 |
| 14 | Then the trip begins, and travellers carry it in their pocket. | QR scan, the iPhone joins, montage: itinerary, budget, documents, translate |
| 15 | Four months after the first commit, it's a US company, already earning revenue. | Timeline to Delaware C-corp and first revenue |
| 16 | Not bad for a side project. | Résumé line rewritten "Founder, WanderBuddy" |
| 17 | WanderBuddy. The travel CRM. | End card, wanderbuddyapp.com/partners |

TTS spellings: "Wander Buddy" and "rez-oo-may"; captions show "WanderBuddy" and "résumé".

## Voice

Groq `canopylabs/orpheus-v1-english`, voice `troy`, 4% faster (atempo 1.04), light EQ and
compression, no pitch shifting: `vo/orpheus.py troy orpheus`. Every line checked with Groq
whisper-large-v3. The model needed its terms accepted once on the Groq org that owns the key.

## Pipeline ($0, local)

- `capture.mjs`: Lantern Trips teaser screenshots (`CRM/lantern` via the `crm-mock` preview) at 2x.
- `composition.html` + `core.js` / `act1.js` / `act2.js` / `act3.js`: one seekable page; `?ar=9x16`
  vertical, `?part=1|2|3` part chip and closing card, `?cc=0` no captions.
- `audio.py`: synthesized score (D minor into F major at the reveal), synced sound design, ambience,
  ducked narration. `parts.py`: per-part audio with the narration cut at each part's end.
- `rebuild60.sh [voice folder] [tag]`: timeline, cues, score, the 60s reel and three parts in both
  formats, loudness -14 LUFS.
- Footage: Mixkit free licence (27770 Bangkok night, 6874 Krabi karst, 11046 longtails,
  46128 plane wing, 11302 floating market, 21237 beach, 9872 dusk sea).
