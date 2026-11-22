# WanderBuddy — Google Play Store listing (2026-09 rewrite)

**Purpose:** replace the stale Play listing that sells WanderBuddy as a *trip
planner*. This version repositions around **the app you actually use on the
ground** — the physical layer rivals cannot copy: live location among trip
members, in-person group translation / Live Conversation, structured border /
entry requirements, split costs, and the group trip chat. AI planning and Trip
Vibe are deliberately demoted, not deleted.

Paste each block into Play Console → **Grow → Store presence → Main store
listing**. Character counts are noted and every block is written to fit. Nothing
here is published automatically — this is a draft for founder review.

Sources: `marketing/ASO_OPTIMIZATION.md` (paste-ready ASO), `STORE_LISTING.md`
(the stale live Play copy), `APP_STORE_LISTING.md` (the strong, feature-vetted
iOS twin — voice borrowed, claims cross-checked), `marketing/COMPETITIVE_ANALYSIS.md`
+ `marketing/GROWTH_PLAN.md` (positioning), and the code itself
(`lib/screens/**`, `lib/config/pricing_config.dart`).

---

## App title (max 30)

```
WanderBuddy: Group Trips
```
**(24 chars.) Recommended.**

Why keep the head term instead of a repositioning phrase in the title: Play
indexes the title more heavily than anything else, and *group trips / group
travel* is the phrase people actually search — there is no meaningful search
volume for "on-the-ground travel app." So the repositioning is carried by the
**short description, the body, and the screenshots**, while the title keeps the
term that earns the ranking. (This is exactly what `COMPETITIVE_ANALYSIS.md §9`
and `ASO_OPTIMIZATION.md §2` recommend.)

A/B title variants (all ≤30):
- `WanderBuddy: Group Travel` (25) — swaps "trips" (reads as *planning*) for
  "travel" (reads as *doing*). Slightly more on-brand for the reposition; test
  it head-to-head against the primary.
- `WanderBuddy: Travel Together` (28) — the current live title; warmer, but
  spends the slot on a feeling instead of a search term. Fallback only.

---

## Short description (max 80)

```
Group travel on the ground: live location, translate, split costs & group chat
```
**(78 chars.) Recommended.** Indexed and shown high on the page, so every word is
a search term — *group travel, live location, translate, split costs, group
chat* — and the first three words ("on the ground") do the repositioning before
the reader taps "more."

Alternates (all ≤80):
- `Live location, group translation & split costs — the app you use on the trip.` (77) — leads with the physical layer, clearest reposition, drops "group chat" from the indexed set.
- `Group travel that works when you land: live location, translate, split costs.` (77) — "when you land" instead of "on the ground."
- `Group trips: shared plan, live location, translate, split costs & group chat.` (77) — keeps a nod to planning; least repositioned.

---

## Full description (max 4000)

