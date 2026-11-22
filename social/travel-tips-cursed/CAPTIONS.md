# 12 travel tips from a man who will not survive them: post copy

10 slides, which is what an Instagram carousel takes. The cover promises twelve tips
and the deck stops at eight, because he did not get to the rest. Slide 10 says so.

The bit only works if you post the whole thing in order and never break character in
the caption. Assets: `out/ig/` (1080x1350) and `out/tiktok/` (1080x1920). Upload in
filename order.

The straight version of this carousel lives in `../travel-tips-carousel/`. If this one
lands badly, that one is the fallback, not a rewrite of this one.

---

## The arc

| Slide | What is happening |
|---|---|
| 1 | Cover. Tells you up front the narrator is doomed. Promises twelve tips. |
| 2 to 5 | He is confident, authoritative, and completely insane. |
| 6 | The sentence starts eating itself. Type ghosts in red. |
| 7 | He has a stroke and is removed, on the same card. The counter gives up: `06 / --` |
| 8 to 9 | A stranger finishes the list and accidentally gets sincere. |
| 10 | The brand stops asking politely. Navy field, a gun pointed at the reader, the offer. |

Slide 9 is the one that makes this land instead of just being random. Do not cut it.

---

## Instagram caption

> We asked a very experienced traveller to write twelve tips for us.
>
> We are not going to comment on what happened after tip six. Legal has asked that we
> not comment on it. What we can say is that the remaining tips were completed by
> somebody else, that we did not hire that person, and that they have since stopped
> replying.
>
> Tips nine through twelve were not recovered.
>
> Slide 9 is real advice. The other seven are not. Please do not get in any vans.
>
> First 500 accounts get lifetime. Link in bio. Do not make us ask again.

**Hashtags** (first comment, not the caption):

```
#traveltips #travelhacks #grouptravel #travelplanning #tripplanning
#surrealhumor #unhingedmarketing #comedy #travelcommunity #wanderbuddy
```

**Pinned first comment**, once it starts moving:

> To the people asking: yes he is fine. To the people asking which one is fine: we
> would prefer not to narrow that down at this time.

---

## TikTok caption

> he made it to tip six
>
> #traveltips #unhinged #comedy #travelhacks #fyp

**On-screen text for the first frame**: `12 travel tips from a man who will not survive them`

**Sound**: something calm, warm and completely unbothered. Soft acoustic or lounge.
The joke is the gap between the sound and slide 7, so do not pick anything that
telegraphs comedy. Nothing dramatic, nothing with a drop.

**TikTok is not capped at ten.** If you want a longer cut there, three more tips are
sitting in the `reserve` array at the top of `build.mjs`: the Swiss train conductor,
the third Rome, and the ceramic frog. Give one a `file` and an `n`, drop it into
`slides`, and it renders like the rest.

---

## Comment replies, in character

Stay deadpan. Never explain the joke. Never break to say "haha just kidding".

- "is he okay" → "He is between countries."
- "what happened at tip 7" → "That information is with the family."
- "who is running this account" → "New management."
- "why not Bruges" → "I will not be elaborating and you will not be asking."
- "what were tips 9 to 12" → "Not recovered."
- "this is unhinged" → "Slide 9 stands."
- Anyone asking about the app → drop character entirely and answer straight. That is
  the actual conversion moment and a bit is not worth losing it.

---

## Risk, and the swaps if you want them

Slides 3 and 4 name sex work and drugs. Both are written as comedic list veers rather
than as the brand telling anyone to do anything, which is the version that survives a
moderation review. Slide 10 points a firearm at the reader. This account is attached to
a live App Store and Play listing, so know the trade before you post:

- **Organic reach is fine on Instagram.** None of it breaks community guidelines.
- **Slide 10 is the riskiest one, and TikTok is where it bites.** TikTok's dangerous
  acts and firearms policy is much broader than Meta's, and weapon imagery gets reach
  limited or age gated by classifier rather than by a human reading the joke. Meta's
  violence policy is narrower, but "we are done asking" next to a pointed gun is the
  exact shape an automated threat classifier looks for. Expect this slide, not slides
  3 or 4, to be the one that costs you distribution.
- **Paid is out entirely.** Do not put spend behind this carousel. Ad review rejects
  drugs, sex work and firearms even as jokes, and repeated rejections put the ad
  account at risk. Boost the straight carousel instead.
- **App store listings are separate** and unaffected. This is social only.

If TikTok suppresses it, the cheapest fix is to keep the carousel and swap slide 10 for
a version with no weapon. Set `cutout` to a different file in `build.mjs` and keep the
copy, or drop the `cutout` field entirely and the slide renders as type on navy, which
still lands because the previous nine slides did the work.

If you want the safer cut, these two are drop in replacements for the `head` and `body`
in `build.mjs`:

**Slide 3 (was: tip everyone)**
> tip everyone. and i do mean everyone
> The barman. The barber. The man who held the door of a building you did not enter
> and had no intention of entering. The sea. The sea has done nothing for you but it
> has been watching you all week and it knows.

**Slide 4 (was: the man on the beach)**
> fall in love with the man selling bracelets on the beach
> Do not buy anything. That is not what he is for. Sit down. Learn his mother's name.
> He has a boat, a scar, and no plans whatsoever. In eleven years you will think about
> him while loading a dishwasher in Leicester and you will have to sit down on the floor.

---

## Alt text, per slide

1. A traveller with a backpack pointing at something on a busy city street.
2. Two people knocking beer bottles together.
3. One hand passing banknotes to another over a table.
4. A man silhouetted against bright golden water at sunset.
5. A vendor and a customer at a covered street market stall.
6. Boarding passes and a passport on a desk.
7. Out of focus lights in the dark.
8. Old brick houses along a canal in Bruges under grey sky.
9. Two hikers with backpacks looking out over a mountain lake.
10. A hand pointing a pistol at the viewer against a dark blue background, with the words we are done asking.
