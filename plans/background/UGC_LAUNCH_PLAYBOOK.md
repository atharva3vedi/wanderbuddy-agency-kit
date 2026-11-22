# WanderBuddy — AI UGC Launch Playbook

Five Higgsfield-ready scripts, the production workflow that makes them cheap,
a day-1 slate of 10 posts, and the marketing plays around them.

Everything below uses **shipped features only** — checked against
`APP_STORE_LISTING.md` and `lib/screens/`. No invented functionality.

---

## 0. Before anything: the three rules

**Rule 1 — The app is never AI.**
Every frame that shows the product is a real screen recording off a real device.
AI generates the *humans*. This is the single biggest credit saver in the whole
playbook (the app footage costs zero credits and is reusable for a year), and
it is the only way the UI is actually correct.

**Rule 2 — One cast, forever.**
Six characters, locked once, reused in every video from now until you get bored.
Recurring faces are why people stop scrolling on video #40. Also: character
references are cheap, re-rolling faces every video is not.

**Rule 3 — Label the synthetic footage.**
Turn on the "AI-generated content" toggle on TikTok / Reels / Shorts for any
clip with a synthetic human in it. Both platforms down-rank realistic
undisclosed synthetic media when they detect it, and stating "these are real
users" about generated actors is the kind of claim that draws an FTC complaint.
Write the captions in the app's voice, not as fake testimonials, and you get to
keep the edge without the liability.

---

## 1. The look bible

Append this to **every** image prompt. It is the whole brand in one paragraph.

```
Shot on a phone by someone in the group. Direct on-camera flash, harsh falloff
into near-black, blown-out neon highlights in electric blue and sodium amber,
heavy grain, slight motion blur, 18mm wide, chromatic fringing, unflattering
honest angle, no makeup, nobody posing for the camera, candid mid-sentence
expression, 2003 point-and-shoot energy on a modern sensor.
```

Negative prompt (paste into the negative field every time):

```
stock photo smile, studio lighting, travel influencer, drone postcard, perfect
skin, symmetrical composition, watermark, text, logo, sunset silhouette, group
jumping on beach
```

**Palette to keep in shot:** ink-navy `#0B141F` shadows, azure `#1E88D6` screen
glow, sand-amber `#E0972A` streetlight, ocean-teal `#1FA89A` accents.
(Source of truth is `lib/theme/app_colors.dart` — the README palette is stale.)

**Edit grammar:** hard cuts only, no crossfades. Freeze-frame + all-caps Roboto
Condensed caption slams. Occasional 4-frame black flash between shots. Audio
cuts one beat *before* the picture.

---

## 2. The cast bible

Build these six once (Section 4, Phase 1) and reuse the character reference in
every generation. Descriptions are deliberately specific — vague prompts drift.

| # | Name | Prompt seed |
|---|------|-------------|
| 1 | **MAYA** | 28, Indian woman, half-shaved buzzcut, gold septum ring, forearm tattoos, oversized black band tee, tired eyes, unbothered |
| 2 | **TOBI** | 31, German man, tall and narrow, wire-frame glasses, moustache, grey technical windbreaker, deadpan |
| 3 | **PLOY** | 24, Thai woman, bleached mullet, oversized football jersey, layered silver chains, always mid-laugh |
| 4 | **DIEGO** | 26, Brazilian man, dense curly hair, white tank top, film camera on a strap, beaded bracelets, chaotic |
| 5 | **NNEKA** | 30, Nigerian woman, braids in a high bun, large gold hoops, oversized linen shirt, the adult in the room |
| 6 | **SAM** | 22, American, red hair, heavy freckles, thrifted flannel, cheap digital camera, permanently overwhelmed |

Six languages at one table is not decoration — it is the setup for the feature
nobody else has (Live Conversation).

---

## 3. The five scripts

Format per shot:
**IMG** = Higgsfield Soul image prompt · **MOT** = motion preset + movement note ·
**AUD** = spoken line or VO · **TXT** = on-screen text.

Every shot is **5 seconds**. Never generate longer. Trim in the edit.

---

### SCRIPT 1 — "SIX STRANGERS, ONE TABLE"
*Feature: Community public trips, join by link/QR, you approve everyone, shared live itinerary.*
*Runtime ~28s.*

