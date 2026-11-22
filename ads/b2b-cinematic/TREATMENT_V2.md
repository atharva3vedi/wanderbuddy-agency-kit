# Agency films, second pass (2026-11-11: film 1 built as the pilot, the rest proposed)

The founder's note on the first four: liked 2, 3 and 4, not 1 (Departures). All four felt
simple, generic and scored with the same music. Wanted: cinematic, a real script, settings
with character, the chaos being sorted, fear of missing out ("others have already begun"),
and a clear sense that WanderBuddy handles their sales and their software, without a feature
list. Plain enough for an agency owner anywhere in Asia to get on a muted phone.

## What changes

| First pass | Second pass |
|---|---|
| One picture, then three captions | A small story with a turn: something is at stake, and somebody wins it |
| Pictures borrowed from Western art (Hopper, knolling, Solari) | Places an owner in Krabi, Hanoi, Kathmandu or Jaipur knows: a shophouse street in rain, a ceiling-fan office in peak season, a flat at night, a pier at blue hour |
| The same bossa bed on all four | One track per film, each with its own instruments, plus real recorded sound (rain, fan, boat engine, a phone buzzing on wood) |
| The message is in the captions | The information is in the picture: clocks, unread counts, seat counts, real chips from the CRM. Captions stay short |
| No fear of missing out | Each film has a loser as well as a winner. The loser is the agency that did nothing |
| 24.7 s | About 30 s, so each line stays up 2.5 s or longer |

Captions: seven words or fewer, a number or a time wherever possible, no idioms, one
serif-italic word per film. Every screen is still a real capture of Lantern Trips.

## Five films, five countries

The founder's second note: the first pass was all Krabi. Each film now has its own country,
and Thailand appears once (Day 2, which is kept).

| Film | Country | Setting | Trip on screen |
|---|---|---|---|
| Three Agencies (now the free-listing film) | Vietnam | A tube-house street in Hanoi's Old Quarter, in rain | The Ha Giang Loop |
| Monsoon | Many | One office; the storm and the pipeline carry Angkor, Luang Prabang, Penang, Komodo and Sapa | Five trips in five countries |
| Opened 3 Times | Indonesia | A block of flats in a big city (the traveller), an agency office below | Komodo by phinisi |
| Empty Seats | Philippines | A pier in El Nido, a bangka with twelve seat lanterns | El Nido lagoons |
| Day 2 | Thailand | Kept as rendered | Krabi Islands |

These trips are real: Ha Giang, Komodo, El Nido, Siem Reap, Luang Prabang, Penang and Sapa are all
among the 20 trips seeded into the app on 11-11 (migrations 0224 and 0225), with their own cover photos.
The CRM demo today only holds Krabi, so the CRM screens need a capture-only copy of the Lantern Trips
sample with these departures added. That copy is used for screenshots and never deployed.

South Asia is not in the set, because every trip we have photos for is in South-East Asia. If India
or Nepal should be in, Monsoon is the film to move (a hill-station office, a Ladakh or Kerala trip).

## The films

### 1. Three Agencies (the free listing). Replaces Departures and 23:48. BUILT, second cut.

A rainy street of three travel agencies in Hanoi's Old Quarter, 23:47. Two behind roll shutters under
lit signboards ("DU LỊCH · TOURS", "TRAVEL & TOURS", no agency names), Lantern Trips behind glass with
one warm lantern over its door.

The founder's call after the first cut: go back to the first pitch (one traveller, three agencies),
with one clear winner and how it won by using WanderBuddy. Nothing in the product answers a new
enquiry by itself (`supabase/functions/whatsapp-webhook/agency.ts`: a message to an agency's number
"goes into that agency's CRM inbox"; the assistant only answers travellers on a live trip). What does
work at 23:47 with nobody there is the listing: dates, seats left, price, and Hold my spot, which
lands in the agency's inbox. So that is how the winner wins.