```
The trip is planned. Now you actually have to find each other in a city where nobody reads the signs.

WanderBuddy is the group travel app your friends use on the ground — once you've landed, split up at a market, and somebody's phone is at 4%. Live location, live translation, border rules, the money and the group chat in one place, instead of five apps and a screenshot of a flight nobody can find again.

SEE WHERE EVERYONE ACTUALLY IS
Live location sharing built for a group in a real place: find each other across a festival, a night market, a metro station you all named differently. It is never on by default. Both people have to agree, it runs out on a timer, and you can switch it off mid-trip without explaining yourself to anybody.

TALK WITHOUT MAKING EVERYONE SWITCH TO ENGLISH
Live Conversation: everyone speaks their own language out loud, and each person reads the room in theirs, live. Nobody gets demoted to the quiet one. Plus a translate tool for the menu, the sign, the taxi, and the pharmacy conversation you were dreading.

KNOW YOU CAN ACTUALLY CROSS THE BORDER
Structured entry requirements for any passport and any destination — whether you need a visa and where to sort it — with a link to the actual immigration page instead of a nine-year-old forum thread.
(Guidance only. Confirm with the official source before you fly.)

MONEY, SETTLED BEFORE ANYONE FLIES HOME
Split expenses evenly, by share, or by the exact amount, because one of you had the lobster. Balances and the shortest way to settle up sit on one screen, so nobody has to send the awkward message three weeks later.

ONE GROUP CHAT, ONE PLAN
Group chat, so plans stop scattering across four different apps, and a shared itinerary the whole group edits in real time. Everyone sees the same days. No more "wait, are we still doing the temple thing".

FIND A TRIP, OR BRING YOUR OWN
Browse public trips with the spots left showing, and join with a link or a QR code — joining a trip is always free. Or start a private one and approve everyone who gets in. WanderBuddy is built for the organizer who ends up running it: bigger groups, more room, and live maps are where a paid plan comes in.

FOR WHEN IT GOES WRONG, BECAUSE IT WILL
The local emergency number wherever you are, your embassy, your exact coordinates ready to send, and a checklist for the morning your phone or your wallet stops existing.
(Safety tools help you move fast. Always follow local authorities.)

AND YES, IT PLANS TOO
Build the itinerary day by day — as a group trip planner it does everything you'd expect — or tell the assistant your dates and what you like and let it draft one around whatever you've already booked. But planning is the easy part. WanderBuddy is for the rest of the trip.

WHAT WE WON'T DO
No ads. No trackers. Your data is not for sale. Every paid feature shows you the arithmetic: Google's cut, the API bill, and what is genuinely left for the developer.

A weekend road trip or three months backpacking. Two of you or eleven. WanderBuddy is the part of the trip nobody wants to volunteer for.

Questions or feedback? Reach us any time from inside the app.
```
**(≈2,760 chars — well under the 4,000 cap; room for a localized block per
`ASO_OPTIMIZATION.md §7` or a billing block per the founder-input notes below.)**

Keyword coverage woven in, once each, naturally: *group travel, group trip,
group chat, live location (sharing), translate / translation, Live Conversation,
entry requirements, visa, split expenses / split costs, itinerary, trip planner,
travel safety, travel with friends, road trip, backpacking, organizer, join a
trip, public trips, QR code.*

---

## What's new (release notes, max 500)

```
- Live location, rebuilt for the group: find each other on the ground, always with consent and a timer.
- Live Conversation: everyone speaks their own language out loud and reads the room in theirs, live.
- Structured entry requirements for any passport and destination, with links to the official immigration page.
- Split costs evenly, by share, or by exact amount, with the shortest way to settle up.
- Browse public trips, see the spots left, and join with a link or QR code.
```
**(≈480 chars.)**

---

## ASO / keyword strategy (Play has no keyword field)

Play ranks from **title + short description + full description** combined, so
terms are *woven*, not listed. Make sure each of these appears at least once in
the copy above (they do), and do **not** keyword-stuff — Google penalizes it.

Core set (physical-layer-forward):
`group travel · group trip · live location sharing · location sharing ·
group translation · translate · live conversation · entry requirements · visa ·
split expenses · split costs · group chat · shared itinerary · travel with
friends · trip organizer · road trip · backpacking · travel safety`

Deliberately demoted (present but not led on): `AI travel planner`, `trip
planner`, `Trip Vibe`. Each appears at most once, low in the body, so the term
is still indexed without steering the pitch.

Revisit after 30 days with Play Console's **search-term acquisition report** and
cut the half that turns out to be dead weight.

### A/B tests worth running
1. **Title:** `Group Trips` (primary) vs `Group Travel` vs `Travel Together`.
2. **Short description:** the "on the ground" primary vs the "the app you use on
   the trip" alternate — one repositions with a scene, the other names the
   category shift outright.
