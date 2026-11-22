---
name: higgsfield-wanderbuddy
description: Produce WanderBuddy UGC ad videos through the Higgsfield MCP. Use when generating ad creative, character stills, motion clips, lipsync, or when working through marketing/HIGGSFIELD_15.md. Enforces credit discipline, the locked cast, the house look, and the standard outro.
---

# Higgsfield → WanderBuddy UGC

Drive the Higgsfield MCP to produce ad creative for WanderBuddy
(`com.wanderbuddy.wanderbuddy`, Android). Concepts live in
`marketing/HIGGSFIELD_15.md`. This file is the *how*.

To make this auto-load as a skill, copy it to
`.claude/skills/higgsfield-wanderbuddy/SKILL.md`.

---

## Step 0 — Discover the tools before calling anything

Higgsfield renames its endpoints. **Never assume a tool name.** At the start of
a session, list the MCP's tools and map them to these four jobs:

| Job | What to look for |
|---|---|
| **IMAGE** | text-to-image, "Soul", character/style reference input |
| **VIDEO** | image-to-video, takes an image + motion preset + duration |
| **SPEAK** | lipsync / talking avatar, takes an image + audio or text |
| **LIST** | presets, models, or styles enumeration |

If a `LIST` tool exists, call it once and cache the real preset names. The
motion names in this file are the common Higgsfield vocabulary, but use whatever
the API actually returns.

If no `SPEAK` tool exists, fall back to: generate a silent close-up with the
VIDEO tool and sync the recorded VO in the edit. Mouths out of sync at 5s in a
fast-cut edit is acceptable; paying for a dialogue-native video model is not.

---

## The credit rules (non-negotiable)

1. **Never text-to-video.** Always IMAGE first, approve, then VIDEO from that image.
2. **Never generate longer than 5 seconds.** Trim in the edit.
3. **Re-roll images freely, videos almost never.** Third failed video means the
   still is wrong. Go back to IMAGE.
4. **One native-audio generation per campaign, maximum.** Reserve it.
5. **The app is never generated.** Every product frame is a real screen
   recording from `marketing/app_capture/`. Zero credits, always correct.
6. **Batch to the slow/relaxed queue** if the plan offers one.
7. **Keep failures.** Warped hands and melted faces cut as 4-frame subliminal
   flashes in this house style. Save them to `graveyard/`.

Expected cost per concept: ~6 images, ~6 five-second videos, 0–3 lipsync.

---

## The house look

Append to **every** IMAGE prompt:

```
Shot on a phone by someone in the group. Direct on-camera flash, harsh falloff
into near-black, blown-out neon highlights in electric blue and sodium amber,
heavy grain, slight motion blur, 18mm wide, chromatic fringing, unflattering
honest angle, no makeup, nobody posing for the camera, candid mid-sentence
expression, 2003 point-and-shoot energy on a modern sensor.
```

Negative prompt, every time:

```
stock photo smile, studio lighting, travel influencer, drone postcard, perfect
skin, symmetrical composition, watermark, text, logo, sunset silhouette, group
jumping on beach, extra fingers, deformed hands
```

**Palette:** ink-navy `#0B141F` shadows · azure `#1E88D6` screen glow ·
sand-amber `#E0972A` streetlight · ocean-teal `#1FA89A` accents.
Source of truth is `lib/theme/app_colors.dart`. The README palette is stale.

**Aspect:** 9:16, 1080×1920. Always.

**Edit grammar:** hard cuts only, never a crossfade. Audio cuts one beat before
picture. Freeze-frame plus all-caps Roboto Condensed caption slams.

---

## The cast (generate once, reference forever)

Build all six as character references in the first session. Every later IMAGE
call passes the reference. This is what stops faces drifting between videos.

| Ref | Name | Prompt seed |
|---|---|---|
| `ref_maya` | **MAYA** | 28, Indian woman, half-shaved buzzcut, gold septum ring, forearm tattoos, oversized black band tee, tired eyes, unbothered |
| `ref_tobi` | **TOBI** | 31, German man, tall and narrow, wire-frame glasses, moustache, grey technical windbreaker, deadpan |
| `ref_ploy` | **PLOY** | 24, Thai woman, bleached mullet, oversized football jersey, layered silver chains, always mid-laugh |
| `ref_diego` | **DIEGO** | 26, Brazilian man, dense curly hair, white tank top, film camera on a strap, beaded bracelets, chaotic |
| `ref_nneka` | **NNEKA** | 30, Nigerian woman, braids in a high bun, large gold hoops, oversized linen shirt, the adult in the room |
| `ref_sam` | **SAM** | 22, American, red hair, heavy freckles, thrifted flannel, cheap digital camera, permanently overwhelmed |

