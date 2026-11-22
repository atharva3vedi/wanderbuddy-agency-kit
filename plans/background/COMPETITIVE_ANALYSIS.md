# WanderBuddy — Competitive Analysis (rev. 2)

> **Everyone in this market is free. One of them is nearly us.**
> Most competitors eat one or two layers of the DIY stack. **Welago eats nearly
> all of them — free forever, on the web.** What none of them touch is the
> physical layer: *where people actually are, what is being said, and whether you
> can cross the border.*

Published page: <https://claude.ai/code/artifact/f401643b-552f-47cd-a05d-d19a43f7f666>

Sits alongside `GROWTH_STRATEGY.md` (who we sell to) and `ASO_OPTIMIZATION.md`
(how the store converts). Researched September 2026. Rev. 2 adds Welago, the full
feature matrix, and the build queue. Rev. 3 (2026-09-10) reconciles the matrix against
shipped code: date voting, the ideas board, a read-only web preview and first-trip-free
all landed on `deploy/play-store-ready` (builds 1.2.0+23/+24), pending Play upload.
Sources at the bottom.

---

## 1. The verdict

WanderBuddy competes against a **stack of five free things people already have**:
WhatsApp for the chat, a Google Sheet for the plan, Splitwise for the money,
Google Maps for the map, Google Translate for the language.

Wanderlog has eaten the most layers of that stack and is still, six years and only
$1.5M of funding later, the category leader — the category does not attract serious
capital, and the leader is beatable. But **Welago** (§4) has now assembled nearly
our whole coordination layer, free forever, on web as well as both app stores,
joinable without an install.

The defensible ground is narrower than it looks, and it is real: **nine capabilities
in the matrix are ours alone**, and seven of them are the physical layer.

**Positioning line:** *Welago is where you organise the trip. WanderBuddy is where
you survive it.*

---

## 2. The competitive map

Six tiers, ordered by damage done to us.

| Tier | Who | Threat | Note |
| --- | --- | --- | --- |
| **00** | **The DIY stack** — WhatsApp + Sheets + Splitwise + Maps + Translate | Critical | The real incumbent. Free, installed, working well enough. Our edge: it has no shared state |
| **01** | **Group trip planners** — Welago, Wanderlog, Troupe, TripIt + a micro-app swarm (Tripsil, WePlanify, AvoSquado, TripProf, Stippl, NomadCrew, mapa) | Critical | The store comparison we actually lose. Welago gets §4 |
| **02** | **Single-function leaders** — Splitwise, Polarsteps, Life360, Microsoft Translator | High | Each owns one of our tabs better than we do |
| **03** | **Funded AI planners** — Layla, Mindtrip, TripVexa, GuideGeek, Jourma | Warning | None do groups, but they made AI planning free and are colonising WhatsApp |
| **04** | **Travel-buddy matching** — GAFFL, JoinMyTrip, Travello, Zostel | Watch | GAFFL's 100k+ trips prove our listing mechanic; all feel empty outside their home region |
| **05** | **B2B / agency** — Travefy, and nobody else | Open | Agent-facing only. Our agency→auto-group channel is uncontested |

Detail worth keeping:

- **Wanderlog** — YC W19, $1.5M seed (General Catalyst, Abstract). Free tier is
  generous: unlimited trips, collaboration, expense splitting, maps. Pro ~$39.99/yr
  adds offline maps, unlimited AI, route optimisation, Gmail scanner, PDF export.
- **Troupe** — owned by **JetBlue Travel Products**. Owns the decide phase (polls,
  date voting) with airline distribution we can never match.
- **TripIt** — SAP Concur. Best-in-class reservation parsing; solo/business shaped.
- **Splitwise** — dominant on expenses, including India via UPI settlement links.
  See §6 for the opening they just handed us.
- **Microsoft Translator** — free group conversation mode, up to 100 people, each
  on their own device in their own language. The closest thing to Live Conversation.
