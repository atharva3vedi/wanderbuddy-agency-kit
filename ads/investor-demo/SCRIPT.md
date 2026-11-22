# Investor product demo: "One app, both ways to run a trip"

16:9, 1920 x 1080, 24 fps, 119 s. Captions and the bossa nova bed, no voiceover.
For investors: one film that shows both halves of the product, with real screens only.

- **B2C, a friend runs the trip:** a friend rallies a group in the app. Dates everyone can make,
  a vote on what to do, a reel DM'd to our Instagram that becomes places, split costs, a live
  map. No agency anywhere.
- **B2B, an agency runs the trip:** the app is an add-on to every trip an agency sells. The agency
  lists its trip, a traveller holds it, the agency's CRM and assistant run it, and the traveller's
  app carries the plan.

The deck's line for it (docs/redesign/proposals/05_DECK_REVIEW_JG.md): one product, two kinds of
organizer, not a B2C-to-B2B pivot story. The film is built that way: act 1 is the friend, act 2
is the agency, and the same app is on the phone in both.

## The picture

A paper map of Southeast Asia lies on a table. The agency's laptop sits on Krabi. The
traveller's phone sits on Singapore. In act 1 only the phone is awake. In act 2 the laptop
opens and one real trip, Lantern Trips' "Krabi Islands, small group", travels between the two
along an azure arc: the listing goes out, the hold comes back, the plan goes out, a midnight
question comes back and is answered. Every hop lands as a real WanderBuddy screen on the
receiving device. At the end the camera rises over the map and the business model is three lines.

It folds in the work of the past sessions (what is live as of 2026-11-12):