**Shot 1 — the confession**
- **IMG:** MAYA, extreme close-up, lying in a dark bedroom at 3am, face lit only by the blue glow of a phone below frame, one eye catching the light, duvet edge in frame
- **MOT:** slow push in
- **AUD (Maya, to camera):** "I let five strangers plan my holiday."
- **TXT:** none — let the line breathe

**Shot 2 — proof**
- **SCREEN RECORDING** — Community tab, scrolling public trips, spots-left counters visible. Thumb enters frame, real hand, real phone.
- **AUD (Maya VO):** "Public trips. You can see how many spots are left. Like picking a table."

**Shot 3 — the roll call**
- **IMG:** five separate flash-lit portraits, each a different city at night — TOBI in a Berlin stairwell, PLOY at a Bangkok street stall, DIEGO on a São Paulo balcony, NNEKA in a Lagos kitchen, SAM in a beige American bedroom
- **MOT:** whip pan between each, 0.6s per face
- **AUD:** each says their own name and city, in their own language, on top of each other
- **TXT:** name slams in corner per face

**Shot 4 — the gate**
- **SCREEN RECORDING** — join-by-code sheet / QR, then a join request being approved.
- **AUD (Maya VO):** "Nobody gets in unless somebody lets them in."

**Shot 5 — arrivals**
- **IMG:** DIEGO at an airport arrivals barrier at night, holding a bent cardboard sign with a handwritten name, harsh overhead fluorescent, crowd blurred around him
- **MOT:** handheld, slight sway
- **AUD:** airport ambience only

**Shot 6 — the table**
- **IMG:** overhead shot of all six around a cluttered plastic table at a night market, direct flash, spilled drinks, phones face-down, everyone mid-laugh, nobody looking at the lens
- **MOT:** overhead descend
- **AUD (Nneka, half-shouted):** "We met four days ago!"

**Shot 7 — end card**
- Freeze the overhead. Grade to ink-navy. Slam text.
- **TXT:** `WANDERBUDDY` / `THE GROUP CHAT IS NOT A PLAN` / `App Store · Google Play`

---

### SCRIPT 2 — "NOBODY SWITCHED TO ENGLISH"
*Feature: Live Conversation — everyone speaks their own language out loud, each person reads the room in theirs, live. This is the one no competitor has. Put the most budget here.*
*Runtime ~26s.*

**Shot 1 — discomfort on purpose**
- **IMG:** PLOY at a Bangkok night market, talking fast and animated directly to camera, harsh flash, steam and neon behind her
- **MOT:** handheld, locked close
- **AUD:** Thai dialogue, fast, **no subtitles for the first 1.5 seconds**
- **TXT:** appears late — Thai caption, then the English under it

**Shot 2 — the reply**
- **IMG:** TOBI opposite her, glasses fogged from food steam, answering flatly
- **MOT:** whip pan from Ploy
- **AUD:** German
- **TXT:** German caption, English under it

**Shot 3 — the overlap (the actual differentiator)**
- **IMG:** two-shot, DIEGO and NNEKA both talking at once, gesturing over each other
- **MOT:** crash zoom out to reveal the table
- **AUD:** Portuguese and English colliding
- **TXT:** two caption streams stacked, both flowing, neither dropping
- *This is the point. Every other translation app dies here. Hold the shot.*

**Shot 4 — proof**
- **SCREEN RECORDING** — Live Conversation screen, speaker names colour-tagged, lines arriving in the viewer's own language.
- **AUD (VO, dry):** "Everyone's phone hears only its owner. That's why it doesn't fall apart when you talk over each other."

**Shot 5 — the payoff**
- **IMG:** NNEKA leaning back, laughing, phone flat on the table beside her, flash-lit
- **AUD (Nneka):** "I haven't spoken English in four days."

**Shot 6 — the menu**
- **SCREEN RECORDING** — Translate tool on a menu / pharmacy sign.
- **AUD (VO):** "And a translate tool, for the pharmacy conversation you were dreading."

**Shot 7 — end card**
- **TXT:** `NOBODY GETS DEMOTED TO THE QUIET ONE` / `WANDERBUDDY` / `App Store · Google Play`

---

### SCRIPT 3 — "THE TRIBUNAL"
*Feature: expense splitting — evenly, by share, or exact amount. Edgy comedy, staged like an interrogation.*
*Runtime ~24s.*