Six people, six languages, one table. That setup is the entire reason
Live Conversation lands.

---

## Motion vocabulary

Use preset names, not prose. Prose camera descriptions fail and cost a re-roll.

`slow push in` · `crash zoom in` · `crash zoom out` · `whip pan` ·
`overhead descend` · `handheld follow` · `snorricam` · `slow orbit` ·
`slow pull back` · `static handheld drift` · `dolly zoom` · `bullet time`

Pick one per shot. Never stack two.

---

## VO and hyphenation

All VO is recorded human voice or TTS from the hyphenated lines in
`HIGGSFIELD_15.md`. Hyphens force correct syllable stress; feed the hyphenated
form to TTS, and use it as a read-guide if recording by voice.

**Standing pronunciation key:**

| Written | Say it |
|---|---|
| WanderBuddy | `Wan-der-Bud-dy` |
| itinerary | `eye-TIN-er-air-ee` |
| Nneka | `n-NEK-ah` |
| Diego | `dee-EH-go` |
| Tobi | `TOH-bee` |
| Ploy | `Ploy` (one beat, rhymes with "boy") |
| Phuket | `Poo-KET` |
| Oaxaca | `wa-HA-ka` |
| extradition | `ex-truh-DISH-un` |
| reconciliation | `rek-un-sil-ee-AY-shun` |
| synchronous | `SIN-kruh-nus` |

Rule: hyphenate anything three syllables or more, and anything a TTS engine
would plausibly get wrong. Leave short common words alone. `It's good` stays
`It's good`.

---

## The outro (identical on every video)

Rockstar cold-open structure. Three seconds. Never change it. Recognition comes
from repetition, so this is the one part of the brand that must never be
creative.

| Time | Picture | Sound |
|---|---|---|
| 0.0 – 1.2s | Last frame of the video, held, grading down to ink-navy | Ambient bed **at full volume**: airport tannoy garble, night-market clatter, train chime, distant traffic |
| 1.2s | **Cut to pure black** | **Total silence.** Hard cut, no fade |
| 1.2 – 1.9s | Black | Silence. Hold it longer than feels right |
| 1.9s | Logo snaps in, dead centre, white on ink-navy, no animation | **Deep sub-bass thump**, 45–55 Hz, short attack, long decay |
| 1.9 – 3.2s | Logo holds, 2px frame shake on the thump only | Sub-bass tail decaying to nothing |
| 3.2s | Play badge + link fade under logo | Silence |

**Siren variant** (use only on the safety and heist concepts): replace the
ambient bed with distant police sirens, wet-street reverb, radio chatter.
Everything after the cut is identical.

The silence is the whole effect. If you shorten the black, it stops working.

---

## The CTA (Android only for now)

Final card, under the logo, exactly this:

```
Android · Google Play
```

Link everywhere (bio, description, QR):

```
https://play.google.com/store/apps/details?id=com.wanderbuddy.wanderbuddy
```

**Do not mention iOS in any creative yet.** When the App Store listing goes
live, the card becomes `iOS · Android` and this file gets updated once.

---

## Structure every concept must follow

From the UGC planning checklist. Non-negotiable ordering.

| Beat | Timing | Job |
|---|---|---|
| **HOOK** | 0.0 – 3.0s | Stop the scroll. Speak directly at the viewer. Bold, unexpected, or uncomfortable. **Put the most effort here.** No hook means no attention means no installs. |
| **PROBLEM** | 3 – 8s | Name the pain they have already lived |
| **SOLUTION** | 8 – 20s | Real app footage. Product visibly in action. One idea per shot, nothing loaded |
| **CTA** | last 3s | The outro. Send them to Google Play |

Product demo footage must appear by 60% of the runtime at the latest.

---

## Working order for one concept

1. Read the concept block from `HIGGSFIELD_15.md`.
2. IMAGE every shot marked `IMG` (cast ref + shot prompt + house look + negative).
3. Show the stills. **Get approval before any VIDEO call.**
4. VIDEO each approved still, 5s, 9:16, one preset.
5. SPEAK for any shot with an on-camera spoken line.
6. Pull the matching clip from `marketing/app_capture/` for every `SCREEN` shot.
7. Assemble in CapCut. Burn captions. Append the outro.
8. Export 1080×1920, then crop 4:5 and 1:1.
9. Save generations to `marketing/output/higgsfield/<concept-slug>/`.

## Naming

```
marketing/output/higgsfield/<NN>-<slug>/
  stills/     shot-01.png …
  clips/      shot-01.mp4 …
  graveyard/  failed generations kept for subliminal cuts
  final/      <NN>-<slug>-9x16.mp4
```
