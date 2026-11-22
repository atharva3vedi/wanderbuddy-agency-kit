# WanderBuddy — App Store screenshot set (copy & notes)

10 shots at **1284 × 2778**, in `output/app-store/`. Listing text lives in
`../../APP_STORE_LISTING.md`.

Rebuild the whole set with:

```bash
cd marketing/src/appstore && node build.mjs && node render.mjs
```

## Why 1284 × 2778

App Store Connect accepts four sizes on this slot: 1242 × 2688, 2688 × 1242,
1284 × 2778, and 2778 × 1284. Portrait rules out two of them, and of the
remaining pair **1284 × 2778 is the only one valid for both the 6.5" and the
6.7" display slot**, so a single upload fills both. It is also the higher
resolution of the two.

The canvas is two constants at the top of `src/appstore/build.mjs`. Switching to
1242 × 2688 (or to a 6.9" set at 1290 × 2796) means changing `W` and `H` and
re-running; every layout is positioned off those, and the aspect ratios differ
by hundredths of a percent.

## The trick: two shots that are halves of one picture

The App Store shows screenshots in a horizontal carousel, so neighbours are
seen together. Two of the pages here render double-wide at **2568 × 2778** and
get sliced down the middle into a pair. Each half stands on its own, and side by
side they read as one image.

| Pair | Page | What crosses the cut |
| --- | --- | --- |
| 1 + 2 | `pano-a.html` | **A single phone.** It sits dead centre, so its left half ends shot 1 and its right half opens shot 2. The headline splits with it: "One App." then "Every Journey." |
| 5 + 6 | `pano-b.html` | **A conversation.** Someone says 駅はどっち？ at the right edge of shot 5, a sound wave carries it across the gap, and it lands as "Which way to the station?" at the left edge of shot 6. The headline splits too: "Everyone Speaks" then "Their Own Language." |

Consequences worth knowing before you upload:

- **Order is load-bearing.** Reordering or dropping one half breaks the effect.
- **Search results show the first three shots**, so slots 1 and 2 appear
  together there. That is the best place for the split phone.
- Add `?guides` to a page URL in a browser to see the cut line drawn in red.

## The 10-shot story

**1-2** does everything → **3** AI writes the days → **4** reads the trip's
personality → **5-6** everyone speaks their own language → **7** find or start a
crew → **8** the whole toolbox → **9** location stays yours → **10** closing card.

| # | Screen | Rendered headline | Alt 1 | Alt 2 |
| --- | --- | --- | --- | --- |
| 1 | Hero, left half | **One App.** | Everything. | One Place. |
| 2 | Hero, right half | **Every Journey.** | Every Trip. | For All Of It. |
| 3 | AI planner | **Plan a Whole Trip in Seconds** | Your Itinerary, Written For You | AI Plans, You Explore |
| 4 | Trip Vibe | **Know Your Trip's Personality** | Every Trip Has a Vibe | See Your Trip's DNA |
| 5 | Live Conversation, left | **Everyone Speaks** | You Talk. | Say It In Yours. |
| 6 | Live Conversation, right | **Their Own Language.** | Everyone Understands. | They Read It In Theirs. |
| 7 | Community | **Find Your Travel Crew** | Travel Together | Join Trips, Meet Travellers |
| 8 | Toolbox | **No More App Switching** | Everything You Need | One App, Every Tool |
| 9 | Privacy | **Your Location. Your Rules.** | Private by Design | Nobody Sees You By Default |
| 10 | Closing | **Your Adventure Starts Here** | Start Exploring Today | Go Somewhere |

## Alt text (under 140 chars each, optional but good for accessibility)

1. One app for planning, chat, expenses, safety, and exploring trips together.
2. Every travel tool your group needs, from itinerary and visas to shared photos.
3. WanderBuddy's AI writes a full day-by-day itinerary you can keep in one tap.
4. Trip Vibe rates a trip on nature, culture, nightlife, adventure, and local food.
5. Live Conversation: a trip member speaks Japanese into a voice room.
6. The same line arrives in English, captioned live for everyone in the room.
7. Browse public travel groups with live capacity bars and QR join codes.
8. Expenses, currency, visa, SOS, tips, maps, photos, and itinerary in one app.
9. Live location sharing with mutual consent, a timer, and revoke at any moment.
10. Explore destinations worldwide. Your adventure starts here.

## Real capture vs designed chrome

Every phone shows a **real captured app screen**:

- #1-2 Your Trips home · #3 Itinerary · #5 Live Conversation · #6 Translate
- #7 Community browser · #9 Members with "Ask for location" · #10 Community browser

Designed marketing chrome, so you can decide what to keep:

- **iOS status bar.** Every capture came off an Android device, so the punch-hole
  camera and Android status icons are covered by a drawn iOS bar (9:41, Dynamic
  Island, signal / wifi / battery), colour-matched per screen. Without this the
  set shows another platform's chrome, which is both a polish problem and an
  unnecessary brush with guideline 2.3.10.
- **Backgrounds.** CSS/SVG night city, mountains, and aurora. No stock photos
  were downloaded. Treat them as brand art, not literal places.
- **#3 day cards** illustrate the AI planner's real day-by-day output.
- **#4 radar** re-creates the real **Trip Vibe** feature: same 5 axes, ring
  style, and fill from `radar_chart.dart`. No populated Trip Vibe screen was
  ever captured, so this panel is drawn. Values: Local Food 95 (standout),
  Nature 92, Adventure 84, Culture 70, Nightlife 41. The app's real factor is
  "Local Experience"; it is framed as "Local Food" here.
- **#5-6 speech bubbles and the sound wave** are drawn. They show what Live
  Conversation does, not a captured transcript.
- **#7 public trip rows** (Kyoto Foodies, Bali Surf Week, Patagonia Trek) are
  example data, not live trips.
- **#10 destination cards** are brand chips. No flag emoji anywhere, because
  Windows and Chromium cannot render them; coloured dots stand in.

## Feature-accuracy calls

Carried over from the Play set, and still true here:

- **No "Documents" or "Packing" tile** in shot 8. Neither is a built feature.
  The grid is Expenses, Currency, Visa, SOS, Travel tips, Maps, Photo feed,
  Itinerary, all of which are real.
- **No in-chat translation exists.** Shots 5-6 market the real **Live
  Conversation** voice room and the **Translate tool**, not per-message chat
  translation.
- **No pricing anywhere.** The captured pricing screens are stale (they show
  $74.99 against a real $59.99), so pricing stays out of the images. Shot 8 says
  only "Free to use. Paid extras only ever add capacity", which is true.

## If you keep iPad support

`TARGETED_DEVICE_FAMILY = "1,2"` still claims iPad, which forces a second set at
**2064 × 2752**. Unlike the iPhone sizes, that one is not a constant swap: its
aspect (0.75) is far wider than 0.46, so the columns have to be re-laid. Either
drop iPad (see `APP_STORE_CHECKLIST.md` 0.6) or add a third canvas to
`build.mjs` and rework the layouts for it.