3. **First screenshot caption:** a live-location scene ("Find each other on the
   ground") vs the old planning hero — the reposition lives or dies on shot 1.

---

## Metadata & categorization (carry-over, confirm before publish)

| Field | Value |
| --- | --- |
| Application type | App |
| Category | Travel & Local |
| Tags | Group travel, Live location, Trip itinerary, Split expenses, Travel safety |
| Contact email | **TODO — a monitored support inbox** (STORE_LISTING.md still had this open) |
| Website | https://wanderbuddyapp.com |
| Privacy policy | `kPrivacyPolicyUrl` in `lib/core/legal.dart` — confirm it loads with no redirect |

Data-safety and content-rating answers are unchanged from `STORE_LISTING.md §Data
safety / Content rating` (UGC = yes; location shared only on opt-in; no ads /
no advertising ID; in-app account deletion exists). Re-use those answers; they
were written truthfully and still hold.

---

## NEEDS FOUNDER INPUT / COULDN'T VERIFY

1. **The free-vs-paid feature boundary is contradictory in the repo — resolve
   before publishing.** `pricing_config.dart` sells add-ons named *"Maps & Live
   Location" ($0.99/mo)* and *"AI Travel Assistant" ($2.99/mo)*, whose taglines
   read as **features you buy** ("Live location sharing and trip maps, on their
   own"). But the vetted iOS review note asserts *"Nothing in the app is gated
   behind a purchase. Paid items raise capacity limits only."* Both cannot be
   true. The draft threads this by saying **joining is always free** and framing
   "bigger groups, more room, and live maps" as "where a paid plan comes in" —
   without hard-claiming live location is either free or paid. **Confirm the real
   boundary** (is live location free, Premium-only, or an add-on?) so neither the
   copy nor the screenshots over- or under-claim.

2. **Exact store pricing — not asserted in the body on purpose.** Live values in
   `pricing_config.dart`: Premium **$6.99/mo**, **$59.99/yr** (~$5/mo, 28% off),
   **Lifetime $100 once**; add-ons **AI $2.99**, **Maps & Live Location $0.99**,
   **Large Trips $1.99**, **Extra Storage +25GB $1.99** (all /mo). Two things to
   settle: (a) Lifetime is **$100** in code but the iOS listing uses **$99.99**
   (store price-points rarely include $100.00) — pick one and make the code
   match; (b) decide whether to paste an explicit **subscription/billing block**
   into the Play description (Apple requires it; Play does not, but it is good
   practice and Play has its own subscription-disclosure policy).

3. **"First-trip-free" / trip-creation gating — is it actually live?**
   `GROWTH_PLAN.md` locks a *first-trip-free reverse trial → thin free tier, gate
   the organizer* model, and memory notes the hard-gate migration (0070) is
   **PENDING db push** with the decision since evolved to first-trip-free. The
   draft says "starting trips is free to start; a paid plan lifts limits" and
   "the organizer is the buyer" **without** asserting a hard creation gate.
   Confirm what ships before launch, and whether to add an explicit **"your first
   trip is free"** line.

4. **Regional / PPP pricing (India + SEA beachhead).** `GROWTH_PLAN.md §3.3`
   targets roughly **₹149/mo · ₹999/yr** for IN/SEA. Not reflected here. If those
   tiers are live in Play Console, the localized Hindi/Thai listings should hint
   at them; if not, the beachhead sees a rich-world USD price.

5. **Trip Vibe & AI planner were intentionally pulled from the hero.** Both are
   shipped (`itinerary_vibe_card.dart`, `ai_planner_screen.dart`) and Trip Vibe
   is a genuine "no rival does this" differentiator. The reposition demotes both;
   each survives as one low, indexed line. **Confirm you're OK leaving Trip Vibe
   out of the body** — it can go back as a single section if you'd rather keep it.

6. **Documents / Tickets vault — omitted deliberately.** `documents_screen.dart`
   exists (per memory: per-person Passport/Tickets/Visa, PDFs) and is a real
   on-the-ground utility, but the vetted iOS listing **explicitly excluded** it,
   and memory flags it as **local-only / backup-excluded**. Left out here to stay
   truthful. Decide whether to add it — and if so, do **not** imply cloud sync.

7. **In-chat message translation is NOT claimed.** The AI add-on tagline mentions
   "chat translations," but the vetted iOS listing explicitly excludes in-chat
   translation as a claim. The draft claims only the **in-person translate tool**
   and **Live Conversation**. Confirm chat-message translation is reliably shipped
   before adding it.

8. **Assets not produced here.** A physical-layer **screenshot set** (lead shot =
   live location, not the planner) and a **Play promo video** are separate
   deliverables (`ASO_OPTIMIZATION.md §5`), as are the **Hindi + Thai localized
   listings** (§7). The current 8-shot plan in `STORE_LISTING.md` still leads on
   the planner and should be re-shot to match this copy.

9. **Launch hook not used:** the first **500 accounts get free Lifetime**
   (`kFounderSeatCount = 500`). Not surfaced in the copy — decide whether it's
   worth a "founding members" line while seats remain.

---

*Draft only. Do not publish without resolving items 1–3 above. — 2026-09-09*
