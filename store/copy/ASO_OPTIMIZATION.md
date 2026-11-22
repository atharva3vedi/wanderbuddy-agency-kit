# WanderBuddy — App Store & Play Store Optimization

Store conversion is the cheapest lever you own. A better listing does not cost a
single view; it just turns more of the views you already have into installs. This
doc audits both listings and gives you paste-ready fixes, ranked by leverage.

Sources of truth: `APP_STORE_LISTING.md` (iOS, current and strong),
`STORE_LISTING.md` (Play, **stale**), `APP_STORE_CHECKLIST.md` (console gates).

---

## 1. Audit — where each listing stands

| Element | iOS | Play | Verdict |
| --- | --- | --- | --- |
| App name / title | `WanderBuddy: Group Trips` (carries the valuable term) | `WanderBuddy: Travel Together` (spends the slot on brand) | **Change Play** → put the searched term in it |
| Subtitle / short desc | `Group trip planner & expenses` (indexed, sharp) | `Plan group trips together: itinerary, chat, AI plans, safety & visa help` | Play OK, tighten (below) |
| Keyword field | Full 100 chars, well-chosen | Play has no keyword field (indexes title+descriptions) | Weave terms into Play copy (§4) |
| Full description | Feature-complete, on-voice, includes Trip Vibe + Live Conversation + Community | **Missing all three** of those | **Rewrite Play** (§3) |
| Preview video | None (skipped) | None | **Ship one** — `ugc-autocut` makes it (§5) |
| Screenshots | 10 shots, panorama split, strong | 8-shot plan, older | Regenerate Play set to match |
| Promo/what's-new | Rotating promo text, good | Static | Rotate it (§6) |
| Localization | English only | English only | **Biggest untapped lever** (§7) |

**The single highest-leverage fix:** the Play full description is missing your
three least-copyable features. Live Conversation, Trip Vibe, and Community are the
reasons someone chooses you over the incumbent, and a Play visitor never sees
them. Fix §3 first.

---

## 2. Titles & short text (paste-ready)

### Play — App name (max 30)
```
WanderBuddy: Group Trips
```
(24 chars.) Play indexes the title heavily for search, and "Group Trips" is your
most valuable searched phrase. If you would rather keep the warmer brand line,
`WanderBuddy: Travel Together` (28) is the fallback, but you are trading a ranking
for a feeling. Recommended: take the term.

### Play — Short description (max 80)
```
Plan group trips with friends: shared itinerary, chat, expenses, AI & safety.
```
(77 chars.) This field is indexed and shown high on the page. Every word here is a
search term: *group trips, friends, itinerary, chat, expenses, AI, safety.*

Alternates:
- `Group trip planner: itinerary, split expenses, group chat, AI plans & visas.` (76)
- `One app for group travel: plan, chat, split costs, translate & stay safe.` (73)

### iOS — leave name/subtitle/keywords as they are
They are already optimized in `APP_STORE_LISTING.md`. The only iOS moves are the
preview video (§5) and rotating promo text (§6).

---

## 3. Play — full description (paste-ready rewrite)

Play *does* index the full description, so this version keeps the strong voice of
the iOS copy but weaves the searched terms in naturally, and it adds the three
missing features. Google may be named on Play (unlike iOS), so the transparency
line keeps "Google's cut."

```
Nobody remembers the itinerary. Everybody remembers the night it fell apart.

WanderBuddy is the one app for planning a group trip with friends, and for keeping
everyone in sync once you land. Put the itinerary, the group chat, the money and
the map in one place, instead of five apps and a screenshot of a flight nobody can
find again.

THE GROUP CHAT IS NOT A PLAN
A shared itinerary the whole group edits in real time. Group chat, so plans stop
scattering. Everyone sees the same days. No more "wait, are we still doing the
temple thing".

TELL IT THE VIBE, NOT THE SCHEDULE
Your AI travel planner: say five days, cheap, hot, walkable, no museums, and it
writes the days around whatever you have already booked. Add the whole plan to
your trip in one tap.

EVERY TRIP HAS A PERSONALITY. NOW IT HAS A SCORE.
Trip Vibe rates a trip on nature, culture, nightlife, adventure and local food.
Two people can fly to the same city and come home from completely different trips.
Find out which one you are actually booking.

TALK WITHOUT MAKING EVERYONE SWITCH TO ENGLISH
Live Conversation: everyone speaks their own language out loud, and each person
reads the room in theirs, live. Nobody gets demoted to the quiet one. Plus a
translate tool for menus, signs, and the pharmacy conversation you were dreading.

MONEY, SETTLED BEFORE ANYONE FLIES HOME
Split expenses evenly, by share, or by the exact amount, because one of you had
the lobster. Who owes what sits on one screen.

FIND PEOPLE, OR BRING YOUR OWN
Browse public trips with the spots left showing, and join with a link or a QR
code. Or start a private one. You approve everyone who gets in.

FOR WHEN IT GOES WRONG, BECAUSE IT WILL
The local emergency number wherever you are, your embassy, your exact coordinates
ready to send, and a checklist for the morning your phone or wallet stops
existing.
(Safety tools help you move fast. Always follow local authorities.)

VISAS, WITHOUT THE FORUM RABBIT HOLE
Check entry requirements for any passport and any destination, with a link to the
actual immigration page instead of a nine-year-old forum thread.
(Guidance only. Confirm with the official source before you fly.)

LOCATION IS NOT ON BY DEFAULT
Nobody sees where you are until you say so. Both people agree, it runs out on a
timer, and you can switch it off mid-trip.

WHAT WE WON'T DO
No ads. No trackers. Your data is not for sale. Every paid feature shows you the
arithmetic: Google's cut, the API bill, and what is left for the developer. The
free app is the whole app. Paid extras buy room, never permission.

A weekend or three months. Two of you or eleven. WanderBuddy is the part of the
trip nobody wants to volunteer for.

Questions or feedback? Reach us any time from inside the app.
```
(≈2,400 chars, well under the 4,000 cap. Room to add a localized block per §7.)