**Shot 1 — the room**
- **IMG:** single bare bulb over a hostel table, six silhouettes around it, DIEGO alone on the lit side, interrogation staging, deep ink-navy shadows
- **MOT:** slow overhead descend
- **AUD:** chair scrape, silence

**Shot 2 — the charge**
- **IMG:** NNEKA standing, arms folded, backlit, prosecutor energy
- **MOT:** low-angle push in
- **AUD (Nneka):** "He ordered the lobster."

**Shot 3 — the defence**
- **IMG:** DIEGO, hands up, mouth open mid-protest, flash blowing out his face
- **MOT:** crash zoom in
- **AUD (Diego):** "It was market price!"

**Shot 4 — the gavel**
- **IMG:** TOBI banging a flip-flop on the table like a gavel, absolutely straight-faced
- **MOT:** snap zoom
- **AUD:** three flat slaps

**Shot 5 — the evidence**
- **SCREEN RECORDING** — expense split screen: switch from *evenly* to *exact amount*, Diego's number climbing.
- **AUD (VO):** "Split evenly, by share, or by the exact amount. Because one of you had the lobster."

**Shot 6 — verdict**
- **IMG:** freeze on Diego's face, defeated
- **TXT:** his owed amount slams over his face in huge type

**Shot 7 — end card**
- **IMG:** everyone cheering, flash, Diego head in hands
- **TXT:** `SETTLED BEFORE ANYONE FLIES HOME` / `WANDERBUDDY`

---

