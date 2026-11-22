# Carousel: "6 apps you can delete before your next group trip"

Content-calendar slot: **Thu Sep 25** (IG + LinkedIn). Static track.
Owner: this session. SoT: the "Content ideas for WanderBuddy" calendar [848807].

## Design system (reuse, do not reinvent)

Same visual language as `marketing/reddit-posters/` so the set stays recognizable:

- **Field:** navy "Mission Control" radial. Reconciled to `app_colors.dart` dark
  tokens (SoT): top `#17293B` (surface) -> bottom `#0B141F` (bgPage). Text `#E7F1FA`,
  muted `#8DA7BC`. (The reddit-posters set predates the token freeze; this corrects it.)
- **Accent:** amber `#F0A431` (`app_colors.dart` dark `accent`, not the posters'
  `#F2A93B`), on exactly ONE word or chip per slide (the punch). On-amber text `#3A2606`.
- **Logo lockup:** real mark (twin peaks + wave) from `assets/icon-master.svg` +
  "WanderBuddy" wordmark, constant in the footer of every slide.
- **Fonts:** Windows system fonts (headless Edge needs no CDN), heavy weight for
  the delete line, regular for the payoff.
- **Sizes:** IG carousel **1080x1350 (4:5)**; LinkedIn document **1080x1080 (1:1)**.
  Build one HTML, render both by changing `--window-size`.
- **App names are TEXT chips, struck through. Do NOT paste real Splitwise / WhatsApp /
  Google logos** into a branded ad: it is a trademark and an AI-slop tell. A struck
  navy chip with the app's name reads cleaner and is safe.

## House rules
No em dashes. No pricing on the card. Only features we actually ship. Every claim
maps to a shipped feature (list at bottom). Warm, not cynical: the tired planner.

---

## The deck (8 slides)

**S1 — Cover**
- Kicker: WANDERBUDDY
- Headline: "6 apps you can **delete** before your next group trip"
- Sub: "Your group chat is quietly doing the job of six apps. Badly."
- Amber: *delete*

**S2 — Splitwise**
- Chip (struck): ~~Splitwise~~
- Line: "Every cost splits as you go and **settles** in everyone's own currency. Nobody sends the awkward money text three weeks later."
- Amber: *settles*
- Feature: expenses + multi-currency settlement

**S3 — the trip group chat**
- Chip (struck): ~~the 247-message group chat~~
- Line: "The plan, the map, the money, and the chat live in **one place**. The chat stops being where decisions go to die."
- Amber: *one place*
- Feature: in-app trip chat

**S4 — Google Maps pins**
- Chip (struck): ~~40 saved pins nobody else can see~~
- Line: "One **shared** map: everyone's pins, the day's plan, and where each other actually is, live."
- Amber: *shared*
- Feature: shared itinerary map + consent-based live location

**S5 — the Sheet itinerary**
- Chip (struck): ~~the itinerary trapped in a Google Sheet~~
- Line: "Say '5 days, Bangkok, cheap, hot, walkable.' Get a **real** itinerary the whole group can edit, not a tab nobody opens."
- Amber: *real*
- Feature: AI planner -> itinerary cards in the trip

**S6 — Google Translate** (the wedge, give it visual weight)
- Chip (struck): ~~Google Translate at the dinner table~~
- Line: "Everyone speaks their **own language** into the voice room. Nobody has to switch to English."
- Amber: *own language*
- Feature: live voice room + live captions/translation

**S7 — When2meet / Doodle**
- Chip (struck): ~~the when2meet nobody filled in~~
- Line: "Throw out some dates, everyone **votes**, the trip picks itself."
- Amber: *votes*
- Feature: date voting

**S8 — Payoff / CTA**
- Headline: "That is six apps. **One** trip. One app."
- Tagline: "Book first, figure it out together."
- CTA: "WanderBuddy. Link in bio."
- Amber: *One*

---

## Caption — Instagram
> Your group chat is not a travel agency, no matter how many voice notes you send it.
>
> Six apps you can leave behind on the next trip, because one app already does the job: splitting costs, the shared map, the plan, live location, the voice room so nobody switches to English, and the date vote that actually ends.
>
> Save this for the friend who is always the spreadsheet person. It is you, isn't it.
>
> WanderBuddy. Link in bio.
>
> #grouptravel #travelplanning #travelapp #traveltok #splitwise #southeastasia #travelhacks

## Caption — LinkedIn (slightly drier)
> Most group trips run on six apps and one exhausted organizer holding them together.
>
> We built the coordination layer into one app: shared expenses and settlement, a live shared map, an AI itinerary the group can edit, a voice room that translates so nobody has to switch to English, and group date voting.
>
> Swipe for the six you can delete. Curious which one your team would keep out of habit.

## Alt text (accessibility, per slide)
S1 cover; S2-S7 "Struck-through app name on a navy card with one line explaining the WanderBuddy feature that replaces it"; S8 "One app replaces six, tagline: book first figure it out together."

---

## Shipped-feature check (so we never claim vapor)
- Expenses + multi-currency settlement: shipped.
- Trip chat: shipped (Stream).
- Shared itinerary map + consent-based live location: shipped.
- AI planner in chat -> itinerary cards: shipped.
- Live voice room + captions: slice 1 shipped (captions). If translate-both-ways is
  not live for the reader's build yet, soften S6 to "captions everyone can read in
  their language" and never imply full two-way voice translation until it ships.
- Date voting: shipped (migration 0079).

## Render (after copy approval)
Build `slides.html` in this folder, then per the reddit-posters recipe:
```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
& $edge --headless=new --disable-gpu --hide-scrollbars `
  --force-device-scale-factor=2 --window-size=1080,1350 `
  --screenshot="out/ig/s1.png" "file:///<abs>/slides.html#s1"
# LinkedIn: rerun with --window-size=1080,1080 -> out/li/
```