| Session work | Where it shows |
|---|---|
| The friend-group app: dates, votes, split costs, live location (the original product) | Act 1 |
| Reels DM'd to our Instagram (@wanderbuddyapp) become places | Act 1, the Instagram beats |
| The app as an add-on for agencies (the CRM's WanderBuddy page) | The hand-off |
| Free listing, Listings as trip cards (11-09, 11-10) | Act 2, listing |
| Marketplace /trips (11-11) | Act 2, the traveller finds it |
| Booking fee at hold, agencies paid their own way (11-11, switched on) | Act 2, the one ring |
| Holds into the agency's inbox (11-09) | Act 2, the hold |
| CRM itinerary maker and the PDF pages (the "Order" film) | Act 2, the plan |
| Traveller app 2.0: home, documents, group chat (store builds) | Act 2, her phone |
| WhatsApp assistant answering from the trip plan (the "23:48" film) | Act 2, 23:47 |
| The marketplace model: agencies list, travellers book, WanderBuddy takes a fee | The closing lines |

Not shown, on purpose: the ask-first CRM home (not deployed), card deposits and the team
Business app (parked), any traction number (the deck carries those), Raasta Theory or any real
agency's data.

## The two trips

- **Act 1, friends:** the app's own sample friends' trip, Bangkok Crew (Maya, Leo, Priya and
  the phone's owner, Sam). Dates 16 to 23 Oct, "Muay Thai at Rajadamnern Stadium" voted, the
  saved reel "Bangkok street food you have to try", Maya pays Priya 445 THB, the live location
  rows for Maya, Leo and Priya. From the app's own harness screens (`../app-25s/screens`, and
  `iceland/live_composited.png` for the live map: its map behind the rows is the harness's
  Iceland sample, the rows are the same three friends).
- **Act 2, agency:** Lantern Trips (the sample agency of the public /trydemo), "Krabi Islands,
  small group", US$690 a person. Hana and Petr Novak hold 2 spots on the 9 Dec departure,
  +420 603 118 274, note "Can we add a night on Railay after the trip?". The phone's hold form
  and the CRM's hold card show the same people, dates, number and note. The 3% fee rows
  (US$1,380, US$41.40, US$1,338.60) are what the live /trips page draws for a fee listing.

Two different people on one phone is deliberate and normal: you plan October's trip with your
friends and book December's with an agency, in the same app.

## How a reel reaches the app (the Instagram beats)

This is the real flow (supabase/functions/instagram-webhook, the app's Connect Instagram screen):
the app gives a one-time code, the traveller DMs it to our account **@wanderbuddyapp**, then DMs it
any reel. The bot's two replies on screen are the real ones: "Got it ✨ reading your reel now, I'll
message you what I find in a moment." (`insp_saving`) and "Nice find ✨ {place}: {places}. I'll use
these when you plan. Open WanderBuddy: {link}" (`insp_enriched`). The DM thread itself is plain set
dressing (a neutral chat, our logo as the avatar), not Instagram's look; the three Bangkok places
in it (Yaowarat Road, Thip Samai, Jay Fai) are sample content for the app's sample reel.

## Beats (as built)

One WbSans line at a time on the left third, no labels above it. A small pill stays in the
corner: "Sample trip, real product screens" in act 1, "Sample agency, real product screens" in act 2.

| # | Time | Picture | On screen |
|---|---|---|---|
| 1 | 0 to 7 | Top-down over the paper map at late light, then down to the table: a closed laptop on Krabi, a dark phone on a stand on Singapore, her passport and boarding pass beside it. | "Every group trip in Asia has someone running it." "Sometimes a friend. Sometimes an agency." |
| 2 | 7 to 10 | The camera pushes in on the phone, which wakes on the group chat's lock screen (Maya: Which dates work for everyone? Leo: Where was the street food place. Priya: I paid for the boat. Who owes me?). | The WanderBuddy lockup. "One app for both." |
| 3 | 10 to 19 | **A friend runs the trip.** Two real screens lift off the phone: the Dates sheet ("Everyone is free 16 to 23 Oct") and the vote on proposed stops. | "A friend rallies the group. WanderBuddy finds the dates everyone can make." "They vote on what to do." |
| 4 | 19 to 27 | The app's Connect Instagram screen lifts its steps (get a one-time code, send it in a DM to our Instagram, DM a reel, get the places in it). Then the DM thread: the friend's reel, "Got it ✨ reading your reel now...", "Nice find ✨ Bangkok: Yaowarat Road, Thip Samai, Jay Fai." | "To save a reel, they DM it to our Instagram, @wanderbuddyapp." "WanderBuddy reads it and replies with the places it found." |
| 5 | 27 to 40 | Back in the app: the saved reel with its 3 places, the Settle up box, then Live location (Maya, Leo and Priya on one map). The phone goes dark and the camera pulls back. | "Saved reels become places on the plan." "The costs get split and settled, so nobody has to chase." "On the trip, everyone is on one live map." |
| 6 | 40 to 44 | The laptop on Krabi opens on the CRM's **WanderBuddy** page, the app as an add-on (Live trips, Travellers joined, Answered for you), which lifts off the screen. | "For agencies, the app is an add-on to every trip they sell." |
| 7 | 44 to 53 | **An agency runs the trip.** Push in to the laptop: the CRM's Listings. The Krabi Islands card (US$690, Listed, 3 holds) lifts off the screen. Back to the wide: the arc rises from the laptop to the phone. | "Lantern Trips lists its Krabi trip on WanderBuddy. Free." |
| 8 | 53 to 62 | The phone: the live /trips page for that trip scrolls to the filled hold form. The fee rows lift off and **the one azure ring** lands on them. | "A traveller in Singapore finds it on WanderBuddy." then "She holds two spots. We take 3% now. The agency gets the rest, paid its own way." |
| 9 | 62 to 71 | A dot runs back along the arc. The laptop: the hold in the CRM inbox; the card "Hold: Krabi Islands, small group" lifts off. | "The hold lands in Lantern's inbox, with her WhatsApp number." |
| 10 | 71 to 80 | The laptop shows the itinerary maker; six real pages of the Krabi plan deal out onto the map. A dot runs to the phone. | "Lantern's AIRM, an AI relationship manager, turns the chat into the plan." then "One plan: a PDF, a page, and the trip in her app." |
| 11 | 80 to 91 | The phone: the app's home, Documents, the group chat; Mai's 07:30 pickup reminder lifts off. | "Every traveller gets the WanderBuddy app with the trip." then "Plan, vouchers and the group chat, in one place." |
| 12 | 91 to 103 | Night falls on the map; one lamp. The phone at 23:47; a dot runs to the laptop; the CRM inbox shows "What time is pickup tomorrow?" and the assistant's reply, which lifts, flies along the arc and lands on her lock screen at 23:48. | "23:47. A traveller asks what time pickup is." then "Lantern's WhatsApp assistant answers from the trip plan. Nobody there has to wake up." |
| 13 | 103 to 112 | Morning comes back; the camera rises over the map, both devices and the arc between them. | "How WanderBuddy earns". Travellers: "Find and run trips, free." Agencies: "List free. Pay for the AIRM." WanderBuddy: "3% of every booking we bring." |
| 14 | 112 to 119 | Brand blue end card. | The lockup. "One app. *Both* ways to run a trip." wanderbuddyapp.com, "Live on iOS, Android and the web." |

## Sound

The reels' own bossa nova recording (Pixabay "Bossa Nova Summer", human-made) from about 56 s of
the track, its fullest stretch, with a downbeat on the laptop opening at 40.25 s. For 23:47 the bed
drops 8 dB and goes muffled, as if through a wall, with a clock ticking; it comes back full for the
morning and fades under the end card. Real Iowa Steinway notes in G sit about 5 dB under it: the
phone waking, each card that lifts, each hop of the arc, the ring, the 23:48 answer, the model
lines, then the end card's notes.

## Rules this follows

Brand Codex Rev 03: WbSans, one Instrument Serif italic word (*Both*), one azure ring,
light-first palette (#F3F6F9 ground, #0C1622 ink, #1E88D6 azure), no yellow in our own UI, no
em dashes, no "!", no "AI-powered". Real screens only: the friends' act uses the app's own
sample trip (Bangkok Crew), the CRM is the public Lantern Trips sample demo, the marketplace is
the live /trips page answered with that demo's sample trip, the rest of the app screens are the
2.0 kit. The lock screens, the Instagram DM thread and the boarding pass are plain set dressing
drawn in Chrome, not product UI. The demo's Krabi itinerary has only two photos set, so its empty
photo slots (hatched in the editor, grey circles in the PDF) are filled with crops of those same
two photos, as it looks once an agency adds its own.

## Open choices for the founder

- The 3% is what the live hold form shows today (0227, switched on 11-11). Booking site plan
  item B0.1 (the fee agencies see) is still open; if it changes, the fee card would be retaken
  and the model line edited (overlay only).
- "AIRM, an AI relationship manager": your word; the expansion is my reading of it.
- "The app is an add-on to every trip they sell" is my reading of "signify the app as an add-on":
  the CRM's WanderBuddy page ("the trip app and WhatsApp assistant your travellers get from you")
  is the screen that shows it. If you meant the app as a paid add-on to the CRM, the caption and
  the model line change (overlay only).
- The live-map screen's map is the harness's Iceland sample under the Bangkok Crew rows. It is
  only legible as blur in the film, but it is not a Bangkok map.
- The three places in the DM reply are sample content, not output of the real bot for that reel.
- The end line changed from "One trip. Both sides." to "One app. Both ways to run a trip."
  because the film now has two trips.
- No voiceover. Hannah could read it later with the b2b-reels recipe.
- No traction numbers in the film, so it never goes stale; the deck carries them.
- The first cut (agency only, 86 s) is kept as `out/wanderbuddy-investor-demo_agency-only.mp4`.