| Time | Picture | Words |
|---|---|---|
| 0 to 3.5 s | The street in rain, three signs, the lantern. | 23:47. One traveller. Three agencies. All closed. |
| 3.5 to 8 s | Along the shopfronts. A phone lights up behind each of two shutters and goes dark. Lantern Trips is dark too. | She messages two. Nobody answers. |
| 8 to 14.5 s | Her phone on a hostel bunk: the real /trips listing, Ha Giang Loop, Lantern Trips, 16 Nov, 3 seats left, US$390. Then the hold form: 2 people, free. Azure ring on Hold my spot, and the tap. | The third is on WanderBuddy. Dates. Seats. Price. She holds two spots. |
| 14.5 to 19.5 s | The dark office. The laptop wakes on the real inbox: "Held a spot on WanderBuddy. Held 2 spots on Ha Giang Loop, small group, 16 Nov 2026", 23:49. Azure ring. | Lantern Trips is asleep. Its seats are *held.* |
| 19.5 to 23.5 s | The phone on the desk next door: her question at 23:47, then at 09:06 "Thanks, but we already booked with Lantern Trips." | 09:02. The others reply. Too late. |
| 23.5 to 29 s | The street at dawn. Two shutters go up. The lantern is still lit and the azure ring lands on the Lantern Trips sign. | Three were closed. One was on WanderBuddy. |

End card: "List your trips on WanderBuddy, free." 32.3 s in all. File: `out/v3-three-agencies.mp4`.

Real: the listing is the live /trips page drawing a Lantern Trips sample departure, and the inbox is
the public demo's CRM with that trip in its sample data (`build/agencies_capture2.mjs`). The hold form
is filled in with sample details and never sent. Set dressing: the lock screen next door
(`build/agencies_stills2.mjs`). The listing's cover is the app's own Ha Giang photo (Khánh Hmoong,
CC BY 2.0, credited on the page).

Sound: an original score generated in `build/agencies2_audio.py` on the founder's say-so ("you can
generate your own music"): synthesized strings, pulse, rain and two low hits under the real piano notes.

The first cut (`out/v2-three-agencies.mp4`, the assistant answering a pickup question) is kept for reference.

### 2. Monsoon (the whole desk in one place). Replaces Order. BUILT.

The same street. Next door to Lantern Trips, an agency doing peak season by hand.

| Time | Picture | Words |
|---|---|---|
| 0 to 3.5 s | The phone on the desk next door: 12 unread, 47, 113. | Peak season. |
| 3.5 to 10.5 s | The office under a ceiling fan. Passport copies, payment screenshots, rate sheets, old PDFs, chat printouts and sticky notes lift off the desk and whirl. | WhatsApp. Instagram. Excel. Canva. A bank app. Five apps. One booking. |
| 10.5 to 13.5 s | The fan stops. It all comes down, and one passport copy slides off the desk onto the floor: "which trip??" | Something always gets lost. |
| 13.5 to 21.5 s | Lantern Trips. The real pipeline board, five countries of trips in lanes, the ring on one card (Erik, quote v2, follow up today). Then Home's "Needs you today": "Erik picked Option B and tapped Book. Send the deposit link: 30% is $672." | Next door, the same messages. Each one in its *place.* And what to do next. |
| 21.5 to 27.2 s | The street at 23:30, in rain. One shop still lit behind its shutter. The azure ring lands on the Lantern Trips sign. | 23:30. One is still sorting. One runs on WanderBuddy. |

End card: "You run the trips. WanderBuddy runs the rest." 30.7 s. File: `out/v2-monsoon.mp4`.
Real: the board and Home are the demo CRM with its sample enquiries spread over five trips
(`build/monsoon_capture.mjs`). Set dressing: the phone and every sheet of paper (`build/monsoon_stills.mjs`).
Score: generated (`build/monsoon_audio.py`): a fan, hand drums that speed up, a dead stop, quiet strings.