### SCRIPT 4 — "TELL IT THE VIBE"
*Feature: AI planner (say the vibe, it writes the days around what you've booked, one tap adds it) + Trip Vibe score.*
*Runtime ~26s.*

**Shot 1 — the refusal**
- **IMG:** SAM on a hostel bunk, upside down, head hanging off the edge, phone above face
- **MOT:** static, handheld drift
- **AUD (Sam):** "I don't want an itinerary. I want a personality."

**Shot 2 — the brief**
- **IMG:** close on Sam's mouth, flash-lit, saying it fast
- **MOT:** extreme close, slight shake
- **AUD (Sam):** "Five days. Cheap. Hot. Walkable. No museums."
- **TXT:** the five words slam one at a time

**Shot 3 — proof**
- **SCREEN RECORDING** — AI planner: prompt in, itinerary cards out, **one tap** writes them into the real trip. Hold on the tap.
- **AUD (VO):** "It writes the days around what you've already booked. One tap and it's a real itinerary, not a chat message."

**Shot 4 — the score**
- **SCREEN RECORDING** — Trip Vibe card: nature, culture, nightlife, adventure, local food.
- **AUD (VO):** "Every trip has a personality. Now it has a score."

**Shot 5 — the score, on people**
- **IMG:** three quick flash portraits — PLOY on a scooter, MAYA eating something unidentifiable, DIEGO on a rooftop at 4am
- **MOT:** whip pan between
- **TXT:** vibe bars slam over each face — `NIGHTLIFE 9` / `LOCAL FOOD 10` / `CULTURE 2`

**Shot 6 — the button**
- **IMG:** TOBI, deadpan, direct to lens
- **AUD (Tobi):** "It suggested a museum. We deleted the museum."

**Shot 7 — end card**
- **TXT:** `TELL IT THE VIBE, NOT THE SCHEDULE` / `WANDERBUDDY`

---

### SCRIPT 5 — "THE MORNING IT WENT WRONG"
*Feature: Safety kit (local emergency number, embassy finder, exact coordinates, stolen-phone checklist), visa checker. This is the origin story — the reason the app exists. Slower, darker, warm landing. Do not make it funny.*
*Runtime ~30s.*

**Shot 1 — the pocket**
- **IMG:** POV down at an empty jacket pocket, hand patting it, crowded night street blurred beyond
- **MOT:** handheld, panicked drift
- **AUD:** street noise, suddenly too loud

**Shot 2 — the room**
- **IMG:** PLOY under green-white fluorescent in a bare police station corridor, plastic chairs, flat harsh light, exhausted
- **MOT:** static, slight sway
- **AUD:** VO out. Room tone only.

**Shot 3 — proof**
- **SCREEN RECORDING** — Safety screen: local emergency number, embassy finder, exact coordinates ready to send, lost-phone checklist.
- **AUD (VO, quiet):** "The local emergency number, wherever you are. Your embassy. Your exact coordinates, ready to send. And a checklist for the morning your phone stops existing."

**Shot 4 — she isn't alone**
- **IMG:** MAYA pushing through the station door, coat over pyjamas, holding her phone out screen-first
- **MOT:** handheld follow
- **AUD:** door, footsteps

**Shot 5 — the paperwork**
- **SCREEN RECORDING** — Visa screen: passport + destination, status, link to the official immigration page.
- **AUD (VO):** "And the visa answer from the actual immigration page. Not a nine-year-old forum thread."

**Shot 6 — dawn**
- **IMG:** wide, all six outside the station at first light, someone handing Ploy a coffee, nobody talking, exhausted, close together
- **MOT:** slow pull back
- **AUD (Ploy VO):** "I met these people three weeks ago."

**Shot 7 — end card**
- Hold on the wide, grade down.
- **TXT:** `BUILT AFTER A NIGHT LIKE THIS` / `WANDERBUDDY` / `App Store · Google Play`

> Keep the claim honest: the app *gives you the number, the embassy and your
> coordinates*. It does not contact emergency services for you. Say it that way.

---

### SCRIPT 6 — "THE PANEL"
*Features: all of them, described badly on purpose. Five beautiful people bury a
simple app in four-syllable words, then someone nobody asked says the actual
thing. The joke is the eloquence. Runtime ~24s.*

Casting note: everyone on the panel is styled to within an inch of their life,
lit like a fragrance campaign, and completely insufferable. The payoff shot is
lit like a phone flash in a kitchen. That contrast is the whole gag.

**Shot 1 — MAYA**
- **IMG:** MAYA in a wine bar, immaculate, backlit amber, one hand mid-gesture like she is presenting a thesis, glass of something orange
- **MOT:** slow push in
- **AUD (Maya):** "It's a synchronous multiparticipant itinerary architecture."
- **TXT:** `SHARED ITINERARY` in small type, bottom corner

**Shot 2 — TOBI**
- **IMG:** TOBI against a concrete wall, glasses, jaw, unreasonably good lighting for a man in a windbreaker
- **MOT:** whip pan in
- **AUD (Tobi):** "Fundamentally, an interoperability layer for irreconcilable temperaments."
- **TXT:** `LIVE CONVERSATION`

**Shot 3 — NNEKA**
- **IMG:** NNEKA, gold hoops catching a rim light, arms folded, absolutely certain
- **MOT:** crash zoom
- **AUD (Nneka):** "I would characterise it as computational fiscal reconciliation."
- **TXT:** `EXPENSE SPLITTING`

**Shot 4 — DIEGO**
- **IMG:** DIEGO on a balcony at golden hour, shirt open, film camera, insufferable
- **MOT:** slow orbit
- **AUD (Diego):** "Phenomenologically? It's transformative."
- **TXT:** `AI PLANNER`

**Shot 5 — SAM, drowning**
- **IMG:** SAM, same beautiful lighting, visibly out of his depth, sweating slightly, eyes darting
- **MOT:** static, hold too long
- **AUD (Sam):** "It's... polycentric."
- **TXT:** `HE DOESN'T KNOW WHAT THAT MEANS`
- Hold one beat past comfortable.

**Shot 6 — the payoff**
- Hard cut. Kill the beautiful lighting. Direct on-camera flash, cluttered
  hostel kitchen, someone who was never part of the conversation, mouth full,
  not looking at the lens, answering a question nobody asked them.
- **IMG:** PLOY at the counter eating instant noodles straight from the pot, flash-lit, unbothered
- **MOT:** handheld, slightly crooked
- **AUD (Ploy, flat, with her mouth full):** "We all use the same one. Nobody's translating. Nobody owes anybody. It's good."
- Beat. She goes back to the noodles.

**Shot 7 — end card**
- **TXT:** `WHAT SHE SAID` / `WANDERBUDDY` / `App Store · Google Play`

**Swap-ins for the payoff, if you want to shoot variants at zero extra cost:**
the night porter who has heard this conversation four hundred times · the
nine-year-old at the next table · the bartender collecting glasses · Nneka's
mother on a video call somebody forgot to end. Same line, same flash, same
crooked frame. Four variants of one video.

---

### SCRIPT 7 — "THE JOB"
*Every feature, mapped to a heist. Played 100% straight. Nobody winks, nobody
smiles, the music never tells you it's a joke. Runtime ~30s.*

Shot like a Michael Mann film that ran out of money. Cold blue, long lenses,
rain on glass, then the app footage cuts in exactly as it really looks, which
is the joke. **Never break the tone.** The moment someone smirks, it dies.

**Shot 1 — the briefing**
- **IMG:** six figures around a table in a stripped warehouse, single caged work-lamp, blueprints, cold blue light, faces half in shadow, cigarette smoke
- **MOT:** slow overhead descend
- **AUD (Nneka, quiet, absolute):** "Everyone sees the same plan. In real time. No exceptions."

**Shot 2 — the plan**
- **SCREEN RECORDING** — shared itinerary, real UI, being edited live. Day 3 entries visible.
- **AUD (Nneka VO):** "Day three. Fourteen hundred."
- **TXT:** the itinerary entry reads `14:00 — THE VAULT`

**Shot 3 — the crew**
- **SCREEN RECORDING** — join request coming in, then being approved.
- **AUD (Tobi VO, flat):** "You approve everyone who gets in."
- Cut to **IMG:** MAYA in a doorway, rain behind her, looking directly at the lens, deciding.

**Shot 4 — the language problem**
- **IMG:** DIEGO and PLOY in a van, headsets on, talking over each other urgently in Portuguese and Thai
- **MOT:** snorricam, tight
- **AUD:** both languages at once, no English
- **TXT:** two caption streams, both flowing
- **AUD (VO):** "The safecracker doesn't speak English. Nobody's asking him to."

**Shot 5 — the money**
- **SCREEN RECORDING** — expense split, switching to *exact amount*.
- **AUD (Sam VO, tense):** "Split by exact amount. He bought the good rope."

**Shot 6 — the contingency**
- **SCREEN RECORDING** — safety screen: coordinates ready to send, lost-phone checklist.
- **AUD (Nneka VO):** "If it goes wrong, your location goes to five people and nobody else. And there's a checklist for the morning your phone stops existing."

**Shot 7 — the exit**
- **SCREEN RECORDING** — visa checker: passport in, destination in, result, link to the official immigration page.
- **AUD (Tobi VO, completely deadpan):** "Any passport. Any destination. Check the visa before you fly."
- Hold on the screen one beat too long.
- *This is the punchline. Do not sell it. Do not cut early.*

**Shot 8 — the reveal that isn't one**
- **IMG:** the same six, wide, walking away from camera down a wet street at dawn, backs to us, carrying nothing suspicious whatsoever
- **MOT:** slow pull back
- **AUD:** silence, then one car door

**Shot 9 — end card**
- **TXT:** `FOR GROUPS WITH A PLAN` / `WANDERBUDDY` / `App Store · Google Play`

**Why this works:** it never actually says a crime happened. Six people made an
itinerary, approved their members, split a cost, checked a visa and went home.
The audience assembles the heist themselves out of real product features, which
means the joke is 100% theirs and 0% a claim you made. That is also why it
passes ad review.

**Zero-credit variants from the same footage:** recut Shot 7 alone as a
standalone 8s post. The visa checker plus the pause is the whole bit.

---

## 4. Higgsfield production workflow

Higgsfield renames plans, presets and credit costs often — check the current
pricing page before you buy a tier. The **order of operations** below is what
saves the credits, and it holds regardless of what the numbers say this month.

### Phase 0 — Zero credits (do this first, one evening)

1. **Record the app.** Android device + iOS simulator, screen record 12 clips at
   5s each: Community list with spots-left · join by QR · approve request ·
   shared itinerary being edited · AI planner one-tap · Trip Vibe card ·
   Live Conversation captions · Translate on a menu · expense split evenly →
   exact · safety screen · visa result · transparency screen.
2. **Name them `app_01_community.mp4`** etc. and put them in one folder. This
   folder feeds every video you make for the next year.
3. **Record the VO.** Your own voice on a phone in a quiet room beats any TTS
   for UGC. Do all five scripts in one sitting, ~10 minutes.

### Phase 1 — Build the cast (image credits only, ~1% of your budget)

4. In **Soul**, generate each of the six characters: cast description + look
   bible + negative prompt. 4 variations per character.
5. Pick one image per character. Save it as a **character reference / Soul ID**.
6. Do not skip this. Every later image references the ID, which is what stops
   Maya from having a different face in every video.

### Phase 2 — Lock every frame as a still (still image credits only)

7. For each shot marked **IMG**, generate the still: character reference +
   shot prompt + look bible + negative.
8. **Re-roll stills, never videos.** A still costs a rounding error. A video
   re-roll costs 20–50× more. If a shot isn't working, fix it here.
9. Approve the whole shot board before you animate a single frame. Five scripts
   ≈ 26 stills.

### Phase 3 — Animate only approved stills

10. Image-to-video, **5 seconds, 9:16**, one generation per approved still.
11. **Pick the model by job, not by prestige:**
    - Silent B-roll and movement → the cheapest video model on your plan.
      This is 80% of your shots.
    - A character speaking on camera → **Speak** (image + your recorded audio).
      Lip-sync from a still is far cheaper than a dialogue-capable video model.
    - Native-audio hero model (Veo-class) → **once per campaign**, on Script 2
      Shot 3 (the overlapping-speech shot). That is the only shot where
      simultaneous natural speech has to look real.
12. **Use the motion presets, don't write camera prose.** Crash zoom, whip pan,
    snorricam, overhead descend, handheld follow. Presets land first try;
    prose descriptions of camera moves fail and cost you a re-roll.
13. Cap re-rolls at two. Third failure means the still is wrong — go back to
    Phase 2.
14. If your plan has a relaxed / slow queue, batch the whole board into it
    overnight. Same output, lower cost.

### Phase 4 — Assemble (CapCut, free)

15. Timeline shape: **hook in the first 1.2s**, product proof by 40–60%,
    end card in the last 2s.
16. Drop in the real app recordings at the **SCREEN RECORDING** markers.
17. Burn captions. 90%+ of views are muted.
18. Export **1080×1920**, then re-crop to 4:5 and 1:1 for feed placements.

### Phase 5 — Multiply for free

19. Every hero cut becomes 3 posts at **zero extra credits**: swap the first
    3 seconds, swap the caption, swap the audio track.
20. Keep a **graveyard folder** of failed generations. Melted hands and warped
    faces cut beautifully as 4-frame subliminal flashes in this visual style.
    Nothing you paid for gets thrown away.

### The credit rules, condensed

| Rule | Why |
|---|---|
| Never text-to-video | You pay video price for a composition you haven't approved |
| Never exceed 5s | Length scales cost linearly; you cut it down anyway |
| Never re-roll a video 3× | The still is the problem, and stills are nearly free |
| One native-audio generation per campaign | It is the most expensive thing on the menu |
| App footage is always real | Free, correct, and reusable forever |
| Batch in the slow queue | Same frames, fewer credits |

---

## 5. The posting plan

### Day 1 — 10 assets

Cross-post each to TikTok, Reels and Shorts. Ten assets, thirty uploads, one
production run.

| # | Asset | Source | Length |
|---|-------|--------|--------|
| 1 | Six Strangers, One Table | Script 1, full | 28s |
| 2 | Nobody Switched To English | Script 2, full | 26s |
| 3 | The Tribunal | Script 3, full | 24s |
| 4 | Tell It The Vibe | Script 4, full | 26s |
| 5 | The Morning It Went Wrong | Script 5, full | 30s |
| 6 | The overlapping-speech loop | Script 2, Shot 3 only, captions, no VO | 8s |
| 7 | "POV: you let strangers plan your holiday" | Script 1 recut, new opener | 9s |
| 8 | One tap, real itinerary | App recording only, no AI humans | 12s |
| 9 | Where your money actually goes | Transparency screen + VO | 15s |
| 10 | 500 lifetime accounts. X left. | Counter card + Script 1 B-roll | 7s |

Assets 6–10 cost **zero new credits**. That is the point of the structure.

Pin #2 and #9. #2 is the feature nobody can copy this quarter; #9 is the one
that gets you written about.

### Day 2 onward — one post a day, batched weekly

Produce a week in one sitting every Sunday. Rotation:

| Day | Slot |
|---|---|
| Mon | **Feature demo** — screen recording + VO, 12s, zero AI credits |
| Tue | **Cast skit** — the six of them, one situation, one feature |
| Wed | **Founder POV** — your real face, real voice, what you built this week |
| Thu | **Reply video** — answer a comment on camera |
| Fri | **Travel hack** — genuinely useful, app appears for 3 seconds |
| Sat | **Trip spotlight** — a real public trip with real spots left |
| Sun | **The receipt** — this week's actual costs and revenue |

Weekly credit load: two Tuesday shots plus one Saturday shot. Everything else
is real footage. Roughly one script's worth of generation per month.

---

## 6. Marketing plays

### 1. Publish the arithmetic
`/transparency` is not a settings screen, it is your entire marketing position.
Post the real numbers weekly: store cut, API bill, what's left. Nobody in this
category does this, and it is the single most screenshot-able thing you own.
Tag it `#buildinpublic`, take it to Hacker News and Product Hunt as *"I publish
my exact infrastructure costs inside my app"* — not as a travel app launch.
HN does not care about another trip planner. It cares about that.

### 2. The 500 counter
First 500 accounts get Lifetime free, and it is already built
(`founder_lifetime`). Put the remaining number in every bio and post it daily
until it hits zero. Real scarcity, honestly counted, is the cheapest growth
mechanic in existence. When it hits zero, the countdown becomes a milestone
post.

### 3. "The Language Test" — a format, not an ad
Sit N people who share no common language at one table. One phone each. English
is banned. Film what happens. Run it as a repeatable series with real people in
your city, at language schools, at hostels. Formats travel; ads don't. This is
the only content in your arsenal that a competitor cannot shoot.

### 4. Ship Trip Vibe to the open web
Put the vibe scorer on the website as a no-signup quiz that outputs a shareable
card (nature / culture / nightlife / adventure / food). Personality quizzes are
the most-shared object on the internet and you already built the engine. The
card carries the app link. Hosting is already there on the Pages site.

### 5. Seed the Community tab before launch day
An empty public-trips list kills the strongest thing in the app. Before you
push the ads, seed 8–10 real founder trips with real dates and real spots-left
counters, and announce them like drops: *"Lisbon. October. 12 spots."* Discord
drop mechanics applied to travel. Scarcity you can see is scarcity that works.

### 6. Give the safety kit away
Publish the stolen-phone checklist and the embassy/emergency guide as a free
web page and a carousel. No signup wall. It gets saved, screenshotted and
re-shared by people who will never post about a travel app but will absolutely
post about not getting stranded.

### 7. Forums, played correctly
r/solotravel, r/backpacking and r/digitalnomad will destroy you for posting an
ad. They will upvote free visa data and a safety checklist all day. Show up as
the person who made the resource. Link in profile, not in post.

### 8. Physical QR at the point of loneliness
Hostel common rooms, language schools, coworking spaces, dive shops. A sticker
whose QR opens a *real public trip* leaving from that city, not a generic store
page. The conversion difference between "download our app" and "there are four
people going to Da Nang on Thursday" is enormous.

### 9. Reverse-psychology cut
One video in the avant-garde register: *"Do not download this app if you like
your holidays planned."* Hard cuts, black frames, no music. It will outperform
the sincere ones and it costs one re-edit of footage you already have.

### 10. Mine your own comments
Every comment is a free script. Reply on video. The algorithm rewards it, it
costs no credits, and it fills the Thursday slot permanently.

### 11. Store-side conversion
The iOS **promotional text** field changes without shipping a build — rotate it
to whatever campaign is live that week. Keep "Group Trips" in the iOS name;
it is indexed as heavily as the keyword field. Point every bio and QR at one
short link on your own domain so you can swap the store target and read the
click data. Check which host is canonical before you print anything: the
marketing site and the in-app support URLs are on different hosts today.

### 12. Launch-week press angle
Pitch one story, not twelve features: *"a travel app that shows you its own
invoices."* Send it to indie-app newsletters, Android/iOS blogs and travel-tech
writers. The transparency screen is the story; Live Conversation is the demo
that closes it.

---

## 7. First-week order of work

1. Record the 12 app clips and all five VO takes. *(one evening, zero credits)*
2. Build the six character references in Soul. *(~30 min)*
3. Generate the 26 stills and approve the board. *(~1 hour)*
4. Animate the board overnight in the slow queue.
5. Cut the five heroes in CapCut. *(~2 hours)*
6. Derive assets 6–10 from the same footage. *(~1 hour)*
7. Seed the Community tab with founder trips.
8. Post all ten. Pin #2 and #9.