### Play — What's new (max 500)
```
- Live Conversation: everyone speaks their own language out loud and reads the room in theirs, live.
- Trip Vibe: every trip scored on nature, culture, nightlife, adventure and local food.
- Community: find public trips, see the spots left, and join with a link or QR code.
- Entry requirements checker for any passport and destination, with official links.
- Fresh look with System / Light / Dark themes and reorderable tabs.
```

---

## 4. Play keyword strategy (there is no keyword field)

Play builds your ranking from the **title + short description + full description**,
so keywords are woven, not listed. The rewrite in §3 already covers the core set.
Make sure these terms each appear at least once in the copy, naturally:

`group trip · trip planner · group travel · itinerary · split expenses · group
chat · AI travel planner · travel with friends · visa · entry requirements ·
travel safety · translate · backpacking · road trip`

Do not keyword-stuff. Google penalizes it and it reads badly. Once each,
naturally, is the whole game. Revisit after 30 days using Play Console's search
term acquisition report.

---

## 5. The preview video (both stores) — you already have the tool

Neither store has a video yet. This is a real conversion lever (a preview can lift
store-view→install meaningfully) and you now produce it for free.

- **Asset:** the `ugc-autocut` output, 15-30s, vertical. Best base is the feature
  walkthrough or the Live Conversation hero.
- **iOS App Preview:** 15-30s, must be captured/rendered UI (Apple is strict:
  mostly real app footage, minimal outside-the-app framing). Use the screen
  recordings as the spine; keep AI-human b-roll to a few seconds. Sits before the
  screenshots.
- **Play promo video:** more permissive; a YouTube link. The full UGC hero works.
- **Opener:** the beach-to-logo match-cut (`logo-transition/SPEC.md`) is a perfect
  2-second intro for the Play version. For the iOS App Preview, lead with real UI
  instead to stay inside Apple's "show the app" rule, and save the logo intro for
  the social cuts.

---

## 6. iOS promotional text — rotate it, no build required

The one text field you can change without shipping a build. Treat it as the
"what's hot" slot. Rotation library (all under the 170 cap) is already in
`APP_STORE_LISTING.md`. Cadence: swap it whenever a campaign changes or a feature
lands. Current recommended default is the Live Conversation line.

---

## 7. Localization — the biggest untapped ASO lever

You have localization in progress (en/hi/es/fr/de/zh/ar/th). **Every localized
store listing is a separate search surface in a separate market**, and your
beachhead is India → SEA. Priorities:

1. **Hindi + Thai first** (the beachhead). Localize the Play title's subtitle
   portion, the short description, and the first three lines of the full
   description at minimum. This alone opens two large, under-competed store search
   markets.
2. **Spanish** (LatAm + Spain) next — large, travel-heavy.
3. The listing localizations do **not** need the whole app localized to ship;
   Play and App Store Connect take per-locale metadata independently. Do the store
   copy now, ahead of the in-app localization finishing.

This is close to free reach and almost nobody in the category bothers.

---

## 8. Ratings & reviews — the invisible ranking factor

Rating is one of the strongest store-ranking and conversion inputs. A 4.6★ page
converts far better than a 4.1★ page at the same traffic.

- **Prompt at the peak, not at launch.** Trigger the native in-app review prompt
  after a *good* moment: a trip successfully created, an itinerary generated, a
  first expense settled. Never on first open.
- **Never prompt an angry user.** Gate the prompt behind a lightweight "enjoying
  WanderBuddy?" — happy → store prompt, unhappy → in-app feedback form. (Confirm
  the app has an `in_app_review` path; if not, it is a small, high-ROI add.)
- **Seed honestly.** Ask your 500 founders directly, in-app, once they have a real
  trip. Real users, real reviews.

---

## 9. Do-this-week checklist

- [ ] Change Play app name to `WanderBuddy: Group Trips`.
- [ ] Replace Play short description (§2) and full description (§3).
- [ ] Update Play "What's new" (§3).
- [ ] Render a 15-30s preview from `ugc-autocut`; upload iOS App Preview + Play
      promo video.
- [ ] Set iOS promo text to the Live Conversation line.
- [ ] Localize Play + App Store metadata for Hindi and Thai (§7).
- [ ] Wire the in-app review prompt to a peak moment (§8).
- [ ] Point every bio/QR at one short link on your domain for click data.

Every item on this list is free and most are a copy-paste. Do them before you
spend one minute worrying about reach.
```