### 3. Opened 3 Times (the follow-up: who does my sales). BUILT.

| Time | Picture | Words |
|---|---|---|
| 0 to 3 s | Her phone on a sofa, Monday 20:14: two notifications, a quotation PDF from Travel & Tours and a plan from Lantern Trips. | Monday. Two agencies quote her for Komodo. |
| 3 to 10 s | She opens the Lantern Trips plan. The screen sleeps. She opens it again. And again. | She opens one plan. Then again. And again. |
| 10 to 17.5 s | Lantern Trips, at night. Home in the real CRM: "Lukas & Sophie Brooks. Opened quote v2 3 times since yesterday. Call while it is fresh", ringed. Then the board: their card under Booked. | Lantern Trips can see it. So they *call.* Booked the same night. |
| 17.5 to 21.5 s | The phone next door, Tuesday 09:00, Wednesday 09:00: "No new messages". | The other agency is still waiting for her reply. |
| 21.5 to 27 s | The street at dawn, the ring on the Lantern Trips sign. | Two quotes. One follow-up. One runs on WanderBuddy. |

End card: "You run the trips. WanderBuddy runs the rest." 30.3 s. File: `out/v2-opened-3-times.mp4`.
Real: Home and the board are the demo CRM with one sample couple's quote opened three times; the
"hot quote" row follows the CRM's own rule (`CRM/app/router.js`: a sent quote opened twice or more in
three days). The plan she opens is the cover from the demo's itinerary maker, with the trip's name and
the app's own Komodo photo put in (`build/opened_capture.mjs`, `build/opened_stills.mjs`).
Not in the film: Broadcasts. In the demo its sample travellers have no phone numbers, so the screen
reads "Nobody here has a phone number".
Score: generated (`build/opened_audio.py`): a heartbeat, strings in A minor to C major, a ringing tone on the call.

### 4. Empty Seats (the free listing). NOT BUILT.

Three Agencies became the free-listing film, so this one would repeat it. Left as a script only:
a 12-seat boat at a pier in El Nido, nine lanterns lit, the last three filled from the listing.

### 5. Day 2 (the trip app). RE-SCORED.

Same picture and words as the first pass. New file `out/v2-day2.mp4` with its own generated score
(`build/day2_audio_v2.py`): plucked strings in G pentatonic over a low drone, no bossa bed.

## Closing line on every end card

"You run the trips. WanderBuddy runs the rest." above wanderbuddyapp.com/partners.

## What each film proves is real (checked in the code today)

- Opened 3 Times: the pipeline chip "Opened 3x" (`CRM/app/screens/pipeline.js`), the Home card "Opened quote v2 3 times since yesterday. Call while it is fresh" (`screens/home.js`), and Broadcasts with its "New trips" message (`screens/broadcast.js`).
- Monsoon: the pipeline stages New, Qualified, Quote sent, Booked, and the Tasks empty state quoted above (`screens/tasks.js`).
- Empty Seats: the /trips listing page, captured again with the El Nido departure (the first pass used the Krabi one).
- Three Agencies: settled. The assistant answers travellers on a live trip only, so the film was rewritten around the pickup question (see film 1).

## Where this bends the current rules (each needs the founder's yes)

1. Music. The codex allows only the bossa bed and the Steinway notes. This proposal uses one licensed, human-made track per film from Pixabay (same licence as the bossa, none registered with Content ID). I cannot judge music by ear, so I would shortlist three per film and the founder picks. Downloading them needs a yes.
2. Warm light. The first pass banned yellow and amber light. A night street with no warm light looks sterile, so film 1 gets one warm lantern and film 4 warm seat lanterns against the blue. Yellow stays out of every screen.
3. Fear of missing out. The codex bans promised results and scale we do not have. These scripts name no number of agencies and promise no bookings. The pressure comes from the traveller: she asks three agencies, and one of them answers.
4. "WanderBuddy runs the rest" is a bigger claim than the codex's "one job per sentence".