- **Layla** — >$1B planned trip value across 30M messages on a €3M seed, and
  reachable inside **WhatsApp, Messenger and Instagram**. **GuideGeek** (Matador)
  lives in WhatsApp/IG DMs. **Jourma** forwards booking emails into WhatsApp and
  pushes flight alerts there. All three are **1:1 assistants** — see build item 05.

---

## 3. Full feature matrix

WanderBuddy inventory read from `lib/screens`, `lib/services` and `pubspec.yaml`
(Sept 2026). Welago and Wanderlog columns verified against published feature lists;
Troupe, TripIt and Splitwise from secondary sources and therefore conservative.

**Legend:** ✅ shipped · ◐ partial / limited / paid tier · ✗ not in published features
**🟡 = moat (only us)** · **🔴 = gap (someone has it, we don't)**
**† = shipped 2026-09-10 in build 1.2.0+23/+24 on `deploy/play-store-ready`, pending the founder Play upload — committed, not yet on users' devices.**

| | Capability | WanderBuddy | Welago | Wanderlog | Troupe | TripIt | Splitwise |
| --- | --- | :--: | :--: | :--: | :--: | :--: | :--: |
| | **DECIDE & PLAN** | | | | | | |
| | Collaborative itinerary | ✅ | ✅ | ✅ | ◐ | ✅ | ✗ |
| | Date voting with overlap detection † | ✅ | ✅ | ✗ | ✅ | ✗ | ✗ |
| 🔴 | Polls — destination, food, activities | ✗ | ✅ | ✗ | ✅ | ✗ | ✗ |
| | Ideas board / saved places to vote on † | ✅ | ✅ | ✅ | ◐ | ✗ | ✗ |
| | Threaded topic discussion | ◐ | ✅ | ✗ | ◐ | ✗ | ✗ |
| | AI trip planning | ✅ | ✅ | ◐ | ✗ | ✗ | ✗ |
| | AI assistant grounded in your trip | ✅ | ✅ | ◐ | ✗ | ✗ | ✗ |
| | **LOGISTICS** | | | | | | |
| | Reservation storage — flights, stays, cars | ◐ | ✅ | ✅ | ✗ | ✅ | ✗ |
| 🔴 | AI confirmation parsing — email, PDF, screenshot | ✗ | ✅ | ◐ | ✗ | ✅ | ✗ |
| 🔴 | Email-forwarding inbox (`confirm@…`) | ✗ | ✅ | ◐ | ✗ | ✅ | ✗ |
| 🔴 | Live flight status & delay alerts | ✗ | ✅ | ✗ | ✗ | ✅ | ✗ |
| 🔴 | Apple / Google Wallet boarding passes | ✗ | ✅ | ✗ | ✗ | ◐ | ✗ |
| 🔴 | Calendar sync | ✗ | ✅ | ◐ | ✗ | ✅ | ✗ |
| | Flight & document-expiry reminders | ✅ | ✅ | ✗ | ✗ | ✅ | ✗ |
| | **MONEY** | | | | | | |
| | Expense splitting | ✅ | ✅ | ✅ | ✗ | ✗ | ✅ |
| 🔴 | AI receipt scanning | ✗ | ✅ | ✗ | ✗ | ✗ | ◐ |
| | Multi-currency, live rates | ✅ | ◐ | ✅ | ✗ | ✗ | ◐ |
| 🔴 | Settlement links — UPI, PayTM, Venmo | ✗ | ✗ | ✗ | ✗ | ✗ | ✅ |
| | **COMMUNICATION** | | | | | | |
| | Group chat, in-app | ✅ | ✅ | ✗ | ◐ | ✗ | ✗ |
| | 1:1 direct messages | ✅ | ✅ | ✗ | ✗ | ✗ | ✗ |
| | Group voice room | ✅ | ✅ | ✗ | ✗ | ✗ | ✗ |
| 🔴 | Daily digest / morning summary | ✗ | ✅ | ✗ | ✗ | ✗ | ✗ |
| 🔴 | Reaches people in WhatsApp / SMS without the app | ✗ | ✅ | ✗ | ✗ | ✗ | ✗ |
| 🟡 | **Live multi-language speech conversation** | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 🟡 | **In-trip text translation** | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| | **ON THE GROUND — the physical layer** | | | | | | |
| | Trip-scoped map | ✅ | ◐ | ✅ | ✗ | ◐ | ✗ |
| | Route & road-trip planning | ✅ | ✗ | ◐ | ✗ | ✗ | ✗ |
| 🟡 | **Geotagged photo map** | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 🔴 | Offline maps & offline itinerary | ✗ | ✗ | ◐ | ✗ | ✗ | ✗ |
| 🟡 | **Consent-based live GPS location** | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 🟡 | **Talk to a local** | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 🟡 | **Structured entry requirements** | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| | Encrypted document vault | ✅ | ✅ | ✗ | ✗ | ◐ | ✗ |
| | Safety centre, block & report | ✅ | ◐ | ✗ | ✗ | ✗ | ✗ |
| | **SOCIAL & DISCOVERY** | | | | | | |
| 🟡 | **Public, joinable trips — meet strangers** | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| | Invite by link or QR | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| | Member profiles | ✅ | ✅ | ◐ | ◐ | ✗ | ◐ |
| | Shared photo gallery | ✅ | ✅ | ✗ | ✗ | ✗ | ✗ |
| | **PLATFORM & ACCESS** | | | | | | |
| | iOS / Android | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 🔴 | **Web app** — read-only trip preview † | ◐ | ✅ | ✅ | ◐ | ✅ | ✅ |
| 🔴 | **Join a trip without installing anything** † | ◐ | ✅ | ◐ | ✗ | ✗ | ◐ |
| | Browse as guest, no account | ✅ | ✅ | ◐ | ◐ | ✗ | ✗ |
| 🟡 | **Localised UI — 8 languages** | ✅ | ◐ | ◐ | ✗ | ◐ | ◐ |
| | **BUSINESS MODEL** | | | | | | |
| | Free to join someone's trip | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| | **Free to create a trip** — first trip free † | ◐ | ✅ | ✅ | ✅ | ✅ | ✅ |
| | Headline price | $6.99/mo · $59.99/yr · **1st trip free** | **$0 forever** | $39.99/yr | Free | Free / Pro | $4.99/mo |
| 🟡 | **Agency / tour-operator channel** | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |

### Reading the matrix

**Nine moat rows, thirteen gap rows** — down from sixteen. Two gaps closed outright
this week (date voting, ideas board) and three narrowed from absent to partial
(read-only web preview, web-join, first-trip-free). See †.

The moat is real but narrow, and almost entirely one thing: **the physical layer**
— where people are, what is being said, whether they can cross the border — plus
two structural positions nobody else wants (public trips, the agency channel).

The gaps still cluster tightly. They are not thirteen problems, they are three:

1. **We cannot be *fully* reached without an install** — the read-only web preview
   (migration 0078) now lets a joiner *see* a trip in a browser, but participating
   still needs the app, and there is no WhatsApp/SMS reach. *Partially closed.*
2. **We make people type what a competitor's AI reads automatically** — confirmation
   parsing, email inbox, receipt scanning, calendar sync. *Untouched — the biggest
   remaining opportunity.*
3. **We skipped the decide phase** — date voting (0079) and the ideas board (0080)
   now ship; only polls remain. *Nearly closed.*

Close cluster 2 and the matrix flips.

---

## 4. Head-to-head: Welago

**The closest competitor that exists.** Near parity with our coordination layer, on
every platform we are on *plus the web*, for free, forever.

| | |
| --- | --- |
| Company | TripDip, LLC — indie |
| Founder | Vincent Senese |
| Price | **$0 per trip, per person, forever** |
| Revenue | Booking affiliate commissions — Expedia, Booking.com, Kayak, 30+ partners |
| Platforms | Web · iOS · Android |
| Limit | 300 guests per trip |
| Tagline | *"Group trip planning without the chaos" / "Every trip starts with 'we'"* |

**Where they beat us:** join by link with no download or signup; runs on the web;
free forever with a revenue model that supports it; live flight status, connected-flight
grouping and crew matching; AI confirmation parsing; Wallet boarding passes; AI receipt
scanning; polls, threaded discussions, voice calls,
shared spreadsheets, Mystery Trip mode; and **encrypted personal document storage —
which kills our Documents vault as a differentiator.**

**Closed since (2026-09-10):** date voting with overlap detection (migration 0079) and
the ideas board (0080) now ship on our side too, and a read-only web trip-preview link
(0078) narrows the web-reach gap — all committed on `deploy/play-store-ready` in builds
1.2.0+23/+24, pending the founder Play upload. Their remaining coordination edges:
AI confirmation parsing, receipt scanning, live flight status, Wallet passes, calendar
sync, daily digest, polls, and full web participation.

**Where we still stand alone** (verified against their published feature list): live
GPS location, live speech translation, structured entry requirements, public/joinable
trips, and the agency channel. They have a *rental-host* product and a corporate-events
beta, not a tour-operator channel.

**The honest read: the product is scarier than the company.** A one-founder LLC with
no visible funding, no visible install base, and no app-store rating footprint we could
find — so today it is not a distribution threat. But it is proof that our coordination
layer is not defensible on its own, and that someone will build it for free and
monetise the booking instead.

**Also new:** *WeGoing!* (founder Paul Eulette) launched to consumers 2026-08-11,
aimed at the money problem — dates, deposits, and budgets nobody wants to say out
loud, so no one is left carrying the trip on their credit card.

---

## 5. The build queue — what to add to stay competitive

Ordered by how much each changes the outcome, not by difficulty. Sizes assume what
is already wired: Groq + Supabase Edge Functions, Mapbox, Stream, Agora,
`share_plus`, `app_links`.

### 01 · A read-only web view of a trip — **S/M** — *defends join-without-install*
Anyone with the invite link opens the trip in a browser (itinerary, map, who's
coming) and only needs the app to participate. Flutter web already compiles; a
stripped SSR page is fine if faster.
**Why:** Welago's single biggest structural advantage, and the reason a six-person
group picks them. Every joiner currently faces an install before seeing anything.
Highest impact per unit of work on this list.
**Status (2026-09-10):** a read-only web *preview* link shipped (`public_token` + anon
`get_public_trip`, migration 0078); full web *participation* is still open.

### 02 · AI confirmation parsing + forwarding inbox — **M** — *defends vs Welago & TripIt*
Forward a booking email, or drop a screenshot/PDF, to `confirm@` → it becomes an
itinerary item with times, confirmation number and location.
**Why:** TripIt's best trick, and Welago has it. Highest perceived magic in the
category. Groq is already behind an Edge Function, so most of the cost is the
inbound mail route and the parser prompt.

### 03 · Offline maps, itinerary and documents — **M** — *deepens the moat*
Cache trip map tiles, the day plan, the document vault and the entry-requirement card.
**Why:** strategically the best item here. Offline is a category-wide weakness (only
Wanderlog Pro has it) and it is worth most **exactly where our moat already is** —
on the ground, abroad, roaming dead. Live location and border rules that fail without
data are a promise we do not currently keep.

### 04 · The decide phase — voting, polls, ideas board — **S** — *defends vs Troupe & Welago*
Availability voting with overlap detection, polls on destination and food, a shared
ideas board people upvote before it becomes itinerary.
**Why:** we start at "the trip exists." Troupe, Welago and AvoSquado start one step
earlier — where the group actually is when the idea is born — so they own the
conversation before we appear. Cheapest row here; closes three matrix gaps at once.
**Status (2026-09-10):** date voting (0079) and the ideas board (0080) shipped in builds
1.2.0+23/+24. Only polls remain (deferred — entangled with Stream chat).

### 05 · WhatsApp: put the group's trip inside the group chat — **L** — *defends against the DIY stack itself*
A WhatsApp presence that posts itinerary changes, expense adds and departure reminders
into the group's **existing** chat and accepts replies back — "add ₹800 dinner, split
4 ways", "where is everyone".
**Why:** Layla, GuideGeek and Jourma are all already in WhatsApp — but every one is a
**1:1 assistant**. Nobody has put a *group's shared trip state* in there. For an
India → SEA beachhead where WhatsApp **is** the group chat, this stops us fighting to
drag six people out of it. Biggest strategic prize, biggest build. Telegram second;
WeChat only for Chinese outbound.

### 06 · AI receipt scanning + UPI settlement links — **S** — *attacks Splitwise's weak moment*
Photograph a receipt and it splits itself; settle through a UPI deep link instead of
a screenshot and a promise.
**Why:** Splitwise capped its free tier and fell to 1.8/5 on Trustpilot. Their India
lock-in is UPI settlement — the one thing our tracker cannot do. Small work; turns a
defensive row into the §6 opening.

### 07 · Live flight status, Wallet passes, calendar sync, daily digest — **M together** — *table stakes*
The polish tier. None wins a comparison alone, but their absence is noticed in every
review. Batch them after 01–04.

### Do NOT build
- **The booking-affiliate marketplace.** Welago's and Wanderlog's model. It needs web
  reach we don't have, and copying it means becoming a worse version of them.
- **More AI trip planning.** Layla and Mindtrip made it free and better. Every hour
  there is an hour not spent on the physical layer nobody else defends.

---

## 6. The hard finding: our price points at our weakest comparison

| | Free tier includes | Paid |
| --- | --- | --- |
| **Welago** | **Everything** — unlimited trips, 300 guests, web + iOS + Android, joinable by link with no download | **Nothing. "$0 per trip, per person, forever."** Booking affiliates |
| **Wanderlog** | Unlimited trips, collaboration, expense tracking, maps, 5 AI msgs/trip | $39.99/yr → offline maps, unlimited AI, route optimisation, Gmail scanner |
| **Troupe** | Everything | — |
| **WanderBuddy** | Joining a trip, chat, itinerary, community, **your first trip free** | **$6.99/mo · $59.99/yr · $100 lifetime** → **every trip after the first** |

We charge roughly **1.5× the category leader's Pro price for the action the category
leader gives away free** — and Welago gives away more than that, forever, on the web.
The comparison is lost before our features are read, at exactly the funnel step
`GROWTH_STRATEGY.md` §2 identifies as narrowest (installs → tries to create → pays,
modelled at 18–28%).

**The counter-argument is good.** The gate makes the organizer the buyer by design,
and every paying organizer drags in 4–6 free joiners. Wanderlog and Welago are
subsidised by booking affiliate revenue we do not have.

**The testable version:** *first trip free; the gate lands on the second.* Keeps "the
organizer is the buyer" but moves the paywall from before value to after it. A pricing
experiment, not a strategy change. **Shipped 2026-09-10** (commits `c0115e5` /
`cfc17d0`), pending Play upload — the store comparison "pay to start" is now "start free."

---

## 7. Three openings

1. **Splitwise just made itself hated.** Free tier capped at ~2–5 expenses/day with
   ads; receipt scanning and currency conversion behind Pro. Trustpilot **1.8/5, 65%
   one-star** (Mar 2026). Bites hardest in **India**, our beachhead. Pair the content
   series with build item 06 and it becomes a wedge, not just a feature.
2. **The physical layer is empty ground.** Not "during the trip" — Welago reaches
   there. Specifically: where people are, what is being said, whether you can cross
   the border. Seven of our nine moat rows live here.
3. **India → SEA is where the moat is deepest.** Language wall, entry-requirement
   anxiety and group-safety need all peak there; Tier 01 is weakest there; and
   WhatsApp is the group chat, which makes build item 05 a distribution strategy.

---

## 8. Threats, ranked

1. **Price against free incumbents — now including a near-clone.** Welago.
2. **We are unreachable without an install.** Three matrix gaps compound into one
   structural disadvantage at the moment a group picks an app. Build items 01, 05.
3. **Breadth without depth.** Nine jobs, each with a free specialist — and Welago is
   now the specialist for most of them at once.
4. **Cold start.** Community and public trips are worthless below a density threshold.
5. **AI is table stakes**, and the funded players are already inside WhatsApp.
6. **Microsoft Translator's free group conversation mode** — up to 100 people, free.
   Our defence is positioning, not technology.
7. **The SEO knife fight.** Head terms are closed; get *into* the listicles instead.
8. **Troupe has JetBlue behind it.** Distribution we cannot match.

---

## 9. Actions, in priority order

1. **Reposition from planner to the app you use on the ground.** Store listing,
   screenshots, hook copy. Free, and fixes the comparison we lose. The live Play
   listing is still stale — paste-ready rewrite is in `ASO_OPTIMIZATION.md`.
2. **Ship build items 01 and 04** — web trip view + the decide phase. Five matrix
   gaps closed; removes the reason a group picks Welago.
3. **Run the first-trip-free experiment.**
4. **Point a content series at the Splitwise cap, and ship item 06 behind it.**
5. **Demote AI in the pitch;** promote live location, Live Conversation, entry
   requirements — seven of the nine moat rows.
6. **Scope the WhatsApp group bridge (item 05)** — a distribution strategy, not a feature.
7. **Treat the agency track as a moat, not a side quest.**

---

## Sources

- **WanderBuddy** — feature inventory read from `lib/screens`, `lib/services`, `pubspec.yaml` (2026-09-09); pricing from `lib/config/pricing_config.dart`
- **Welago** — [site](https://www.welago.com/) · [features](https://www.welago.com/features) · [pricing](https://www.welago.com/pricing)
- **WeGoing!** — [consumer launch 2026-08-11](https://finance.yahoo.com/small-business/articles/wegoing-launches-group-travel-app-123000560.html)
- **Wanderlog** — [Pro pricing](https://monkeyeatingmango.com/blog/wanderlog-pricing-2026/) · [free vs paid](https://tripstone.app/blog/wanderlog-pro-cost) · [expense splitting](https://wanderlog.com/travel-budget-expense-splitting-app) · [funding](https://aitravel.tools/wanderlog-review/)
- **Troupe / JetBlue** — [Travel Massive](https://www.travelmassive.com/posts/troupe-148183304) · [Vacationer](https://www.vacationer.travel/the-troupe-app-makes-group-travel-easier/)
- **Splitwise** — [free-tier cap](https://splittyapp.com/learn/splitwise-free-limits/) · [free vs Pro](https://split-circle.com/en/blog/splitwise-free-vs-pro) · [pricing & Trustpilot](https://usefairsplit.com/blog/splitwise-pricing/)
- **Messaging-surface AI** — [Layla — WhatsApp/Messenger/Instagram](https://layla.ai/) · [Jourma & GuideGeek WhatsApp assistants](https://jourma.de/en/blog/best-trip-planner-whatsapp-integration-2026-5ih8)
- **Layla / Mindtrip** — [$1B trips planned](https://finance.yahoo.com/news/layla-surpasses-1-billion-trips-165400507.html) · [Layla seed](https://www.phocuswire.com/layla-launch-funding-ai-travel-planner) · [Mindtrip funding](https://vctavern.com/mindtrip-raises-multi-million-dollar-funding-to-expand-ai-powered-travel-planning-platform/)
- **Offline & feature expectations** — [Airalo roundup](https://www.airalo.com/blog/best-group-travel-apps) · [mapa — offline cached maps, polls](https://apps.apple.com/us/app/mapa-group-travel-planner/id6777733374)
- **Polarsteps** — [ratings](https://www.wandrly.app/comparisons/wanderlog-vs-polarsteps)
- **Travel-buddy apps** — [GAFFL](https://www.gogaffl.com/best-travel-buddy-app) · [Hostelworld roundup](https://www.hostelworld.com/blog/7-best-apps-for-solo-travellers-to-meet-people-on-the-road/)
- **Translation** — [live conversation apps](https://maestra.ai/blogs/best-translation-apps-for-live-conversation)