## Questions, with the default I would take

1. Does the assistant answer a new enquiry (dates, seats left, price) today, or only travellers already on a trip? Default: if only the second, film 1 keeps the same street and clock, but the traveller is on the trip and the loser is the agency whose traveller waited till morning.
2. Voice. Default: none. The films are read muted; sound and picture carry them.
3. Order of work. Default: build Three Agencies alone first as the pilot (about half a day to build, 45 minutes to render), show it, then build the rest in the same style.
4. Old films. Default: keep the four first-pass files in `out/` untouched; the new ones get new names.

## Film 6: The Reel (the itinerary maker and the assistant). BUILT.

The founder's ask (2026-11-12): one film that shows how good the itinerary PDF maker is, and that the
AI does more than hold seats: it answers their queries and gets them to close.

What the product really does at each step (checked in the code), and so what the film shows:

- **A reel becomes a plan.** `CRM/app/proposal.js`: a traveller sends a reel or a link; one press ("Turn
  into a proposal") reads it, makes the enquiry, prices the quote from the agency's past trips, drafts the
  day by day and lays it out in the agency's design. The agent checks it and presses Send; nothing is sent
  on its own.
- **It tells you the moment they say yes.** On the itinerary link the traveller picks an option and taps
  Book; Home says "picked Option B and tapped Book. Send the deposit link: 30% is ...".
- **It answers on the trip, by itself.** The assistant answers travellers on a live trip from the trip plan.

The film does not show the AI closing a sale alone. It shows the work around the sale being done, and the
agent pressing one button and then Send.

| Time | Picture | Words |
|---|---|---|
| 0 to 4 s | Her phone on a bunk at 23:40: a reel of the Ha Giang loop and her message to Lantern Trips. | 23:40. A reel, and one question. |
| 4 to 6.5 s | The laptop: the real conversation, the reel strip above the reply box, the ring on "Turn into a proposal". | You press one button. |
| 6.5 to 10 s | The real panel: reading the reel, pricing from past trips, making the enquiry, drafting the day by day, laying it out. Then the result (trip, price, plan), ringed. | It reads the reel, prices it, and writes the plan. |
| 10 to 18 s | The plan. On a dark desk the cover deals out into all fourteen real pages, two by seven, as the camera rises. | Fourteen pages. Your logo. Your colours. Your prices. |
| 18 to 23 s | Home: "Mia picked Option B and tapped Book. Send the deposit link: 30% is $1,037.", ringed. | You press Send. She taps *Book.* |
| 23 to 28 s | The inbox on the trip: "What time is pickup tomorrow?" at 23:47, answered from the trip plan at 23:48, ringed. | On the trip it answers her. You are asleep. |
| 28 to 32 s | The pages squared in one stack, in warm early light. | One reel in. One booking out. |

End card: "You run the trips. WanderBuddy runs the rest." 35.2 s. File: `out/v2-the-reel.mp4`.

What is real and what is not:

- The conversation, the panel, Home and the inbox are the public demo's CRM (`build/reel_capture.mjs`).
  The reel conversation was added to the demo's sample data in the browser, and the panel was really run on it.
- In the demo the reading and writing are done by a built-in stand-in for the model. So the panel's steps
  and layout are real, but its speed is not: its clock and its "Ready in 4 seconds" line are hidden, and
  the film makes no claim about how long it takes.
- The fourteen pages are the demo's real itinerary design (`build/reel_pages.mjs`). The sample trip's
  words were swapped from Krabi to the Ha Giang loop, and every photo frame was filled with the app's own
  four Vietnam photos (Ha Giang, Ninh Binh, Sapa, Hoi An), so photos repeat across pages.
- Her phone is set dressing (`build/reel_stills.mjs`).
- Score: generated (`build/reel_audio.py`): D major, plucked strings, one note a page.
